"""STEP-058 tests: MOD010 data-only explainability and MOD011 evidence-grounded forensic reasoning."""

from __future__ import annotations

import json
from pathlib import Path

from confidence import estimate_confidence
from evidence.item import make_item
from evidence.registry import HEADER, register
from evidence.validation import validate_items
from explainability import DEFAULT_METHODS, assemble_explanation
from fusion import fuse_case
from reasoning import ReasoningSentence, compose_reasoning

CASE = "CASE000001"
DECISIONS = ("Real", "Fake", "Inconclusive", "Unknown")


def _registry(tmp_path: Path) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / "evidence_registry.csv"
    path.write_text(",".join(HEADER) + "\n", encoding="utf-8")
    return path


def _validate(path: Path, items) -> list[str]:
    reg = register(list(items), path)
    val = validate_items(path, [item.evidence_id for item in reg.items])
    return [item.evidence_id for item in val.items]


def _explain_item(method: str = "grad_cam", map_data=None, model_id: str | None = "MODEL0001"):
    has_map = map_data is not None
    return make_item(
        evidence_type="explainability_input",
        description=f"{method} map data recorded" if has_map else f"{method} produced no map",
        raw_output={
            "case_id": CASE,
            "input_id": f"{CASE}-input-01",
            "method": method,
            "map": map_data,
            "model_id": model_id if has_map else None,
        },
        value=map_data if has_map else "no_data",
        unit="",
        extra_processed={"model_id": model_id if has_map else None},
    )


def test_explainability_records_one_gradcam_payload_and_no_second_map(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    grid = {"grid": [[0.1, 0.8], [0.3, 0.9]], "layer": "0.7.2", "shape": [2, 2]}
    val_ids = _validate(path, [_explain_item("grad_cam", map_data=grid)])

    res = assemble_explanation(path, val_ids, case_id=CASE, storage_root=tmp_path)
    assert not res.failures and res.record is not None
    assert res.explanation_path is not None and res.explanation_path.is_file()

    payload = json.loads(res.explanation_path.read_text(encoding="utf-8"))
    by_method = {entry["method"]: entry for entry in payload["methods"]}
    assert tuple(by_method) == DEFAULT_METHODS
    assert by_method["grad_cam"]["status"] == "recorded"
    assert by_method["grad_cam"]["evidence_id"] == val_ids[0]
    assert by_method["grad_cam"]["data"] == grid
    for other in ("attention_maps", "saliency", "integrated_gradients"):
        assert by_method[other]["status"] == "no_data"
        assert by_method[other]["evidence_id"] is None
        assert by_method[other]["data"] is None

    text = res.explanation_path.read_text(encoding="utf-8")
    assert not any(word in text for word in DECISIONS)


def test_explainability_with_no_collector_data_writes_no_data_and_no_pixels(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    val_ids = _validate(path, [_explain_item("grad_cam", map_data=None)])

    res = assemble_explanation(path, val_ids, case_id=CASE, storage_root=tmp_path)
    assert not res.failures and res.record is not None
    payload = json.loads(res.explanation_path.read_text(encoding="utf-8"))
    for entry in payload["methods"]:
        assert entry["status"] == "no_data"
        assert entry["data"] is None
    assert payload["methods"][0]["evidence_id"] == val_ids[0]


def test_explainability_rejects_rendered_images_and_image_arguments(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    bad_ids = _validate(path, [_explain_item("grad_cam", map_data={"heatmap_png": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUg=="})])

    rendered = assemble_explanation(path, bad_ids, case_id=CASE, storage_root=tmp_path)
    assert rendered.record is None
    assert rendered.failures and "A.9" in rendered.failures[0].detail
    assert not (tmp_path / CASE / "explanation.json").exists()

    forbidden = assemble_explanation(path, [], case_id=CASE, storage_root=tmp_path, image_path="C:/img.png")
    assert forbidden.record is None
    assert forbidden.failures and "forbids image" in forbidden.failures[0].detail


def test_reasoning_composes_grounded_sentences_citing_present_ev_ids(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    face = make_item(
        evidence_type="face_detection",
        description="1 face detected",
        raw_output={"case_id": CASE, "input_id": f"{CASE}-input-01"},
        value=1,
        unit="count",
    )
    freq = make_item(
        evidence_type="frequency_domain",
        description="high-frequency ratio 0.4125",
        raw_output={"case_id": CASE, "input_id": f"{CASE}-input-01"},
        value=0.4125,
        unit="ratio",
    )
    det = make_item(
        evidence_type="deep_learning_prediction",
        description="MODEL0001 probability 0.9100",
        raw_output={"case_id": CASE, "input_id": f"{CASE}-input-01", "model_id": "MODEL0001", "positive_class": "fake"},
        value=0.91,
        unit="probability",
        extra_processed={"model_id": "MODEL0001", "threshold": 0.3951},
        source_module="MOD004",
    )
    val_ids = _validate(path, [face, freq, det])
    fused = fuse_case(path, val_ids, case_id=CASE)
    conf = estimate_confidence(path, [*val_ids, fused.validated.evidence_id], case_id=CASE)

    all_ids = [*val_ids, fused.validated.evidence_id, conf.validated.evidence_id]
    res = compose_reasoning(path, all_ids, case_id=CASE, storage_root=tmp_path)
    assert not res.failures and res.record is not None
    assert res.reasoning_path_file is not None and res.reasoning_path_file.is_file()
    assert res.record.reasoning_path == all_ids
    assert len(res.record.sentences) == 5
    for sentence, expected_id in zip(res.record.sentences, all_ids):
        assert sentence.evidence_ids == (expected_id,)
        assert expected_id in sentence.text


def test_sentence_whose_cited_id_is_removed_from_input_is_rejected(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    face = make_item(
        evidence_type="face_detection",
        description="1 face detected",
        raw_output={"case_id": CASE, "input_id": f"{CASE}-input-01"},
        value=1,
        unit="count",
    )
    freq = make_item(
        evidence_type="frequency_domain",
        description="high-frequency ratio 0.3500",
        raw_output={"case_id": CASE, "input_id": f"{CASE}-input-01"},
        value=0.35,
        unit="ratio",
    )
    val_ids = _validate(path, [face, freq])
    full = compose_reasoning(path, val_ids, case_id=CASE)
    assert len(full.record.sentences) == 2

    # Remove the second EV id from the input, but pass both candidate sentences
    trimmed = compose_reasoning(
        path,
        val_ids[:1],
        case_id=CASE,
        candidate_sentences=full.record.sentences,
        storage_root=tmp_path,
    )
    assert trimmed.record is not None
    assert len(trimmed.record.sentences) == 1
    assert trimmed.record.sentences[0].evidence_ids == (val_ids[0],)
    assert trimmed.record.rejected_count == 1
    assert trimmed.failures and "absent from input" in trimmed.failures[0].detail
    saved_text = (tmp_path / CASE / "reasoning.json").read_text(encoding="utf-8")
    assert val_ids[1] not in saved_text


def test_wording_that_names_an_absent_measurement_is_rejected(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    face = make_item(
        evidence_type="face_detection",
        description="1 face detected",
        raw_output={"case_id": CASE, "input_id": f"{CASE}-input-01"},
        value=1,
        unit="count",
    )
    val_ids = _validate(path, [face])

    # Sentence cites val_ids[0] (face_detection=1) but claims frequency_domain or invented number 0.8765
    bad_type = ReasoningSentence(
        text=f"Evidence {val_ids[0]} (frequency_domain) records value 1.",
        evidence_ids=(val_ids[0],),
        evidence_types=("face_detection",),
        fields_used={val_ids[0]: {"value": 1}},
    )
    bad_number = ReasoningSentence(
        text=f"Evidence {val_ids[0]} (face_detection) records value 0.8765.",
        evidence_ids=(val_ids[0],),
        evidence_types=("face_detection",),
        fields_used={val_ids[0]: {"value": 1}},
    )
    untied = ReasoningSentence(
        text="A face was detected and artifacts were found.",
        evidence_ids=(),
    )

    res = compose_reasoning(
        path,
        val_ids,
        case_id=CASE,
        candidate_sentences=[bad_type, bad_number, untied],
        storage_root=tmp_path,
    )
    assert res.record is not None
    assert res.record.sentences == []
    assert res.record.reasoning_path == []
    assert res.record.rejected_count == 3
    assert len(res.failures) == 3


def test_empty_evidence_list_produces_no_sentence_and_empty_reasoning_path(tmp_path: Path) -> None:
    path = _registry(tmp_path)
    res = compose_reasoning(path, [], case_id=CASE, storage_root=tmp_path)
    assert not res.failures and res.record is not None
    assert res.record.sentences == []
    assert res.record.reasoning_path == []
    assert res.record.narrative == ""
