"""Structured failure reports. Callers stop; this module does not decide a case."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

FAILURE_NAMES = (
    "no_face",
    "multiple_faces",
    "corrupted_image",
    "unsupported_format",
    "model_unavailable",
    "low_confidence",
    "timeout",
    "unexpected_error",
)


@dataclass(frozen=True)
class FailureRecord:
    failure_id: str
    name: str
    reported_name: str
    module_id: str
    case_id: str
    input_id: str | None
    detail: str
    timestamp: str

    def to_json(self) -> dict:
        return asdict(self)


def write_failure(
    storage_root: Path,
    *,
    name: str,
    module_id: str,
    case_id: str,
    detail: str,
    input_id: str | None = None,
    now: datetime | None = None,
) -> FailureRecord:
    """Append one failure file. An unknown name is stored as unexpected_error."""

    reported = name
    canonical = name if name in FAILURE_NAMES else "unexpected_error"
    if canonical != name and name:
        detail = f"{detail} reported_name={name}".strip()
    case_dir = storage_root / case_id / "failures"
    case_dir.mkdir(parents=True, exist_ok=True)
    seq = len(list(case_dir.glob("*.json"))) + 1
    failure_id = f"{case_id}-fail-{seq:02d}"
    stamp = (now or datetime.now().astimezone()).replace(microsecond=0).isoformat()
    record = FailureRecord(
        failure_id=failure_id,
        name=canonical,
        reported_name=reported if reported in FAILURE_NAMES else canonical,
        module_id=module_id,
        case_id=case_id,
        input_id=input_id,
        detail=detail,
        timestamp=stamp,
    )
    (case_dir / f"{failure_id}.json").write_text(json.dumps(record.to_json(), indent=2) + "\n", encoding="utf-8")
    return record
