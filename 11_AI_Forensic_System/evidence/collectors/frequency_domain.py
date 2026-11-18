"""Ratio of adjacent-pixel change to luminance level. No other collector is consulted."""

from __future__ import annotations

from evidence.item import CollectorContext, CollectorOutcome, luminance, make_item

EVIDENCE_TYPE = "frequency_domain"


class FrequencyDomainCollector:
    evidence_type = EVIDENCE_TYPE

    def collect(self, context: CollectorContext) -> CollectorOutcome:
        values = luminance(context.image)
        if len(values) < 2:
            return CollectorOutcome.failed("unexpected_error", "not enough pixels for a frequency measurement")
        change = sum(abs(values[index] - values[index - 1]) for index in range(1, len(values))) / (len(values) - 1)
        level = sum(values) / len(values)
        raw = {"input_id": context.input_id, "case_id": context.case_id, "adjacent_change": change, "luminance_mean": level}
        item = make_item(
            evidence_type=self.evidence_type,
            description="mean absolute change between adjacent luminance pixels",
            raw_output=raw,
            value=round(change, 4),
            unit="gray_level",
        )
        return CollectorOutcome.one(item)
