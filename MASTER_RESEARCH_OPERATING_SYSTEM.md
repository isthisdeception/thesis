<!--
============================================================================
 MASTER RESEARCH OPERATING SYSTEM
 Single Source of Truth for the AI Digital Forensics Research Project
============================================================================
 This is a PLANNING document. It contains no implementation code by design.
 It governs every phase of the project from the first downloaded paper until
 thesis defense and journal publication. All future planning and
 implementation artifacts must comply with this handbook.
============================================================================
-->

# MASTER RESEARCH OPERATING SYSTEM

### The Official Internal Handbook of the AI Digital Forensics Research Laboratory

---

## Cover Page

| Field | Value |
|---|---|
| **Project Title** | AI Digital Forensics — Image-Based AI-Generated Face Detection (Version 1) |
| **Primary Scientific Contribution** | The AI Forensic Analyst (an intelligent, evidence-driven forensic system) |
| **Document Title** | `MASTER_RESEARCH_OPERATING_SYSTEM.md` |
| **Document Type** | Research + Engineering Operating System (Planning / Governance) |
| **Document Status** | Ratified |
| **Owner** | Chief Research Architect (human researcher is the final authority) |
| **Scope** | Literature → Data → Models → Forensic System → Evaluation → Web App → Writing → Publication |
| **Applies To** | Cursor, Google Antigravity, Kaggle, GitHub, local development environment |

---

## Version Information

| Version | Date | Author | Summary of Changes | Status |
|---|---|---|---|---|
| v1.0.0 | Day 0 (initialization) | Chief Research Architect | Initial synthesis of the complete operating system. | Ratified |

**Document versioning follows the canonical Semantic Versioning policy defined in [Appendix A.3](#a3-canonical-versioning-policy).**

- **MAJOR** (`vX.0.0`): a structural change to the operating system (e.g., a new top-level section, a redefinition of a registry, a change to the folder architecture).
- **MINOR** (`v1.X.0`): a new sub-policy, template, agent, or workflow that does not break existing structure.
- **PATCH** (`v1.0.X`): clarifications, typo fixes, wording, or non-semantic corrections.

Every change to this document must be recorded in the table above and committed following the [Git Workflow](#10-github--kaggle--antigravity-workflow).

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Section 1 — Project Constitution](#1-project-constitution)
3. [Section 2 — Repository Architecture](#2-repository-architecture)
4. [Section 3 — Research & Literature Workflow](#3-research--literature-workflow)
5. [Section 4 — Dataset Operating System](#4-dataset-operating-system)
6. [Section 5 — Model Development Operating System](#5-model-development-operating-system)
7. [Section 6 — AI Forensic Analyst Architecture](#6-ai-forensic-analyst-architecture)
8. [Section 7 — Evaluation Protocol](#7-evaluation-protocol)
9. [Section 8 — Web Application Architecture](#8-web-application-architecture)
10. [Section 9 — Writing Operating System](#9-writing-operating-system)
11. [Section 10 — GitHub + Kaggle + Antigravity Workflow](#10-github--kaggle--antigravity-workflow)
12. [Section 11 — Agent Framework](#11-agent-framework)
13. [Section 12 — Daily Research Operating Workflow](#12-daily-research-operating-workflow)
14. [Section 13 — Quality Assurance](#13-quality-assurance)
15. [Section 14 — Template Library](#14-template-library)
16. [Appendix A — Canonical Definitions](#appendix-a--canonical-definitions)
17. [Appendix B — Registry Index](#appendix-b--registry-index)
18. [Appendix C — Cross-Reference Map](#appendix-c--cross-reference-map)
19. [Appendix D — Glossary](#appendix-d--glossary)
20. [Appendix E — Acronyms](#appendix-e--acronyms)
21. [Appendix F — Self-Review & Validation Record](#appendix-f--self-review--validation-record)

> **How to read this handbook.** Canonical rules that are reused everywhere (identifiers, naming, versioning, Definition of Done, README policy, registry format, storage tiers, Git workflow) are defined **once** in [Appendix A](#appendix-a--canonical-definitions) and referenced by every section. Sections describe *workflows and responsibilities*; the Appendix defines *the rules those workflows obey*.

---

## Executive Summary

This project builds an **AI Digital Forensics system**. Version 1 targets a single, well-scoped modality: **detecting AI-generated human faces in images**. However, the system is deliberately architected so that Audio, Video, Text, and Multimodal specialists can be added later **without redesign**.

The central thesis is that the primary scientific contribution is **not the deep learning detector**, but the **AI Forensic Analyst** — a modular system that collects independent *evidence*, validates it, fuses it, reasons over it, estimates *calibrated confidence*, explains its conclusions, and produces reproducible *forensic reports*. The detector is one *specialist* that supplies evidence; it never makes the final decision. This is defined in [Section 6](#6-ai-forensic-analyst-architecture).

The operating system rests on eight non-negotiable principles from the [Constitution](#1-project-constitution): reproducibility, version control, documentation, experiment metadata, figure traceability, evidence-backed results, elimination of manual chaos, and permanent repository organization.

The project is executed across four platforms with **strictly separated responsibilities** ([Section 10](#10-github--kaggle--antigravity-workflow)):

- **Cursor** — planning, architecture, research design, documentation, prompt authoring, code review. Never the implementation environment.
- **Google Antigravity** — the primary software engineer: implementation, debugging, local execution, report generation.
- **Kaggle** — GPU training and experiment execution only; never permanent storage.
- **GitHub** — the **single source of truth**; every important artifact eventually flows through it.
- **The human** — the final authority on all irreversible scientific decisions.

Everything is coordinated through a set of **canonical registries** (papers, datasets, preprocessing, experiments, models, evaluations, evidence, cases, modules, writing, risks — see [Appendix B](#appendix-b--registry-index)), a strict [identifier scheme](#a1-canonical-identifier-scheme), and a universal [Definition of Done](#a5-canonical-definition-of-done). Quality is enforced by [phase gates](#132-quality-gates) that block progress until objective checklists pass. Every recurring document is produced from a [template](#14-template-library), and every scientific sentence in the final thesis and journal manuscript traces back to recorded evidence via the [Claim Database](#claim-database).

This handbook is the blueprint. It is designed to guide the project from Day 1 to publication and to remain reusable for future research projects.

---

# 1. Project Constitution

> *This section states the supreme rules. Where any later section appears to conflict with the Constitution, the Constitution prevails. Where the Constitution is silent, the relevant operating section governs.*

## 1.1 Mandate

The role adopted for this project is **Chief Research Architect** and **Principal Software Architect**. The mandate is to design and maintain a **reproducible, maintainable, research-grade operating system**, not to produce ad-hoc code. Every decision must move the project toward scientific rigor, reproducibility, software quality, explainability, maintainability, extensibility, and publication readiness.

## 1.2 Project Identity

- **Domain:** AI Digital Forensics.
- **Version 1 scope:** image-based AI-generated face detection **only**.
- **Designed-for future:** Audio, Video, Text, and Multimodal forensics. The architecture is modular from Day 1. This is **not** a one-off image classifier; it is a **reusable forensic platform**.
- **Primary contribution:** the **AI Forensic Analyst** (the system), with the detector as one replaceable component.

## 1.3 What We Optimize For (in priority order)

1. Reproducibility
2. Research quality
3. Publication readiness
4. Maintainability
5. Software engineering quality
6. Clear documentation
7. Modularity

**We never optimize for:** shortest code, quickest implementation, unnecessary complexity, flashy architectures, or hype.

## 1.4 Fixed Technology Stack

The stack is fixed unless the human explicitly changes it. Build **around** these; do not replace them.

| Layer | Technology |
|---|---|
| Research planning | Cursor + Claude Opus |
| Implementation | Google Antigravity |
| GPU training | Kaggle |
| Version control | GitHub |
| Deep learning | FastAI + PyTorch (FastAI-first) |
| Backend | Django + Django REST Framework |
| Frontend | React + Vite + Tailwind CSS |
| Deployment | To be decided later (deferred decision — see [§1.11](#111-deferred-decisions)) |

## 1.5 Platform Responsibilities (canonical)

The authoritative statement of platform responsibilities and the artifact flow live in [Section 10](#10-github--kaggle--antigravity-workflow). In brief: **Local ↔ GitHub ↔ Kaggle ↔ GitHub ↔ Local**, with **GitHub as the source of truth**. No platform may assume another's responsibility.

## 1.6 The Eight Operating Principles

1. **Everything is reproducible.** If it cannot be reproduced, it does not exist.
2. **Everything is version controlled.**
3. **Everything has documentation.**
4. **Every experiment has metadata.**
5. **Every figure has traceability** (to data, script, and experiment).
6. **Every result has supporting evidence.**
7. **No manual chaos.** If something happens more than once, it becomes a documented workflow.
8. **The repository stays organized.** No random folders, filenames, or duplicate structures.

## 1.7 Governing Philosophies

- **Research philosophy.** Every phase answers an explicit research question. Work with no question attached is not performed.
- **Software philosophy.** This is a software *system*, not a notebook project. Notebook logic migrates into reusable Python packages ([Section 5](#5-model-development-operating-system), [Section 2](#2-repository-architecture)).
- **Model philosophy.** Do not fall in love with models. Models are replaceable; interfaces that allow model swaps are mandatory ([Section 6, Module 4](#module-4--deep-learning-specialist)).
- **Writing philosophy.** Never fabricate. Every sentence traces to experiments, evidence, literature, or recorded decisions ([Section 9](#9-writing-operating-system)).
- **Documentation philosophy.** Every important decision records: *What? Why? Alternatives? Reason for rejection? Expected impact?* (captured by the [Decision Log](#template-3--decision-log-decisionmd) and [ADR](#template-15--architecture-decision-record-adrmd) templates).
- **Agent philosophy.** One agent, one responsibility. Agents communicate **only through repository files** — never hidden conversation memory ([Section 11](#11-agent-framework)).
- **Error philosophy.** Errors are expected; silent failures are forbidden. Document, log, explain, continue safely.

## 1.8 Research Ethics (binding)

Never: manipulate experiments, cherry-pick results, ignore or hide negative/failed experiments, misuse datasets, violate licenses, leak test data, fabricate citations, or fabricate figures. **Scientific integrity outranks accuracy.** This rule is enforced by the [Quality Assurance](#13-quality-assurance) gates and the [Research Integrity checklist](#5-model-development-operating-system).

## 1.9 Human-in-the-Loop Rule

The human makes all important scientific decisions. The AI never makes irreversible research decisions (methodology, datasets, evaluation, architecture direction) without explicit approval. When human action is required, the workflow must **stop** and state: *why* it is needed, *exactly what* to do, *exactly where* files go, and *exactly what* the expected output is. See the [Human Tasks convention](#a8-human-task-protocol).

## 1.10 Planning-Before-Implementation

Design the workflow before implementing; understand the architecture before coding; understand the dataset before training; complete the experiments before writing. Planning always precedes implementation.

## 1.11 Deferred Decisions

When multiple reasonable approaches exist, the AI documents Option A / Option B, advantages, disadvantages, a recommendation, and **objective decision criteria**, then postpones the choice until evidence exists. Deferred decisions are tracked in the [Decision Log](#template-3--decision-log-decisionmd). Current known deferrals:

| Deferral ID | Topic | Decision Criteria | Blocking? |
|---|---|---|---|
| DEF-001 | Deployment target (Docker/VPS/PaaS/serverless) | Cost, reproducibility, GPU availability, maintenance burden | No (Version 1 runs locally) |
| DEF-002 | Final backbone architecture | Cross-dataset generalization, calibration, inference cost, explainability support ([Section 7](#7-evaluation-protocol)) | No (baselines proceed first) |
| DEF-003 | Primary training dataset(s) | Dataset evaluation score, license, generator diversity ([Section 4](#4-dataset-operating-system)) | Yes for training gate |
| DEF-004 | Evidence fusion strategy (rule-based → weighted → Bayesian) | Ablation results, calibration, interpretability ([Section 6](#module-7--evidence-fusion-engine)) | No (rule-based baseline first) |

## 1.12 Final Deliverables

Complete source code; research dataset pipeline; trained models; the [Experiment Registry](#experiment-registry); evaluation reports; explainability outputs; the AI Forensic Analyst; React frontend; Django backend; the REST API; the thesis; the journal manuscript; full documentation; a deployment guide; a user manual; and a developer manual.

---

# 2. Repository Architecture

> *This section defines the physical home for every artifact produced by every other section. The [identifier scheme](#a1-canonical-identifier-scheme), [file naming rules](#a2-canonical-file-naming-rules), [versioning](#a3-canonical-versioning-policy), [README policy](#a4-canonical-readme-policy), [storage tiers](#a6-canonical-storage--synchronization-policy), and [.gitignore policy](#a7-canonical-ignore-policy) are canonical and defined in [Appendix A](#appendix-a--canonical-definitions); this section defines the folder tree and each folder's contract.*

## 2.1 Design Goals

The repository must remain organized after **hundreds of experiments and dozens of datasets**. Every file type has exactly **one** correct location. No folder exists without a written purpose. The forbidden-name rules in [§2.4](#24-repository-hygiene-rules) are strictly enforced.

## 2.2 Top-Level Directory Tree

```
ai-digital-forensics/
├── README.md                      # Root README (Template 1)
├── LICENSE                        # Project license (human-approved)
├── CONTRIBUTING.md                # Contribution + workflow rules
├── CHANGELOG.md                   # Human-readable change history
├── CODEOWNERS                     # Ownership map
├── .gitignore                     # Canonical ignore policy (A.7)
├── .gitattributes                 # Git LFS + line-ending rules
├── environment/                   # Dependency + environment definitions
│   ├── requirements.txt
│   ├── environment.yml
│   ├── kaggle-requirements.txt
│   └── versions.lock.md           # Pinned Python/FastAI/PyTorch/CUDA record
│
├── 01_Project_Management/
├── 02_Literature/
├── 03_Datasets/
├── 04_Preprocessing/
├── 05_Models/
├── 06_Experiments/
├── 07_Checkpoints/
├── 08_Evaluation/
├── 09_Figures/
├── 10_Tables/
├── 11_AI_Forensic_System/
├── 12_Web/
├── 13_Backend/
├── 14_Deployment/
├── 15_Writing/
├── 16_Documentation/
├── 17_Automation/
├── 18_Templates/
├── 19_Prompts/
└── 20_Archive/
```

**Every folder contains a `README.md` conforming to the [README policy](#a4-canonical-readme-policy).** The numeric prefixes fix ordering and give each domain a stable, unambiguous home.

## 2.3 Folder Contracts

Each folder below is specified with: **Purpose · Writes (who generates) · Reads (who consumes) · Allowed · Forbidden · Example contents · Related folders.** Naming of all files obeys [Appendix A.1–A.2](#a1-canonical-identifier-scheme).

### 01_Project_Management
- **Purpose:** governance and coordination of the project.
- **Writes:** human; Planning/Operations agents ([Section 12](#12-daily-research-operating-workflow)).
- **Reads:** everyone; used to orient daily work.
- **Allowed:** project rules, `decision_log/` (Decision Log entries), `research_diary/` (`daily_research.md`), `reviews/` (`daily_review.md`, `weekly_review.md`, `monthly_review.md`), `meetings/`, `timeline.md`, `milestones/`, `dashboard_status.md`, `risk_register.csv`.
- **Forbidden:** datasets, model weights, source code, figures.
- **Example:** `decision_log/DEC0007.md`, `reviews/2026-week-31_weekly_review.md`.
- **Related:** [Section 12](#12-daily-research-operating-workflow), [Section 13](#13-quality-assurance).

### 02_Literature
- **Purpose:** the Literature Intelligence System ([Section 3](#3-research--literature-workflow)).
- **Writes:** Literature agents; human (downloads, approvals).
- **Reads:** Writing system ([Section 9](#9-writing-operating-system)); Research Planning.
- **Allowed:** `papers/` (`P0001.pdf` …), `summaries/` (`P0001_summary.md`), `metadata/` (`papers.csv`, `papers.bib`), `indexes/` (`keyword_index.csv`, `author_index.csv`, `venue_index.csv`, `dataset_index.csv`, `model_index.csv`), `research_gap/` (`research_gap.csv`, `gap/*.md`), `claims/` (`claim_database.csv`, `claim/*.md`), `search_history/`, `trends/`, `drafts/` (`literature_review.md`, `related_work.md`).
- **Forbidden:** renaming PDFs to titles; unregistered papers.
- **Example:** `papers/P0042.pdf`, `summaries/P0042_summary.md`.
- **Related:** [Section 3](#3-research--literature-workflow), [Section 9](#9-writing-operating-system).

### 03_Datasets
- **Purpose:** the Dataset Management System ([Section 4](#4-dataset-operating-system)).
- **Writes:** Dataset agents; human (downloads, approvals).
- **Reads:** [Preprocessing](#04_preprocessing), [Experiments](#06_experiments).
- **Allowed:** `raw/DS0001/` (immutable originals), `processed/DS0001_PP0001/`, `splits/DS0001_PP0001_SPLITxxxx/`, `metadata/` (`datasets.csv`, `dataset_candidates.csv`, `dataset_evaluation.csv`, `dataset_versions.csv`, `dataset_registry.csv`), `reports/` (`dataset_report.md`, `validation_report.csv`, `quality_report.csv`, `integrity_report.csv`, `split_report.md`), `licenses/`.
- **Forbidden:** modifying anything under `raw/`; overwriting processed datasets; committing large image data to Git (see [storage tiers](#a6-canonical-storage--synchronization-policy)).
- **Related:** [Section 4](#4-dataset-operating-system), [Section 7](#7-evaluation-protocol).

### 04_Preprocessing
- **Purpose:** modular, versioned preprocessing pipelines (`PP0001`…).
- **Writes:** Preprocessing agent (via Antigravity).
- **Reads:** [Datasets](#03_datasets) (produces `processed/`), [Experiments](#06_experiments).
- **Allowed:** reusable pipeline modules (packaged Python), `preprocessing_registry.csv`, `preprocessing_report.md` per pipeline, validation modules.
- **Forbidden:** one monolithic preprocessing script; unrecorded parameters.
- **Related:** [Section 4, Phases 9–11](#4-dataset-operating-system).

### 05_Models
- **Purpose:** model definitions, the [Model Registry](#model-registry), and exported inference models.
- **Writes:** Model/Training agents.
- **Reads:** [AI Forensic System](#11_ai_forensic_system), [Backend](#13_backend), [Evaluation](#08_evaluation).
- **Allowed:** architecture definitions (packaged), `candidate_models.csv`, `model_registry.csv`, `model_card.md` per model, exported inference artifacts pointers (weights live in the [artifact tier](#a6-canonical-storage--synchronization-policy)).
- **Forbidden:** committing large weight files to plain Git; anonymous models with no `MODELxxxx` ID.
- **Related:** [Section 5](#5-model-development-operating-system), [Section 6](#6-ai-forensic-analyst-architecture).

### 06_Experiments
- **Purpose:** one folder per experiment (`EXP0001`…). Never mix experiments.
- **Writes:** Experiment/Training agents.
- **Reads:** [Evaluation](#08_evaluation), [Writing](#15_writing).
- **Allowed (per experiment folder):** `config.yaml`, `README.md` (`experiment_readme.md`), `logs/`, `metrics/`, `predictions/`, `learning_curves/` (data, not final figures), `checkpoints_info.md`, `observations.md`, `failure_report.md`, `conclusions.md`, `notebook/`.
- **Forbidden:** shared/mixed experiment artifacts; editing a completed experiment's config.
- **Related:** [Section 5](#5-model-development-operating-system), [Experiment Registry](#experiment-registry).

### 07_Checkpoints
- **Purpose:** checkpoint policy and the pointer/manifest layer for recoverable training state.
- **Writes:** Checkpoint agent.
- **Reads:** [Experiments](#06_experiments), Kaggle resume workflow ([Section 10](#phase-8--checkpoint-recovery)).
- **Allowed:** `checkpoint_policy.md`, per-experiment checkpoint manifests (`EXP0007_checkpoints.md` listing best/last/recovery + checksums + storage location), FastAI export pointers.
- **Forbidden:** overwriting checkpoints; storing the only copy of a checkpoint here without an artifact-tier backup.
- **Related:** [Section 5, Phase 7](#phase-7--checkpoint-management-critical); [Section 10, Phase 8](#phase-8--checkpoint-recovery).

### 08_Evaluation
- **Purpose:** all evaluation outputs and the [Evaluation Registry](#evaluation-registry) ([Section 7](#7-evaluation-protocol)).
- **Writes:** Evaluation agents.
- **Reads:** [Figures](#09_figures), [Tables](#10_tables), [Writing](#15_writing).
- **Allowed:** metric CSVs, ROC/PR/calibration/confusion **data**, robustness/generalization/unseen-generator/ablation results, statistical test outputs, `evaluation_report.md`, `failure_analysis.md`, `comparison_report.md`, `evaluation_registry.csv`, `prediction_validation_report.md`.
- **Forbidden:** final publication figures (those are specs → [Figures](#09_figures)); re-computing metrics after seeing results without a new Evaluation ID.
- **Related:** [Section 7](#7-evaluation-protocol), [Section 9](#9-writing-operating-system).

### 09_Figures
- **Purpose:** every figure used anywhere plus its **specification** and generation provenance.
- **Writes:** human (final figures), Figure specification agents (`figure_spec.md`).
- **Reads:** [Writing](#15_writing), [Web](#12_web), presentations.
- **Allowed:** `specs/FIG0001_spec.md`, generation scripts/notebooks, `assets/FIG0001_v1.png|svg|pdf`, `captions.md`.
- **Forbidden:** figures without a `FIG` ID, caption, source experiment, and generation script (see [Figure Policy](#a9-canonical-figure-policy)).
- **Related:** [Section 7, Phase 17](#7-evaluation-protocol), [Section 9, Phase 8](#9-writing-operating-system).

### 10_Tables
- **Purpose:** every table (`TAB0001`…) in CSV / Markdown / Excel with a specification.
- **Writes:** Evaluation/Writing agents.
- **Reads:** [Writing](#15_writing).
- **Allowed:** `specs/TAB0001_spec.md`, `data/TAB0001.csv`, `rendered/TAB0001.md`.
- **Forbidden:** tables without a source experiment or data provenance.
- **Related:** [Section 7](#7-evaluation-protocol), [Section 9](#9-writing-operating-system).

### 11_AI_Forensic_System
- **Purpose:** the AI Forensic Analyst source ([Section 6](#6-ai-forensic-analyst-architecture)).
- **Writes:** Antigravity (implementation of module specs).
- **Reads:** [Backend](#13_backend) (serves it), [Evaluation](#08_evaluation).
- **Allowed:** module packages (input, validation, evidence collectors, DL specialist wrapper, evidence registry, validation, fusion, decision, confidence, explainability, reasoning, report generator), `module_registry.csv`, module specs.
- **Forbidden:** frontend code; training code; datasets.
- **Related:** [Section 6](#6-ai-forensic-analyst-architecture), [Section 8](#8-web-application-architecture).

### 12_Web
- **Purpose:** React + Vite + Tailwind frontend ([Section 8](#8-web-application-architecture)).
- **Writes:** Antigravity (frontend).
- **Reads:** end users; backend API contracts.
- **Allowed:** `src/pages`, `src/layouts`, `src/components`, `src/hooks`, `src/api`, `src/context`, `src/assets`, `src/styles`, frontend docs.
- **Forbidden:** any AI/inference logic; hardcoded API URLs; business/forensic reasoning.
- **Related:** [Section 8](#8-web-application-architecture).

### 13_Backend
- **Purpose:** Django + DRF backend that owns the investigation ([Section 8](#8-web-application-architecture)).
- **Writes:** Antigravity (backend).
- **Reads:** frontend (via API); the AI Forensic System.
- **Allowed:** Django project + apps (`api`, `forensic_engine`, `evidence`, `reports`, `health`, `versioning`, `core/config`, future `accounts`, future `history`), `media/` config, `static/` config, `api_spec/`.
- **Forbidden:** model training code; committed media uploads; committed secrets.
- **Related:** [Section 6](#6-ai-forensic-analyst-architecture), [Section 8](#8-web-application-architecture).

### 14_Deployment
- **Purpose:** deployment configuration and documentation (target deferred — [DEF-001](#111-deferred-decisions)).
- **Writes:** Deployment agent.
- **Reads:** operators.
- **Allowed:** `Dockerfile`(s), `docker-compose.yml`, `nginx/`, `gunicorn/`, env templates (`.env.example`), `deployment.md`, production settings templates.
- **Forbidden:** real `.env` with secrets; production credentials.
- **Related:** [Section 8](#8-web-application-architecture), [Section 10](#10-github--kaggle--antigravity-workflow).

### 15_Writing
- **Purpose:** thesis + journal + supplementary material ([Section 9](#9-writing-operating-system)).
- **Writes:** Writing agents; human (approvals, edits).
- **Reads:** supervisors, reviewers.
- **Allowed:** `thesis/` (per-chapter), `journal/`, `shared/` (`writing_database.csv`, `knowledge_index.csv`, `writing_progress.csv`), `references/` (`references.bib`), `reviewer_responses/` (`review_response.md`), `revisions/`.
- **Forbidden:** unsupported claims; invented citations; final PDFs mixed with drafts (finals go to [Archive](#20_archive) on submission).
- **Related:** [Section 9](#9-writing-operating-system), [Section 3](#3-research--literature-workflow), [Section 7](#7-evaluation-protocol).

### 16_Documentation
- **Purpose:** developer + user + system documentation.
- **Writes:** Documentation agent.
- **Reads:** developers, users, examiners.
- **Allowed:** `architecture.md`, `api_guide.md`, `developer_guide.md`, `user_guide.md`, `installation.md`, `workflow_diagrams/`, folder guides.
- **Forbidden:** duplicating this handbook (link to it instead).
- **Related:** all sections.

### 17_Automation
- **Purpose:** reproducible scripts and pipeline automation (specs here; implementation by Antigravity).
- **Writes:** Automation/DevOps agents.
- **Reads:** all workflows.
- **Allowed:** environment setup scripts, Git automation, Kaggle sync scripts, report-generation scripts, registry-validation scripts, health checks.
- **Forbidden:** automating scientific *decisions* ([§1.9](#19-human-in-the-loop-rule)).
- **Related:** [Section 10](#10-github--kaggle--antigravity-workflow), [Section 13](#13-quality-assurance).

### 18_Templates
- **Purpose:** the canonical template library ([Section 14](#14-template-library)).
- **Writes:** Research Process Architect.
- **Reads:** everyone.
- **Allowed:** every template file listed in [Section 14](#14-template-library).
- **Forbidden:** filled-in instances (those live in their domain folders).
- **Related:** [Section 14](#14-template-library).

### 19_Prompts
- **Purpose:** every prompt used in the project, versioned.
- **Writes:** human; Cursor planning agents.
- **Reads:** all agents.
- **Allowed:** `planning/`, `implementation/`, `literature/`, `writing/`, `evaluation/`, `review/`, `prompt_changelog.md`, versioned prompt files (`prompt.md` template).
- **Forbidden:** secrets embedded in prompts.
- **Related:** [Section 11](#11-agent-framework), [Section 14, Template 26](#template-26--prompt-template-promptmd).

### 20_Archive
- **Purpose:** **read-only** storage of completed/superseded artifacts.
- **Writes:** human only (on archival events: submissions, releases).
- **Reads:** anyone (reference only).
- **Allowed:** submitted/accepted/camera-ready documents, retired designs, historical snapshots.
- **Forbidden:** **any modification of contents**; active/working files.
- **Related:** [Section 9, Phase 19](#9-writing-operating-system), [Section 10, Phase 12](#phase-12--release-workflow).

## 2.4 Repository Hygiene Rules

The repository must **never** contain: `misc`, `temp`, `tmp`, `new`, `old`, `backup`, `copy`, `copy2`, `Untitled*`, `test123`, stray/unregistered notebooks, duplicate files, or orphan files. Anything temporary uses the ignore policy ([Appendix A.7](#a7-canonical-ignore-policy)) and never gets committed. Enforcement is a mandatory item of the [Repository Readiness checklist](#checklist-1--repository-readiness).

---

# 3. Research & Literature Workflow

> *Goal: a **Literature Intelligence System** that stays organized past 500+ papers and drives the research direction. Literature drives implementation — never the reverse. Files live in [02_Literature](#02_literature); agents are specified in [Section 11](#11-agent-framework); outputs feed the [Writing System](#9-writing-operating-system). All IDs follow [Appendix A.1](#a1-canonical-identifier-scheme).*

## 3.1 Phase Format

Each phase specifies **Purpose · Inputs · Outputs · Responsible Agent · Human Tasks · AI Tasks · Folder · Acceptance Criteria · Definition of Done · Failure Handling.** The universal DoD checklist in [Appendix A.5](#a5-canonical-definition-of-done) always applies in addition to the phase-specific DoD.

## 3.2 Phases

### Phase L1 — Research Question Definition
- **Purpose:** convert a vague topic into an official research question, keyword list, and exclusion list.
- **Inputs:** initial topic ("image-based AI-generated face detection"); domain knowledge.
- **Outputs:** `research_question.md`, `keywords.csv`, `exclusion_list.csv` (in `02_Literature/`).
- **Responsible Agent:** Research Planning Agent. **Human Tasks:** approve the question and scope. **AI Tasks:** propose candidate questions, keyword seeds, and scope boundaries.
- **Acceptance Criteria:** one primary question + ≤3 sub-questions; ≥20 seed keywords; explicit out-of-scope list.
- **DoD:** human-approved research question recorded and committed.
- **Failure Handling:** if scope is too broad/narrow, record the tension in the [Decision Log](#template-3--decision-log-decisionmd) and iterate.

### Phase L2 — Literature Search Strategy
- **Purpose:** a reproducible, evolving search across Google Scholar, IEEE Xplore, ACM DL, Springer, ScienceDirect, CVF Open Access, OpenReview, and arXiv.
- **Outputs:** `search_history/` entries recording *source, search string, date, filters, result count, papers selected*; `search_string_templates.md`.
- **Search string template (canonical):** `("<core concept>" ) AND ("<method family>" OR "<synonym>") AND ("<modality>") [year>=YYYY] [venue filter]`.
  - Example: `("AI-generated" OR "synthetic" OR "deepfake") AND ("face" OR "facial") AND ("detection" OR "forensics") AND (GAN OR "diffusion")`.
- **Search evolution rule:** new keywords are *harvested from collected papers* (titles, keyword sections, method names) and appended to `keywords.csv` with the source `Paper ID`. Every search run is logged so it can be repeated.
- **Filters:** publication year, venue quality, citation threshold, duplicate detection (by DOI/title normalization), and priority ranking.
- **Responsible Agent:** Literature Search Agent (searches, filters, ranks, collects — never summarizes).
- **DoD:** each search run is reproducible from its logged string + filters.

### Phase L3 — Paper Download Workflow
- **Purpose:** acquire PDFs with canonical, title-free filenames.
- **Rule:** filenames are `P0001.pdf`, `P0002.pdf`, …; **titles live only in metadata** ([papers.csv](#papers-registry)). Duplicate detection by DOI/normalized title before assigning a new `P` ID. License is verified and recorded before use.
- **Human Task:** manually download the PDF (respecting access rights) and place it in `02_Literature/papers/` with the assigned ID (see [Human Task Protocol](#a8-human-task-protocol)).
- **DoD:** every PDF present has a matching row in `papers.csv`; no title-named files exist.

### Phase L4 — Paper Registration
- **Purpose:** no paper exists without metadata.
- **Output:** the **[Papers Registry](#papers-registry)** (`papers.csv`), the canonical literature registry.
- **Responsible Agent:** Paper Registration Agent (registers/maintains metadata; never downloads). **Metadata Extraction Agent** fills structured fields.
- **DoD:** every `P` ID has all required columns populated or explicitly marked `unknown`.

<a id="papers-registry"></a>
**Papers Registry — `papers.csv` (canonical columns):** `Paper ID, Title, Authors, Year, Venue, Publisher, DOI, Citation Count, Dataset, Architecture, Task, Modality, Explainability, Generalization, Limitations, Future Work, Code Available, Dataset Available, Keywords, Reading Status, Priority, Notes, Folder Location, BibTeX Available, PDF Available, Reviewed, Quality Score, Research Relevance.`

### Phase L5 — Paper Reading Workflow
- **Purpose:** structured, non-blind reading. Every paper produces a unique summary using the [Paper Summary template](#template-2--paper-summary-paper_summarymd).
- **Output:** `summaries/P0001_summary.md` capturing Problem, Motivation, Method, Architecture, Dataset, Training, Evaluation, Results, Strengths, Weaknesses, Research Gap, Future Work, Interesting Ideas, Possible Reuse, Questions, Connections.
- **Responsible Agent:** Paper Summary Agent (never invents; every statement traces to the paper). **Human Task:** approve summaries for high-priority papers.
- **DoD:** summary exists, cross-links other `P` IDs, and its extracted limitations/future-work are pushed to Phase L8 inputs.

### Phase L6 — Literature Database & Indexing
- **Purpose:** a searchable database spanning CSV, Markdown, JSON, and BibTeX with automatic indexing.
- **Outputs:** `papers.bib`; the indexes `keyword_index.csv`, `author_index.csv`, `venue_index.csv`, `dataset_index.csv`, `model_index.csv`, plus `research_gap` and `future_work` indexes (below). Each index maps a term → list of `P` IDs.
- **DoD:** every index regenerates deterministically from `papers.csv` + summaries.

### Phase L7 — Paper Relationship Graph
- **Purpose:** derive relationships (same dataset, improves prior work, new architecture, uses explainability, robustness, cross-dataset, distillation, frequency-domain, ViT, foundation models) **from metadata only** — never guessed.
- **Output:** `citation_network.csv` (and derived dataset/architecture/topic networks).
- **Responsible Agent:** Relationship Agent.
- **DoD:** every edge cites the metadata field(s) that produced it.

### Phase L8 — Research Gap Discovery *(most important)*
- **Purpose:** discover gaps from evidence, never invent them.
- **Method:** extract every limitation, future-work item, weakness, and open problem from every summary → cluster → rank by frequency and importance.
- **Output:** the **Research Gap Registry** `research_gap.csv` (`Gap ID, Category, Supporting Papers, Frequency, Conflicting Papers, Importance, Research Opportunity`) plus one `gap/GAP0001.md` per gap ([Gap template](#template-14--research-gap-gapmd)); and `future_work.csv`.
- **Responsible Agent:** Research Gap Agent.
- **Validation:** a gap is valid only if supported by ≥2 independent papers **or** explicitly flagged as a single-source hypothesis awaiting confirmation.
- **DoD:** every gap links to supporting `P` IDs.

### Phase L9 — Evidence Collection (Claim Database)
- **Purpose:** every scientific claim is supported.
- **Output:** the **[Claim Database](#claim-database)** `claim_database.csv`, the canonical evidence ledger shared with the [Writing System](#phase-w11--claim-verification).

<a id="claim-database"></a>
**Claim Database — `claim_database.csv` (canonical columns):** `Claim ID, Statement, Supporting Papers, Supporting Experiments, Supporting Figures, Supporting Tables, Contradicting Evidence, Confidence, Page References, Status.` This single registry links literature evidence *and* experimental evidence and is the backbone of [Claim Verification](#phase-w11--claim-verification).

### Phase L10 — Research Direction Selection
- **Purpose:** the AI proposes; the human decides.
- **Output:** `research_directions.md` listing top candidate directions with advantages, disadvantages, complexity, novelty, publication potential, implementation difficulty, dataset needs, evaluation needs, future scalability, and **objective decision criteria**.
- **Human Task:** choose the direction; the choice is recorded in the [Decision Log](#template-3--decision-log-decisionmd).

### Phase L11 — Living Literature Review
- **Purpose:** the review is never "finished." New papers trigger **incremental** updates to only affected sections, with version history and change tracking (versioning per [Appendix A.3](#a3-canonical-versioning-policy)).

### Phase L12 — Literature Review Generation
- **Purpose:** generate Introduction, Related Work, comparison tables, research trends/evolution, and gap discussion **only after enough evidence exists**.
- **Rule:** every paragraph traces to papers, summaries, the Claim Database, and the Research Gap Registry. No hallucinated citations. Outputs (`literature_review.md`, `related_work.md`) feed [Section 9](#9-writing-operating-system).

## 3.3 Paper Quality Policy
Objective scoring (0–5 each, recorded as `Quality Score` in `papers.csv`): Venue Quality, Citation Impact, Novelty, Dataset Quality, Evaluation Quality, Reproducibility, Code Availability, Explainability, External Validation, Generalization. Papers are ranked by the aggregate; priority reading follows the ranking.

## 3.4 Literature Output Files (ownership summary)

| File | Purpose | Generated by | Consumed by | Update frequency |
|---|---|---|---|---|
| `papers.csv` | Papers Registry | Paper Registration Agent | all literature phases, Writing | on every new paper |
| `papers.bib` | Citation source | Citation Agent | Writing | on registration/verification |
| `P####_summary.md` | Structured notes | Paper Summary Agent | Gap, Writing | per paper |
| `research_gap.csv` | Research Gap Registry | Research Gap Agent | Direction Selection, Writing | on new summaries |
| `claim_database.csv` | Claim Database | Knowledge Base Agent | Writing, Evaluation | continuous |
| `research_trends.csv` | Trends | Trend Analysis Agent | Writing | periodic |
| `comparison_table.csv` | Related-work comparison | Relationship/Writer agents | Writing | periodic |
| `*_index.csv` | Indexes | Knowledge Base Agent | search, Writing | on registry change |
| `reading_progress.csv` | Reading status | Registration Agent | Daily/weekly reviews | daily |
| `citation_network.csv` | Relationship graph | Relationship Agent | Writing, trends | periodic |
| `literature_review.md`, `related_work.md` | Draft prose | Literature Writer Agent | Writing | as evidence grows |

## 3.5 Literature Definition of Done
Every paper registered with metadata and structured notes; every important claim has evidence; every gap has supporting papers; the literature review regenerates from evidence; the research direction is objectively selectable; the system keeps growing. Plus the universal [DoD](#a5-canonical-definition-of-done).

---

# 4. Dataset Operating System

> *Goal: a research-grade dataset lifecycle guaranteeing reproducibility, traceability, integrity, versioning, and scalability. Files live in [03_Datasets](#03_datasets) and [04_Preprocessing](#04_preprocessing). Datasets feed [Experiments (Section 5)](#5-model-development-operating-system) and are evaluated in [Section 7](#7-evaluation-protocol). Identifiers follow [Appendix A.1](#a1-canonical-identifier-scheme); storage/sync follows [Appendix A.6](#a6-canonical-storage--synchronization-policy).*

## 4.1 Lifecycle Overview
`Discovery → Evaluation → Registration → Download → Raw-lock → Validation → EDA → Documentation → Preprocessing (PPxxxx) → Processed generation → Splitting → FastAI preparation → Version control → Registry`.

## 4.2 Phases

### Phase D1 — Dataset Discovery
- **Purpose:** find candidate datasets (Kaggle, Hugging Face, GitHub, papers, project sites, university/CVPR supplements, Zenodo, Figshare, OpenML).
- **Output:** `dataset_candidates.csv` (`Candidate ID, Name, Source, URL, License seen, Availability, Duplicate-of, Notes`). Duplicates flagged before evaluation; licenses recorded at first sight.
- **Responsible Agent:** Dataset Discovery Agent.

### Phase D2 — Dataset Evaluation
- **Purpose:** objective, comparable scoring; the AI ranks, the human approves.
- **Output:** `dataset_evaluation.csv` scoring Dataset Size, Image Quality, Resolution, Label Quality, Metadata Quality, Class Balance, License, Source Credibility, Research Popularity, Citation Count, Top-Conference Use, Availability, Maintenance, Bias, Explainability Suitability, Generalization Suitability.
- **Human Task:** approve which datasets proceed (relates to [DEF-003](#111-deferred-decisions)).

### Phase D3 — Dataset Registration
- **Purpose:** every accepted dataset gets a `DSxxxx` ID and metadata.
- **Output:** `datasets.csv` (`Dataset ID, Name, Version, Source, Download URL, License, Citation, Publication, Image Count, Real Images, Fake Images, Resolution, File Format, Split Available, Metadata, Downloaded, Validated, Ready`).
- **Responsible Agent:** Metadata Agent.

### Phase D4 — Dataset Download
- **Purpose:** acquire data with integrity guarantees.
- **Rules:** record checksums (SHA-256) for archives; verify file integrity; controlled extraction into `raw/DSxxxx/`; never overwrite. Large data stays in the [artifact/Kaggle tier](#a6-canonical-storage--synchronization-policy), never plain Git.
- **Human Task:** perform the manual download and placement per the [Human Task Protocol](#a8-human-task-protocol).

### Phase D5 — Raw Dataset Policy *(sacred)*
The raw dataset is **immutable**: never rename, modify, delete, or overwrite files under `raw/`. Everything must remain identical to the original source. Any transformation happens downstream in `processed/`.

### Phase D6 — Dataset Validation
- **Purpose:** catch broken/duplicate images, wrong labels, corrupted/unsupported files, invalid filenames, missing labels/metadata; analyze resolution and aspect ratio.
- **Outputs:** `validation_report.csv`, `quality_report.csv`, `integrity_report.csv`.
- **Responsible Agents:** Validation Agent, Quality Agent.

### Phase D7 — Exploratory Dataset Analysis
- **Purpose:** understand the data before training.
- **Analyses (AI recommends, human approves):** class distribution, resolution, brightness, contrast, color channels, compression, balance, generator distribution, identity distribution, and — *if available* — age/gender/ethnicity distribution, missing values, outliers.
- **Figures:** produced as **specs only** ([Figure Policy](#a9-canonical-figure-policy)).

### Phase D8 — Dataset Documentation
- **Output:** `dataset_report.md` ([Dataset Report template](#template-5--dataset-report-dataset_reportmd)) + `dataset_card.md` ([Dataset Card template](#template-23--dataset-card-dataset_cardmd)) covering origin, purpose, license, statistics, strengths, weaknesses, known biases, recommended usage, known problems, research relevance, citation, location.
- **Responsible Agent:** Documentation Agent.

### Phase D9 — Preprocessing Workflow
- **Purpose:** modular, independent preprocessing steps: image verification, face detection, face alignment, cropping, resize, normalization, quality filtering, artifact removal, format conversion, metadata extraction.
- **Rule:** never one monolithic script; each step is an independent, testable, reusable module ([04_Preprocessing](#04_preprocessing)).

### Phase D10 — Preprocessing Versioning
- **Output:** the **Preprocessing Registry** `preprocessing_registry.csv` (`Pipeline ID, Operations, Parameters, Dataset, Output, Purpose, Date, Research Question`). Each pipeline is `PPxxxx`.

### Phase D11 — Processed Dataset Generation
- **Rule:** never overwrite processed data. Outputs are named `DS0001_PP0001`, `DS0001_PP0002`, … under `processed/`. Each processed dataset carries a `preprocessing_report.md` ([template](#template-6--preprocessing-report-preprocessing_reportmd)).

### Phase D12 — Train/Validation/Test Split *(leakage-critical)*
- **Purpose:** scientific, reproducible splitting that prevents identity leakage, duplicate leakage, generator leakage, future leakage, and train/test contamination.
- **Rule:** splits are grouped by identity and (where relevant) by generator so the same identity/generator never spans train and test. Record random seed, algorithm, and statistics.
- **Output:** `split_report.md` + split index files named `DS0001_PP0001_SPLIT0001`.

### Phase D13 — FastAI Dataset Preparation *(design only)*
- **Purpose:** define how a processed+split dataset becomes FastAI `DataLoaders`: `DataBlock` definition, transforms, augmentations, normalization stats, batch/image size, and version tracking. These parameters live in the experiment `config.yaml` ([Section 5, Phase 4](#phase-m4--configuration-system)), not hidden in code.

### Phase D14 — Dataset Version Control
- **Output:** `dataset_versions.csv` tracking added/removed images, corrected labels, preprocessing changes, split changes, documentation changes, using [SemVer](#a3-canonical-versioning-policy) (`v1.0`, `v1.1`, `v2.0`).

### Phase D15 — Dataset Registry *(master traceability)*
<a id="dataset-registry"></a>
- **Output:** the **Dataset Registry** `dataset_registry.csv` — the master ledger linking **every dataset → every version → every preprocessing (`PP`) → every split → every experiment (`EXP`) using it → every model (`MODEL`) trained on it.** This is the canonical dataset-side traceability spine referenced by [Section 5](#5-model-development-operating-system) and [Section 7](#7-evaluation-protocol).

### Phase D16 — Dataset Change Policy
Any change generates a change record: `Change ID, Reason, Author, Date, Files Changed, Impact, Affected Experiments, Rollback Strategy`. Recorded in the [Decision Log](#template-3--decision-log-decisionmd) when methodologically significant.

### Phase D17 — Dataset Figures
Specs only, per the [Figure Policy](#a9-canonical-figure-policy).

### Phase D18 — Dataset Agents
Discovery, Evaluation, Metadata, Validation, Quality, Preprocessing, Split, Statistics, Documentation, Registry — each fully specified in [Section 11](#11-agent-framework).

### Phase D19 — Kaggle Data Workflow
Data flow: `Local → GitHub (metadata/pointers) → Kaggle Dataset (raw/processed data) → Training → Outputs → Download → GitHub → Local`. **What lives where** is governed by the canonical [storage tiers](#a6-canonical-storage--synchronization-policy): large image data lives in Kaggle Datasets / artifact storage; only metadata, registries, reports, and small indexes live in Git.

## 4.3 Dataset Research Rules (binding)
Never modify raw datasets; never overwrite processed datasets; never silently change labels; never mix datasets without documentation; never create train/test leakage; never preprocess without recording parameters; never train on undocumented datasets. Every dataset is citable; every pipeline reproducible; every split repeatable.

## 4.4 Dataset Definition of Done
Every dataset registered, documented, and versioned; every pipeline versioned; every split reproducible; every processed dataset traceable; every experiment can name its exact dataset version; every dataset figure recreatable; every dataset claim evidence-backed. Plus the universal [DoD](#a5-canonical-definition-of-done).

---

# 5. Model Development Operating System

> *Reframe: you never "train a model" — you **conduct Experiment `EXPxxxx`**. The model is one component of the experiment. FastAI-first. Files live in [06_Experiments](#06_experiments), [05_Models](#05_models), [07_Checkpoints](#07_checkpoints). Consumes the [Dataset Registry](#dataset-registry); feeds [Evaluation (Section 7)](#7-evaluation-protocol) and the [Writing Database](#writing-database).*

## 5.1 Phases

### Phase M1 — Candidate Model Discovery
- **Output:** `candidate_models.csv` (`Model ID, Architecture, Paper, Year, Conference, Parameters, Pretrained, FastAI Compatible, Input Size, Advantages, Weaknesses, Computation Cost, Research Relevance, Explainability Support, Generalization, Notes`). Sources: CVPR/ICCV/ECCV/WACV, FastAI, `timm`, Hugging Face, official repos. **The AI ranks; the human approves** ([DEF-002](#111-deferred-decisions)).

### Phase M2 — Baseline Strategy
- **Output:** `baseline_plan.md`. A baseline is a fair reference experiment. **Fairness invariants:** identical dataset version, split version, preprocessing (`PP`), metrics, and evaluation protocol across compared experiments. Never compare unfair experiments.

### Phase M3 — FastAI Training Standard *(design, not code)*
Standard workflow embracing FastAI: `DataBlock → DataLoaders → Learner → callbacks → mixed precision → transfer learning → LR Finder → fit_one_cycle → unfreeze/fine-tune → export`. The project uses FastAI deliberately for cleaner code, readability, faster experimentation, and standardized workflows — **design with FastAI, not against it.**

### Phase M4 — Configuration System
<a id="phase-m4--configuration-system"></a>
- **Rule:** nothing lives only in notebook code; everything lives in `config.yaml` ([Config template](#template-8--configuration-configyaml)).
- **Config sections:** Experiment ID, Dataset Version, Split Version, Model Version, FastAI Settings, Image Size, Batch Size, Epochs, Optimizer, Learning Rate, Loss Function, Metrics, Random Seed, Augmentations, Hardware, Git Commit, Timestamp, Research Question, Purpose, Expected Outcome.

### Phase M5 — Experiment Creation
Each `EXPxxxx` receives a dedicated folder ([06_Experiments contract](#06_experiments)) with README, config, notebook, logs, metrics, predictions, checkpoint info, observations, failure report, conclusions. **Never mix experiments.**

### Phase M6 — Training Workflow
`Dataset validation → Config validation → Training → Validation → Checkpoint save → Metric update → Learning-curve data → Model export → Experiment summary → GitHub sync`. Every step logged.

### Phase M7 — Checkpoint Management *(critical)*
<a id="phase-7--checkpoint-management-critical"></a>
Because Kaggle sessions terminate, checkpointing is designed for full recoverability. Capture: **best model, last epoch, recovery checkpoint**, and training state = model weights + optimizer state + scheduler state + epoch number + random state + experiment state. Policies: checkpoint frequency, resume policy, failure recovery, early stopping, FastAI `export.pkl`, PyTorch `weights.pth`. **Nothing is ever overwritten** (see [Checkpoint Integrity checklist](#checklist-7--checkpoint-integrity)). Manifests + checksums live in [07_Checkpoints](#07_checkpoints); binaries live in the [artifact tier](#a6-canonical-storage--synchronization-policy).

### Phase M8 — Kaggle Training Workflow
`Start session → git pull → verify repo → download dataset → verify checkpoints → resume experiment → train → evaluate → export artifacts → upload outputs → push metadata → shutdown`. Detailed in [Section 10, Phase 7](#phase-7--kaggle-training-workflow); must survive time limits.

### Phase M9 — Model Registry
<a id="model-registry"></a>
- **Output:** the **Model Registry** `model_registry.csv` (`Model ID, Experiment, Dataset, Split, Architecture, Training Time, GPU, Metrics, Checkpoint, Git Commit, Export Path, Deployment Ready, Research Notes, Publication Used`). Each model also has a `model_card.md` ([template](#template-22--model-card-model_cardmd)).

### Phase M10 — Experiment Registry
<a id="experiment-registry"></a>
- **Output:** the **Experiment Registry** `experiment_registry.csv` (`Experiment ID, Purpose, Research Question, Configuration, Dataset, Model, Results, Best Epoch, Training Time, Status, Failures, Reviewer Notes, Next Actions`). This is the canonical experiment-side spine, complementing the [Dataset Registry](#dataset-registry) and [Model Registry](#model-registry). **This name is fixed** — never "experiment database/tracker/log."

### Phase M11 — Logging System
Log training/validation metrics, GPU usage, epoch summaries, learning curves, hyperparameters, timing, warnings, errors. Nothing important disappears.

### Phase M12 — Hyperparameter Strategy
Methods: manual, FastAI LR suggestions, grid, random, Bayesian (future). The AI proposes; the human approves search scope. All runs are version-tracked as distinct experiments.

### Phase M13 — Model Comparison
Comparison tables/reports, ranking, radar-chart specs, metric summaries, failure analysis — **only across fairness-compatible experiments** ([Phase M2](#phase-m2--baseline-strategy)). Feeds [Section 7, Phase 16](#phase-e16--comparison-study).

### Phase M14 — Failure Analysis
Every failed experiment produces `failure_report.md` ([template](#template-9--failure-report-failure_reportmd)): instability, overfitting, underfitting, poor convergence, bad augmentation, wrong preprocessing, checkpoint failure, hardware interruption, unexpected behavior. **Failed experiments are never deleted** — they are knowledge.

### Phase M15 — FastAI Export Policy
Standard artifacts: `export.pkl`, `weights.pth`, `best_model.pth`, `last_checkpoint.pth`, prediction files, inference package, deployment package, documentation, versioning. Export paths recorded in the [Model Registry](#model-registry).

### Phase M16 — Evaluation Trigger
Training completion **automatically prepares** all evaluation inputs: prediction files, metrics, confusion-matrix data, ROC data, PR data, calibration data, feature-importance data, attention maps, explainability inputs. Figures are made later from this data ([Section 7](#7-evaluation-protocol)).

### Phase M17 — Model Agents
Model Discovery, Training, Checkpoint, Experiment, Evaluation Trigger, Failure Analysis, Registry, Comparison, FastAI Configuration — specified in [Section 11](#11-agent-framework).

### Phase M18 — GitHub Synchronization
What belongs in Git vs. Releases vs. Git LFS vs. never-committed is governed by [Appendix A.6](#a6-canonical-storage--synchronization-policy) and [Section 10, Phases 10–11](#phase-10--synchronization-strategy).

### Phase M19 — Research Integrity *(binding)*
Never overwrite checkpoints, delete failed experiments, modify previous metrics, change configs after training, rename experiments, change dataset versions retroactively, hide failed models, or cherry-pick. Integrity outranks performance.

## 5.2 Model Development Definition of Done
Every experiment reproducible; every checkpoint recoverable; every FastAI learner documented; every model registered; every result traceable; every experiment resumable after Kaggle interruption; every trained model deployable; every publication figure regenerable; every claim traceable to a specific experiment. Plus the universal [DoD](#a5-canonical-definition-of-done).

---

# 6. AI Forensic Analyst Architecture

> *The primary scientific contribution. Not a classifier — an **evidence-driven forensic system**. It consumes the [Model Registry](#model-registry) (detector as one specialist), is validated in [Section 7, Phase 14](#phase-e14--ai-forensic-analyst-evaluation), and is served by the [Backend (Section 8)](#8-web-application-architecture). Source lives in [11_AI_Forensic_System](#11_ai_forensic_system). Everything revolves around **evidence**.*

## 6.1 Architectural Principles
Everything revolves around evidence. Modules are loosely coupled and communicate through defined interfaces. The prediction model **never** makes the final decision. Uncertainty is never hidden; explanations are never fabricated; every conclusion traces to recorded evidence. Evidence collectors are **pluggable** and mutually independent, so Audio/Video/Text/Multimodal specialists can be added later without redesign ([Module 18](#module-18--future-modality-support)).

## 6.2 Pipeline
`Image Upload → Evidence Collection → Evidence Validation → Evidence Fusion → Reasoning → Decision → Explanation → Forensic Report → API Response → Frontend Visualization`.

## 6.3 Modules
Each module below is specified with Purpose · Inputs · Outputs · Dependencies · Failure Handling · Interfaces · Future Extensions. All modules are listed in the **Module Registry** `module_registry.csv` ([Module 17](#module-17--system-registry)).

### Module 1 — Input Management
Receive uploads; validate format/size/resolution/corruption; generate `Input ID`; store metadata; reject unsupported files. **Output:** `input_metadata.json`.

### Module 2 — Image Validation Engine
Verify integrity, supported format, corruption, color channels, resolution, compression, noise, missing data, quality, face availability. On failure → structured failure report ([Module 16](#module-16--failure-handling)); never silently continue.

### Module 3 — Evidence Acquisition Layer
Independent specialist collectors: Image Statistics, Metadata Collector, Face Detection, Face Quality, Frequency Domain, Compression Artifact Analysis, Color Distribution, Texture Analysis, Deep Learning Prediction ([Module 4](#module-4--deep-learning-specialist)), Explainability Inputs. **No collector depends on another.** New collectors register via a common `EvidenceCollector` interface.

### Module 4 — Deep Learning Specialist
<a id="module-4--deep-learning-specialist"></a>
Loads the trained FastAI model (from the [Model Registry](#model-registry)); performs **inference only**: probabilities, confidence, optional embeddings, prediction metadata, execution time. **Never decides.** Model is swappable behind the interface ([Model philosophy §1.7](#17-governing-philosophies)).

### Module 5 — Evidence Registry
<a id="evidence-registry"></a>
Every evidence item gets an `EVxxxxxx` ID. **Output:** the **Evidence Registry** `evidence_registry.csv` (`Evidence ID, Evidence Type, Source Module, Timestamp, Confidence, Description, Raw Output, Processed Output, Quality, Dependencies`). Everything traceable.

### Module 6 — Evidence Validation
Estimate reliability per item (low confidence, poor image quality, face-detection failure, incomplete metadata, model uncertainty, conflicting evidence). Evidence is never treated as uniformly reliable.

### Module 7 — Evidence Fusion Engine *(heart of the system)*
<a id="module-7--evidence-fusion-engine"></a>
Turns independent, validated evidence into one coherent conclusion via a **pluggable strategy interface** (rule-based → weighted → probabilistic/Bayesian/ensemble in future — [DEF-004](#111-deferred-decisions)). Accepts evidence from unlimited future modules. No single strategy is hardcoded.

### Module 8 — Decision Engine
Reads **validated evidence only** (never the image). Interprets fused evidence, estimates confidence, and determines: **Real / Fake / Inconclusive / Unknown**, with a reasoning path and decision metadata. **Output:** `decision.json`.

### Module 9 — Confidence Estimation
Separates confidence from raw softmax probability. Reports Prediction confidence, Evidence confidence, System confidence, Decision confidence, with documented interpretation. Softmax probability ≠ forensic certainty (see [Section 7, Phase 4](#phase-e4--calibration-analysis)).

### Module 10 — Explainability Engine
Interfaces for Grad-CAM, attention maps, saliency, integrated gradients (SHAP/LIME/counterfactuals future). **Output:** `explanation.json` (data only, no rendered images — [Figure Policy](#a9-canonical-figure-policy)).

### Module 11 — Forensic Reasoning Engine
Generates human-readable reasoning **derived from collected evidence** (e.g., "face detected; frequency artifacts present; prediction confidence high → evidence supports AI-generated origin"). Never invents explanations.

### Module 12 — Report Generator
Structured reports in JSON / Markdown / HTML (PDF future) using the [Case Report template](#template-24--forensic-case-report-case_reportmd). Includes Case ID, input summary, evidence summary, model results, confidence, explanation, decision, limitations, recommendations, execution stats, **System/Model/Dataset/Experiment versions, and Git commit** — everything needed for reproducibility.

### Module 13 — API Layer
Endpoints designed (not implemented) here; the canonical REST contract lives in [Section 8](#django-rest-api-contract): upload, status, prediction, evidence, explanation, report, history (future), health, version.

### Module 14 — Frontend Interaction
The experience is an **investigation**, not a verdict. Progress reads: *Uploading → Validating → Detecting Face → Running Analysis → Collecting Evidence → Evaluating Confidence → Generating Explanation → Preparing Report → Complete.* Avoid bare "Fake (99.8%)". Implemented in [Section 8](#8-web-application-architecture).

### Module 15 — Audit Trail
<a id="case-registry"></a>
Every investigation logs to the **Case Registry** `case_registry.csv` (`Case ID, Timestamp, Input, Evidence, Decision, Model, Version, Configuration, Execution Time, Errors, Warnings`). Everything auditable.

### Module 16 — Failure Handling
<a id="module-16--failure-handling"></a>
Structured handling for: no face, multiple faces, corrupted image, unsupported format, model unavailable, low confidence, timeout, unexpected error. Every failure → structured report; never silent.

### Module 17 — System Registry
<a id="module-17--system-registry"></a>
The **Module Registry** `module_registry.csv` (`Module ID, Responsibilities, Inputs, Outputs, Dependencies, Version, Status, Owner, Future Extensions`).

### Module 18 — Future Modality Support
<a id="module-18--future-modality-support"></a>
Interfaces already anticipate Audio/Video/Text specialists, multimodal fusion, knowledge graphs, and LLM reasoners — added by registering new collectors ([Module 3](#module-3--evidence-acquisition-layer)) and fusion strategies ([Module 7](#module-7--evidence-fusion-engine)) without core redesign.

### Module 19 — Forensic Agents
Input, Validation, Evidence, Fusion, Decision, Explanation, Report, Audit, API — specified in [Section 11](#11-agent-framework).

## 6.4 Forensic Analyst Definition of Done
Every module has one responsibility; every evidence item is traceable; every decision explainable; every report reproducible; every output versioned; every confidence value meaningful; every failure documented; every module independently replaceable; the architecture supports future modalities; the system behaves like a professional forensic platform. Plus the universal [DoD](#a5-canonical-definition-of-done).

---

# 7. Evaluation Protocol

> *Scientifically validates the detector, the [AI Forensic Analyst](#6-ai-forensic-analyst-architecture), and the full pipeline to peer-review standards. Consumes [Experiment](#experiment-registry)/[Model](#model-registry)/[Dataset](#dataset-registry) registries; produces the [Evaluation Registry](#evaluation-registry); feeds [Figures](#09_figures), [Tables](#10_tables), and the [Writing System](#9-writing-operating-system). Files live in [08_Evaluation](#08_evaluation).*

## 7.1 Phases

### Phase E1 — Evaluation Preparation
Verify experiment completed, model exported, dataset+split registered, predictions + ground truth available, config + checkpoint archived, Git commit recorded. **Reject incomplete experiments.**

### Phase E2 — Prediction Validation
Verify prediction/ground-truth counts, image IDs, duplicate/missing predictions, class labels, probability ranges, file integrity. **Output:** `prediction_validation_report.md`.

### Phase E3 — Classification Metrics
Accuracy, Precision, Recall, Specificity, Sensitivity, F1, Balanced Accuracy, MCC, ROC-AUC, PR-AUC, FPR, FNR, macro/micro/weighted averages. Each metric is documented with *when appropriate, how to interpret, common mistakes, publication recommendation*. **Never report Accuracy alone** (class imbalance is expected).

### Phase E4 — Calibration Analysis
<a id="phase-e4--calibration-analysis"></a>
Calibration curve, ECE, Maximum Calibration Error, reliability diagram, confidence distribution, Brier score. Distinguish **probability vs. confidence vs. reliability** — feeds [Module 9](#module-9--confidence-estimation).

### Phase E5 — Threshold Analysis
Threshold sweep; optimal-threshold selection (ROC/PR); operating-point trade-offs; application-specific threshold recommendations.

### Phase E6 — Confusion Analysis
Confusion matrix, per-class statistics, FP/FN case summaries, confusion trends, failure categories.

### Phase E7 — Robustness Evaluation
Perturbations: JPEG compression, Gaussian noise, blur, brightness, contrast, scaling, cropping, rotation, color perturbation, partial occlusion, low-quality uploads, resolution changes (adversarial future). Measure degradation, recovery, and failure patterns.

### Phase E8 — Generalization Evaluation
Cross-dataset, external datasets, different distributions, different generators, different preprocessing. **Never evaluate only on the training dataset.**

### Phase E9 — Unseen Generator Evaluation *(critical)*
Leave-one-generator-out: train without Generator X, test on Generator X (StyleGAN family, Stable Diffusion, Midjourney, FLUX, DALL·E, and future generators). **Generators are configuration, not hardcoded** — new ones are added by config.

### Phase E10 — Ablation Study
Systematic, question-driven ablations: without augmentation, without transfer learning, different image sizes/preprocessing/loss/optimizer, different evidence modules, different confidence estimation, different explainability. Every ablation answers one scientific question.

### Phase E11 — Statistical Testing
Confidence intervals, bootstrap, McNemar's test, paired comparisons, Wilcoxon, significance testing, variance reporting, multi-seed analysis, repeatability. **No superiority claim without statistical evidence.**

### Phase E12 — Failure Analysis
`failure_analysis.md` categorizing generator confusion, identity confusion, compression failure, poor quality, background influence, lighting, occlusion, artifacts, unexpected behavior. State *possible causes*, never invented conclusions.

### Phase E13 — Explainability Evaluation
Grad-CAM quality, attention consistency, saliency stability, explanation completeness, human interpretability (SHAP/LIME/counterfactuals future). Explainability itself is evaluated.

### Phase E14 — AI Forensic Analyst Evaluation *(the contribution)*
<a id="phase-e14--ai-forensic-analyst-evaluation"></a>
Evaluate evidence completeness, fusion quality, decision consistency, confidence consistency, report quality, reasoning quality, execution time, module failures, recovery behavior. Evaluate the **whole platform**, not just the model.

### Phase E15 — Performance Evaluation
Inference time, memory, GPU/CPU usage, batch throughput, latency, model size, disk usage, deployment suitability.

### Phase E16 — Comparison Study
<a id="phase-e16--comparison-study"></a>
Compare baselines vs. proposed model, architectures, preprocessing, datasets, and fusion strategies. **Outputs:** `comparison_tables.csv`, `comparison_report.md`. Only fairness-compatible experiments ([Section 5, Phase M2](#phase-m2--baseline-strategy)).

### Phase E17 — Publication Figures
Specs only ([Figure Policy](#a9-canonical-figure-policy)): ROC, PR, calibration, confusion matrix, metric comparison, training curve, loss curve, threshold curve, robustness curve, ablation chart.

### Phase E18 — Evaluation Registry
<a id="evaluation-registry"></a>
The **Evaluation Registry** `evaluation_registry.csv` (`Evaluation ID, Experiment, Dataset, Model, Metrics, Figures, Reports, Statistical Tests, Status, Version, Reviewer Notes`). Each evaluation is `EVAL0001`.

### Phase E19 — Evaluation Agents
Metric, Calibration, Robustness, Generalization, Ablation, Statistics, Comparison, Failure Analysis, Explainability, Reporting — specified in [Section 11](#11-agent-framework).

## 7.2 Evaluation Principles (binding)
Never report Accuracy alone; never cherry-pick the best run; never ignore failed experiments; never evaluate on one dataset or one seed; never modify evaluation after seeing results; never claim SOTA without objective evidence.

## 7.3 Evaluation Definition of Done
Every experiment evaluated consistently; every metric reproducible; every figure recreatable; every statistical claim supported; every failure documented; generalization, robustness, and calibration evaluated; the Forensic Analyst itself evaluated; publication-quality standards met. Plus the universal [DoD](#a5-canonical-definition-of-done).

---

# 8. Web Application Architecture

> *A production-quality research platform demonstrating the [AI Forensic Analyst](#6-ai-forensic-analyst-architecture). Frontend in [12_Web](#12_web); backend in [13_Backend](#13_backend); deployment in [14_Deployment](#14_deployment). **The backend owns the investigation; the frontend owns the experience.***

## 8.1 Separation of Concerns *(binding)*
The frontend **never** performs inference, contains model logic, or interprets probabilities — it only displays backend results. The backend owns evidence, inference, reasoning, decision, confidence, reports, versioning, and audit. Communication is exclusively via the documented API. API URLs are always configured, never hardcoded.

## 8.2 Data Flow
`Browser → React → API Client → Django REST API → AI Forensic Analyst → Inference → Evidence Fusion → Decision → Report → JSON Response → React Rendering`, asynchronous where appropriate (investigation is a polled/streamed job).

## 8.3 Frontend Architecture (React + Vite + Tailwind)
Structure under `12_Web/src/`: `pages/`, `layouts/`, `components/` (reusable), `hooks/`, `api/` (all fetch logic — never in components), `context/` (providers), `utils/`, `assets/`, `styles/` (Tailwind + theme tokens). Cross-cutting: routing, access control (future), error boundaries, loading states, future i18n, future dark mode, future mobile.

**Pages:** Landing, About Project, Investigation Dashboard, Image Upload, Investigation Progress, Evidence Viewer, Result Summary, Explanation Viewer, Report Viewer, System Information, Documentation, API Documentation, 404, Error pages; future Login/History/Admin. Each page defines purpose, components, API dependencies, navigation, and future extensions.

**Component library:** Navbar, Footer, Sidebar, Button, Card, Upload Area, Progress Indicator, Status Badge, Evidence Card, Confidence Gauge, Timeline, Accordion, Table, Modal, Toast, Alert, Loading Spinner, Empty State, Error State, Report Viewer, Image Viewer, Metric Card, Version Badge, Case Summary. Every component defines purpose, props, reusability, accessibility, and extensibility.

**State management:** global (theme, API status, future auth) vs. local (case/investigation/upload/error state). Avoid unnecessary global state.

## 8.4 Backend Architecture (Django + DRF)
Apps under `13_Backend/`: `api` (routing/serializers), `forensic_engine` (wraps the [AI Forensic System](#11_ai_forensic_system)), `evidence`, `reports`, `core` (config/utilities), `health`, `versioning`; future `accounts`, `history`, `analytics`. Plus `media/` handling, `static/`, admin, logging. Each app has a single responsibility.

## 8.5 Django REST API Contract
<a id="django-rest-api-contract"></a>
Canonical endpoints (documented via the [API Spec template](#template-16--api-specification-api_specmd)):

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/cases` | Create a case |
| GET | `/cases/{id}` | Case detail |
| POST | `/cases/{id}/upload` | Upload image for a case |
| GET | `/cases/{id}/status` | Investigation status (progress) |
| GET | `/cases/{id}/evidence` | Collected evidence |
| GET | `/cases/{id}/decision` | Decision + confidence |
| GET | `/cases/{id}/explanation` | Explanation data |
| GET | `/cases/{id}/report` | Forensic report |
| GET | `/health` | Health check |
| GET | `/version` | System/model/dataset versions + Git commit |

Future: authentication, history, user profiles, batch upload.

## 8.6 File Storage
Temporary uploads, per-case folders, generated reports, images, exports, logs, media — with a retention policy and cleanup strategy. **Uploaded files are never overwritten** (versioned per case). Media is never committed to Git ([Appendix A.7](#a7-canonical-ignore-policy)).

## 8.7 Error Handling
Handle network failures, timeouts, unsupported/corrupted uploads, backend unavailable, inference failure, report-generation failure, partial failures, validation errors. Show meaningful messages; **never expose stack traces to users**; log details server-side.

## 8.8 Security (right-sized)
Input + file validation, upload limits, rate limiting, CORS, CSRF, secrets via environment variables, logging; future auth/authz. Appropriate for an undergraduate research project while following good practice — do not over-engineer.

## 8.9 Configuration, Logging, Testing, Accessibility, Performance
- **Configuration:** environment-based (dev/test/prod), configured API URLs, model locations, media, logging, secrets; version tracking.
- **Logging:** application, API, inference, case, error, audit, performance logs with retention.
- **Testing:** frontend, backend, API, component, integration, manual, smoke, regression, UAT.
- **Accessibility:** keyboard nav, screen readers, semantic HTML, color contrast, focus management, responsive layouts, basic WCAG.
- **Performance:** lazy loading, code splitting, image optimization, efficient rendering, bundle organization, future API caching.

## 8.10 Deployment Readiness & Future Extensions
Dev/prod environments, Docker readiness, static/media handling, env config, health checks; future cloud deployment ([DEF-001](#111-deferred-decisions)). Extensible to Audio/Video/Text forensics, batch processing, accounts, case history, i18n, model switching, multiple specialists, cloud storage, enterprise dashboard — without major redesign.

## 8.11 Web Definition of Done
Frontend/backend responsibilities clearly separated; every page purposeful; every component reusable; every endpoint documented; the Forensic Analyst isolated behind the backend; both tiers independently evolvable; supports future modalities; maintainable, scalable, publication-quality. Plus the universal [DoD](#a5-canonical-definition-of-done).

---

# 9. Writing Operating System

> *A reproducible writing pipeline where **every paragraph originates from verified evidence**. Writing is the output of research, not where research happens. Consumes the [Claim Database](#claim-database), [Evaluation Registry](#evaluation-registry), [Figure specs](#09_figures), and literature outputs ([Section 3](#3-research--literature-workflow)). Files live in [15_Writing](#15_writing).*

## 9.1 Writing Philosophy
Never write from memory or assumption. Every sentence traces to downloaded literature, experiment results, evaluation reports, decision logs, research notes, the Claim Database, failure analyses, or the Research Gap Registry. **If supporting evidence does not exist, the sentence is not written.**

## 9.2 Phases

### Phase W1 — Evidence Collection
Gather from the literature database, paper summaries, Claim Database, Research Gap Registry, dataset reports, experiment reports, evaluation reports, failure reports, decision logs. Never start from a blank page.

### Phase W2 — Knowledge Organization
Categorize evidence: research questions, methodology, evaluation, related work, novelty, limitations, future work, contribution statements. **Output:** `knowledge_index.csv`.

### Phase W3 — Writing Database
<a id="writing-database"></a>
The **Writing Database** `writing_database.csv` (`Writing ID, Section, Topic, Supporting Papers, Supporting Experiments, Supporting Claims, Supporting Figures, Supporting Tables, Status, Last Updated, Owner, Revision Number`). This is the canonical traceability spine for prose.

### Phase W4 — Writing Templates
Reusable section templates (Abstract, Introduction, Related Work, Research Gap, Methodology, Dataset, Implementation, Evaluation, Results, Discussion, Conclusion, Future Work, Acknowledgements, Appendix, References), each defining purpose, required evidence, expected length, objectives, common mistakes, acceptance criteria.

### Phase W5 — Thesis Pipeline
Chapters: 1 Introduction, 2 Literature Review, 3 Methodology, 4 Implementation, 5 Evaluation, 6 Results, 7 Discussion, 8 Conclusion, plus Appendices and References. Each chapter defines purpose, inputs, outputs, required evidence, completion criteria.

### Phase W6 — Journal Pipeline
Sections: Abstract, Introduction, Related Work, Method, Experiments, Results, Discussion, Conclusion, References, Supplementary. Reuses the **same evidence base** as the thesis (see [§9.4](#94-thesis-vs-journal)).

### Phase W7 — Writing Rules
Formal academic tone; consistent terminology ([Appendix D](#appendix-d--glossary)); logical flow; objective, evidence-based language; clear transitions; no unnecessary repetition, exaggeration, marketing language, AI clichés, or unsupported statements. Prose should read as written by a careful human researcher; avoid gratuitous em-dashes and formulaic phrasing.

### Phase W8 — Figure Integration
Figures referenced by `FIG` ID + spec per the [Figure Policy](#a9-canonical-figure-policy); each is traceable to its source experiment and generation script.

### Phase W9 — Table Integration
Tables referenced by `TAB` ID + spec, each defining purpose, data source, supporting experiment, version, expected filename ([10_Tables](#10_tables)).

### Phase W10 — Citation Management
BibTeX (`references.bib`), citation keys, reference verification, duplicate detection, consistency, cross-references, updates. **Never invent citations** — the Citation Verification Agent checks every reference against the [Papers Registry](#papers-registry).

### Phase W11 — Claim Verification
<a id="phase-w11--claim-verification"></a>
Every claim is verified through the [Claim Database](#claim-database): supporting papers/experiments/figures/tables, contradicting evidence, confidence, page references. No unsupported claims survive review.

### Phase W12 — Writing Version Control
Draft/major/minor/reviewer/chapter/journal versions tracked with who/what/why/when/impact, using [SemVer](#a3-canonical-versioning-policy) for documents.

### Phase W13 — Revision Workflow
Self-review → supervisor review → grammar → technical → evidence → reference → formatting → final approval. Every revision documented.

### Phase W14 — Reviewer Response System
`review_response.md` ([template](#template-18--reviewer-response-review_responsemd)): reviewer comment, issue category, affected section, planned action, implemented change, evidence, response draft, status. Reviewer history is never lost.

### Phase W15 — Consistency Checking
Automatic checks for terminology, figure/table numbering, citation consistency, dataset/model names, experiment IDs, version numbers, abbreviations, section references.

### Phase W16 — Writing Agents
Outline, Evidence, Related Work, Methodology, Results, Discussion, Conclusion, Citation, Grammar, Consistency, Reviewer Response — specified in [Section 11](#11-agent-framework).

### Phase W17 — Writing Dashboard
`writing_progress.csv`: section completion, evidence completeness, missing figures/tables/citations, pending reviews, outstanding revisions, publication readiness. Feeds the [Productivity Dashboard](#phase-o16--productivity-dashboard).

### Phase W18 — Publication Readiness
Objective criteria: all experiments complete, figures finalized, tables verified, citations verified, grammar reviewed, references complete, supervisor approved, similarity checked, reproducibility verified, supplementary prepared. Scored by the [Publication Readiness checklist](#checklist-19--publication-readiness-score).

### Phase W19 — Archiving Policy
Draft/final/submitted/accepted/camera-ready versions and revision history preserved; finals move to [20_Archive](#20_archive); historical documents are never overwritten.

## 9.3 Scientific Writing Principles (binding)
Never fabricate results/citations/limitations; never exaggerate novelty; never hide failed experiments; never ignore contradictory evidence; never copy paper wording; never use AI filler. Honesty outranks persuasiveness.

## 9.4 Thesis vs. Journal
<a id="94-thesis-vs-journal"></a>
**Thesis:** comprehensive, educational, detailed implementation, extensive background. **Journal:** concise, novelty-focused, method-centric, high information density. Both draw from the same [Writing Database](#writing-database) and [Claim Database](#claim-database).

## 9.5 Writing Definition of Done
Every sentence evidence-originated; every claim traceable; every figure/table reproducible; every citation verified; thesis and journal share one knowledge base; reviewer responses documented; version history preserved; supports future publications. Plus the universal [DoD](#a5-canonical-definition-of-done).

---

# 10. GitHub + Kaggle + Antigravity Workflow

> *The Research Infrastructure & Synchronization Operating System coordinating Local ↔ GitHub ↔ Kaggle ↔ Antigravity. **GitHub is the single source of truth.** Canonical storage tiers and Git rules are in [Appendix A.6](#a6-canonical-storage--synchronization-policy).*

## 10.1 Core Philosophy & Platform Responsibilities
`Local Repository → GitHub → Kaggle → GitHub → Local Repository`. No important work exists only in Kaggle or only locally. Responsibilities are fixed: **Cursor** = planning only; **Antigravity** = implementation; **GitHub** = version control / source of truth; **Kaggle** = training; **Human** = scientific decisions. No platform assumes another's role. Antigravity **never** becomes the source of truth.

## 10.2 Phases

### Phase 1 — Repository Initialization
Structure per [Section 2](#2-repository-architecture); branch model per [Phase 4](#phase-4--branch-strategy); tagging per [SemVer](#a3-canonical-versioning-policy); branch protection recommended on `main` and `develop`.

### Phase 2 — Development Workflow
`Planning (Cursor) → Approved Plan → Implementation (Antigravity) → Testing → Documentation → Commit → Push`. Every platform's responsibility is explicit.

### Phase 3 — Commit Policy
Conventional-style prefixes: `feat:`, `fix:`, `docs:`, `refactor:`, `research:`, `experiment:`, `dataset:`, `evaluation:`, `writing:`, `deployment:`, `config:`, `chore:`. Commit when a unit of work is complete, documented, and reproducible. **Never** commit secrets, virtual environments, caches, large binaries (use the [artifact tier](#a6-canonical-storage--synchronization-policy)), or partial/broken work to shared branches.

### Phase 4 — Branch Strategy
<a id="phase-4--branch-strategy"></a>
`main` (protected, releasable) · `develop` (integration) · `feature/*` · `experiment/*` · `hotfix/*` · `release/*` · `writing/*` · `research/*`. Merge into `develop` via reviewed PR; `develop → main` at releases. Delete merged branches (cleanup). Approval requirements are set by the human.

### Phase 5 — GitHub Repository Policy
`README`, `LICENSE`, `CONTRIBUTING`, `CHANGELOG`, `CODEOWNERS`, issue templates, PR templates, release notes, project boards, milestones.

### Phase 6 — Google Antigravity Workflow
Clone → environment setup → implement feature → test → document → prepare commit → (optional) PR → code review → sync. Antigravity implements the specs written in Cursor.

### Phase 7 — Kaggle Training Workflow
<a id="phase-7--kaggle-training-workflow"></a>
`Start session → clone repo → verify environment → download dataset → download checkpoints → verify config → resume experiment → train → evaluate → export artifacts → upload outputs → push metadata → shutdown`. Designed to survive time limits (ties to [Section 5, Phases M7–M8](#phase-7--checkpoint-management-critical)).

### Phase 8 — Checkpoint Recovery
<a id="phase-8--checkpoint-recovery"></a>
Automatic checkpoint detection, resume policy, checkpoint validation, recovery procedure, failure handling, best-model + last-checkpoint policies, experiment continuity. Nothing important is lost.

### Phase 9 — Artifact Management
Categories: model weights, `export.pkl`, training logs, predictions, metrics, config, learning curves, evaluation reports, failure reports, generated tables/data. Every artifact versioned and placed in the correct [storage tier](#a6-canonical-storage--synchronization-policy).

### Phase 10 — Synchronization Strategy
<a id="phase-10--synchronization-strategy"></a>
**Always syncs (Git):** source code, configs, documentation, registries, experiment metadata, small predictions, reports. **Syncs after experiments (artifact tier / Releases):** checkpoints, weights, large predictions. **Never syncs:** secrets, virtualenvs, caches, notebook outputs, temporary files, raw image data (Kaggle Datasets instead). Governed by [Appendix A.6](#a6-canonical-storage--synchronization-policy).

### Phase 11 — Git LFS Strategy
Use Git LFS only for medium binary artifacts that must be versioned in-repo (e.g., a small canonical exported model) when Releases are unsuitable. Never LFS for raw datasets or large weight collections (those go to Kaggle Datasets / GitHub Releases). Keep repository size small.

### Phase 12 — Release Workflow
<a id="phase-12--release-workflow"></a>
`v0.1` research prototype · `v0.5` internal evaluation · `v1.0` thesis submission · `v1.1` journal revision · `v2.0` future multimodal. Each release bundles source snapshot, key artifacts (Releases), documentation, and a CHANGELOG entry; finals archived to [20_Archive](#20_archive).

### Phase 13 — Experiment Synchronization
Each `EXPxxxx` → creates metadata → updates the [Experiment Registry](#experiment-registry) → stores checkpoints → updates the [Model Registry](#model-registry) → updates the [Evaluation Registry](#evaluation-registry) → updates writing evidence ([Writing Database](#writing-database)).

### Phase 14 — Issue Management
Categories: Bug, Dataset, Experiment, Writing, Documentation, Architecture, Deployment, Evaluation, Research, Enhancement — with priority, status, milestones.

### Phase 15 — Documentation Workflow
Every important change updates documentation ([16_Documentation](#16_documentation)); documentation never goes stale ([Documentation checklist](#checklist-12--documentation)).

### Phase 16 — Environment Management
Pin Python/FastAI/PyTorch/CUDA in `environment/versions.lock.md`; lock dependencies; separate `kaggle-requirements.txt`; future Docker. Configuration is reproducible.

### Phase 17 — Backup Strategy
Local backups, GitHub as canonical remote, artifact backups, checkpoint backups, experiment reports, writing; documented recovery and disaster-recovery procedures.

### Phase 18 — Automation
Automate: repository validation, experiment registration, config validation, documentation generation, artifact verification, registry updates, health checks, sync reminders. **Never automate scientific decisions** ([§1.9](#19-human-in-the-loop-rule)).

### Phase 19 — Platform Responsibilities
Restated authoritatively in [§10.1](#101-core-philosophy--platform-responsibilities).

## 10.3 Infrastructure Rules (binding)
Never develop directly in Kaggle; never edit code only in notebooks; never overwrite checkpoints; never lose experiment metadata; never commit secrets/venvs/caches; never modify previous experiment configs; never allow repository drift between platforms; always document major architectural changes.

## 10.4 Infrastructure Definition of Done
Every experiment reproducible; every artifact traceable; every checkpoint recoverable; every implementation version-controlled; every sync documented; every platform single-responsibility; GitHub remains source of truth; supports future research (CI/CD, Docker, cloud GPU, Hugging Face Hub, multiple researchers) without redesign. Plus the universal [DoD](#a5-canonical-definition-of-done).

---

# 11. Agent Framework

> *The virtual research laboratory. **One agent, one responsibility.** Agents never overlap and communicate **only through repository files** — never hidden conversation memory ([§1.7 Agent philosophy](#17-governing-philosophies)). Every agent is specified with the [Agent template](#template-27--agent-specification-agentmd).*

## 11.1 Canonical Agent Contract
Every agent defines: **Agent Name · Mission · Purpose · Primary Responsibilities · Allowed Responsibilities · Forbidden Responsibilities · Inputs · Outputs · Folder Access · Files Generated · Files Consumed · Dependencies · Workflow Position · Decision Authority · Escalation Rules · Failure Handling · Quality Checklist · Definition of Done · Example Task · Example Output · Prompt Template.** Agents escalate to the human for any irreversible scientific decision ([§1.9](#19-human-in-the-loop-rule)).

## 11.2 Agent Registry (by domain)

**Literature ([Section 3](#3-research--literature-workflow)):**
| Agent | Single Responsibility | Must NOT |
|---|---|---|
| Literature Search | Search, filter, rank, collect papers | Summarize or download |
| Paper Registration | Maintain `papers.csv` | Download or summarize |
| Metadata Extraction | Extract structured fields | Write prose |
| Paper Summary | Structured per-paper notes | Invent content |
| Relationship | Build relationship graph from metadata | Guess relationships |
| Research Gap | Extract + rank gaps from evidence | Invent gaps |
| Trend Analysis | Detect research trends | Recommend direction |
| Research Planning | Propose candidate directions | Select the final topic |
| Citation Verification | Verify references | Add citations that lack a `P` ID |
| Knowledge Base | Maintain Claim Database + indexes | Alter source papers |

**Dataset ([Section 4](#4-dataset-operating-system)):** Discovery, Evaluation, Metadata, Validation, Quality, Preprocessing, Split, Statistics, Documentation, Registry.

**Model ([Section 5](#5-model-development-operating-system)):** Model Discovery, Training, Checkpoint, Experiment, Evaluation Trigger, Failure Analysis, Registry, Comparison, FastAI Configuration.

**Forensic ([Section 6](#6-ai-forensic-analyst-architecture)):** Input, Validation, Evidence, Fusion, Decision, Explanation, Report, Audit, API.

**Evaluation ([Section 7](#7-evaluation-protocol)):** Metric, Calibration, Robustness, Generalization, Ablation, Statistics, Comparison, Failure Analysis, Explainability, Reporting.

**Web ([Section 8](#8-web-application-architecture)):** Frontend Architect, Backend Architect, API Designer, Component Designer, State Manager, Documentation, Testing, Deployment, Security Review.

**Writing ([Section 9](#9-writing-operating-system)):** Outline, Evidence, Related Work, Methodology, Results, Discussion, Conclusion, Citation, Grammar, Consistency, Reviewer Response.

**Operations ([Section 12](#12-daily-research-operating-workflow)):** Planning, Task Prioritization, Research Coordinator, Engineering Coordinator, Training Coordinator, Writing Coordinator, Documentation Coordinator, Progress Tracker, Risk Monitor, Review.

**Quality Assurance ([Section 13](#13-quality-assurance)):** Repository Auditor, Literature Auditor, Dataset Auditor, Experiment Auditor, Evaluation Auditor, Writing Auditor, Documentation Auditor, Security Auditor, Architecture Auditor, Publication Auditor.

## 11.3 Agent Rules (binding)
Single responsibility; well-defined inputs/outputs; failure recovery; quality validation; communication through repository files only; escalate irreversible scientific decisions to the human.

---

# 12. Daily Research Operating Workflow

> *The official daily operating procedure. The objective is **measurable research progress**, not busyness. Reads/writes [01_Project_Management](#01_project_management); coordinated by Operations agents ([Section 11](#11-agent-framework)).*

## 12.1 Phases

### Phase O1 — Daily Startup
Checklist: open repository, review yesterday's `daily_review.md`, review the [dashboard](#phase-o16--productivity-dashboard), review outstanding tasks, check experiment status, check documentation, verify Git status, review priorities, define today's single objective.

### Phase O2 — Daily Planning
Produce `daily_plan.md` (today's objective, tasks, dependencies, expected outputs, estimated duration, potential risks) via task selection, priority ranking, dependency mapping, effort estimation, and success criteria.

### Phase O3 — Work Classification
Classify the day: Research / Engineering / Training / Evaluation / Writing / Documentation / Review / Maintenance. **Never mix unrelated work in one focused session.**

### Phase O4 — Focused Work Sessions
Each block has one objective, one deliverable, one validation step, one documentation step. No multitasking.

### Phase O5 — Experiment Day
Verify dataset → verify config → verify checkpoint → launch training → monitor → record observations → save checkpoints → update the [Experiment Registry](#experiment-registry) → sync outputs. Never launch training unprepared.

### Phase O6 — Engineering Day
Review architecture → implement one feature → run tests → review code → update documentation → commit → push. Never implement without documentation.

### Phase O7 — Research Day
Paper selection → registration → metadata extraction → structured summary → gap extraction → knowledge-base update → citation verification → update `reading_progress.csv`.

### Phase O8 — Writing Day
Gather evidence → verify claims → write section → verify citations → update figures/tables → consistency review → revision tracking. Never write unsupported content.

### Phase O9 — Documentation Workflow
Every completed task updates the relevant documentation and registry. Documentation is part of the work.

### Phase O10 — Quality Check
End-of-day validation: code reviewed, experiment reproducible, documentation updated, files organized, registries updated, naming conventions followed, outstanding issues recorded.

### Phase O11 — Repository Synchronization
Git status → review changes → meaningful commit → push → verify sync → update dashboard. Never end the day with untracked important work.

### Phase O12 — Daily Review
Produce `daily_review.md`: tasks completed/postponed, problems, decisions, lessons, risks, supervisor questions, overall progress.

### Phase O13 — Next-Day Preparation
Prepare tomorrow's priorities, required files/datasets/papers/checkpoints, blocked tasks, dependencies. Reduce startup friction.

### Phase O14 — Weekly Review
`weekly_review.md`: research/engineering/experiment/writing progress, documentation quality, repository health, technical debt, open risks.

### Phase O15 — Monthly Review
`monthly_review.md`: milestones, research direction, publication readiness, architecture health, dataset growth, experiment quality, writing completeness, future priorities.

### Phase O16 — Productivity Dashboard
<a id="phase-o16--productivity-dashboard"></a>
`dashboard_status.md`: current phase, active experiment, current dataset, writing progress, pending reviews, open issues, milestone completion, risk indicators, publication readiness. Aggregates the [Writing Dashboard](#phase-w17--writing-dashboard) and registries.

### Phase O17 — Daily Agents
Operations agents listed in [Section 11](#11-agent-framework).

### Phase O18 — Failure Recovery
For training interrupted, implementation blocked, dataset issue, missing paper, merge conflict, corrupted checkpoint, lost progress, unexpected errors: end each with documented cause, recovery plan, and preventive action.

### Phase O19 — Time Allocation Guidelines
Flexible effort distribution by project stage (literature-heavy, experiment-heavy, implementation-heavy, writing-heavy, revision). No rigid hours prescribed.

## 12.2 Daily Deliverable Policy
Every working day produces ≥1 meaningful deliverable (paper summary, experiment result, dataset validation, feature, endpoint, evaluation report, figure spec, writing section, documentation update, or registry update). Days with no demonstrable output are investigated and the reason recorded.

## 12.3 Daily Definition of Done
Every day has an objective; every completed task is documented; every experiment synchronized; every decision recorded; every registry updated; repository organized; next day prepared; progress measurable. Plus the universal [DoD](#a5-canonical-definition-of-done).

---

# 13. Quality Assurance

> *The Research QA Operating System. Every phase must pass an objective checklist — **PASS or FAIL, no subjective judgment** — before progress continues. QA is enforced by [phase gates](#132-quality-gates) and QA agents ([Section 11](#11-agent-framework)). A checklist is not documentation; it tests whether documentation is sufficient.*

## 13.1 Master Checklists
Each checklist defines Purpose, Items, Evidence Required, Responsible Agent, Human Verification, Acceptance Criteria, Failure Conditions, Common Mistakes, DoD, Escalation. Summarized here; full items are enumerated within the referenced sections.

### Checklist 1 — Repository Readiness
Structure, README, license, folder organization, `.gitignore`, versioning, naming conventions, documentation, branch structure, repository health, no [forbidden names](#24-repository-hygiene-rules). → gates [Section 2](#2-repository-architecture).

### Checklist 2 — Literature Review
Research question, search strategy, paper registration, metadata, summaries, research gaps, Claim Database, knowledge index, citation verification, related-work completeness. → gates [Section 3](#3-research--literature-workflow).

### Checklist 3 — Dataset Readiness
Registered, license verified, metadata complete, validation done, integrity/quality/dataset reports, version assigned, preprocessing documented, split documented, no leakage. → gates [Section 4](#4-dataset-operating-system).

### Checklist 4 — Preprocessing
Pipeline registered, parameters recorded, outputs documented, version assigned, raw untouched, processed reproducible, config stored.

### Checklist 5 — Experiment Readiness
Dataset version, split version, config, random seed, model version, experiment ID, hardware, checkpoint location, output folders, expected metrics, research question — **before** training.

### Checklist 6 — Training Completion
Training finished, logs saved, metrics recorded, checkpoints exported, config archived, learning curves generated, summary written, registry updated, Git synchronized.

### Checklist 7 — Checkpoint Integrity
<a id="checklist-7--checkpoint-integrity"></a>
Best model, last checkpoint, optimizer state, scheduler state, epoch, resume capability, export model, version consistency, checksum.

### Checklist 8 — Evaluation
Metrics complete, ROC/PR/confusion data, calibration, statistical testing, robustness, generalization, ablation, failure analysis, comparison report. → gates [Section 7](#7-evaluation-protocol).

### Checklist 9 — AI Forensic Analyst
Evidence collection, validation, fusion, decision, confidence, explanation, report generation, API integration, failure handling, audit trail. → gates [Section 6](#6-ai-forensic-analyst-architecture).

### Checklist 10 — Frontend
Pages, components, accessibility, responsive design, loading states, error handling, API integration, navigation, documentation.

### Checklist 11 — Backend
REST API, validation, logging, configuration, media handling, security, versioning, documentation, health endpoint.

### Checklist 12 — Documentation
<a id="checklist-12--documentation"></a>
Architecture, API, README, developer guide, user guide, workflow, folder explanations, decision logs, experiment registry.

### Checklist 13 — Writing Readiness
Claims supported, figures/tables available, citations verified, references complete, terminology consistent, grammar reviewed, formatting reviewed, supervisor notes addressed.

### Checklist 14 — Figure Quality
Figure ID, caption, source experiment, source notebook, axis labels, units, legend, resolution, reproducibility, referenced in writing ([Figure Policy](#a9-canonical-figure-policy)).

### Checklist 15 — Table Quality
Table ID, title, source, supporting experiment, formatting, consistency, units, referenced in writing.

### Checklist 16 — Journal Submission
Abstract, keywords, novelty, contribution, references, formatting, supplementary material, reproducibility, code availability, data availability, author checklist.

### Checklist 17 — Thesis Submission
All chapters, figures, tables, references, appendices complete; formatting; supervisor approval; grammar review; similarity check; final PDF; repository archived.

### Checklist 18 — Project Completion
Source code, documentation, datasets, models, experiments, evaluation, writing, deployment, presentation, backup, repository health, everything archived.

### Checklist 19 — Publication Readiness Score
<a id="checklist-19--publication-readiness-score"></a>
Weighted score across Research Quality, Engineering Quality, Reproducibility, Documentation, Writing, Evaluation, Novelty, Software Quality, Scientific Integrity → `publication_readiness_report.md` with category scores, overall readiness, critical issues, recommended actions, PASS/FAIL.

### Checklist 20 — Definition of Done
The universal template lives in [Appendix A.5](#a5-canonical-definition-of-done); every task answers its eight questions.

## 13.2 Quality Gates
<a id="132-quality-gates"></a>
Mandatory gates between phases: `Literature → Dataset → Experiment → Evaluation → Writing → Submission`. **No phase begins until the previous gate passes.** Each gate is the corresponding checklist above.

## 13.3 Audit Reports
Standard reports (using the [Audit report structure](#a10-canonical-audit-report-structure)): `repository_audit.md`, `dataset_audit.md`, `experiment_audit.md`, `evaluation_audit.md`, `writing_audit.md`, `publication_audit.md` — each with Summary, Passed, Failed, Evidence, Recommendations, Approval Status.

## 13.4 Risk Register
`risk_register.csv` (`Risk ID, Description, Probability, Impact, Owner, Mitigation, Status, Review Date`), reviewed in [weekly/monthly reviews](#phase-o14--weekly-review).

## 13.5 QA Principles (binding)
Never mark incomplete work complete; never bypass a failed checklist; never hide failed experiments; never ignore missing documentation; never submit unsupported claims; never sacrifice reproducibility. Every completed task is independently verifiable. Integrity outranks speed.

---

# 14. Template Library

> *Standardizes every recurring document so nothing starts from a blank page. Templates live in [18_Templates](#18_templates); instances live in their domain folders. Every template obeys the [naming rules](#a2-canonical-file-naming-rules) and, where it produces a registry, the [registry format](#a11-canonical-registry-format).*

## 14.1 Template Contract
Each template defines: **Template Name · Purpose · When Used · Owner · Inputs · Outputs · Required Sections · Optional Sections · Validation Rules · Naming Convention · Folder Location · Example Usage · Definition of Done · Common Mistakes · Related Templates.**

## 14.2 The Templates

- **Template 1 — README.md**: Purpose, project description, repository structure, installation, quick start, folder guide, workflow, dependencies, license, citation, contact. → [Section 2 / README policy](#a4-canonical-readme-policy).
- **Template 2 — Paper Summary (`paper_summary.md`)**: fields per [Phase L5](#phase-l5--paper-reading-workflow). → [02_Literature](#02_literature).
- **Template 3 — Decision Log (`decision.md`)**: Decision ID, Date, Problem, Options, Chosen Option, Rejected Options, Reason, Expected Impact, Supporting Evidence, Future Review. → [§1.7](#17-governing-philosophies), [§1.11](#111-deferred-decisions).
- **Template 4 — Research Diary (`daily_research.md`)**: Date, Objective, Completed Work, Problems, Lessons, Ideas, Questions, Next Actions. → [Section 12](#12-daily-research-operating-workflow).
- **Template 5 — Dataset Report (`dataset_report.md`)**: → [Phase D8](#phase-d8--dataset-documentation).
- **Template 6 — Preprocessing Report (`preprocessing_report.md`)**: → [Phase D11](#phase-d11--processed-dataset-generation).
- **Template 7 — Experiment README (`experiment_readme.md`)**: Experiment ID, Research Question, Hypothesis, Dataset, Model, Configuration, Results, Failures, Observations, Conclusion, Next Experiment. → [06_Experiments](#06_experiments).
- **Template 8 — Configuration (`config.yaml`)**: sections per [Phase M4](#phase-m4--configuration-system).
- **Template 9 — Failure Report (`failure_report.md`)**: Failure ID, Experiment, Symptoms, Root Cause, Evidence, Impact, Resolution, Preventive Action, Status. → [Phase M14](#phase-m14--failure-analysis).
- **Template 10 — Evaluation Report (`evaluation_report.md`)**: → [Section 7](#7-evaluation-protocol).
- **Template 11 — Figure Specification (`figure_spec.md`)**: → [Figure Policy](#a9-canonical-figure-policy).
- **Template 12 — Table Specification (`table_spec.md`)**: → [10_Tables](#10_tables).
- **Template 13 — Claim Record (`claim.md`)**: expands one row of the [Claim Database](#claim-database).
- **Template 14 — Research Gap (`gap.md`)**: Gap ID, Category, Supporting Papers, Frequency, Importance, Potential Contribution, Implementation Difficulty, Publication Potential. → [Phase L8](#phase-l8--research-gap-discovery-most-important).
- **Template 15 — Architecture Decision Record (`adr.md`)**: ADR ID, Context, Decision, Alternatives, Trade-offs, Consequences, Status.
- **Template 16 — API Specification (`api_spec.md`)**: Endpoint, Method, Purpose, Request, Response, Errors, Authentication, Examples, Version. → [Section 8](#django-rest-api-contract).
- **Template 17 — Module Specification (`module_spec.md`)**: Module ID, Purpose, Inputs, Outputs, Dependencies, Configuration, Testing, Future Extensions. → [Section 6](#6-ai-forensic-analyst-architecture).
- **Template 18 — Reviewer Response (`review_response.md`)**: → [Phase W14](#phase-w14--reviewer-response-system).
- **Template 19 — Meeting Notes (`meeting.md`)**: Date, Participants, Agenda, Discussion, Decisions, Action Items, Deadlines.
- **Template 20 — Supervisor Meeting (`supervisor_meeting.md`)**: Questions, Progress, Problems, Feedback, Decisions, Next Steps.
- **Template 21 — Milestone Report (`milestone.md`)**: Milestone, Objectives, Completed, Pending, Risks, Deliverables, Next Milestone.
- **Template 22 — Model Card (`model_card.md`)**: Model ID, Architecture, Training Data, Evaluation, Limitations, Bias, Intended Use, Not Recommended For, Version. → [Model Registry](#model-registry).
- **Template 23 — Dataset Card (`dataset_card.md`)**: Dataset ID, Origin, License, Collection Method, Statistics, Bias, Ethics, Recommended Usage, Limitations. → [Section 4](#4-dataset-operating-system).
- **Template 24 — Forensic Case Report (`case_report.md`)**: Case ID, Input Summary, Evidence, Decision, Confidence, Reasoning, Explanation, Limitations, System Version, Model Version. → [Module 12](#module-12--report-generator).
- **Template 25 — Submission Checklist (`submission.md`)**: Requirements, Completed, Pending, Evidence, Approval, Status.
- **Template 26 — Prompt Template (`prompt.md`)**: Purpose, Role, Context, Inputs, Outputs, Constraints, Expected Result, Version. → [19_Prompts](#19_prompts).
- **Template 27 — Agent Specification (`agent.md`)**: the [Agent contract](#111-canonical-agent-contract). → [Section 11](#11-agent-framework).
- **Template 28 — Registry Record (`registry.md`)**: Record ID, Owner, Version, Dependencies, Status, Created, Updated. → [Appendix A.11](#a11-canonical-registry-format).
- **Template 29 — Risk Assessment (`risk.md`)**: Risk ID, Description, Probability, Impact, Mitigation, Owner, Review Date. → [§13.4](#134-risk-register).
- **Template 30 — Deployment Report (`deployment.md`)**: Version, Environment, Configuration, Verification, Rollback Plan, Known Issues, Release Notes. → [14_Deployment](#14_deployment).

## 14.3 Template Validation, Versioning, Automation
- **Validation:** required fields present, unique IDs, naming consistency, valid cross-references, version consistency, completeness, traceability.
- **Versioning:** [SemVer](#a3-canonical-versioning-policy) with a changelog per template; track changes, reasons, compatibility, migration.
- **Automation matrix (per template):** whether the AI can generate it, whether it requires human review, whether it is partially automatable, whether it requires supervisor approval, and whether it can be validated automatically. As a rule: registries and reports are AI-generatable + auto-validatable; decision logs, ADRs, research directions, and any scientific-direction document **require human approval**.

## 14.4 Template Relationship Map
`Experiment → Evaluation → Figures/Tables → Claims → Writing → Journal → Reviewer Response`. Everything remains traceable through the shared [Claim Database](#claim-database) and [Writing Database](#writing-database) (full map in [Appendix C](#appendix-c--cross-reference-map)).

---

# Appendix A — Canonical Definitions

> *These rules are defined once and referenced everywhere. Any section that mentions IDs, naming, versioning, README, DoD, storage, ignore rules, human tasks, figures, audits, or registry format is bound by this appendix.*

## A.1 Canonical Identifier Scheme
Zero-padded, prefix-based, immutable once assigned. IDs are never reused, even after deletion/archival.

| Entity | Prefix | Example | Assigned by | Registry |
|---|---|---|---|---|
| Research paper | `P` (4 digits) | `P0042` | Paper Registration Agent | [papers.csv](#papers-registry) |
| Dataset | `DS` (4) | `DS0001` | Metadata Agent | [dataset_registry.csv](#dataset-registry) |
| Preprocessing pipeline | `PP` (4) | `PP0003` | Preprocessing Agent | preprocessing_registry.csv |
| Split | `SPLIT` (4) | `DS0001_PP0001_SPLIT0001` | Split Agent | dataset_registry.csv |
| Experiment | `EXP` (4) | `EXP0007` | Experiment Agent | [experiment_registry.csv](#experiment-registry) |
| Run (within experiment) | `RUN` (4) | `RUN0002` | Training Agent | experiment folder |
| Checkpoint | `CKPT` (4) | `CKPT0005` | Checkpoint Agent | checkpoint manifest |
| Model | `MODEL` (4) | `MODEL0001` | Registry Agent | [model_registry.csv](#model-registry) |
| Evaluation | `EVAL` (4) | `EVAL0001` | Reporting Agent | [evaluation_registry.csv](#evaluation-registry) |
| Evidence item | `EV` (6) | `EV000123` | Evidence Registry ([Module 5](#module-5--evidence-registry)) | evidence_registry.csv |
| Forensic case | `CASE` (6) | `CASE000045` | Audit Agent | [case_registry.csv](#case-registry) |
| Module | `MOD` (3) | `MOD012` | Systems Architect | [module_registry.csv](#module-17--system-registry) |
| Figure | `FIG` (4) | `FIG0011` | Figure Agent | figure specs |
| Table | `TAB` (4) | `TAB0008` | Table Agent | table specs |
| Report | `REPORT` (4) | `REPORT0003` | relevant agent | domain folder |
| Research gap | `GAP` (4) | `GAP0002` | Research Gap Agent | research_gap.csv |
| Claim | `CLAIM` (4) | `CLAIM0015` | Knowledge Base Agent | [claim_database.csv](#claim-database) |
| Decision | `DEC` (4) | `DEC0009` | author | decision log |
| Risk | `RISK` (4) | `RISK0004` | Risk Monitor | risk_register.csv |
| Writing unit | `WR` (4) | `WR0021` | Writing agents | [writing_database.csv](#writing-database) |

## A.2 Canonical File Naming Rules
- **General:** lowercase `snake_case` for code, config, and generated files; ID-prefixed for registered artifacts (`P0042.pdf`, `EXP0007/config.yaml`). No spaces, no uppercase in filenames except acknowledged constants (`README.md`, `LICENSE`, `CHANGELOG.md`, `CODEOWNERS`).
- **Markdown:** `snake_case.md`; instance files carry their ID (`P0042_summary.md`, `DEC0009.md`).
- **Python:** `snake_case.py`, packaged into importable modules (never one-off scripts in random places).
- **Notebooks:** `EXPxxxx_<purpose>.ipynb`, stored in the owning experiment's `notebook/` folder; outputs stripped before commit ([A.7](#a7-canonical-ignore-policy)).
- **CSV/JSON/YAML:** `snake_case` describing content (`experiment_registry.csv`, `input_metadata.json`, `config.yaml`).
- **PDF:** papers are `Pxxxx.pdf` only; other PDFs are `snake_case.pdf`.
- **PNG/JPG (figures):** `FIGxxxx_v<major>.png`; source-of-truth vector as `.svg`/`.pdf` where possible.
- **Model weights / FastAI exports:** `MODELxxxx_export.pkl`, `MODELxxxx_weights.pth`, `EXPxxxx_best.pth`, `EXPxxxx_last.pth`.
- **Logs:** `EXPxxxx_<stage>.log`.
- Inconsistent naming is a [Repository Readiness](#checklist-1--repository-readiness) failure.

## A.3 Canonical Versioning Policy
Semantic Versioning `vMAJOR.MINOR.PATCH` applies uniformly to: datasets, models, experiments (as immutable IDs plus config version), prompts, documentation, writing, figures, and this handbook.
- **MAJOR:** breaking/structural change (schema change, incompatible data change, redesign).
- **MINOR:** backward-compatible addition (new field, new pipeline, new template).
- **PATCH:** fixes/clarifications with no structural effect.
Datasets may use the short form `v1.0/v1.1/v2.0`; documents use full `vX.Y.Z`. Experiments are **immutable once run** — a change means a *new* `EXP` ID, never an edit.

## A.4 Canonical README Policy
Every folder contains `README.md` stating: **Purpose · Contents · Workflow · Owner · Related folders · Expected outputs.** READMEs are generated from [Template 1](#template-1--readmemd) and kept current as part of the [Documentation Workflow](#phase-15--documentation-workflow).

## A.5 Canonical Definition of Done
A task is **Done** only when all eight are true (this is [Checklist 20](#checklist-20--definition-of-done)):
1. The objective was completed.
2. The work is reproducible.
3. Documentation is complete.
4. The relevant registry is updated.
5. The repository is synchronized (committed + pushed).
6. Quality has been verified (relevant checklist PASS).
7. Another researcher could reproduce the work.
8. It would survive peer review.
Every phase-specific DoD in Sections 3–13 is **in addition to** these eight.

## A.6 Canonical Storage & Synchronization Policy
Three storage tiers determine where every artifact lives:

| Tier | Contents | Location | In Git? |
|---|---|---|---|
| **Source tier** | code, configs, registries, metadata, reports, small indexes, documentation, prompts, templates, figure/table specs | GitHub repo | Yes |
| **Artifact tier** | model weights, `export.pkl`, checkpoints, large predictions | GitHub Releases / Git LFS (small) / Kaggle output | Pointer only |
| **Data tier** | raw + processed image datasets | Kaggle Datasets / external storage | No (metadata only) |

**Never committed:** secrets/`.env`, virtualenvs, caches, notebook outputs, `__pycache__`, OS files, node_modules, media uploads, raw datasets, large binaries. Synchronization frequency and rules are in [Section 10, Phase 10](#phase-10--synchronization-strategy).

## A.7 Canonical Ignore Policy
`.gitignore` covers: Python (`__pycache__/`, `*.pyc`, `.venv/`, `env/`, `*.egg-info/`), Node (`node_modules/`, `dist/`, `.vite/`), FastAI/training outputs (`models/`, `*.pth`, `*.pkl` except explicitly tracked exports via `.gitattributes`), notebook checkpoints (`.ipynb_checkpoints/`), caches (`.cache/`, `.pytest_cache/`), OS files (`.DS_Store`, `Thumbs.db`), secrets (`.env`, `*.key`, `credentials*.json`), media (`13_Backend/media/`, uploads), and raw/processed data paths. `.gitattributes` declares Git LFS tracking and normalized line endings.

## A.8 Human Task Protocol
Whenever human action is required, the workflow **stops** and provides: **(1) Why** it is needed, **(2) Exactly what** to do, **(3) Exactly where** files go (absolute path within the [folder structure](#22-top-level-directory-tree)), **(4) Exactly what** the expected output is, and **(5) How** to confirm success. See [§1.9](#19-human-in-the-loop-rule).

## A.9 Canonical Figure Policy
The AI **never renders publication figures**. Whenever a figure is required, it produces a **specification** ([Template 11](#template-11--figure-specification-figure_specmd)) containing: Figure ID (`FIGxxxx`), Purpose, Required data (with source experiment/evaluation), Recommended chart type, Exact axes (+units), Legend, Caption, Color recommendations, Data source path, Responsible notebook/script, Manual creation instructions, Expected output filename. This lets the human recreate figures consistently and keeps every figure traceable ([Checklist 14](#checklist-14--figure-quality)). The same policy applies to tables via [Template 12](#template-12--table-specification-table_specmd).

## A.10 Canonical Audit Report Structure
Every audit report contains: **Summary · Passed Items · Failed Items · Evidence · Recommendations · Approval Status.** Used by all reports in [§13.3](#133-audit-reports).

## A.11 Canonical Registry Format
Every registry is a single CSV with a stable header, one row per entity, an ID column as primary key ([A.1](#a1-canonical-identifier-scheme)), and columns for `Owner`, `Version`, `Status`, `Created`, `Updated`. Registries are append-or-update only (rows are never silently deleted; retirement is a `Status` change). Each registry has exactly one owning agent and one canonical file path. The registry catalog is [Appendix B](#appendix-b--registry-index).

---

# Appendix B — Registry Index

| Registry | File | Owner Agent | Primary Key | Section |
|---|---|---|---|---|
| Papers Registry | `02_Literature/metadata/papers.csv` | Paper Registration | `P` | [3](#papers-registry) |
| Research Gap Registry | `02_Literature/research_gap/research_gap.csv` | Research Gap | `GAP` | [3](#phase-l8--research-gap-discovery-most-important) |
| Claim Database | `02_Literature/claims/claim_database.csv` | Knowledge Base | `CLAIM` | [3](#claim-database) |
| Dataset Candidates | `03_Datasets/metadata/dataset_candidates.csv` | Dataset Discovery | `Candidate` | [4](#phase-d1--dataset-discovery) |
| Datasets | `03_Datasets/metadata/datasets.csv` | Metadata | `DS` | [4](#phase-d3--dataset-registration) |
| Preprocessing Registry | `04_Preprocessing/preprocessing_registry.csv` | Preprocessing | `PP` | [4](#phase-d10--preprocessing-versioning) |
| Dataset Registry | `03_Datasets/metadata/dataset_registry.csv` | Registry | `DS`/`PP`/`SPLIT` | [4](#dataset-registry) |
| Candidate Models | `05_Models/candidate_models.csv` | Model Discovery | `MODEL` | [5](#phase-m1--candidate-model-discovery) |
| Experiment Registry | `06_Experiments/experiment_registry.csv` | Experiment | `EXP` | [5](#experiment-registry) |
| Model Registry | `05_Models/model_registry.csv` | Registry | `MODEL` | [5](#model-registry) |
| Evidence Registry | `11_AI_Forensic_System/evidence_registry.csv` | Evidence | `EV` | [6](#module-5--evidence-registry) |
| Case Registry | `11_AI_Forensic_System/case_registry.csv` | Audit | `CASE` | [6](#case-registry) |
| Module Registry | `11_AI_Forensic_System/module_registry.csv` | Systems Architect | `MOD` | [6](#module-17--system-registry) |
| Evaluation Registry | `08_Evaluation/evaluation_registry.csv` | Reporting | `EVAL` | [7](#evaluation-registry) |
| Writing Database | `15_Writing/shared/writing_database.csv` | Writing agents | `WR` | [9](#writing-database) |
| Knowledge Index | `15_Writing/shared/knowledge_index.csv` | Evidence Agent | — | [9](#phase-w2--knowledge-organization) |
| Risk Register | `01_Project_Management/risk_register.csv` | Risk Monitor | `RISK` | [13](#134-risk-register) |
| Decision Log | `01_Project_Management/decision_log/` | author | `DEC` | [1](#17-governing-philosophies) |

---

# Appendix C — Cross-Reference Map

- **Constitution ([1](#1-project-constitution))** → governs every section.
- **Repository ([2](#2-repository-architecture))** ← used by all; defines homes for outputs of 3–14.
- **Literature ([3](#3-research--literature-workflow))** → feeds Research Direction, [Writing (9)](#9-writing-operating-system); populates [Claim Database](#claim-database).
- **Dataset ([4](#4-dataset-operating-system))** ← [Repo (2)](#2-repository-architecture); → [Experiments (5)](#5-model-development-operating-system), [Evaluation (7)](#7-evaluation-protocol); tracked in [Dataset Registry](#dataset-registry).
- **Model Dev ([5](#5-model-development-operating-system))** ← [Dataset Registry](#dataset-registry); → [Model Registry](#model-registry), [Evaluation (7)](#7-evaluation-protocol), [Writing Database](#writing-database); serves [Forensic Analyst (6)](#6-ai-forensic-analyst-architecture).
- **Forensic Analyst ([6](#6-ai-forensic-analyst-architecture))** ← [Model Registry](#model-registry); evaluated in [7, Phase E14](#phase-e14--ai-forensic-analyst-evaluation); served by [Web (8)](#8-web-application-architecture).
- **Evaluation ([7](#7-evaluation-protocol))** ← [Experiment](#experiment-registry)/[Model](#model-registry)/[Dataset](#dataset-registry) registries; → [Figures (9)](#09_figures), [Tables (10)](#10_tables), [Writing (9)](#9-writing-operating-system); tracked in [Evaluation Registry](#evaluation-registry).
- **Web ([8](#8-web-application-architecture))** ← [Forensic Analyst (6)](#6-ai-forensic-analyst-architecture); deployed via [Deployment (14_Deployment)](#14_deployment).
- **Writing ([9](#9-writing-operating-system))** ← [Claim Database](#claim-database), [Evaluation Registry](#evaluation-registry), [Figure specs](#a9-canonical-figure-policy).
- **Infra ([10](#10-github--kaggle--antigravity-workflow))** ← [Storage tiers (A.6)](#a6-canonical-storage--synchronization-policy); synchronizes all registries.
- **Agents ([11](#11-agent-framework))** ← one per responsibility across 3–13.
- **Daily ([12](#12-daily-research-operating-workflow))** → executes 3–10 day-by-day; updates registries + dashboard.
- **QA ([13](#13-quality-assurance))** → gates transitions between 3→4→5→7→9→submission.
- **Templates ([14](#14-template-library))** → standardize outputs of every section.

---

# Appendix D — Glossary

- **AI Forensic Analyst** — the primary contribution: the evidence-driven forensic system ([Section 6](#6-ai-forensic-analyst-architecture)); not the detector.
- **Evidence** — any independent signal about an input (statistics, frequency artifacts, model prediction, etc.), recorded in the [Evidence Registry](#module-5--evidence-registry).
- **Specialist** — an evidence collector, including the deep learning detector ([Module 3–4](#module-3--evidence-acquisition-layer)).
- **Experiment** — the unit of model work (`EXPxxxx`); a model is one component of it ([Section 5](#5-model-development-operating-system)).
- **Registry** — a canonical CSV ledger with one owner ([Appendix A.11](#a11-canonical-registry-format), [Appendix B](#appendix-b--registry-index)).
- **Definition of Done (DoD)** — the eight universal completion criteria ([Appendix A.5](#a5-canonical-definition-of-done)).
- **Quality Gate** — a checklist that must PASS before the next phase begins ([§13.2](#132-quality-gates)).
- **Source / Artifact / Data tier** — the three storage tiers ([Appendix A.6](#a6-canonical-storage--synchronization-policy)).
- **Living Literature Review** — the continuously updated review ([Phase L11](#phase-l11--living-literature-review)).
- **Leakage** — contamination between train and test (identity/duplicate/generator/future) ([Phase D12](#phase-d12--trainvalidationtest-split-leakage-critical)).
- **Calibration** — agreement between predicted confidence and observed accuracy ([Phase E4](#phase-e4--calibration-analysis)).

---

# Appendix E — Acronyms

| Acronym | Meaning |
|---|---|
| ADR | Architecture Decision Record |
| API | Application Programming Interface |
| CSV | Comma-Separated Values |
| DoD | Definition of Done |
| DRF | Django REST Framework |
| EDA | Exploratory Data Analysis |
| ECE | Expected Calibration Error |
| GAN | Generative Adversarial Network |
| LFS | (Git) Large File Storage |
| LR | Learning Rate |
| MCC | Matthews Correlation Coefficient |
| PR | Precision–Recall |
| QA | Quality Assurance |
| ROC | Receiver Operating Characteristic |
| SemVer | Semantic Versioning |
| SOTA | State Of The Art |
| UAT | User Acceptance Testing |
| ViT | Vision Transformer |
| WCAG | Web Content Accessibility Guidelines |

---

# Appendix F — Self-Review & Validation Record

A self-review was performed against the required checks. Findings and resolutions:

- **Duplicated definitions removed.** Naming, versioning, DoD, README policy, storage/sync, ignore rules, figure policy, human-task protocol, audit structure, and registry format were consolidated into [Appendix A](#appendix-a--canonical-definitions) and referenced from every section (resolving duplication across the Dataset, Model, Evaluation, and Writing sections).
- **Consistent terminology.** The Experiment Registry, Model Registry, Dataset Registry, Evaluation Registry, Claim Database, Evidence Registry, Case Registry, Module Registry, and Writing Database each have exactly one name and one file path ([Appendix B](#appendix-b--registry-index)); no aliases are used.
- **No contradictory workflows.** The artifact flow `Local ↔ GitHub ↔ Kaggle` and platform responsibilities are stated once ([§10.1](#101-core-philosophy--platform-responsibilities)) and referenced elsewhere.
- **Dependencies present.** Every registry has an owner ([Appendix B](#appendix-b--registry-index)); every folder has a contract ([§2.3](#23-folder-contracts)); every phase has a DoD (phase text + [A.5](#a5-canonical-definition-of-done)).
- **No circular workflows / broken references.** The [Cross-Reference Map](#appendix-c--cross-reference-map) forms a directed flow Literature → Data → Model → Forensic/Evaluation → Web/Writing → Publication, gated by QA.

**Final validation checklist:**

| Criterion | Status |
|---|---|
| Every workflow complete | ✓ |
| Every artifact has one owner | ✓ ([Appendix B](#appendix-b--registry-index)) |
| Every file has one location | ✓ ([§2.3](#23-folder-contracts), [A.2](#a2-canonical-file-naming-rules)) |
| Every registry has one purpose | ✓ ([A.11](#a11-canonical-registry-format)) |
| Every experiment reproducible | ✓ ([Section 5](#5-model-development-operating-system)) |
| Every dataset traceable | ✓ ([Dataset Registry](#dataset-registry)) |
| Every figure reproducible | ✓ ([A.9](#a9-canonical-figure-policy)) |
| Every scientific claim evidence-based | ✓ ([Claim Database](#claim-database)) |
| Every component has a responsibility | ✓ (Sections [6](#6-ai-forensic-analyst-architecture), [8](#8-web-application-architecture)) |
| Every agent single-responsibility | ✓ ([Section 11](#11-agent-framework)) |
| Every phase has a DoD | ✓ |
| Every section supports the thesis objective | ✓ |
| GitHub is the single source of truth | ✓ ([Section 10](#10-github--kaggle--antigravity-workflow)) |
| AI Forensic Analyst is the primary contribution | ✓ ([§1.2](#12-project-identity), [Section 6](#6-ai-forensic-analyst-architecture)) |
| Guides Day 1 → thesis defense → journal publication | ✓ |

**Human ratification required.** This handbook is a draft pending the researcher's approval of the [deferred decisions](#111-deferred-decisions) (DEF-001…DEF-004) and the fixed technology stack, license, and repository name. Upon approval, set the status on the [cover page](#cover-page) to *Ratified* and record the event in the [Decision Log](#template-3--decision-log-decisionmd).

---

*End of `MASTER_RESEARCH_OPERATING_SYSTEM.md` — v1.0.0.*
