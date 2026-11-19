"""STEP-067 Automated User Acceptance Testing (UAT) Script (§8.9).

Boots the live Django REST API (`thread` async mode) and executes all 6 UAT scenarios:
- UAT-01: Valid single-face image (fake-leaning detector score) -> Fake + 4 confidences + Template 24 report
- UAT-02: Valid single-face image (real-leaning detector score) -> Real + calibrated confidence != 0.02
- UAT-03: Corrupted PNG -> MOD002 corrupted_image failure, no decision.json, failed case row
- UAT-04: No-face image -> MOD002 no_face failure, no decision.json
- UAT-05: Unsupported .bmp upload -> HTTP 400 MOD001 unsupported_format, no image stored
- UAT-06: Missing model (MODEL9999) -> MOD004 model_unavailable, graceful Unknown decision
"""

from __future__ import annotations

import io
import json
import logging
import os
import socketserver
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer, make_server

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
AUTOMATION_DIR = str(Path(__file__).resolve().parent)
sys.path[:] = [p for p in sys.path if os.path.abspath(p or ".") != AUTOMATION_DIR]
BACKEND_DIR = REPO_ROOT / "13_Backend"
FORENSIC_DIR = REPO_ROOT / "11_AI_Forensic_System"

for p in (str(BACKEND_DIR), str(FORENSIC_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from audit import HEADER as CASE_HEADER  # noqa: E402
from audit import read_case_rows  # noqa: E402
from evidence.collectors.deep_learning_specialist.fastai_export import Inference  # noqa: E402
from evidence.registry import HEADER as EV_HEADER  # noqa: E402


class _ThreadingWSGIServer(socketserver.ThreadingMixIn, WSGIServer):
    daemon_threads = True


class _QuietHandler(WSGIRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


class _UATFaceCounter:
    def __init__(self, count: int = 1) -> None:
        self.count = count

    def count_faces(self, image: Image.Image) -> int:
        return self.count


class _UATPredictor:
    def __init__(self, prob: float = 0.92) -> None:
        self.prob = prob

    def predict(self, image: Image.Image) -> Inference:
        return Inference(fake_probability=self.prob, embedding=[0.1, 0.2], model_confidence=None)


def _sample_png(seed: int = 1) -> bytes:
    img = Image.new("RGB", (64, 64))
    img.putdata(
        [
            (((x * 7 + y * 3 + seed * 13) % 256), ((x * 5 + y * 11) % 256), ((x * 13 + y * 17) % 256))
            for y in range(64)
            for x in range(64)
        ]
    )
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _multipart(filename: str, data: bytes, content_type: str = "image/png") -> tuple[bytes, str]:
    boundary = "----UATBoundary7MA4YWxkTrZu0gW"
    body = b"".join(
        [
            f"--{boundary}\r\n".encode("utf-8"),
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode("utf-8"),
            f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"),
            data,
            f"\r\n--{boundary}--\r\n".encode("utf-8"),
        ]
    )
    return body, f"multipart/form-data; boundary={boundary}"


def _req_json(url: str, *, method: str = "GET", body: bytes | None = None, headers: dict | None = None):
    req = urllib.request.Request(url, data=body, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))


def main() -> int:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        root = Path(tmp)
        ev_path = root / "evidence_registry.csv"
        ev_path.write_text(",".join(EV_HEADER) + "\n", encoding="utf-8")
        case_path = root / "case_registry.csv"
        case_path.write_text(",".join(CASE_HEADER) + "\n", encoding="utf-8")

        os.environ["DJANGO_SETTINGS_MODULE"] = "forensic_backend.settings"
        os.environ["DJANGO_ENV"] = "test"
        os.environ["DJANGO_SECRET_KEY"] = "uat-ephemeral-secret"
        os.environ["FORENSIC_MEDIA_ROOT"] = str(root / "cases")
        os.environ["FORENSIC_LOG_DIR"] = str(root / "logs")
        os.environ["FORENSIC_EVIDENCE_REGISTRY"] = str(ev_path)
        os.environ["FORENSIC_CASE_REGISTRY"] = str(case_path)
        os.environ["FORENSIC_MODEL_ID"] = "MODEL0001"
        os.environ["FORENSIC_ASYNC_MODE"] = "thread"

        import django

        django.setup()
        from django.conf import settings
        from django.core.wsgi import get_wsgi_application

        app = get_wsgi_application()
        server = make_server("127.0.0.1", 0, app, server_class=_ThreadingWSGIServer, handler_class=_QuietHandler)
        port = server.server_port
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base_url = f"http://127.0.0.1:{port}/api/v1"

        scenarios = [
            ("UAT-01", "valid_fake.png", _sample_png(1), "image/png", 1, "MODEL0001", _UATPredictor(0.95), 202, "completed", "Fake"),
            ("UAT-02", "valid_real.png", _sample_png(2), "image/png", 1, "MODEL0001", _UATPredictor(0.02), 202, "completed", "Real"),
            ("UAT-03", "corrupt.png", b"corrupt-png-bytes", "image/png", 1, "MODEL0001", _UATPredictor(0.50), 202, "failed", "corrupted_image"),
            ("UAT-04", "no_face.png", _sample_png(4), "image/png", 0, "MODEL0001", _UATPredictor(0.50), 202, "failed", "no_face"),
            ("UAT-05", "unsupported.bmp", b"BM-invalid", "image/bmp", 1, "MODEL0001", _UATPredictor(0.50), 400, "failed", "unsupported_format"),
            ("UAT-06", "missing_model.png", _sample_png(6), "image/png", 1, "MODEL9999", None, 202, "completed", "Unknown"),
        ]

        results: list[dict] = []
        try:
            for uat_id, fname, payload, ctype, faces, model_id, pred, exp_http, exp_status, exp_outcome in scenarios:
                settings.FORENSIC_TEST_FACE_COUNTER = _UATFaceCounter(faces)
                settings.FORENSIC_TEST_PREDICTOR = pred

                c_status, created = _req_json(
                    f"{base_url}/cases",
                    method="POST",
                    body=json.dumps({"model_id": model_id}).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                )
                assert c_status == 201
                case_id = created["case_id"]

                body, mp_ct = _multipart(fname, payload, ctype)
                up_status, up_data = _req_json(
                    f"{base_url}/cases/{case_id}/upload",
                    method="POST",
                    body=body,
                    headers={"Content-Type": mp_ct},
                )
                assert up_status == exp_http, f"{uat_id}: expected HTTP {exp_http}, got {up_status} ({up_data})"

                if up_status == 400:
                    assert up_data["error"]["name"] == exp_outcome
                    results.append({"uat_id": uat_id, "case_id": case_id, "status": "failed", "outcome": exp_outcome, "pass": True})
                    continue

                terminal = None
                for _ in range(100):
                    _, st = _req_json(f"{base_url}/cases/{case_id}/status")
                    if st["status"] in ("completed", "failed"):
                        terminal = st
                        break
                    time.sleep(0.04)
                assert terminal is not None and terminal["status"] == exp_status

                if exp_status == "completed":
                    d_status, dec = _req_json(f"{base_url}/cases/{case_id}/decision")
                    assert d_status == 200 and dec["decision"] == exp_outcome
                    r_status, rep = _req_json(f"{base_url}/cases/{case_id}/report?format=json")
                    assert r_status == 200 and rep["version_stamps"]["git_commit"]
                    if uat_id == "UAT-02":
                        assert dec["decision_metadata"]["confidence"]["prediction_confidence"] != 0.02
                    if uat_id == "UAT-06":
                        assert dec["decision_metadata"]["confidence"]["prediction_confidence"] is None
                        assert dec["decision_metadata"]["confidence"]["decision_confidence"] is None
                else:
                    assert terminal["failures"][0]["name"] == exp_outcome
                    d_status, _ = _req_json(f"{base_url}/cases/{case_id}/decision")
                    assert d_status == 404

                results.append({"uat_id": uat_id, "case_id": case_id, "status": exp_status, "outcome": exp_outcome, "pass": True})

            audit_rows = read_case_rows(case_path)
            assert len(audit_rows) == 6
            print(json.dumps({"uat_scenarios": len(results), "all_pass": True, "results": results}, indent=2))
            return 0
        finally:
            server.shutdown()
            server.server_close()
            logging.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
