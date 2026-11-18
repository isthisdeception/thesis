"""The FusionStrategy contract (specs/interfaces.md). A strategy reads evidence records, never the image."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Protocol, Sequence

EVIDENCE_TYPE = "fused_conclusion"
MODULE_ID = "MOD007"
RESERVED_STRATEGY_IDS = ("rule_based", "weighted", "bayesian")
DECISION_WORDS = re.compile(r"\b(Real|Fake|Inconclusive|Unknown)\b")
# Keys that could point a strategy at the stored image or the model file.
_HIDDEN_RAW_KEYS = ("path", "pointer", "bytes")


@dataclass(frozen=True)
class ValidatedEvidence:
    """One MOD006 row, as a strategy sees it. `evidence_id` is the validation row id."""

    evidence_id: str
    evidence_type: str
    collector_evidence_id: str
    collector_source_module: str
    quality: str
    status: str
    confidence: float | None
    validation_reason: str
    processed_output: dict
    raw_output: dict
    dependencies: tuple[str, ...] = ()

    @property
    def conflict_partners(self) -> tuple[str, ...]:
        """Collector ids MOD006 named as conflicting with this item."""

        return tuple(dep for dep in self.dependencies if dep != self.collector_evidence_id)


@dataclass(frozen=True)
class Unresolved:
    evidence_id: str
    reason: str

    def to_json(self) -> dict:
        return {"evidence_id": self.evidence_id, "reason": self.reason}


@dataclass
class FusionOutput:
    """The Processed Output of the fused item. `summary` is a structured conclusion, not a case decision."""

    strategy_id: str
    supporting_ids: list[str]
    summary: dict
    unresolved: list[Unresolved] = field(default_factory=list)
    strategy_version: str = ""

    def to_processed(self) -> dict:
        return {
            "strategy_id": self.strategy_id,
            "supporting_ids": list(self.supporting_ids),
            "summary": self.summary,
            "unresolved": [entry.to_json() for entry in self.unresolved],
        }


class FusionStrategy(Protocol):
    strategy_id: str
    version: str

    def fuse(self, evidence: Sequence[ValidatedEvidence]) -> FusionOutput: ...


def safe_raw(raw: dict) -> dict:
    """Raw output without keys that name a file location."""

    return {key: value for key, value in raw.items() if not any(part in key.lower() for part in _HIDDEN_RAW_KEYS)}


def states_a_decision(payload) -> bool:
    return bool(DECISION_WORDS.search(json.dumps(payload, sort_keys=True)))
