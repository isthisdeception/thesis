"""PPMOD04 — Cropping (spatial crop only)."""

from __future__ import annotations

from dataclasses import dataclass

from .types import FaceBox, ImageRecord, ModuleError

MODULE_ID = "PPMOD04"


@dataclass
class CroppingParams:
    enabled: bool = False
    crop_margin: float = 0.25
    square_crop: bool = True


def _expand_box(
    box: FaceBox,
    margin: float,
    square: bool,
    img_w: int,
    img_h: int,
) -> tuple[int, int, int, int]:
    cx = (box.x1 + box.x2) / 2.0
    cy = (box.y1 + box.y2) / 2.0
    w = box.width * (1.0 + 2.0 * margin)
    h = box.height * (1.0 + 2.0 * margin)
    if square:
        side = max(w, h)
        w = h = side
    x1 = int(round(cx - w / 2.0))
    y1 = int(round(cy - h / 2.0))
    x2 = int(round(cx + w / 2.0))
    y2 = int(round(cy + h / 2.0))
    # Clip to image bounds without crashing
    x1 = max(0, min(img_w - 1, x1))
    y1 = max(0, min(img_h - 1, y1))
    x2 = max(x1 + 1, min(img_w, x2))
    y2 = max(y1 + 1, min(img_h, y2))
    if square:
        side = min(x2 - x1, y2 - y1)
        x2 = x1 + side
        y2 = y1 + side
    return x1, y1, x2, y2


def crop_face(record: ImageRecord, params: CroppingParams) -> ImageRecord:
    """Crop around face box / full frame. Disabled → passthrough."""
    if not params.enabled:
        return record

    im = record.ensure_image()
    if record.face_boxes and record.primary_face_index is not None:
        box = record.face_boxes[record.primary_face_index]
    elif record.face_boxes:
        box = record.face_boxes[0]
    else:
        box = FaceBox(0, 0, im.width, im.height, score=1.0)

    crop = _expand_box(box, params.crop_margin, params.square_crop, im.width, im.height)
    x1, y1, x2, y2 = crop
    if x2 <= x1 or y2 <= y1:
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="INVALID_CROP",
            message=f"degenerate crop box {crop}",
            path=record.relative_path,
        )
    record.image = im.crop(crop)
    record.crop_box = crop
    record.sync_size_from_image()
    return record
