"""Phase E3 classification metrics from validated predictions. Accuracy is never the only output."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    matthews_corrcoef,
    precision_recall_fscore_support,
    roc_auc_score,
)

COLUMNS = [
    "split",
    "positive_class",
    "threshold",
    "n",
    "n_positive",
    "n_negative",
    "tp",
    "tn",
    "fp",
    "fn",
    "accuracy",
    "precision",
    "recall",
    "sensitivity",
    "specificity",
    "f1",
    "balanced_accuracy",
    "mcc",
    "roc_auc",
    "pr_auc",
    "fpr",
    "fnr",
    "precision_macro",
    "precision_micro",
    "precision_weighted",
    "recall_macro",
    "recall_micro",
    "recall_weighted",
    "f1_macro",
    "f1_micro",
    "f1_weighted",
]

# Accuracy may appear only inside this full set.
assert "accuracy" in COLUMNS and "mcc" in COLUMNS and "pr_auc" in COLUMNS and "balanced_accuracy" in COLUMNS

COUNT_COLUMNS = ["split", "positive_class", "threshold", "n", "n_positive", "n_negative", "tp", "tn", "fp", "fn"]
METRIC_COLUMNS = [name for name in COLUMNS if name not in COUNT_COLUMNS]

# (when appropriate, how to interpret, common mistakes, publication recommendation)
METRIC_NOTES: dict[str, tuple[str, str, str, str]] = {
    "accuracy": (
        "Only alongside the rest of this table, on near-balanced data.",
        "Share of all images classified correctly.",
        "Reporting it alone; a constant classifier scores the majority share.",
        "Report with balanced accuracy and MCC, never alone.",
    ),
    "precision": (
        "When a false fake alarm is costly.",
        "Of images flagged fake, the share that are fake.",
        "Depends on the fake share in the test set; does not transfer to other prevalences.",
        "Report with recall and the threshold used.",
    ),
    "recall": (
        "When a missed fake is costly.",
        "Of fake images, the share flagged fake.",
        "Can be pushed to 1.0 by flagging everything; read it with specificity.",
        "Report with precision or specificity.",
    ),
    "sensitivity": (
        "Same as recall; the term used next to specificity.",
        "True positive rate for the fake class. Equal to recall by definition.",
        "Listing it as a separate result from recall.",
        "Use one name per table; pair with specificity.",
    ),
    "specificity": (
        "When real images must not be flagged.",
        "Of real images, the share classified real.",
        "Omitting it, which hides how often real images are flagged.",
        "Report with sensitivity.",
    ),
    "f1": (
        "One thresholded score for the fake class.",
        "Harmonic mean of precision and recall for the fake class.",
        "Ignores true negatives; changes when the positive class is swapped.",
        "Report with MCC and state which class is positive.",
    ),
    "balanced_accuracy": (
        "Always; it is robust to class imbalance.",
        "Mean of sensitivity and specificity. 0.5 is chance.",
        "Comparing values computed at thresholds tuned on different data.",
        "Primary thresholded metric (DEC0006 sanity bar).",
    ),
    "mcc": (
        "Always; uses all four confusion cells.",
        "Correlation between prediction and label, from -1 to 1. 0 is chance.",
        "Reading it on the 0-1 scale of accuracy; 0.7 is strong, not mediocre.",
        "Report as the imbalance-aware summary of the confusion matrix.",
    ),
    "roc_auc": (
        "Threshold-free ranking quality.",
        "Probability that a random fake scores above a random real image.",
        "Can look high under heavy imbalance while precision is poor.",
        "Primary threshold-free metric; report with PR-AUC.",
    ),
    "pr_auc": (
        "Threshold-free quality for the fake class, especially under imbalance.",
        "Average precision over recall levels. Chance level is the fake share.",
        "Comparing across test sets with different fake shares.",
        "Report with ROC-AUC and the fake share.",
    ),
    "fpr": (
        "When the cost of flagging a real image matters.",
        "Share of real images flagged fake. Equal to 1 - specificity.",
        "Confusing it with the false discovery rate (1 - precision).",
        "Report with FNR at the same threshold.",
    ),
    "fnr": (
        "When the cost of missing a fake matters.",
        "Share of fake images classified real. Equal to 1 - recall.",
        "Reporting FPR without FNR, which hides one error type.",
        "Report with FPR at the same threshold.",
    ),
    "macro": (
        "Class-symmetric view; each class counts equally.",
        "Unweighted mean of the per-class real and fake scores.",
        "Mixing it up with weighted averages.",
        "Report macro F1 when the two classes matter equally.",
    ),
    "micro": (
        "Rarely useful in binary classification.",
        "Pools all decisions. In binary tasks every micro score equals accuracy.",
        "Presenting micro F1 as a separate result from accuracy.",
        "Keep in the CSV for completeness; do not report as its own result.",
    ),
    "weighted": (
        "When per-class scores should follow class frequency.",
        "Per-class scores averaged by class support.",
        "Hiding weak minority-class scores behind the majority class.",
        "Report only with macro averages.",
    ),
}


def note_key(column: str) -> str:
    suffix = column.rsplit("_", 1)[-1]
    return suffix if suffix in {"macro", "micro", "weighted"} else column


def require_validated(report_path: Path) -> None:
    """Metrics may only use predictions whose E1-E2 report passed."""

    if not report_path.is_file():
        raise FileNotFoundError(f"prediction validation report not found: {report_path}")
    if "**Status:** PASS" not in report_path.read_text(encoding="utf-8"):
        raise ValueError(f"prediction validation did not pass: {report_path}")


def _ratio(num: float, den: float) -> float:
    return float(num / den) if den else 0.0


def _average(y_true: np.ndarray, y_pred: np.ndarray, kind: str) -> dict[str, float]:
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average=kind, zero_division=0, labels=[0, 1]
    )
    return {f"precision_{kind}": float(precision), f"recall_{kind}": float(recall), f"f1_{kind}": float(f1)}


def classification_row(
    split: str,
    y_true: np.ndarray,
    y_prob: np.ndarray,
    y_pred: np.ndarray,
    threshold: float,
    positive_class: str,
) -> dict:
    """One split. Thresholded metrics use the saved decisions, not a recomputed threshold."""

    y_true = np.asarray(y_true).astype(int).ravel()
    y_prob = np.asarray(y_prob, dtype=float).ravel()
    y_pred = np.asarray(y_pred).astype(int).ravel()
    if not (len(y_true) == len(y_prob) == len(y_pred)) or len(y_true) == 0:
        raise ValueError("y_true, y_prob, and y_pred must be non-empty and the same length")
    if not set(np.unique(y_true)).issubset({0, 1}) or not set(np.unique(y_pred)).issubset({0, 1}):
        raise ValueError("y_true and y_pred must be 0 or 1")
    if np.any((y_prob < 0) | (y_prob > 1)) or np.any(np.isnan(y_prob)):
        raise ValueError("y_prob must be finite and inside [0, 1]")

    tp = int(np.sum((y_pred == 1) & (y_true == 1)))
    tn = int(np.sum((y_pred == 0) & (y_true == 0)))
    fp = int(np.sum((y_pred == 1) & (y_true == 0)))
    fn = int(np.sum((y_pred == 0) & (y_true == 1)))
    precision = _ratio(tp, tp + fp)
    recall = _ratio(tp, tp + fn)
    specificity = _ratio(tn, tn + fp)
    both = len(np.unique(y_true)) == 2
    row = {
        "split": split,
        "positive_class": positive_class,
        "threshold": float(threshold),
        "n": int(y_true.size),
        "n_positive": int(y_true.sum()),
        "n_negative": int((y_true == 0).sum()),
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "accuracy": _ratio(tp + tn, y_true.size),
        "precision": precision,
        "recall": recall,
        "sensitivity": recall,
        "specificity": specificity,
        "f1": _ratio(2 * precision * recall, precision + recall),
        "balanced_accuracy": (recall + specificity) / 2,
        "mcc": float(matthews_corrcoef(y_true, y_pred)),
        "roc_auc": float(roc_auc_score(y_true, y_prob)) if both else float("nan"),
        "pr_auc": float(average_precision_score(y_true, y_prob)) if both else float("nan"),
        "fpr": _ratio(fp, fp + tn),
        "fnr": _ratio(fn, fn + tp),
    }
    for kind in ("macro", "micro", "weighted"):
        row.update(_average(y_true, y_pred, kind))
    missing = [name for name in COLUMNS if name not in row]
    if missing:
        raise RuntimeError(f"metric row is missing {missing}")
    return row


def metrics_frame(predictions: pd.DataFrame, positive_class: str) -> pd.DataFrame:
    required = {"split", "y_true", "y_prob", "y_pred", "threshold"}
    missing = required - set(predictions.columns)
    if missing:
        raise ValueError(f"predictions are missing column(s): {', '.join(sorted(missing))}")
    rows = []
    for split, frame in predictions.groupby("split", sort=True):
        thresholds = frame["threshold"].unique()
        if len(thresholds) != 1:
            raise ValueError(f"{split} has more than one threshold")
        rows.append(
            classification_row(
                str(split),
                frame["y_true"].to_numpy(),
                frame["y_prob"].to_numpy(),
                frame["y_pred"].to_numpy(),
                float(thresholds[0]),
                positive_class,
            )
        )
    return pd.DataFrame(rows)[COLUMNS]


def write_metrics(predictions_path: Path, out_path: Path, positive_class: str) -> pd.DataFrame:
    frame = metrics_frame(pd.read_csv(predictions_path), positive_class)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(out_path, index=False)
    return frame


def _fmt(value: float) -> str:
    return "n/a" if pd.isna(value) else f"{value:.4f}"


def render_report(frame: pd.DataFrame, evaluation_id: str, experiment_id: str, predictions_sha256: str, date: str) -> str:
    """Metrics section for the evaluation report. Numbers come from `frame` only."""

    splits = [s for s in ("test", "val") if s in set(frame["split"])]
    rows = {s: frame[frame["split"] == s].iloc[0] for s in splits}
    first = rows[splits[0]]
    lines = [
        f"# Classification Metrics: {evaluation_id}",
        "",
        f"**Experiment:** {experiment_id}",
        "**Phase:** E3",
        f"**Date:** {date}",
        "",
        f"Source: `08_Evaluation/{experiment_id}/predictions.csv` (SHA-256 `{predictions_sha256}`), "
        f"validated in `prediction_validation_report.md`. Values: `classification_metrics.csv`.",
        "",
        f"Positive class: `{first['positive_class']}`. Thresholded metrics use the saved decisions at threshold "
        f"{first['threshold']:.4f}. The threshold was chosen on `val`, so `val` values are optimistic. Report `test`.",
        "",
        "## Counts",
        "",
        "| Split | n | fake | real | TP | TN | FP | FN |",
        "|-------|---|------|------|----|----|----|----|",
    ]
    for s in splits:
        r = rows[s]
        lines.append(f"| {s} | {r['n']} | {r['n_positive']} | {r['n_negative']} | {r['tp']} | {r['tn']} | {r['fp']} | {r['fn']} |")
    lines += ["", "## Metrics", "", "| Metric | " + " | ".join(splits) + " |", "|--------|" + "|".join("------" for _ in splits) + "|"]
    for name in METRIC_COLUMNS:
        lines.append(f"| {name} | " + " | ".join(_fmt(rows[s][name]) for s in splits) + " |")
    test = rows[splits[0]]
    lines += [
        "",
        "## Reading the table",
        "",
        f"- Fake share in `{splits[0]}` is {test['n_positive'] / test['n']:.3f}. That is the chance level for PR-AUC.",
        f"- FNR is {_fmt(test['fnr'])} and FPR is {_fmt(test['fpr'])} on `{splits[0]}`. "
        + ("Missed fakes are the larger error." if test["fnr"] > test["fpr"] else "Flagged real images are the larger error."),
        "- Micro averages equal accuracy in binary classification. They are not separate results.",
        "- Accuracy is never reported without balanced accuracy, MCC, ROC-AUC, and PR-AUC.",
        "- No confidence intervals here. Statistical testing is Phase E11.",
        "",
        "## Metric notes",
        "",
        "| Metric | When appropriate | How to interpret | Common mistakes | Publication recommendation |",
        "|--------|------------------|------------------|-----------------|----------------------------|",
    ]
    for key, (when, meaning, mistakes, publish) in METRIC_NOTES.items():
        label = f"{key} averages" if key in {"macro", "micro", "weighted"} else key
        lines.append(f"| {label} | {when} | {meaning} | {mistakes} | {publish} |")
    return "\n".join(lines) + "\n"
