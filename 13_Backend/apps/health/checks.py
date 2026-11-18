"""Lightweight health check (`GET /health`). Does not load a case or model weights (`MOD013_spec.md`)."""

from __future__ import annotations

from typing import Any

from apps.core.config import BackendConfig, ensure_forensic_sys_path

ensure_forensic_sys_path()
from evidence.item import clock  # noqa: E402


def check_system_health(config: BackendConfig) -> tuple[dict[str, Any], bool]:
    """Return `(payload, is_healthy)` without opening a case or loading model weights."""

    media_writable = False
    try:
        config.media_root.mkdir(parents=True, exist_ok=True)
        media_writable = config.media_root.is_dir()
    except OSError:
        media_writable = False

    ev_readable = config.evidence_registry_path.is_file()
    case_readable = config.case_registry_path.is_file()
    model_reg_path = config.repo_root / "05_Models" / "model_registry.csv"
    model_readable = model_reg_path.is_file()

    checks = {
        "media_root_writable": media_writable,
        "evidence_registry_readable": ev_readable,
        "case_registry_readable": case_readable,
        "model_registry_readable": model_readable,
    }
    healthy = all(checks.values())
    payload = {
        "status": "ok" if healthy else "degraded",
        "service": "ai-forensic-analyst-backend",
        "environment": config.env,
        "checks": checks,
        "timestamp": clock(),
    }
    return payload, healthy
