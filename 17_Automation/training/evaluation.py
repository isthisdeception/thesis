"""Threshold selection and the canonical metric set, computed from saved predictions."""

from __future__ import annotations

import numpy as np
from sklearn.metrics import average_precision_score, matthews_corrcoef, roc_auc_score


def _confusion(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[int, int, int, int]:
    tp = int(np.sum((y_pred == 1) & (y_true == 1)))
    tn = int(np.sum((y_pred == 0) & (y_true == 0)))
    fp = int(np.sum((y_pred == 1) & (y_true == 0)))
    fn = int(np.sum((y_pred == 0) & (y_true == 1)))
    return tp, tn, fp, fn


def _ratio(num: float, den: float) -> float:
    return float(num / den) if den else 0.0


def _check_inputs(y_true: np.ndarray, prob: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    y_true = np.asarray(y_true).astype(int).ravel()
    prob = np.asarray(prob, dtype=float).ravel()
    if y_true.shape != prob.shape:
        raise ValueError(f"y_true and prob lengths differ: {y_true.shape} vs {prob.shape}")
    if y_true.size == 0:
        raise ValueError("cannot compute metrics on an empty prediction set")
    if not set(np.unique(y_true)) <= {0, 1}:
        raise ValueError("y_true must be binary 0/1 (1 = positive class)")
    if np.any((prob < 0) | (prob > 1)) or np.any(np.isnan(prob)):
        raise ValueError("probabilities must be finite values in [0, 1]")
    return y_true, prob


def thresholded_metrics(y_true: np.ndarray, prob: np.ndarray, threshold: float) -> dict[str, float]:
    y_true, prob = _check_inputs(y_true, prob)
    y_pred = (prob >= threshold).astype(int)
    tp, tn, fp, fn = _confusion(y_true, y_pred)
    precision = _ratio(tp, tp + fp)
    recall = _ratio(tp, tp + fn)
    specificity = _ratio(tn, tn + fp)
    return {
        "threshold": float(threshold),
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "fpr": _ratio(fp, fp + tn),
        "fnr": _ratio(fn, fn + tp),
        "f1": _ratio(2 * precision * recall, precision + recall),
        "balanced_accuracy": (recall + specificity) / 2,
        "accuracy": _ratio(tp + tn, y_true.size),
        "mcc": float(matthews_corrcoef(y_true, y_pred)),
    }


def expected_calibration_error(y_true: np.ndarray, prob: np.ndarray, bins: int) -> float:
    """Binary ECE over equal-width bins of the positive-class probability."""

    y_true, prob = _check_inputs(y_true, prob)
    edges = np.linspace(0.0, 1.0, bins + 1)
    idx = np.clip(np.digitize(prob, edges[1:-1], right=True), 0, bins - 1)
    ece = 0.0
    for b in range(bins):
        mask = idx == b
        if mask.any():
            ece += mask.mean() * abs(prob[mask].mean() - y_true[mask].mean())
    return float(ece)


def calibration_table(y_true: np.ndarray, prob: np.ndarray, bins: int) -> list[dict[str, float]]:
    """Per-bin data for a reliability diagram (figure is rendered later, per A.9)."""

    y_true, prob = _check_inputs(y_true, prob)
    edges = np.linspace(0.0, 1.0, bins + 1)
    idx = np.clip(np.digitize(prob, edges[1:-1], right=True), 0, bins - 1)
    rows = []
    for b in range(bins):
        mask = idx == b
        rows.append(
            {
                "bin": b,
                "lower": float(edges[b]),
                "upper": float(edges[b + 1]),
                "count": int(mask.sum()),
                "mean_confidence": float(prob[mask].mean()) if mask.any() else float("nan"),
                "fraction_positive": float(y_true[mask].mean()) if mask.any() else float("nan"),
            }
        )
    return rows


def select_threshold(y_true: np.ndarray, prob: np.ndarray, criterion: str) -> float:
    """Pick the operating threshold on validation data only."""

    y_true, prob = _check_inputs(y_true, prob)
    if criterion == "fixed_0.5":
        return 0.5
    if criterion not in {"max_balanced_accuracy", "max_f1"}:
        raise ValueError(f"unknown threshold criterion {criterion!r}")
    candidates = np.unique(np.concatenate([prob, [0.5]]))
    # Counts of predictions >= each candidate threshold, via sorted search.
    pos_sorted = np.sort(prob[y_true == 1])
    neg_sorted = np.sort(prob[y_true == 0])
    tp = pos_sorted.size - np.searchsorted(pos_sorted, candidates, side="left")
    fp = neg_sorted.size - np.searchsorted(neg_sorted, candidates, side="left")
    fn = pos_sorted.size - tp
    tn = neg_sorted.size - fp
    with np.errstate(divide="ignore", invalid="ignore"):
        recall = np.where(tp + fn > 0, tp / np.maximum(tp + fn, 1), 0.0)
        specificity = np.where(tn + fp > 0, tn / np.maximum(tn + fp, 1), 0.0)
        precision = np.where(tp + fp > 0, tp / np.maximum(tp + fp, 1), 0.0)
        if criterion == "max_balanced_accuracy":
            score = (recall + specificity) / 2
        else:
            denom = precision + recall
            score = np.where(denom > 0, 2 * precision * recall / np.where(denom > 0, denom, 1), 0.0)
    best = score.max()
    tied = candidates[np.isclose(score, best, rtol=0, atol=1e-12)]
    # Ties resolve toward the threshold closest to 0.5 for stability.
    return float(tied[np.argmin(np.abs(tied - 0.5))])


def compute_metrics(y_true: np.ndarray, prob: np.ndarray, threshold: float, calibration_bins: int) -> dict:
    """Canonical metric set (05_Models/baseline_plan.md) at a frozen threshold."""

    y_true, prob = _check_inputs(y_true, prob)
    metrics = thresholded_metrics(y_true, prob, threshold)
    both_classes = len(np.unique(y_true)) == 2
    metrics["roc_auc"] = float(roc_auc_score(y_true, prob)) if both_classes else float("nan")
    metrics["pr_auc"] = float(average_precision_score(y_true, prob)) if both_classes else float("nan")
    metrics["ece"] = expected_calibration_error(y_true, prob, calibration_bins)
    metrics["brier"] = float(np.mean((prob - y_true) ** 2))
    metrics["n"] = int(y_true.size)
    metrics["n_positive"] = int(y_true.sum())
    return metrics
