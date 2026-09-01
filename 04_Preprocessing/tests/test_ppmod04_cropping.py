"""Unit tests — PPMOD04 cropping."""

from __future__ import annotations

from PIL import Image

from modules.cropping import CroppingParams, crop_face
from modules.types import FaceBox, ImageRecord
from modules.validation import validate_cropping


def test_disabled_passthrough() -> None:
    im = Image.new("RGB", (100, 80))
    rec = ImageRecord(relative_path="a.png", image=im, original_size=(100, 80))
    out = crop_face(rec, CroppingParams(enabled=False))
    assert out.image.size == (100, 80)


def test_square_crop_forces_equal_sides() -> None:
    im = Image.new("RGB", (200, 200), color=(5, 5, 5))
    rec = ImageRecord(
        relative_path="a.png",
        image=im,
        original_size=(200, 200),
        face_boxes=[FaceBox(20, 40, 80, 160, 1.0)],  # 60x120
        primary_face_index=0,
    )
    out = crop_face(rec, CroppingParams(enabled=True, crop_margin=0.0, square_crop=True))
    assert out.image.width == out.image.height
    validate_cropping(out, enabled=True)


def test_margin_clips_without_crash() -> None:
    im = Image.new("RGB", (50, 50))
    rec = ImageRecord(
        relative_path="a.png",
        image=im,
        original_size=(50, 50),
        face_boxes=[FaceBox(0, 0, 40, 40, 1.0)],
        primary_face_index=0,
    )
    out = crop_face(rec, CroppingParams(enabled=True, crop_margin=0.5, square_crop=True))
    assert out.image.width > 0 and out.image.height > 0
    validate_cropping(out, enabled=True)
