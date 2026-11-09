"""STEP-042 prediction validation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from prediction_validation import PredictionValidationError, validate, write_report
from prediction_validation.validate import check_predictions

REPO = Path(__file__).resolve().parents[2]


def test_exp0001_validation_passes() -> None:
    checks = write_report(REPO)
    assert checks and all(c.passed for c in checks)
    text = (REPO / "08_Evaluation/EVAL0001/prediction_validation_report.md").read_text(encoding="utf-8")
    assert "**Status:** PASS" in text
    assert "ROC-AUC" in text


def test_duplicate_prediction_fails(tmp_path: Path) -> None:
    source = REPO / "08_Evaluation" / "EXP0001"
    dest = tmp_path / "08_Evaluation" / "EXP0001"
    dest.mkdir(parents=True)
    (dest / "manifest.json").write_text((source / "manifest.json").read_text(encoding="utf-8"), encoding="utf-8")
    frame = pd.read_csv(source / "predictions.csv")
    frame = pd.concat([frame, frame.iloc[[0]]], ignore_index=True)
    frame.to_csv(dest / "predictions.csv", index=False)
    checks = check_predictions(tmp_path, "EXP0001")
    failed = [c.name for c in checks if not c.passed]
    assert "no duplicate ids" in failed


def test_probability_out_of_range_fails(tmp_path: Path) -> None:
    source = REPO / "08_Evaluation" / "EXP0001"
    dest = tmp_path / "08_Evaluation" / "EXP0001"
    dest.mkdir(parents=True)
    (dest / "manifest.json").write_text((source / "manifest.json").read_text(encoding="utf-8"), encoding="utf-8")
    frame = pd.read_csv(source / "predictions.csv")
    frame.loc[0, "y_prob"] = 1.2
    frame.to_csv(dest / "predictions.csv", index=False)
    checks = check_predictions(tmp_path, "EXP0001")
    assert any(c.name == "probabilities in [0, 1]" and not c.passed for c in checks)


def test_incomplete_experiment_is_rejected(tmp_path: Path) -> None:
    checks = validate(tmp_path)
    assert any(c.phase == "E1" and not c.passed for c in checks)
    with pytest.raises(PredictionValidationError):
        write_report(tmp_path)
