"""Calibration and threshold section for the evaluation report. Numbers come from the frames only."""

from __future__ import annotations

import pandas as pd

SUMMARY_FIELDS = ["n", "ece", "mce", "brier", "brier_reference", "log_loss", "mean_probability", "fraction_positive", "mean_confidence", "accuracy"]
POINT_FIELDS = ["threshold", "recall", "specificity", "precision", "fpr", "fnr", "balanced_accuracy", "f1", "mcc"]


def _fmt(value) -> str:
    if isinstance(value, (int,)) or (hasattr(value, "dtype") and value.dtype.kind in "iu"):
        return str(int(value))
    return "n/a" if pd.isna(value) else f"{float(value):.4f}"


def render_report(
    summary: pd.DataFrame,
    reliability: pd.DataFrame,
    confidence: pd.DataFrame,
    points: pd.DataFrame,
    evaluation_id: str,
    experiment_id: str,
    predictions_sha256: str,
    date: str,
) -> str:
    splits = [s for s in ("test", "val") if s in set(summary["split"])]
    by_split = {s: summary[summary["split"] == s].iloc[0] for s in splits}
    head = splits[0]
    t = by_split[head]
    rel = reliability[(reliability["split"] == head) & (reliability["count"] > 0)]
    worst = rel.loc[rel["gap"].abs().idxmax()]
    conf = confidence[(confidence["split"] == head) & (confidence["bin"] >= 0) & (confidence["count"] > 0)]
    over = int(((conf["mean_confidence"] - conf["accuracy"]) > 0.02).sum())
    top = conf[conf["bin"] == conf["bin"].max()].iloc[0]
    frozen = points[(points["point"] == "frozen") & (points["split"] == head)].iloc[0]

    lines = [
        f"# Calibration and Threshold Analysis: {evaluation_id}",
        "",
        f"**Experiment:** {experiment_id}",
        "**Phases:** E4, E5",
        f"**Date:** {date}",
        "",
        f"Source: `08_Evaluation/{experiment_id}/predictions.csv` (SHA-256 `{predictions_sha256}`), "
        "validated in `prediction_validation_report.md`. No figures are rendered (A.9); specs are FIG0011–FIG0013.",
        "",
        "## Probability, confidence, reliability",
        "",
        "- **Probability** is the model's P(fake) for an image. It is a score, not forensic certainty.",
        "- **Confidence** is the probability of the predicted class, max(p, 1 − p) at the decision taken.",
        "- **Reliability** is how often predictions at a given probability or confidence are right. "
        "Calibration compares probability with the observed fake share; the confidence table compares confidence with accuracy.",
        "",
        "## Calibration (E4)",
        "",
        f"Equal-width bins: {int(t['bins'])}. `brier_reference` is the Brier score of always predicting the fake share.",
        "",
        "| Metric | " + " | ".join(splits) + " |",
        "|--------|" + "|".join("------" for _ in splits) + "|",
    ]
    for name in SUMMARY_FIELDS:
        lines.append(f"| {name} | " + " | ".join(_fmt(by_split[s][name]) for s in splits) + " |")
    direction = "below" if t["mean_probability"] < t["fraction_positive"] else "above"
    lines += [
        "",
        f"- On `{head}`, the mean P(fake) is {t['mean_probability']:.3f}, {direction} the fake share of {t['fraction_positive']:.3f}.",
        f"- The largest bin gap is {worst['gap']:+.3f} in [{worst['lower']:.3f}, {worst['upper']:.3f}] "
        f"({int(worst['count'])} images). A positive gap means more fakes than the probability implies.",
        f"- Confidence exceeds accuracy by more than 0.02 in {over} of {len(conf)} confidence bins.",
        f"- {top['share']:.1%} of `{head}` decisions have confidence ≥ {top['lower']:.2f}; their accuracy is {top['accuracy']:.3f}.",
        "",
        "Bins are in `reliability.csv` and `confidence_distribution.csv`. Bin `-1` holds decisions whose confidence is "
        "below 0.5, which happens because the threshold is not 0.5.",
        "",
        "## Threshold analysis (E5)",
        "",
        f"Every threshold is chosen on `val`, then applied to `{head}` unchanged. Sweep: `threshold_sweep.csv` (0.00–1.00, step 0.01).",
        "",
        "| Point | Criterion | " + " | ".join(POINT_FIELDS) + " |",
        "|-------|-----------|" + "|".join("------" for _ in POINT_FIELDS) + "|",
    ]
    for _, row in points[points["split"] == head].iterrows():
        lines.append(f"| {row['point']} | {row['criterion']} | " + " | ".join(_fmt(row[f]) for f in POINT_FIELDS) + " |")
    lines += [
        "",
        "Recomputed decisions use `prob >= threshold`. One `val` row sits within 1e-5 of the frozen threshold because the "
        "CSV rounded its probability, so `val` counts for `frozen` can differ from `classification_metrics.csv` by one image. "
        f"`{head}` counts match.",
        "",
        "## Recommended operating points",
        "",
        f"- **Reporting:** `frozen` (threshold {frozen['threshold']:.4f}). Its selection rule was set in the EXP0001 config before "
        "training, and §7.2 forbids changing the evaluation after seeing results. It equals the ROC (Youden J) optimum on `val`.",
    ]
    for _, row in points[(points["split"] == head) & points["point"].isin(["high_sensitivity", "high_specificity"])].iterrows():
        lines.append(
            f"- **{row['use'].split(':')[0]}:** `{row['point']}` (threshold {row['threshold']:.4f}). "
            f"On `{head}`: FNR {row['fnr']:.3f}, FPR {row['fpr']:.3f}, versus FNR {frozen['fnr']:.3f}, FPR {frozen['fpr']:.3f} for `frozen`."
        )
    lines += [
        "- `max_f1` and `fixed_0.5` are listed for comparison only.",
        "",
        "## For Module 9",
        "",
        f"Raw P(fake) is not shown as certainty. ECE is {t['ece']:.3f} and MCE is {t['mce']:.3f} on `{head}`. "
        "Post-hoc calibration fitted on `val` (for example temperature scaling) has not been applied; any later use needs a new Evaluation ID.",
    ]
    return "\n".join(lines) + "\n"
