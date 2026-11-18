"""Evidence item and the EvidenceCollector contract. Collectors do not assign EV ids."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Protocol

from PIL import Image

SCHEMA_VERSION = "0.1.0"
SOURCE_MODULE = "MOD003"


def clock(now: datetime | None = None) -> str:
    return (now or datetime.now().astimezone()).replace(microsecond=0).isoformat()


def luminance(image: Image.Image) -> list[int]:
    gray = image.convert("L")
    reader = getattr(gray, "get_flattened_data", gray.getdata)
    return [int(pixel) for pixel in reader()]


@dataclass(frozen=True)
class CollectorContext:
    case_id: str
    input_id: str
    image: Image.Image
    stored_path: Path
    validation_status: str


@dataclass
class EvidenceItem:
    evidence_type: str
    description: str
    raw_output: dict
    processed_output: dict
    confidence: float | None
    timestamp: str
    evidence_id: str | None = None
    source_module: str = SOURCE_MODULE
    quality: str = "unevaluated"
    dependencies: list[str] = field(default_factory=list)
    owner: str = SOURCE_MODULE
    version: str = SCHEMA_VERSION
    status: str = "recorded"
    created: str = ""
    updated: str = ""

    def __post_init__(self) -> None:
        if not self.created:
            self.created = self.timestamp
        if not self.updated:
            self.updated = self.timestamp

    def to_json(self) -> dict:
        return {
            "evidence_id": self.evidence_id,
            "evidence_type": self.evidence_type,
            "source_module": self.source_module,
            "timestamp": self.timestamp,
            "confidence": self.confidence,
            "description": self.description,
            "raw_output": self.raw_output,
            "processed_output": self.processed_output,
            "quality": self.quality,
            "dependencies": list(self.dependencies),
            "owner": self.owner,
            "version": self.version,
            "status": self.status,
            "created": self.created,
            "updated": self.updated,
        }


def make_item(
    *,
    evidence_type: str,
    description: str,
    raw_output: dict,
    value,
    unit: str,
    confidence: float | None = None,
    extra_processed: dict | None = None,
    now: datetime | None = None,
    source_module: str = SOURCE_MODULE,
) -> EvidenceItem:
    processed = {"value": value, "unit": unit}
    if extra_processed:
        processed.update(extra_processed)
    return EvidenceItem(
        evidence_type=evidence_type,
        description=description,
        raw_output=raw_output,
        processed_output=processed,
        confidence=confidence,
        timestamp=clock(now),
        source_module=source_module,
        owner=source_module,
    )


@dataclass(frozen=True)
class CollectorOutcome:
    items: tuple[EvidenceItem, ...] = ()
    failure_name: str | None = None
    failure_detail: str | None = None

    @classmethod
    def one(cls, item: EvidenceItem) -> CollectorOutcome:
        return cls(items=(item,))

    @classmethod
    def failed(cls, name: str, detail: str) -> CollectorOutcome:
        return cls(failure_name=name, failure_detail=detail)


class EvidenceCollector(Protocol):
    evidence_type: str

    def collect(self, context: CollectorContext) -> CollectorOutcome: ...
