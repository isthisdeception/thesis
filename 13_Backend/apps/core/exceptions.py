"""DRF exception handler and MOD016 error envelope builder (§8.7). Never exposes stack traces to clients."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .config import ensure_forensic_sys_path
from .logging_config import get_channel_logger

ensure_forensic_sys_path()
from failure_handling import FAILURE_NAMES, FailureRecord  # noqa: E402


def make_error_envelope(
    *,
    detail: str = "",
    name: str = "unexpected_error",
    module_id: str = "MOD013",
    case_id: str = "",
    input_id: str | None = None,
    failure_id: str = "",
    record: FailureRecord | None = None,
) -> dict[str, Any]:
    if record is not None:
        return {"error": record.to_json()}
    canonical = name if name in FAILURE_NAMES else "unexpected_error"
    stamp = datetime.now().astimezone().replace(microsecond=0).isoformat()
    return {
        "error": {
            "failure_id": failure_id,
            "name": canonical,
            "reported_name": name if name in FAILURE_NAMES else canonical,
            "module_id": module_id,
            "case_id": case_id,
            "input_id": input_id,
            "detail": detail,
            "timestamp": stamp,
        }
    }


def forensic_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    """Catch DRF and unhandled exceptions, log server-side, and return a clean MOD016 envelope without stack traces."""

    from django.conf import settings

    err_logger = get_channel_logger("error", getattr(settings, "FORENSIC_CONFIG", None) and settings.FORENSIC_CONFIG.log_dir)
    view = context.get("view")
    kwargs = getattr(view, "kwargs", {}) if view is not None else {}
    case_id = str(kwargs.get("case_id") or kwargs.get("id") or "")

    drf_response = exception_handler(exc, context)
    if drf_response is not None:
        raw_detail = drf_response.data
        if isinstance(raw_detail, dict) and "error" in raw_detail and isinstance(raw_detail["error"], dict):
            return drf_response
        detail_str = str(raw_detail.get("detail") if isinstance(raw_detail, dict) and "detail" in raw_detail else raw_detail)
        err_logger.warning("API handled error | case_id=%s | status=%s | detail=%s", case_id, drf_response.status_code, detail_str)
        envelope = make_error_envelope(detail=detail_str, case_id=case_id)
        return Response(envelope, status=drf_response.status_code)

    err_logger.exception("Unhandled server exception | case_id=%s | type=%s", case_id, exc.__class__.__name__)
    envelope = make_error_envelope(
        detail="An unexpected server error occurred.",
        name="unexpected_error",
        module_id="MOD013",
        case_id=case_id,
    )
    return Response(envelope, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
