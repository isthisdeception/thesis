"""PPMOD09 — Format / color-mode conversion."""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from PIL import Image

from .types import ImageRecord, ModuleError

MODULE_ID = "PPMOD09"


@dataclass
class FormatConversionParams:
    force_rgb: bool = True
    output_format: str = "PNG"
    jpeg_quality: int = 95
    png_compress_level: int = 3


def convert_format(record: ImageRecord, params: FormatConversionParams) -> ImageRecord:
    """Force color mode and record output format (save is caller's job)."""
    im = record.ensure_image()
    record.source_mode = im.mode

    fmt = params.output_format.upper()
    if fmt not in {"PNG", "JPEG", "JPG"}:
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="INVALID_PARAM",
            message=f"unsupported output_format={params.output_format!r}",
            path=record.relative_path,
        )
    if fmt == "JPG":
        fmt = "JPEG"

    if params.force_rgb and im.mode != "RGB":
        if im.mode in {"RGBA", "LA", "PA"}:
            bg = Image.new("RGB", im.size, (0, 0, 0))
            rgba = im.convert("RGBA")
            bg.paste(rgba, mask=rgba.split()[-1])
            im = bg
        else:
            im = im.convert("RGB")

    if fmt == "JPEG" and im.mode != "RGB":
        im = im.convert("RGB")

    record.image = im
    record.output_format = fmt
    record.extras["jpeg_quality"] = params.jpeg_quality
    record.extras["png_compress_level"] = params.png_compress_level
    record.sync_size_from_image()
    return record


def save_processed_image(
    record: ImageRecord,
    dest_path: Path,
    params: FormatConversionParams,
) -> Path:
    """Write processed image under ``processed/`` only (caller supplies dest)."""
    dest_path = Path(dest_path)
    if "raw" in dest_path.parts and "processed" not in dest_path.parts:
        # Guardrail: refuse writes that look like raw tier
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="RAW_WRITE_FORBIDDEN",
            message=f"refusing to write into raw-like path: {dest_path}",
            path=record.relative_path,
        )
    record = convert_format(record, params)
    im = record.ensure_image()
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    fmt = record.output_format or "PNG"
    save_kwargs: dict = {}
    if fmt == "JPEG":
        save_kwargs["quality"] = params.jpeg_quality
        save_kwargs["optimize"] = True
    elif fmt == "PNG":
        save_kwargs["compress_level"] = params.png_compress_level
    im.save(dest_path, format=fmt, **save_kwargs)
    return dest_path


def encode_bytes(record: ImageRecord, params: FormatConversionParams) -> bytes:
    record = convert_format(record, params)
    buf = BytesIO()
    fmt = record.output_format or "PNG"
    kwargs: dict = {}
    if fmt == "JPEG":
        kwargs["quality"] = params.jpeg_quality
    elif fmt == "PNG":
        kwargs["compress_level"] = params.png_compress_level
    record.ensure_image().save(buf, format=fmt, **kwargs)
    return buf.getvalue()
