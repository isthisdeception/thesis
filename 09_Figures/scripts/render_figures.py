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
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.4, 5.6), gridspec_kw={"height_ratios": [2.8, 1.1]}, sharex=True)
    ax1.plot([0, 1], [0, 1], "--", color=PALETTE["gray"], label="Perfect calibration")
    ax1.plot(xs, ys, "o-", color=PALETTE["slate"], label=f"Test (ECE={float(summ['ece']):.4f}, MCE={float(summ['mce']):.4f})")
    ax1.set_ylabel("Observed fraction fake")
    ax1.set_title("(a) Reliability Curve (ArtiFact Test Split)", fontsize=9.5, fontweight="bold")
    ax1.legend(loc="upper left")
    ax2.bar(xs, cnts, width=0.055, color=PALETTE["slate"], alpha=0.75)
    ax2.set_title("(b) Sample Count per Predicted Probability Bin", fontsize=9.5, fontweight="bold")
    ax2.set_xlabel("Mean predicted P(fake)")
    ax2.set_ylabel("Count")
    ax2.set_yscale("log")
    fig.subplots_adjust(hspace=0.28)
    save_fig(fig, "FIG0011")


def render_fig0012() -> None:
    rows = [r for r in read_csv("08_Evaluation/EVAL0001/confidence_distribution.csv") if r["split"] == "test" and int(r["count"]) > 0 and int(r["bin"]) >= 0]
    conf = [float(r["mean_confidence"]) for r in rows]
    acc = [float(r["accuracy"]) for r in rows]
    share = [float(r["share"]) * 100 for r in rows]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.4, 5.4), sharex=True, gridspec_kw={"height_ratios": [2.5, 1.1]})
    ax1.plot([0.5, 1.0], [0.5, 1.0], "--", color=PALETTE["gray"], label="Ideal (Confidence = Accuracy)")
    ax1.plot(conf, acc, "o-", color=PALETTE["teal"], label="Observed accuracy")
    ax1.set_ylabel("Empirical accuracy")
    ax1.set_title("(a) Confidence vs. Empirical Accuracy", fontsize=9.5, fontweight="bold")
    ax1.legend()
    ax2.bar(conf, share, width=0.04, color=PALETTE["slate"], alpha=0.8)
    ax2.set_title("(b) Share of Predictions per Bin", fontsize=9.5, fontweight="bold")
    ax2.set_xlabel("Mean predicted-class confidence")
    ax2.set_ylabel("Share (%)")
    fig.subplots_adjust(hspace=0.28)
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
    ax.set_title("Subgroup Error Rates by Generator & Real Source (ArtiFact Test)")
    save_fig(fig, "FIG0015")


def render_fig0016() -> None:
    rows = [r for r in read_csv("08_Evaluation/EVAL0001/robustness/robustness_metrics.csv") if r["perturbation"] != "clean"]
    clean = [r for r in read_csv("08_Evaluation/EVAL0001/robustness/robustness_metrics.csv") if r["perturbation"] == "clean"][0]
    by_p: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in rows:
        by_p[r["perturbation"]].append(r)
    perts = sorted(by_p)
    pretty = {
        "brightness_down": "Brightness Down",
        "brightness_up": "Brightness Up",
        "center_crop": "Center Crop",
        "contrast_down": "Contrast Down",
        "contrast_up": "Contrast Up",
        "desaturate": "Desaturate",
        "gaussian_blur": "Gaussian Blur",
        "gaussian_noise": "Gaussian Noise",
        "jpeg": "JPEG Quality",
        "low_quality_upload": "Low-Quality Upload",
        "occlusion": "Occlusion",
        "oversaturate": "Oversaturate",
        "resolution": "Downscaling",
        "rotation": "Rotation (deg)",
        "upscaling": "Upscaling",
    }
    fig, axes = plt.subplots(3, 5, figsize=(12.8, 8.2), sharey=True)
    for idx, (ax, p) in enumerate(zip(axes.flat, perts)):
        panel_lbl = chr(ord("a") + idx)
        seq = sorted(by_p[p], key=lambda x: int(x["rank"]))
        lvls = [r["level"].replace("_", "/q") if p == "low_quality_upload" else r["level"] for r in seq]
        ax.plot(lvls, [float(r["balanced_accuracy"]) for r in seq], "o-", color=PALETTE["slate"], lw=1.5, ms=4.5, label="BA")
        ax.plot(lvls, [float(r["roc_auc"]) for r in seq], "s--", color=PALETTE["teal"], lw=1.5, ms=4.5, label="ROC-AUC")
        ax.axhline(float(clean["balanced_accuracy"]), color=PALETTE["gray"], ls=":", lw=1)
        ax.set_title(f"({panel_lbl}) {pretty.get(p, p)}", fontsize=9, fontweight="bold", pad=6)
        ax.set_ylim(0.45, 1.0)
        ax.tick_params(axis="x", labelrotation=30, labelsize=7.5)
        for lbl in ax.get_xticklabels():
            lbl.set_ha("right")
    axes[0, 0].legend(fontsize=7.5, loc="lower left")
    fig.supylabel("Score (0-1)", fontsize=10, x=0.015)
    fig.subplots_adjust(hspace=0.60, wspace=0.14, top=0.94, bottom=0.09, left=0.065, right=0.985)
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
    ds_names = {
        "DS0001": "ArtiFact\n(In-Dist.)",
        "DS0002": "DiFF\n(Diffusion)",
        "DS0003": "140k Faces\n(GAN/FFHQ)",
        "DS0004": "Synthbuster\n(Diff./Scenes)",
        "DS0005": "FairFace\n(Real Only)",
    }
    ds = [ds_names.get(r["dataset"], r["dataset"]) for r in rows]
    fnr = [float(r["fnr"]) * 100 if r["fnr"] else np.nan for r in rows]
    fpr = [float(r["fpr"]) * 100 if r["fpr"] else np.nan for r in rows]
    x = np.arange(len(ds))
    w = 0.35
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.bar(x - w / 2, np.nan_to_num(fnr), w, label="FNR (missed fakes)", color=PALETTE["fake"])
    ax.bar(x + w / 2, np.nan_to_num(fpr), w, label="FPR (real flagged fake)", color=PALETTE["real"])
    for i, (vn, vp) in enumerate(zip(fnr, fpr)):
        if not np.isnan(vn):
            ax.text(i - w / 2, vn + 1.8, f"{vn:.1f}%", ha="center", fontsize=8, fontweight="bold")
        if not np.isnan(vp):
            ax.text(i + w / 2, vp + 1.8, f"{vp:.1f}%", ha="center", fontsize=8, fontweight="bold")
    ax.set_xticks(x, ds, fontsize=8)
    ax.set_ylabel("Error rate (%) at frozen threshold 0.3951")
    ax.set_ylim(0, 100)
    ax.set_title("Cross-Dataset Error Rates (Baseline ResNet-50)")
    ax.legend(loc="upper left")
    save_fig(fig, "FIG0018")


def render_fig0019() -> None:
    det = read_csv("08_Evaluation/EVAL0002/unseen_generator/unseen_detection.csv")
    paired = read_csv("08_Evaluation/EVAL0002/unseen_generator/unseen_paired.csv")[0]
    det_fakes = [r for r in det if r["group"] in {"stable_diffusion", "all seen generators", "real"}]
    pretty_grp = {
        "stable_diffusion": "Held-Out\nStable Diff.",
        "all seen generators": "12 Seen\nGenerators",
        "real": "Real Faces\n(Specificity)",
    }
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.8))
    labels1 = [pretty_grp.get(r["group"], r["group"]) for r in det_fakes]
    vals1 = [float(r["rate"]) * 100 for r in det_fakes]
    colors1 = [PALETTE["crimson"] if r["group"] == "stable_diffusion" else PALETTE["slate"] for r in det_fakes]
    ax1.bar(labels1, vals1, color=colors1, width=0.55)
    for i, v in enumerate(vals1):
        ax1.text(i, v + 2.0, f"{v:.1f}%", ha="center", fontsize=8.5, fontweight="bold")
    ax1.set_ylabel("Recall / Specificity (%)")
    ax1.set_ylim(0, 108)
    ax1.set_title("(a) Seen Generators vs. Held-Out SD", fontsize=9.5, fontweight="bold")
    vals2 = [float(paired["recall_reference"]) * 100, float(paired["recall_held_out"]) * 100]
    ax2.bar(
        ["Baseline\n(seen in train)", "LOGO Holdout\n(unseen)"],
        vals2,
        color=[PALETTE["teal"], PALETTE["crimson"]],
        width=0.5,
    )
    for i, v in enumerate(vals2):
        ax2.text(i, v + 2.0, f"{v:.1f}%", ha="center", fontsize=8.5, fontweight="bold")
    ax2.set_ylim(0, 108)
    ax2.set_ylabel("Recall (%) on identical 299 SD images")
    ax2.set_title("(b) Paired Recall on Shared SD Set (n = 299)", fontsize=9.5, fontweight="bold")
    fig.subplots_adjust(wspace=0.28)
    save_fig(fig, "FIG0019")


def render_fig0020() -> None:
    rows = [r for r in read_csv("08_Evaluation/ablations/ablation_results.csv") if r["experiment_id"] != "EXP0001"]
    nice_factor = {
        "EXP0003": "Seed 43\n(Noise Floor)",
        "EXP0004": "No\nAugmentation",
        "EXP0005": "No ImageNet\nPretraining",
        "EXP0006": "Reduced Res.\n(160 x 160)",
    }
    labels = [nice_factor.get(r["experiment_id"], r["factor"]) for r in rows]
    metrics = [("delta_roc_auc", "ΔROC-AUC", PALETTE["slate"]), ("delta_balanced_accuracy", "ΔBA", PALETTE["teal"]), ("delta_mcc", "ΔMCC", PALETTE["amber"])]
    x = np.arange(len(rows))
    w = 0.25
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    for k, (col, lbl, colr) in enumerate(metrics):
        vals = [float(r[col]) for r in rows]
        ax.bar(x + (k - 1) * w, vals, w, label=lbl, color=colr)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks(x, labels, fontsize=8.5)
    ax.set_ylabel("Delta vs. Baseline ResNet-50")
    ax.set_title("One-Factor Ablations Against Two-Seed Noise Floor")
    ax.legend(loc="lower left")
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


def render_fig0031() -> None:
    """Criterion-selected lowest-error vs highest-error representative samples across DS0001-DS0005."""
    from PIL import Image

    panels = [
        # Top row (a)-(e): lowest-error / authentic baseline per dataset
        ("(a) CelebA-HQ (Real, 7.0% FPR)", "real", "ArtiFact", "_processed_dataset/processed_DS0001_PP0001/images/real/celebahq_img000764_e337de19.png"),
        ("(b) DCFace (Fake, 0.0% FNR)", "fake", "DiFF (Unseen)", "_processed_dataset/processed_DS0002_PP0002/images/DCFace/DCFace/id_0002/030.png"),
        ("(c) FFHQ (Real, 30.4% FPR)", "real", "140k Faces", "_processed_dataset/processed_DS0003_PP0003/images/real-vs-fake/valid/real/00037.png"),
        ("(d) RAISE (Real, 76.7% FPR)", "real", "Synthbuster", "_processed_dataset/DS0004_PP0006/DS0004_PP0006/images/r04e19833t.png"),
        ("(e) FairFace (Real, True Neg.)", "real", "FairFace", "_processed_dataset/processed_DS0005_PP0005/images/train/1003.png"),
        # Bottom row (f)-(j): highest-error / failure-mode subgroup per dataset
        ("(f) StyleGAN3 (Fake, 43.7% FNR)", "fake", "ArtiFact", "_processed_dataset/processed_DS0001_PP0001/images/fake/stylegan3/stylegan3_img000234_de786252.png"),
        ("(g) FreeDoM_I (Fake, 81.5% FNR)", "fake", "DiFF (Unseen)", "_processed_dataset/processed_DS0002_PP0002/images/FreeDoM_I/FreeDoM_I/id_0190/save_segs_2/0.jpg/FreeDom_Gene.png"),
        ("(h) StyleGAN (Fake, 9.2% FNR)", "fake", "140k Faces", "_processed_dataset/processed_DS0003_PP0003/images/real-vs-fake/valid/fake/00BYVMEI3I.png"),
        ("(i) DALL-E 3 (Fake, 46.9% FNR)", "fake", "Synthbuster", "_processed_dataset/DS0004_PP0006/DS0004_PP0006/images/dalle3/r0282ca06t.png"),
        ("(j) FairFace (Real, False Pos.)", "real", "FairFace", "_processed_dataset/processed_DS0005_PP0005/images/train/10120.png"),
    ]
    fig, axes = plt.subplots(2, 5, figsize=(11.2, 4.9))
    for idx, (ax, (sublbl, cls, col_hdr, rel_p)) in enumerate(zip(axes.flat, panels)):
        img_path = ROOT / rel_p
        if not img_path.exists():
            raise FileNotFoundError(f"Missing sample image for FIG0031: {img_path}")
        arr = np.asarray(Image.open(img_path).convert("RGB"))
        ax.imshow(arr)
        ax.set_xticks([])
        ax.set_yticks([])
        border_col = PALETTE["real"] if cls == "real" else PALETTE["fake"]
        for side in ("top", "right", "bottom", "left"):
            ax.spines[side].set_visible(True)
            ax.spines[side].set_color(border_col)
            ax.spines[side].set_linewidth(2.0)
        if idx < 5:
            ax.set_title(col_hdr, fontsize=10, fontweight="bold", pad=6, color="#212F3C")
        ax.set_xlabel(sublbl, fontsize=7.8, fontweight="bold", labelpad=5, color=border_col)
    fig.subplots_adjust(hspace=0.22, wspace=0.10, top=0.92, bottom=0.08, left=0.02, right=0.98)
    save_fig(fig, "FIG0031")


def render_fig0032() -> None:
    """Complete 42-panel (6 x 7) Multi-Dataset Generator and Authentic Source Visual Atlas."""
    from PIL import Image

    atlas_items = [
        ("ArtiFact: CelebA-HQ", "real", "_processed_dataset/processed_DS0001_PP0001/images/real/celebahq_img000764_e337de19.png"),
        ("ArtiFact: FFHQ", "real", "_processed_dataset/processed_DS0001_PP0001/images/real/ffhq_img001202_a6a464a3.png"),
        ("ArtiFact: MetFaces", "real", "_processed_dataset/processed_DS0001_PP0001/images/real/metfaces_img000282_d6288260.png"),
        ("ArtiFact: CIPS", "fake", "_processed_dataset/processed_DS0001_PP0001/images/fake/cips/cips_img000312_2d851fbc.png"),
        ("ArtiFact: FaceSynth.", "fake", "_processed_dataset/processed_DS0001_PP0001/images/fake/face_synthetics/face_synthetics_img001394_cfd88542.png"),
        ("ArtiFact: GANSformer", "fake", "_processed_dataset/processed_DS0001_PP0001/images/fake/gansformer/gansformer_img005477_6bf9c1a7.png"),
        ("ArtiFact: LaMa", "fake", "_processed_dataset/processed_DS0001_PP0001/images/fake/lama/lama_img000070_4f3c0127.png"),
        ("ArtiFact: MAT", "fake", "_processed_dataset/processed_DS0001_PP0001/images/fake/mat/mat_img000856_371b6efa.png"),
        ("ArtiFact: Proj. GAN", "fake", "_processed_dataset/processed_DS0001_PP0001/images/fake/projected_gan/projected_gan_img008185_bcc65884.png"),
        ("ArtiFact: SFHQ", "fake", "_processed_dataset/processed_DS0001_PP0001/images/fake/sfhq/sfhq_img000878_1fe39b18.png"),
        ("ArtiFact: StableDiff.", "fake", "_processed_dataset/processed_DS0001_PP0001/images/fake/stable_diffusion/stable_diffusion_img000256_3aed6a92.png"),
        ("ArtiFact: StarGAN", "fake", "_processed_dataset/processed_DS0001_PP0001/images/fake/stargan/stargan_img000616_1eca7f68.png"),
        ("ArtiFact: StyleGAN1", "fake", "_processed_dataset/processed_DS0001_PP0001/images/fake/stylegan1/stylegan1_img000913_6cf0b145.png"),
        ("ArtiFact: StyleGAN2", "fake", "_processed_dataset/processed_DS0001_PP0001/images/fake/stylegan2/stylegan2_img004988_654f15df.png"),
        ("ArtiFact: StyleGAN3", "fake", "_processed_dataset/processed_DS0001_PP0001/images/fake/stylegan3/stylegan3_img000234_de786252.png"),
        ("ArtiFact: TamingTr.", "fake", "_processed_dataset/processed_DS0001_PP0001/images/fake/taming_transformer/taming_transformer_img001918_f0c7ed97.png"),
        ("DiFF: CoDiff", "fake", "_processed_dataset/processed_DS0002_PP0002/images/CoDiff/CoDiff/id_0156/11.jpg/id_0630_1.png/0C_interText_optDM_2_alpha=0.0.png"),
        ("DiFF: DCFace", "fake", "_processed_dataset/processed_DS0002_PP0002/images/DCFace/DCFace/id_0002/030.png"),
        ("DiFF: DiffFace", "fake", "_processed_dataset/processed_DS0002_PP0002/images/DiffFace/DiffFace/id_0074/0.jpg/id_0233/img_id_002_000.png"),
        ("DiFF: DreamBooth", "fake", "_processed_dataset/processed_DS0002_PP0002/images/DreamBooth/DreamBooth/id_0620/1024/img_db_001.png"),
        ("DiFF: FreeDoM_I", "fake", "_processed_dataset/processed_DS0002_PP0002/images/FreeDoM_I/FreeDoM_I/id_0190/save_segs_2/0.jpg/FreeDom_Gene.png"),
        ("DiFF: FreeDoM_T", "fake", "_processed_dataset/processed_DS0002_PP0002/images/FreeDoM_T/FreeDoM_T/id_0232/clip_face_4/8380/FreeDom_Gene.png"),
        ("DiFF: HPS", "fake", "_processed_dataset/processed_DS0002_PP0002/images/HPS/HPS/id_0002/image_1/2.jpg/align_sd_gene_003_000.png"),
        ("DiFF: Imagic", "fake", "_processed_dataset/processed_DS0002_PP0002/images/Imagic/Imagic/id_0224/1.jpg_0/img_003.png"),
        ("DiFF: LoRA", "fake", "_processed_dataset/processed_DS0002_PP0002/images/LoRA/LoRA/id_0422/AnnaLynne_McCord_lora_013_000.png"),
        ("DiFF: Midjourney", "fake", "_processed_dataset/processed_DS0002_PP0002/images/Midjourney/Midjourney/id_0482/008.png"),
        ("DiFF: SDXL", "fake", "_processed_dataset/processed_DS0002_PP0002/images/SDXL/SDXL/id_0564/images_2/M1_006/sd2_gene_1.png"),
        ("DiFF: CycleDiff", "fake", "_processed_dataset/processed_DS0002_PP0002/images/cycle_diff/cycle_diff/id_0354/seed_1/10.jpg_2/gene.png"),
        ("140k: FFHQ (Real)", "real", "_processed_dataset/processed_DS0003_PP0003/images/real-vs-fake/valid/real/00037.png"),
        ("140k: StyleGAN", "fake", "_processed_dataset/processed_DS0003_PP0003/images/real-vs-fake/valid/fake/00BYVMEI3I.png"),
        ("Synth: RAISE (Real)", "real", "_processed_dataset/DS0004_PP0006/DS0004_PP0006/images/r04e19833t.png"),
        ("Synth: DALL-E 2", "fake", "_processed_dataset/DS0004_PP0006/DS0004_PP0006/images/dalle2/r0417f5e3t.png"),
        ("Synth: DALL-E 3", "fake", "_processed_dataset/DS0004_PP0006/DS0004_PP0006/images/dalle3/r0282ca06t.png"),
        ("Synth: Firefly", "fake", "_processed_dataset/DS0004_PP0006/DS0004_PP0006/images/firefly/r0341853dt.png"),
        ("Synth: GLIDE", "fake", "_processed_dataset/DS0004_PP0006/DS0004_PP0006/images/glide/r066358d3t.png"),
        ("Synth: Midjourney v5", "fake", "_processed_dataset/DS0004_PP0006/DS0004_PP0006/images/midjourney-v5/r03f70ccdt.png"),
        ("Synth: SD v1.3", "fake", "_processed_dataset/DS0004_PP0006/DS0004_PP0006/images/stable-diffusion-1-3/r065472d8t.png"),
        ("Synth: SD v1.4", "fake", "_processed_dataset/DS0004_PP0006/DS0004_PP0006/images/stable-diffusion-1-4/r03f70ccdt.png"),
        ("Synth: SD v2", "fake", "_processed_dataset/DS0004_PP0006/DS0004_PP0006/images/stable-diffusion-2/r043951a3t.png"),
        ("Synth: SDXL", "fake", "_processed_dataset/DS0004_PP0006/DS0004_PP0006/images/stable-diffusion-xl/r01170470t.png"),
        ("FairFace: Real (TN)", "real", "_processed_dataset/processed_DS0005_PP0005/images/train/1003.png"),
        ("FairFace: Real (FP)", "real", "_processed_dataset/processed_DS0005_PP0005/images/train/10120.png"),
    ]
    fig, axes = plt.subplots(6, 7, figsize=(13.2, 12.2))
    for idx, (ax, (lbl, cls, rel_p)) in enumerate(zip(axes.flat, atlas_items), 1):
        img_path = ROOT / rel_p
        if not img_path.exists():
            raise FileNotFoundError(f"Missing atlas image {idx}: {img_path}")
        arr = np.asarray(Image.open(img_path).convert("RGB"))
        ax.imshow(arr)
        ax.set_xticks([])
        ax.set_yticks([])
        col = PALETTE["real"] if cls == "real" else PALETTE["fake"]
        for side in ("top", "right", "bottom", "left"):
            ax.spines[side].set_visible(True)
            ax.spines[side].set_color(col)
            ax.spines[side].set_linewidth(1.6)
        ax.set_title(f"({idx}) {lbl}", fontsize=7.0, fontweight="bold", pad=3, color=col)
    fig.subplots_adjust(hspace=0.26, wspace=0.08, top=0.96, bottom=0.02, left=0.015, right=0.985)
    save_fig(fig, "FIG0032")


def render_fig0033() -> None:
    """EVAL0008 Large-scale M1-M18 Abstention (K=1 vs K=3) & Selective Risk-Coverage Figure (a)-(b)."""
    tracks = read_csv("08_Evaluation/EVAL0008/abstention_by_track.csv")
    rc = read_csv("08_Evaluation/EVAL0008/selective_risk_coverage.csv")

    pretty_tr = {
        "DS0001_clean": "ArtiFact\nClean",
        "DS0001_jpeg10": "ArtiFact\nJPEG-10",
        "DS0001_blur3": "ArtiFact\nBlur r=3",
        "DS0001_noise01": "ArtiFact\nNoise 0.1",
        "DS0001_downscale025": "ArtiFact\n0.25x Res",
        "DS0002_diff": "DiFF\n(Unseen DM)",
        "DS0003_140k": "140k\nFaces",
        "DS0004_synthbuster": "Synth-\nbuster",
        "DS0005_fairface": "FairFace\n(Real)",
    }
    labels = [pretty_tr.get(r["track"], r["track"]) for r in tracks]
    st_err = [float(r["standalone_error_rate"]) * 100 for r in tracks]
    k1_err = [float(r["k1_erroneous_verdict_rate"]) * 100 for r in tracks]
    k3_err = [float(r["platform_erroneous_verdict_rate"]) * 100 for r in tracks]
    abst = [float(r["platform_abstention_rate"]) * 100 for r in tracks]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.2, 4.4), gridspec_kw={"width_ratios": [1.55, 1.0]})
    x = np.arange(len(labels))
    w = 0.20
    ax1.bar(x - 1.5 * w, st_err, w, color=PALETTE["crimson"], label="Standalone ResNet-50 error (%)")
    ax1.bar(x - 0.5 * w, k1_err, w, color=PALETTE["slate"], label="M1-M18 wrong verdict (K=1, %)")
    ax1.bar(x + 0.5 * w, k3_err, w, color=PALETTE["teal"], label="M1-M18 wrong verdict (K=3, %)")
    ax1.bar(x + 1.5 * w, abst, w, color=PALETTE["amber"], alpha=0.88, label="Safe Inconclusive abstention (%)")
    ax1.set_xticks(x, labels, fontsize=7.2)
    ax1.set_ylabel("Percentage of evaluated cases (%)")
    ax1.set_ylim(0, 120)
    ax1.set_title("(a) Standalone vs. K=1 & K=3 M1-M18 Wrong Verdicts (n = 2,700)", fontsize=9.4, fontweight="bold")
    ax1.legend(loc="upper left", fontsize=7.2, ncol=2)

    cov = [float(r["coverage"]) * 100 for r in rc]
    cal_risk = [float(r["calibrated_4d_selective_risk"]) * 100 for r in rc]
    raw_risk = [float(r["raw_margin_selective_risk_at_matched_coverage"]) * 100 for r in rc]
    ax2.plot(cov, raw_risk, "s--", color=PALETTE["crimson"], lw=1.6, ms=4.3, label="Raw margin |p - t|")
    ax2.plot(cov, cal_risk, "o-", color=PALETTE["teal"], lw=2.0, ms=4.8, label="4D calibrated C_dec (M9)")
    ax2.set_xlabel("Coverage (% of cases issued Real/Fake verdict)")
    ax2.set_ylabel("Selective error rate on decided cases (%)")
    ax2.set_ylim(0, 46)
    ax2.set_title("(b) Selective Risk-Coverage Curve (Clean + Degraded, n = 1,500)", fontsize=9.4, fontweight="bold")
    ax2.legend(loc="lower right", fontsize=7.8)
    fig.subplots_adjust(wspace=0.22, top=0.88, bottom=0.16, left=0.055, right=0.985)
    save_fig(fig, "FIG0033")


def render_fig0034() -> None:
    """Multi-Backbone In-Distribution ROC (a) & Cross-Dataset Error Polarization (b)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.8, 4.3), gridspec_kw={"width_ratios": [1.0, 1.42]})

    # Panel (a): Exact ROC curves on DS0001 SPLIT0001 test (n = 7,505)
    model_specs = [
        ("EXP0008", "ViT-B/16 (AUC = 0.9750)", PALETTE["teal"], 0.490620),
        ("EXP0001", "ResNet-50 (AUC = 0.9261)", PALETTE["slate"], 0.395057),
        ("EXP0007", "EfficientNet-B4 (AUC = 0.8247)", PALETTE["amber"], 0.516066),
    ]
    for exp_id, label, color, thresh in model_specs:
        rows = read_csv(f"06_Experiments/{exp_id}/predictions/test_predictions.csv")
        yt = np.array([1 if r["class_label"] == "fake" else 0 for r in rows], dtype=np.int32)
        ps = np.array([float(r["prob_positive"]) for r in rows], dtype=np.float64)
        order = np.argsort(-ps)
        y_sorted = yt[order]
        tps = np.cumsum(y_sorted == 1) / float((yt == 1).sum())
        fps = np.cumsum(y_sorted == 0) / float((yt == 0).sum())
        step = max(1, len(tps) // 400)
        ax1.plot(np.concatenate(([0.0], fps[::step], [1.0])), np.concatenate(([0.0], tps[::step], [1.0])), lw=2.0, color=color, label=label)
        op_tpr = float(((ps >= thresh) & (yt == 1)).sum()) / float((yt == 1).sum())
        op_fpr = float(((ps >= thresh) & (yt == 0)).sum()) / float((yt == 0).sum())
        ax1.scatter([op_fpr], [op_tpr], color=color, edgecolors="black", zorder=5, s=42)

    ax1.plot([0, 1], [0, 1], "--", color=PALETTE["gray"], lw=1.0, alpha=0.6)
    ax1.set_xlabel("False Positive Rate (1 - Specificity)")
    ax1.set_ylabel("True Positive Rate (Recall)")
    ax1.set_xlim(-0.02, 1.02)
    ax1.set_ylim(-0.02, 1.02)
    ax1.set_title("(a) In-Distribution ROC Curves on ArtiFact Test (n = 7,505)", fontsize=9.4, fontweight="bold")
    ax1.legend(loc="lower right", fontsize=7.8)

    # Panel (b): Cross-Dataset Error Polarization across DS0001-DS0005
    uni = {(r["experiment_id"], r["dataset"]): r for r in read_csv("08_Evaluation/cross_backbone_generalization.csv")}
    strata = [
        ("ArtiFact\nFNR", "DS0001", "fnr"),
        ("ArtiFact\nFPR", "DS0001", "fpr"),
        ("DiFF\nFNR", "DS0002", "fnr"),
        ("140k\nFNR", "DS0003", "fnr"),
        ("140k\nFPR", "DS0003", "fpr"),
        ("Synth.\nFNR", "DS0004", "fnr"),
        ("Synth.\nFPR", "DS0004", "fpr"),
        ("FairFace\nFPR", "DS0005", "fpr"),
    ]
    x = np.arange(len(strata))
    w = 0.25
    for offset, (exp_id, short_lbl, color) in [
        (-w, ("EXP0001", "ResNet-50 (CNN)", PALETTE["slate"])),
        (0.0, ("EXP0007", "EfficientNet-B4 (CNN)", PALETTE["amber"])),
        (+w, ("EXP0008", "ViT-B/16 (Transformer)", PALETTE["teal"])),
    ]:
        vals = [float(uni[(exp_id, ds)][col]) * 100.0 for _, ds, col in strata]
        ax2.bar(x + offset, vals, w, color=color, label=short_lbl)

    ax2.set_xticks(x, [s[0] for s in strata], fontsize=7.4)
    ax2.set_ylabel("Error rate at frozen validation threshold (%)")
    ax2.set_ylim(0, 105)
    ax2.set_title("(b) Zero-Shot Cross-Dataset FNR & FPR Polarization (n = 46,369 / model)", fontsize=9.4, fontweight="bold")
    ax2.legend(loc="upper left", fontsize=7.6)
    fig.subplots_adjust(wspace=0.22, top=0.88, bottom=0.16, left=0.06, right=0.985)
    save_fig(fig, "FIG0034")


RENDERERS = {
    **{f"FIG{i:04d}": globals()[f"render_fig{i:04d}"] for i in range(1, 26)},
    "FIG0031": render_fig0031,
    "FIG0032": render_fig0032,
    "FIG0033": render_fig0033,
    "FIG0034": render_fig0034,
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
