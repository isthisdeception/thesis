"""MOD011 Forensic Reasoning Engine. Writes human-readable reasoning strictly grounded in cited EV ids.

Every sentence must map to one or more input `EV` ids and state only measurements present on those rows.
Any untied sentence or wording that names an absent measurement records a MOD016 `unexpected_error`
and is discarded. An empty evidence list produces no sentences and an empty reasoning path.
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
from fusion.interface import Unresolved, safe_raw

MODULE_ID = "MOD011"
CONFIG_PATH = Path(__file__).resolve().parent / "reasoning_config.json"
EV_TOKEN = re.compile(r"\bEV\d{6}\b")
ID_TOKENS = re.compile(r"\b(?:EV\d{6}|MODEL\d+|MOD\d+|CASE\d+|EXP\d+|EVAL\d+|SPLIT\d+|DS\d+|PP\d+)\b")
NUMBER_TOKEN = re.compile(r"(?<![A-Za-z_])-?\d+(?:\.\d+)?(?![A-Za-z_])")
KNOWN_EVIDENCE_TYPES = (
    "image_statistics",
    "metadata",
    "face_detection",
    "face_quality",
    "frequency_domain",
    "compression_artifacts",
    "color_distribution",
    "texture_analysis",
    "deep_learning_prediction",
    "explainability_input",
    "fused_conclusion",
    "confidence",
)
_FORBIDDEN_INPUT_KEYS = ("image", "image_path", "image_bytes", "stored_path", "file_path", "bytes", "model", "weights")


@dataclass(frozen=True)
class ReasoningSentence:
    text: str
    evidence_ids: tuple[str, ...]
    evidence_types: tuple[str, ...] = ()
    fields_used: dict[str, dict] = field(default_factory=dict)

    def to_json(self) -> dict:
        return {
            "text": self.text,
            "evidence_ids": list(self.evidence_ids),
            "evidence_types": list(self.evidence_types),
            "fields_used": dict(self.fields_used),
        }


@dataclass
class ReasoningRecord:
    case_id: str
    module_id: str
    version: str
    language: str
    max_sentences: int
    sentences: list[ReasoningSentence]
    reasoning_path: list[str]
    narrative: str
    unresolved: list[Unresolved]
    rejected_count: int
    timestamp: str

    def to_json(self) -> dict:
        return {
            "case_id": self.case_id,
            "module_id": self.module_id,
            "version": self.version,
            "language": self.language,
            "max_sentences": self.max_sentences,
            "sentences": [entry.to_json() for entry in self.sentences],
            "reasoning_path": list(self.reasoning_path),
            "narrative": self.narrative,
            "unresolved": [entry.to_json() for entry in self.unresolved],
            "rejected_count": self.rejected_count,
            "timestamp": self.timestamp,
        }


@dataclass
class ReasoningResult:
    record: ReasoningRecord | None = None
    reasoning_path_file: Path | None = None
    failures: list[FailureRecord] = field(default_factory=list)


def load_reasoning_config(path: Path = CONFIG_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _fmt_value(value: object) -> str:
    if value is None or value == "":
        return "empty"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.4f}"
    if isinstance(value, dict):
        return json.dumps(value, sort_keys=True)
    return str(value)


def _row_numbers(item: dict) -> list[float]:
    nums: list[float] = []

    def collect(obj: object) -> None:
        if isinstance(obj, bool):
            return
        if isinstance(obj, (int, float)):
            nums.append(float(obj))
        elif isinstance(obj, dict):
            for v in obj.values():
                collect(v)
        elif isinstance(obj, (list, tuple)):
            for v in obj:
                collect(v)

    collect(item.get("confidence"))
    collect(item.get("processed_output", {}))
    collect(item.get("raw_output", {}))
    supp = item.get("processed_output", {}).get("supporting_ids")
    if isinstance(supp, list):
        nums.append(float(len(supp)))
    return nums


def _build_sentence(item: dict, templates: dict[str, str]) -> ReasoningSentence:
    ev_id = item["evidence_id"]
    ev_type = item["evidence_type"]
    quality = item["quality"]
    proc = item["processed_output"]
    val = proc.get("value")
    unit = str(proc.get("unit") or "").strip()

    if item["status"] == "failed" or quality == "unusable":
        reason = str(proc.get("validation_reason", "unusable"))
        text = templates["collector_unusable"].format(
            evidence_id=ev_id,
            evidence_type=ev_type,
            validation_reason=reason,
            value=_fmt_value(val),
        )
        fields = {"quality": quality, "validation_reason": reason, "value": val}
    elif ev_type == "deep_learning_prediction":
        model_id = str(proc.get("model_id") or item["raw_output"].get("model_id") or "unknown")
        threshold = proc.get("threshold")
        text = templates["deep_learning_prediction"].format(
            evidence_id=ev_id,
            model_id=model_id,
            quality=quality,
            value=_fmt_value(val),
            threshold=_fmt_value(threshold),
        )
        fields = {"model_id": model_id, "quality": quality, "value": val, "threshold": threshold}
    elif ev_type == "fused_conclusion":
        strategy_id = str(proc.get("strategy_id") or "")
        summary = proc.get("summary") if isinstance(proc.get("summary"), dict) else {}
        lean = str(summary.get("lean") or "")
        supporting_count = len(proc.get("supporting_ids", []))
        text = templates["fused_conclusion"].format(
            evidence_id=ev_id,
            strategy_id=strategy_id,
            quality=quality,
            supporting_count=supporting_count,
            lean=lean,
        )
        fields = {"strategy_id": strategy_id, "quality": quality, "lean": lean}
    elif ev_type == "confidence":
        formula_id = str(proc.get("formula_id") or "")
        text = templates["confidence"].format(
            evidence_id=ev_id,
            formula_id=formula_id,
            quality=quality,
            prediction_confidence=_fmt_value(proc.get("prediction_confidence")),
            evidence_confidence=_fmt_value(proc.get("evidence_confidence")),
            system_confidence=_fmt_value(proc.get("system_confidence")),
            decision_confidence=_fmt_value(proc.get("decision_confidence")),
        )
        fields = {
            "formula_id": formula_id,
            "quality": quality,
            "prediction_confidence": proc.get("prediction_confidence"),
            "evidence_confidence": proc.get("evidence_confidence"),
            "system_confidence": proc.get("system_confidence"),
            "decision_confidence": proc.get("decision_confidence"),
        }
    else:
        unit_suffix = f" {unit}" if unit else ""
        text = templates["collector_value"].format(
            evidence_id=ev_id,
            evidence_type=ev_type,
            quality=quality,
            value=_fmt_value(val),
            unit_suffix=unit_suffix,
        )
        fields = {"quality": quality, "value": val}

    return ReasoningSentence(
        text=text,
        evidence_ids=(ev_id,),
        evidence_types=(ev_type,),
        fields_used={ev_id: fields},
    )


def verify_sentence(
    sentence: ReasoningSentence,
    valid_rows_by_id: dict[str, dict],
) -> str | None:
    """Return an error reason if `sentence` cites an absent id or names an absent measurement."""

    if not sentence.text or not sentence.text.strip():
        return "sentence text is empty"
    if not sentence.evidence_ids:
        return "sentence has no cited evidence_ids"

    text_ev_ids = set(EV_TOKEN.findall(sentence.text))
    if not text_ev_ids:
        return "sentence text does not contain an EV id slot"
    declared_ids = set(sentence.evidence_ids)
    if text_ev_ids != declared_ids:
        return f"sentence text EV ids {sorted(text_ev_ids)} do not match declared {sorted(declared_ids)}"

    missing_ids = [ev_id for ev_id in sentence.evidence_ids if ev_id not in valid_rows_by_id]
    if missing_ids:
        return f"sentence cites evidence id(s) absent from input: {missing_ids}"

    cited_rows = [valid_rows_by_id[ev_id] for ev_id in sentence.evidence_ids]
    cited_types = {row["evidence_type"] for row in cited_rows}

    for known_type in KNOWN_EVIDENCE_TYPES:
        if re.search(rf"\b{re.escape(known_type)}\b", sentence.text) and known_type not in cited_types:
            return f"sentence names evidence type {known_type!r} absent from cited rows {list(sentence.evidence_ids)}"

    for ev_id, fields in sentence.fields_used.items():
        if ev_id not in valid_rows_by_id:
            return f"fields_used references absent evidence id {ev_id}"
        row = valid_rows_by_id[ev_id]
        proc = row["processed_output"]
        raw = row["raw_output"]
        summary = proc.get("summary") if isinstance(proc.get("summary"), dict) else {}
        for key, expected in fields.items():
            if key == "quality":
                actual = row["quality"]
            elif key in proc:
                actual = proc[key]
            elif key in summary:
                actual = summary[key]
            elif key in raw:
                actual = raw[key]
            else:
                return f"sentence claims field {key!r} absent from row {ev_id}"
            if actual != expected:
                return f"sentence field {key!r}={expected!r} does not match row {ev_id} value {actual!r}"

    allowed_numbers: list[float] = []
    for row in cited_rows:
        allowed_numbers.extend(_row_numbers(row))

    scrubbed = ID_TOKENS.sub("", sentence.text)
    for match in NUMBER_TOKEN.findall(scrubbed):
        num = float(match)
        if not any(abs(num - allowed) <= 1e-3 for allowed in allowed_numbers):
            return f"sentence states numeric measurement {match} absent from cited rows {list(sentence.evidence_ids)}"

    return None


def compose_reasoning(
    registry_path: Path,
    evidence_ids: list[str],
    *,
    case_id: str,
    candidate_sentences: list[ReasoningSentence] | None = None,
    storage_root: Path | None = None,
    reasoning_path: Path | None = None,
    config: dict | None = None,
    **forbidden_kwargs: object,
) -> ReasoningResult:
    """Compose and verify the human-readable reasoning record from validated evidence rows."""

    result = ReasoningResult()

    def fail(detail: str) -> ReasoningResult:
        result.failures.append(_failure(storage_root, case_id, detail))
        return result

    if forbidden_kwargs:
        bad = ", ".join(sorted(forbidden_kwargs))
        if any(any(tok in key.lower() for tok in _FORBIDDEN_INPUT_KEYS) for key in forbidden_kwargs):
            return fail(f"MOD011 forbids image or model inputs ({bad})")
        return fail(f"unexpected arguments to MOD011 ({bad})")

    try:
        settings = config or load_reasoning_config()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return fail(f"reasoning config could not be loaded: {exc}")

    language = str(settings.get("language", "en"))
    max_sentences = int(settings.get("max_sentences", 12))
    templates = dict(settings.get("templates", {}))
    if max_sentences <= 0:
        return fail("max_sentences must be positive")
    for name, tpl in templates.items():
        if "{evidence_id}" not in str(tpl):
            return fail(f"template {name!r} is missing required {{evidence_id}} slot")

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
        candidate_items.append(item)

    last_for_collector = {
        str(item["raw_output"].get("collector_evidence_id", item["evidence_id"])): item["evidence_id"]
        for item in candidate_items
    }
    valid_items: list[dict] = []
    for item in candidate_items:
        collector_id = str(item["raw_output"].get("collector_evidence_id", item["evidence_id"]))
        later = last_for_collector.get(collector_id)
        if later != item["evidence_id"]:
            unresolved.append(Unresolved(item["evidence_id"], f"superseded_by:{later}"))
            continue
        valid_items.append(item)

    valid_by_id = {item["evidence_id"]: item for item in valid_items}

    if candidate_sentences is not None:
        raw_sentences = list(candidate_sentences)
    else:
        raw_sentences = [_build_sentence(item, templates) for item in valid_items]

    verified: list[ReasoningSentence] = []
    rejected_count = 0
    for sentence in raw_sentences:
        error = verify_sentence(sentence, valid_by_id)
        if error is not None:
            rejected_count += 1
            result.failures.append(_failure(storage_root, case_id, error))
            continue
        if len(verified) < max_sentences:
            verified.append(sentence)

    cited_path: list[str] = []
    for sentence in verified:
        for ev_id in sentence.evidence_ids:
            if ev_id not in cited_path:
                cited_path.append(ev_id)

    stamp = clock()
    record = ReasoningRecord(
        case_id=case_id,
        module_id=MODULE_ID,
        version=SCHEMA_VERSION,
        language=language,
        max_sentences=max_sentences,
        sentences=verified,
        reasoning_path=cited_path,
        narrative=" ".join(s.text for s in verified),
        unresolved=unresolved,
        rejected_count=rejected_count,
        timestamp=stamp,
    )

    out_path = reasoning_path or (storage_root / case_id / "reasoning.json" if storage_root is not None else None)
    if out_path is not None:
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(record.to_json(), indent=2) + "\n", encoding="utf-8")
            result.reasoning_path_file = out_path
        except OSError as exc:
            return fail(f"reasoning.json could not be written: {exc}")

    result.record = record
    return result


def _failure(storage_root: Path | None, case_id: str, detail: str) -> FailureRecord:
    if storage_root is None:
        return FailureRecord("", "unexpected_error", "unexpected_error", MODULE_ID, case_id, None, detail, "")
    return write_failure(storage_root, name="unexpected_error", module_id=MODULE_ID, case_id=case_id, detail=detail)
