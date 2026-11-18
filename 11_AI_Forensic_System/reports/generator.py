"""MOD012 Report Generator. Produces reproducible JSON, Markdown (Template 24), and HTML case reports.

Reads only recorded pipeline artifacts (`decision.json`, `explanation.json`, `reasoning.json`,
`input_metadata.json`, `validation.json`, and `evidence_registry.csv`) and version stamps.
Never opens the image and never recomputes a prediction.
"""

from __future__ import annotations

import html
import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from failure_handling import FailureRecord, write_failure

from confidence.estimator import FOUR_CONFIDENCE_FIELDS
from evidence.collectors.deep_learning_specialist.lookup import REPO, RegistryError, lookup_model
from evidence.item import SCHEMA_VERSION, clock
from evidence.registry.writer import read_rows
from evidence.validation.validate import _load_item
from fusion.interface import safe_raw

MODULE_ID = "MOD012"
DEFAULT_FORMATS = ("json", "markdown", "html")
_FORBIDDEN_INPUT_KEYS = ("image", "image_path", "image_bytes", "stored_path", "file_path", "bytes", "model", "weights")


@dataclass(frozen=True)
class VersionStamps:
    system_version: str
    model_id: str
    model_version: str
    dataset_id: str
    experiment_id: str
    git_commit: str

    def to_json(self) -> dict[str, str]:
        return {
            "system_version": self.system_version,
            "model_id": self.model_id,
            "model_version": self.model_version,
            "dataset_id": self.dataset_id,
            "experiment_id": self.experiment_id,
            "git_commit": self.git_commit,
        }


@dataclass
class CaseReport:
    case_id: str
    module_id: str
    input_summary: dict
    evidence_summary: list[dict]
    model_results: dict
    decision: dict
    confidence: dict
    reasoning: dict
    explanation: dict
    limitations: list[str]
    recommendations: list[str]
    execution_stats: dict
    version_stamps: VersionStamps
    timestamp: str

    def to_json(self) -> dict:
        return {
            "case_id": self.case_id,
            "module_id": self.module_id,
            "input_summary": dict(self.input_summary),
            "evidence_summary": list(self.evidence_summary),
            "model_results": dict(self.model_results),
            "decision": dict(self.decision),
            "confidence": dict(self.confidence),
            "reasoning": dict(self.reasoning),
            "explanation": dict(self.explanation),
            "limitations": list(self.limitations),
            "recommendations": list(self.recommendations),
            "execution_stats": dict(self.execution_stats),
            "version_stamps": self.version_stamps.to_json(),
            "timestamp": self.timestamp,
        }


@dataclass
class ReportResult:
    report: CaseReport | None = None
    json_path: Path | None = None
    markdown_path: Path | None = None
    html_path: Path | None = None
    failures: list[FailureRecord] = field(default_factory=list)


def resolve_git_commit(repo_root: Path = REPO) -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=str(repo_root),
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5,
        )
        return out.strip()
    except Exception:
        return ""


def resolve_version_stamps(
    model_id: str,
    *,
    system_version: str = SCHEMA_VERSION,
    git_commit: str | None = None,
    repo_root: Path = REPO,
) -> VersionStamps:
    import csv

    reg_path = repo_root / "05_Models" / "model_registry.csv"
    row_match: dict[str, str] | None = None
    if reg_path.is_file():
        with reg_path.open(encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            header = [name.strip() for name in next(reader, [])]
            for r in reader:
                if r:
                    d = {header[i]: val.strip() for i, val in enumerate(r)}
                    if d.get("Model ID") == model_id:
                        row_match = d
                        break
    if row_match is None:
        raise RegistryError(f"{model_id} is not in {reg_path}")
    commit = git_commit if git_commit is not None else (resolve_git_commit(repo_root) or row_match.get("Git Commit", ""))
    return VersionStamps(
        system_version=system_version,
        model_id=row_match.get("Model ID", model_id),
        model_version=row_match.get("Version", "1.0"),
        dataset_id=row_match.get("Dataset", ""),
        experiment_id=row_match.get("Experiment", ""),
        git_commit=commit,
    )


def _coerce_version_stamps(
    version_stamps: VersionStamps | dict | None,
    *,
    model_id: str = "MODEL0001",
    repo_root: Path = REPO,
) -> VersionStamps:
    if isinstance(version_stamps, VersionStamps):
        return version_stamps
    if isinstance(version_stamps, dict):
        return VersionStamps(
            system_version=str(version_stamps.get("system_version") or "").strip(),
            model_id=str(version_stamps.get("model_id") or "").strip(),
            model_version=str(version_stamps.get("model_version") or "1.0").strip(),
            dataset_id=str(version_stamps.get("dataset_id") or "").strip(),
            experiment_id=str(version_stamps.get("experiment_id") or "").strip(),
            git_commit=str(version_stamps.get("git_commit") or "").strip(),
        )
    return resolve_version_stamps(model_id, repo_root=repo_root)


def _fmt_conf(val: object) -> str:
    if val is None or val == "":
        return "empty (null)"
    if isinstance(val, (int, float)):
        return f"{float(val):.4f}"
    return str(val)


def _render_markdown(report: CaseReport) -> str:
    stamps = report.version_stamps
    inp = report.input_summary
    dec = report.decision
    conf = report.confidence
    ev_ids = ", ".join(item["evidence_id"] for item in report.evidence_summary) or "none"
    ev_lines = "; ".join(
        f"{item['evidence_id']} ({item['evidence_type']}, quality={item['quality']}, status={item['status']})"
        for item in report.evidence_summary
    )
    mod_res = report.model_results
    if mod_res.get("evidence_id"):
        mod_text = (
            f"evidence_id={mod_res['evidence_id']}, model_id={mod_res['model_id']}, "
            f"probability={mod_res['probability']}, threshold={mod_res['threshold']}"
        )
    else:
        mod_text = "No validated deep_learning_prediction evidence item recorded."
    conf_text = ", ".join(f"{k}={_fmt_conf(conf.get(k))}" for k in FOUR_CONFIDENCE_FIELDS)
    reas_text = report.reasoning.get("narrative") or "No reasoning sentences recorded."
    expl_methods = report.explanation.get("methods", [])
    expl_text = "; ".join(
        f"{m['method']}={m['status']}" + (f" ({m['evidence_id']})" if m.get("evidence_id") else "")
        for m in expl_methods
    ) or "no_data"
    lim_text = "; ".join(report.limitations)
    rec_text = "; ".join(report.recommendations)
    stats = report.execution_stats
    stats_text = (
        f"execution_time_seconds={stats.get('execution_time_seconds')}, "
        f"evidence_count={stats.get('evidence_count')}, "
        f"error_count={stats.get('error_count')}, warning_count={stats.get('warning_count')}"
    )
    return (
        f"# Case Report: {report.case_id}\n\n"
        f"**Input Summary:** input_id={inp.get('input_id')}, intake_status={inp.get('intake_status')}, "
        f"validation_status={inp.get('validation_status')}\n"
        f"**Evidence:** {ev_ids} — {ev_lines}\n"
        f"**Model Results:** {mod_text}\n"
        f"**Decision:** {dec.get('decision')} (rule_id={dec.get('rule_id')}, strategy_id={dec.get('strategy_id')}, "
        f"fused_evidence_id={dec.get('fused_evidence_id')}, confidence_evidence_id={dec.get('confidence_evidence_id')}, "
        f"reasoning_path={';'.join(dec.get('reasoning_path', []))})\n"
        f"**Confidence:** {conf_text} (formula_id={conf.get('formula_id')})\n"
        f"**Reasoning:** {reas_text}\n"
        f"**Explanation:** {expl_text}\n"
        f"**Limitations:** {lim_text}\n"
        f"**Recommendations:** {rec_text}\n"
        f"**Execution Stats:** {stats_text}\n"
        f"**System Version:** {stamps.system_version} (git_commit={stamps.git_commit})\n"
        f"**Model Version:** {stamps.model_id} v{stamps.model_version} "
        f"(experiment_id={stamps.experiment_id}, dataset_id={stamps.dataset_id})\n"
    )


def _render_html(report: CaseReport, markdown_text: str) -> str:
    escaped_body = html.escape(markdown_text)
    return (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head><meta charset=\"utf-8\"><title>"
        f"Case Report: {html.escape(report.case_id)}"
        "</title></head>\n"
        f"<body><pre>{escaped_body}</pre></body>\n"
        "</html>\n"
    )


def generate_report(
    registry_path: Path,
    *,
    case_id: str,
    decision_path: Path | None = None,
    explanation_path: Path | None = None,
    reasoning_path: Path | None = None,
    input_dir: Path | None = None,
    evidence_ids: list[str] | None = None,
    version_stamps: VersionStamps | dict | None = None,
    execution_stats: dict | None = None,
    formats: tuple[str, ...] = DEFAULT_FORMATS,
    storage_root: Path | None = None,
    output_dir: Path | None = None,
    repo_root: Path = REPO,
    **forbidden_kwargs: object,
) -> ReportResult:
    """Generate the reproducible case report in JSON, Markdown (Template 24), and HTML."""

    result = ReportResult()

    def fail(detail: str) -> ReportResult:
        result.failures.append(_failure(storage_root, case_id, detail))
        return result

    if forbidden_kwargs:
        bad = ", ".join(sorted(forbidden_kwargs))
        if any(any(tok in key.lower() for tok in _FORBIDDEN_INPUT_KEYS) for key in forbidden_kwargs):
            return fail(f"MOD012 forbids image or model inputs ({bad})")
        return fail(f"unexpected arguments to MOD012 ({bad})")

    case_dir = storage_root / case_id if storage_root is not None else None
    dec_file = decision_path or (case_dir / "decision.json" if case_dir is not None else None)
    if dec_file is None or not dec_file.is_file():
        return fail("decision.json is missing; report cannot be generated")
    try:
        dec_payload = json.loads(dec_file.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return fail(f"decision.json could not be read: {exc}")

    if dec_payload.get("case_id") != case_id or not dec_payload.get("decision"):
        return fail("decision.json is missing case_id or decision")

    expl_file = explanation_path or (case_dir / "explanation.json" if case_dir is not None else None)
    if expl_file is None or not expl_file.is_file():
        return fail("explanation.json is missing; report cannot be generated")
    try:
        expl_payload = json.loads(expl_file.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return fail(f"explanation.json could not be read: {exc}")

    reas_file = reasoning_path or (case_dir / "reasoning.json" if case_dir is not None else None)
    if reas_file is None or not reas_file.is_file():
        return fail("reasoning.json is missing; report cannot be generated")
    try:
        reas_payload = json.loads(reas_file.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return fail(f"reasoning.json could not be read: {exc}")

    try:
        rows = read_rows(registry_path)
    except (OSError, ValueError) as exc:
        return fail(f"evidence registry could not be read: {exc}")
    by_id = {row["Evidence ID"]: row for row in rows}

    cited_ids: list[str] = []
    source_list = (
        list(evidence_ids)
        if evidence_ids is not None
        else [
            *dec_payload.get("reasoning_path", []),
            dec_payload.get("fused_evidence_id", ""),
            dec_payload.get("confidence_evidence_id", ""),
            *expl_payload.get("supporting_ids", []),
            *reas_payload.get("reasoning_path", []),
        ]
    )
    for ev_id in source_list:
        if not ev_id:
            continue
        if ev_id not in by_id:
            return fail(f"evidence id {ev_id!r} is not in evidence_registry.csv")
        if ev_id not in cited_ids:
            cited_ids.append(ev_id)

    if not cited_ids:
        return fail("no registered evidence ids cited for report")

    evidence_summary: list[dict] = []
    detector_item: dict | None = None
    conf_item_loaded: dict | None = None
    fused_item_loaded: dict | None = None

    for ev_id in cited_ids:
        loaded = _load_item(by_id[ev_id])
        loaded["raw_output"] = safe_raw(loaded["raw_output"])
        evidence_summary.append(
            {
                "evidence_id": loaded["evidence_id"],
                "evidence_type": loaded["evidence_type"],
                "source_module": loaded["source_module"],
                "quality": loaded["quality"],
                "status": loaded["status"],
                "confidence": loaded["confidence"],
                "description": loaded["description"],
                "dependencies": list(loaded["dependencies"]),
            }
        )
        if loaded["evidence_type"] == "deep_learning_prediction" and loaded["source_module"] == "MOD006":
            detector_item = loaded
        elif loaded["evidence_type"] == "confidence" and loaded["source_module"] == "MOD006":
            conf_item_loaded = loaded
        elif loaded["evidence_type"] == "fused_conclusion" and loaded["source_module"] == "MOD006":
            fused_item_loaded = loaded

    inferred_model_id = (
        str(detector_item["processed_output"].get("model_id") or detector_item["raw_output"].get("model_id") or "MODEL0001")
        if detector_item is not None
        else "MODEL0001"
    )
    try:
        stamps = _coerce_version_stamps(version_stamps, model_id=inferred_model_id, repo_root=repo_root)
    except RegistryError as exc:
        return fail(f"version stamps could not be resolved: {exc}")

    missing_stamps = [
        name
        for name, val in stamps.to_json().items()
        if not val or not str(val).strip()
    ]
    if missing_stamps:
        return fail(f"missing required version stamp(s): {', '.join(missing_stamps)}")

    # Input summary from recorded MOD001/MOD002 JSON files (no image read)
    resolved_input_dir = input_dir
    if resolved_input_dir is None and case_dir is not None and case_dir.is_dir():
        candidates = sorted(path for path in case_dir.glob(f"{case_id}-input-*") if path.is_dir())
        if candidates:
            resolved_input_dir = candidates[-1]

    input_summary = {
        "input_id": f"{case_id}-input-01",
        "intake_status": "accepted",
        "validation_status": "passed",
    }
    if resolved_input_dir is not None:
        meta_file = resolved_input_dir / "input_metadata.json"
        val_file = resolved_input_dir / "validation.json"
        if meta_file.is_file():
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            input_summary["input_id"] = meta.get("input_id", input_summary["input_id"])
            input_summary["intake_status"] = meta.get("status", input_summary["intake_status"])
            input_summary["declared_format"] = meta.get("declared_format")
            input_summary["byte_size"] = meta.get("byte_size")
        if val_file.is_file():
            val_data = json.loads(val_file.read_text(encoding="utf-8"))
            input_summary["validation_status"] = val_data.get("status", input_summary["validation_status"])

    if detector_item is not None:
        model_results = {
            "evidence_id": detector_item["evidence_id"],
            "collector_evidence_id": detector_item["raw_output"].get("collector_evidence_id"),
            "model_id": detector_item["processed_output"].get("model_id") or stamps.model_id,
            "probability": detector_item["processed_output"].get("value"),
            "threshold": detector_item["processed_output"].get("threshold"),
            "quality": detector_item["quality"],
        }
    else:
        model_results = {
            "evidence_id": None,
            "collector_evidence_id": None,
            "model_id": stamps.model_id,
            "probability": None,
            "threshold": None,
            "quality": None,
        }

    meta_dec = dec_payload.get("decision_metadata", {})
    conf_from_dec = meta_dec.get("confidence", {})
    conf_proc = conf_item_loaded["processed_output"] if conf_item_loaded is not None else {}
    confidence_section = {
        "evidence_id": dec_payload.get("confidence_evidence_id"),
        "formula_id": conf_proc.get("formula_id", "e4_calibrated_v1"),
        **{name: conf_proc.get(name, conf_from_dec.get(name)) for name in FOUR_CONFIDENCE_FIELDS},
    }

    limitations: list[str] = []
    for name in FOUR_CONFIDENCE_FIELDS:
        if confidence_section.get(name) is None:
            limitations.append(f"{name} is empty (null) and was not estimated.")
    for item in evidence_summary:
        if item["confidence"] is None:
            limitations.append(f"Evidence {item['evidence_id']} ({item['evidence_type']}) has an empty (null) collector confidence.")
        if item["quality"] in ("low", "unusable"):
            limitations.append(f"Evidence {item['evidence_id']} ({item['evidence_type']}) has reliability quality={item['quality']}.")
    if fused_item_loaded is not None:
        f_sum = fused_item_loaded["processed_output"].get("summary", {})
        if isinstance(f_sum, dict) and f_sum.get("single_source"):
            limitations.append("Directional fusion is single-source (only one directional specialist contributed).")
    limitations.append(
        "Detector baseline (MODEL0001) exhibits elevated false-positive rates under heavy blur/JPEG compression (E7) and cross-dataset domain shift (E8), and reduced recall on held-out diffusion generators (E9)."
    )

    decision_word = str(dec_payload.get("decision"))
    recommendations: list[str] = []
    if decision_word in ("Inconclusive", "Unknown"):
        recommendations.append(
            f"Decision is {decision_word}; do not treat this case as a confirmed Real or Fake verdict without additional independent forensic evidence."
        )
    else:
        recommendations.append(
            f"Review the cited evidence IDs ({', '.join(dec_payload.get('reasoning_path', []))}) alongside the limitations above; softmax probability is not standalone proof."
        )

    stats_section = {
        "execution_time_seconds": (execution_stats or {}).get("execution_time_seconds", 0.0),
        "evidence_count": len(evidence_summary),
        "error_count": (execution_stats or {}).get("error_count", 0),
        "warning_count": (execution_stats or {}).get("warning_count", len(meta_dec.get("warning_failure_ids", []))),
    }

    stamp = clock()
    report = CaseReport(
        case_id=case_id,
        module_id=MODULE_ID,
        input_summary=input_summary,
        evidence_summary=evidence_summary,
        model_results=model_results,
        decision={
            "decision": decision_word,
            "fused_evidence_id": dec_payload.get("fused_evidence_id"),
            "confidence_evidence_id": dec_payload.get("confidence_evidence_id"),
            "reasoning_path": list(dec_payload.get("reasoning_path", [])),
            "strategy_id": meta_dec.get("strategy_id"),
            "rule_id": meta_dec.get("rule_id"),
            "warning_failure_ids": list(meta_dec.get("warning_failure_ids", [])),
        },
        confidence=confidence_section,
        reasoning={
            "reasoning_path": list(reas_payload.get("reasoning_path", [])),
            "narrative": reas_payload.get("narrative", ""),
            "sentences": list(reas_payload.get("sentences", [])),
        },
        explanation={
            "figure_policy": expl_payload.get("figure_policy"),
            "methods": list(expl_payload.get("methods", [])),
            "supporting_ids": list(expl_payload.get("supporting_ids", [])),
        },
        limitations=limitations,
        recommendations=recommendations,
        execution_stats=stats_section,
        version_stamps=stamps,
        timestamp=stamp,
    )

    target_dir = output_dir or (case_dir / "reports" if case_dir is not None else None)
    md_text = _render_markdown(report)
    if target_dir is not None:
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            if "json" in formats:
                j_path = target_dir / f"{case_id}_report.json"
                j_path.write_text(json.dumps(report.to_json(), indent=2) + "\n", encoding="utf-8")
                result.json_path = j_path
            if "markdown" in formats:
                m_path = target_dir / f"{case_id}_report.md"
                m_path.write_text(md_text, encoding="utf-8")
                result.markdown_path = m_path
            if "html" in formats:
                h_path = target_dir / f"{case_id}_report.html"
                h_path.write_text(_render_html(report, md_text), encoding="utf-8")
                result.html_path = h_path
        except OSError as exc:
            return fail(f"report files could not be written: {exc}")

    result.report = report
    return result


def _failure(storage_root: Path | None, case_id: str, detail: str) -> FailureRecord:
    if storage_root is None:
        return FailureRecord("", "unexpected_error", "unexpected_error", MODULE_ID, case_id, None, detail, "")
    return write_failure(storage_root, name="unexpected_error", module_id=MODULE_ID, case_id=case_id, detail=detail)
