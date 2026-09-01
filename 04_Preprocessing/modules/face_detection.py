"""PPMOD02 — Face detection (boxes + scores only)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .types import FULL_FRAME, FaceBox, ImageRecord, ModuleError

MODULE_ID = "PPMOD02"


@dataclass
class FaceDetectionParams:
    enabled: bool = False
    assume_single_face_crop: bool = True
    detector_name: str = "stub"
    min_face_confidence: float = 0.9
    max_faces_keep: int = 1
    fail_if_no_face: bool = True


DetectorFn = Callable[[ImageRecord, FaceDetectionParams], list[FaceBox]]


def _stub_detector(record: ImageRecord, params: FaceDetectionParams) -> list[FaceBox]:
    """Deterministic stub: box covering central 60% of the frame (for unit tests)."""
    im = record.ensure_image()
    w, h = im.width, im.height
    mx, my = 0.2 * w, 0.2 * h
    return [FaceBox(mx, my, w - mx, h - my, score=1.0)]


def _opencv_haar_detector(record: ImageRecord, params: FaceDetectionParams) -> list[FaceBox]:
    try:
        import cv2  # type: ignore
        import numpy as np
    except ImportError as exc:
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="MISSING_DEPENDENCY",
            message="opencv-python required for detector_name=opencv_haar",
            path=record.relative_path,
        ) from exc

    im = record.ensure_image().convert("RGB")
    arr = np.array(im)[:, :, ::-1]  # RGB -> BGR
    gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    boxes: list[FaceBox] = []
    for x, y, fw, fh in faces:
        boxes.append(FaceBox(float(x), float(y), float(x + fw), float(y + fh), score=1.0))
    return boxes


_DETECTORS: dict[str, DetectorFn] = {
    "stub": _stub_detector,
    "opencv_haar": _opencv_haar_detector,
}


def detect_faces(record: ImageRecord, params: FaceDetectionParams) -> ImageRecord:
    """Attach face boxes to ``record``. Never writes files."""
    if not params.enabled:
        if params.assume_single_face_crop:
            record.face_sentinel = FULL_FRAME
            record.face_boxes = []
            record.primary_face_index = None
            return record
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="DISABLED_WITHOUT_ASSUME",
            message="enabled=false requires assume_single_face_crop=true for passthrough",
            path=record.relative_path,
        )

    name = params.detector_name.lower()
    if name in {"retinaface", "mtcnn"}:
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="DETECTOR_NOT_PINNED",
            message=(
                f"detector_name={params.detector_name!r} requires environment pin "
                "(STEP-030); use stub or opencv_haar until then"
            ),
            path=record.relative_path,
        )

    detector = _DETECTORS.get(name)
    if detector is None:
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="INVALID_PARAM",
            message=f"unknown detector_name={params.detector_name!r}",
            path=record.relative_path,
        )

    boxes = detector(record, params)
    im = record.ensure_image()
    filtered = [
        b.clip(im.width, im.height)
        for b in boxes
        if b.score >= params.min_face_confidence and b.width > 0 and b.height > 0
    ]
    filtered.sort(key=lambda b: (b.score, b.width * b.height), reverse=True)
    filtered = filtered[: max(1, params.max_faces_keep)]

    if not filtered:
        if params.fail_if_no_face:
            raise ModuleError(
                module_id=MODULE_ID,
                reason_code="NO_FACE",
                message="no face detected above confidence threshold",
                path=record.relative_path,
            )
        record.face_boxes = []
        record.primary_face_index = None
        record.face_sentinel = None
        return record

    record.face_boxes = filtered
    record.primary_face_index = 0
    record.face_sentinel = None
    return record


def box_within_bounds(box: FaceBox, width: int, height: int, tol: float = 1.0) -> bool:
    return (
        -tol <= box.x1 <= width + tol
        and -tol <= box.y1 <= height + tol
        and -tol <= box.x2 <= width + tol
        and -tol <= box.y2 <= height + tol
        and 0.0 <= box.score <= 1.0
    )
