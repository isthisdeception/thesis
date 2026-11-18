"""Read-only adapter over `MOD012` generated reports (`json`, `markdown`, `html`)."""

from __future__ import annotations

import json
from typing import Any

from apps.core.config import BackendConfig

ALLOWED_REPORT_FORMATS = ("json", "markdown", "html")


def read_case_report(
    config: BackendConfig,
    case_id: str,
    *,
    report_format: str = "json",
) -> tuple[Any, str] | None:
    """Return `(content, content_type)` for the requested report format, or `None` if not generated."""

    fmt = (report_format or "json").strip().lower()
    if fmt not in ALLOWED_REPORT_FORMATS:
        raise ValueError(f"unsupported report format {report_format!r}; expected one of {ALLOWED_REPORT_FORMATS}")

    reports_dir = config.media_root / case_id / "reports"
    if fmt == "json":
        path = reports_dir / f"{case_id}_report.json"
        if not path.is_file():
            return None
        return json.loads(path.read_text(encoding="utf-8")), "application/json"
    if fmt == "markdown":
        path = reports_dir / f"{case_id}_report.md"
        if not path.is_file():
            return None
        return path.read_text(encoding="utf-8"), "text/markdown; charset=utf-8"
    path = reports_dir / f"{case_id}_report.html"
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8"), "text/html; charset=utf-8"
