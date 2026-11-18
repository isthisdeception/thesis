"""Structured failure reports (MOD016). Callers stop or continue as their specs say; this module never decides a case."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

MODULE_ID = "MOD016"
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
DEFAULT_WARNING_NAMES = ("low_confidence",)


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
    """Append one failure file. An unknown name is stored as unexpected_error with reported_name preserved in detail."""

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


def read_case_failures(storage_root: Path, case_id: str) -> list[FailureRecord]:
    """Read back all structured failure records stored for `case_id` in chronological/id order."""

    case_dir = storage_root / case_id / "failures"
    if not case_dir.is_dir():
        return []
    records: list[FailureRecord] = []
    for path in sorted(case_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        records.append(
            FailureRecord(
                failure_id=str(payload["failure_id"]),
                name=str(payload["name"]),
                reported_name=str(payload.get("reported_name", payload["name"])),
                module_id=str(payload["module_id"]),
                case_id=str(payload["case_id"]),
                input_id=payload.get("input_id"),
                detail=str(payload["detail"]),
                timestamp=str(payload["timestamp"]),
            )
        )
    return records


def classify_failures(
    records: list[FailureRecord],
    *,
    warning_names: tuple[str, ...] = DEFAULT_WARNING_NAMES,
) -> tuple[list[str], list[str]]:
    """Partition failure records into `(error_ids, warning_ids)` for the case audit row."""

    errors: list[str] = []
    warnings: list[str] = []
    for rec in records:
        fid = rec.failure_id or rec.name
        if rec.name in warning_names:
            if fid not in warnings:
                warnings.append(fid)
        else:
            if fid not in errors:
                errors.append(fid)
    return errors, warnings
