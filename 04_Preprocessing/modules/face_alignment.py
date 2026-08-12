"""PPMOD03 — Face alignment (geometric transform only)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from PIL import Image

from .types import FaceBox, ImageRecord, ModuleError

MODULE_ID = "PPMOD03"


@dataclass
class FaceAlignmentParams:
    enabled: bool = False
    align_method: str = "eyes_horizontal"
    output_template_size: int = 112


def _identity_matrix() -> list[list[float]]:
    return [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]


def _primary_box(record: ImageRecord) -> FaceBox:
    if record.face_boxes and record.primary_face_index is not None:
        return record.face_boxes[record.primary_face_index]
    if record.face_boxes:
        return record.face_boxes[0]
    im = record.ensure_image()
    return FaceBox(0, 0, im.width, im.height, score=1.0)


def _align_eyes_horizontal(record: ImageRecord, params: FaceAlignmentParams) -> ImageRecord:
    """Approximate alignment: crop face box and resize to template (no landmarks)."""
    im = record.ensure_image()
    box = _primary_box(record).clip(im.width, im.height)
    if box.width < 1 or box.height < 1:
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="INVALID_BOX",
            message="face box has zero area",
            path=record.relative_path,
        )
    cropped = im.crop((int(box.x1), int(box.y1), int(box.x2), int(box.y2)))
    size = int(params.output_template_size)
    aligned = cropped.resize((size, size), Image.Resampling.BILINEAR)
    # Translation+scale affine approximating the crop→template map
    sx = size / box.width
    sy = size / box.height
    matrix = [[sx, 0.0, -box.x1 * sx], [0.0, sy, -box.y1 * sy]]
    record.image = aligned
    record.affine_matrix = matrix
    record.sync_size_from_image()
    return record


def _align_five_point(record: ImageRecord, params: FaceAlignmentParams) -> ImageRecord:
    """Five-point path: requires landmarks in ``record.extras['landmarks']``.

    Landmarks must be five (x,y) pairs: left_eye, right_eye, nose, mouth_left, mouth_right.
    """
    landmarks = record.extras.get("landmarks")
    if not landmarks or len(landmarks) < 2:
        # Fall back to eyes_horizontal when landmarks absent
        return _align_eyes_horizontal(record, params)

    left_eye = np.array(landmarks[0], dtype=float)
    right_eye = np.array(landmarks[1], dtype=float)
    dy = right_eye[1] - left_eye[1]
    dx = right_eye[0] - left_eye[0]
    angle = float(np.degrees(np.arctan2(dy, dx)))
    im = record.ensure_image()
    center = ((left_eye[0] + right_eye[0]) / 2.0, (left_eye[1] + right_eye[1]) / 2.0)
    rotated = im.rotate(angle, resample=Image.Resampling.BILINEAR, center=center)
    # After rotation, re-crop primary box and resize
    tmp = ImageRecord(
        relative_path=record.relative_path,
        dataset_id=record.dataset_id,
        image=rotated,
        face_boxes=record.face_boxes,
        primary_face_index=record.primary_face_index,
        extras=record.extras,
    )
    out = _align_eyes_horizontal(tmp, params)
    record.image = out.image
    record.affine_matrix = out.affine_matrix
    record.sync_size_from_image()
    return record


def align_face(record: ImageRecord, params: FaceAlignmentParams) -> ImageRecord:
    """Align face geometrically. Disabled path returns input unchanged."""
    if not params.enabled:
        record.affine_matrix = _identity_matrix()
        return record

    method = params.align_method.lower()
    if method == "eyes_horizontal":
        return _align_eyes_horizontal(record, params)
    if method == "five_point":
        return _align_five_point(record, params)
    raise ModuleError(
        module_id=MODULE_ID,
        reason_code="INVALID_PARAM",
        message=f"unknown align_method={params.align_method!r}",
        path=record.relative_path,
    )


def matrix_is_finite(matrix: list[list[float]] | None) -> bool:
    if matrix is None:
        return False
    arr = np.asarray(matrix, dtype=float)
    return bool(np.isfinite(arr).all())
