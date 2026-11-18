"""MOD008 Decision Engine. Reads only validated fused and confidence evidence rows; never the image."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from failure_handling import FailureRecord, write_failure

from confidence.estimator import FOUR_CONFIDENCE_FIELDS
from evidence.item import SCHEMA_VERSION, clock
from evidence.registry.writer import read_rows
from evidence.validation.validate import MODULE_ID as VALIDATION_MODULE
from evidence.validation.validate import _load_item
from fusion.interface import safe_raw

MODULE_ID = "MOD008"
ALLOWED_DECISIONS = ("Real", "Fake", "Inconclusive", "Unknown")
EV_ID_PATTERN = re.compile(r"^EV\d{6}$")
CONFIG_PATH = Path(__file__).resolve().parent / "decision_config.json"
_FORBIDDEN_INPUT_KEYS = ("image", "image_path", "image_bytes", "stored_path", "file_path", "bytes", "model", "weights")


@dataclass
class DecisionRecord:
    case_id: str
    decision: str
    fused_evidence_id: str
    confidence_evidence_id: str
    reasoning_path: list[str]
    decision_metadata: dict

    def to_json(self) -> dict:
        return {
            "case_id": self.case_id,
            "decision": self.decision,
            "fused_evidence_id": self.fused_evidence_id,
            "confidence_evidence_id": self.confidence_evidence_id,
            "reasoning_path": list(self.reasoning_path),
            "decision_metadata": dict(self.decision_metadata),
        }


@dataclass
class DecisionResult:
    record: DecisionRecord | None = None
    decision_path: Path | None = None
    failures: list[FailureRecord] = field(default_factory=list)
    warnings: list[FailureRecord] = field(default_factory=list)


def load_decision_config(path: Path = CONFIG_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _is_ev_id(value: object) -> bool:
    return isinstance(value, str) and bool(EV_ID_PATTERN.match(value))


def decide_case(
    registry_path: Path,
    *,
    case_id: str,
    fused_evidence_id: str = "",
    confidence_evidence_id: str = "",
    storage_root: Path | None = None,
    decision_path: Path | None = None,
    config: dict | None = None,
    **forbidden_kwargs: object,
) -> DecisionResult:
    """Write `decision.json` from the validated `fused_conclusion` id and validated `confidence` id only."""

    result = DecisionResult()

    def fail(detail: str, *, name: str = "unexpected_error") -> DecisionResult:
        result.failures.append(_failure(storage_root, case_id, detail, name=name))
        return result

    if forbidden_kwargs:
        bad = ", ".join(sorted(forbidden_kwargs))
        if any(any(tok in key.lower() for tok in _FORBIDDEN_INPUT_KEYS) for key in forbidden_kwargs):
            return fail(f"MOD008 forbids image or model inputs ({bad})")
        return fail(f"unexpected arguments to MOD008 ({bad})")

    if not _is_ev_id(fused_evidence_id) or not _is_ev_id(confidence_evidence_id):
        return fail(
            f"MOD008 requires EV ids for fused_evidence_id ({fused_evidence_id!r}) "
            f"and confidence_evidence_id ({confidence_evidence_id!r})"
        )

    try:
        settings = config or load_decision_config()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return fail(f"decision config could not be loaded: {exc}")

    allowed = tuple(settings.get("allowed_decisions", ALLOWED_DECISIONS))
    if set(allowed) != set(ALLOWED_DECISIONS):
        return fail(f"allowed_decisions {allowed!r} does not match canonical vocabulary")

    try:
        rows = read_rows(registry_path)
    except (OSError, ValueError) as exc:
        return fail(f"registry could not be read: {exc}")
    by_id = {row["Evidence ID"]: row for row in rows}

    fused_row = by_id.get(fused_evidence_id)
    if fused_row is None:
        return fail(f"fused_evidence_id {fused_evidence_id} is not in registry")
    if fused_row["Source Module"] != VALIDATION_MODULE:
        return fail(f"fused_evidence_id {fused_evidence_id} was not validated by {VALIDATION_MODULE}")
    if fused_row["Evidence Type"] != "fused_conclusion":
        return fail(f"fused_evidence_id {fused_evidence_id} has type {fused_row['Evidence Type']!r}, expected 'fused_conclusion'")
    if fused_row["Status"] != "validated" or fused_row["Quality"] == "unusable":
        return fail(f"fused_evidence_id {fused_evidence_id} is {fused_row['Quality']}/{fused_row['Status']}")

    conf_row = by_id.get(confidence_evidence_id)
    if conf_row is None:
        return fail(f"confidence_evidence_id {confidence_evidence_id} is not in registry")
    if conf_row["Source Module"] != VALIDATION_MODULE:
        return fail(f"confidence_evidence_id {confidence_evidence_id} was not validated by {VALIDATION_MODULE}")
    if conf_row["Evidence Type"] != "confidence":
        return fail(f"confidence_evidence_id {confidence_evidence_id} has type {conf_row['Evidence Type']!r}, expected 'confidence'")
    if conf_row["Status"] != "validated" or conf_row["Quality"] == "unusable":
        return fail(f"confidence_evidence_id {confidence_evidence_id} is {conf_row['Quality']}/{conf_row['Status']}")

    fused_item = _load_item(fused_row)
    fused_item["raw_output"] = safe_raw(fused_item["raw_output"])
    conf_item = _load_item(conf_row)
    conf_item["raw_output"] = safe_raw(conf_item["raw_output"])

    if fused_item["raw_output"].get("case_id") not in (None, "", case_id):
        return fail(f"fused_evidence_id {fused_evidence_id} belongs to another case")
    if conf_item["raw_output"].get("case_id") not in (None, "", case_id):
        return fail(f"confidence_evidence_id {confidence_evidence_id} belongs to another case")

    fused_proc = fused_item["processed_output"]
    strategy_id = str(fused_proc.get("strategy_id", ""))
    summary = fused_proc.get("summary") if isinstance(fused_proc.get("summary"), dict) else {}
    if not strategy_id or not summary:
        return fail(f"fused_evidence_id {fused_evidence_id} is missing strategy_id or summary")

    conf_proc = conf_item["processed_output"]
    if not all(field_name in conf_proc for field_name in FOUR_CONFIDENCE_FIELDS):
        return fail(f"confidence_evidence_id {confidence_evidence_id} is missing one of the four confidence fields")

    lean = str(summary.get("lean", ""))
    positive_class = str(summary.get("positive_class") or "").lower()
    conflicts = summary.get("conflicts") if isinstance(summary.get("conflicts"), dict) else {}
    directional_conflict = bool(conflicts.get("directional"))
    validation_conflict = bool(conflicts.get("flagged_by_validation"))

    conf_values = {name: conf_proc.get(name) for name in FOUR_CONFIDENCE_FIELDS}
    decision_conf = conf_values["decision_confidence"]
    min_decision_conf = float(settings.get("min_decision_confidence", 0.5))
    low_conf_warn_below = float(settings.get("low_confidence_warning_below", 0.5))
    stop_on_low_conf = bool(settings.get("stop_on_low_confidence", False))
    inconclusive_on_val_conflict = bool(settings.get("inconclusive_on_validation_conflict", True))
    class_map = settings.get("positive_class_decisions", {}).get(positive_class)

    # Evaluate decision rules in priority order
    if lean == "no_directional_evidence" or not class_map:
        decision = "Unknown"
        rule_id = "no_directional_evidence_unknown" if lean == "no_directional_evidence" else "unmapped_positive_class_unknown"
    elif lean == "contested" or directional_conflict:
        decision = "Inconclusive"
        rule_id = "contested_directional_evidence_inconclusive"
    elif inconclusive_on_val_conflict and validation_conflict:
        decision = "Inconclusive"
        rule_id = "conflicting_evidence_inconclusive"
    elif decision_conf is None or float(decision_conf) < min_decision_conf:
        if decision_conf is None or float(decision_conf) < low_conf_warn_below:
            detail = (
                f"decision_confidence is {decision_conf} (below {low_conf_warn_below}) "
                f"on {confidence_evidence_id}"
            )
            if stop_on_low_conf:
                return fail(detail, name="low_confidence")
            result.warnings.append(_failure(storage_root, case_id, detail, name="low_confidence"))
        decision = "Inconclusive"
        rule_id = "low_decision_confidence_inconclusive"
    elif lean == "positive_class":
        decision = str(class_map["positive_class"])
        rule_id = "validated_positive_lean_fake"
    elif lean == "negative_class":
        decision = str(class_map["negative_class"])
        rule_id = "validated_negative_lean_real"
    else:
        return fail(f"unrecognized lean {lean!r} in fused item {fused_evidence_id}")

    if decision not in ALLOWED_DECISIONS:
        return fail(f"mapped decision {decision!r} is outside allowed vocabulary")

    supporting_ids = [
        ev_id
        for ev_id in fused_proc.get("supporting_ids", [])
        if _is_ev_id(ev_id) and ev_id in by_id
    ]
    reasoning_path: list[str] = []
    for ev_id in [*supporting_ids, fused_evidence_id, confidence_evidence_id]:
        if ev_id not in reasoning_path:
            reasoning_path.append(ev_id)

    unresolved_ids = [
        entry.get("evidence_id")
        for entry in fused_proc.get("unresolved", [])
        if isinstance(entry, dict) and _is_ev_id(entry.get("evidence_id"))
    ]
    reasoning_steps = [
        {
            "step": "supporting_evidence",
            "evidence_ids": supporting_ids,
            "unresolved_evidence_ids": unresolved_ids,
        },
        {
            "step": "evidence_fusion",
            "evidence_id": fused_evidence_id,
            "collector_evidence_id": str(fused_item["raw_output"].get("collector_evidence_id", "")),
            "strategy_id": strategy_id,
            "lean": lean,
        },
        {
            "step": "confidence_estimation",
            "evidence_id": confidence_evidence_id,
            "collector_evidence_id": str(conf_item["raw_output"].get("collector_evidence_id", "")),
            "formula_id": str(conf_proc.get("formula_id", "")),
        },
        {
            "step": "decision_rule",
            "evidence_ids": [fused_evidence_id, confidence_evidence_id],
            "rule_id": rule_id,
            "decision": decision,
        },
    ]

    stamp = clock()
    metadata = {
        "module_id": MODULE_ID,
        "version": SCHEMA_VERSION,
        "strategy_id": strategy_id,
        "rule_id": rule_id,
        "rule_version": str(settings.get("rule_version", "0.1.0")),
        "rule_status": str(settings.get("rule_status", "")),
        "lean": lean,
        "confidence": conf_values,
        "reasoning_steps": reasoning_steps,
        "warning_failure_ids": [w.failure_id for w in result.warnings if w.failure_id],
        "timestamp": stamp,
    }
    record = DecisionRecord(
        case_id=case_id,
        decision=decision,
        fused_evidence_id=fused_evidence_id,
        confidence_evidence_id=confidence_evidence_id,
        reasoning_path=reasoning_path,
        decision_metadata=metadata,
    )
    result.record = record

    out_path = decision_path or (storage_root / case_id / "decision.json" if storage_root is not None else None)
    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(record.to_json(), indent=2) + "\n", encoding="utf-8")
        result.decision_path = out_path
    return result


def _failure(
    storage_root: Path | None,
    case_id: str,
    detail: str,
    *,
    name: str = "unexpected_error",
) -> FailureRecord:
    if storage_root is None:
        return FailureRecord("", name, name, MODULE_ID, case_id, None, detail, "")
    return write_failure(storage_root, name=name, module_id=MODULE_ID, case_id=case_id, detail=detail)
