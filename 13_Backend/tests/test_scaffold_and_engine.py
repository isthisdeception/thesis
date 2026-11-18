"""STEP-061 tests: Django scaffold, single-responsibility apps, env config, 7 log channels, and forensic_engine wrapper."""

from __future__ import annotations

import io
from pathlib import Path

import pytest
from django.apps import apps
from django.core.management import call_command
from PIL import Image

from apps.core.config import BACKEND_ROOT, BackendConfig, load_backend_config
from apps.core.logging_config import LOG_CHANNELS, get_channel_logger
from apps.evidence import read_case_decision, read_case_evidence, read_case_explanation
from apps.forensic_engine import (
    allocate_case,
    get_case_detail,
    get_job_status,
    submit_investigation_upload,
    wait_for_case_job,
)
from apps.health import check_system_health
from apps.reports import read_case_report
from apps.versioning import get_version_info
from audit import HEADER as CASE_HEADER
from evidence.collectors.deep_learning_specialist.fastai_export import Inference
from evidence.registry import HEADER as EV_HEADER
from pipeline import PROGRESS_STAGES


class _StubFaceCounter:
    def __init__(self, count: int = 1) -> None:
        self.count = count

    def count_faces(self, image: Image.Image) -> int:
        return self.count


class _StubPredictor:
    def __init__(self, prob: float = 0.94) -> None:
        self.prob = prob

    def predict(self, image: Image.Image) -> Inference:
        return Inference(fake_probability=self.prob, embedding=[0.2, 0.4], model_confidence=None)


def _sample_png(width: int = 64, height: int = 64) -> bytes:
    img = Image.new("RGB", (width, height))
    img.putdata(
        [
            (((x * 7 + y * 3) % 256), ((x * 5 + y * 11) % 256), ((x * 13 + y * 17) % 256))
            for y in range(height)
            for x in range(width)
        ]
    )
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _test_config(tmp_path: Path, *, async_mode: str = "eager") -> BackendConfig:
    ev_path = tmp_path / "evidence_registry.csv"
    ev_path.write_text(",".join(EV_HEADER) + "\n", encoding="utf-8")
    case_path = tmp_path / "case_registry.csv"
    case_path.write_text(",".join(CASE_HEADER) + "\n", encoding="utf-8")
    return load_backend_config(
        {
            "DJANGO_ENV": "test",
            "DJANGO_SECRET_KEY": "test-secret-key",
            "FORENSIC_MEDIA_ROOT": str(tmp_path / "cases"),
            "FORENSIC_LOG_DIR": str(tmp_path / "logs"),
            "FORENSIC_EVIDENCE_REGISTRY": str(ev_path),
            "FORENSIC_CASE_REGISTRY": str(case_path),
            "FORENSIC_MODEL_ID": "MODEL0001",
            "FORENSIC_ASYNC_MODE": async_mode,
        }
    )


def test_django_check_and_single_responsibility_apps_registered() -> None:
    call_command("check")
    expected_apps = {
        "apps.core",
        "apps.forensic_engine",
        "apps.evidence",
        "apps.reports",
        "apps.health",
        "apps.versioning",
        "apps.api",
    }
    installed = {cfg.name for cfg in apps.get_app_configs()}
    assert expected_apps <= installed


def test_env_config_profiles_and_env_example_has_no_secrets(tmp_path: Path) -> None:
    env_example = (BACKEND_ROOT / ".env.example").read_text(encoding="utf-8")
    assert "DJANGO_SECRET_KEY=replace-with-env-secret-key-in-production" in env_example
    assert "FORENSIC_MEDIA_ROOT=" in env_example

    with pytest.raises(ValueError, match="DJANGO_SECRET_KEY"):
        load_backend_config({"DJANGO_ENV": "prod"})

    with pytest.raises(ValueError, match="DJANGO_SECRET_KEY"):
        load_backend_config(
            {
                "DJANGO_ENV": "prod",
                "DJANGO_SECRET_KEY": "replace-with-env-secret-key-in-production",
            }
        )

    prod_cfg = load_backend_config(
        {
            "DJANGO_ENV": "prod",
            "DJANGO_SECRET_KEY": "strong-ephemeral-test-value-not-committed",
            "FORENSIC_MEDIA_ROOT": str(tmp_path / "prod_cases"),
            "FORENSIC_LOG_DIR": str(tmp_path / "prod_logs"),
        }
    )
    assert prod_cfg.env == "prod" and prod_cfg.debug is False


def test_all_seven_log_channels_write_to_disk(tmp_path: Path) -> None:
    log_dir = tmp_path / "logs"
    for channel in LOG_CHANNELS:
        logger = get_channel_logger(channel, log_dir)
        logger.info("smoke test for %s channel", channel)
        for handler in logger.handlers:
            handler.flush()
        log_file = log_dir / f"{channel}.log"
        assert log_file.is_file()
        assert f"smoke test for {channel} channel" in log_file.read_text(encoding="utf-8")


def test_forensic_engine_invokes_pipeline_async_and_versions_uploads(tmp_path: Path) -> None:
    cfg = _test_config(tmp_path, async_mode="thread")
    allocated = allocate_case(cfg)
    case_id = allocated["case_id"]
    assert case_id == "CASE000001"
    assert allocated["stage"] == "Created"

    intake1, job1 = submit_investigation_upload(
        cfg,
        case_id=case_id,
        filename="sample.png",
        data=_sample_png(),
        face_counter=_StubFaceCounter(1),
        predictor=_StubPredictor(0.94),
    )
    assert intake1.accepted
    assert job1["input_id"] == "CASE000001-input-01"
    assert "stored_path" not in job1["intake"]

    res1 = wait_for_case_job(case_id, timeout=10.0)
    assert res1 is not None and res1.status == "completed"

    status_payload = get_job_status(cfg, case_id)
    assert status_payload is not None
    assert status_payload["status"] == "completed"
    assert status_payload["stage"] == "Complete"
    assert tuple(status_payload["stage_history"]) == PROGRESS_STAGES
    assert status_payload["progress_percent"] == 100

    detail = get_case_detail(cfg, case_id)
    assert detail is not None
    assert detail["decision"] == "Fake"
    assert len(detail["evidence_ids"]) == 24

    ev_data = read_case_evidence(cfg, case_id, validated_only=True)
    assert ev_data["count"] == 12
    assert all("stored_path" not in item["raw_output"] for item in ev_data["items"])

    dec_data = read_case_decision(cfg, case_id)
    assert dec_data is not None and dec_data["decision"] == "Fake"

    expl_data = read_case_explanation(cfg, case_id, include_reasoning=True)
    assert expl_data is not None and "reasoning" in expl_data

    rep_json, ct_json = read_case_report(cfg, case_id, report_format="json")
    assert ct_json == "application/json" and rep_json["case_id"] == case_id
    rep_md, ct_md = read_case_report(cfg, case_id, report_format="markdown")
    assert "text/markdown" in ct_md and f"# Case Report: {case_id}" in rep_md

    # Second upload to same case receives input-02 and never overwrites input-01
    intake2, job2 = submit_investigation_upload(
        cfg,
        case_id=case_id,
        filename="second.png",
        data=_sample_png(),
        face_counter=_StubFaceCounter(1),
        predictor=_StubPredictor(0.03),
    )
    assert intake2.accepted
    assert job2["input_id"] == "CASE000001-input-02"
    wait_for_case_job(case_id, timeout=10.0)
    assert (cfg.media_root / case_id / "CASE000001-input-01" / "original.png").is_file()
    assert (cfg.media_root / case_id / "CASE000001-input-02" / "original.png").is_file()


def test_rejected_upload_and_health_and_version_adapters(tmp_path: Path) -> None:
    cfg = _test_config(tmp_path, async_mode="eager")
    allocated = allocate_case(cfg)
    case_id = allocated["case_id"]

    intake, job = submit_investigation_upload(
        cfg,
        case_id=case_id,
        filename="unsupported.bmp",
        data=b"BM-fake",
        face_counter=_StubFaceCounter(1),
    )
    assert not intake.accepted
    assert job["job_status"] == "failed"
    assert intake.failure is not None and intake.failure.name == "unsupported_format"
    assert read_case_decision(cfg, case_id) is None

    health_payload, healthy = check_system_health(cfg)
    assert healthy and health_payload["status"] == "ok"

    version_payload = get_version_info(cfg)
    assert version_payload["model_id"] == "MODEL0001"
    assert version_payload["experiment_id"] == "EXP0001"
    assert version_payload["git_commit"]
