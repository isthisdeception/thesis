"""Sharpness of a center crop. This collector does not call face detection."""

from __future__ import annotations

from evidence.item import CollectorContext, CollectorOutcome, luminance, make_item

EVIDENCE_TYPE = "face_quality"


def _center(image):
    width, height = image.size
    left, top = int(width * 0.2), int(height * 0.2)
    right, bottom = int(width * 0.8), int(height * 0.8)
    if right - left < 2 or bottom - top < 2:
        return None
    return image.crop((left, top, right, bottom))


class FaceQualityCollector:
    evidence_type = EVIDENCE_TYPE

    def collect(self, context: CollectorContext) -> CollectorOutcome:
        crop = _center(context.image)
        if crop is None:
            return CollectorOutcome.failed("unexpected_error", "center region is too small to measure")
        values = luminance(crop)
        if len(values) < 2:
            return CollectorOutcome.failed("unexpected_error", "center region has no pixel variation to measure")
        diffs = [abs(values[index] - values[index - 1]) for index in range(1, len(values))]
        sharpness = sum(diffs) / len(diffs)
        raw = {
            "input_id": context.input_id,
            "case_id": context.case_id,
            "region": "center_60_percent",
            "sharpness": sharpness,
            "used_face_box": False,
        }
        item = make_item(
            evidence_type=self.evidence_type,
            description="center-region sharpness measured without a face box",
            raw_output=raw,
            value=round(sharpness, 4),
            unit="gray_level",
        )
        return CollectorOutcome.one(item)
