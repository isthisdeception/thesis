"""PPMOD01 — Image verification (read-only intake check)."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

from .types import ImageRecord, ModuleError

MODULE_ID = "PPMOD01"

DEFAULT_ALLOWED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

REASON_OK = "OK"
REASON_UNSUPPORTED = "UNSUPPORTED_FORMAT"
REASON_MACOS_JUNK = "MACOS_JUNK"
REASON_EMPTY = "EMPTY_FILE"
REASON_UNREADABLE = "UNREADABLE"

REASON_CODES = frozenset(
    {REASON_OK, REASON_UNSUPPORTED, REASON_MACOS_JUNK, REASON_EMPTY, REASON_UNREADABLE}
)


@dataclass
class ImageVerificationParams:
    allowed_extensions: list[str] = field(
        default_factory=lambda: list(DEFAULT_ALLOWED_EXTENSIONS)
    )
    reject_macos_junk: bool = True
    reject_zero_byte: bool = True
    open_verify: bool = True
    hash_algorithm: str = "sha256"


def _norm(path: str) -> str:
    return path.replace("\\", "/")


def is_macos_junk(relative_path: str) -> bool:
    """Detect AppleDouble / __MACOSX junk paths."""
    p = _norm(relative_path)
    name = Path(p).name
    if name.startswith("._") or name in {".DS_Store", "Thumbs.db"}:
        return True
    low = f"/{p.lower()}/"
    if "/__macosx/" in low or p.lower().startswith("__macosx/"):
        return True
    return False


def verify_path(
    path: Path,
    relative_path: str,
    params: ImageVerificationParams,
    *,
    dataset_id: str = "",
) -> ImageRecord:
    """Verify a filesystem path is a readable image under policy.

    Does not modify the file. On soft reject, returns ``kept=False`` with a
    reason code. Hard I/O surprises raise ``ModuleError``.
    """
    rel = _norm(relative_path)
    record = ImageRecord(relative_path=rel, dataset_id=dataset_id, source_path=path)

    if params.reject_macos_junk and is_macos_junk(rel):
        record.kept = False
        record.reason_code = REASON_MACOS_JUNK
        return record

    suffix = Path(rel).suffix.lower()
    allowed = {e.lower() if e.startswith(".") else f".{e.lower()}" for e in params.allowed_extensions}
    if suffix not in allowed:
        record.kept = False
        record.reason_code = REASON_UNSUPPORTED
        return record

    if not path.is_file():
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code=REASON_UNREADABLE,
            message=f"path is not a file: {path}",
            path=rel,
        )

    size = path.stat().st_size
    if params.reject_zero_byte and size == 0:
        record.kept = False
        record.reason_code = REASON_EMPTY
        return record

    data = path.read_bytes()
    if params.reject_zero_byte and not data:
        record.kept = False
        record.reason_code = REASON_EMPTY
        return record

    if params.hash_algorithm:
        try:
            h = hashlib.new(params.hash_algorithm)
        except ValueError as exc:
            raise ModuleError(
                module_id=MODULE_ID,
                reason_code="INVALID_PARAM",
                message=f"unsupported hash_algorithm={params.hash_algorithm!r}",
                path=rel,
            ) from exc
        h.update(data)
        record.content_hash = h.hexdigest()

    if params.open_verify:
        try:
            from io import BytesIO

            with Image.open(BytesIO(data)) as im:
                im.verify()
            with Image.open(BytesIO(data)) as im:
                im.load()
                record.image = im.copy()
                record.source_mode = im.mode
                record.original_size = (im.width, im.height)
                record.current_size = (im.width, im.height)
        except Exception as exc:  # Pillow raises many types for corrupt files
            record.kept = False
            record.reason_code = REASON_UNREADABLE
            record.extras["verify_error"] = str(exc)
            return record

    record.kept = True
    record.reason_code = REASON_OK
    return record


def verify_image_bytes(
    data: bytes,
    relative_path: str,
    params: ImageVerificationParams,
    *,
    dataset_id: str = "",
) -> ImageRecord:
    """Verify in-memory bytes (e.g. zip member) without writing to disk."""
    rel = _norm(relative_path)
    record = ImageRecord(relative_path=rel, dataset_id=dataset_id)

    if params.reject_macos_junk and is_macos_junk(rel):
        record.kept = False
        record.reason_code = REASON_MACOS_JUNK
        return record

    suffix = Path(rel).suffix.lower()
    allowed = {e.lower() if e.startswith(".") else f".{e.lower()}" for e in params.allowed_extensions}
    if suffix not in allowed:
        record.kept = False
        record.reason_code = REASON_UNSUPPORTED
        return record

    if params.reject_zero_byte and not data:
        record.kept = False
        record.reason_code = REASON_EMPTY
        return record

    if params.hash_algorithm:
        h = hashlib.new(params.hash_algorithm)
        h.update(data)
        record.content_hash = h.hexdigest()

    if params.open_verify:
        try:
            from io import BytesIO

            with Image.open(BytesIO(data)) as im:
                im.verify()
            with Image.open(BytesIO(data)) as im:
                im.load()
                record.image = im.copy()
                record.source_mode = im.mode
                record.original_size = (im.width, im.height)
                record.current_size = (im.width, im.height)
        except Exception as exc:
            record.kept = False
            record.reason_code = REASON_UNREADABLE
            record.extras["verify_error"] = str(exc)
            return record

    record.kept = True
    record.reason_code = REASON_OK
    return record
