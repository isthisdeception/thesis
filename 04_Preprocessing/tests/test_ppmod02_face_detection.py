"""Unit tests — PPMOD02 face detection."""

from __future__ import annotations

import pytest
from PIL import Image

from modules.face_detection import FaceDetectionParams, detect_faces
from modules.types import FULL_FRAME, ImageRecord, ModuleError
from modules.validation import validate_face_detection


def _rec(size: int = 100) -> ImageRecord:
    return ImageRecord(
        relative_path="face.png",
        dataset_id="DS0001",
        image=Image.new("RGB", (size, size), color=(128, 128, 128)),
    )


def test_assume_single_face_crop_short_circuit() -> None:
    params = FaceDetectionParams(enabled=False, assume_single_face_crop=True)
    out = detect_faces(_rec(), params)
    assert out.face_sentinel == FULL_FRAME
    assert out.face_boxes == []
    validate_face_detection(out, 100, 100)


def test_stub_detector_iou() -> None:
    params = FaceDetectionParams(
        enabled=True,
        assume_single_face_crop=False,
        detector_name="stub",
        min_face_confidence=0.5,
    )
    out = detect_faces(_rec(100), params)
    assert out.face_boxes
    box = out.face_boxes[0]
    # Expected stub box is central 60%: (20,20)-(80,80)
    assert abs(box.x1 - 20) < 1 and abs(box.y2 - 80) < 1
    validate_face_detection(out, 100, 100)


def test_disabled_without_assume_raises() -> None:
    with pytest.raises(ModuleError) as ei:
        detect_faces(_rec(), FaceDetectionParams(enabled=False, assume_single_face_crop=False))
    assert ei.value.reason_code == "DISABLED_WITHOUT_ASSUME"
