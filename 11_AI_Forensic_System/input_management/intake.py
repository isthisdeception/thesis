"""Receive one upload, assign an input id, and store metadata.

A rejected upload writes a MOD016 failure and does not store the image.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from failure_handling import FailureRecord, write_failure

MODULE_ID = "MOD001"


@dataclass(frozen=True)
class IntakeConfig:
    allowed_formats: tuple[str, ...] = ("jpg", "jpeg", "png", "webp")
    max_bytes: int = 20 * 1024 * 1024
    min_edge: int = 32
    max_edge: int = 8192


@dataclass(frozen=True)
class IntakeResult:
    metadata: dict
    failure: FailureRecord | None
    image_stored: bool

    @property
    def accepted(self) -> bool:
        return self.failure is None and self.metadata["status"] == "accepted"


def _suffix(filename: str) -> str:
    return Path(filename).suffix.lower().lstrip(".")


def _next_input_id(case_dir: Path, case_id: str) -> str:
    existing = [path.name for path in case_dir.glob(f"{case_id}-input-*") if path.is_dir()]
    return f"{case_id}-input-{len(existing) + 1:02d}"


def _reject(
    storage_root: Path,
    case_id: str,
    input_id: str,
    filename: str,
    data: bytes,
    declared: str,
    stamp: str,
    name: str,
    detail: str,
) -> IntakeResult:
    failure = write_failure(
        storage_root,
        name=name,
        module_id=MODULE_ID,
        case_id=case_id,
        input_id=input_id,
        detail=detail,
    )
    metadata = {
        "input_id": input_id,
        "case_id": case_id,
        "declared_filename": filename,
        "stored_path": None,
        "byte_size": len(data),
        "declared_format": declared,
        "received_timestamp": stamp,
        "status": "rejected",
        "failure_id": failure.failure_id,
    }
    input_dir = storage_root / case_id / input_id
    input_dir.mkdir(parents=True, exist_ok=True)
    (input_dir / "input_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return IntakeResult(metadata=metadata, failure=failure, image_stored=False)


def receive_upload(
    *,
    case_id: str,
    filename: str,
    data: bytes,
    storage_root: Path,
    config: IntakeConfig | None = None,
    now: datetime | None = None,
) -> IntakeResult:
    """Store one file for an existing case. A second call uses a new input id and does not overwrite."""

    settings = config or IntakeConfig()
    stamp = (now or datetime.now().astimezone()).replace(microsecond=0).isoformat()
    case_dir = storage_root / case_id
    case_dir.mkdir(parents=True, exist_ok=True)
    input_id = _next_input_id(case_dir, case_id)
    declared = _suffix(filename)
    if not data:
        return _reject(storage_root, case_id, input_id, filename, data, declared, stamp, "unexpected_error", "empty file, byte_size=0")
    if declared not in settings.allowed_formats:
        return _reject(
            storage_root,
            case_id,
            input_id,
            filename,
            data,
            declared,
            stamp,
            "unsupported_format",
            f"extension {declared or '(none)'} is not in {', '.join(settings.allowed_formats)}",
        )
    if len(data) > settings.max_bytes:
        return _reject(
            storage_root,
            case_id,
            input_id,
            filename,
            data,
            declared,
            stamp,
            "unexpected_error",
            f"byte_size={len(data)} exceeds max_bytes={settings.max_bytes}",
        )
    input_dir = storage_root / case_id / input_id
    input_dir.mkdir(parents=True)
    stored = input_dir / f"original.{declared}"
    if stored.exists():
        raise FileExistsError(stored)
    stored.write_bytes(data)
    metadata = {
        "input_id": input_id,
        "case_id": case_id,
        "declared_filename": filename,
        "stored_path": str(stored),
        "byte_size": len(data),
        "declared_format": declared,
        "received_timestamp": stamp,
        "status": "accepted",
        "failure_id": None,
        "limits": {"min_edge": settings.min_edge, "max_edge": settings.max_edge, "max_bytes": settings.max_bytes},
    }
    (input_dir / "input_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return IntakeResult(metadata=metadata, failure=None, image_stored=True)
