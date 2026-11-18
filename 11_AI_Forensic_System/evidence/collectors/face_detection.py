"""Count faces with the counter this collector was given. It does not import face_quality."""

from __future__ import annotations

from typing import Protocol

from PIL import Image

from evidence.item import CollectorContext, CollectorOutcome, make_item

EVIDENCE_TYPE = "face_detection"


class FaceCounter(Protocol):
    def count_faces(self, image: Image.Image) -> int: ...


class FaceDetectionCollector:
    evidence_type = EVIDENCE_TYPE

    def __init__(self, counter: FaceCounter) -> None:
        self._counter = counter

    def collect(self, context: CollectorContext) -> CollectorOutcome:
        try:
            count = int(self._counter.count_faces(context.image))
        except Exception as exc:
            return CollectorOutcome.failed("unexpected_error", f"face counter failed: {exc.__class__.__name__}")
        if count < 0:
            return CollectorOutcome.failed("unexpected_error", f"face count {count} is below zero")
        raw = {"input_id": context.input_id, "case_id": context.case_id, "face_count": count}
        item = make_item(
            evidence_type=self.evidence_type,
            description=f"face count is {count}",
            raw_output=raw,
            value=count,
            unit="count",
        )
        return CollectorOutcome.one(item)
