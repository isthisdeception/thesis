"""Bridge to `11_AI_Forensic_System/pipeline.py`. Zero duplicated forensic or inference logic."""

from __future__ import annotations

import json
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from typing import Any

from PIL import Image

from apps.core.config import BackendConfig, ensure_forensic_sys_path
from apps.core.logging_config import get_channel_logger

ensure_forensic_sys_path()
from audit import CASE_ID_PATTERN, read_case_rows  # noqa: E402
from evidence.collectors.deep_learning_specialist.collector import Predictor  # noqa: E402
from evidence.item import SCHEMA_VERSION, clock  # noqa: E402
from failure_handling import read_case_failures  # noqa: E402
from fusion.interface import safe_raw  # noqa: E402
from image_validation import FaceCounter  # noqa: E402
from image_validation.faces import count_faces_opencv  # noqa: E402
from input_management import IntakeConfig, IntakeResult, receive_upload  # noqa: E402
from pipeline import PROGRESS_STAGES, InvestigationResult, run_investigation  # noqa: E402

_EXECUTOR = ThreadPoolExecutor(max_workers=4, thread_name_prefix="forensic-job")
_LOCK = threading.Lock()
_PIPELINE_LOCK = threading.Lock()
_FUTURES: dict[str, Future] = {}


class _DefaultFaceCounter:
    """Calls OpenCV Haar cascade when installed, else reports 1 face if image has non-zero dimensions."""

    def count_faces(self, image: Image.Image) -> int:
        try:
            return count_faces_opencv(image)
        except Exception:
            return 1 if (image.width > 0 and image.height > 0) else 0


DEFAULT_FACE_COUNTER: FaceCounter = _DefaultFaceCounter()


def _next_available_case_id(config: BackendConfig) -> str:
    numbers: list[int] = []
    if config.case_registry_path.is_file():
        for row in read_case_rows(config.case_registry_path):
            cid = row.get("Case ID", "")
            if CASE_ID_PATTERN.match(cid):
                numbers.append(int(cid[4:]))
    if config.media_root.is_dir():
        for child in config.media_root.iterdir():
            if child.is_dir() and CASE_ID_PATTERN.match(child.name):
                numbers.append(int(child.name[4:]))
    return f"CASE{max(numbers, default=0) + 1:06d}"


def _job_status_path(config: BackendConfig, case_id: str) -> Path:
    return config.media_root / case_id / "job_status.json"


def _write_job_status(config: BackendConfig, case_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    path = _job_status_path(config, case_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def allocate_case(
    config: BackendConfig,
    *,
    model_id: str | None = None,
    configuration: str = "rule_based/e4_calibrated_v1",
) -> dict[str, Any]:
    """Allocate a new `CASExxxxxx` directory and initial `job_status.json`."""

    with _LOCK:
        case_id = _next_available_case_id(config)
        stamp = clock()
        selected_model = (model_id or config.model_id).strip() or config.model_id
        payload = {
            "case_id": case_id,
            "status": "created",
            "stage": "Created",
            "stage_history": [],
            "progress_percent": 0,
            "input_id": None,
            "model_id": selected_model,
            "configuration": configuration,
            "created_timestamp": stamp,
            "updated_timestamp": stamp,
        }
        _write_job_status(config, case_id, payload)
    get_channel_logger("case", config.log_dir).info(
        "Case allocated | case_id=%s | model_id=%s | config=%s",
        case_id,
        selected_model,
        configuration,
    )
    return {
        "case_id": case_id,
        "status": "created",
        "stage": "Created",
        "model_id": selected_model,
        "configuration": configuration,
        "created_timestamp": stamp,
    }


def case_exists(config: BackendConfig, case_id: str) -> bool:
    if not CASE_ID_PATTERN.match(case_id or ""):
        return False
    if _job_status_path(config, case_id).is_file():
        return True
    if config.case_registry_path.is_file():
        return any(r.get("Case ID") == case_id for r in read_case_rows(config.case_registry_path))
    return False


def get_job_status(config: BackendConfig, case_id: str) -> dict[str, Any] | None:
    """Return live progress (`MOD014` stage label, `progress_percent`, and `MOD016` failures) for `case_id`."""

    if not case_exists(config, case_id):
        return None
    path = _job_status_path(config, case_id)
    if path.is_file():
        base = json.loads(path.read_text(encoding="utf-8"))
    else:
        base = {
            "case_id": case_id,
            "status": "completed",
            "stage": "Complete",
            "stage_history": list(PROGRESS_STAGES),
            "progress_percent": 100,
            "input_id": None,
            "updated_timestamp": clock(),
        }
    failures = [rec.to_json() for rec in read_case_failures(config.media_root, case_id)]
    return {
        "case_id": case_id,
        "status": base.get("status", "created"),
        "stage": base.get("stage", "Created"),
        "stage_history": list(base.get("stage_history", [])),
        "progress_percent": int(base.get("progress_percent", 0)),
        "input_id": base.get("input_id"),
        "failures": failures,
        "updated_timestamp": base.get("updated_timestamp") or clock(),
    }


def get_case_detail(config: BackendConfig, case_id: str) -> dict[str, Any] | None:
    """Combine `case_registry.csv` (`MOD015`) and live `job_status.json` for `GET /cases/{id}`."""

    job = get_job_status(config, case_id)
    if job is None:
        return None
    reg_row: dict[str, str] | None = None
    if config.case_registry_path.is_file():
        matches = [r for r in read_case_rows(config.case_registry_path) if r.get("Case ID") == case_id]
        if matches:
            reg_row = matches[-1]

    status_file = _job_status_path(config, case_id)
    raw_job = json.loads(status_file.read_text(encoding="utf-8")) if status_file.is_file() else {}

    if reg_row is not None:
        exec_str = reg_row.get("Execution Time", "")
        return {
            "case_id": case_id,
            "status": reg_row.get("Status") or job["status"],
            "stage": job["stage"],
            "input_id": reg_row.get("Input") or job["input_id"],
            "evidence_ids": [part for part in reg_row.get("Evidence", "").split(";") if part],
            "decision": reg_row.get("Decision", ""),
            "model_id": reg_row.get("Model") or raw_job.get("model_id", config.model_id),
            "version": reg_row.get("Version") or SCHEMA_VERSION,
            "configuration": reg_row.get("Configuration") or raw_job.get("configuration", "rule_based/e4_calibrated_v1"),
            "execution_time_seconds": float(exec_str) if exec_str not in ("", None) else None,
            "errors": [part for part in reg_row.get("Errors", "").split(";") if part],
            "warnings": [part for part in reg_row.get("Warnings", "").split(";") if part],
            "timestamp": reg_row.get("Timestamp") or job["updated_timestamp"],
        }

    return {
        "case_id": case_id,
        "status": job["status"],
        "stage": job["stage"],
        "input_id": job["input_id"],
        "evidence_ids": [],
        "decision": "",
        "model_id": raw_job.get("model_id", config.model_id),
        "version": SCHEMA_VERSION,
        "configuration": raw_job.get("configuration", "rule_based/e4_calibrated_v1"),
        "execution_time_seconds": None,
        "errors": [f["failure_id"] for f in job["failures"] if f.get("name") != "low_confidence"],
        "warnings": [f["failure_id"] for f in job["failures"] if f.get("name") == "low_confidence"],
        "timestamp": job["updated_timestamp"],
    }


def _execute_pipeline_job(
    config: BackendConfig,
    *,
    case_id: str,
    filename: str,
    data: bytes,
    intake_res: IntakeResult,
    model_id: str,
    configuration_id: str,
    face_counter: FaceCounter,
    predictor: Predictor | None,
) -> InvestigationResult:
    case_log = get_channel_logger("case", config.log_dir)
    inf_log = get_channel_logger("inference", config.log_dir)
    aud_log = get_channel_logger("audit", config.log_dir)
    perf_log = get_channel_logger("performance", config.log_dir)
    err_log = get_channel_logger("error", config.log_dir)

    input_id = str(intake_res.metadata.get("input_id") or "")

    def on_stage(stage_label: str, history: list[str]) -> None:
        pct = int(round((len(history) / len(PROGRESS_STAGES)) * 100))
        _write_job_status(
            config,
            case_id,
            {
                "case_id": case_id,
                "status": "completed" if stage_label == "Complete" else "running",
                "stage": stage_label,
                "stage_history": history,
                "progress_percent": min(100, pct),
                "input_id": input_id,
                "model_id": model_id,
                "configuration": configuration_id,
                "updated_timestamp": clock(),
            },
        )
        case_log.info("Stage transition | case_id=%s | stage=%s | progress=%d%%", case_id, stage_label, pct)

    with _PIPELINE_LOCK:
        res = run_investigation(
            case_id=case_id,
            filename=filename,
            data=data,
            storage_root=config.media_root,
            evidence_registry_path=config.evidence_registry_path,
            case_registry_path=config.case_registry_path,
            face_counter=face_counter,
            model_id=model_id,
            predictor=predictor,
            artifact_root=config.artifact_root,
            intake_result=intake_res,
            stage_callback=on_stage,
            configuration_id=configuration_id,
            repo_root=config.repo_root,
        )

    if res.status != "completed":
        _write_job_status(
            config,
            case_id,
            {
                "case_id": case_id,
                "status": "failed",
                "stage": "Failed",
                "stage_history": list(res.stage_history),
                "progress_percent": int(round((len(res.stage_history) / len(PROGRESS_STAGES)) * 100)),
                "input_id": input_id,
                "model_id": model_id,
                "configuration": configuration_id,
                "updated_timestamp": clock(),
            },
        )
        for failure in res.failures:
            err_log.warning(
                "Case failure | case_id=%s | failure_id=%s | module=%s | name=%s | detail=%s",
                case_id,
                failure.failure_id,
                failure.module_id,
                failure.name,
                failure.detail,
            )

    inf_log.info(
        "Detector step finished | case_id=%s | model_id=%s | status=%s",
        case_id,
        model_id,
        res.status,
    )
    if res.case_row is not None:
        aud_log.info(
            "Audit row written | case_id=%s | status=%s | decision=%s | ev_count=%d",
            case_id,
            res.case_row.status,
            res.case_row.decision or "none",
            len(res.case_row.evidence_ids),
        )
    perf_log.info(
        "Case finished | case_id=%s | status=%s | elapsed_ms=%.2f",
        case_id,
        res.status,
        res.execution_time_seconds * 1000.0,
    )
    return res


def submit_investigation_upload(
    config: BackendConfig,
    *,
    case_id: str,
    filename: str,
    data: bytes,
    face_counter: FaceCounter | None = None,
    predictor: Predictor | None = None,
) -> tuple[IntakeResult, dict[str, Any]]:
    """Run `MOD001` intake immediately; if accepted, run or enqueue `11_AI_Forensic_System/pipeline.py`."""

    status_file = _job_status_path(config, case_id)
    raw_job = json.loads(status_file.read_text(encoding="utf-8")) if status_file.is_file() else {}
    model_id = str(raw_job.get("model_id") or config.model_id)
    configuration_id = str(raw_job.get("configuration") or "rule_based/e4_calibrated_v1")
    fc = face_counter or DEFAULT_FACE_COUNTER

    intake_cfg = IntakeConfig(max_bytes=config.max_upload_bytes)
    intake_res = receive_upload(
        case_id=case_id,
        filename=filename,
        data=data,
        storage_root=config.media_root,
        config=intake_cfg,
    )
    sanitized_intake = safe_raw(dict(intake_res.metadata))

    if not intake_res.accepted:
        # Finalize failed case row via the pipeline immediately
        _execute_pipeline_job(
            config,
            case_id=case_id,
            filename=filename,
            data=data,
            intake_res=intake_res,
            model_id=model_id,
            configuration_id=configuration_id,
            face_counter=fc,
            predictor=predictor,
        )
        return intake_res, {
            "case_id": case_id,
            "input_id": intake_res.metadata.get("input_id"),
            "intake": sanitized_intake,
            "job_status": "failed",
            "stage": "Failed",
        }

    input_id = str(intake_res.metadata.get("input_id") or "")
    _write_job_status(
        config,
        case_id,
        {
            "case_id": case_id,
            "status": "running",
            "stage": "Uploading",
            "stage_history": ["Uploading"],
            "progress_percent": int(round((1 / len(PROGRESS_STAGES)) * 100)),
            "input_id": input_id,
            "model_id": model_id,
            "configuration": configuration_id,
            "updated_timestamp": clock(),
        },
    )

    if config.async_mode == "eager":
        res = _execute_pipeline_job(
            config,
            case_id=case_id,
            filename=filename,
            data=data,
            intake_res=intake_res,
            model_id=model_id,
            configuration_id=configuration_id,
            face_counter=fc,
            predictor=predictor,
        )
        return intake_res, {
            "case_id": case_id,
            "input_id": input_id,
            "intake": sanitized_intake,
            "job_status": res.status,
            "stage": "Complete" if res.status == "completed" else "Failed",
        }

    future = _EXECUTOR.submit(
        _execute_pipeline_job,
        config,
        case_id=case_id,
        filename=filename,
        data=data,
        intake_res=intake_res,
        model_id=model_id,
        configuration_id=configuration_id,
        face_counter=fc,
        predictor=predictor,
    )
    with _LOCK:
        _FUTURES[case_id] = future

    return intake_res, {
        "case_id": case_id,
        "input_id": input_id,
        "intake": sanitized_intake,
        "job_status": "running",
        "stage": "Uploading",
    }


def wait_for_case_job(case_id: str, timeout: float = 10.0) -> InvestigationResult | None:
    """Wait for an in-flight background job (used by tests and graceful shutdown)."""

    with _LOCK:
        future = _FUTURES.get(case_id)
    if future is None:
        return None
    return future.result(timeout=timeout)
