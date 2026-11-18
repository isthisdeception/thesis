"""Append a reliability row for each evidence item. The collector row is left as it was."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from failure_handling import FailureRecord, write_failure

from evidence.item import EvidenceItem, clock
from evidence.registry.writer import _append, _next_id, read_rows

from .checks import ValidationConfig, conflicts, findings_for

MODULE_ID = "MOD006"
RANK = {"high": 0, "medium": 1, "low": 2, "unusable": 3}


@dataclass
class ValidationResult:
    items: list[EvidenceItem] = field(default_factory=list)
    failures: list[FailureRecord] = field(default_factory=list)


def _load_item(row: dict[str, str]) -> dict:
    confidence = row.get("Confidence", "")
    return {
        "evidence_id": row["Evidence ID"],
        "evidence_type": row["Evidence Type"],
        "source_module": row["Source Module"],
        "timestamp": row["Timestamp"],
        "confidence": float(confidence) if confidence not in ("", None) else None,
        "description": row["Description"],
        "raw_output": json.loads(row["Raw Output"]) if row.get("Raw Output") else {},
        "processed_output": json.loads(row["Processed Output"]) if row.get("Processed Output") else {},
        "quality": row["Quality"],
        "dependencies": [part for part in row.get("Dependencies", "").split(";") if part],
        "owner": row["Owner"],
        "version": row["Version"],
        "status": row["Status"],
        "created": row["Created"],
        "updated": row["Updated"],
    }


def _quality(findings, conflict: bool) -> tuple[str, str, str]:
    reasons = [finding.reason for finding in findings]
    quality = "high"
    for finding in findings:
        if RANK[finding.quality] > RANK[quality]:
            quality = finding.quality
    if conflict:
        reasons.append("conflicting_evidence")
        if RANK["low"] > RANK[quality]:
            quality = "low"
    status = "failed" if quality == "unusable" else "validated"
    return quality, status, ";".join(reasons) if reasons else "no_reliability_concern"


def validate_items(
    registry_path: Path,
    evidence_ids: list[str],
    *,
    storage_root: Path | None = None,
    case_id: str = "",
    config: ValidationConfig | None = None,
) -> ValidationResult:
    """Score each requested id. A missing registry does not mark any item high."""

    settings = config or ValidationConfig()
    result = ValidationResult()
    try:
        rows = read_rows(registry_path)
    except (OSError, ValueError) as exc:
        result.failures.append(_failure(storage_root, case_id, f"registry could not be read: {exc}"))
        return result
    by_id = {row["Evidence ID"]: _load_item(row) for row in rows}
    chosen = []
    for evidence_id in evidence_ids:
        item = by_id.get(evidence_id)
        if item is None or item["source_module"] == MODULE_ID:
            result.failures.append(_failure(storage_root, case_id, f"{evidence_id} is not a collector row"))
            continue
        chosen.append(item)
    if not chosen and evidence_ids:
        return result
    partner_ids = conflicts(chosen, settings)
    before = registry_path.read_text(encoding="utf-8")
    number = _next_id(rows)
    stamp = clock()
    for item in chosen:
        findings = findings_for(item, settings)
        partners = partner_ids.get(item["evidence_id"], [])
        quality, status, reason = _quality(findings, bool(partners))
        evidence_id = f"EV{number:06d}"
        number += 1
        scored = EvidenceItem(
            evidence_id=evidence_id,
            evidence_type=item["evidence_type"],
            source_module=MODULE_ID,
            timestamp=stamp,
            confidence=item["confidence"],
            description=f"{item['description']} | validation: {reason}",
            raw_output={**item["raw_output"], "collector_evidence_id": item["evidence_id"], "collector_source_module": item["source_module"]},
            processed_output={**item["processed_output"], "validation_reason": reason, "reliability": quality},
            quality=quality,
            dependencies=[item["evidence_id"], *partners],
            owner=MODULE_ID,
            version=item["version"],
            status=status,
            created=stamp,
            updated=stamp,
        )
        _append(registry_path, scored)
        result.items.append(scored)
    if not registry_path.read_text(encoding="utf-8").startswith(before):
        raise RuntimeError("validation rewrote existing evidence rows")
    return result


def _failure(storage_root: Path | None, case_id: str, detail: str) -> FailureRecord:
    if storage_root is None:
        return FailureRecord("", "unexpected_error", "unexpected_error", MODULE_ID, case_id, None, detail, "")
    return write_failure(storage_root, name="unexpected_error", module_id=MODULE_ID, case_id=case_id, detail=detail)
