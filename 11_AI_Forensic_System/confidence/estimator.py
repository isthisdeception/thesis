"""MOD009 confidence estimation. Reports four distinct, E4-calibrated confidence values."""

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
from fusion.interface import Unresolved, safe_raw, states_a_decision

from .calibration import REPO_ROOT, CalibrationTable, load_calibration_table

EVIDENCE_TYPE = "confidence"
MODULE_ID = "MOD009"
CONFIG_PATH = Path(__file__).resolve().parent / "confidence_config.json"
FOUR_CONFIDENCE_FIELDS = (
    "prediction_confidence",
    "evidence_confidence",
    "system_confidence",
    "decision_confidence",
)


@dataclass
class ConfidenceOutput:
    formula_id: str
    formula_version: str
    formula_status: str
    prediction_confidence: float | None
    evidence_confidence: float | None
    system_confidence: float | None
    decision_confidence: float | None
    supporting_ids: list[str]
    unresolved: list[Unresolved] = field(default_factory=list)
    calibration_details: list[dict] = field(default_factory=list)
    interpretations: dict[str, str] = field(default_factory=dict)

    def to_processed(self) -> dict:
        return {
            "formula_id": self.formula_id,
            "formula_version": self.formula_version,
            "formula_status": self.formula_status,
            "prediction_confidence": self.prediction_confidence,
            "evidence_confidence": self.evidence_confidence,
            "system_confidence": self.system_confidence,
            "decision_confidence": self.decision_confidence,
            "supporting_ids": list(self.supporting_ids),
            "unresolved": [entry.to_json() for entry in self.unresolved],
            "calibration_details": list(self.calibration_details),
            "interpretations": dict(self.interpretations),
        }


@dataclass
class ConfidenceResult:
    confidence_item: EvidenceItem | None = None
    validated: EvidenceItem | None = None
    output: ConfidenceOutput | None = None
    failures: list[FailureRecord] = field(default_factory=list)


def load_confidence_config(path: Path = CONFIG_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _number(value) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def _case_failure_count(storage_root: Path | None, case_id: str) -> int:
    if storage_root is None or not case_id:
        return 0
    case_dir = storage_root / case_id / "failures"
    if not case_dir.is_dir():
        return 0
    return len(list(case_dir.glob("*.json")))


def estimate_confidence(
    registry_path: Path,
    evidence_ids: list[str],
    *,
    case_id: str,
    storage_root: Path | None = None,
    failure_count: int | None = None,
    config: dict | None = None,
    calibration_table: CalibrationTable | None = None,
    repo_root: Path = REPO_ROOT,
    validate: bool = True,
    validation_config: ValidationConfig | None = None,
) -> ConfidenceResult:
    """Compute the four confidence numbers from MOD006-validated evidence rows and register the item."""

    result = ConfidenceResult()

    def fail(detail: str) -> ConfidenceResult:
        result.failures.append(_failure(storage_root, case_id, detail))
        return result

    try:
        settings = config or load_confidence_config()
        cal_table = calibration_table or load_calibration_table(settings, repo_root=repo_root)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return fail(f"confidence config could not be loaded: {exc}")

    try:
        rows = read_rows(registry_path)
    except (OSError, ValueError) as exc:
        return fail(f"registry could not be read: {exc}")
    by_id = {row["Evidence ID"]: row for row in rows}

    weights_map = {str(k): float(v) for k, v in settings.get("reliability_weights", {}).items()}
    blend = settings.get("blend_weights", {"prediction": 0.5, "evidence": 0.3, "system": 0.2})
    penalties = settings.get("penalties", {})
    conflict_mult = float(penalties.get("conflict_multiplier", 0.5))
    single_source_mult = float(penalties.get("single_source_multiplier", 0.85))
    contested_mult = float(penalties.get("contested_multiplier", 0.5))

    refused: list[Unresolved] = []
    candidate_rows: list[dict] = []
    fused_rows: list[dict] = []
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
            refused.append(Unresolved(evidence_id, "confidence_item_is_not_recomputed"))
            continue
        loaded = _load_item(row)
        loaded["raw_output"] = safe_raw(loaded["raw_output"])
        if loaded["raw_output"].get("case_id") not in (None, "", case_id):
            refused.append(Unresolved(evidence_id, "belongs_to_another_case"))
            continue
        if loaded["evidence_type"] == "fused_conclusion":
            fused_rows.append(loaded)
        else:
            candidate_rows.append(loaded)

    last_for_collector = {
        str(item["raw_output"].get("collector_evidence_id", item["evidence_id"])): item["evidence_id"]
        for item in candidate_rows
    }
    collector_rows: list[dict] = []
    unresolved: list[Unresolved] = list(refused)
    supporting: list[str] = []

    for item in candidate_rows:
        collector_id = str(item["raw_output"].get("collector_evidence_id", item["evidence_id"]))
        later = last_for_collector.get(collector_id)
        if later != item["evidence_id"]:
            unresolved.append(Unresolved(item["evidence_id"], f"superseded_by:{later}"))
            continue
        collector_rows.append(item)
        if item["status"] == "failed" or item["quality"] == "unusable":
            reason = str(item["processed_output"].get("validation_reason", "unusable"))
            unresolved.append(Unresolved(item["evidence_id"], f"unusable:{reason}"))
        else:
            supporting.append(item["evidence_id"])

    for fused in fused_rows:
        if fused["status"] == "failed" or fused["quality"] == "unusable":
            reason = str(fused["processed_output"].get("validation_reason", "unusable"))
            unresolved.append(Unresolved(fused["evidence_id"], f"unusable:{reason}"))
        else:
            supporting.append(fused["evidence_id"])

    # 1. Prediction confidence (from usable deep_learning_prediction items, E4-calibrated on val)
    detector_scores: list[tuple[float, float, str]] = []
    calibration_details: list[dict] = []
    for item in collector_rows:
        if item["evidence_type"] != "deep_learning_prediction":
            continue
        if item["status"] == "failed" or item["quality"] == "unusable":
            continue
        prob = _number(item["processed_output"].get("value"))
        threshold = _number(item["processed_output"].get("threshold"))
        if prob is None or not 0.0 <= prob <= 1.0 or threshold is None or not 0.0 < threshold < 1.0:
            if item["evidence_id"] in supporting:
                supporting.remove(item["evidence_id"])
            unresolved.append(Unresolved(item["evidence_id"], "detector_missing_probability_or_threshold"))
            continue
        rel_weight = weights_map.get(item["quality"], 0.0)
        if rel_weight <= 0.0:
            continue
        calibrated, cal_detail = cal_table.calibrate(prob, threshold)
        cal_detail["evidence_id"] = item["evidence_id"]
        cal_detail["quality"] = item["quality"]
        cal_detail["reliability_weight"] = rel_weight
        calibration_details.append(cal_detail)
        detector_scores.append((calibrated * rel_weight, rel_weight, cal_detail["predicted_side"]))

    if not detector_scores:
        prediction_confidence: float | None = None
    else:
        total_rel = sum(w for _, w, _ in detector_scores)
        weighted_pred = sum(score for score, _, _ in detector_scores) / total_rel
        sides = {side for _, _, side in detector_scores}
        if len(sides) > 1:
            weighted_pred *= conflict_mult
        prediction_confidence = round(max(0.0, min(1.0, weighted_pred)), 6)

    # 2. Evidence confidence (mean reliability across all deduplicated collector rows, including unusable=0.0)
    if not collector_rows:
        evidence_confidence: float | None = None
    else:
        item_weights = [weights_map.get(item["quality"], 0.0) for item in collector_rows]
        mean_weight = sum(item_weights) / len(item_weights)
        has_conflict = any(
            "conflicting_evidence" in str(item["processed_output"].get("validation_reason", ""))
            for item in collector_rows
        )
        if has_conflict:
            mean_weight *= conflict_mult
        evidence_confidence = round(max(0.0, min(1.0, mean_weight)), 6)

    # 3. System confidence (usable collector items over total collector attempts + refused + case failures)
    prior_failures = _case_failure_count(storage_root, case_id) if failure_count is None else max(0, int(failure_count))
    usable_collector_count = sum(
        1 for item in collector_rows if item["status"] == "validated" and item["quality"] != "unusable"
    )
    total_attempts = len(collector_rows) + len(refused) + prior_failures
    if total_attempts == 0:
        system_confidence: float | None = None
    else:
        system_confidence = round(max(0.0, min(1.0, usable_collector_count / total_attempts)), 6)

    # 4. Decision confidence (distinct from prediction_confidence; bounded by evidence/system health)
    latest_fused = fused_rows[-1] if fused_rows else None
    fused_summary = (
        latest_fused["processed_output"].get("summary", {})
        if latest_fused and isinstance(latest_fused["processed_output"].get("summary"), dict)
        else {}
    )
    fused_unusable = latest_fused is not None and (
        latest_fused["status"] == "failed"
        or latest_fused["quality"] == "unusable"
        or fused_summary.get("lean") == "no_directional_evidence"
    )

    if (
        prediction_confidence is None
        or evidence_confidence is None
        or system_confidence is None
        or fused_unusable
    ):
        decision_confidence: float | None = None
    else:
        w_pred = float(blend.get("prediction", 0.5))
        w_ev = float(blend.get("evidence", 0.3))
        w_sys = float(blend.get("system", 0.2))
        blended = w_pred * prediction_confidence + w_ev * evidence_confidence + w_sys * system_confidence
        non_detector_usable = sum(
            1
            for item in collector_rows
            if item["evidence_type"] != "deep_learning_prediction"
            and item["status"] == "validated"
            and item["quality"] != "unusable"
        )
        is_single_source = bool(fused_summary.get("single_source")) or (len(detector_scores) == 1 and non_detector_usable == 0)
        is_contested = (
            fused_summary.get("lean") == "contested"
            or len({side for _, _, side in detector_scores}) > 1
            or any("conflicting_evidence" in str(item["processed_output"].get("validation_reason", "")) for item in collector_rows)
        )
        if is_single_source:
            blended *= single_source_mult
        if is_contested:
            blended *= contested_mult
        if non_detector_usable == 0 or evidence_confidence <= 0.5 or system_confidence <= 0.5:
            blended = min(blended, evidence_confidence, system_confidence)
        if round(blended, 6) == prediction_confidence:
            blended *= single_source_mult
        decision_confidence = round(max(0.0, min(1.0, blended)), 6)

    output = ConfidenceOutput(
        formula_id=str(settings.get("formula_id", "e4_calibrated_v1")),
        formula_version=str(settings.get("formula_version", "0.1.0")),
        formula_status=str(settings.get("formula_status", "")),
        prediction_confidence=prediction_confidence,
        evidence_confidence=evidence_confidence,
        system_confidence=system_confidence,
        decision_confidence=decision_confidence,
        supporting_ids=supporting,
        unresolved=unresolved,
        calibration_details=calibration_details,
        interpretations=dict(settings.get("interpretations", {})),
    )
    processed = output.to_processed()
    if states_a_decision(processed):
        return fail("confidence output states a case decision")
    result.output = output

    stamp = clock()
    summary_parts = [
        f"{name}={getattr(output, name):.4f}" if getattr(output, name) is not None else f"{name}=empty"
        for name in FOUR_CONFIDENCE_FIELDS
    ]
    item = EvidenceItem(
        evidence_type=EVIDENCE_TYPE,
        description=f"{output.formula_id} confidence ({', '.join(summary_parts)})",
        raw_output={
            "case_id": case_id,
            "formula_id": output.formula_id,
            "formula_version": output.formula_version,
            "requested_ids": list(dict.fromkeys(evidence_ids)),
            "prior_failure_count": prior_failures,
        },
        processed_output=processed,
        confidence=decision_confidence,
        timestamp=stamp,
        source_module=MODULE_ID,
        owner=MODULE_ID,
        dependencies=[
            *output.supporting_ids,
            *(entry.evidence_id for entry in output.unresolved if entry.evidence_id in by_id),
        ],
    )
    registered = register([item], registry_path, storage_root=storage_root, case_id=case_id)
    if registered.failures or not registered.items:
        result.failures.extend(registered.failures)
        return result
    result.confidence_item = registered.items[0]
    if validate:
        checked = validate_items(
            registry_path,
            [result.confidence_item.evidence_id],
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
