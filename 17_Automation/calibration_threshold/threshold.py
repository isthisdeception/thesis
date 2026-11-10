"""Phase E5 threshold sweep and operating points. Thresholds are chosen on `val` only, then applied to `test`."""

from __future__ import annotations

import numpy as np
import pandas as pd

from training.evaluation import select_threshold, thresholded_metrics

SWEEP = np.round(np.linspace(0.0, 1.0, 101), 2)
TARGET_RATE = 0.05

# name -> (criterion, use)
OPERATING_POINTS: dict[str, tuple[str, str]] = {
    "frozen": ("max balanced accuracy on val (rule set in config before training)", "Default. Equals the ROC (Youden J) optimum."),
    "max_f1": ("max F1 on val", "PR-curve optimum for the fake class."),
    "fixed_0.5": ("0.5", "Uncalibrated reference only."),
    "high_specificity": (f"lowest threshold with FPR <= {TARGET_RATE} on val", "Flag for review: few real images flagged."),
    "high_sensitivity": (f"highest threshold with FNR <= {TARGET_RATE} on val", "Screening: few fakes missed."),
}


def _counts(y_true: np.ndarray, prob: np.ndarray, candidates: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """FPR and FNR when predicting fake for prob >= each candidate."""

    pos = np.sort(prob[y_true == 1])
    neg = np.sort(prob[y_true == 0])
    tp = pos.size - np.searchsorted(pos, candidates, side="left")
    fp = neg.size - np.searchsorted(neg, candidates, side="left")
    return fp / max(neg.size, 1), (pos.size - tp) / max(pos.size, 1)


def rate_threshold(y_true: np.ndarray, prob: np.ndarray, rate: str, target: float) -> float:
    y_true = np.asarray(y_true).astype(int).ravel()
    prob = np.asarray(prob, dtype=float).ravel()
    candidates = np.unique(prob)
    fpr, fnr = _counts(y_true, prob, candidates)
    if rate == "fpr":
        ok = candidates[fpr <= target]
        return float(ok.min()) if ok.size else 1.0
    if rate == "fnr":
        ok = candidates[fnr <= target]
        return float(ok.max()) if ok.size else 0.0
    raise ValueError(f"unknown rate {rate!r}")


def select_operating_points(val: pd.DataFrame) -> dict[str, float]:
    thresholds = val["threshold"].unique()
    if len(thresholds) != 1:
        raise ValueError("val has more than one recorded threshold")
    y, p = val["y_true"].to_numpy(), val["y_prob"].to_numpy()
    return {
        "frozen": float(thresholds[0]),
        "max_f1": select_threshold(y, p, "max_f1"),
        "fixed_0.5": 0.5,
        "high_specificity": rate_threshold(y, p, "fpr", TARGET_RATE),
        "high_sensitivity": rate_threshold(y, p, "fnr", TARGET_RATE),
    }


def sweep_frame(predictions: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for split, frame in predictions.groupby("split", sort=True):
        y, p = frame["y_true"].to_numpy(), frame["y_prob"].to_numpy()
        rows += [{"split": str(split), **thresholded_metrics(y, p, float(t))} for t in SWEEP]
    return pd.DataFrame(rows)


def operating_frame(predictions: pd.DataFrame) -> pd.DataFrame:
    splits = {str(s): f for s, f in predictions.groupby("split", sort=True)}
    if "val" not in splits:
        raise ValueError("operating points need a val split")
    points = select_operating_points(splits["val"])
    rows = []
    for name, threshold in points.items():
        criterion, use = OPERATING_POINTS[name]
        for split, frame in splits.items():
            metrics = thresholded_metrics(frame["y_true"].to_numpy(), frame["y_prob"].to_numpy(), threshold)
            rows.append({"point": name, "criterion": criterion, "selected_on": "val", "split": split, **metrics, "use": use})
    return pd.DataFrame(rows)
