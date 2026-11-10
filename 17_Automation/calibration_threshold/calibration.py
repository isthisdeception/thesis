"""Phase E4 calibration data. Probability, confidence, and reliability are kept apart.

- probability: the model's P(fake) for an image (`y_prob`).
- confidence: the probability of the predicted class, max(p, 1 - p).
- reliability: how often predictions at a given probability or confidence are right.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from training.evaluation import calibration_table, expected_calibration_error

CONFIDENCE_BINS = 10


def _check(y_true: np.ndarray, prob: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    y_true = np.asarray(y_true).astype(int).ravel()
    prob = np.asarray(prob, dtype=float).ravel()
    if y_true.shape != prob.shape or y_true.size == 0:
        raise ValueError("y_true and prob must be non-empty and the same length")
    if not set(np.unique(y_true)) <= {0, 1}:
        raise ValueError("y_true must be 0 or 1")
    if np.any(np.isnan(prob)) or np.any((prob < 0) | (prob > 1)):
        raise ValueError("prob must be finite and inside [0, 1]")
    return y_true, prob


def reliability_rows(split: str, y_true: np.ndarray, prob: np.ndarray, bins: int) -> list[dict]:
    rows = []
    for row in calibration_table(y_true, prob, bins):
        gap = row["fraction_positive"] - row["mean_confidence"] if row["count"] else float("nan")
        rows.append({"split": split, **row, "gap": gap})
    return rows


def maximum_calibration_error(y_true: np.ndarray, prob: np.ndarray, bins: int) -> float:
    """Largest |fraction_positive - mean_probability| over non-empty bins."""

    gaps = [abs(r["fraction_positive"] - r["mean_confidence"]) for r in calibration_table(y_true, prob, bins) if r["count"]]
    return float(max(gaps))


def confidence_rows(split: str, y_true: np.ndarray, prob: np.ndarray, y_pred: np.ndarray, bins: int = CONFIDENCE_BINS) -> list[dict]:
    """Confidence of the predicted class, binned over [0.5, 1.0], with the accuracy observed in each bin."""

    y_true, prob = _check(y_true, prob)
    y_pred = np.asarray(y_pred).astype(int).ravel()
    confidence = np.where(y_pred == 1, prob, 1 - prob)
    correct = y_pred == y_true
    edges = np.linspace(0.5, 1.0, bins + 1)
    # Decisions below 0.5 confidence happen when the threshold is not 0.5; they go in a separate row.
    rows = []
    low = confidence < 0.5
    if low.any():
        rows.append(_confidence_row(split, -1, 0.0, 0.5, confidence[low], correct[low], confidence.size))
    idx = np.clip(np.digitize(confidence, edges[1:-1], right=True), 0, bins - 1)
    for b in range(bins):
        mask = (idx == b) & ~low
        rows.append(_confidence_row(split, b, edges[b], edges[b + 1], confidence[mask], correct[mask], confidence.size))
    return rows


def _confidence_row(split: str, b: int, lower: float, upper: float, conf: np.ndarray, correct: np.ndarray, total: int) -> dict:
    n = int(conf.size)
    return {
        "split": split,
        "bin": b,
        "lower": float(lower),
        "upper": float(upper),
        "count": n,
        "share": n / total,
        "mean_confidence": float(conf.mean()) if n else float("nan"),
        "accuracy": float(correct.mean()) if n else float("nan"),
    }


def calibration_summary(split: str, y_true: np.ndarray, prob: np.ndarray, y_pred: np.ndarray, bins: int) -> dict:
    y_true, prob = _check(y_true, prob)
    y_pred = np.asarray(y_pred).astype(int).ravel()
    prevalence = float(y_true.mean())
    confidence = np.where(y_pred == 1, prob, 1 - prob)
    clipped = np.clip(prob, 1e-7, 1 - 1e-7)
    return {
        "split": split,
        "n": int(y_true.size),
        "bins": bins,
        "ece": expected_calibration_error(y_true, prob, bins),
        "mce": maximum_calibration_error(y_true, prob, bins),
        "brier": float(np.mean((prob - y_true) ** 2)),
        "brier_reference": prevalence * (1 - prevalence),
        "log_loss": float(-np.mean(y_true * np.log(clipped) + (1 - y_true) * np.log(1 - clipped))),
        "mean_probability": float(prob.mean()),
        "fraction_positive": prevalence,
        "mean_confidence": float(confidence.mean()),
        "accuracy": float((y_pred == y_true).mean()),
    }


def calibration_frames(predictions: pd.DataFrame, bins: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    summary, reliability, confidence = [], [], []
    for split, frame in predictions.groupby("split", sort=True):
        y, p, d = frame["y_true"].to_numpy(), frame["y_prob"].to_numpy(), frame["y_pred"].to_numpy()
        summary.append(calibration_summary(str(split), y, p, d, bins))
        reliability += reliability_rows(str(split), y, p, bins)
        confidence += confidence_rows(str(split), y, p, d)
    return pd.DataFrame(summary), pd.DataFrame(reliability), pd.DataFrame(confidence)
