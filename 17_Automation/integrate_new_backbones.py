"""Unpack EXP0007 & EXP0008 Kaggle result bundles, compute paired statistics, unify cross-dataset tables, and run K=3 M1-M18 fusion."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import zipfile
from math import comb, sqrt
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def roc_auc_fast(y_true: np.ndarray, y_score: np.ndarray) -> float:
    order = np.argsort(y_score)
    y = y_true[order]
    n_pos = int(y.sum())
    n_neg = len(y) - n_pos
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    ranks = np.arange(1, len(y) + 1, dtype=np.float64)
    _, inv, counts = np.unique(y_score[order], return_inverse=True, return_counts=True)
    if np.any(counts > 1):
        sums = np.bincount(inv, weights=ranks)
        ranks = (sums / counts)[inv]
    pos_ranks = ranks[y == 1].sum()
    return float((pos_ranks - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg))


def balanced_acc_fast(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    pos = y_true == 1
    neg = y_true == 0
    tpr = float((y_pred[pos] == 1).mean())
    tnr = float((y_pred[neg] == 0).mean())
    return 0.5 * (tpr + tnr)


def mcc_fast(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    tp = float(((y_true == 1) & (y_pred == 1)).sum())
    tn = float(((y_true == 0) & (y_pred == 0)).sum())
    fp = float(((y_true == 0) & (y_pred == 1)).sum())
    fn = float(((y_true == 1) & (y_pred == 0)).sum())
    denom = sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    return 0.0 if denom == 0.0 else float((tp * tn - fp * fn) / denom)


def mcnemar_exact_two_sided(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    # Use log2 / float safely for large n
    if n > 1000:
        z = (abs(b - c) - 1.0) / sqrt(n)
        from math import erfc
        return min(1.0, erfc(z / sqrt(2.0)))
    p_one = sum(comb(n, i) * (0.5 ** n) for i in range(k + 1))
    return min(1.0, 2.0 * p_one)


def unpack_bundle(zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.namelist():
            if member.endswith("/") or ".." in member:
                continue
            dest = ROOT / member
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(zf.read(member))
    print(f"Unpacked {zip_path} into {ROOT}")


def compute_backbone_statistics() -> None:
    specs = [
        ("EXP0001", "MODEL0001", "ResNet-50"),
        ("EXP0007", "MODEL0003", "EfficientNet-B4"),
        ("EXP0008", "MODEL0004", "ViT-B/16"),
    ]
    data: dict[str, dict[str, tuple[int, float, int]]] = {}
    for exp_id, _, _ in specs:
        pred_csv = ROOT / "06_Experiments" / exp_id / "predictions/test_predictions.csv"
        if not pred_csv.is_file():
            raise FileNotFoundError(f"Missing {pred_csv}")
        by_h: dict[str, tuple[int, float, int]] = {}
        with pred_csv.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                yt = 1 if r["class_label"] == "fake" else 0
                by_h[r["content_hash"]] = (yt, float(r["prob_positive"]), int(r["pred_positive"]))
        data[exp_id] = by_h

    hashes = sorted(data["EXP0001"])
    yt = np.array([data["EXP0001"][h][0] for h in hashes], dtype=np.int32)
    n = len(yt)
    rng = np.random.default_rng(49)
    n_boot = 10000
    boot_idx = rng.integers(0, n, size=(n_boot, n))

    # 1. Per-backbone bootstrap CIs
    ci_rows: list[dict] = []
    arrays: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for exp_id, model_id, arch in specs:
        p = np.array([data[exp_id][h][1] for h in hashes], dtype=np.float64)
        yp = np.array([data[exp_id][h][2] for h in hashes], dtype=np.int32)
        arrays[exp_id] = (p, yp)

        aucs = np.empty(n_boot, dtype=np.float64)
        bas = np.empty(n_boot, dtype=np.float64)
        mccs = np.empty(n_boot, dtype=np.float64)
        for i in range(n_boot):
            idx = boot_idx[i]
            aucs[i] = roc_auc_fast(yt[idx], p[idx])
            bas[i] = balanced_acc_fast(yt[idx], yp[idx])
            mccs[i] = mcc_fast(yt[idx], yp[idx])

        for metric_name, pt, dist in [
            ("roc_auc", roc_auc_fast(yt, p), aucs),
            ("balanced_accuracy", balanced_acc_fast(yt, yp), bas),
            ("mcc", mcc_fast(yt, yp), mccs),
        ]:
            ci_rows.append({
                "experiment_id": exp_id,
                "model_id": model_id,
                "architecture": arch,
                "metric": metric_name,
                "point_estimate": round(pt, 6),
                "ci_95_low": round(float(np.percentile(dist, 2.5)), 6),
                "ci_95_high": round(float(np.percentile(dist, 97.5)), 6),
                "n_resamples": n_boot,
            })

    ci_out = ROOT / "08_Evaluation/statistics/backbone_bootstrap_cis.csv"
    with ci_out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(ci_rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(ci_rows)
    print(f"Wrote {ci_out} ({len(ci_rows)} rows)")

    # 2. All-pairs paired bootstrap + exact McNemar
    pairs = [
        ("EXP0008", "ViT-B/16", "EXP0001", "ResNet-50"),
        ("EXP0007", "EfficientNet-B4", "EXP0001", "ResNet-50"),
        ("EXP0008", "ViT-B/16", "EXP0007", "EfficientNet-B4"),
    ]
    pair_rows: list[dict] = []
    for exp_a, arch_a, exp_b, arch_b in pairs:
        pa, ypa = arrays[exp_a]
        pb, ypb = arrays[exp_b]
        auc_a, auc_b = roc_auc_fast(yt, pa), roc_auc_fast(yt, pb)
        ba_a, ba_b = balanced_acc_fast(yt, ypa), balanced_acc_fast(yt, ypb)

        d_auc = np.empty(n_boot, dtype=np.float64)
        d_ba = np.empty(n_boot, dtype=np.float64)
        for i in range(n_boot):
            idx = boot_idx[i]
            d_auc[i] = roc_auc_fast(yt[idx], pa[idx]) - roc_auc_fast(yt[idx], pb[idx])
            d_ba[i] = balanced_acc_fast(yt[idx], ypa[idx]) - balanced_acc_fast(yt[idx], ypb[idx])

        b_cnt = int(((ypb == yt) & (ypa != yt)).sum())
        c_cnt = int(((ypb != yt) & (ypa == yt)).sum())
        p_mcn = mcnemar_exact_two_sided(b_cnt, c_cnt)

        row = {
            "challenger_exp": exp_a,
            "challenger_arch": arch_a,
            "reference_exp": exp_b,
            "reference_arch": arch_b,
            "delta_roc_auc": round(auc_a - auc_b, 6),
            "delta_roc_auc_ci_low": round(float(np.percentile(d_auc, 2.5)), 6),
            "delta_roc_auc_ci_high": round(float(np.percentile(d_auc, 97.5)), 6),
            "delta_bal_acc": round(ba_a - ba_b, 6),
            "delta_bal_acc_ci_low": round(float(np.percentile(d_ba, 2.5)), 6),
            "delta_bal_acc_ci_high": round(float(np.percentile(d_ba, 97.5)), 6),
            "mcnemar_ref_right_chal_wrong": b_cnt,
            "mcnemar_ref_wrong_chal_right": c_cnt,
            "mcnemar_p_two_sided": p_mcn,
        }
        pair_rows.append(row)
        print("Paired test:", json.dumps(row, indent=2))

    pair_out = ROOT / "08_Evaluation/statistics/backbone_paired_tests.csv"
    with pair_out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(pair_rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(pair_rows)
    print(f"Wrote {pair_out}")

    # 3. Unified cross-dataset generalization table across DS0001-DS0005
    gen_sources = [
        ("EXP0001", "MODEL0001", "ResNet-50", "EVAL0001"),
        ("EXP0007", "MODEL0003", "EfficientNet-B4", "EVAL0009"),
        ("EXP0008", "MODEL0004", "ViT-B/16", "EVAL0010"),
    ]
    unified: list[dict] = []
    for exp_id, model_id, arch, eval_id in gen_sources:
        cd_csv = ROOT / "08_Evaluation" / eval_id / "generalization/cross_dataset_metrics.csv"
        with cd_csv.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                unified.append({
                    "experiment_id": exp_id,
                    "model_id": model_id,
                    "architecture": arch,
                    "evaluation_id": eval_id,
                    **r,
                })
    uni_out = ROOT / "08_Evaluation/cross_backbone_generalization.csv"
    with uni_out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(unified[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(unified)
    print(f"Wrote {uni_out} ({len(unified)} rows)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundles", nargs="*", type=Path, help="Paths to EXP0007/EXP0008_results_bundle.zip")
    args = parser.parse_args()
    for zp in args.bundles:
        if zp.is_file():
            unpack_bundle(zp)
    compute_backbone_statistics()
    subprocess.run(
        [sys.executable, str(ROOT / "11_AI_Forensic_System/evaluate_benchmark_abstention.py"), "--multi-specialist"],
        check=True,
    )


if __name__ == "__main__":
    main()
