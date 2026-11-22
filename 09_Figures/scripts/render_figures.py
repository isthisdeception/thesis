"""Human-runnable publication figure renderer for FIG0001-FIG0025 (Policy A.9).

This script reads strictly from verified repository CSV outputs using Python's
standard library ``csv`` module (no pandas required) and ``matplotlib``,
producing 600 DPI PNG and vector PDF figures styled for IEEE/ACM/Elsevier
publication in ``09_Figures/assets/``.

Policy A.9 Notice:
    The AI does NOT execute this script to commit figures. The human researcher
    reviews, executes, visually inspects every rendered asset against
    Checklist 14 (09_Figures/FIGURE_RENDERING_RUNBOOK.md), and commits the
    approved assets.

Usage (from repository root):
    python 09_Figures/scripts/render_figures.py
    python 09_Figures/scripts/render_figures.py --only FIG0011 FIG0018 FIG0021
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "09_Figures" / "assets"

# Cohesive IEEE/ACM colorblind-safe palette (matches FIG0026-FIG0030 Draw.io)
PALETTE = {
    "slate": "#1F618D",
    "real": "#3B6D9A",
    "fake": "#B85C38",
    "teal": "#117A65",
    "amber": "#B9770E",
    "crimson": "#922B21",
    "gray": "#566573",
    "steel": "#5D6D7E",
    "gold": "#B7950B",
}


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "grid.linestyle": "--",
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.bbox": "tight",
            "savefig.dpi": 600,
        }
    )


def read_csv(rel_path: str) -> list[dict[str, str]]:
    with open(ROOT / rel_path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def save_fig(fig: plt.Figure, fig_id: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_DIR / f"{fig_id}_v1.png", dpi=600)
    fig.savefig(OUT_DIR / f"{fig_id}_v1.pdf")
    plt.close(fig)
    print(f"Rendered {fig_id}_v1.png and {fig_id}_v1.pdf")


def plot_class_balance(dataset_id: str, fig_id: str, title: str) -> None:
    rows = [r for r in read_csv("03_Datasets/reports/eda_class_distribution.csv") if r["Dataset ID"] == dataset_id]
    rows.sort(key=lambda r: r["Class"])
    labels = [r["Class"].capitalize() for r in rows]
    counts = [int(float(r["Count"])) for r in rows]
    props = [float(r["Proportion"]) * 100 for r in rows]
    colors = [PALETTE["fake"] if r["Class"] == "fake" else PALETTE["real"] for r in rows]
    fig, ax = plt.subplots(figsize=(4.2, 3.0))
    bars = ax.bar(labels, counts, color=colors, width=0.52)
    for bar, cnt, prop in zip(bars, counts, props):
        ax.text(bar.get_x() + bar.get_width() / 2, cnt, f"{cnt:,}\n({prop:.1f}%)", ha="center", va="bottom", fontsize=8)
    ax.set_ylabel("Image count")
    ax.set_title(title)
    ax.set_ylim(0, max(counts) * 1.22)
    save_fig(fig, fig_id)


def render_fig0001() -> None:
    plot_class_balance("DS0001", "FIG0001", "DS0001 (ArtiFact Face Subset) Class Balance")


def render_fig0002() -> None:
    rows = [r for r in read_csv("03_Datasets/reports/eda_generator_distribution.csv") if r["Dataset ID"] == "DS0001"]
    agg: dict[str, int] = defaultdict(int)
    cls_map: dict[str, str] = {}
    for r in rows:
        g = r["Generator"]
        agg[g] += int(float(r["Count"]))
        cls_map[g] = r["Class"]
    items = sorted(agg.items(), key=lambda x: x[1])
    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    colors = [PALETTE["real"] if cls_map[k] == "real" else PALETTE["fake"] for k, _ in items]
    ax.barh([k for k, _ in items], [v for _, v in items], color=colors)
    ax.set_xlabel("Image count")
    ax.set_title("DS0001 Generator Composition (13 Synthetic Generators + Real)")
    save_fig(fig, "FIG0002")


def render_fig0003() -> None:
    rows = [r for r in read_csv("03_Datasets/reports/eda_generator_distribution.csv") if r["Dataset ID"] == "DS0002"]
    gens = sorted({r["Generator"] for r in rows})
    conds = sorted({r["Condition"] for r in rows if r["Condition"]})
    mat = np.zeros((len(gens), len(conds)), dtype=float)
    for r in rows:
        if r["Condition"] in conds:
            mat[gens.index(r["Generator"]), conds.index(r["Condition"])] += float(r["Count"])
    fig, ax = plt.subplots(figsize=(6.5, 4.8))
    im = ax.imshow(mat, aspect="auto", cmap="Blues")
    ax.set_xticks(range(len(conds)), conds)
    ax.set_yticks(range(len(gens)), gens)
    for i in range(len(gens)):
        for j in range(len(conds)):
            if mat[i, j] > 0:
                ax.text(j, i, f"{int(mat[i, j]):,}", ha="center", va="center", fontsize=7, color="black")
    fig.colorbar(im, ax=ax, label="Image count")
    ax.set_title("DS0002 (DiFF Official Test) Generator x Condition Counts")
    save_fig(fig, "FIG0003")


def render_fig0004() -> None:
    plot_class_balance("DS0003", "FIG0004", "DS0003 (140k Real & Fake Faces) Class Balance")


def render_fig0005() -> None:
    rows = [r for r in read_csv("03_Datasets/reports/eda_generator_distribution.csv") if r["Dataset ID"] == "DS0004"]
    agg: dict[str, int] = defaultdict(int)
    cls_map: dict[str, str] = {}
    for r in rows:
        agg[r["Generator"]] += int(float(r["Count"]))
        cls_map[r["Generator"]] = r["Class"]
    items = sorted(agg.items(), key=lambda x: x[1])
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    colors = [PALETTE["real"] if cls_map[k] == "real" else PALETTE["fake"] for k, _ in items]
    ax.barh([k for k, _ in items], [v for _, v in items], color=colors)
    ax.set_xlabel("Image count")
    ax.set_title("DS0004 (Synthbuster) Generator Mix + RAISE Real")
    save_fig(fig, "FIG0005")


def render_fig0006() -> None:
    rows = [
        r
        for r in read_csv("03_Datasets/reports/eda_demographic_distribution.csv")
        if r["Dataset ID"] == "DS0005" and r["Attribute"].lower() == "race"
    ]
    agg: dict[str, int] = defaultdict(int)
    for r in rows:
        agg[r["Level"]] += int(float(r["Count"]))
    items = sorted(agg.items(), key=lambda x: x[1])
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.barh([k for k, _ in items], [v for _, v in items], color=PALETTE["slate"])
    ax.set_xlabel("Image count")
    ax.set_title("DS0005 (FairFace) Demographic Race Distribution")
    save_fig(fig, "FIG0006")


def render_fig0007() -> None:
    rows = read_csv("03_Datasets/reports/eda_resolution_distribution.csv")
    by_ds: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for r in rows:
        by_ds[r["Dataset ID"]].append((int(float(r["Width"])), int(float(r["Count"]))))
    ds_ids = sorted(by_ds)
    med_w = []
    for ds in ds_ids:
        vals = sorted(by_ds[ds], key=lambda x: x[0])
        tot = sum(c for _, c in vals)
        acc = 0
        m = vals[0][0]
        for w, c in vals:
            acc += c
            if acc >= tot / 2:
                m = w
                break
        med_w.append(m)
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    ax.bar(ds_ids, med_w, color=PALETTE["slate"], width=0.55)
    ax.set_ylabel("Median source width (px)")
    ax.set_title("Median Source Image Resolution Across Datasets (DS0001-DS0005)")
    save_fig(fig, "FIG0007")


def plot_luma_stat(csv_path: str, fig_id: str, ylabel: str, title: str) -> None:
    rows = [r for r in read_csv(csv_path) if r["Stratum"] == "ALL"]
    rows.sort(key=lambda r: r["Dataset ID"])
    ds = [r["Dataset ID"] for r in rows]
    means = [float(r["Mean"]) for r in rows]
    stds = [float(r["Std"]) for r in rows]
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    ax.bar(ds, means, yerr=stds, capsize=4, color=PALETTE["teal"], width=0.55)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    save_fig(fig, fig_id)


def render_fig0008() -> None:
    plot_luma_stat("03_Datasets/reports/eda_brightness_stats.csv", "FIG0008", "Mean luminance (0-1)", "Mean Brightness Across Datasets (+/- 1 SD)")


def render_fig0009() -> None:
    plot_luma_stat("03_Datasets/reports/eda_contrast_stats.csv", "FIG0009", "Contrast (luminance SD)", "Image Contrast Across Datasets (+/- 1 SD)")


def render_fig0010() -> None:
    rows = read_csv("03_Datasets/reports/eda_compression_stats.csv")
    labels = [f"{r['Dataset ID']} ({r['Format']})" for r in rows]
    kb = [float(r["Median Bytes"]) / 1024.0 for r in rows]
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.barh(labels, kb, color=PALETTE["amber"])
    ax.set_xlabel("Median file size (KB)")
    ax.set_title("Source File Format & Compression Footprint Across Datasets")
    save_fig(fig, "FIG0010")


def render_fig0011() -> None:
    rows = [r for r in read_csv("08_Evaluation/EVAL0001/reliability.csv") if r["split"] == "test" and int(r["count"]) > 0]
    summ = {r["split"]: r for r in read_csv("08_Evaluation/EVAL0001/calibration_summary.csv")}["test"]
    xs = [float(r["mean_confidence"]) for r in rows]
    ys = [float(r["fraction_positive"]) for r in rows]
    cnts = [int(r["count"]) for r in rows]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.2, 5.4), gridspec_kw={"height_ratios": [3, 1]}, sharex=True)
    ax1.plot([0, 1], [0, 1], "--", color=PALETTE["gray"], label="Perfect calibration")
    ax1.plot(xs, ys, "o-", color=PALETTE["slate"], label=f"Test (ECE={float(summ['ece']):.4f}, MCE={float(summ['mce']):.4f})")
    ax1.set_ylabel("Observed fraction fake")
    ax1.set_title("Reliability Diagram — MODEL0001 (EXP0001 Test)")
    ax1.legend(loc="upper left")
    ax2.bar(xs, cnts, width=0.055, color=PALETTE["slate"], alpha=0.75)
    ax2.set_xlabel("Mean predicted P(fake)")
    ax2.set_ylabel("Count")
    ax2.set_yscale("log")
    save_fig(fig, "FIG0011")


def render_fig0012() -> None:
    rows = [r for r in read_csv("08_Evaluation/EVAL0001/confidence_distribution.csv") if r["split"] == "test" and int(r["count"]) > 0 and int(r["bin"]) >= 0]
    conf = [float(r["mean_confidence"]) for r in rows]
    acc = [float(r["accuracy"]) for r in rows]
    share = [float(r["share"]) * 100 for r in rows]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.4, 5.2), sharex=True, gridspec_kw={"height_ratios": [2.5, 1]})
    ax1.plot([0.5, 1.0], [0.5, 1.0], "--", color=PALETTE["gray"], label="Ideal (Confidence = Accuracy)")
    ax1.plot(conf, acc, "o-", color=PALETTE["teal"], label="Observed accuracy")
    ax1.set_ylabel("Empirical accuracy")
    ax1.set_title("Confidence vs. Empirical Accuracy — MODEL0001 (EXP0001 Test)")
    ax1.legend()
    ax2.bar(conf, share, width=0.04, color=PALETTE["slate"], alpha=0.8)
    ax2.set_xlabel("Mean predicted-class confidence")
    ax2.set_ylabel("Share (%)")
    save_fig(fig, "FIG0012")


def render_fig0013() -> None:
    sw = [r for r in read_csv("08_Evaluation/EVAL0001/threshold_sweep.csv") if r["split"] == "test"]
    ops = [r for r in read_csv("08_Evaluation/EVAL0001/operating_points.csv") if r["split"] == "test"]
    t = [float(r["threshold"]) for r in sw]
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(t, [float(r["balanced_accuracy"]) for r in sw], color=PALETTE["slate"], lw=1.8, label="Balanced accuracy")
    ax.plot(t, [float(r["fnr"]) for r in sw], color=PALETTE["crimson"], lw=1.5, label="FNR (missed fakes)")
    ax.plot(t, [float(r["fpr"]) for r in sw], color=PALETTE["amber"], lw=1.5, label="FPR (false alarms)")
    for op in ops:
        if op["point"] in {"frozen", "high_sensitivity", "high_specificity"}:
            tv = float(op["threshold"])
            ax.axvline(tv, linestyle=":", color=PALETTE["gray"], lw=1.2)
            ax.text(tv + 0.01, 0.96, f"{op['point']}\n({tv:.3f})", fontsize=7, va="top")
    ax.set_xlabel("Decision threshold on P(fake)")
    ax.set_ylabel("Metric value (0-1)")
    ax.set_title("Threshold Trade-Off & Val-Selected Operating Points (EXP0001 Test)")
    ax.legend(loc="center right")
    save_fig(fig, "FIG0013")


def render_fig0014() -> None:
    rows = [r for r in read_csv("08_Evaluation/EVAL0001/confusion_matrix.csv") if r["split"] == "test"]
    labels = ["fake", "real"]
    mat = np.zeros((2, 2), dtype=int)
    pct = np.zeros((2, 2), dtype=float)
    for r in rows:
        i = labels.index(r["true_label"])
        j = labels.index(r["predicted_label"])
        mat[i, j] = int(r["count"])
        pct[i, j] = float(r["share_of_true"]) * 100
    fig, ax = plt.subplots(figsize=(4.2, 3.8))
    im = ax.imshow(pct, cmap="Blues", vmin=0, vmax=100)
    ax.set_xticks([0, 1], ["Predicted Fake", "Predicted Real"])
    ax.set_yticks([0, 1], ["True Fake", "True Real"])
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{mat[i, j]:,}\n({pct[i, j]:.1f}%)", ha="center", va="center",
                    color="white" if pct[i, j] > 55 else "black", fontsize=9, fontweight="bold")
    fig.colorbar(im, ax=ax, label="Row percentage (%)")
    ax.set_title("Confusion Matrix — MODEL0001 (t = 0.3951)")
    save_fig(fig, "FIG0014")


def render_fig0015() -> None:
    rows = [r for r in read_csv("08_Evaluation/EVAL0001/error_by_group.csv") if r["split"] == "test" and r["small_group"].lower() != "true"]
    rows.sort(key=lambda r: (r["true_label"], float(r["error_rate"])))
    labels = [f"{r['group']} ({r['true_label']})" for r in rows]
    rates = [float(r["error_rate"]) * 100 for r in rows]
    lo = [(float(r["error_rate"]) - float(r["ci_low"])) * 100 for r in rows]
    hi = [(float(r["ci_high"]) - float(r["error_rate"])) * 100 for r in rows]
    colors = [PALETTE["fake"] if r["true_label"] == "fake" else PALETTE["real"] for r in rows]
    fig, ax = plt.subplots(figsize=(7.0, 5.2))
    ax.barh(labels, rates, xerr=[lo, hi], color=colors, capsize=2.5, alpha=0.9)
    ax.set_xlabel("Error rate (%) with 95% Wilson CI (FNR for fake, FPR for real)")
    ax.set_title("Subgroup Error Rates by Generator & Real Source (EXP0001 Test)")
    save_fig(fig, "FIG0015")


def render_fig0016() -> None:
    rows = [r for r in read_csv("08_Evaluation/EVAL0001/robustness/robustness_metrics.csv") if r["perturbation"] != "clean"]
    clean = [r for r in read_csv("08_Evaluation/EVAL0001/robustness/robustness_metrics.csv") if r["perturbation"] == "clean"][0]
    by_p: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in rows:
        by_p[r["perturbation"]].append(r)
    perts = sorted(by_p)
    fig, axes = plt.subplots(3, 5, figsize=(11.5, 6.8), sharey=True)
    for ax, p in zip(axes.flat, perts):
        seq = sorted(by_p[p], key=lambda x: int(x["rank"]))
        lvls = [r["level"] for r in seq]
        ax.plot(lvls, [float(r["balanced_accuracy"]) for r in seq], "o-", color=PALETTE["slate"], label="BA")
        ax.plot(lvls, [float(r["roc_auc"]) for r in seq], "s--", color=PALETTE["teal"], label="ROC-AUC")
        ax.axhline(float(clean["balanced_accuracy"]), color=PALETTE["gray"], ls=":", lw=1)
        ax.set_title(p, fontsize=8)
        ax.set_ylim(0.45, 1.0)
        ax.tick_params(axis="x", labelrotation=35, labelsize=7)
    axes[0, 0].legend(fontsize=7)
    fig.supylabel("Score (0-1)")
    fig.suptitle("Phase E7 Robustness Curves Across 15 Perturbation Families (53 Conditions)", fontsize=11)
    save_fig(fig, "FIG0016")


def render_fig0017() -> None:
    rows = read_csv("08_Evaluation/EVAL0001/robustness/robustness_by_group.csv")
    max_rank: dict[str, int] = defaultdict(int)
    for r in rows:
        if r["perturbation"] != "clean":
            max_rank[r["perturbation"]] = max(max_rank[r["perturbation"]], int(r["rank"]))
    worst = [r for r in rows if r["perturbation"] != "clean" and int(r["rank"]) == max_rank[r["perturbation"]] and r["small_group"].lower() != "true"]
    perts = sorted({r["perturbation"] for r in worst})
    groups = sorted({f"{r['true_label']}:{r['group']}" for r in worst})
    mat = np.zeros((len(groups), len(perts)))
    for r in worst:
        mat[groups.index(f"{r['true_label']}:{r['group']}"), perts.index(r["perturbation"])] = float(r["delta_error_rate"]) * 100
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    im = ax.imshow(mat, aspect="auto", cmap="RdBu_r", vmin=-30, vmax=95)
    ax.set_xticks(range(len(perts)), perts, rotation=45, ha="right", fontsize=7.5)
    ax.set_yticks(range(len(groups)), groups, fontsize=7.5)
    fig.colorbar(im, ax=ax, label="Delta error rate vs. clean (percentage points)")
    ax.set_title("Worst-Level Subgroup Error Shift Across 15 Perturbation Families (Phase E7)")
    save_fig(fig, "FIG0017")


def render_fig0018() -> None:
    rows = read_csv("08_Evaluation/EVAL0001/generalization/cross_dataset_metrics.csv")
    ds = [r["dataset"] for r in rows]
    fnr = [float(r["fnr"]) * 100 if r["fnr"] else np.nan for r in rows]
    fpr = [float(r["fpr"]) * 100 if r["fpr"] else np.nan for r in rows]
    x = np.arange(len(ds))
    w = 0.35
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.bar(x - w / 2, np.nan_to_num(fnr), w, label="FNR (missed fakes)", color=PALETTE["fake"])
    ax.bar(x + w / 2, np.nan_to_num(fpr), w, label="FPR (real flagged fake)", color=PALETTE["real"])
    for i, (vn, vp) in enumerate(zip(fnr, fpr)):
        if not np.isnan(vn):
            ax.text(i - w / 2, vn + 1.5, f"{vn:.1f}%", ha="center", fontsize=7.5)
        if not np.isnan(vp):
            ax.text(i + w / 2, vp + 1.5, f"{vp:.1f}%", ha="center", fontsize=7.5)
    ax.set_xticks(x, ds)
    ax.set_ylabel("Error rate (%) at frozen threshold 0.3951")
    ax.set_ylim(0, 98)
    ax.set_title("Phase E8 Cross-Dataset Error Rates (MODEL0001)")
    ax.legend()
    save_fig(fig, "FIG0018")


def render_fig0019() -> None:
    det = read_csv("08_Evaluation/EVAL0002/unseen_generator/unseen_detection.csv")
    paired = read_csv("08_Evaluation/EVAL0002/unseen_generator/unseen_paired.csv")[0]
    det_fakes = [r for r in det if r["group"] in {"stable_diffusion", "all seen generators", "real"}]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.2, 3.6))
    labels1 = [r["group"] for r in det_fakes]
    vals1 = [float(r["rate"]) * 100 for r in det_fakes]
    colors1 = [PALETTE["crimson"] if r["group"] == "stable_diffusion" else PALETTE["slate"] for r in det_fakes]
    ax1.bar(labels1, vals1, color=colors1, width=0.55)
    ax1.set_ylabel("Detection / Specificity (%)")
    ax1.set_ylim(0, 105)
    ax1.set_title("EXP0002 (MODEL0008) Seen vs. Held-Out")
    ax1.tick_params(axis="x", labelrotation=15)
    ax2.bar(
        ["MODEL0001\n(seen in train)", "MODEL0008\n(held out)"],
        [float(paired["recall_reference"]) * 100, float(paired["recall_held_out"]) * 100],
        color=[PALETTE["teal"], PALETTE["crimson"]],
        width=0.5,
    )
    ax2.set_ylim(0, 108)
    ax2.set_ylabel("Recall (%) on identical 299 SD images")
    ax2.set_title("Paired Stable Diffusion Recall (n=299)")
    save_fig(fig, "FIG0019")


def render_fig0020() -> None:
    rows = [r for r in read_csv("08_Evaluation/ablations/ablation_results.csv") if r["experiment_id"] != "EXP0001"]
    labels = [f"{r['experiment_id']}\n({r['factor']})" for r in rows]
    metrics = [("delta_roc_auc", "ΔROC-AUC", PALETTE["slate"]), ("delta_balanced_accuracy", "ΔBA", PALETTE["teal"]), ("delta_mcc", "ΔMCC", PALETTE["amber"])]
    x = np.arange(len(rows))
    w = 0.25
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    for k, (col, lbl, colr) in enumerate(metrics):
        vals = [float(r[col]) for r in rows]
        ax.bar(x + (k - 1) * w, vals, w, label=lbl, color=colr)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks(x, labels)
    ax.set_ylabel("Delta vs. EXP0001 baseline")
    ax.set_title("Phase E10 One-Factor Ablations Against Seed Noise Floor")
    ax.legend()
    save_fig(fig, "FIG0020")


def render_fig0021() -> None:
    exps = [("EXP0001", "EXP0001 baseline", PALETTE["slate"]), ("EXP0003", "EXP0003 seed 43", PALETTE["teal"]),
            ("EXP0004", "EXP0004 no aug", PALETTE["amber"]), ("EXP0005", "EXP0005 no pretrain", PALETTE["crimson"]),
            ("EXP0006", "EXP0006 160px", PALETTE["steel"])]
    fig, ax = plt.subplots(figsize=(5.2, 5.0))
    for eid, lbl, colr in exps:
        rows = [r for r in read_csv(f"08_Evaluation/{eid}/roc_curve.csv") if r["split"] == "test"]
        ax.plot([float(r["fpr"]) for r in rows], [float(r["tpr"]) for r in rows], color=colr, lw=1.6, label=lbl)
    ax.plot([0, 1], [0, 1], "--", color=PALETTE["gray"], lw=1, label="Chance")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_aspect("equal")
    ax.set_title("Test ROC Curves — Fairness-Compatible Runs (SPLIT0001)")
    ax.legend(loc="lower right", fontsize=7.5)
    save_fig(fig, "FIG0021")


def render_fig0022() -> None:
    exps = [("EXP0001", "EXP0001 baseline", PALETTE["slate"]), ("EXP0003", "EXP0003 seed 43", PALETTE["teal"]),
            ("EXP0004", "EXP0004 no aug", PALETTE["amber"]), ("EXP0005", "EXP0005 no pretrain", PALETTE["crimson"]),
            ("EXP0006", "EXP0006 160px", PALETTE["steel"])]
    fig, ax = plt.subplots(figsize=(5.2, 5.0))
    for eid, lbl, colr in exps:
        rows = [r for r in read_csv(f"08_Evaluation/{eid}/pr_curve.csv") if r["split"] == "test"]
        ax.plot([float(r["recall"]) for r in rows], [float(r["precision"]) for r in rows], color=colr, lw=1.6, label=lbl)
    ax.axhline(0.5035, ls="--", color=PALETTE["gray"], lw=1, label="Chance (0.504)")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Test Precision-Recall Curves — Fairness-Compatible Runs (SPLIT0001)")
    ax.legend(loc="lower left", fontsize=7.5)
    save_fig(fig, "FIG0022")


def render_fig0023() -> None:
    rows = read_csv("08_Evaluation/comparison_tables.csv")
    labels = [f"{r['experiment_id']} ({r['factor']})" for r in rows]
    y = np.arange(len(rows))
    h = 0.25
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.barh(y - h, [float(r["roc_auc"]) for r in rows], h, label="ROC-AUC", color=PALETTE["slate"])
    ax.barh(y, [float(r["balanced_accuracy"]) for r in rows], h, label="Balanced Acc.", color=PALETTE["teal"])
    ax.barh(y + h, [float(r["mcc"]) for r in rows], h, label="MCC", color=PALETTE["amber"])
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlabel("Metric value")
    ax.set_xlim(0.2, 1.0)
    ax.set_title("Fairness-Compatible Metric Comparison (SPLIT0001 Test)")
    ax.legend(loc="lower right")
    save_fig(fig, "FIG0023")


def _load_exp0001_session_epochs() -> list[dict[str, str]]:
    summary = json.loads((ROOT / "06_Experiments/EXP0001/metrics/run_summary.json").read_text(encoding="utf-8"))
    sess = summary["sessions"][-1]
    rows = [r for r in read_csv("06_Experiments/EXP0001/logs/EXP0001_epochs.csv") if r["session"] == sess]
    rows.sort(key=lambda r: int(r["epoch"]))
    return rows


def render_fig0024() -> None:
    rows = _load_exp0001_session_epochs()
    ep = [int(r["epoch"]) for r in rows]
    auc = [float(r["roc_auc_score"]) for r in rows]
    fig, ax = plt.subplots(figsize=(5.8, 3.4))
    ax.plot(ep, auc, "o-", color=PALETTE["slate"], lw=1.8)
    ax.axvline(7, ls="--", color=PALETTE["teal"], lw=1.2, label="Best epoch (7, min valid_loss)")
    ax.set_xlabel("Epoch (0 = frozen head; 1-10 = unfrozen)")
    ax.set_ylabel("Validation ROC-AUC")
    ax.set_title("EXP0001 Validation ROC-AUC Trajectory")
    ax.legend()
    save_fig(fig, "FIG0024")


def render_fig0025() -> None:
    rows = _load_exp0001_session_epochs()
    ep = [int(r["epoch"]) for r in rows]
    tr = [float(r["train_loss"]) for r in rows]
    va = [float(r["valid_loss"]) for r in rows]
    fig, ax = plt.subplots(figsize=(5.8, 3.4))
    ax.plot(ep, tr, "o-", color=PALETTE["slate"], lw=1.6, label="Training loss")
    ax.plot(ep, va, "s-", color=PALETTE["crimson"], lw=1.6, label="Validation loss")
    ax.axvline(7, ls="--", color=PALETTE["teal"], lw=1.2, label="Best epoch (7)")
    ax.set_xlabel("Epoch (0 = frozen head; 1-10 = unfrozen)")
    ax.set_ylabel("Cross-entropy loss")
    ax.set_title("EXP0001 Training & Validation Loss Trajectory")
    ax.legend()
    save_fig(fig, "FIG0025")


RENDERERS = {
    f"FIG{i:04d}": globals()[f"render_fig{i:04d}"] for i in range(1, 26)
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Human-runnable renderer for FIG0001-FIG0025 (Policy A.9).")
    parser.add_argument("--only", nargs="*", help="Optional list of FIG IDs to render (default: all 25).")
    args = parser.parse_args()
    setup_style()
    targets = args.only if args.only else sorted(RENDERERS)
    for fid in targets:
        if fid not in RENDERERS:
            raise SystemExit(f"Unknown figure ID: {fid}")
        RENDERERS[fid]()


if __name__ == "__main__":
    main()
