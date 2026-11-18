"""Record that a map method produced no data. This collector does not draw a map."""

from __future__ import annotations

from evidence.item import CollectorContext, CollectorOutcome, make_item

EVIDENCE_TYPE = "explainability_input"


class ExplainabilityInputCollector:
    evidence_type = EVIDENCE_TYPE

    def __init__(self, method: str = "grad_cam") -> None:
        self.method = method

    def collect(self, context: CollectorContext) -> CollectorOutcome:
        if not self.method:
            return CollectorOutcome.failed("unexpected_error", "explainability method name is empty")
        raw = {
            "input_id": context.input_id,
            "case_id": context.case_id,
            "method": self.method,
            "map": None,
        }
        item = make_item(
            evidence_type=self.evidence_type,
            description=f"{self.method} produced no map",
            raw_output=raw,
            value="no_data",
            unit="",
            extra_processed={"model_id": None},
        )
        return CollectorOutcome.one(item)
