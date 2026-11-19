"""Canonical REST API views (STEP-062 / MOD013).

Matches `13_Backend/api_spec/api_spec.md` and `11_AI_Forensic_System/specs/MOD013_spec.md` exactly.
This layer does not run a model directly and does not choose a decision; it delegates to `apps.forensic_engine`
and transports the records written by `11_AI_Forensic_System`.
"""

from __future__ import annotations

import time
from typing import Any

from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.config import BackendConfig, ensure_forensic_sys_path
from apps.core.exceptions import make_error_envelope
from apps.core.logging_config import get_channel_logger
from apps.evidence import read_case_decision, read_case_evidence, read_case_explanation
from apps.forensic_engine import (
    allocate_case,
    case_exists,
    get_case_detail,
    get_job_status,
    submit_investigation_upload,
)
from apps.health import check_system_health
from apps.reports import ALLOWED_REPORT_FORMATS, read_case_report
from apps.versioning import get_version_info

from .serializers import (
    CaseCreateRequestSerializer,
    CaseCreateResponseSerializer,
    CaseDetailResponseSerializer,
    CaseEvidenceResponseSerializer,
    CaseStatusResponseSerializer,
    CaseUploadRequestSerializer,
    CaseUploadResponseSerializer,
    HealthResponseSerializer,
    VersionResponseSerializer,
)
from .throttles import ApiReadRateThrottle, UploadRateThrottle

ensure_forensic_sys_path()
from audit import CASE_ID_PATTERN  # noqa: E402
from evidence.collectors.deep_learning_specialist.lookup import RegistryError  # noqa: E402
from failure_handling import read_case_failures, write_failure  # noqa: E402

MODULE_ID = "MOD013"


def get_active_config() -> BackendConfig:
    return settings.FORENSIC_CONFIG


class ForensicAPIView(APIView):
    """Base APIView that logs every HTTP request/response to the `forensic.api` channel."""

    throttle_classes = [ApiReadRateThrottle]

    def dispatch(self, request, *args, **kwargs):
        started = time.perf_counter()
        response = super().dispatch(request, *args, **kwargs)
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        cfg = get_active_config()
        get_channel_logger("api", cfg.log_dir).info(
            "HTTP %s %s -> %s (%.2f ms)",
            request.method,
            request.get_full_path(),
            getattr(response, "status_code", "?"),
            elapsed_ms,
        )
        return response


def _validate_case_id_or_error(config: BackendConfig, case_id: str) -> Response | None:
    if not CASE_ID_PATTERN.match(case_id or ""):
        return Response(
            make_error_envelope(
                detail=f"case id {case_id!r} must match CASExxxxxx",
                name="unexpected_error",
                module_id=MODULE_ID,
                case_id=case_id,
            ),
            status=status.HTTP_400_BAD_REQUEST,
        )
    if not case_exists(config, case_id):
        return Response(
            make_error_envelope(
                detail=f"case {case_id} was not found",
                name="unexpected_error",
                module_id=MODULE_ID,
                case_id=case_id,
            ),
            status=status.HTTP_404_NOT_FOUND,
        )
    return None


class CaseCreateView(ForensicAPIView):
    """`POST /cases` — allocate a new immutable `CASExxxxxx` identifier."""

    def post(self, request: Request) -> Response:
        cfg = get_active_config()
        serializer = CaseCreateRequestSerializer(data=request.data if request.data else {})
        if not serializer.is_valid():
            return Response(
                make_error_envelope(
                    detail=str(serializer.errors),
                    name="unexpected_error",
                    module_id=MODULE_ID,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        validated = serializer.validated_data
        allocated = allocate_case(
            cfg,
            model_id=validated.get("model_id"),
            configuration=validated.get("configuration", "rule_based/e4_calibrated_v1"),
        )
        out = CaseCreateResponseSerializer(allocated)
        return Response(out.data, status=status.HTTP_201_CREATED)


class CaseDetailView(ForensicAPIView):
    """`GET /cases/{id}` — return the case record and live stage."""

    def get(self, request: Request, case_id: str) -> Response:
        cfg = get_active_config()
        err = _validate_case_id_or_error(cfg, case_id)
        if err is not None:
            return err
        detail = get_case_detail(cfg, case_id)
        if detail is None:
            return Response(
                make_error_envelope(
                    detail=f"case {case_id} was not found",
                    name="unexpected_error",
                    module_id=MODULE_ID,
                    case_id=case_id,
                ),
                status=status.HTTP_404_NOT_FOUND,
            )
        out = CaseDetailResponseSerializer(detail)
        return Response(out.data, status=status.HTTP_200_OK)


class CaseUploadView(ForensicAPIView):
    """`POST /cases/{id}/upload` — receive one image via MOD001 and trigger the investigation job."""

    throttle_classes = [UploadRateThrottle]

    def post(self, request: Request, case_id: str) -> Response:
        cfg = get_active_config()
        err = _validate_case_id_or_error(cfg, case_id)
        if err is not None:
            return err

        serializer = CaseUploadRequestSerializer(data=request.FILES)
        if not serializer.is_valid():
            failure = write_failure(
                cfg.media_root,
                name="unexpected_error",
                module_id="MOD001",
                case_id=case_id,
                detail="upload request is missing required 'file' field",
            )
            return Response(
                make_error_envelope(record=failure),
                status=status.HTTP_400_BAD_REQUEST,
            )

        uploaded = serializer.validated_data["file"]
        raw_bytes = uploaded.read()
        face_counter = getattr(settings, "FORENSIC_TEST_FACE_COUNTER", None)
        predictor = getattr(settings, "FORENSIC_TEST_PREDICTOR", None)

        intake_res, job_payload = submit_investigation_upload(
            cfg,
            case_id=case_id,
            filename=uploaded.name or "",
            data=raw_bytes,
            face_counter=face_counter,
            predictor=predictor,
        )
        if not intake_res.accepted:
            return Response(
                make_error_envelope(record=intake_res.failure),
                status=status.HTTP_400_BAD_REQUEST,
            )

        out = CaseUploadResponseSerializer(job_payload)
        http_status = status.HTTP_200_OK if job_payload["job_status"] == "completed" else status.HTTP_202_ACCEPTED
        return Response(out.data, status=http_status)


class CaseStatusView(ForensicAPIView):
    """`GET /cases/{id}/status` — return current MOD014 progress stage and MOD016 failure records."""

    def get(self, request: Request, case_id: str) -> Response:
        cfg = get_active_config()
        err = _validate_case_id_or_error(cfg, case_id)
        if err is not None:
            return err
        job = get_job_status(cfg, case_id)
        out = CaseStatusResponseSerializer(job)
        return Response(out.data, status=status.HTTP_200_OK)


class CaseEvidenceView(ForensicAPIView):
    """`GET /cases/{id}/evidence` — return registered and validated evidence rows for `case_id`."""

    def get(self, request: Request, case_id: str) -> Response:
        cfg = get_active_config()
        err = _validate_case_id_or_error(cfg, case_id)
        if err is not None:
            return err
        validated_only = request.query_params.get("validated_only", "false").strip().lower() in ("true", "1", "yes")
        payload = read_case_evidence(cfg, case_id, validated_only=validated_only)
        out = CaseEvidenceResponseSerializer(payload)
        return Response(out.data, status=status.HTTP_200_OK)


class CaseDecisionView(ForensicAPIView):
    """`GET /cases/{id}/decision` — return `decision.json` written by MOD008 unchanged (`MOD013_spec.md`)."""

    def get(self, request: Request, case_id: str) -> Response:
        cfg = get_active_config()
        err = _validate_case_id_or_error(cfg, case_id)
        if err is not None:
            return err
        dec_payload = read_case_decision(cfg, case_id)
        if dec_payload is None:
            failures = read_case_failures(cfg.media_root, case_id)
            if failures:
                return Response(
                    make_error_envelope(record=failures[-1]),
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(
                make_error_envelope(
                    detail=f"decision.json is not available for {case_id}",
                    name="unexpected_error",
                    module_id=MODULE_ID,
                    case_id=case_id,
                ),
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(dec_payload, status=status.HTTP_200_OK)


class CaseExplanationView(ForensicAPIView):
    """`GET /cases/{id}/explanation` — return data-only `explanation.json` (plus `reasoning.json` if requested)."""

    def get(self, request: Request, case_id: str) -> Response:
        cfg = get_active_config()
        err = _validate_case_id_or_error(cfg, case_id)
        if err is not None:
            return err
        include_reas = request.query_params.get("include_reasoning", "false").strip().lower() in ("true", "1", "yes")
        expl_payload = read_case_explanation(cfg, case_id, include_reasoning=include_reas)
        if expl_payload is None:
            failures = read_case_failures(cfg.media_root, case_id)
            if failures:
                return Response(
                    make_error_envelope(record=failures[-1]),
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(
                make_error_envelope(
                    detail=f"explanation.json is not available for {case_id}",
                    name="unexpected_error",
                    module_id=MODULE_ID,
                    case_id=case_id,
                ),
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(expl_payload, status=status.HTTP_200_OK)


class CaseReportView(ForensicAPIView):
    """`GET /cases/{id}/report` — return reproducible case report in `json`, `markdown`, or `html`."""

    def get(self, request: Request, case_id: str) -> Response | HttpResponse:
        cfg = get_active_config()
        err = _validate_case_id_or_error(cfg, case_id)
        if err is not None:
            return err
        fmt = request.query_params.get("format", "json").strip().lower() or "json"
        if fmt not in ALLOWED_REPORT_FORMATS:
            return Response(
                make_error_envelope(
                    detail=f"unsupported report format {fmt!r}; expected one of {ALLOWED_REPORT_FORMATS}",
                    name="unexpected_error",
                    module_id=MODULE_ID,
                    case_id=case_id,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        found = read_case_report(cfg, case_id, report_format=fmt)
        if found is None:
            failures = read_case_failures(cfg.media_root, case_id)
            if failures:
                return Response(
                    make_error_envelope(record=failures[-1]),
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(
                make_error_envelope(
                    detail=f"report is not available for {case_id}",
                    name="unexpected_error",
                    module_id=MODULE_ID,
                    case_id=case_id,
                ),
                status=status.HTTP_404_NOT_FOUND,
            )
        content, content_type = found
        if fmt == "json":
            return Response(content, status=status.HTTP_200_OK)
        return HttpResponse(content, content_type=content_type, status=status.HTTP_200_OK)


class HealthView(ForensicAPIView):
    """`GET /health` — lightweight service and registry health check without loading a case."""

    def get(self, request: Request) -> Response:
        cfg = get_active_config()
        payload, healthy = check_system_health(cfg)
        out = HealthResponseSerializer(payload)
        http_status = status.HTTP_200_OK if healthy else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response(out.data, status=http_status)


class VersionView(ForensicAPIView):
    """`GET /version` — return system, API, model, dataset, experiment, and Git commit versions."""

    def get(self, request: Request) -> Response:
        cfg = get_active_config()
        try:
            payload = get_version_info(cfg)
        except RegistryError as exc:
            return Response(
                make_error_envelope(
                    detail=str(exc),
                    name="model_unavailable",
                    module_id=MODULE_ID,
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        out = VersionResponseSerializer(payload)
        return Response(out.data, status=status.HTTP_200_OK)
