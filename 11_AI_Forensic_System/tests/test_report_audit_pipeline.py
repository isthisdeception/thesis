"""STEP-059 tests: MOD012 report generator, MOD015 audit trail, MOD016 failures, MOD017/018 registries, and E2E pipeline."""

from __future__ import annotations

import io
import json
from pathlib import Path

from PIL import Image

from audit import HEADER as CASE_HEADER
from audit import append_case_row, read_case_rows
from confidence import estimate_confidence
from decision import decide_case
from evidence.collectors.deep_learning_specialist.fastai_export import Inference
from evidence.item import make_item
from evidence.registry import HEADER as EV_HEADER
from evidence.registry import read_rows, register
from evidence.validation import validate_items
from explainability import assemble_explanation
from failure_handling import FAILURE_NAMES, classify_failures, read_case_failures, write_failure
from fusion import fuse_case
from pipeline import PROGRESS_STAGES, run_investigation
from reasoning import compose_reasoning
from reports import VersionStamps, generate_report
from system_registry import ModalityProposal, validate_modality_proposal, validate_module_registry


class _StubFaceCounter:
    def __init__(self, count: int = 1) -> None:
        self.count = count

    def count_faces(self, image: Image.Image) -> int:
        return self.count


class _StubPredictor:
    def __init__(self, prob: float = 0.93) -> None:
        self.prob = prob

    def predict(self, image: Image.Image) -> Inference:
        return Inference(fake_probability=self.prob, embedding=[0.1, 0.2], model_confidence=None)


def _png_bytes(width: int = 64, height: int = 64) -> bytes:
    img = Image.new("RGB", (width, height))
    pixels = []
    for y in range(height):
        for x in range(width):
            pixels.append(((x * 7 + y * 3) % 256, (x * 5 + y * 11) % 256, (x * 13 + y * 17) % 256))
    img.putdata(pixels)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _registries(tmp_path: Path) -> tuple[Path, Path]:
    tmp_path.mkdir(parents=True, exist_ok=True)
    ev_path = tmp_path / "evidence_registry.csv"
    ev_path.write_text(",".join(EV_HEADER) + "\n", encoding="utf-8")
    case_path = tmp_path / "case_registry.csv"
    case_path.write_text(",".join(CASE_HEADER) + "\n", encoding="utf-8")
    return ev_path, case_path


def test_mod016_all_accepted_failure_names_written_and_read_back(tmp_path: Path) -> None:
    case_id = "CASE000001"
    for idx, name in enumerate(FAILURE_NAMES, start=1):
        rec = write_failure(
            tmp_path,
            name=name,
            module_id=f"MOD{idx:03d}",
            case_id=case_id,
            detail=f"test {name}",
        )
        assert rec.name == name
        assert rec.module_id == f"MOD{idx:03d}"

    unknown = write_failure(
        tmp_path,
        name="invented_category",
        module_id="MOD003",
        case_id=case_id,
        detail="something odd",
    )
    assert unknown.name == "unexpected_error"
    assert "reported_name=invented_category" in unknown.detail

    stored = read_case_failures(tmp_path, case_id)
    assert len(stored) == len(FAILURE_NAMES) + 1
    errors, warnings = classify_failures(stored)
    assert len(warnings) == 1
    assert len(errors) == len(FAILURE_NAMES)


def test_mod012_report_reproducibility_version_stamps_and_guards(tmp_path: Path) -> None:
    ev_path, _ = _registries(tmp_path)
    case_id = "CASE000001"
    det = make_item(
        evidence_type="deep_learning_prediction",
        description="MODEL0001 probability 0.9100",
        raw_output={"case_id": case_id, "input_id": f"{case_id}-input-01", "model_id": "MODEL0001", "positive_class": "fake"},
        value=0.91,
        unit="probability",
        confidence=None,
        extra_processed={"model_id": "MODEL0001", "threshold": 0.3951},
        source_module="MOD004",
    )
    face = make_item(
        evidence_type="face_detection",
        description="1 face detected",
        raw_output={"case_id": case_id, "input_id": f"{case_id}-input-01"},
        value=1,
        unit="count",
        confidence=None,
    )
    reg = register([det, face], ev_path)
    val = validate_items(ev_path, [item.evidence_id for item in reg.items])
    val_ids = [item.evidence_id for item in val.items]
    fused = fuse_case(ev_path, val_ids, case_id=case_id, storage_root=tmp_path)
    conf = estimate_confidence(ev_path, [*val_ids, fused.validated.evidence_id], case_id=case_id, storage_root=tmp_path)
    dec = decide_case(
        ev_path,
        case_id=case_id,
        fused_evidence_id=fused.validated.evidence_id,
        confidence_evidence_id=conf.validated.evidence_id,
        storage_root=tmp_path,
    )
    expl = assemble_explanation(ev_path, val_ids, case_id=case_id, storage_root=tmp_path)
    reas = compose_reasoning(
        ev_path,
        [*val_ids, fused.validated.evidence_id, conf.validated.evidence_id],
        case_id=case_id,
        storage_root=tmp_path,
    )
    assert dec.record and expl.record and reas.record

    stamps = VersionStamps(
        system_version="0.1.0",
        model_id="MODEL0001",
        model_version="1.0",
        dataset_id="DS0001/v1.0/PP0001",
        experiment_id="EXP0001",
        git_commit="abc1234def5678",
    )
    rep = generate_report(
        ev_path,
        case_id=case_id,
        version_stamps=stamps,
        storage_root=tmp_path,
    )
    assert not rep.failures and rep.report is not None
    assert rep.json_path.is_file() and rep.markdown_path.is_file() and rep.html_path.is_file()

    # Byte-for-byte version match
    saved = json.loads(rep.json_path.read_text(encoding="utf-8"))
    assert saved["version_stamps"]["model_id"] == "MODEL0001"
    assert saved["version_stamps"]["dataset_id"] == "DS0001/v1.0/PP0001"
    assert saved["version_stamps"]["experiment_id"] == "EXP0001"
    assert saved["version_stamps"]["git_commit"] == "abc1234def5678"

    # Evidence summary lists only IDs that exist in the registry
    reg_ids = {row["Evidence ID"] for row in read_rows(ev_path)}
    report_ids = {entry["evidence_id"] for entry in saved["evidence_summary"]}
    assert report_ids <= reg_ids

    # Limitations include empty collector confidence values rather than omitting them
    assert any("empty (null)" in lim for lim in saved["limitations"])

    # Missing version stamp is refused
    blank_stamp = generate_report(
        ev_path,
        case_id=case_id,
        version_stamps={"system_version": "0.1.0", "model_id": "MODEL0001", "dataset_id": "", "experiment_id": "EXP0001", "git_commit": "abc"},
        storage_root=tmp_path,
        output_dir=tmp_path / "blank_out",
    )
    assert blank_stamp.report is None and "missing required version stamp" in blank_stamp.failures[0].detail

    # Unregistered EV id is refused
    bad_ev = generate_report(
        ev_path,
        case_id=case_id,
        evidence_ids=["EV999999"],
        version_stamps=stamps,
        storage_root=tmp_path,
        output_dir=tmp_path / "bad_ev_out",
    )
    assert bad_ev.report is None and "not in evidence_registry.csv" in bad_ev.failures[0].detail

    # Removing decision.json prevents the report
    dec.decision_path.unlink()
    no_dec = generate_report(
        ev_path,
        case_id=case_id,
        version_stamps=stamps,
        storage_root=tmp_path,
        output_dir=tmp_path / "no_dec_out",
    )
    assert no_dec.report is None and "decision.json is missing" in no_dec.failures[0].detail


def test_end_to_end_pipeline_and_audit_trail_invariants(tmp_path: Path) -> None:
    ev_path, case_path = _registries(tmp_path)
    storage = tmp_path / "cases"

    # 1. Corrupt image fails at MOD002, produces no decision.json, and still writes a case row with Decision="" and Errors set
    corrupt_run = run_investigation(
        filename="broken.png",
        data=b"not-a-valid-png",
        storage_root=storage,
        evidence_registry_path=ev_path,
        case_registry_path=case_path,
        face_counter=_StubFaceCounter(1),
        predictor=_StubPredictor(0.95),
    )
    assert corrupt_run.case_id == "CASE000001"
    assert corrupt_run.status == "failed"
    assert corrupt_run.decision is None
    assert not (storage / "CASE000001" / "decision.json").exists()
    assert corrupt_run.case_row is not None
    assert corrupt_run.case_row.decision == ""
    assert corrupt_run.case_row.errors

    # 2. Successful end-to-end Fake investigation appends CASE000002 without deleting or rewriting CASE000001
    before_cases = case_path.read_text(encoding="utf-8")
    fake_run = run_investigation(
        filename="sample.png",
        data=_png_bytes(),
        storage_root=storage,
        evidence_registry_path=ev_path,
        case_registry_path=case_path,
        face_counter=_StubFaceCounter(1),
        predictor=_StubPredictor(0.95),
    )
    assert fake_run.case_id == "CASE000002"
    assert fake_run.status == "completed"
    assert tuple(fake_run.stage_history) == PROGRESS_STAGES
    assert fake_run.decision is not None and fake_run.decision.record.decision == "Fake"
    assert fake_run.report is not None and fake_run.report.markdown_path.is_file()
    assert case_path.read_text(encoding="utf-8").startswith(before_cases)

    # Verify case row EV IDs match all evidence registry rows for CASE000002 and Decision matches decision.json
    case_rows = {r["Case ID"]: r for r in read_case_rows(case_path)}
    assert set(case_rows) == {"CASE000001", "CASE000002"}
    assert case_rows["CASE000001"]["Decision"] == ""
    assert case_rows["CASE000001"]["Errors"] != ""

    ev_rows_case2 = [
        r["Evidence ID"]
        for r in read_rows(ev_path)
        if json.loads(r["Raw Output"]).get("case_id") == "CASE000002"
    ]
    assert case_rows["CASE000002"]["Evidence"].split(";") == ev_rows_case2
    dec_json = json.loads((storage / "CASE000002" / "decision.json").read_text(encoding="utf-8"))
    assert case_rows["CASE000002"]["Decision"] == dec_json["decision"] == "Fake"

    # 3. Missing model export recovers to explicit Unknown decision and logs MOD004 error on the case row
    unknown_run = run_investigation(
        filename="sample2.png",
        data=_png_bytes(),
        storage_root=storage,
        evidence_registry_path=ev_path,
        case_registry_path=case_path,
        face_counter=_StubFaceCounter(1),
        model_id="MODEL9999",
    )
    assert unknown_run.case_id == "CASE000003"
    assert unknown_run.status == "completed"
    assert unknown_run.decision.record.decision == "Unknown"
    assert unknown_run.case_row.decision == "Unknown"
    assert unknown_run.case_row.errors


def test_mod017_and_mod018_system_registry_and_modality_checks() -> None:
    rows = validate_module_registry()
    assert len(rows) == 18

    ok_collector, _ = validate_modality_proposal(
        ModalityProposal(kind="collector", name="audio_spectrum", owner_module="MOD003", contract="EvidenceCollector")
    )
    assert ok_collector

    bad_decision, reason = validate_modality_proposal(
        ModalityProposal(
            kind="collector",
            name="raw_image_shortcut",
            owner_module="MOD008",
            contract="EvidenceCollector",
            decision_reads_image=True,
        )
    )
    assert not bad_decision and "MOD008" in reason

    bad_coupled, _ = validate_modality_proposal(
        ModalityProposal(
            kind="collector",
            name="coupled_collector",
            owner_module="MOD003",
            contract="EvidenceCollector",
            calls_other_collectors=True,
        )
    )
    assert not bad_coupled
