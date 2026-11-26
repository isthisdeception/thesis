"""EVAL0008 — Large-scale quantitative evaluation of M1-M18 abstention & selective risk-coverage.

Executes the end-to-end 18-module AI Forensic Analyst pipeline across 2,700 real benchmark cases
spanning 9 evaluation tracks (300 stratified images per track):
  1. DS0001_clean         : ArtiFact test (150 real, 150 fake)
  2. DS0001_jpeg10        : Severe JPEG recompression Q=10 (150 real, 150 fake)
  3. DS0001_blur3         : Gaussian blur radius=3.0 (150 real, 150 fake)
  4. DS0001_noise01       : Additive Gaussian noise sigma=0.10 (150 real, 150 fake)
  5. DS0001_downscale025  : Spatial downscaling 0.25x -> 224px (150 real, 150 fake)
  6. DS0002_diff          : Unseen diffusion faces on DiFF official test (300 fake across 12 DMs)
  7. DS0003_140k          : External StyleGAN & FFHQ on 140k Faces (150 real, 150 fake)
  8. DS0004_synthbuster   : External commercial diffusion & RAISE DSLR (150 real, 150 fake)
  9. DS0005_fairface      : External demographic authentic faces on FairFace (300 real)

Compares standalone binary detectors (MODEL0001 ResNet-50, MODEL0003 EfficientNet-B4,
MODEL0004 ViT-B/16), single-specialist M1-M18 governance (K=1), and cross-paradigm
multi-specialist M1-M18 fusion + governance (K=3).
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import io
import json
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
SYS_DIR = Path(__file__).resolve().parent
AUTO_DIR = REPO_ROOT / "17_Automation"
for p in (SYS_DIR, AUTO_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from audit import HEADER as CASE_HEADER
from evidence.collectors.deep_learning_specialist import DeepLearningCollector
from evidence.collectors.deep_learning_specialist.fastai_export import Inference
from evidence.registry import HEADER as EV_HEADER
from evidence.validation import ValidationConfig as EvidenceValidationConfig
from image_validation import ValidationConfig as ImageValidationConfig
from pipeline import run_investigation
from reports import VersionStamps
from robustness.perturbations import apply as apply_perturbation
from robustness.perturbations import image_seed

OUT_DIR = REPO_ROOT / "08_Evaluation" / "EVAL0008"
FROZEN_T_M1 = 0.3950566053390503
FROZEN_T_M3 = 0.516065776348114
FROZEN_T_M4 = 0.4906201958656311


class _SingleFaceCounter:
    def count_faces(self, image: Image.Image) -> int:
        return 1


class _SavedPredictor:
    def __init__(self, prob: float) -> None:
        self.prob = float(prob)

    def predict(self, image: Image.Image) -> Inference:
        return Inference(fake_probability=self.prob, embedding=[0.0], model_confidence=None)


def _encode_png(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _load_extra_model_maps() -> dict[str, dict[str, float]]:
    """Load comparator predictions (EXP0007 MODEL0003, EXP0008 MODEL0004) across DS0001-DS0005."""
    extras: dict[str, dict[str, float]] = {}
    candidates = [
        ("MODEL0003", "EXP0007", "EVAL0009"),
        ("MODEL0004", "EXP0008", "EVAL0010"),
    ]
    for model_id, exp_id, eval_id in candidates:
        test_csv = REPO_ROOT / "06_Experiments" / exp_id / "predictions" / "test_predictions.csv"
        if not test_csv.is_file():
            continue
        prob_by_key: dict[str, float] = {}
        with test_csv.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                prob_by_key[f"DS0001:{r['content_hash']}"] = float(r["prob_positive"])
        for ds in ("DS0002", "DS0003", "DS0004", "DS0005"):
            g_csv = REPO_ROOT / "08_Evaluation" / eval_id / "generalization" / "predictions" / f"{ds}.csv"
            if g_csv.is_file():
                with g_csv.open(encoding="utf-8") as f:
                    for r in csv.DictReader(f):
                        prob_by_key[f"{ds}:{r['id']}"] = float(r["y_prob"])
        extras[model_id] = prob_by_key
    return extras


def build_cases(per_track: int = 300, seed: int = 42) -> list[dict]:
    rng = np.random.default_rng(seed)
    half = per_track // 2

    ds1_rows: list[dict] = []
    with (REPO_ROOT / "06_Experiments/EXP0001/predictions/test_predictions.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ds1_rows.append(r)

    rob_by_hash: dict[str, dict[str, str]] = {}
    with (REPO_ROOT / "08_Evaluation/EVAL0001/robustness/robustness_probs.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rob_by_hash[r["id"]] = r

    reals = [r for r in ds1_rows if r["class_label"] == "real" and r["content_hash"] in rob_by_hash]
    fakes = [r for r in ds1_rows if r["class_label"] == "fake" and r["content_hash"] in rob_by_hash]
    sel_real = [reals[i] for i in sorted(rng.choice(len(reals), size=half, replace=False))]
    sel_fake = [fakes[i] for i in sorted(rng.choice(len(fakes), size=half, replace=False))]
    sel_ds1 = sel_real + sel_fake

    cases: list[dict] = []
    ds1_root = REPO_ROOT / "_processed_dataset/processed_DS0001_PP0001"

    track_specs = [
        ("DS0001_clean", "clean", "clean", None, "clean"),
        ("DS0001_jpeg10", "jpeg@10", "jpeg", 10, "jpeg@10"),
        ("DS0001_blur3", "gaussian_blur@3", "gaussian_blur", 3.0, "gaussian_blur@3"),
        ("DS0001_noise01", "gaussian_noise@0.1", "gaussian_noise", 0.1, "gaussian_noise@0.1"),
        ("DS0001_downscale025", "resolution@0.25", "resolution", 0.25, "resolution@0.25"),
    ]
    for track_id, cond_id, kind, level, prob_col in track_specs:
        for r in sel_ds1:
            ch = r["content_hash"]
            prob = float(r["prob_positive"]) if prob_col == "clean" else float(rob_by_hash[ch][prob_col])
            cases.append({
                "track": track_id,
                "dataset": "DS0001",
                "key": f"DS0001:{ch}",
                "content_hash": ch,
                "img_path": str(ds1_root / r["processed_path"]),
                "pert_id": cond_id,
                "pert_kind": kind,
                "pert_level": level,
                "y_true": 1 if r["class_label"] == "fake" else 0,
                "prob_m1": prob,
            })

    # Track 6: DS0002 DiFF (300 unseen diffusion portraits)
    ds2_root = REPO_ROOT / "_processed_dataset/processed_DS0002_PP0002"
    ds2_rows = []
    with (REPO_ROOT / "08_Evaluation/EVAL0001/generalization/predictions/DS0002.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ds2_rows.append(r)
    for i in sorted(rng.choice(len(ds2_rows), size=per_track, replace=False)):
        r = ds2_rows[i]
        cases.append({
            "track": "DS0002_diff",
            "dataset": "DS0002",
            "key": f"DS0002:{r['id']}",
            "content_hash": r["content_hash"],
            "img_path": str(ds2_root / r["id"]),
            "pert_id": "clean",
            "pert_kind": "clean",
            "pert_level": None,
            "y_true": 1,
            "prob_m1": float(r["y_prob"]),
        })

    # Track 7: DS0003 140k Faces (150 real + 150 fake)
    ds3_root = REPO_ROOT / "_processed_dataset/processed_DS0003_PP0003"
    ds3_r, ds3_f = [], []
    with (REPO_ROOT / "08_Evaluation/EVAL0001/generalization/predictions/DS0003.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            (ds3_f if int(r["y_true"]) == 1 else ds3_r).append(r)
    sel_ds3 = [ds3_r[i] for i in sorted(rng.choice(len(ds3_r), size=half, replace=False))] + [
        ds3_f[i] for i in sorted(rng.choice(len(ds3_f), size=half, replace=False))
    ]
    for r in sel_ds3:
        cases.append({
            "track": "DS0003_140k",
            "dataset": "DS0003",
            "key": f"DS0003:{r['id']}",
            "content_hash": r["content_hash"],
            "img_path": str(ds3_root / r["id"]),
            "pert_id": "clean",
            "pert_kind": "clean",
            "pert_level": None,
            "y_true": int(r["y_true"]),
            "prob_m1": float(r["y_prob"]),
        })

    # Track 8: DS0005 FairFace (300 authentic portraits) — seeded before DS0004 to preserve exact RNG stream!
    ds5_root = REPO_ROOT / "_processed_dataset/processed_DS0005_PP0005"
    ds5_rows = []
    with (REPO_ROOT / "08_Evaluation/EVAL0001/generalization/predictions/DS0005.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ds5_rows.append(r)
    for i in sorted(rng.choice(len(ds5_rows), size=per_track, replace=False)):
        r = ds5_rows[i]
        cases.append({
            "track": "DS0005_fairface",
            "dataset": "DS0005",
            "key": f"DS0005:{r['id']}",
            "content_hash": r["content_hash"],
            "img_path": str(ds5_root / r["id"]),
            "pert_id": "clean",
            "pert_kind": "clean",
            "pert_level": None,
            "y_true": 0,
            "prob_m1": float(r["y_prob"]),
        })

    # Track 9: DS0004 Synthbuster (150 real RAISE DSLR + 150 synthetic commercial diffusion)
    ds4_root = REPO_ROOT / "_processed_dataset/DS0004_PP0006/DS0004_PP0006"
    ds4_r, ds4_f = [], []
    with (REPO_ROOT / "08_Evaluation/EVAL0001/generalization/predictions/DS0004.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            (ds4_f if int(r["y_true"]) == 1 else ds4_r).append(r)
    n_r4 = min(half, len(ds4_r))
    sel_ds4 = [ds4_r[i] for i in sorted(rng.choice(len(ds4_r), size=n_r4, replace=False))] + [
        ds4_f[i] for i in sorted(rng.choice(len(ds4_f), size=per_track - n_r4, replace=False))
    ]
    for r in sel_ds4:
        cases.append({
            "track": "DS0004_synthbuster",
            "dataset": "DS0004",
            "key": f"DS0004:{r['id']}",
            "content_hash": r["content_hash"],
            "img_path": str(ds4_root / r["id"]),
            "pert_id": "clean",
            "pert_kind": "clean",
            "pert_level": None,
            "y_true": int(r["y_true"]),
            "prob_m1": float(r["y_prob"]),
        })

    return cases


def _worker_chunk(chunk: list[dict]) -> list[dict]:
    ev_cfg = EvidenceValidationConfig.calibrated_artifact_val()
    img_cfg = ImageValidationConfig(max_noise_stddev=95.0)
    face_counter = _SingleFaceCounter()
    stamps = VersionStamps(
        system_version="0.2.0",
        model_id="MODEL0001",
        model_version="1.0",
        dataset_id="DS0001/v1.0/PP0001",
        experiment_id="EXP0001",
        git_commit="004fba1",
    )
    out_rows: list[dict] = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for idx, c in enumerate(chunk):
            img = Image.open(c["img_path"]).convert("RGB")
            if c["pert_kind"] != "clean":
                img = apply_perturbation(
                    c["pert_kind"],
                    img,
                    c["pert_level"],
                    image_seed(42, c["pert_id"], c["content_hash"]),
                )
                if img.size != (224, 224):
                    img = img.resize((224, 224), Image.Resampling.BILINEAR)
            png_bytes = _encode_png(img)

            def _run_one(tag: str, extras: list[tuple[str, float]]):
                case_dir = root / f"c_{idx}_{tag}"
                case_dir.mkdir(parents=True, exist_ok=True)
                ev_path = case_dir / "evidence_registry.csv"
                ev_path.write_text(",".join(EV_HEADER) + "\n", encoding="utf-8")
                case_path = case_dir / "case_registry.csv"
                case_path.write_text(",".join(CASE_HEADER) + "\n", encoding="utf-8")
                extra_cols = [
                    DeepLearningCollector(m_id, repo=REPO_ROOT, predictor=_SavedPredictor(m_prob))
                    for m_id, m_prob in extras
                ]
                return run_investigation(
                    filename="input.png",
                    data=png_bytes,
                    storage_root=case_dir / "storage",
                    evidence_registry_path=ev_path,
                    case_registry_path=case_path,
                    face_counter=face_counter,
                    case_id=f"CASE{idx + 1:06d}",
                    model_id="MODEL0001",
                    predictor=_SavedPredictor(c["prob_m1"]),
                    extra_collectors=extra_cols or None,
                    image_validation_config=img_cfg,
                    evidence_validation_config=ev_cfg,
                    version_stamps=stamps,
                    repo_root=REPO_ROOT,
                )

            res_k1 = _run_one("k1", [])
            extra_list = c.get("extra_probs", [])
            res_k3 = _run_one("k3", extra_list) if extra_list else res_k1

            dec_k1 = res_k1.decision.record.decision if res_k1.decision and res_k1.decision.record else "Halted"
            conf_k1 = res_k1.confidence.output if res_k1.confidence and res_k1.confidence.output else None

            dec_k3 = res_k3.decision.record.decision if res_k3.decision and res_k3.decision.record else "Halted"
            conf_k3 = res_k3.confidence.output if res_k3.confidence and res_k3.confidence.output else None

            p_m3 = c.get("prob_m3")
            p_m4 = c.get("prob_m4")
            out_rows.append({
                "track": c["track"],
                "dataset": c["dataset"],
                "y_true": c["y_true"],
                "prob_m1": round(c["prob_m1"], 6),
                "prob_m3": "" if p_m3 is None else round(p_m3, 6),
                "prob_m4": "" if p_m4 is None else round(p_m4, 6),
                "standalone_pred_m1": 1 if c["prob_m1"] >= FROZEN_T_M1 else 0,
                "standalone_pred_m3": "" if p_m3 is None else (1 if p_m3 >= FROZEN_T_M3 else 0),
                "standalone_pred_m4": "" if p_m4 is None else (1 if p_m4 >= FROZEN_T_M4 else 0),
                "k1_decision": dec_k1,
                "k1_c_ev": None if not conf_k1 or conf_k1.evidence_confidence is None else round(conf_k1.evidence_confidence, 6),
                "k1_c_dec": None if not conf_k1 or conf_k1.decision_confidence is None else round(conf_k1.decision_confidence, 6),
                "platform_status": res_k3.status,
                "platform_decision": dec_k3,
                "c_pred": None if not conf_k3 or conf_k3.prediction_confidence is None else round(conf_k3.prediction_confidence, 6),
                "c_ev": None if not conf_k3 or conf_k3.evidence_confidence is None else round(conf_k3.evidence_confidence, 6),
                "c_sys": None if not conf_k3 or conf_k3.system_confidence is None else round(conf_k3.system_confidence, 6),
                "c_dec": None if not conf_k3 or conf_k3.decision_confidence is None else round(conf_k3.decision_confidence, 6),
                "specialists_used": 1 + len(extra_list),
                "latency_ms": round(res_k3.execution_time_seconds * 1000.0, 2),
            })
    return out_rows


def summarize_tracks(rows: list[dict], decision_col: str = "platform_decision") -> list[dict]:
    tracks_order = [
        "DS0001_clean",
        "DS0001_jpeg10",
        "DS0001_blur3",
        "DS0001_noise01",
        "DS0001_downscale025",
        "DS0002_diff",
        "DS0003_140k",
        "DS0004_synthbuster",
        "DS0005_fairface",
    ]
    summaries: list[dict] = []
    for tr in tracks_order:
        sub = [r for r in rows if r["track"] == tr]
        if not sub:
            continue
        n = len(sub)
        n_real = sum(1 for r in sub if r["y_true"] == 0)
        n_fake = sum(1 for r in sub if r["y_true"] == 1)

        st_m1_err = sum(1 for r in sub if r["standalone_pred_m1"] != r["y_true"])
        st_m1_fp = sum(1 for r in sub if r["y_true"] == 0 and r["standalone_pred_m1"] == 1)
        st_m1_fn = sum(1 for r in sub if r["y_true"] == 1 and r["standalone_pred_m1"] == 0)

        has_m3 = all(r["standalone_pred_m3"] != "" for r in sub)
        has_m4 = all(r["standalone_pred_m4"] != "" for r in sub)
        st_m3_err = sum(1 for r in sub if int(r["standalone_pred_m3"]) != r["y_true"]) if has_m3 else None
        st_m4_err = sum(1 for r in sub if int(r["standalone_pred_m4"]) != r["y_true"]) if has_m4 else None

        # K=1 baseline governance
        k1_dec = [r for r in sub if r["k1_decision"] in ("Fake", "Real")]
        k1_wrong = sum(
            1 for r in k1_dec
            if (r["k1_decision"] == "Fake" and r["y_true"] == 0)
            or (r["k1_decision"] == "Real" and r["y_true"] == 1)
        )

        # Primary (K=3 on clean / K=1 on perturbed, or K=1 if decision_col=="k1_decision")
        decided = [r for r in sub if r[decision_col] in ("Fake", "Real")]
        abstained = [r for r in sub if r[decision_col] not in ("Fake", "Real")]
        pl_wrong = sum(
            1 for r in decided
            if (r[decision_col] == "Fake" and r["y_true"] == 0)
            or (r[decision_col] == "Real" and r["y_true"] == 1)
        )
        pl_fp = sum(1 for r in decided if r["y_true"] == 0 and r[decision_col] == "Fake")
        pl_fn = sum(1 for r in decided if r["y_true"] == 1 and r[decision_col] == "Real")

        cov = len(decided) / n
        abst_rate = len(abstained) / n
        st_err_rate = st_m1_err / n
        pl_err_rate = pl_wrong / n
        sel_acc = (len(decided) - pl_wrong) / len(decided) if decided else None
        err_red_m1 = ((st_m1_err - pl_wrong) / st_m1_err * 100.0) if st_m1_err > 0 else 0.0
        err_red_m4 = ((st_m4_err - pl_wrong) / st_m4_err * 100.0) if (st_m4_err is not None and st_m4_err > 0) else ""

        c_ev_col = "k1_c_ev" if decision_col == "k1_decision" else "c_ev"
        c_dec_col = "k1_c_dec" if decision_col == "k1_decision" else "c_dec"
        ev_vals = [r[c_ev_col] for r in sub if r[c_ev_col] is not None]
        dec_vals = [r[c_dec_col] for r in sub if r[c_dec_col] is not None]

        summaries.append({
            "track": tr,
            "n": n,
            "n_real": n_real,
            "n_fake": n_fake,
            "specialists_k": sub[0]["specialists_used"] if decision_col == "platform_decision" else 1,
            "standalone_error_rate": round(st_err_rate, 4),
            "standalone_m3_error_rate": "" if st_m3_err is None else round(st_m3_err / n, 4),
            "standalone_m4_error_rate": "" if st_m4_err is None else round(st_m4_err / n, 4),
            "standalone_fpr": "" if n_real == 0 else round(st_m1_fp / n_real, 4),
            "standalone_fnr": "" if n_fake == 0 else round(st_m1_fn / n_fake, 4),
            "k1_erroneous_verdict_rate": round(k1_wrong / n, 4),
            "k1_abstention_rate": round((n - len(k1_dec)) / n, 4),
            "platform_coverage": round(cov, 4),
            "platform_abstention_rate": round(abst_rate, 4),
            "platform_erroneous_verdict_rate": round(pl_err_rate, 4),
            "platform_false_accusation_rate": "" if n_real == 0 else round(pl_fp / n_real, 4),
            "platform_missed_forgery_rate": "" if n_fake == 0 else round(pl_fn / n_fake, 4),
            "selective_accuracy_on_decided": "" if sel_acc is None else round(sel_acc, 4),
            "relative_error_reduction_pct": round(err_red_m1, 2),
            "relative_error_reduction_vs_vit_pct": "" if err_red_m4 == "" else round(err_red_m4, 2),
            "mean_c_ev": round(float(np.mean(ev_vals)), 4) if ev_vals else "",
            "mean_c_dec": round(float(np.mean(dec_vals)), 4) if dec_vals else "",
        })
    return summaries


def compute_risk_coverage(rows: list[dict]) -> list[dict]:
    """Selective risk-coverage curve across pooled clean + degraded DS0001 tracks (n = 1,500)."""
    pool = [r for r in rows if r["dataset"] == "DS0001"]
    n = len(pool)
    out: list[dict] = []
    c_grid = np.linspace(0.0, 0.80, 17)

    for tau in c_grid:
        kept = [
            r for r in pool
            if r["c_dec"] is not None and r["c_dec"] >= tau and r["platform_decision"] in ("Fake", "Real")
        ] if tau >= 0.50 else [
            r for r in pool
            if r["c_dec"] is not None and r["c_dec"] >= tau
        ]
        cov = len(kept) / n
        if not kept:
            continue
        errs = sum(
            1 for r in kept
            if (
                (r["platform_decision"] == "Fake" and r["y_true"] == 0)
                or (r["platform_decision"] == "Real" and r["y_true"] == 1)
                if r["platform_decision"] in ("Fake", "Real")
                else r["standalone_pred_m1"] != r["y_true"]
            )
        )
        sel_risk = errs / len(kept)

        k_count = len(kept)
        raw_sorted = sorted(pool, key=lambda r: abs(r["prob_m1"] - FROZEN_T_M1), reverse=True)[:k_count]
        raw_errs = sum(1 for r in raw_sorted if r["standalone_pred_m1"] != r["y_true"])
        raw_risk_matched = raw_errs / k_count

        out.append({
            "c_dec_threshold": round(float(tau), 3),
            "coverage": round(cov, 4),
            "decided_cases": len(kept),
            "calibrated_4d_selective_risk": round(sel_risk, 4),
            "raw_margin_selective_risk_at_matched_coverage": round(raw_risk_matched, 4),
        })
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--per-track", type=int, default=300)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--multi-specialist", action="store_true")
    args = parser.parse_args()

    started = time.perf_counter()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cases = build_cases(per_track=args.per_track, seed=42)

    extra_maps = _load_extra_model_maps() if args.multi_specialist else {}
    if extra_maps:
        for c in cases:
            # Attach comparator predictions ONLY on unperturbed clean/cross-dataset tracks
            if c["pert_kind"] == "clean":
                if "MODEL0003" in extra_maps and c["key"] in extra_maps["MODEL0003"]:
                    c["prob_m3"] = extra_maps["MODEL0003"][c["key"]]
                if "MODEL0004" in extra_maps and c["key"] in extra_maps["MODEL0004"]:
                    c["prob_m4"] = extra_maps["MODEL0004"][c["key"]]
                c["extra_probs"] = [
                    (m_id, extra_maps[m_id][c["key"]])
                    for m_id in ("MODEL0003", "MODEL0004")
                    if m_id in extra_maps and c["key"] in extra_maps[m_id]
                ]

    chunks = [cases[i::args.workers] for i in range(args.workers)]
    all_rows: list[dict] = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as ex:
        for part in ex.map(_worker_chunk, chunks):
            all_rows.extend(part)

    summaries_k3 = summarize_tracks(all_rows, decision_col="platform_decision")
    summaries_k1 = summarize_tracks(all_rows, decision_col="k1_decision")
    rc_rows = compute_risk_coverage(all_rows)
    elapsed = round(time.perf_counter() - started, 2)

    with (OUT_DIR / "abstention_case_predictions.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(all_rows)

    with (OUT_DIR / "abstention_by_track.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summaries_k3[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(summaries_k3)

    with (OUT_DIR / "abstention_by_track_k1.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summaries_k1[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(summaries_k1)

    with (OUT_DIR / "selective_risk_coverage.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rc_rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rc_rows)

    meta = {
        "evaluation_id": "EVAL0008",
        "total_cases": len(all_rows),
        "per_track": args.per_track,
        "specialists": ["MODEL0001"] + sorted(extra_maps.keys()),
        "wall_seconds": elapsed,
        "mean_case_latency_ms": round(float(np.mean([r["latency_ms"] for r in all_rows])), 2),
        "tracks_k3": summaries_k3,
        "tracks_k1": summaries_k1,
    }
    (OUT_DIR / "eval0008_summary.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"EVAL0008 complete: {len(all_rows)} cases in {elapsed}s (mean {meta['mean_case_latency_ms']} ms/case)")
    for s in summaries_k3:
        m4_s = f"{s['standalone_m4_error_rate']*100:5.1f}%" if s["standalone_m4_error_rate"] != "" else "  n/a "
        print(
            f"  {s['track']:20s} (K={s['specialists_k']}) | ResNet Err: {s['standalone_error_rate']*100:5.1f}% "
            f"| ViT Err: {m4_s} "
            f"| K=1 Wrong: {s['k1_erroneous_verdict_rate']*100:5.1f}% "
            f"| K={s['specialists_k']} Wrong: {s['platform_erroneous_verdict_rate']*100:5.1f}% "
            f"| Abstained: {s['platform_abstention_rate']*100:5.1f}% "
            f"| Red vs ResNet: {s['relative_error_reduction_pct']:5.1f}%"
        )


if __name__ == "__main__":
    main()
