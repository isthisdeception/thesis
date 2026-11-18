"""comparison_report.md and evaluation_report.md. Figures are not rendered."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

HEADLINE = ["roc_auc", "pr_auc", "balanced_accuracy", "mcc", "fnr", "fpr", "ece"]


def _f(value, digits: int = 4) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)) or pd.isna(value):
        return "—"
    return f"{float(value):.{digits}f}"


def _s(value) -> str:
    if value is None or pd.isna(value):
        return "—"
    return f"{float(value):+.4f}"


def render_comparison(ranked: pd.DataFrame, excluded: pd.DataFrame, date: str) -> str:
    base = ranked[ranked["role"] == "baseline"].iloc[0]
    lines = [
        "# Comparison Study: STEP-050",
        "",
        f"**Baseline:** {base.experiment_id} ({base.model_id})  ",
        "**Phase:** E16  ",
        f"**Date:** {date}",
        "",
        "A row is ranked only when it keeps the baseline data invariants: dataset DS0001, version v1.0, "
        f"pipeline {base.pipeline_id}, split {base.split_id}. Labeled one-factor ablations stay in that set. "
        "Accuracy is one column of the metric set, never the comparison by itself.",
        "",
        "The ROC-AUC difference column is challenger minus baseline. Its interval and `run difference` come from "
        "STEP-049. `superiority_claim` is `none` on every row. A difference between two saved runs is not a claim "
        "that one method is superior.",
        "",
        "## Ranked experiments",
        "",
        "| Experiment | Factor | " + " | ".join(HEADLINE) + " | Delta ROC-AUC | Run difference |",
        "|---|---|" + "---|" * len(HEADLINE) + "---|---|",
    ]
    for row in ranked.itertuples(index=False):
        cells = " | ".join(_f(getattr(row, metric)) for metric in HEADLINE)
        lines.append(f"| {row.experiment_id} | {row.factor} | {cells} | {_s(row.delta_roc_auc)} | {row.roc_auc_run_difference or '—'} |")
    lines += ["", "## Not ranked", "", "| Experiment | Reason |", "|---|---|"]
    for row in excluded.itertuples(index=False):
        lines.append(f"| {row.experiment_id} | {row.reason} |")
    lines += [
        "",
        "EXP0002 trains and tests on SPLIT0002, with Stable Diffusion held out. Its unseen-generator result stays in "
        "`08_Evaluation/EVAL0002/unseen_generator/unseen_report.md` and is not a row of the ranked table.",
        "",
        "Reading the ranked deltas: the seed replicate's ROC-AUC interval includes zero. The three factor runs are "
        "lower than EXP0001 on this test split, and each adjusted interval excludes zero. That supports a difference "
        "between those saved runs. It does not support a superiority claim, because each configuration has one seed.",
        "",
    ]
    return "\n".join(lines)


def _robustness_sentence(repo: Path) -> str:
    frame = pd.read_csv(repo / "08_Evaluation/EVAL0001/robustness/robustness_metrics.csv")
    clean = frame[frame["condition"] == "clean"].iloc[0]
    perturbed = frame[frame["condition"] != "clean"]
    worst = perturbed.loc[perturbed["balanced_accuracy"].idxmin()]
    return (
        f"Clean balanced accuracy is {_f(clean.balanced_accuracy)} and clean ROC-AUC is {_f(clean.roc_auc)}. "
        f"Across {len(perturbed)} perturbed conditions, the lowest balanced accuracy is {_f(worst.balanced_accuracy)} "
        f"at `{worst.condition}` (ROC-AUC {_f(worst.roc_auc)}). "
        "The full curves are in `08_Evaluation/EVAL0001/robustness/robustness_report.md`."
    )


def _generalization_sentence(repo: Path) -> str:
    frame = pd.read_csv(repo / "08_Evaluation/EVAL0001/generalization/cross_dataset_metrics.csv")
    bits = []
    for row in frame.itertuples(index=False):
        if pd.notna(row.roc_auc):
            bits.append(f"{row.dataset} ROC-AUC {_f(row.roc_auc)}")
        else:
            bits.append(
                f"{row.dataset} is one class (fake={int(row.n_fake)}, real={int(row.n_real)}), so ROC-AUC is undefined"
            )
    paired = pd.read_csv(repo / "08_Evaluation/EVAL0002/unseen_generator/unseen_paired.csv").iloc[0]
    return (
        "MODEL0001 at its frozen threshold, from `cross_dataset_metrics.csv`: " + "; ".join(bits) + ". "
        f"On the same {int(paired.n)} `{paired.generator}` images, MODEL0001 recall is {paired.recall_reference:.1%} "
        f"and MODEL0008 recall is {paired.recall_held_out:.1%}. "
        "That pair uses SPLIT0002 and is not ranked above."
    )


def render_evaluation(ranked: pd.DataFrame, repo: Path, date: str) -> str:
    base = ranked[ranked["role"] == "baseline"].iloc[0]
    calibration = pd.read_csv(repo / "08_Evaluation/EVAL0001/calibration_summary.csv")
    test = calibration[calibration["split"] == "test"].iloc[0]
    return "\n".join([
        "# Evaluation Report",
        "",
        "**Evaluation IDs:** EVAL0001–EVAL0006  ",
        "**Template:** 10  ",
        f"**Date:** {date}",
        "",
        "## Metrics",
        "",
        f"The ranked comparison is {', '.join(ranked.experiment_id)}. Test metrics are in `comparison_tables.csv`. "
        f"For {base.experiment_id} / {base.model_id} on the SPLIT0001 test split: ROC-AUC {_f(base.roc_auc)}, "
        f"PR-AUC {_f(base.pr_auc)}, balanced accuracy {_f(base.balanced_accuracy)}, MCC {_f(base.mcc)}, "
        f"FNR {_f(base.fnr)}, FPR {_f(base.fpr)}. Accuracy is {_f(base.accuracy)} and is reported only inside that set.",
        "",
        "The per-split E3 table, including accuracy, is `08_Evaluation/EVAL0001/classification_metrics.csv`.",
        "",
        "## Analysis",
        "",
        "EXP0003 changes only the training seed. Its test ROC-AUC difference from EXP0001 is inside the 95% interval "
        "that includes zero, and the exact McNemar test does not find a decision difference. "
        "Removing augmentation, training without ImageNet weights, and reducing the input to 160 pixels each produce "
        "a lower test ROC-AUC on this split; the Bonferroni-adjusted intervals exclude zero. "
        "Those are differences between the saved runs. `superiority_claim` remains `none`.",
        "",
        "## Calibration",
        "",
        f"EVAL0001 test ECE is {_f(test.ece)}, MCE is {_f(test.mce)}, and Brier score is {_f(test.brier)} "
        f"at the frozen threshold. Detail: `08_Evaluation/EVAL0001/calibration_threshold.md`.",
        "",
        "## Robustness",
        "",
        _robustness_sentence(repo),
        "",
        "## Generalization",
        "",
        _generalization_sentence(repo),
        "",
        "## Ablation",
        "",
        "The one-factor questions and the seed-pair noise floor are in `08_Evaluation/ablations/ablation_report.md`. "
        "The statistical reading of those same runs is in `08_Evaluation/statistics/statistics_report.md`.",
        "",
        "## Failure analysis",
        "",
        f"On the EVAL0001 test split the fake miss rate is {_f(base.fnr)} and the false-fake rate is {_f(base.fpr)}. "
        "Where those errors concentrate, and which causes are only hypotheses, is `08_Evaluation/EVAL0001/failure_analysis.md`.",
        "",
        "## Statistical testing",
        "",
        "Intervals, exact McNemar tests, two-seed variance, and the decision not to run Wilcoxon across seeds are in "
        "`08_Evaluation/statistics/`. No superiority claim is made.",
        "",
    ])
