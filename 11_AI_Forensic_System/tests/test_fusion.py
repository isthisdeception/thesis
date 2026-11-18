"""MOD007: swappable strategy, explicit conflicts, missing and single-source evidence, no decision."""

from __future__ import annotations

from pathlib import Path

import pytest

from evidence.item import make_item
from evidence.registry import read_rows, register
from evidence.validation import validate_items
from fusion import (
    FusionOutput,
    RuleBasedStrategy,
    RuleTable,
    Unresolved,
    build_strategy,
    fuse_case,
    load_config,
    register_strategy,
    registered_ids,
)
from fusion.strategies.rule_based import DirectionalRule

CASE = "CASE000001"
DECISIONS = ("Real", "Fake", "Inconclusive", "Unknown")


def _registry(tmp_path: Path) -> Path:
    path = tmp_path / "evidence_registry.csv"
    path.write_text(
        "Evidence ID,Evidence Type,Source Module,Timestamp,Confidence,Description,Raw Output,Processed Output,"
        "Quality,Dependencies,Owner,Version,Status,Created,Updated\n",
        encoding="utf-8",
    )
    return path


def _detector(value, *, model="MODEL0001", threshold=0.395, confidence=None, evidence_type="deep_learning_prediction", raw=None):
    return make_item(
        evidence_type=evidence_type,
        description=f"{model} probability {value:.4f}",
        raw_output={"case_id": CASE, "input_id": f"{CASE}-input-01", "model_id": model, "positive_class": "fake", **(raw or {})},
        value=value,
        unit="probability",
        confidence=confidence,
        extra_processed={"model_id": model, "threshold": threshold},
        source_module="MOD004",
    )


def _context(evidence_type: str, value, **raw):
    return make_item(
        evidence_type=evidence_type,
        description=f"{evidence_type} observation",
        raw_output={"case_id": CASE, "input_id": f"{CASE}-input-01", **raw},
        value=value,
        unit="",
    )


def _validated(path: Path, items) -> list[str]:
    registered = register(list(items), path)
    scored = validate_items(path, [item.evidence_id for item in registered.items])
    return [item.evidence_id for item in scored.items]


def _no_decision_words(text: str) -> None:
    import re

    assert not re.search(r"\b(" + "|".join(DECISIONS) + r")\b", text)


def test_single_source_leans_and_cites_ev_ids(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    ids = _validated(path, [_detector(0.9)])
    result = fuse_case(path, ids, case_id=CASE, strategy_id="rule_based")
    assert not result.failures
    fused = result.fused
    assert fused.evidence_id.startswith("EV") and fused.source_module == "MOD007"
    assert fused.evidence_type == "fused_conclusion" and fused.confidence is None
    processed = fused.processed_output
    assert processed["strategy_id"] == "rule_based"
    assert processed["supporting_ids"] == ids
    summary = processed["summary"]
    assert summary["lean"] == "positive_class" and summary["single_source"] is True
    assert any(ids[0] in line for line in summary["rationale"])
    assert fused.dependencies == ids
    assert result.validated.quality == "medium"
    assert "single_source" in result.validated.processed_output["validation_reason"]
    _no_decision_words(path.read_text(encoding="utf-8"))


def test_conflicting_detectors_are_contested_and_both_cited(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    ids = _validated(path, [_detector(0.9, model="MODEL0001"), _detector(0.1, model="MODEL0008")])
    result = fuse_case(path, ids, case_id=CASE, strategy_id="rule_based")
    summary = result.fused.processed_output["summary"]
    assert summary["lean"] == "contested"
    assert summary["conflicts"]["directional"] == {"positive_ids": [ids[0]], "negative_ids": [ids[1]]}
    assert {entry["evidence_id"] for entry in summary["conflicts"]["flagged_by_validation"]} == set(ids)
    assert set(result.fused.processed_output["supporting_ids"]) == set(ids)
    assert result.validated.quality == "low"
    assert "fused_conflict" in result.validated.processed_output["validation_reason"]


def test_reliability_weights_change_the_lean(tmp_path: Path) -> None:
    table = RuleTable(directional_rules={"deep_learning_prediction": DirectionalRule(), "second_detector": DirectionalRule()})
    path = _registry(tmp_path)
    ids = _validated(path, [_detector(0.9), _detector(0.1, confidence=0.1, evidence_type="second_detector")])
    qualities = {row["Evidence ID"]: row["Quality"] for row in read_rows(path)}
    assert qualities[ids[0]] == "high" and qualities[ids[1]] == "low"
    leaning = fuse_case(path, ids, case_id=CASE, strategy=RuleBasedStrategy(table))
    summary = leaning.fused.processed_output["summary"]
    assert summary["weights"] == {"positive": 1.0, "negative": 0.3}
    assert summary["lean"] == "positive_class"
    strict = RuleTable(directional_rules=table.directional_rules, contested_balance_below=0.6)
    contested = fuse_case(path, ids, case_id=CASE, strategy=RuleBasedStrategy(strict))
    assert contested.fused.processed_output["summary"]["lean"] == "contested"


def test_missing_directional_evidence_and_unusable_items_stay_visible(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    ids = _validated(path, [_context("image_statistics", 1, luminance_variance=10.0), _context("face_detection", 0)])
    result = fuse_case(path, ids, case_id=CASE, strategy_id="rule_based")
    processed = result.fused.processed_output
    assert processed["summary"]["lean"] == "no_directional_evidence"
    assert processed["supporting_ids"] == [ids[0]]
    assert processed["unresolved"] == [{"evidence_id": ids[1], "reason": "unusable:face_detection_failure"}]
    assert ids[1] in result.fused.dependencies
    assert result.validated.quality == "low"


def test_empty_evidence_list_still_writes_an_explicit_record(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    result = fuse_case(path, [], case_id=CASE, strategy_id="rule_based")
    assert result.fused.processed_output["supporting_ids"] == []
    assert result.fused.processed_output["summary"]["lean"] == "no_directional_evidence"


def test_a_new_evidence_type_is_accepted_as_context(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    ids = _validated(path, [_detector(0.2), _context("audio_spectrum", 3.5)])
    result = fuse_case(path, ids, case_id=CASE, strategy_id="rule_based")
    summary = result.fused.processed_output["summary"]
    assert ids[1] in result.fused.processed_output["supporting_ids"]
    assert summary["context"] == [{"evidence_id": ids[1], "evidence_type": "audio_spectrum", "quality": "high"}]
    assert summary["lean"] == "negative_class"


def test_unregistered_strategy_does_not_fall_back(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    ids = _validated(path, [_detector(0.9)])
    before = path.read_text(encoding="utf-8")
    result = fuse_case(path, ids, case_id=CASE, strategy_id="bayesian", storage_root=tmp_path)
    assert result.fused is None
    assert result.failures[0].name == "unexpected_error" and result.failures[0].module_id == "MOD007"
    assert "reserved" in result.failures[0].detail
    assert path.read_text(encoding="utf-8") == before
    assert list((tmp_path / CASE / "failures").glob("*.json"))


class _CountStrategy:
    strategy_id = "test_count"
    version = "test"

    def fuse(self, evidence):
        return FusionOutput(self.strategy_id, [item.evidence_id for item in evidence], {"lean": "not_estimated", "count": len(evidence)})


def test_strategies_are_swappable_without_engine_changes(tmp_path: Path) -> None:
    if "test_count" not in registered_ids():
        register_strategy("test_count", lambda settings: _CountStrategy())
    with pytest.raises(ValueError):
        register_strategy("rule_based", lambda settings: _CountStrategy())
    path = _registry(tmp_path)
    ids = _validated(path, [_detector(0.9), _context("texture_analysis", 2.0)])
    first = fuse_case(path, ids, case_id=CASE, strategy_id="rule_based")
    second = fuse_case(path, ids, case_id=CASE, strategy_id="test_count")
    assert first.fused.processed_output["strategy_id"] == "rule_based"
    assert second.fused.processed_output["strategy_id"] == "test_count"
    assert first.fused.evidence_id != second.fused.evidence_id
    assert second.fused.processed_output["summary"]["count"] == 2


class _Broken:
    strategy_id = "broken"
    version = "test"

    def __init__(self, mode: str) -> None:
        self.mode = mode

    def fuse(self, evidence):
        if self.mode == "raise":
            raise RuntimeError("bad rule")
        if self.mode == "decide":
            return FusionOutput(self.strategy_id, [item.evidence_id for item in evidence], {"verdict": "Fake"})
        return FusionOutput(self.strategy_id, [], {"lean": "x"})  # drops every id


@pytest.mark.parametrize("mode, detail", [("raise", "raised RuntimeError"), ("decide", "states a case decision"), ("drop", "neither supporting nor unresolved")])
def test_a_bad_strategy_writes_no_fused_item(tmp_path: Path, mode: str, detail: str) -> None:
    path = _registry(tmp_path)
    ids = _validated(path, [_detector(0.9)])
    before = path.read_text(encoding="utf-8")
    result = fuse_case(path, ids, case_id=CASE, strategy=_Broken(mode))
    assert result.fused is None and detail in result.failures[0].detail
    assert path.read_text(encoding="utf-8") == before


def test_unvalidated_missing_and_superseded_ids_are_unresolved(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    registered = register([_detector(0.9), _detector(0.7, model="MODEL0001", threshold=None, evidence_type="deep_learning_prediction")], path)
    collector_ids = [item.evidence_id for item in registered.items]
    first = validate_items(path, collector_ids[:1]).items[0].evidence_id
    again = validate_items(path, collector_ids[:1]).items[0].evidence_id
    no_threshold = validate_items(path, collector_ids[1:]).items[0].evidence_id
    result = fuse_case(path, [collector_ids[0], "EV999999", first, again, no_threshold], case_id=CASE, strategy_id="rule_based")
    reasons = {entry["evidence_id"]: entry["reason"] for entry in result.fused.processed_output["unresolved"]}
    assert reasons[collector_ids[0]] == "not_validated_by_MOD006"
    assert reasons["EV999999"] == "not_in_registry"
    assert reasons[first] == f"superseded_by:{again}"
    assert reasons[no_threshold] == "no_threshold_recorded"
    assert result.fused.processed_output["supporting_ids"] == [again]
    assert "EV999999" not in result.fused.dependencies


def test_strategy_never_sees_file_locations(tmp_path: Path) -> None:
    seen = []

    class _Spy(_CountStrategy):
        strategy_id = "spy"

        def fuse(self, evidence):
            seen.extend(evidence)
            return super().fuse(evidence)

    path = _registry(tmp_path)
    ids = _validated(path, [_detector(0.9, raw={"stored_path": "C:/case/image.png", "export_pointer": "kaggle://x"})])
    fuse_case(path, ids, case_id=CASE, strategy=_Spy())
    assert "stored_path" not in seen[0].raw_output and "export_pointer" not in seen[0].raw_output
    assert seen[0].raw_output["model_id"] == "MODEL0001"


def test_configuration_selects_rule_based_and_rejects_bad_tables() -> None:
    strategy_id, settings = load_config()
    assert strategy_id == "rule_based"
    strategy = build_strategy(strategy_id, settings)
    assert isinstance(strategy, RuleBasedStrategy)
    assert strategy.table.reliability_weights == {"high": 1.0, "medium": 0.6, "low": 0.3}
    with pytest.raises(ValueError):
        RuleTable.from_json({**settings, "reliability_weights": {"high": 1.0, "unusable": 0.1}})
    assert Unresolved("EV000001", "r").to_json() == {"evidence_id": "EV000001", "reason": "r"}
