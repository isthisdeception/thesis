"""MOD005 assigns EV ids without rewriting rows. MOD006 scores items differently."""

from __future__ import annotations

from pathlib import Path

from evidence.item import EvidenceItem, make_item
from evidence.registry import HEADER, read_rows, register
from evidence.validation import validate_items

CANONICAL = Path(__file__).resolve().parents[1] / "evidence_registry.csv"


def _registry(tmp_path: Path) -> Path:
    path = tmp_path / "evidence_registry.csv"
    path.write_text(CANONICAL.read_text(encoding="utf-8"), encoding="utf-8")
    if not path.read_text(encoding="utf-8").endswith("\n"):
        path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    return path


def _item(evidence_type: str, value, **kwargs) -> EvidenceItem:
    return make_item(
        evidence_type=evidence_type,
        description=f"{evidence_type} observation",
        raw_output={"case_id": "CASE000001", "input_id": "CASE000001-input-01", **kwargs.get("raw", {})},
        value=value,
        unit="count",
        confidence=kwargs.get("confidence"),
    )


def test_ids_are_new_and_the_header_stays(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    first = register([_item("image_statistics", 1), _item("image_statistics", 1)], path)
    assert [item.evidence_id for item in first.items] == ["EV000001", "EV000002"]
    again = register([_item("metadata", 3)], path)
    assert again.items[0].evidence_id == "EV000003"
    rows = read_rows(path)
    assert [row["Evidence ID"] for row in rows] == ["EV000001", "EV000002", "EV000003"]
    assert [name.strip() for name in path.read_text(encoding="utf-8").splitlines()[0].split(",")] == HEADER
    assert rows[0]["Quality"] == "unevaluated" and rows[0]["Source Module"] == "MOD003"


def test_a_malformed_item_is_not_given_an_id(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    broken = EvidenceItem(
        evidence_type="",
        description="missing type",
        raw_output={"case_id": "CASE000001"},
        processed_output={"value": 1, "unit": ""},
        confidence=None,
        timestamp="2026-11-17T10:00:00+06:00",
        source_module="MOD003",
    )
    result = register([broken, _item("texture_analysis", 2)], path, storage_root=tmp_path, case_id="CASE000001")
    assert result.failures and result.failures[0].name == "unexpected_error"
    assert [item.evidence_id for item in result.items] == ["EV000001"]
    assert "missing type" not in path.read_text(encoding="utf-8")


def test_empty_confidence_is_not_filled_and_scores_are_not_uniform(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    quiet = _item("face_quality", 5.0, confidence=None)
    unsure = _item("face_quality", 5.0, confidence=0.1)
    registered = register([quiet, unsure], path)
    scored = validate_items(path, [item.evidence_id for item in registered.items], storage_root=tmp_path, case_id="CASE000001")
    by_reason = {item.processed_output["validation_reason"]: item for item in scored.items}
    assert by_reason["no_reliability_concern"].confidence is None
    assert by_reason["no_reliability_concern"].quality == "high"
    assert by_reason["low_confidence"].quality == "low"
    assert by_reason["low_confidence"].confidence == 0.1
    originals = read_rows(path)[:2]
    assert [row["Quality"] for row in originals] == ["unevaluated", "unevaluated"]
    assert [row["Confidence"] for row in originals] == ["", "0.1"]


def test_conflicting_items_both_remain_and_cite_each_other(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    none = _item("face_detection", 0)
    many = _item("face_detection", 2)
    registered = register([none, many], path)
    before = path.read_text(encoding="utf-8")
    scored = validate_items(path, [item.evidence_id for item in registered.items])
    assert path.read_text(encoding="utf-8").startswith(before)
    by_value = {item.processed_output["value"]: item for item in scored.items}
    assert by_value[0].quality == "unusable" and by_value[0].status == "failed"
    assert by_value[2].quality == "low" and "conflicting_evidence" in by_value[2].processed_output["validation_reason"]
    assert registered.items[1].evidence_id in by_value[0].dependencies
    assert registered.items[0].evidence_id in by_value[2].dependencies
    rows = read_rows(path)
    assert len(rows) == 4
    assert rows[0]["Evidence ID"] == registered.items[0].evidence_id
    assert "face_detection_failure" in by_value[0].processed_output["validation_reason"]


def test_incomplete_metadata_and_model_uncertainty(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    incomplete = make_item(
        evidence_type="metadata",
        description="metadata observation",
        raw_output={"case_id": "CASE000001", "byte_size": 10},
        value={"byte_size": 10},
        unit="byte",
    )
    uncertain = make_item(
        evidence_type="deep_learning_prediction",
        description="MODEL0001 probability 0.5000",
        raw_output={"case_id": "CASE000001", "model_id": "MODEL0001"},
        value=0.5,
        unit="probability",
        source_module="MOD004",
    )
    registered = register([incomplete, uncertain], path)
    scored = validate_items(path, [item.evidence_id for item in registered.items])
    qualities = {item.evidence_type: item.quality for item in scored.items}
    assert qualities == {"metadata": "unusable", "deep_learning_prediction": "low"}
    assert scored.items[1].source_module == "MOD006"
    assert scored.items[1].raw_output["collector_source_module"] == "MOD004"
