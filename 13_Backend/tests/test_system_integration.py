"""STEP-066 live HTTP integration tests across Django REST API (`thread` async mode) and 11_AI_Forensic_System."""

from __future__ import annotations

import io
import json
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path
from wsgiref.simple_server import make_server

import pytest
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from PIL import Image

from apps.core.config import BackendConfig, load_backend_config
from audit import HEADER as CASE_HEADER
from evidence.collectors.deep_learning_specialist.fastai_export import Inference
from evidence.registry import HEADER as EV_HEADER
from pipeline import PROGRESS_STAGES


class _StubFaceCounter:
    def count_faces(self, image: Image.Image) -> int:
        return 1


class _StubPredictor:
    def __init__(self, prob: float = 0.92) -> None:
        self.prob = prob

    def predict(self, image: Image.Image) -> Inference:
        return Inference(fake_probability=self.prob, embedding=[0.1, 0.2], model_confidence=None)


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


def _multipart_upload(field_name: str, filename: str, data: bytes, content_type: str = "image/png") -> tuple[bytes, str]:
    boundary = "----ForensicIntegrationBoundary7MA4YWxkTrZu0gW"
    lines = [
        f"--{boundary}\r\n".encode("utf-8"),
        f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'.encode("utf-8"),
        f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"),
        data,
        f"\r\n--{boundary}--\r\n".encode("utf-8"),
    ]
    return b"".join(lines), f"multipart/form-data; boundary={boundary}"


def _http_json(url: str, *, method: str = "GET", body: bytes | None = None, headers: dict[str, str] | None = None):
    req = urllib.request.Request(url, data=body, method=method, headers=headers or {})
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read().decode("utf-8")
        hdrs = {k.lower(): v for k, v in resp.headers.items()}
        return resp.status, hdrs, json.loads(raw)


def _http_text(url: str, *, headers: dict[str, str] | None = None):
    req = urllib.request.Request(url, method="GET", headers=headers or {})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, dict(resp.headers), resp.read().decode("utf-8")


@pytest.fixture()
def live_server_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[str, BackendConfig]:
    ev_path = tmp_path / "evidence_registry.csv"
    ev_path.write_text(",".join(EV_HEADER) + "\n", encoding="utf-8")
    case_path = tmp_path / "case_registry.csv"
    case_path.write_text(",".join(CASE_HEADER) + "\n", encoding="utf-8")
    cfg = load_backend_config(
        {
            "DJANGO_ENV": "test",
            "DJANGO_SECRET_KEY": "integration-test-secret",
            "FORENSIC_MEDIA_ROOT": str(tmp_path / "cases"),
            "FORENSIC_LOG_DIR": str(tmp_path / "logs"),
            "FORENSIC_EVIDENCE_REGISTRY": str(ev_path),
            "FORENSIC_CASE_REGISTRY": str(case_path),
            "FORENSIC_MODEL_ID": "MODEL0001",
            "FORENSIC_ASYNC_MODE": "thread",
        }
    )
    monkeypatch.setattr(settings, "FORENSIC_CONFIG", cfg)
    monkeypatch.setattr(settings, "FORENSIC_TEST_FACE_COUNTER", _StubFaceCounter(), raising=False)
    monkeypatch.setattr(settings, "FORENSIC_TEST_PREDICTOR", _StubPredictor(0.92), raising=False)

    app = get_wsgi_application()
    server = make_server("127.0.0.1", 0, app)
    port = server.server_port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{port}/api/v1", cfg
    finally:
        server.shutdown()
        server.server_close()


def test_live_http_async_investigation_cors_versioning_and_report(
    live_server_env: tuple[str, BackendConfig],
) -> None:
    base_url, cfg = live_server_env
    cors_headers = {"Origin": "http://localhost:5173"}

    # 1. Verify /health and /version provenance over live HTTP with CORS header
    h_status, h_headers, health = _http_json(f"{base_url}/health", headers=cors_headers)
    assert h_status == 200
    assert health["status"] == "ok"
    assert h_headers.get("access-control-allow-origin") == "http://localhost:5173"

    v_status, _, version = _http_json(f"{base_url}/version", headers=cors_headers)
    assert v_status == 200
    assert version["model_id"] == "MODEL0001"
    assert version["dataset_id"] == "DS0001/v1.0/PP0001"
    assert version["experiment_id"] == "EXP0001"
    assert version["git_commit"]

    # 2. CORS preflight OPTIONS check for frontend origin
    preflight_req = urllib.request.Request(
        f"{base_url}/cases",
        method="OPTIONS",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    with urllib.request.urlopen(preflight_req, timeout=5) as pre_resp:
        assert pre_resp.status == 200
        pre_hdrs = {k.lower(): v for k, v in pre_resp.headers.items()}
        assert pre_hdrs.get("access-control-allow-origin") == "http://localhost:5173"

    # 3. POST /cases -> CASE000001
    c_status, _, created = _http_json(
        f"{base_url}/cases",
        method="POST",
        body=b"{}",
        headers={**cors_headers, "Content-Type": "application/json"},
    )
    assert c_status == 201
    case_id = created["case_id"]
    assert case_id == "CASE000001"

    # 4. POST /cases/{id}/upload -> 202 Accepted (async thread mode)
    body, content_type = _multipart_upload("file", "face.png", _sample_png())
    u_status, _, uploaded = _http_json(
        f"{base_url}/cases/{case_id}/upload",
        method="POST",
        body=body,
        headers={**cors_headers, "Content-Type": content_type},
    )
    assert u_status == 202
    assert uploaded["input_id"] == "CASE000001-input-01"
    assert uploaded["job_status"] == "running"

    # 5. Poll GET /cases/{id}/status until Complete
    terminal = None
    for _ in range(80):
        _, _, st = _http_json(f"{base_url}/cases/{case_id}/status", headers=cors_headers)
        if st["status"] in ("completed", "failed"):
            terminal = st
            break
        time.sleep(0.05)
    assert terminal is not None
    assert terminal["status"] == "completed"
    assert terminal["stage"] == "Complete"
    assert tuple(terminal["stage_history"]) == PROGRESS_STAGES
    assert terminal["progress_percent"] == 100

    # 6. Retrieve evidence, decision, explanation, and reports (JSON/Markdown/HTML)
    _, _, ev = _http_json(f"{base_url}/cases/{case_id}/evidence?validated_only=true", headers=cors_headers)
    assert ev["count"] == 12

    _, _, dec = _http_json(f"{base_url}/cases/{case_id}/decision", headers=cors_headers)
    assert dec["decision"] == "Fake"
    assert len(dec["reasoning_path"]) >= 11

    _, _, expl = _http_json(f"{base_url}/cases/{case_id}/explanation?include_reasoning=true", headers=cors_headers)
    assert expl["figure_policy"] == "A.9_data_only_no_rendered_images"
    assert len(expl["reasoning"]["sentences"]) == 12

    _, _, rep_json = _http_json(f"{base_url}/cases/{case_id}/report?format=json", headers=cors_headers)
    assert rep_json["version_stamps"]["model_id"] == "MODEL0001"
    assert rep_json["version_stamps"]["git_commit"] == version["git_commit"]

    _, _, rep_md = _http_text(f"{base_url}/cases/{case_id}/report?format=markdown", headers=cors_headers)
    assert f"# Case Report: {case_id}" in rep_md

    # 7. Versioned media check: a second upload to the same case creates -input-02 without overwriting -input-01
    body2, ct2 = _multipart_upload("file", "face_second.png", _sample_png())
    u2_status, _, uploaded2 = _http_json(
        f"{base_url}/cases/{case_id}/upload",
        method="POST",
        body=body2,
        headers={**cors_headers, "Content-Type": ct2},
    )
    assert u2_status == 202
    assert uploaded2["input_id"] == "CASE000001-input-02"
    for _ in range(80):
        _, _, st2 = _http_json(f"{base_url}/cases/{case_id}/status", headers=cors_headers)
        if st2["status"] in ("completed", "failed") and st2["input_id"] == "CASE000001-input-02":
            break
        time.sleep(0.05)

    assert (cfg.media_root / case_id / "CASE000001-input-01" / "original.png").is_file()
    assert (cfg.media_root / case_id / "CASE000001-input-02" / "original.png").is_file()
