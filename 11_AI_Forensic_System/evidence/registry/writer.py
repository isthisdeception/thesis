"""Append-only evidence registry. An id is assigned once and never reused."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from pathlib import Path

from failure_handling import FailureRecord, write_failure

from evidence.item import EvidenceItem

MODULE_ID = "MOD005"
HEADER = [
    "Evidence ID",
    "Evidence Type",
    "Source Module",
    "Timestamp",
    "Confidence",
    "Description",
    "Raw Output",
    "Processed Output",
    "Quality",
    "Dependencies",
    "Owner",
    "Version",
    "Status",
    "Created",
    "Updated",
]


@dataclass
class RegisterResult:
    items: list[EvidenceItem] = field(default_factory=list)
    failures: list[FailureRecord] = field(default_factory=list)


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = [name.strip() for name in next(reader, [])]
        if header != HEADER:
            raise ValueError(f"evidence registry header is {header}")
        return [{header[i]: value for i, value in enumerate(row)} for row in reader if row]


def _ensure_header(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file() or path.stat().st_size == 0:
        with path.open("w", encoding="utf-8", newline="") as handle:
            csv.writer(handle, lineterminator="\n").writerow(HEADER)
        return
    if not path.read_bytes().endswith(b"\n"):
        with path.open("a", encoding="utf-8", newline="") as handle:
            handle.write("\n")


def _next_id(rows: list[dict[str, str]]) -> int:
    numbers = []
    for row in rows:
        evidence_id = row.get("Evidence ID", "")
        if evidence_id.startswith("EV") and evidence_id[2:].isdigit() and len(evidence_id) == 8:
            numbers.append(int(evidence_id[2:]))
    return max(numbers, default=0) + 1


def _cell(value) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True)
    return str(value)


def _append(path: Path, item: EvidenceItem) -> None:
    row = [
        item.evidence_id,
        item.evidence_type,
        item.source_module,
        item.timestamp,
        _cell(item.confidence),
        item.description,
        _cell(item.raw_output),
        _cell(item.processed_output),
        item.quality,
        ";".join(item.dependencies),
        item.owner,
        item.version,
        item.status,
        item.created,
        item.updated,
    ]
    with path.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(row)


def register(
    items: list[EvidenceItem],
    registry_path: Path,
    *,
    storage_root: Path | None = None,
    case_id: str = "",
) -> RegisterResult:
    """Give each well-formed item a new EV id. A bad item is skipped and the file is not otherwise rewritten."""

    result = RegisterResult()
    _ensure_header(registry_path)
    before = registry_path.read_text(encoding="utf-8")
    rows = read_rows(registry_path)
    number = _next_id(rows)
    for item in items:
        missing = [name for name, value in (("evidence_type", item.evidence_type), ("source_module", item.source_module)) if not value]
        if missing or item.description == "":
            field_name = ", ".join(missing) if missing else "description"
            if storage_root is not None:
                result.failures.append(write_failure(
                    storage_root,
                    name="unexpected_error",
                    module_id=MODULE_ID,
                    case_id=case_id or str(item.raw_output.get("case_id") or ""),
                    input_id=item.raw_output.get("input_id"),
                    detail=f"evidence item is missing {field_name}",
                ))
            else:
                result.failures.append(FailureRecord(
                    failure_id="",
                    name="unexpected_error",
                    reported_name="unexpected_error",
                    module_id=MODULE_ID,
                    case_id=case_id,
                    input_id=item.raw_output.get("input_id"),
                    detail=f"evidence item is missing {field_name}",
                    timestamp="",
                ))
            continue
        evidence_id = f"EV{number:06d}"
        number += 1
        item.evidence_id = evidence_id
        if item.quality != "unevaluated":
            item.quality = "unevaluated"
        if item.status != "recorded":
            item.status = "recorded"
        _append(registry_path, item)
        result.items.append(item)
    after = registry_path.read_text(encoding="utf-8")
    if not after.startswith(before):
        raise RuntimeError("registry writer rewrote existing rows")
    return result
