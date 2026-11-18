"""Block-boundary contrast minus interior contrast, on an 8-pixel grid."""

from __future__ import annotations

from evidence.item import CollectorContext, CollectorOutcome, luminance, make_item

EVIDENCE_TYPE = "compression_artifacts"


class CompressionArtifactCollector:
    evidence_type = EVIDENCE_TYPE

    def collect(self, context: CollectorContext) -> CollectorOutcome:
        image = context.image
        if image.width < 16 or image.height < 16:
            return CollectorOutcome.failed("unexpected_error", "image is smaller than two compression blocks")
        values = luminance(image)
        width = image.width
        boundary: list[int] = []
        interior: list[int] = []
        for y in range(image.height):
            row = y * width
            for x in range(1, width):
                diff = abs(values[row + x] - values[row + x - 1])
                if x % 8 == 0:
                    boundary.append(diff)
                else:
                    interior.append(diff)
        if not boundary or not interior:
            return CollectorOutcome.failed("unexpected_error", "compression grid could not be measured")
        boundary_mean = sum(boundary) / len(boundary)
        interior_mean = sum(interior) / len(interior)
        score = boundary_mean - interior_mean
        raw = {
            "input_id": context.input_id,
            "case_id": context.case_id,
            "pil_format": image.format,
            "boundary_mean": boundary_mean,
            "interior_mean": interior_mean,
            "blockiness": score,
        }
        item = make_item(
            evidence_type=self.evidence_type,
            description="difference between 8-pixel boundary contrast and interior contrast",
            raw_output=raw,
            value=round(score, 4),
            unit="gray_level",
        )
        return CollectorOutcome.one(item)
