"""MOD007 engine: pick the configured strategy, fuse validated rows, register and validate the fused item.

The engine owns the checks every strategy must pass (traceability, no decision words).
It does not contain any strategy's rules and does not decide the case.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from failure_handling import FailureRecord, write_failure

from evidence.item import EvidenceItem, clock
from evidence.registry.writer import read_rows, register
from evidence.validation import ValidationConfig, validate_items
from evidence.validation.validate import MODULE_ID as VALIDATION_MODULE
from evidence.validation.validate import _load_item

from fusion.interface import (
    EVIDENCE_TYPE,
    MODULE_ID,
    FusionOutput,
    FusionStrategy,
    Unresolved,
    ValidatedEvidence,
    safe_raw,
    states_a_decision,
)
from fusion.strategies import build_strategy

CONFIG_PATH = Path(__file__).resolve().parent / "fusion_config.json"


@dataclass
class FusionResult:
    fused: EvidenceItem | None = None
    validated: EvidenceItem | None = None
    output: FusionOutput | None = None
    failures: list[FailureRecord] = field(default_factory=list)


def load_config(path: Path = CONFIG_PATH) -> tuple[str, dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    strategy_id = payload["strategy_id"]
    return strategy_id, payload.get(strategy_id, {})


def _to_validated(item: dict) -> ValidatedEvidence:
    raw = item["raw_output"]
    processed = item["processed_output"]
    return ValidatedEvidence(
        evidence_id=item["evidence_id"],
        evidence_type=item["evidence_type"],
        collector_evidence_id=str(raw.get("collector_evidence_id", "")),
        collector_source_module=str(raw.get("collector_source_module", "")),
        quality=item["quality"],
        status=item["status"],
        confidence=item["confidence"],
        validation_reason=str(processed.get("validation_reason", "")),
        processed_output=dict(processed),
        raw_output=safe_raw(raw),
        dependencies=tuple(item["dependencies"]),
    )


def _check_output(output: FusionOutput, strategy: FusionStrategy, given: set[str], refused: list[Unresolved]) -> str | None:
    if output.strategy_id != strategy.strategy_id:
        return f"strategy returned strategy_id {output.strategy_id!r}"
    supporting = set(output.supporting_ids)
    unresolved = {entry.evidence_id for entry in output.unresolved}
    if not supporting <= given:
        return f"supporting ids not given to the strategy: {sorted(supporting - given)}"
    if supporting & unresolved:
        return f"ids both supporting and unresolved: {sorted(supporting & unresolved)}"
    missing = given - supporting - unresolved
    if missing:
        return f"ids neither supporting nor unresolved: {sorted(missing)}"
    if states_a_decision(output.to_processed()):
        return "fused output states a case decision"
    if any(not entry.reason for entry in [*output.unresolved, *refused]):
        return "an unresolved id has no reason"
    return None


def fuse_case(
    registry_path: Path,
    evidence_ids: list[str],
    *,
    case_id: str,
    strategy_id: str | None = None,
    strategy: FusionStrategy | None = None,
    settings: dict | None = None,
    storage_root: Path | None = None,
    validate: bool = True,
    validation_config: ValidationConfig | None = None,
) -> FusionResult:
    """Fuse the MOD006 rows named by `evidence_ids` for one case.

    `strategy` (an instance) or `strategy_id` (looked up in the registry) selects the
    strategy; with neither, `fusion_config.json` does. An unknown id writes a MOD016
    failure and no fused item; it does not fall back to `rule_based`.
    """

    result = FusionResult()

    def fail(detail: str) -> FusionResult:
        result.failures.append(_failure(storage_root, case_id, detail))
        return result

    if strategy is None:
        if strategy_id is None:
            strategy_id, configured = load_config()
            settings = configured if settings is None else settings
        try:
            strategy = build_strategy(strategy_id, settings)
        except (KeyError, ValueError, TypeError) as exc:
            return fail(str(exc).strip("'\""))

    try:
        rows = read_rows(registry_path)
    except (OSError, ValueError) as exc:
        return fail(f"registry could not be read: {exc}")
    by_id = {row["Evidence ID"]: row for row in rows}

    refused: list[Unresolved] = []
    usable: list[ValidatedEvidence] = []
    seen: set[str] = set()
    for evidence_id in evidence_ids:
        if evidence_id in seen:
            continue
        seen.add(evidence_id)
        row = by_id.get(evidence_id)
        if row is None:
            refused.append(Unresolved(evidence_id, "not_in_registry"))
            continue
        if row["Source Module"] != VALIDATION_MODULE:
            refused.append(Unresolved(evidence_id, f"not_validated_by_{VALIDATION_MODULE}"))
            continue
        if row["Evidence Type"] == EVIDENCE_TYPE:
            refused.append(Unresolved(evidence_id, "fused_item_is_not_refused"))
            continue
        item = _load_item(row)
        if item["raw_output"].get("case_id") not in (None, "", case_id):
            refused.append(Unresolved(evidence_id, "belongs_to_another_case"))
            continue
        usable.append(_to_validated(item))

    try:
        output = strategy.fuse(usable)
    except Exception as exc:  # a strategy bug must not become a fused item
        return fail(f"strategy {strategy.strategy_id} raised {exc.__class__.__name__}: {exc}")
    problem = _check_output(output, strategy, {item.evidence_id for item in usable}, refused)
    if problem:
        return fail(problem)
    output.unresolved = [*refused, *output.unresolved]
    result.output = output

    lean = output.summary.get("lean", "")
    stamp = clock()
    fused = EvidenceItem(
        evidence_type=EVIDENCE_TYPE,
        description=(
            f"{output.strategy_id} fusion of {len(output.supporting_ids)} supporting and "
            f"{len(output.unresolved)} unresolved evidence items; lean {lean or 'not reported'}"
        ),
        raw_output={
            "case_id": case_id,
            "strategy_id": output.strategy_id,
            "strategy_version": output.strategy_version or getattr(strategy, "version", ""),
            "requested_ids": list(dict.fromkeys(evidence_ids)),
        },
        processed_output=output.to_processed(),
        confidence=None,
        timestamp=stamp,
        source_module=MODULE_ID,
        owner=MODULE_ID,
        dependencies=[*output.supporting_ids, *(entry.evidence_id for entry in output.unresolved if entry.evidence_id in by_id)],
    )
    registered = register([fused], registry_path, storage_root=storage_root, case_id=case_id)
    if registered.failures or not registered.items:
        result.failures.extend(registered.failures)
        return result
    result.fused = registered.items[0]
    if validate:
        checked = validate_items(
            registry_path,
            [result.fused.evidence_id],
            storage_root=storage_root,
            case_id=case_id,
            config=validation_config,
        )
        result.failures.extend(checked.failures)
        result.validated = checked.items[0] if checked.items else None
    return result


def _failure(storage_root: Path | None, case_id: str, detail: str) -> FailureRecord:
    if storage_root is None:
        return FailureRecord("", "unexpected_error", "unexpected_error", MODULE_ID, case_id, None, detail, "")
    return write_failure(storage_root, name="unexpected_error", module_id=MODULE_ID, case_id=case_id, detail=detail)
