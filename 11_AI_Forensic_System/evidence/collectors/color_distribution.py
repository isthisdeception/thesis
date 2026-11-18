"""Mean of each channel that the image actually has."""

from __future__ import annotations

from evidence.item import CollectorContext, CollectorOutcome, make_item

EVIDENCE_TYPE = "color_distribution"


def _mean(band) -> float:
    reader = getattr(band, "get_flattened_data", band.getdata)
    values = [int(pixel) for pixel in reader()]
    if not values:
        return 0.0
    return sum(values) / len(values)


class ColorDistributionCollector:
    evidence_type = EVIDENCE_TYPE

    def collect(self, context: CollectorContext) -> CollectorOutcome:
        bands = context.image.getbands()
        if not bands:
            return CollectorOutcome.failed("unexpected_error", "image has no color channels")
        means = {band: round(_mean(channel), 4) for band, channel in zip(bands, context.image.split())}
        raw = {"input_id": context.input_id, "case_id": context.case_id, "channel_means": means}
        item = make_item(
            evidence_type=self.evidence_type,
            description="mean value of each image channel",
            raw_output=raw,
            value=means,
            unit="gray_level",
        )
        return CollectorOutcome.one(item)
