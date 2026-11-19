# Repository Folder Guide

**Version:** `0.1.0`  
**Date:** 2026-11-19  
**Canonical Policy:** Folder rules, allowed/forbidden contents, and storage tiers are governed by [§2 Repository Architecture](../MASTER_RESEARCH_OPERATING_SYSTEM.md#2-repository-architecture) and [Appendix A.6](../MASTER_RESEARCH_OPERATING_SYSTEM.md#a6-canonical-storage--synchronization-policy). Each top-level folder also carries its own local `README.md`.

---

## 1. Root Files & Environment

| Path | Role |
|---|---|
| [README.md](../README.md) | Top-level project overview, quick start, and navigation links |
| [MASTER_RESEARCH_OPERATING_SYSTEM.md](../MASTER_RESEARCH_OPERATING_SYSTEM.md) | Canonical governance handbook (methodology, naming, storage tiers, Checklists 1–20) |
| [PROJECT_EXECUTION_BLUEPRINT.md](../PROJECT_EXECUTION_BLUEPRINT.md) | Step-by-step execution plan (`STEP-001`–`STEP-078`) |
| [CONTRIBUTING.md](../CONTRIBUTING.md), [CHANGELOG.md](../CHANGELOG.md), [LICENSE](../LICENSE), [CODEOWNERS](../CODEOWNERS) | Governance, release history, MIT license, and ownership map |
| [environment/](../environment/) | Pinned Python/PyTorch/FastAI dependency locks (`requirements.txt`, `environment.yml`, `kaggle-requirements.txt`, `versions.lock.md`) |

---

## 2. Canonical Twenty-Folder Hierarchy

| Folder | Role | Key Artifacts Inside |
|---|---|---|
| `01_Project_Management/` | Governance, progress tracking, human decisions, risk ledger | [dashboard_status.md](../01_Project_Management/dashboard_status.md), `decision_log/DEC0001.md`–`DEC0010.md`, `milestones/`, `risk_register.csv`, `reviews/` |
| `02_Literature/` | Systematic literature review, gaps, and research claims | Screened paper records, summaries, claim database (`CLMxxxx`), research question docs |
| `03_Datasets/` | Dataset registry, checksums, splits (`SPLITxxxx`), and EDA specs | Registered `DS0001`–`DS0005` metadata and manifests (raw/processed media stored off-Git per A.6) |
| `04_Preprocessing/` | Deterministic, versioned preprocessing & split pipelines (`PP0001`–`PP0006`) | Face extraction, normalization, leakage-checked splitters, unit tests |
| `05_Models/` | Model architecture definitions and master Model Registry | [model_registry.csv](../05_Models/model_registry.csv) (`MODEL0001`, `MODEL0008`–`MODEL0012`) |
| `06_Experiments/` | Individual immutable experiment directories (`EXP0001`–`EXP0006`) & registry | [experiment_registry.csv](../06_Experiments/experiment_registry.csv), `EXPxxxx/config.yaml`, `ablations/` |
| `07_Checkpoints/` | Checkpointing policies and SHA-256 checkpoint manifests | Recoverable training checkpoint manifests (binary `.pth` weights live on Kaggle/Releases) |
| `08_Evaluation/` | Evaluation metrics (E1–E14), robustness, cross-dataset, statistical tests, and gate audits | `EVAL0001/`, `comparison_report.md`, `evaluation_audit.md`, `forensic_audit.md`, `statistics/` |
| `09_Figures/` | Figure specifications (`FIGxxxx`) per Policy A.9 | Figure provenance and data specs for thesis and papers |
| `10_Tables/` | Publication table specifications (`TABxxxx`) and rendered CSVs | Statistical comparison, metrics, and ablation tables |
| `11_AI_Forensic_System/` | Modular 18-module AI Forensic Analyst (`MOD001`–`MOD018`) | `pipeline.py`, `module_registry.csv`, `evidence/`, `fusion/`, `confidence/`, `decision/`, `explainability/`, `reasoning/`, `reports/`, `audit/`, `failure_handling/`, `specs/` |
| `12_Web/` | React + Vite + Tailwind web frontend (`MOD014`) | `src/api/`, 24 components (`src/components/`), 14 pages (`src/pages/`), `frontend_audit.md`, Vitest tests |
| `13_Backend/` | Django + DRF REST API backend (`MOD013`) & `forensic_engine` wrapper | `apps/`, `forensic_backend/`, `api_spec/api_spec.md`, `backend_audit.md`, `.env.example`, pytest suite |
| `14_Deployment/` | Deployment topology templates & server scaffolding | `nginx/`, `gunicorn/` specs and future deployment manifests |
| `15_Writing/` | Living literature review, writing evidence database, thesis & journal drafts | `literature_review/` and upcoming Part 14 thesis/manuscript chapters |
| `16_Documentation/` | System, API, developer, user, installation, test plan, and workflow docs | This folder (`architecture.md`, `api_guide.md`, `developer_guide.md`, `user_guide.md`, `installation.md`, `integration_guide.md`, `test_plan.md`, `documentation_audit.md`, `workflow_diagrams/`) |
| `17_Automation/` | Reproducible automation scripts, training runner, Kaggle sync, and UAT/test runners | `run_all_tests.py`, `run_uat.py`, `verify_integration.py`, `training/`, `kaggle_sync/`, `evaluation_trigger/` |
| `18_Templates/` | Canonical reusable Markdown templates (`Template 1`–`Template 24`) | Clean blank templates only; filled instances reside in domain folders |
| `19_Prompts/` | Versioned system prompts for specialized research, coding, and forensic agents | Agent prompt definitions including `forensic/` agents |
| `20_Archive/` | Immutable archive for superseded documents and completed snapshots | Historical outputs preserved without deletion |
