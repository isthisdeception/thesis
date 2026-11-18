"""MOD010 Explainability Engine. Assembles data-only `explanation.json` from validated `explainability_input` items.

Per Module 10 and A.9 (Canonical Figure Policy), this module never reads the image, never renders an image,
never fabricates a map when a collector recorded none, and never states a case decision.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from failure_handling import FailureRecord, write_failure

from evidence.item import SCHEMA_VERSION, clock
from evidence.registry.writer import read_rows
from evidence.validation.validate import MODULE_ID as VALIDATION_MODULE
from evidence.validation.validate import _load_item
from fusion.interface import Unresolved, safe_raw, states_a_decision

MODULE_ID = "MOD010"
EVIDENCE_TYPE = "explainability_input"
CONFIG_PATH = Path(__file__).resolve().parent / "explainability_config.json"
DEFAULT_METHODS = ("grad_cam", "attention_maps", "saliency", "integrated_gradients")
RESERVED_FUTURE_METHODS = ("shap", "lime", "counterfactuals")
_FORBIDDEN_INPUT_KEYS = ("image", "image_path", "image_bytes", "stored_path", "file_path", "bytes", "model", "weights")
_RENDERED_IMAGE_PATTERN = re.compile(
    r"(data:image/|iVBORw0KGgo|/9j/4AAQSkZJRg|\.png\b|\.jpg\b|\.jpeg\b|\.svg\b|\.pdf\b|\.webp\b)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class MethodExplanation:
    method: str
    status: str
    evidence_id: str | None
    collector_evidence_id: str | None
    quality: str | None
    model_id: str | None
    data: dict | list | None

    def to_json(self) -> dict:
        return {
            "method": self.method,
            "status": self.status,
            "evidence_id": self.evidence_id,
            "collector_evidence_id": self.collector_evidence_id,
            "quality": self.quality,
            "model_id": self.model_id,
            "data": self.data,
        }


@dataclass
class ExplanationRecord:
    case_id: str
    module_id: str
    version: str
    figure_policy: str
    methods: list[MethodExplanation]
    supporting_ids: list[str]
    unresolved: list[Unresolved]
    timestamp: str

    def to_json(self) -> dict:
        return {
            "case_id": self.case_id,
            "module_id": self.module_id,
            "version": self.version,
            "figure_policy": self.figure_policy,
            "methods": [entry.to_json() for entry in self.methods],
            "supporting_ids": list(self.supporting_ids),
            "unresolved": [entry.to_json() for entry in self.unresolved],
            "timestamp": self.timestamp,
        }


@dataclass
class ExplanationResult:
    record: ExplanationRecord | None = None
    explanation_path: Path | None = None
    failures: list[FailureRecord] = field(default_factory=list)


def load_explainability_config(path: Path = CONFIG_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def contains_rendered_image(payload: object) -> bool:
    """True when payload contains rendered image bytes, data URIs, or image file paths (violating A.9)."""

    if isinstance(payload, (bytes, bytearray)):
        return True
    try:
        serialized = json.dumps(payload, sort_keys=True)
    except TypeError:
        return True
    return bool(_RENDERED_IMAGE_PATTERN.search(serialized))


def assemble_explanation(
    registry_path: Path,
    evidence_ids: list[str],
    *,
    case_id: str,
    storage_root: Path | None = None,
    explanation_path: Path | None = None,
    config: dict | None = None,
    **forbidden_kwargs: object,
) -> ExplanationResult:
    """Assemble `explanation.json` from validated `explainability_input` items for one case."""

    result = ExplanationResult()

    def fail(detail: str) -> ExplanationResult:
        result.failures.append(_failure(storage_root, case_id, detail))
        return result

    if forbidden_kwargs:
        bad = ", ".join(sorted(forbidden_kwargs))
        if any(any(tok in key.lower() for tok in _FORBIDDEN_INPUT_KEYS) for key in forbidden_kwargs):
            return fail(f"MOD010 forbids image or model inputs ({bad})")
        return fail(f"unexpected arguments to MOD010 ({bad})")

    try:
        settings = config or load_explainability_config()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return fail(f"explainability config could not be loaded: {exc}")

    configured_methods = [str(m) for m in settings.get("configured_methods", DEFAULT_METHODS)]
    if not configured_methods:
        return fail("configured_methods is empty")

    try:
        rows = read_rows(registry_path)
    except (OSError, ValueError) as exc:
        return fail(f"registry could not be read: {exc}")
    by_id = {row["Evidence ID"]: row for row in rows}

    unresolved: list[Unresolved] = []
    candidate_items: list[dict] = []
    seen: set[str] = set()

    for evidence_id in evidence_ids:
        if evidence_id in seen:
            continue
        seen.add(evidence_id)
        row = by_id.get(evidence_id)
        if row is None:
            unresolved.append(Unresolved(evidence_id, "not_in_registry"))
            continue
        if row["Source Module"] != VALIDATION_MODULE:
            unresolved.append(Unresolved(evidence_id, f"not_validated_by_{VALIDATION_MODULE}"))
            continue
        item = _load_item(row)
        item["raw_output"] = safe_raw(item["raw_output"])
        if item["raw_output"].get("case_id") not in (None, "", case_id):
            unresolved.append(Unresolved(evidence_id, "belongs_to_another_case"))
            continue
        if item["evidence_type"] != EVIDENCE_TYPE:
            continue
        candidate_items.append(item)

    last_for_collector = {
        str(item["raw_output"].get("collector_evidence_id", item["evidence_id"])): item["evidence_id"]
        for item in candidate_items
    }
    by_method: dict[str, dict] = {}
    supporting_ids: list[str] = []

    for item in candidate_items:
        collector_id = str(item["raw_output"].get("collector_evidence_id", item["evidence_id"]))
        later = last_for_collector.get(collector_id)
        if later != item["evidence_id"]:
            unresolved.append(Unresolved(item["evidence_id"], f"superseded_by:{later}"))
            continue
        if item["status"] == "failed" or item["quality"] == "unusable":
            reason = str(item["processed_output"].get("validation_reason", "unusable"))
            unresolved.append(Unresolved(item["evidence_id"], f"unusable:{reason}"))
            continue
        method = str(item["raw_output"].get("method") or item["processed_output"].get("method") or "").strip()
        if not method:
            unresolved.append(Unresolved(item["evidence_id"], "missing_method_name"))
            continue
        raw_map = item["raw_output"].get("map")
        proc_val = item["processed_output"].get("value")
        map_payload = raw_map if raw_map is not None else (None if proc_val in (None, "", "no_data") else proc_val)
        if map_payload is not None and contains_rendered_image(map_payload):
            return fail(f"explainability item {item['evidence_id']} contains a rendered image or image path (violates A.9)")
        if method not in configured_methods:
            configured_methods.append(method)
        by_method[method] = {
            "evidence_id": item["evidence_id"],
            "collector_evidence_id": collector_id,
            "quality": item["quality"],
            "model_id": item["processed_output"].get("model_id") or item["raw_output"].get("model_id"),
            "map_payload": map_payload,
        }
        supporting_ids.append(item["evidence_id"])

    method_entries: list[MethodExplanation] = []
    for method in configured_methods:
        recorded = by_method.get(method)
        if recorded is None:
            method_entries.append(
                MethodExplanation(
                    method=method,
                    status="no_data",
                    evidence_id=None,
                    collector_evidence_id=None,
                    quality=None,
                    model_id=None,
                    data=None,
                )
            )
            continue
        payload = recorded["map_payload"]
        if payload is None:
            method_entries.append(
                MethodExplanation(
                    method=method,
                    status="no_data",
                    evidence_id=recorded["evidence_id"],
                    collector_evidence_id=recorded["collector_evidence_id"],
                    quality=recorded["quality"],
                    model_id=recorded["model_id"],
                    data=None,
                )
            )
        else:
            method_entries.append(
                MethodExplanation(
                    method=method,
                    status="recorded",
                    evidence_id=recorded["evidence_id"],
                    collector_evidence_id=recorded["collector_evidence_id"],
                    quality=recorded["quality"],
                    model_id=recorded["model_id"],
                    data=payload,
                )
            )

    stamp = clock()
    record = ExplanationRecord(
        case_id=case_id,
        module_id=MODULE_ID,
        version=SCHEMA_VERSION,
        figure_policy=str(settings.get("figure_policy", "A.9_data_only_no_rendered_images")),
        methods=method_entries,
        supporting_ids=supporting_ids,
        unresolved=unresolved,
        timestamp=stamp,
    )
    serialized_record = record.to_json()
    if states_a_decision(serialized_record):
        return fail("explanation.json contains a case decision word")
    if contains_rendered_image(serialized_record):
        return fail("explanation.json contains a rendered image or image path (violates A.9)")

    out_path = explanation_path or (storage_root / case_id / "explanation.json" if storage_root is not None else None)
    if out_path is not None:
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(serialized_record, indent=2) + "\n", encoding="utf-8")
            result.explanation_path = out_path
        except OSError as exc:
            return fail(f"explanation.json could not be written: {exc}")

    result.record = record
    return result


def _failure(storage_root: Path | None, case_id: str, detail: str) -> FailureRecord:
    if storage_root is None:
        return FailureRecord("", "unexpected_error", "unexpected_error", MODULE_ID, case_id, None, detail, "")
    return write_failure(storage_root, name="unexpected_error", module_id=MODULE_ID, case_id=case_id, detail=detail)
