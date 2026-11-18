"""Measure one accepted image. A failed check writes a MOD016 record and stops.

This module does not decide Real or Fake. Face availability is a gate, not a verdict.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Protocol

from PIL import Image, UnidentifiedImageError

from failure_handling import FailureRecord, write_failure

MODULE_ID = "MOD002"
FORMAT_BY_EXTENSION = {"jpg": "JPEG", "jpeg": "JPEG", "png": "PNG", "webp": "WEBP"}


class FaceCounter(Protocol):
    def count_faces(self, image: Image.Image) -> int: ...


@dataclass(frozen=True)
class ValidationConfig:
    allowed_channels: tuple[int, ...] = (1, 3, 4)
    max_noise_stddev: float = 80.0


@dataclass(frozen=True)
class ValidationResult:
    record: dict
    failure: FailureRecord | None

    @property
    def passed(self) -> bool:
        return self.record["status"] == "passed"


def _noise(image: Image.Image) -> float:
    gray = image.convert("L")
    reader = getattr(gray, "get_flattened_data", gray.getdata)
    pixels = list(reader())
    if not pixels:
        return 0.0
    mean = sum(pixels) / len(pixels)
    variance = sum((pixel - mean) ** 2 for pixel in pixels) / len(pixels)
    return math.sqrt(variance)


def _fail(storage_root: Path, case_id: str, input_id: str, name: str, detail: str, measured: dict) -> ValidationResult:
    failure = write_failure(
        storage_root,
        name=name,
        module_id=MODULE_ID,
        case_id=case_id,
        input_id=input_id,
        detail=detail,
    )
    record = {**measured, "status": "failed", "failure_id": failure.failure_id}
    return ValidationResult(record=record, failure=failure)


def validate_stored_input(
    input_dir: Path,
    face_counter: FaceCounter,
    *,
    storage_root: Path,
    config: ValidationConfig | None = None,
    now: datetime | None = None,
) -> ValidationResult:
    """Validate the image stored by MOD001. A rejected intake is not treated as an image."""

    settings = config or ValidationConfig()
    metadata = json.loads((input_dir / "input_metadata.json").read_text(encoding="utf-8"))
    case_id = metadata["case_id"]
    input_id = metadata["input_id"]
    base = {
        "input_id": input_id,
        "checked_timestamp": (now or datetime.now().astimezone()).replace(microsecond=0).isoformat(),
        "format": None,
        "corruption": False,
        "channels": None,
        "width": None,
        "height": None,
        "compression": None,
        "missing_data": False,
        "noise_stddev": None,
        "quality_note": None,
        "face_count": None,
        "face_availability": None,
    }
    if metadata["status"] != "accepted" or not metadata.get("stored_path"):
        result = _fail(storage_root, case_id, input_id, "unexpected_error", "intake was not accepted; validation did not read an image", base)
        _write(input_dir, result)
        return result
    path = Path(metadata["stored_path"])
    data = path.read_bytes()
    declared = metadata["declared_format"]
    try:
        with Image.open(BytesIO(data)) as probe:
            probe.verify()
        image = Image.open(BytesIO(data))
        image.load()
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError) as exc:
        base["corruption"] = True
        result = _fail(storage_root, case_id, input_id, "corrupted_image", f"image did not decode: {exc.__class__.__name__}", base)
        _write(input_dir, result)
        return result
    actual = image.format
    expected = FORMAT_BY_EXTENSION.get(declared)
    base.update(format=actual, compression=(actual or "").lower() or None, channels=len(image.getbands()), width=image.width, height=image.height)
    if actual is None or expected is None or actual != expected:
        result = _fail(
            storage_root,
            case_id,
            input_id,
            "unsupported_format",
            f"declared {declared}, decoded {actual}",
            base,
        )
        _write(input_dir, result)
        return result
    if image.width < 1 or image.height < 1:
        base["missing_data"] = True
        result = _fail(storage_root, case_id, input_id, "corrupted_image", "image has no pixels", base)
        _write(input_dir, result)
        return result
    limits = metadata.get("limits") or {}
    min_edge = int(limits.get("min_edge", 32))
    max_edge = int(limits.get("max_edge", 8192))
    if image.width < min_edge or image.height < min_edge or image.width > max_edge or image.height > max_edge:
        result = _fail(
            storage_root,
            case_id,
            input_id,
            "unexpected_error",
            f"resolution {image.width}x{image.height} outside {min_edge}-{max_edge}",
            base,
        )
        _write(input_dir, result)
        return result
    if base["channels"] not in settings.allowed_channels:
        result = _fail(storage_root, case_id, input_id, "unexpected_error", f"channels={base['channels']}", base)
        _write(input_dir, result)
        return result
    noise = _noise(image)
    base["noise_stddev"] = round(noise, 4)
    if noise == 0:
        base["missing_data"] = True
        base["quality_note"] = "blank"
        result = _fail(storage_root, case_id, input_id, "corrupted_image", "missing pixel variation", base)
        _write(input_dir, result)
        return result
    if noise > settings.max_noise_stddev:
        base["quality_note"] = "noisy"
        result = _fail(storage_root, case_id, input_id, "unexpected_error", f"noise_stddev={base['noise_stddev']}", base)
        _write(input_dir, result)
        return result
    face_count = int(face_counter.count_faces(image))
    base["face_count"] = face_count
    if face_count <= 0:
        base["face_availability"] = "none"
        base["quality_note"] = "ok"
        result = _fail(storage_root, case_id, input_id, "no_face", "face_count=0", base)
        _write(input_dir, result)
        return result
    if face_count > 1:
        base["face_availability"] = "multiple"
        base["quality_note"] = "ok"
        result = _fail(storage_root, case_id, input_id, "multiple_faces", f"face_count={face_count}", base)
        _write(input_dir, result)
        return result
    base["face_availability"] = "single"
    base["quality_note"] = "ok"
    record = {**base, "status": "passed", "failure_id": None}
    result = ValidationResult(record=record, failure=None)
    _write(input_dir, result)
    return result


def _write(input_dir: Path, result: ValidationResult) -> None:
    (input_dir / "validation.json").write_text(json.dumps(result.record, indent=2) + "\n", encoding="utf-8")
