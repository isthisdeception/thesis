"""Rule-based fusion (DEF-004 baseline). The rule table is configuration, not code.

Each validated item is weighted by its MOD006 reliability. Items with a directional rule
(today only the detector probability against its recorded threshold) add weight to the
positive-class or negative-class side. Every other evidence type, including types added
later, is kept as context and cited. Unusable or failed items are listed as unresolved,
never silently dropped. The output is a lean, not a case decision.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from fusion.interface import FusionOutput, Unresolved, ValidatedEvidence

STRATEGY_ID = "rule_based"
VERSION = "0.1.0"

LEAN_POSITIVE = "positive_class"
LEAN_NEGATIVE = "negative_class"
LEAN_CONTESTED = "contested"
LEAN_NONE = "no_directional_evidence"


@dataclass(frozen=True)
class DirectionalRule:
    rule: str = "probability_vs_threshold"
    value_field: str = "value"
    threshold_field: str = "threshold"
    positive_class_raw_field: str = "positive_class"


@dataclass(frozen=True)
class RuleTable:
    table_version: str = "0.1.0"
    table_status: str = "approved in DEC0009 (Human, 2026-11-18)"
    reliability_weights: dict = field(default_factory=lambda: {"high": 1.0, "medium": 0.6, "low": 0.3})
    directional_rules: dict = field(default_factory=lambda: {"deep_learning_prediction": DirectionalRule()})
    contested_balance_below: float = 0.5

    @classmethod
    def from_json(cls, payload: dict) -> RuleTable:
        rules = {name: DirectionalRule(**spec) for name, spec in payload.get("directional_rules", {}).items()}
        weights = {str(k): float(v) for k, v in payload.get("reliability_weights", {}).items()}
        if "unusable" in weights:
            raise ValueError("unusable evidence is never weighted")
        for rule in rules.values():
            if rule.rule != "probability_vs_threshold":
                raise ValueError(f"rule {rule.rule} is not implemented")
        return cls(
            table_version=str(payload.get("table_version", "")),
            table_status=str(payload.get("table_status", "")),
            reliability_weights=weights,
            directional_rules=rules,
            contested_balance_below=float(payload.get("contested_balance_below", 0.5)),
        )


def _number(value) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


class RuleBasedStrategy:
    strategy_id = STRATEGY_ID
    version = VERSION

    def __init__(self, table: RuleTable | None = None) -> None:
        self.table = table or RuleTable()

    def fuse(self, evidence: Sequence[ValidatedEvidence]) -> FusionOutput:
        table = self.table
        last_for_collector = {item.collector_evidence_id: item.evidence_id for item in evidence}
        supporting: list[str] = []
        unresolved: list[Unresolved] = []
        directional: list[dict] = []
        context: list[dict] = []
        rationale: list[str] = []
        reference_class: str | None = None

        for item in evidence:
            later = last_for_collector.get(item.collector_evidence_id)
            if later != item.evidence_id:
                unresolved.append(Unresolved(item.evidence_id, f"superseded_by:{later}"))
                continue
            if item.status == "failed" or item.quality == "unusable":
                unresolved.append(Unresolved(item.evidence_id, f"unusable:{item.validation_reason}"))
                rationale.append(f"{item.evidence_id} ({item.evidence_type}) is unusable ({item.validation_reason}) and carries no weight.")
                continue
            weight = table.reliability_weights.get(item.quality)
            if weight is None:
                unresolved.append(Unresolved(item.evidence_id, f"quality_not_weighted:{item.quality}"))
                continue
            rule = table.directional_rules.get(item.evidence_type)
            if rule is None:
                supporting.append(item.evidence_id)
                context.append({"evidence_id": item.evidence_id, "evidence_type": item.evidence_type, "quality": item.quality})
                continue
            value = _number(item.processed_output.get(rule.value_field))
            threshold = _number(item.processed_output.get(rule.threshold_field))
            if value is None or not 0.0 <= value <= 1.0:
                unresolved.append(Unresolved(item.evidence_id, "value_not_a_probability"))
                continue
            if threshold is None:
                unresolved.append(Unresolved(item.evidence_id, "no_threshold_recorded"))
                continue
            item_class = str(item.raw_output.get(rule.positive_class_raw_field) or "").lower() or None
            if reference_class is None:
                reference_class = item_class
            elif item_class != reference_class:
                unresolved.append(Unresolved(item.evidence_id, f"positive_class_mismatch:{item_class}"))
                continue
            side = LEAN_POSITIVE if value >= threshold else LEAN_NEGATIVE
            directional.append({
                "evidence_id": item.evidence_id,
                "evidence_type": item.evidence_type,
                "model_id": item.processed_output.get("model_id"),
                "quality": item.quality,
                "weight": weight,
                "value": value,
                "threshold": threshold,
                "margin": round(value - threshold, 6),
                "side": side,
            })
            supporting.append(item.evidence_id)
            rationale.append(
                f"{item.evidence_id} ({item.evidence_type}, quality {item.quality}, weight {weight}) records "
                f"{value:.4f} against threshold {threshold:.4f}: {side} side."
            )

        positive = sum(entry["weight"] for entry in directional if entry["side"] == LEAN_POSITIVE)
        negative = sum(entry["weight"] for entry in directional if entry["side"] == LEAN_NEGATIVE)
        total = positive + negative
        balance = None if total == 0 else round((positive - negative) / total, 6)
        positive_ids = [entry["evidence_id"] for entry in directional if entry["side"] == LEAN_POSITIVE]
        negative_ids = [entry["evidence_id"] for entry in directional if entry["side"] == LEAN_NEGATIVE]

        if not directional:
            lean = LEAN_NONE
            rationale.append("No usable directional evidence; the lean is not estimated.")
        elif positive_ids and negative_ids and (balance == 0 or abs(balance) < table.contested_balance_below):
            lean = LEAN_CONTESTED
            rationale.append(
                f"Directional evidence disagrees ({', '.join(positive_ids)} vs {', '.join(negative_ids)}); "
                f"balance {balance} is inside the contested band {table.contested_balance_below}."
            )
        else:
            lean = LEAN_POSITIVE if balance > 0 else LEAN_NEGATIVE
            rationale.append(f"Weighted balance {balance} leans {lean}.")

        flagged = [
            {"evidence_id": item.evidence_id, "collector_evidence_id": item.collector_evidence_id, "partners": list(item.conflict_partners)}
            for item in evidence
            if "conflicting_evidence" in item.validation_reason
        ]
        for entry in flagged:
            rationale.append(f"{entry['evidence_id']} was flagged by validation as conflicting with {', '.join(entry['partners']) or 'another item'}.")
        if len(directional) == 1:
            rationale.append(f"Only one directional source ({directional[0]['evidence_id']}); the lean is single-source.")

        summary = {
            "lean": lean,
            "positive_class": reference_class,
            "weights": {"positive": round(positive, 6), "negative": round(negative, 6)},
            "balance": balance,
            "single_source": len(directional) == 1,
            "directional": directional,
            "context": context,
            "conflicts": {
                "directional": {"positive_ids": positive_ids, "negative_ids": negative_ids} if positive_ids and negative_ids else None,
                "flagged_by_validation": flagged,
            },
            "rule_table": {"version": table.table_version, "status": table.table_status},
            "rationale": rationale,
        }
        return FusionOutput(
            strategy_id=self.strategy_id,
            supporting_ids=supporting,
            summary=summary,
            unresolved=unresolved,
            strategy_version=self.version,
        )
