"""STEP-057 tests: MOD009 confidence estimation (E4 calibrated) and MOD008 decision engine."""

from __future__ import annotations

import json
from pathlib import Path

from confidence import FOUR_CONFIDENCE_FIELDS, estimate_confidence
from decision import ALLOWED_DECISIONS, decide_case
from evidence.item import make_item
from evidence.registry import HEADER, read_rows, register
from evidence.validation import validate_items
from failure_handling import write_failure
from fusion import fuse_case

CASE = "CASE000001"


def _registry(tmp_path: Path) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / "evidence_registry.csv"
    path.write_text(",".join(HEADER) + "\n", encoding="utf-8")
    return path


def _detector(
    prob: float,
    *,
    model: str = "MODEL0001",
    threshold: float | None = 0.3950566053390503,
    confidence: float | None = None,
    raw: dict | None = None,
):
    return make_item(
        evidence_type="deep_learning_prediction",
        description=f"{model} probability {prob:.4f}",
        raw_output={
            "case_id": CASE,
            "input_id": f"{CASE}-input-01",
            "model_id": model,
            "positive_class": "fake",
            **(raw or {}),
        },
        value=prob,
        unit="probability",
        confidence=confidence,
        extra_processed={"model_id": model, "threshold": threshold},
        source_module="MOD004",
    )


def _context(evidence_type: str, value, *, confidence: float | None = None, **raw):
    return make_item(
        evidence_type=evidence_type,
        description=f"{evidence_type} observation",
        raw_output={"case_id": CASE, "input_id": f"{CASE}-input-01", **raw},
        value=value,
        unit="",
        confidence=confidence,
    )


def _register_and_validate(path: Path, items) -> list[str]:
    reg = register(list(items), path)
    val = validate_items(path, [item.evidence_id for item in reg.items])
    return [item.evidence_id for item in val.items]


def test_four_confidences_are_calibrated_documented_and_distinct_from_raw_softmax(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    val_ids = _register_and_validate(
        path,
        [
            _detector(0.99, confidence=None),
            _context("face_detection", 1, confidence=None),
            _context("image_statistics", 1, luminance_variance=25.0, confidence=None),
        ],
    )
    fused = fuse_case(path, val_ids, case_id=CASE, storage_root=tmp_path)
    conf = estimate_confidence(
        path,
        [*val_ids, fused.validated.evidence_id],
        case_id=CASE,
        storage_root=tmp_path,
    )
    assert not conf.failures
    assert conf.confidence_item is not None and conf.validated is not None
    proc = conf.confidence_item.processed_output

    for field_name in FOUR_CONFIDENCE_FIELDS:
        val = proc[field_name]
        assert isinstance(val, float) and 0.0 <= val <= 1.0
        assert field_name in proc["interpretations"] and proc["interpretations"][field_name]

    # Raw P(fake) is 0.99; E4 val bin [0.95, 1.0] empirical accuracy is ~0.971745 (not 0.99)
    assert proc["prediction_confidence"] != 0.99
    assert abs(proc["prediction_confidence"] - 0.971745) < 1e-5
    assert proc["evidence_confidence"] == 1.0
    assert proc["system_confidence"] == 1.0
    assert proc["decision_confidence"] < proc["prediction_confidence"]
    assert set(val_ids) <= set(proc["supporting_ids"])

    # Empty collector confidence stays empty on the source rows in evidence_registry.csv
    rows = read_rows(path)
    collector_rows = [r for r in rows if r["Source Module"] in ("MOD003", "MOD004")]
    assert all(r["Confidence"] == "" for r in collector_rows)


def test_detector_099_with_all_other_evidence_unusable_lowers_decision_confidence(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    val_ids = _register_and_validate(
        path,
        [
            _detector(0.99),
            _context("face_detection", 0),  # unusable: face_detection_failure
            _context("metadata", {"byte_size": 10}, byte_size=10),  # unusable: incomplete_metadata
            _context("image_statistics", 0, luminance_variance=0.0),  # unusable: poor_image_quality
        ],
    )
    fused = fuse_case(path, val_ids, case_id=CASE, storage_root=tmp_path)
    conf = estimate_confidence(
        path,
        [*val_ids, fused.validated.evidence_id],
        case_id=CASE,
        storage_root=tmp_path,
    )
    proc = conf.confidence_item.processed_output
    assert abs(proc["prediction_confidence"] - 0.971745) < 1e-5
    assert proc["evidence_confidence"] == 0.25
    assert proc["system_confidence"] == 0.25
    assert proc["decision_confidence"] != proc["prediction_confidence"]
    assert proc["decision_confidence"] <= 0.25

    # Decision engine turns low decision_confidence into Inconclusive and logs a low_confidence warning
    dec = decide_case(
        path,
        case_id=CASE,
        fused_evidence_id=fused.validated.evidence_id,
        confidence_evidence_id=conf.validated.evidence_id,
        storage_root=tmp_path,
    )
    assert not dec.failures
    assert dec.record is not None
    assert dec.record.decision == "Inconclusive"
    assert dec.warnings and dec.warnings[0].name == "low_confidence"
    assert dec.record.decision_metadata["warning_failure_ids"] == [dec.warnings[0].failure_id]


def test_decision_fake_and_real_from_two_evidence_records_only(tmp_path: Path) -> None:
    # Fake path
    path_fake = _registry(tmp_path / "fake")
    ids_fake = _register_and_validate(
        path_fake,
        [_detector(0.92), _context("face_detection", 1), _context("image_statistics", 1, luminance_variance=15.0)],
    )
    fused_fake = fuse_case(path_fake, ids_fake, case_id=CASE)
    conf_fake = estimate_confidence(path_fake, [*ids_fake, fused_fake.validated.evidence_id], case_id=CASE)
    dec_fake = decide_case(
        path_fake,
        case_id=CASE,
        fused_evidence_id=fused_fake.validated.evidence_id,
        confidence_evidence_id=conf_fake.validated.evidence_id,
        storage_root=tmp_path / "fake",
    )
    assert not dec_fake.failures and dec_fake.record is not None
    assert dec_fake.record.decision == "Fake"
    assert dec_fake.decision_path is not None and dec_fake.decision_path.is_file()
    payload = json.loads(dec_fake.decision_path.read_text(encoding="utf-8"))
    assert payload["case_id"] == CASE
    assert payload["decision"] == "Fake"
    assert payload["fused_evidence_id"] == fused_fake.validated.evidence_id
    assert payload["confidence_evidence_id"] == conf_fake.validated.evidence_id
    assert set(ids_fake) <= set(payload["reasoning_path"])
    assert payload["decision_metadata"]["strategy_id"] == "rule_based"
    assert payload["decision_metadata"]["timestamp"]

    # Real path: low P(fake) = 0.02 -> predicted class is Real (raw class confidence 0.98, E4 val accuracy ~0.971745)
    path_real = _registry(tmp_path / "real")
    ids_real = _register_and_validate(
        path_real,
        [_detector(0.02), _context("face_detection", 1), _context("image_statistics", 1, luminance_variance=15.0)],
    )
    fused_real = fuse_case(path_real, ids_real, case_id=CASE)
    conf_real = estimate_confidence(path_real, [*ids_real, fused_real.validated.evidence_id], case_id=CASE)
    assert conf_real.confidence_item.processed_output["prediction_confidence"] != 0.02
    assert abs(conf_real.confidence_item.processed_output["prediction_confidence"] - 0.971745) < 1e-5
    dec_real = decide_case(
        path_real,
        case_id=CASE,
        fused_evidence_id=fused_real.validated.evidence_id,
        confidence_evidence_id=conf_real.validated.evidence_id,
        storage_root=tmp_path / "real",
    )
    assert not dec_real.failures and dec_real.record is not None
    assert dec_real.record.decision == "Real"


def test_conflicting_evidence_yields_inconclusive(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    val_ids = _register_and_validate(
        path,
        [
            _detector(0.91, model="MODEL0001"),
            _detector(0.08, model="MODEL0008"),
            _context("face_detection", 1),
        ],
    )
    fused = fuse_case(path, val_ids, case_id=CASE, storage_root=tmp_path)
    conf = estimate_confidence(path, [*val_ids, fused.validated.evidence_id], case_id=CASE, storage_root=tmp_path)
    dec = decide_case(
        path,
        case_id=CASE,
        fused_evidence_id=fused.validated.evidence_id,
        confidence_evidence_id=conf.validated.evidence_id,
        storage_root=tmp_path,
    )
    assert not dec.failures and dec.record is not None
    assert dec.record.decision == "Inconclusive"
    assert dec.record.decision_metadata["rule_id"] == "contested_directional_evidence_inconclusive"


def test_missing_model_yields_unknown_and_leaves_prediction_confidence_empty(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    # Simulate MOD004 model_unavailable failure recorded in the case directory
    write_failure(
        tmp_path,
        name="model_unavailable",
        module_id="MOD004",
        case_id=CASE,
        detail="MODEL0001 export missing",
    )
    val_ids = _register_and_validate(
        path,
        [_context("face_detection", 1), _context("image_statistics", 1, luminance_variance=12.0)],
    )
    fused = fuse_case(path, val_ids, case_id=CASE, storage_root=tmp_path)
    conf = estimate_confidence(path, [*val_ids, fused.validated.evidence_id], case_id=CASE, storage_root=tmp_path)
    proc = conf.confidence_item.processed_output
    assert proc["prediction_confidence"] is None
    assert proc["decision_confidence"] is None
    assert proc["evidence_confidence"] == 1.0
    # 2 usable collector items out of (2 collector items + 1 prior MOD016 failure) = 2/3
    assert abs(proc["system_confidence"] - round(2 / 3, 6)) < 1e-6

    dec = decide_case(
        path,
        case_id=CASE,
        fused_evidence_id=fused.validated.evidence_id,
        confidence_evidence_id=conf.validated.evidence_id,
        storage_root=tmp_path,
    )
    assert not dec.failures and dec.record is not None
    assert dec.record.decision == "Unknown"
    assert dec.record.decision in ALLOWED_DECISIONS
    saved = json.loads((tmp_path / CASE / "decision.json").read_text(encoding="utf-8"))
    assert saved["decision"] == "Unknown"


def test_image_path_or_missing_evidence_ids_refuses_to_run(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    # Supplying an image path and no evidence ids
    by_image = decide_case(
        path,
        case_id=CASE,
        storage_root=tmp_path,
        image_path=str(tmp_path / "input.png"),
    )
    assert by_image.record is None
    assert by_image.failures and by_image.failures[0].module_id == "MOD008"
    assert not (tmp_path / CASE / "decision.json").exists()

    # Supplying a file path where an EV id is required
    bad_ids = decide_case(
        path,
        case_id=CASE,
        fused_evidence_id="C:/case/image.png",
        confidence_evidence_id="",
        storage_root=tmp_path,
    )
    assert bad_ids.record is None
    assert bad_ids.failures and "EV ids" in bad_ids.failures[0].detail
    assert not (tmp_path / CASE / "decision.json").exists()


def test_unvalidated_unusable_or_missing_records_write_failure_and_no_decision(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    val_ids = _register_and_validate(path, [_detector(0.85), _context("face_detection", 1)])
    fused = fuse_case(path, val_ids, case_id=CASE)
    conf = estimate_confidence(path, [*val_ids, fused.validated.evidence_id], case_id=CASE)

    # Pass collector (MOD007) id instead of MOD006-validated id
    unvalidated = decide_case(
        path,
        case_id=CASE,
        fused_evidence_id=fused.fused.evidence_id,
        confidence_evidence_id=conf.validated.evidence_id,
        storage_root=tmp_path,
    )
    assert unvalidated.record is None
    assert "not validated by MOD006" in unvalidated.failures[0].detail

    # Absent id
    missing = decide_case(
        path,
        case_id=CASE,
        fused_evidence_id="EV999999",
        confidence_evidence_id=conf.validated.evidence_id,
        storage_root=tmp_path,
    )
    assert missing.record is None
    assert "not in registry" in missing.failures[0].detail
    assert not (tmp_path / CASE / "decision.json").exists()
