"""STEP-043 classification metrics."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from classification_metrics import (
    COLUMNS,
    METRIC_COLUMNS,
    METRIC_NOTES,
    classification_row,
    note_key,
    render_report,
    require_validated,
    write_metrics,
)

REPO = Path(__file__).resolve().parents[2]


def test_known_confusion() -> None:
    y_true = np.array([1, 1, 1, 0, 0, 0, 0, 1])
    y_prob = np.array([0.9, 0.8, 0.3, 0.2, 0.6, 0.1, 0.4, 0.7])
    y_pred = (y_prob >= 0.5).astype(int)
    row = classification_row("test", y_true, y_prob, y_pred, 0.5, "fake")
    assert (row["tp"], row["fn"], row["fp"], row["tn"]) == (3, 1, 1, 3)
    assert row["precision"] == pytest.approx(0.75)
    assert row["recall"] == pytest.approx(0.75)
    assert row["sensitivity"] == row["recall"]
    assert row["specificity"] == pytest.approx(0.75)
    assert row["fpr"] == pytest.approx(0.25)
    assert row["fnr"] == pytest.approx(0.25)
    assert row["balanced_accuracy"] == pytest.approx(0.75)
    assert row["mcc"] == pytest.approx(0.5)
    assert row["accuracy"] == pytest.approx(0.75)
    assert set(COLUMNS) <= set(row)


def test_suite_is_never_accuracy_alone() -> None:
    assert "accuracy" in COLUMNS
    others = [name for name in COLUMNS if name not in {"split", "positive_class", "threshold", "n", "n_positive", "n_negative", "tp", "tn", "fp", "fn", "accuracy"}]
    assert {"mcc", "pr_auc", "balanced_accuracy", "roc_auc", "f1_macro"} <= set(others)


def test_invalid_probability_fails() -> None:
    with pytest.raises(ValueError, match="\\[0, 1\\]"):
        classification_row("test", np.array([0, 1]), np.array([0.2, 1.4]), np.array([0, 1]), 0.5, "fake")


def test_eval0001_matches_training_record(tmp_path: Path) -> None:
    out = tmp_path / "classification_metrics.csv"
    frame = write_metrics(REPO / "08_Evaluation/EXP0001/predictions.csv", out, "fake")
    stored = json.loads((REPO / "06_Experiments/EXP0001/metrics/test_metrics.json").read_text(encoding="utf-8"))
    test = frame[frame["split"] == "test"].iloc[0]
    assert list(pd.read_csv(out).columns) == COLUMNS
    for key in ("roc_auc", "pr_auc", "f1", "balanced_accuracy", "mcc", "precision", "recall", "specificity", "fpr", "fnr", "accuracy"):
        assert test[key] == pytest.approx(stored[key])
    assert int(test["tp"]) == stored["tp"]
    assert test["sensitivity"] == test["recall"]


def test_metrics_are_deterministic(tmp_path: Path) -> None:
    source = REPO / "08_Evaluation/EXP0001/predictions.csv"
    write_metrics(source, tmp_path / "a.csv", "fake")
    write_metrics(source, tmp_path / "b.csv", "fake")
    assert (tmp_path / "a.csv").read_bytes() == (tmp_path / "b.csv").read_bytes()


def test_every_metric_is_documented() -> None:
    assert {note_key(name) for name in METRIC_COLUMNS} == set(METRIC_NOTES)
    assert all(len(note) == 4 and all(note) for note in METRIC_NOTES.values())


def test_unvalidated_predictions_are_refused(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        require_validated(tmp_path / "missing.md")
    failed = tmp_path / "report.md"
    failed.write_text("**Status:** FAIL\n", encoding="utf-8")
    with pytest.raises(ValueError, match="did not pass"):
        require_validated(failed)
    require_validated(REPO / "08_Evaluation/EVAL0001/prediction_validation_report.md")


def test_report_lists_full_suite(tmp_path: Path) -> None:
    frame = write_metrics(REPO / "08_Evaluation/EXP0001/predictions.csv", tmp_path / "m.csv", "fake")
    report = render_report(frame, "EVAL0001", "EXP0001", "0" * 64, "2026-11-10")
    for name in METRIC_COLUMNS:
        assert f"| {name} |" in report
    assert "| test | val |" in report
