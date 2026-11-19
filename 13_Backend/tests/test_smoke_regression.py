"""STEP-067 Smoke & Regression test suite for the Django backend + AI Forensic Analyst (§8.9)."""

from __future__ import annotations

import io
import json
from pathlib import Path

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from PIL import Image
from rest_framework.test import APIClient

from apps.core.config import BackendConfig, load_backend_config
from audit import HEADER as CASE_HEADER
from audit import read_case_rows
from evidence.collectors.deep_learning_specialist.fastai_export import Inference
from evidence.registry import HEADER as EV_HEADER


class _ConfigurableFaceCounter:
    def __init__(self, count: int = 1) -> None:
        self.count = count

    def count_faces(self, image: Image.Image) -> int:
        return self.count


class _ConfigurablePredictor:
    def __init__(self, prob: float = 0.92) -> None:
        self.prob = prob

    def predict(self, image: Image.Image) -> Inference:
        return Inference(fake_probability=self.prob, embedding=[0.1, 0.2], model_confidence=None)


def _sample_png(seed: int = 1, width: int = 64, height: int = 64) -> bytes:
    img = Image.new("RGB", (width, height))
    img.putdata(
        [
            (((x * 7 + y * 3 + seed * 11) % 256), ((x * 5 + y * 13) % 256), ((x * 17 + y * 19) % 256))
            for y in range(height)
            for x in range(width)
        ]
    )
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture()
def regression_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[APIClient, BackendConfig]:
    ev_path = tmp_path / "evidence_registry.csv"
    ev_path.write_text(",".join(EV_HEADER) + "\n", encoding="utf-8")
    case_path = tmp_path / "case_registry.csv"
    case_path.write_text(",".join(CASE_HEADER) + "\n", encoding="utf-8")
    cfg = load_backend_config(
        {
            "DJANGO_ENV": "test",
            "DJANGO_SECRET_KEY": "smoke-regression-secret",
            "FORENSIC_MEDIA_ROOT": str(tmp_path / "cases"),
            "FORENSIC_LOG_DIR": str(tmp_path / "logs"),
            "FORENSIC_EVIDENCE_REGISTRY": str(ev_path),
            "FORENSIC_CASE_REGISTRY": str(case_path),
            "FORENSIC_MODEL_ID": "MODEL0001",
            "FORENSIC_ASYNC_MODE": "eager",
        }
    )
    monkeypatch.setattr(settings, "FORENSIC_CONFIG", cfg)
    monkeypatch.setattr(settings, "FORENSIC_TEST_FACE_COUNTER", _ConfigurableFaceCounter(1), raising=False)
    monkeypatch.setattr(settings, "FORENSIC_TEST_PREDICTOR", _ConfigurablePredictor(0.92), raising=False)
    return APIClient(), cfg


def test_smoke_django_check_health_and_version(regression_env: tuple[APIClient, BackendConfig]) -> None:
    client, _ = regression_env
    call_command("check")

    health = client.get("/api/v1/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    version = client.get("/api/v1/version")
    assert version.status_code == 200
    v_data = version.json()
    assert v_data["model_id"] == "MODEL0001"
    assert v_data["git_commit"]


@pytest.mark.parametrize(
    "scenario, filename, payload_fn, face_count, model_id, prob, expected_status, expected_dec, expected_err_name",
    [
        ("real_face_fake_pred", "fake.png", lambda: _sample_png(1), 1, "MODEL0001", 0.94, "completed", "Fake", None),
        ("real_face_real_pred", "real.png", lambda: _sample_png(2), 1, "MODEL0001", 0.02, "completed", "Real", None),
        ("missing_model_unknown", "nomodel.png", lambda: _sample_png(3), 1, "MODEL9999", 0.50, "completed", "Unknown", "model_unavailable"),
        ("no_face_stop", "noface.png", lambda: _sample_png(4), 0, "MODEL0001", 0.50, "failed", "", "no_face"),
        ("multiple_faces_stop", "multi.png", lambda: _sample_png(5), 3, "MODEL0001", 0.50, "failed", "", "multiple_faces"),
        ("corrupted_png_stop", "corrupt.png", lambda: b"not-a-valid-png", 1, "MODEL0001", 0.50, "failed", "", "corrupted_image"),
    ],
)
def test_regression_matrix_covers_decisions_and_failure_gates(
    regression_env: tuple[APIClient, BackendConfig],
    monkeypatch: pytest.MonkeyPatch,
    scenario: str,
    filename: str,
    payload_fn,
    face_count: int,
    model_id: str,
    prob: float,
    expected_status: str,
    expected_dec: str,
    expected_err_name: str | None,
) -> None:
    client, cfg = regression_env
    monkeypatch.setattr(settings, "FORENSIC_TEST_FACE_COUNTER", _ConfigurableFaceCounter(face_count), raising=False)
    monkeypatch.setattr(
        settings,
        "FORENSIC_TEST_PREDICTOR",
        None if model_id == "MODEL9999" else _ConfigurablePredictor(prob),
        raising=False,
    )

    c_res = client.post("/api/v1/cases", {"model_id": model_id}, format="json")
    assert c_res.status_code == 201, scenario
    case_id = c_res.json()["case_id"]

    upload = SimpleUploadedFile(filename, payload_fn(), content_type="image/png")
    up_res = client.post(f"/api/v1/cases/{case_id}/upload", {"file": upload}, format="multipart")
    assert up_res.status_code in (200, 202), scenario

    st = client.get(f"/api/v1/cases/{case_id}/status").json()
    assert st["status"] == expected_status, scenario

    rows = [r for r in read_case_rows(cfg.case_registry_path) if r["Case ID"] == case_id]
    assert len(rows) == 1
    assert rows[0]["Decision"] == expected_dec

    if expected_status == "completed":
        dec_res = client.get(f"/api/v1/cases/{case_id}/decision")
        assert dec_res.status_code == 200
        assert dec_res.json()["decision"] == expected_dec
        # Regression: explanation.json never leaks rendered image bytes/paths (A.9)
        expl_text = client.get(f"/api/v1/cases/{case_id}/explanation").content.decode("utf-8")
        assert "data:image/" not in expl_text
        # Regression: report embeds exact git_commit provenance
        rep = client.get(f"/api/v1/cases/{case_id}/report?format=json").json()
        assert rep["version_stamps"]["git_commit"]
    else:
        assert not (cfg.media_root / case_id / "decision.json").exists()
        assert st["failures"][0]["name"] == expected_err_name
        dec_err = client.get(f"/api/v1/cases/{case_id}/decision")
        assert dec_err.status_code == 404
        assert dec_err.json()["error"]["name"] == expected_err_name


def test_regression_empty_and_unsupported_uploads_preserve_audit_history(
    regression_env: tuple[APIClient, BackendConfig],
) -> None:
    client, cfg = regression_env

    # Empty upload
    c1 = client.post("/api/v1/cases", {}, format="json").json()["case_id"]
    empty_file = SimpleUploadedFile("empty.png", b"", content_type="image/png")
    r1 = client.post(f"/api/v1/cases/{c1}/upload", {"file": empty_file}, format="multipart")
    assert r1.status_code == 400
    assert r1.json()["error"]["module_id"] == "MOD001"
    assert not list((cfg.media_root / c1).rglob("original.*"))

    # Unsupported extension
    c2 = client.post("/api/v1/cases", {}, format="json").json()["case_id"]
    bmp_file = SimpleUploadedFile("bad.bmp", b"BM-invalid", content_type="image/bmp")
    r2 = client.post(f"/api/v1/cases/{c2}/upload", {"file": bmp_file}, format="multipart")
    assert r2.status_code == 400
    assert r2.json()["error"]["name"] == "unsupported_format"

    # Both failed cases remain appended in case_registry.csv
    rows = read_case_rows(cfg.case_registry_path)
    assert [r["Case ID"] for r in rows] == [c1, c2]
    assert all(r["Status"] == "failed" and r["Decision"] == "" for r in rows)
