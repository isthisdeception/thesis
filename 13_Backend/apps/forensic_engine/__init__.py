"""Single-responsibility forensic_engine app: wraps `11_AI_Forensic_System/pipeline.py` as an async/eager job."""

from .service import (
    DEFAULT_FACE_COUNTER,
    allocate_case,
    case_exists,
    get_case_detail,
    get_job_status,
    submit_investigation_upload,
    wait_for_case_job,
)

__all__ = [
    "DEFAULT_FACE_COUNTER",
    "allocate_case",
    "case_exists",
    "get_case_detail",
    "get_job_status",
    "submit_investigation_upload",
    "wait_for_case_job",
]
