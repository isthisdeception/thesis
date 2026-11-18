"""Mean absolute difference between horizontal neighbors."""

from __future__ import annotations

from evidence.item import CollectorContext, CollectorOutcome, luminance, make_item

EVIDENCE_TYPE = "texture_analysis"


class TextureAnalysisCollector:
    evidence_type = EVIDENCE_TYPE

    def collect(self, context: CollectorContext) -> CollectorOutcome:
        image = context.image
        if image.width < 2:
            return CollectorOutcome.failed("unexpected_error", "image is too narrow for a texture measurement")
        values = luminance(image)
        width = image.width
        diffs = []
        for y in range(image.height):
            row = y * width
            for x in range(1, width):
                diffs.append(abs(values[row + x] - values[row + x - 1]))
        if not diffs:
            return CollectorOutcome.failed("unexpected_error", "texture measurement had no pairs")
        score = sum(diffs) / len(diffs)
        raw = {"input_id": context.input_id, "case_id": context.case_id, "neighbor_contrast": score}
        item = make_item(
            evidence_type=self.evidence_type,
            description="mean absolute difference between horizontal neighbors",
            raw_output=raw,
            value=round(score, 4),
            unit="gray_level",
        )
        return CollectorOutcome.one(item)
