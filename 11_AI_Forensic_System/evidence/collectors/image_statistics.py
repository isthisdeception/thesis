"""Width, height, channels, and simple luminance statistics. No other collector is consulted."""

from __future__ import annotations

from evidence.item import CollectorContext, CollectorOutcome, luminance, make_item

EVIDENCE_TYPE = "image_statistics"


class ImageStatisticsCollector:
    evidence_type = EVIDENCE_TYPE

    def collect(self, context: CollectorContext) -> CollectorOutcome:
        values = luminance(context.image)
        if not values:
            return CollectorOutcome.failed("unexpected_error", "image has no pixels")
        mean = sum(values) / len(values)
        variance = sum((value - mean) ** 2 for value in values) / len(values)
        raw = {
            "input_id": context.input_id,
            "case_id": context.case_id,
            "width": context.image.width,
            "height": context.image.height,
            "channels": len(context.image.getbands()),
            "luminance_mean": mean,
            "luminance_variance": variance,
        }
        item = make_item(
            evidence_type=self.evidence_type,
            description=f"image is {raw['width']} by {raw['height']} with {raw['channels']} channels",
            raw_output=raw,
            value={"width": raw["width"], "height": raw["height"], "channels": raw["channels"], "luminance_mean": round(mean, 4)},
            unit="pixel",
        )
        return CollectorOutcome.one(item)
