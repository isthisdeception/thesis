"""STEP-066 live cross-tier integration verifier.

Boots the real Django REST API (`13_Backend`) on an ephemeral localhost port using `thread` async mode,
wires `12_Web` via `VITE_API_BASE_URL`, and executes the live React Vitest flow against the live server
with zero mocked HTTP calls.
"""

from __future__ import annotations

import logging
import os
import socketserver
import subprocess
import sys
import tempfile
import threading
from pathlib import Path
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer, make_server

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
AUTOMATION_DIR = str(Path(__file__).resolve().parent)
sys.path[:] = [p for p in sys.path if os.path.abspath(p or ".") != AUTOMATION_DIR]
BACKEND_DIR = REPO_ROOT / "13_Backend"
WEB_DIR = REPO_ROOT / "12_Web"
FORENSIC_DIR = REPO_ROOT / "11_AI_Forensic_System"

for p in (str(BACKEND_DIR), str(FORENSIC_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from audit import HEADER as CASE_HEADER  # noqa: E402
from evidence.collectors.deep_learning_specialist.fastai_export import Inference  # noqa: E402
from evidence.registry import HEADER as EV_HEADER  # noqa: E402


class _IntegrationFaceCounter:
    def count_faces(self, image: Image.Image) -> int:
        return 1


class _IntegrationPredictor:
    def predict(self, image: Image.Image) -> Inference:
        return Inference(fake_probability=0.92, embedding=[0.1, 0.2], model_confidence=None)


class _ThreadingWSGIServer(socketserver.ThreadingMixIn, WSGIServer):
    daemon_threads = True


def main() -> int:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        root = Path(tmp)
        ev_path = root / "evidence_registry.csv"
        ev_path.write_text(",".join(EV_HEADER) + "\n", encoding="utf-8")
        case_path = root / "case_registry.csv"
        case_path.write_text(",".join(CASE_HEADER) + "\n", encoding="utf-8")

        os.environ["DJANGO_SETTINGS_MODULE"] = "forensic_backend.settings"
        os.environ["DJANGO_ENV"] = "test"
        os.environ["DJANGO_SECRET_KEY"] = "live-integration-ephemeral-key"
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

        settings.FORENSIC_TEST_FACE_COUNTER = _IntegrationFaceCounter()
        settings.FORENSIC_TEST_PREDICTOR = _IntegrationPredictor()

        app = get_wsgi_application()
        server = make_server("127.0.0.1", 0, app, server_class=_ThreadingWSGIServer, handler_class=WSGIRequestHandler)
        port = server.server_port
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        live_api_url = f"http://127.0.0.1:{port}/api/v1"
        print(f"Live Django backend listening on {live_api_url}")
        import base64
        import io

        img = Image.new("RGB", (64, 64))
        img.putdata(
            [
                (((x * 7 + y * 3) % 256), ((x * 5 + y * 11) % 256), ((x * 13 + y * 17) % 256))
                for y in range(64)
                for x in range(64)
            ]
        )
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        png_b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        try:
            env = dict(os.environ)
            env["VITE_API_BASE_URL"] = live_api_url
            env["VITE_LIVE_API_URL"] = live_api_url
            env["VITE_TEST_PNG_BASE64"] = png_b64
            env["VITE_POLL_INTERVAL_MS"] = "50"
            npx_cmd = "npx.cmd" if os.name == "nt" else "npx"
            proc = subprocess.run(
                [npx_cmd, "vitest", "run", "src/__tests__/live_integration.test.jsx"],
                cwd=str(WEB_DIR),
                env=env,
                check=False,
            )
            return proc.returncode
        finally:
            server.shutdown()
            server.server_close()
            logging.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
