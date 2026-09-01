"""Unit tests — PPMOD09 format conversion."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from modules.format_conversion import FormatConversionParams, convert_format, save_processed_image
from modules.types import ImageRecord, ModuleError
from modules.validation import validate_format_conversion
import pytest


def test_rgba_to_rgb() -> None:
    rec = ImageRecord(relative_path="a.png", image=Image.new("RGBA", (16, 16), (1, 2, 3, 255)))
    out = convert_format(rec, FormatConversionParams(force_rgb=True, output_format="PNG"))
    assert out.image.mode == "RGB" and out.output_format == "PNG"
    validate_format_conversion(out)


def test_l_to_rgb() -> None:
    rec = ImageRecord(relative_path="a.png", image=Image.new("L", (16, 16), 128))
    out = convert_format(rec, FormatConversionParams())
    assert out.image.mode == "RGB"


def test_jpeg_format_param() -> None:
    rec = ImageRecord(relative_path="a.png", image=Image.new("RGB", (16, 16)))
    out = convert_format(rec, FormatConversionParams(output_format="JPEG"))
    assert out.output_format == "JPEG"
    validate_format_conversion(out)


def test_refuse_raw_write(tmp_path: Path) -> None:
    rec = ImageRecord(relative_path="a.png", image=Image.new("RGB", (8, 8)))
    rawish = tmp_path / "raw" / "DS0001" / "a.png"
    with pytest.raises(ModuleError) as ei:
        save_processed_image(rec, rawish, FormatConversionParams())
    assert ei.value.reason_code == "RAW_WRITE_FORBIDDEN"
