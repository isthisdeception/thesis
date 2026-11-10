"""robustness_report.md. Numbers come from the frames; causes are not asserted."""

from __future__ import annotations

import pandas as pd

from .config import CLEAN


def _f(value, digits: int = 4) -> str:
    return "n/a" if pd.isna(value) else f"{float(value):.{digits}f}"


def _signed(value) -> str:
    return "n/a" if pd.isna(value) else f"{float(value):+.4f}"


def render_report(metrics: pd.DataFrame, flips: pd.DataFrame, summary: pd.DataFrame, manifest: dict,
                  tolerance: float, ranking_kept: float, date: str) -> str:
    clean = metrics[metrics["condition"] == CLEAN].iloc[0]
    check = manifest.get("clean_check") or {}
    counts = summary["pattern"].value_counts()
    worst = summary.sort_values(["delta_balanced_accuracy", "perturbation"]).iloc[0]
    to_fake = int((summary["flip_direction"] == "to_fake").sum())
    to_real = int((summary["flip_direction"] == "to_real").sum())

    lines = [
        f"# Robustness Evaluation: {manifest['evaluation_id']}",
        "",
        f"**Experiment:** {manifest['experiment_id']}  ",
        f"**Model:** {manifest['model_id']} (export SHA-256 `{manifest['export_sha256'][:12]}…`)  ",
        "**Phase:** E7  ",
        f"**Date:** {date}",
        "",
        f"{manifest['n_images']} `{manifest['split']}` images, {len(metrics) - 1} perturbed conditions plus clean. "
        f"Config: `{manifest['config']}` (SHA-256 `{manifest['config_sha256'][:12]}…`). Probabilities: `robustness_probs.csv`. "
        f"Device: {manifest.get('device', 'n/a')}.",
        "",
        f"Clean check: the clean run reproduces `predictions.csv` with max |diff| {check.get('max_abs_diff', float('nan')):.2e} "
        f"(limit {check.get('atol', 'n/a')}) and {check.get('decision_mismatches', 'n/a')} decision mismatch(es).",
        "",
        f"Decisions use the frozen threshold {clean['threshold']:.4f}. No threshold is chosen on perturbed data.",
        "",
        "## Terms",
        "",
        "- **Degradation:** change against clean (`delta_*`). Clean balanced accuracy is "
        f"{_f(clean['balanced_accuracy'])}, ROC-AUC {_f(clean['roc_auc'])}.",
        f"- **Tolerance level:** the strongest level up to which balanced accuracy stays within {tolerance} of clean at every milder level. "
        "Blank means even the mildest level falls outside.",
        f"- **Pattern:** `robust` (worst drop within {tolerance}); `threshold_shift` (balanced accuracy drops but ROC-AUC drops "
        f"less than {ranking_kept}: ranking kept, probabilities moved, so recalibration might recover it without retraining); "
        "`ranking_loss` (ROC-AUC drops too).",
        "- **Flip direction:** whether changed decisions at the worst level mostly move to fake or to real.",
        "",
        "## Summary by perturbation",
        "",
        "| Perturbation | Levels (mild → strong) | Tolerance level | Worst level | Worst BA | ΔBA | ΔROC-AUC | ΔFNR | ΔFPR | Flip rate | Direction | Pattern | Most affected group (Δ error) |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for _, r in summary.iterrows():
        lines.append(
            f"| {r['perturbation']} | {r['levels']} | {r['tolerance_level'] or '—'} | {r['worst_level']} | {_f(r['worst_balanced_accuracy'])} | "
            f"{_signed(r['delta_balanced_accuracy'])} | {_signed(r['delta_roc_auc'])} | {_signed(r['delta_fnr'])} | {_signed(r['delta_fpr'])} | "
            f"{_f(r['flip_rate'], 3)} | {r['flip_direction']} | {r['pattern']} | {r['most_affected_group']} ({_signed(r['most_affected_delta'])}) |"
        )
    lines += [
        "",
        f"- Patterns: " + ", ".join(f"`{k}` {v}" for k, v in counts.items()) + ".",
        f"- Largest balanced-accuracy drop: `{worst['perturbation']}` at {worst['worst_level']} ({_signed(worst['delta_balanced_accuracy'])}).",
        f"- At the worst level, changed decisions mostly move to fake for {to_fake} perturbation(s) and to real for {to_real}.",
        "",
        "## All conditions",
        "",
        "| Condition | BA | ΔBA | ROC-AUC | ΔROC-AUC | FNR | FPR | ECE | Mean P(fake) | Flip rate |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    fl = flips.set_index("condition")
    for _, r in metrics.iterrows():
        lines.append(
            f"| {r['condition']} | {_f(r['balanced_accuracy'])} | {_signed(r['delta_balanced_accuracy'])} | {_f(r['roc_auc'])} | "
            f"{_signed(r['delta_roc_auc'])} | {_f(r['fnr'])} | {_f(r['fpr'])} | {_f(r['ece'])} | {_f(r['mean_prob'])} | {_f(fl.loc[r['condition'], 'flip_rate'], 3)} |"
        )
    lines += [
        "",
        "Per-generator and per-source error rates for every condition: `robustness_by_group.csv`. Figure specs: FIG0016, FIG0017.",
        "",
        "## Limits",
        "",
        "- Perturbations are synthetic and applied after preprocessing (to the 224 px face crop), not to the original upload.",
        "- One model, one seed, one split. No statistical test (Phase E11).",
        "- `threshold_shift` marks where recalibration might help; it has not been tried. Any recalibration needs a new Evaluation ID.",
        "- Patterns describe where performance changes, not why.",
    ]
    return "\n".join(lines) + "\n"
