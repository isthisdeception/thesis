"""MOD015 Audit Trail. Appends immutable case rows to `case_registry.csv`; never rewrites or deletes rows."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path

from failure_handling import FailureRecord, write_failure

from decision import ALLOWED_DECISIONS
from evidence.item import SCHEMA_VERSION, clock

MODULE_ID = "MOD015"
CASE_ID_PATTERN = re.compile(r"^CASE\d{6}$")
ALLOWED_STATUSES = ("running", "completed", "failed")
HEADER = [
    "Case ID",
    "Timestamp",
    "Input",
    "Evidence",
    "Decision",
    "Model",
    "Version",
    "Configuration",
    "Execution Time",
    "Errors",
    "Warnings",
    "Owner",
    "Status",
    "Created",
    "Updated",
]


@dataclass(frozen=True)
class CaseRow:
    case_id: str
    timestamp: str
    input_id: str
    evidence_ids: tuple[str, ...]
    decision: str
    model_id: str
    version: str
    configuration: str
    execution_time_seconds: float | None
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    owner: str
    status: str
    created: str
    updated: str

    def to_dict(self) -> dict[str, str]:
        return {
            "Case ID": self.case_id,
            "Timestamp": self.timestamp,
            "Input": self.input_id,
            "Evidence": ";".join(self.evidence_ids),
            "Decision": self.decision,
            "Model": self.model_id,
            "Version": self.version,
            "Configuration": self.configuration,
            "Execution Time": f"{self.execution_time_seconds:.4f}" if self.execution_time_seconds is not None else "",
            "Errors": ";".join(self.errors),
            "Warnings": ";".join(self.warnings),
            "Owner": self.owner,
            "Status": self.status,
            "Created": self.created,
            "Updated": self.updated,
        }


@dataclass
class AuditResult:
    row: CaseRow | None = None
    failures: list[FailureRecord] = field(default_factory=list)


def read_case_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = [name.strip() for name in next(reader, [])]
        if header != HEADER:
            raise ValueError(f"case registry header is {header}")
        return [{header[i]: value.strip() for i, value in enumerate(row)} for row in reader if row]


def _ensure_header(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file() or path.stat().st_size == 0:
        with path.open("w", encoding="utf-8", newline="") as handle:
            csv.writer(handle, lineterminator="\n").writerow(HEADER)
        return
    if not path.read_bytes().endswith(b"\n"):
        with path.open("a", encoding="utf-8", newline="") as handle:
            handle.write("\n")


def next_case_id(path: Path) -> str:
    rows = read_case_rows(path) if path.is_file() else []
    numbers: list[int] = []
    for row in rows:
        cid = row.get("Case ID", "")
        if CASE_ID_PATTERN.match(cid):
            numbers.append(int(cid[4:]))
    return f"CASE{max(numbers, default=0) + 1:06d}"


def append_case_row(
    registry_path: Path,
    *,
    case_id: str = "",
    input_id: str = "",
    evidence_ids: list[str] | tuple[str, ...] = (),
    decision: str = "",
    model_id: str = "",
    version: str = SCHEMA_VERSION,
    configuration: str = "rule_based/e4_calibrated_v1",
    execution_time_seconds: float | None = None,
    errors: list[str] | tuple[str, ...] = (),
    warnings: list[str] | tuple[str, ...] = (),
    status: str = "completed",
    owner: str = MODULE_ID,
    timestamp: str | None = None,
    storage_root: Path | None = None,
) -> AuditResult:
    """Append one immutable case row to `case_registry.csv`."""

    result = AuditResult()

    def fail(detail: str) -> AuditResult:
        result.failures.append(_failure(storage_root, case_id or "CASE000000", detail))
        return result

    try:
        _ensure_header(registry_path)
        before = registry_path.read_text(encoding="utf-8")
        _ = read_case_rows(registry_path)
    except (OSError, ValueError) as exc:
        return fail(f"case registry could not be prepared: {exc}")

    resolved_case_id = case_id or next_case_id(registry_path)
    if not CASE_ID_PATTERN.match(resolved_case_id):
        return fail(f"invalid case_id {resolved_case_id!r}")
    if status not in ALLOWED_STATUSES:
        return fail(f"invalid case status {status!r}")
    if decision and decision not in ALLOWED_DECISIONS:
        return fail(f"invalid decision word {decision!r}")
    if status == "completed" and not decision:
        return fail("completed case row requires a decision word")
    if not version:
        return fail("system version is required on a case row")

    stamp = timestamp or clock()
    row = CaseRow(
        case_id=resolved_case_id,
        timestamp=stamp,
        input_id=input_id,
        evidence_ids=tuple(dict.fromkeys(evidence_ids)),
        decision=decision,
        model_id=model_id,
        version=version,
        configuration=configuration,
        execution_time_seconds=execution_time_seconds,
        errors=tuple(dict.fromkeys(errors)),
        warnings=tuple(dict.fromkeys(warnings)),
        owner=owner,
        status=status,
        created=stamp,
        updated=stamp,
    )
    cells = [row.to_dict()[col] for col in HEADER]
    try:
        with registry_path.open("a", encoding="utf-8", newline="") as handle:
            csv.writer(handle, lineterminator="\n").writerow(cells)
        after = registry_path.read_text(encoding="utf-8")
    except OSError as exc:
        return fail(f"case row could not be appended: {exc}")

    if not after.startswith(before):
        raise RuntimeError("audit trail rewrote existing case rows")
    result.row = row
    return result


def _failure(storage_root: Path | None, case_id: str, detail: str) -> FailureRecord:
    if storage_root is None:
        return FailureRecord("", "unexpected_error", "unexpected_error", MODULE_ID, case_id, None, detail, "")
    return write_failure(storage_root, name="unexpected_error", module_id=MODULE_ID, case_id=case_id, detail=detail)
