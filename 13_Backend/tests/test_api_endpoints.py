"""STEP-062 API tests: all 10 canonical REST endpoints, validation, error envelopes, no stack traces, and MOD013 checks."""

from __future__ import annotations

import io
import json
from pathlib import Path
from unittest.mock import patch

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework.test import APIClient

from apps.core.config import BackendConfig, load_backend_config
from audit import HEADER as CASE_HEADER
from audit import read_case_rows
from evidence.collectors.deep_learning_specialist.fastai_export import Inference
from evidence.registry import HEADER as EV_HEADER
from pipeline import PROGRESS_STAGES


class _StubFaceCounter:
    def __init__(self, count: int = 1) -> None:
        self.count = count

    def count_faces(self, image: Image.Image) -> int:
        return self.count


class _StubPredictor:
    def __init__(self, prob: float = 0.93) -> None:
        self.prob = prob

    def predict(self, image: Image.Image) -> Inference:
        return Inference(fake_probability=self.prob, embedding=[0.1, 0.3], model_confidence=None)


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


@pytest.fixture()
def api_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[APIClient, BackendConfig]:
    ev_path = tmp_path / "evidence_registry.csv"
    ev_path.write_text(",".join(EV_HEADER) + "\n", encoding="utf-8")
    case_path = tmp_path / "case_registry.csv"
    case_path.write_text(",".join(CASE_HEADER) + "\n", encoding="utf-8")
    cfg = load_backend_config(
        {
            "DJANGO_ENV": "test",
            "DJANGO_SECRET_KEY": "test-api-secret",
            "FORENSIC_MEDIA_ROOT": str(tmp_path / "cases"),
            "FORENSIC_LOG_DIR": str(tmp_path / "logs"),
            "FORENSIC_EVIDENCE_REGISTRY": str(ev_path),
            "FORENSIC_CASE_REGISTRY": str(case_path),
            "FORENSIC_MODEL_ID": "MODEL0001",
            "FORENSIC_ASYNC_MODE": "eager",
        }
    )
    monkeypatch.setattr(settings, "FORENSIC_CONFIG", cfg)
    monkeypatch.setattr(settings, "FORENSIC_TEST_FACE_COUNTER", _StubFaceCounter(1), raising=False)
    monkeypatch.setattr(settings, "FORENSIC_TEST_PREDICTOR", _StubPredictor(0.93), raising=False)
    return APIClient(), cfg


def test_happy_path_all_case_endpoints_and_decision_json_unchanged(
    api_env: tuple[APIClient, BackendConfig],
) -> None:
    client, cfg = api_env

    # 1. POST /cases
    create_res = client.post("/cases", {"model_id": "MODEL0001"}, format="json")
    assert create_res.status_code == 201
    created = create_res.json()
    case_id = created["case_id"]
    assert case_id == "CASE000001"
    assert created["status"] == "created"
    assert created["stage"] == "Created"

    # 2. POST /cases/{id}/upload
    upload_file = SimpleUploadedFile("suspect.png", _sample_png(), content_type="image/png")
    upload_res = client.post(f"/cases/{case_id}/upload", {"file": upload_file}, format="multipart")
    assert upload_res.status_code in (200, 202)
    up_body = upload_res.json()
    assert up_body["case_id"] == case_id
    assert up_body["input_id"] == "CASE000001-input-01"
    assert "stored_path" not in up_body["intake"]

    # 3. GET /cases/{id}/status
    status_res = client.get(f"/cases/{case_id}/status")
    assert status_res.status_code == 200
    st_body = status_res.json()
    assert st_body["status"] == "completed"
    assert st_body["stage"] == "Complete"
    assert tuple(st_body["stage_history"]) == PROGRESS_STAGES
    assert st_body["progress_percent"] == 100

    # 4. GET /cases/{id}
    detail_res = client.get(f"/cases/{case_id}")
    assert detail_res.status_code == 200
    det_body = detail_res.json()
    assert det_body["case_id"] == case_id
    assert det_body["decision"] == "Fake"
    assert len(det_body["evidence_ids"]) == 24

    # Verify audit trail row in case_registry.csv
    case_rows = read_case_rows(cfg.case_registry_path)
    assert len(case_rows) == 1
    assert case_rows[0]["Case ID"] == case_id
    assert case_rows[0]["Decision"] == "Fake"

    # 5. GET /cases/{id}/evidence
    ev_res = client.get(f"/cases/{case_id}/evidence?validated_only=true")
    assert ev_res.status_code == 200
    ev_body = ev_res.json()
    assert ev_body["count"] == 12
    assert all(item["source_module"] == "MOD006" for item in ev_body["items"])

    # 6. GET /cases/{id}/decision — MOD013_spec.md requires returning decision.json unchanged
    dec_res = client.get(f"/cases/{case_id}/decision")
    assert dec_res.status_code == 200
    on_disk_decision = json.loads((cfg.media_root / case_id / "decision.json").read_text(encoding="utf-8"))
    assert dec_res.json() == on_disk_decision

    # 7. GET /cases/{id}/explanation
    expl_res = client.get(f"/cases/{case_id}/explanation")
    assert expl_res.status_code == 200
    on_disk_expl = json.loads((cfg.media_root / case_id / "explanation.json").read_text(encoding="utf-8"))
    assert expl_res.json() == on_disk_expl

    expl_with_reas = client.get(f"/cases/{case_id}/explanation?include_reasoning=true")
    assert expl_with_reas.status_code == 200
    assert "reasoning" in expl_with_reas.json()

    # 8. GET /cases/{id}/report (json, markdown, html) and /api/v1/ prefix parity
    rep_json = client.get(f"/cases/{case_id}/report?format=json")
    assert rep_json.status_code == 200
    assert rep_json.json()["case_id"] == case_id
    assert rep_json.json()["version_stamps"]["model_id"] == "MODEL0001"

    rep_md = client.get(f"/api/v1/cases/{case_id}/report?format=markdown")
    assert rep_md.status_code == 200
    assert "text/markdown" in rep_md["Content-Type"]
    assert f"# Case Report: {case_id}" in rep_md.content.decode("utf-8")

    rep_html = client.get(f"/cases/{case_id}/report?format=html")
    assert rep_html.status_code == 200
    assert "text/html" in rep_html["Content-Type"]
    assert "<!DOCTYPE html>" in rep_html.content.decode("utf-8")


def test_health_and_version_do_not_load_a_case(api_env: tuple[APIClient, BackendConfig]) -> None:
    client, cfg = api_env

    health_res = client.get("/health")
    assert health_res.status_code == 200
    h_body = health_res.json()
    assert h_body["status"] == "ok"
    assert all(h_body["checks"].values())

    ver_res = client.get("/api/v1/version")
    assert ver_res.status_code == 200
    v_body = ver_res.json()
    assert v_body["system_version"] == "0.1.0"
    assert v_body["api_version"] == "0.1.0"
    assert v_body["model_id"] == "MODEL0001"
    assert v_body["dataset_id"] == "DS0001/v1.0/PP0001"
    assert v_body["experiment_id"] == "EXP0001"
    assert v_body["git_commit"]
    assert list(cfg.media_root.glob("CASE*")) == []


def test_unsupported_and_corrupted_uploads_return_mod016_and_no_decision(
    api_env: tuple[APIClient, BackendConfig],
) -> None:
    client, cfg = api_env

    # Case 1: unsupported .bmp upload rejected at MOD001
    c1 = client.post("/cases", {}, format="json").json()["case_id"]
    bad_file = SimpleUploadedFile("bad.bmp", b"BM-invalid", content_type="image/bmp")
    up1 = client.post(f"/cases/{c1}/upload", {"file": bad_file}, format="multipart")
    assert up1.status_code == 400
    err1 = up1.json()["error"]
    assert err1["name"] == "unsupported_format"
    assert err1["module_id"] == "MOD001"
    assert not list((cfg.media_root / c1).rglob("original.*"))

    dec1 = client.get(f"/cases/{c1}/decision")
    assert dec1.status_code == 404
    assert dec1.json()["error"]["name"] == "unsupported_format"

    # Case 2: corrupted .png upload accepted by MOD001, stopped at MOD002
    c2 = client.post("/cases", {}, format="json").json()["case_id"]
    corrupt_png = SimpleUploadedFile("corrupt.png", b"not-a-valid-png-stream", content_type="image/png")
    up2 = client.post(f"/cases/{c2}/upload", {"file": corrupt_png}, format="multipart")
    assert up2.status_code == 202
    st2 = client.get(f"/cases/{c2}/status").json()
    assert st2["status"] == "failed"
    assert st2["failures"][0]["name"] == "corrupted_image"
    assert st2["failures"][0]["module_id"] == "MOD002"

    dec2 = client.get(f"/cases/{c2}/decision")
    assert dec2.status_code == 404
    assert dec2.json()["error"]["name"] == "corrupted_image"


def test_validation_not_found_and_internal_error_never_expose_stack_traces(
    api_env: tuple[APIClient, BackendConfig],
) -> None:
    client, _ = api_env

    # Invalid model_id on POST /cases
    bad_create = client.post("/cases", {"model_id": "invalid"}, format="json")
    assert bad_create.status_code == 400
    assert "error" in bad_create.json()

    # Invalid case_id format -> 400
    bad_id = client.get("/cases/NOTACASE")
    assert bad_id.status_code == 400
    assert bad_id.json()["error"]["name"] == "unexpected_error"

    # Non-existent case_id -> 404
    not_found = client.get("/cases/CASE999999")
    assert not_found.status_code == 404
    assert not_found.json()["error"]["case_id"] == "CASE999999"

    # Missing file on upload -> 400
    c1 = client.post("/cases", {}, format="json").json()["case_id"]
    no_file = client.post(f"/cases/{c1}/upload", {}, format="multipart")
    assert no_file.status_code == 400
    assert no_file.json()["error"]["module_id"] == "MOD001"

    # Invalid report format -> 400
    bad_fmt = client.get(f"/cases/{c1}/report?format=pdf")
    assert bad_fmt.status_code == 400
    assert "unsupported report format" in bad_fmt.json()["error"]["detail"]

    # Simulated unhandled internal exception -> 500 MOD016 envelope, zero stack trace leaked
    with patch("apps.api.views.get_case_detail", side_effect=RuntimeError("sensitive internal stack path /secret/db")):
        err_res = client.get(f"/cases/{c1}")
    assert err_res.status_code == 500
    raw_text = err_res.content.decode("utf-8")
    assert "Traceback" not in raw_text
    assert "sensitive internal stack path" not in raw_text
    assert err_res.json()["error"]["name"] == "unexpected_error"
