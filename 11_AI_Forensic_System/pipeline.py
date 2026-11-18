"""End-to-end AI Forensic Analyst pipeline entrypoint (MOD001..MOD012, MOD015, MOD016)."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path

from audit import CaseRow, append_case_row, next_case_id
from confidence import ConfidenceResult, estimate_confidence
from decision import DecisionResult, decide_case
from evidence.collectors import builtin_collectors
from evidence.collectors.deep_learning_specialist import DeepLearningCollector
from evidence.collectors.deep_learning_specialist.collector import Predictor
from evidence.collectors.deep_learning_specialist.lookup import REPO
from evidence.item import SCHEMA_VERSION, EvidenceCollector
from evidence.layer import CollectionResult, run_collectors
from evidence.registry import register
from evidence.registry.writer import RegisterResult
from evidence.validation import ValidationConfig as EvidenceValidationConfig
from evidence.validation import validate_items
from evidence.validation.validate import ValidationResult as EvidenceValidationResult
from explainability import ExplanationResult, assemble_explanation
from failure_handling import FailureRecord, classify_failures, read_case_failures
from fusion import FusionResult, fuse_case
from image_validation import FaceCounter, ValidationConfig as ImageValidationConfig
from image_validation import ValidationResult as ImageValidationResult
from image_validation import validate_stored_input
from input_management import IntakeConfig, IntakeResult, receive_upload
from reasoning import ReasoningResult, compose_reasoning
from reports import ReportResult, VersionStamps, generate_report

PROGRESS_STAGES = (
    "Uploading",
    "Validating",
    "Detecting Face",
    "Running Analysis",
    "Collecting Evidence",
    "Evaluating Confidence",
    "Generating Explanation",
    "Preparing Report",
    "Complete",
)


@dataclass
class InvestigationResult:
    case_id: str
    status: str  # "completed" | "failed"
    stage_history: list[str] = field(default_factory=list)
    intake: IntakeResult | None = None
    image_validation: ImageValidationResult | None = None
    collection: CollectionResult | None = None
    registered: RegisterResult | None = None
    validated_evidence: EvidenceValidationResult | None = None
    fusion: FusionResult | None = None
    confidence: ConfidenceResult | None = None
    decision: DecisionResult | None = None
    explanation: ExplanationResult | None = None
    reasoning: ReasoningResult | None = None
    report: ReportResult | None = None
    case_row: CaseRow | None = None
    failures: list[FailureRecord] = field(default_factory=list)
    execution_time_seconds: float = 0.0


def run_investigation(
    *,
    filename: str,
    data: bytes,
    storage_root: Path,
    evidence_registry_path: Path,
    case_registry_path: Path,
    face_counter: FaceCounter,
    case_id: str = "",
    model_id: str = "MODEL0001",
    predictor: Predictor | None = None,
    artifact_root: Path | None = None,
    detector_timeout_seconds: float | None = None,
    extra_collectors: list[EvidenceCollector] | None = None,
    collectors_override: list[EvidenceCollector] | None = None,
    strategy_id: str | None = None,
    intake_config: IntakeConfig | None = None,
    image_validation_config: ImageValidationConfig | None = None,
    evidence_validation_config: EvidenceValidationConfig | None = None,
    version_stamps: VersionStamps | dict | None = None,
    configuration_id: str = "rule_based/e4_calibrated_v1",
    repo_root: Path = REPO,
) -> InvestigationResult:
    """Run one forensic investigation end-to-end and append the immutable case audit row."""

    started = time.perf_counter()
    resolved_case_id = case_id or next_case_id(case_registry_path)
    out = InvestigationResult(case_id=resolved_case_id, status="failed")

    def finalize_failed(input_id: str = "", ev_ids: list[str] | None = None) -> InvestigationResult:
        elapsed = time.perf_counter() - started
        out.execution_time_seconds = elapsed
        all_failures = read_case_failures(storage_root, resolved_case_id)
        out.failures = all_failures
        err_ids, warn_ids = classify_failures(all_failures)
        audit_res = append_case_row(
            case_registry_path,
            case_id=resolved_case_id,
            input_id=input_id,
            evidence_ids=ev_ids or [],
            decision="",
            model_id=model_id,
            version=SCHEMA_VERSION,
            configuration=configuration_id,
            execution_time_seconds=elapsed,
            errors=err_ids,
            warnings=warn_ids,
            status="failed",
            storage_root=storage_root,
        )
        out.case_row = audit_res.row
        return out

    # 1. MOD001 — Input Management
    out.stage_history.append("Uploading")
    intake_res = receive_upload(
        case_id=resolved_case_id,
        filename=filename,
        data=data,
        storage_root=storage_root,
        config=intake_config,
    )
    out.intake = intake_res
    input_id = str(intake_res.metadata.get("input_id") or "")
    if not intake_res.accepted:
        return finalize_failed(input_id=input_id)

    input_dir = storage_root / resolved_case_id / input_id

    # 2. MOD002 — Image Validation (includes face gate)
    out.stage_history.append("Validating")
    out.stage_history.append("Detecting Face")
    img_val = validate_stored_input(
        input_dir,
        face_counter,
        storage_root=storage_root,
        config=image_validation_config,
    )
    out.image_validation = img_val
    if not img_val.passed:
        return finalize_failed(input_id=input_id)

    # 3. MOD003 + MOD004 — Evidence Collection & Deep Learning Specialist
    out.stage_history.append("Running Analysis")
    out.stage_history.append("Collecting Evidence")
    if collectors_override is not None:
        collector_list = list(collectors_override)
    else:
        collector_list = list(builtin_collectors(face_counter).values())
        collector_list.append(
            DeepLearningCollector(
                model_id,
                repo=repo_root,
                predictor=predictor,
                artifact_root=artifact_root,
                timeout_seconds=detector_timeout_seconds,
            )
        )
        if extra_collectors:
            collector_list.extend(extra_collectors)

    coll_res = run_collectors(input_dir, storage_root, collector_list)
    out.collection = coll_res

    # 4. MOD005 + MOD006 — Evidence Registration & Validation
    reg_res = register(
        coll_res.items,
        evidence_registry_path,
        storage_root=storage_root,
        case_id=resolved_case_id,
    )
    out.registered = reg_res
    collector_ev_ids = [item.evidence_id for item in reg_res.items if item.evidence_id]
    val_res = validate_items(
        evidence_registry_path,
        collector_ev_ids,
        storage_root=storage_root,
        case_id=resolved_case_id,
        config=evidence_validation_config,
    )
    out.validated_evidence = val_res
    validated_collector_ids = [item.evidence_id for item in val_res.items if item.evidence_id]

    # 5. MOD007 — Evidence Fusion
    prior_failures_before_conf = len(read_case_failures(storage_root, resolved_case_id))
    fus_res = fuse_case(
        evidence_registry_path,
        validated_collector_ids,
        case_id=resolved_case_id,
        strategy_id=strategy_id,
        storage_root=storage_root,
        validation_config=evidence_validation_config,
    )
    out.fusion = fus_res
    if fus_res.failures or fus_res.validated is None or fus_res.fused is None:
        return finalize_failed(input_id=input_id, ev_ids=[*collector_ev_ids, *validated_collector_ids])

    # 6. MOD009 — Confidence Estimation
    out.stage_history.append("Evaluating Confidence")
    conf_res = estimate_confidence(
        evidence_registry_path,
        [*validated_collector_ids, fus_res.validated.evidence_id],
        case_id=resolved_case_id,
        storage_root=storage_root,
        failure_count=prior_failures_before_conf,
        repo_root=repo_root,
        validation_config=evidence_validation_config,
    )
    out.confidence = conf_res
    if conf_res.failures or conf_res.validated is None or conf_res.confidence_item is None:
        return finalize_failed(
            input_id=input_id,
            ev_ids=[
                *collector_ev_ids,
                *validated_collector_ids,
                fus_res.fused.evidence_id,
                fus_res.validated.evidence_id,
            ],
        )

    all_case_ev_ids = [
        *collector_ev_ids,
        *validated_collector_ids,
        fus_res.fused.evidence_id,
        fus_res.validated.evidence_id,
        conf_res.confidence_item.evidence_id,
        conf_res.validated.evidence_id,
    ]
    validated_case_ev_ids = [
        *validated_collector_ids,
        fus_res.validated.evidence_id,
        conf_res.validated.evidence_id,
    ]

    # 7. MOD008 — Decision Engine
    dec_res = decide_case(
        evidence_registry_path,
        case_id=resolved_case_id,
        fused_evidence_id=fus_res.validated.evidence_id,
        confidence_evidence_id=conf_res.validated.evidence_id,
        storage_root=storage_root,
    )
    out.decision = dec_res
    if dec_res.failures or dec_res.record is None:
        return finalize_failed(input_id=input_id, ev_ids=all_case_ev_ids)

    # 8. MOD010 + MOD011 — Explainability & Forensic Reasoning
    out.stage_history.append("Generating Explanation")
    expl_res = assemble_explanation(
        evidence_registry_path,
        validated_collector_ids,
        case_id=resolved_case_id,
        storage_root=storage_root,
    )
    out.explanation = expl_res
    if expl_res.failures or expl_res.record is None:
        return finalize_failed(input_id=input_id, ev_ids=all_case_ev_ids)

    reas_res = compose_reasoning(
        evidence_registry_path,
        validated_case_ev_ids,
        case_id=resolved_case_id,
        storage_root=storage_root,
    )
    out.reasoning = reas_res
    if reas_res.failures or reas_res.record is None:
        return finalize_failed(input_id=input_id, ev_ids=all_case_ev_ids)

    # 9. MOD012 — Report Generator
    out.stage_history.append("Preparing Report")
    elapsed = time.perf_counter() - started
    all_failures = read_case_failures(storage_root, resolved_case_id)
    err_ids, warn_ids = classify_failures(all_failures)

    rep_res = generate_report(
        evidence_registry_path,
        case_id=resolved_case_id,
        input_dir=input_dir,
        evidence_ids=all_case_ev_ids,
        version_stamps=version_stamps,
        execution_stats={
            "execution_time_seconds": round(elapsed, 4),
            "error_count": len(err_ids),
            "warning_count": len(warn_ids),
        },
        storage_root=storage_root,
        repo_root=repo_root,
    )
    out.report = rep_res
    if rep_res.failures or rep_res.report is None:
        return finalize_failed(input_id=input_id, ev_ids=all_case_ev_ids)

    # 10. MOD015 — Audit Trail
    elapsed = time.perf_counter() - started
    out.execution_time_seconds = elapsed
    all_failures = read_case_failures(storage_root, resolved_case_id)
    out.failures = all_failures
    err_ids, warn_ids = classify_failures(all_failures)
    audit_res = append_case_row(
        case_registry_path,
        case_id=resolved_case_id,
        input_id=input_id,
        evidence_ids=all_case_ev_ids,
        decision=dec_res.record.decision,
        model_id=rep_res.report.version_stamps.model_id,
        version=rep_res.report.version_stamps.system_version,
        configuration=configuration_id,
        execution_time_seconds=elapsed,
        errors=err_ids,
        warnings=warn_ids,
        status="completed",
        storage_root=storage_root,
    )
    out.case_row = audit_res.row
    if audit_res.failures or audit_res.row is None:
        out.status = "failed"
        out.failures = read_case_failures(storage_root, resolved_case_id)
        return out

    out.stage_history.append("Complete")
    out.status = "completed"
    return out
