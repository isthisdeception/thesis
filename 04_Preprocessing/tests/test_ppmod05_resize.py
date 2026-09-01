"""Unit tests — PPMOD05 resize."""

from __future__ import annotations

from PIL import Image

from modules.resize import ResizeParams, resize_image
from modules.types import ImageRecord
from modules.validation import validate_resize


def test_stretch_256_to_224() -> None:
    rec = ImageRecord(relative_path="a.png", image=Image.new("RGB", (256, 256)))
    out = resize_image(rec, ResizeParams(target_size=224, keep_aspect=False))
    assert out.image.size == (224, 224)
    validate_resize(out, 224, 224)


def test_letterbox_preserves_aspect() -> None:
    rec = ImageRecord(relative_path="a.png", image=Image.new("RGB", (100, 50), color=(255, 0, 0)))
    out = resize_image(
        rec,
        ResizeParams(target_size=100, keep_aspect=True, pad_value=0),
    )
    assert out.image.size == (100, 100)
    # Inner content should be 100x50 centered → letterbox_inner
    assert out.extras["letterbox_inner"] == (100, 50)
    validate_resize(out, 100, 100)
