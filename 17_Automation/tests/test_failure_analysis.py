"""STEP-045 confusion and failure analysis."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from failure_analysis import (
    confusion_frame,
    error_cases_frame,
    error_summary_frame,
    group_frame,
    join_metadata,
    metadata_coverage,
    per_class_frame,
    render_report,
    wilson_interval,
)

REPO = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def frame() -> pd.DataFrame:
    predictions = pd.read_csv(REPO / "08_Evaluation/EXP0001/predictions.csv")
    index = pd.read_csv(REPO / "04_Preprocessing/reports/metadata/DS0001_PP0001/index.csv")
    return join_metadata(predictions, index)


def _toy() -> pd.DataFrame:
    return pd.DataFrame({
        "split": ["test"] * 6,
        "id": list("abcdef"),
        "y_true": [1, 1, 1, 0, 0, 0],
        "y_prob": [0.9, 0.2, 0.95, 0.1, 0.6, 0.05],
        "y_pred": [1, 0, 1, 0, 1, 0],
        "threshold": [0.5] * 6,
        "processed_path": list("abcdef"),
        "generator": ["g1", "g1", "g2", "none", "none", "none"],
    })


def _toy_index() -> pd.DataFrame:
    return pd.DataFrame({
        "content_hash": list("abcdef"),
        "identity": ["g1_1", "g1_2", "g2_1", "ffhq_1", "ffhq_2", "celebahq_1"],
        "original_size": ["200x200"] * 6,
        "relative_path": [f"{x}.jpg" for x in "abcdef"],
    })


def test_wilson_interval() -> None:
    low, high = wilson_interval(0, 100)
    assert low == 0 and 0 < high < 0.05
    low, high = wilson_interval(50, 100)
    assert low == pytest.approx(0.4038, abs=1e-3) and high == pytest.approx(0.5962, abs=1e-3)


def test_toy_confusion_and_groups() -> None:
    f = join_metadata(_toy(), _toy_index())
    c = confusion_frame(f).set_index(["true_label", "predicted_label"])["count"]
    assert (c[("fake", "fake")], c[("fake", "real")], c[("real", "fake")], c[("real", "real")]) == (2, 1, 1, 2)
    g = group_frame(f).set_index("group")
    assert g.loc["g1", "error_rate"] == 0.5 and g.loc["g2", "errors"] == 0
    assert g.loc["ffhq", "group_type"] == "real_source" and g.loc["ffhq", "errors"] == 1
    assert g["small_group"].all()


def test_missing_metadata_fails() -> None:
    with pytest.raises(ValueError, match="no metadata"):
        join_metadata(_toy(), _toy_index().iloc[:5])


def test_matches_step043(frame: pd.DataFrame) -> None:
    metrics = pd.read_csv(REPO / "08_Evaluation/EVAL0001/classification_metrics.csv").set_index("split")
    c = confusion_frame(frame).set_index(["split", "true_label", "predicted_label"])["count"]
    for split in ("val", "test"):
        assert c[(split, "fake", "fake")] == metrics.loc[split, "tp"]
        assert c[(split, "real", "fake")] == metrics.loc[split, "fp"]
        assert c[(split, "fake", "real")] == metrics.loc[split, "fn"]
        assert c[(split, "real", "real")] == metrics.loc[split, "tn"]
    pc = per_class_frame(frame).set_index(["split", "class"])
    assert pc.loc[("test", "fake"), "recall"] == pytest.approx(metrics.loc["test", "recall"])


def test_groups_cover_every_error(frame: pd.DataFrame) -> None:
    g = group_frame(frame)
    for (split, label), part in g.groupby(["split", "true_label"]):
        assert part["share_of_class_errors"].sum() == pytest.approx(1.0)
    assert g.groupby("split")["errors"].sum().to_dict() == frame.groupby("split")["error"].sum().to_dict()


def test_cases_are_errors_and_deterministic(frame: pd.DataFrame) -> None:
    a, b = error_cases_frame(frame), error_cases_frame(frame)
    pd.testing.assert_frame_equal(a, b)
    assert (a["y_true"] != a["y_pred"]).all()
    assert len(a) == 2 * 2 * 20


def test_report_states_hypotheses(frame: pd.DataFrame) -> None:
    report = render_report(
        confusion_frame(frame), per_class_frame(frame), group_frame(frame), error_summary_frame(frame),
        error_cases_frame(frame), metadata_coverage(frame, "test"), "EVAL0001", "EXP0001", "0" * 64, "2026-11-10",
    )
    assert "**hypotheses**" in report
    for category in ("Generator confusion", "Identity confusion", "Compression", "Poor quality", "Background, lighting, occlusion", "Artifacts", "Unexpected behaviour"):
        assert f"| {category}" in report
    for banned in (" caused by ", " because the model ", " proves "):
        assert banned not in report
