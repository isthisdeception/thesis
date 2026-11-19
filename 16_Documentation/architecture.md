# System Architecture — AI Digital Forensics & AI Forensic Analyst

**Version:** `0.1.0`  
**Date:** 2026-11-19  
**Governing Policies:** See [MASTER_RESEARCH_OPERATING_SYSTEM.md](../MASTER_RESEARCH_OPERATING_SYSTEM.md) (§1.12, §2, §7–§8, Appendix A) — this document synthesizes the implemented architecture and links to specs and registries without duplicating handbook policy text.  
**Visual Diagrams:** [system_architecture.md](./workflow_diagrams/system_architecture.md) · [forensic_pipeline.md](./workflow_diagrams/forensic_pipeline.md)

---

## 1. Architectural Overview (Three-Tier Separation)

The platform separates interactive presentation, HTTP orchestration, and forensic investigation across three strict boundaries ([§8.1](../MASTER_RESEARCH_OPERATING_SYSTEM.md)):

| Tier | Folder | Runtime Stack | Strict Responsibility | Forbidden |
|---|---|---|---|---|
| **Frontend UI** | `12_Web/` | React `18.3`, Vite `6.0`, Tailwind CSS `3.4`, React Router `6.28` | Presents 14 pages (`MOD014`), polls stage status, visualizes 4 decisions + 4 confidence values + `EV` records | No inference, no threshold logic, no `fetch()` outside `src/api/` |
| **REST Backend** | `13_Backend/` | Django `5.2.19`, Django REST Framework `3.18.3`, `django-cors-headers` `4.9.0` | Exposes 10 REST endpoints (`MOD013`), manages per-case jobs, wraps `run_investigation()`, serves unchanged records | No duplicated detection/fusion/decision logic; no stack traces in responses |
| **Forensic Core** | `11_AI_Forensic_System/` | Python (`3.12`/`3.13`), Pillow, optional PyTorch/FastAI model weights | Executes `MOD001`–`MOD018`: upload intake, validation, 10 evidence collectors, fusion, E4 confidence, decision, explainability, reasoning, report, audit | Never hides uncertainty or alters collector evidence rows |

Canonical tier specifications:
- Forensic Analyst specification: [11_AI_Forensic_System/architecture.md](../11_AI_Forensic_System/architecture.md)
- Backend & API specification: [13_Backend/architecture.md](../13_Backend/architecture.md) & [api_spec.md](../13_Backend/api_spec/api_spec.md)
- Frontend & API client specification: [12_Web/architecture.md](../12_Web/architecture.md) & [api_client_spec.md](../12_Web/api_client_spec.md)
- Cross-tier integration guide: [integration_guide.md](./integration_guide.md)

---

## 2. The Eighteen-Module Forensic Pipeline (`MOD001`–`MOD018`)

All 18 modules are tracked as `implemented` (`v0.1.0`) in [11_AI_Forensic_System/module_registry.csv](../11_AI_Forensic_System/module_registry.csv) and orchestrated by `run_investigation()` in [11_AI_Forensic_System/pipeline.py](../11_AI_Forensic_System/pipeline.py).

| Stage / Group | Modules | Role in Investigation |
|---|---|---|
| **Intake & Validation Gate** | `MOD001`, `MOD002` | `MOD001` stores valid uploads (`jpg`, `jpeg`, `png`, `webp`, non-empty, `<= 20 MB`) as `{case_id}-input-{seq}` and drops invalid files before persistence. `MOD002` verifies decoding, dimensions/channels, and single-face availability before collectors run. |
| **Independent Evidence Acquisition** | `MOD003`, `MOD004` | `MOD003` runs 9 non-calling collectors (`image_statistics`, `metadata`, `face_detection`, `face_quality`, `frequency_domain`, `compression_artifacts`, `color_distribution`, `texture_analysis`, `explainability_input`). `MOD004` invokes the registered detector (`MODEL0001`, frozen threshold `0.395057`) to emit raw `P(fake)` and optional embeddings — or records `model_unavailable` if no export is configured. |
| **Evidence Ledger & Reliability** | `MOD005`, `MOD006` | `MOD005` assigns immutable `EVxxxxxx` IDs in [evidence_registry.csv](../11_AI_Forensic_System/evidence_registry.csv). `MOD006` appends non-destructive reliability rows (`high`, `medium`, `low`, `unusable`) and cross-cites conflicting items. |
| **Evidence Fusion** | `MOD007` | Combines validated evidence via pluggable `FusionStrategy` (configured in `fusion/fusion_config.json` as `rule_based`, approved in [DEC0009](../01_Project_Management/decision_log/DEC0009.md)) into `fused_conclusion` (`lean`: `positive_class`, `negative_class`, `contested`, `no_directional_evidence`). |
| **Confidence & Case Decision** | `MOD009`, `MOD008` | `MOD009` computes four distinct metrics (`prediction_confidence`, `evidence_confidence`, `system_confidence`, `decision_confidence`, approved in [DEC0010](../01_Project_Management/decision_log/DEC0010.md)). `MOD008` reads only the validated `fused_conclusion` and `confidence` `EV` IDs and emits `Real`, `Fake`, `Inconclusive`, or `Unknown` (`decision.json`). |
| **Explainability, Reasoning & Reports** | `MOD010`, `MOD011`, `MOD012` | `MOD010` writes data-only `explanation.json` (`grad_cam`, `attention_maps`, `saliency`, `integrated_gradients`, `no_data` if unavailable per [Policy A.9](../MASTER_RESEARCH_OPERATING_SYSTEM.md#a9-canonical-figure-policy)). `MOD011` generates `reasoning.json` with verified `EV` ID citations. `MOD012` writes JSON, Markdown (Template 24), and HTML reports stamped with model, dataset, experiment, and Git commit SHA. |
| **Transport & UI** | `MOD013`, `MOD014` | `MOD013` exposes the 10-endpoint DRF API (`13_Backend/apps/api/`). `MOD014` renders the 9 live polling stages (`Uploading` → `Complete`) and multi-page forensic workspace (`12_Web/src/pages/`). |
| **Audit, Failures & Registry Governance** | `MOD015`, `MOD016`, `MOD017`, `MOD018` | `MOD015` appends immutable `CASExxxxxx` rows to [case_registry.csv](../11_AI_Forensic_System/case_registry.csv). `MOD016` structures all 8 canonical failures (`unsupported_format`, `corrupted_image`, `no_face`, `multiple_faces`, `model_unavailable`, `low_confidence`, `timeout`, `unexpected_error`). `MOD017` validates `module_registry.csv` and specs; `MOD018` governs new modalities via `EvidenceCollector` and `FusionStrategy`. |

---

## 3. Core Architectural Invariants

1. **The detector never decides:** `MOD004` outputs raw probabilities and metadata only; only `MOD008` assigns `Real`, `Fake`, `Inconclusive`, or `Unknown`.
2. **Decision isolation:** `MOD008` never touches image bytes or file paths; it reads only validated `fused_conclusion` and `confidence` `EV` IDs.
3. **Uncertainty & conflict preservation:** Null confidence remains `null` (`Empty (not estimated)` in UI); low-quality or conflicting evidence stays in `evidence_registry.csv` and routes decisions to `Inconclusive` or `Unknown`.
4. **Thread-safe backend execution:** `13_Backend/apps/forensic_engine/service.py` serializes `run_investigation()` calls under `_PIPELINE_LOCK` when running asynchronous worker jobs (`FORENSIC_ASYNC_MODE=thread`) so shared CSV registries remain append-safe.
5. **Single source of provenance:** `GET /api/v1/version` and `MOD012` reports pull model, dataset, and experiment lineage dynamically from [model_registry.csv](../05_Models/model_registry.csv) and Git HEAD.

---

## 4. Linked Registries, Decision Logs & Audit Gates

| Artifact | Purpose | Location |
|---|---|---|
| Experiment Registry | Authoritative record of training & ablation runs (`EXP0001`–`EXP0006`) | [06_Experiments/experiment_registry.csv](../06_Experiments/experiment_registry.csv) |
| Model Registry | Model checkpoints, metrics, and export pointers (`MODEL0001`, `MODEL0008`–`MODEL0012`) | [05_Models/model_registry.csv](../05_Models/model_registry.csv) |
| Decision Logs | Human-approved scientific & architectural choices (`DEC0001`–`DEC0010`) | [01_Project_Management/decision_log/](../01_Project_Management/decision_log/) |
| Forensic Gate Audit (Checklist 9) | Phase E14 (`EVAL0007`) & Checklist 9 PASS | [08_Evaluation/forensic_audit.md](../08_Evaluation/forensic_audit.md) |
| Backend Gate Audit (Checklist 11) | REST API & backend separation-of-concerns PASS | [13_Backend/backend_audit.md](../13_Backend/backend_audit.md) |
| Frontend Gate Audit (Checklist 10) | 14 pages, 24 components, `MOD014` PASS | [12_Web/frontend_audit.md](../12_Web/frontend_audit.md) |
| Documentation Gate Audit (Checklist 12) | Documentation completeness & consistency PASS | [documentation_audit.md](./documentation_audit.md) |
