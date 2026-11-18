# 11_AI_Forensic_System

**Purpose:** The AI Forensic Analyst source.

## Contents
Module specs, the shared interfaces, and the module registry. Implementation begins at STEP-052.

STEP-051 (2026-11-17): `architecture.md` states the pipeline and the invariants. `specs/MOD001_spec.md` through `specs/MOD018_spec.md` are the module specs. `specs/interfaces.md` defines `EvidenceCollector`, `FusionStrategy`, and the evidence item tied to `EV` ids. `module_registry.csv` lists MOD001–MOD018.

STEP-052: `input_management/` receives one upload and writes `input_metadata.json` (`input_management/input_metadata_schema.md`). `image_validation/` measures the stored file and stops on a structured failure from `failure_handling/`. MOD001 and MOD002 are `implemented` in the registry. Tests: `python -m pytest tests/test_input_validation.py` from this folder.

STEP-053: `evidence/collectors/` holds image statistics, metadata, face detection, face quality, frequency, compression, color, texture, and explainability input. `evidence/layer.py` runs the configured list after a passed validation. MOD003 is `implemented`. Tests: `python -m pytest tests/test_collectors.py` from this folder.

STEP-054: `evidence/collectors/deep_learning_specialist/` loads the detector named by `model_id`. The export pointer comes from `05_Models/model_registry.csv`. The evidence item carries the probability and the run time. The threshold is recorded and not applied. MOD004 is `implemented`. Tests: `python -m pytest tests/test_deep_learning_specialist.py` from this folder.

STEP-055: `evidence/registry/` appends `EVxxxxxx` rows. `evidence/validation/` appends a reliability row for each item and does not rewrite the collector row. MOD005 and MOD006 are `implemented`. The checked-in `evidence_registry.csv` stays a header until a case is run. Tests: `python -m pytest tests/test_evidence_registry.py` from this folder.

STEP-056: `fusion/` fuses MOD006 rows into one `fused_conclusion` item through the strategy named in `fusion/fusion_config.json` (`rule_based`; table approved in DEC0009). An unknown strategy id writes a MOD016 failure and no item. The summary is a lean with rationale citing `EV` ids, not a decision. MOD007 is `implemented`. See `fusion/README.md`. Tests: `python -m pytest tests/test_fusion.py` from this folder.

STEP-057: `confidence/` computes the four E4-calibrated confidence values (`prediction_confidence`, `evidence_confidence`, `system_confidence`, `decision_confidence`, formula `e4_calibrated_v1` in `confidence/confidence_config.json`, approved in DEC0010) and registers a `confidence` item through MOD005 and MOD006. `decision/` reads only the validated `fused_conclusion` `EV` id and the validated `confidence` `EV` id—never the image—and writes `decision.json` (`Real`, `Fake`, `Inconclusive`, or `Unknown` with `reasoning_path`). MOD008 and MOD009 are `implemented`. See `confidence/README.md` and `decision/README.md`. Tests: `python -m pytest tests/test_decision_confidence.py` from this folder.

STEP-058: `explainability/` assembles data-only `explanation.json` from validated `explainability_input` items (`grad_cam`, `attention_maps`, `saliency`, `integrated_gradients`), recording `"no_data"` (`data: null`) when no map was collected and rejecting any rendered image (A.9). `reasoning/` writes `reasoning.json` from validated evidence rows, verifying that every sentence cites an input `EV` id and states only measurements present on that row. MOD010 and MOD011 are `implemented`. See `explainability/README.md` and `reasoning/README.md`. Tests: `python -m pytest tests/test_explainability_reasoning.py` from this folder.

STEP-059: `reports/` generates reproducible JSON, Markdown (Template 24), and HTML case reports with byte-for-byte system/model/dataset/experiment/Git-commit provenance. `audit/` appends immutable `CASExxxxxx` rows to `case_registry.csv`. `failure_handling/` writes, reads, and classifies structured failure records across all 8 canonical failure names. `system_registry/` verifies `MOD001`–`MOD018` specs and modality proposals. `pipeline.py` (`run_investigation`) runs the end-to-end investigation. `evaluate_e14.py` produces Phase E14 (`EVAL0007`) in `08_Evaluation/forensic_analyst_eval/` and Checklist 9 audit in `08_Evaluation/forensic_audit.md`. MOD012 and MOD015–MOD018 are `implemented` (MOD013 API and MOD014 Frontend belong to Parts 10–11). Tests: `python -m pytest tests/test_report_audit_pipeline.py` from this folder.

## Workflow
Antigravity writes, Backend consumes. No frontend/training code.

## Owner
Antigravity

## Related Folders
13_Backend, 08_Evaluation

## Expected Outputs
module_registry.csv, module source files

> *This folder follows the canonical repository hygiene and naming rules defined in `MASTER_RESEARCH_OPERATING_SYSTEM.md`. Please refer to the handbook for full policy details.*

## Cross-Linked Agents

The following agents operate within this domain:
- [Input](../../19_Prompts/agents/forensic/input.md)
- [Validation](../../19_Prompts/agents/forensic/validation.md)
- [Evidence](../../19_Prompts/agents/forensic/evidence.md)
- [Fusion](../../19_Prompts/agents/forensic/fusion.md)
- [Decision](../../19_Prompts/agents/forensic/decision.md)
- [Explanation](../../19_Prompts/agents/forensic/explanation.md)
- [Report](../../19_Prompts/agents/forensic/report.md)
- [Audit](../../19_Prompts/agents/forensic/audit.md)
- [API](../../19_Prompts/agents/forensic/api.md)
