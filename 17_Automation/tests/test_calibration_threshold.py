"""STEP-044 calibration and threshold analysis."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from calibration_threshold import (
    SWEEP,
    calibration_frames,
    calibration_summary,
    confidence_rows,
    maximum_calibration_error,
    operating_frame,
    rate_threshold,
    render_report,
    sweep_frame,
)
from training.evaluation import select_threshold

REPO = Path(__file__).resolve().parents[2]
PREDICTIONS = REPO / "08_Evaluation/EXP0001/predictions.csv"


@pytest.fixture(scope="module")
def predictions() -> pd.DataFrame:
    return pd.read_csv(PREDICTIONS)


def test_perfect_calibration_has_zero_error() -> None:
    y = np.array([0, 0, 1, 1])
    p = np.array([0.0, 0.0, 1.0, 1.0])
    row = calibration_summary("test", y, p, y, 10)
    assert row["ece"] == 0 and row["mce"] == 0 and row["brier"] == 0


def test_mce_is_largest_bin_gap() -> None:
    y = np.array([0, 1, 1, 1])
    p = np.array([0.05, 0.05, 0.95, 0.95])
    assert maximum_calibration_error(y, p, 10) == pytest.approx(0.45)


def test_confidence_is_probability_of_predicted_class() -> None:
    y = np.array([1, 0, 1])
    p = np.array([0.9, 0.2, 0.45])
    pred = np.array([1, 0, 1])
    rows = confidence_rows("test", y, p, pred, bins=5)
    low = [r for r in rows if r["bin"] == -1][0]
    assert low["count"] == 1 and low["mean_confidence"] == pytest.approx(0.45)
    assert sum(r["count"] for r in rows) == 3


def test_rate_thresholds_meet_target() -> None:
    rng = np.random.default_rng(0)
    y = rng.integers(0, 2, 2000)
    p = np.clip(rng.normal(0.35 + 0.3 * y, 0.15), 0, 1)
    t_fpr = rate_threshold(y, p, "fpr", 0.05)
    t_fnr = rate_threshold(y, p, "fnr", 0.05)
    assert np.mean(p[y == 0] >= t_fpr) <= 0.05
    assert np.mean(p[y == 1] < t_fnr) <= 0.05
    with pytest.raises(ValueError):
        rate_threshold(y, p, "tpr", 0.05)


def test_matches_training_record(predictions: pd.DataFrame) -> None:
    summary, reliability, _ = calibration_frames(predictions, 15)
    stored = json.loads((REPO / "06_Experiments/EXP0001/metrics/test_metrics.json").read_text(encoding="utf-8"))
    test = summary[summary["split"] == "test"].iloc[0]
    assert test["ece"] == pytest.approx(stored["ece"])
    assert test["brier"] == pytest.approx(stored["brier"])
    stored_bins = pd.read_csv(REPO / "08_Evaluation/EXP0001/calibration.csv")
    for split in ("val", "test"):
        ours = reliability[reliability["split"] == split]
        theirs = stored_bins[stored_bins["split"] == split]
        assert ours["count"].tolist() == theirs["count"].tolist()
        assert np.allclose(ours["fraction_positive"], theirs["fraction_positive"], equal_nan=True)


def test_frozen_threshold_is_val_optimum(predictions: pd.DataFrame) -> None:
    val = predictions[predictions["split"] == "val"]
    refit = select_threshold(val["y_true"].to_numpy(), val["y_prob"].to_numpy(), "max_balanced_accuracy")
    assert refit == pytest.approx(val["threshold"].iloc[0], abs=1e-5)


def test_operating_points_are_chosen_on_val(predictions: pd.DataFrame) -> None:
    points = operating_frame(predictions)
    assert set(points["selected_on"]) == {"val"}
    for _, group in points.groupby("point"):
        assert group["threshold"].nunique() == 1
    test = points[points["split"] == "test"].set_index("point")
    assert test.loc["high_sensitivity", "fnr"] < test.loc["frozen", "fnr"]
    assert test.loc["high_specificity", "fpr"] < test.loc["frozen", "fpr"]
    stored = json.loads((REPO / "06_Experiments/EXP0001/metrics/test_metrics.json").read_text(encoding="utf-8"))
    assert int(test.loc["frozen", "tp"]) == stored["tp"]


def test_outputs_are_deterministic(predictions: pd.DataFrame) -> None:
    a, b = sweep_frame(predictions), sweep_frame(predictions)
    pd.testing.assert_frame_equal(a, b)
    assert len(a) == 2 * len(SWEEP)


def test_report_covers_e4_and_e5(predictions: pd.DataFrame) -> None:
    summary, reliability, confidence = calibration_frames(predictions, 15)
    report = render_report(summary, reliability, confidence, operating_frame(predictions), "EVAL0001", "EXP0001", "0" * 64, "2026-11-10")
    for text in ("| ece |", "| mce |", "| brier |", "**Probability**", "**Confidence**", "**Reliability**", "| frozen |", "**Screening:**", "Flag for review"):
        assert text in report
