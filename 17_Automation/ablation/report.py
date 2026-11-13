"""ablation_report.md. Numbers come from the comparison frame; no cause is asserted."""

from __future__ import annotations

import pandas as pd

from .compare import direction
from .plan import AblationPlan

HEADLINE = ["roc_auc", "balanced_accuracy", "mcc", "fnr", "fpr", "ece"]


def _f(v, d: int = 4) -> str:
    return "—" if v is None or pd.isna(v) else f"{float(v):.{d}f}"


def _s(v) -> str:
    return "—" if v is None or pd.isna(v) else f"{float(v):+.4f}"


def render_report(frame: pd.DataFrame, plan: AblationPlan, date: str) -> str:
    base = frame.iloc[0]
    noise = frame[frame["experiment_id"] == plan.noise_reference].iloc[0]
    lines = [
        "# Ablation Study: STEP-048",
        "",
        f"**Baseline:** {plan.baseline} (MODEL0001)  ",
        "**Phase:** E10  ",
        f"**Date:** {date}",
        "",
        f"Every ablation changes exactly one factor of {plan.baseline} (checked when the experiment was created; DEC0008). "
        "All use DS0001 / v1.0 / PP0001 / SPLIT0001, the same epoch budget, and the same threshold rule (max balanced accuracy on val). "
        "Metrics are on the SPLIT0001 test partition at each model's own val-chosen threshold.",
        "",
        f"**Noise floor:** {plan.noise_reference} changes only the training seed. Its differences from {plan.baseline} are the run-to-run "
        "variation. A difference no larger than that is marked `within seed noise`.",
        "",
        "## Test metrics",
        "",
        "| Experiment | Factor | " + " | ".join(HEADLINE) + " | Best epoch | Minutes |",
        "|---|---|" + "|".join("---" for _ in HEADLINE) + "|---|---|",
    ]
    for _, r in frame.iterrows():
        lines.append(f"| {r['experiment_id']} | {r['factor']} | " + " | ".join(_f(r[m]) for m in HEADLINE)
                     + f" | {r['best_epoch'] if pd.notna(r['best_epoch']) else '—'} | {_f(r['training_minutes'], 1)} |")
    lines += ["", f"## Differences from {plan.baseline}", "",
              "| Experiment | Factor | " + " | ".join(f"Δ{m}" for m in HEADLINE) + " |",
              "|---|---|" + "|".join("---" for _ in HEADLINE) + "|"]
    for _, r in frame.iloc[1:].iterrows():
        cells = []
        for m in HEADLINE:
            flag = r[f"beyond_seed_{m}"]
            mark = "" if flag is None or pd.isna(flag) else ("" if flag else " (noise)")
            cells.append(_s(r[f"delta_{m}"]) + mark)
        lines.append(f"| {r['experiment_id']} | {r['factor']} | " + " | ".join(cells) + " |")
    lines += ["", "`(noise)`: the difference is no larger than the seed replicate's for that metric.", "", "## Answers", ""]
    lines.append(f"- **{noise['factor']}** ({noise['experiment_id']}): {noise['question']} ROC-AUC changes by {_s(noise['delta_roc_auc'])}, "
                 f"balanced accuracy by {_s(noise['delta_balanced_accuracy'])}, MCC by {_s(noise['delta_mcc'])}.")
    for _, r in frame.iloc[1:].iterrows():
        if r["experiment_id"] == plan.noise_reference:
            continue
        beyond = [m for m in HEADLINE if r[f"beyond_seed_{m}"]]
        summary = ", ".join(f"{m} {direction(m, r[f'delta_{m}'])} ({_s(r[f'delta_{m}'])})" for m in beyond) or "no headline metric beyond seed noise"
        lines.append(f"- **{r['factor']}** ({r['experiment_id']}): {r['question']} Beyond seed noise: {summary}.")
    lines += [
        "",
        "Per-metric values and flags for all metrics: `ablation_results.csv`. Figure spec: FIG0020.",
        "",
        "## Limits",
        "",
        "- One seed per configuration; the noise floor comes from a single seed pair. Formal tests are STEP-049 (Phase E11).",
        "- In-distribution test only (SPLIT0001). Robustness and cross-dataset behaviour of the ablations were not measured.",
        f"- Every ablation reuses {plan.baseline}'s learning rate and schedule. For the no-pretraining run this keeps one factor changed, "
        "but it is not a tuned from-scratch training.",
        "- Evidence-module, confidence, and explainability ablations wait until those modules exist (DEC0008).",
    ]
    return "\n".join(lines) + "\n"
