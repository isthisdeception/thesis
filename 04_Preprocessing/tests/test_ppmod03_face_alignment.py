"""Unit tests — PPMOD03 face alignment."""

from __future__ import annotations

from PIL import Image

from modules.face_alignment import FaceAlignmentParams, align_face
from modules.types import FaceBox, ImageRecord
from modules.validation import validate_face_alignment


def test_disabled_passthrough() -> None:
    im = Image.new("RGB", (64, 64), color=(1, 2, 3))
    rec = ImageRecord(relative_path="a.png", image=im.copy())
    out = align_face(rec, FaceAlignmentParams(enabled=False))
    assert out.image.size == (64, 64)
    validate_face_alignment(out, enabled=False, template=112)


def test_enabled_eyes_horizontal_size() -> None:
    im = Image.new("RGB", (200, 200), color=(40, 40, 40))
    rec = ImageRecord(
        relative_path="a.png",
        image=im,
        face_boxes=[FaceBox(50, 50, 150, 150, 1.0)],
        primary_face_index=0,
    )
    out = align_face(rec, FaceAlignmentParams(enabled=True, output_template_size=112))
    assert out.image.size == (112, 112)
    validate_face_alignment(out, enabled=True, template=112)


def test_five_point_with_landmarks_horizontalizes() -> None:
    im = Image.new("RGB", (200, 200), color=(80, 80, 80))
    rec = ImageRecord(
        relative_path="a.png",
        image=im,
        face_boxes=[FaceBox(40, 40, 160, 160, 1.0)],
        primary_face_index=0,
        extras={"landmarks": [(60, 80), (140, 100), (100, 120), (80, 150), (120, 150)]},
    )
    out = align_face(
        rec,
        FaceAlignmentParams(enabled=True, align_method="five_point", output_template_size=96),
    )
    assert out.image.size == (96, 96)
    validate_face_alignment(out, enabled=True, template=96)
