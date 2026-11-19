# AI Digital Forensics

## Purpose
An evidence-driven forensic system (**AI Forensic Analyst**) designed to evaluate, classify, and explain AI-generated vs. real human face media. This repository spans the complete reproducible pipeline from systematic literature review, dataset curation (`DS0001`–`DS0005`), preprocessing (`PP0001`–`PP0006`), and Kaggle GPU experiments (`EXP0001`–`EXP0006` / `MODEL0001`), through the modular 18-module Forensic System (`11_AI_Forensic_System/`), Django REST API (`13_Backend/`), and React Web Application (`12_Web/`).

## Project Description
The AI Forensic Analyst is not a single black-box classifier: `MOD004` (the deep learning detector) acts as one independent specialist among 10 collectors. Validated `EV` items are registered immutably (`MOD005`), reliability-graded (`MOD006`), fused via replaceable strategy (`MOD007`), evaluated across four distinct confidence dimensions (`MOD009`), and converted by the isolated Decision Engine (`MOD008`) into `Real`, `Fake`, `Inconclusive`, or `Unknown` with `EV`-cited explanations (`MOD010`–`MOD011`) and Template 24 reports (`MOD012`). Governance strictly follows [`MASTER_RESEARCH_OPERATING_SYSTEM.md`](./MASTER_RESEARCH_OPERATING_SYSTEM.md).

## Quick Start & Installation

Full setup details live in [`16_Documentation/installation.md`](./16_Documentation/installation.md). Summary:

1. **Create virtual environment & install Python dependencies:**
   ```bash
   python -m venv .venv
   .venv/Scripts/pip.exe install -r environment/requirements.txt
   .venv/Scripts/pip.exe install -r 13_Backend/requirements.txt
   ```
2. **Install React frontend dependencies:**
   ```bash
   cd 12_Web && npm ci
   ```
3. **Copy `.env.example` templates** in `13_Backend/.env.example` and `12_Web/.env.example` (never commit `.env`), then start both tiers:
   ```bash
   # Terminal 1 (Backend API on http://127.0.0.1:8000/api/v1)
   .venv/Scripts/python.exe 13_Backend/manage.py runserver 127.0.0.1:8000

   # Terminal 2 (Frontend UI on http://localhost:5173)
   cd 12_Web && npm run dev
   ```
4. **Verify all tiers (unit, API, Vitest, Vite build, live integration, and 6 UAT scenarios):**
   ```bash
   .venv/Scripts/python.exe 17_Automation/run_all_tests.py
   ```

## Documentation Hub (`16_Documentation/`)

| Document | Audience | Link |
|---|---|---|
| **System Architecture** | Engineers & Examiners | [`16_Documentation/architecture.md`](./16_Documentation/architecture.md) |
| **REST API Guide** | API Consumers | [`16_Documentation/api_guide.md`](./16_Documentation/api_guide.md) |
| **Developer Guide & Extension Contracts** | Contributors (`EvidenceCollector` / `FusionStrategy`) | [`16_Documentation/developer_guide.md`](./16_Documentation/developer_guide.md) |
| **User Manual** | Forensic Analysts / End Users | [`16_Documentation/user_guide.md`](./16_Documentation/user_guide.md) |
| **Installation Guide** | Local & Dev Setup | [`16_Documentation/installation.md`](./16_Documentation/installation.md) |
| **Integration & Test Plan** | QA & CI | [`integration_guide.md`](./16_Documentation/integration_guide.md) · [`test_plan.md`](./16_Documentation/test_plan.md) |
| **Folder Guide & Workflow Diagrams** | Repository Navigation | [`folder_guide.md`](./16_Documentation/folder_guide.md) · [`workflow_diagrams/`](./16_Documentation/workflow_diagrams/README.md) |

## Repository Structure Map

See [`16_Documentation/folder_guide.md`](./16_Documentation/folder_guide.md) for detailed explanations of all 20 canonical directories (`01_Project_Management/`–`20_Archive/`).

| Folder | Purpose |
|---|---|
| `01_Project_Management/` | Governance, decision logs (`DEC0001`–`DEC0010`), dashboard, risks, and reviews. |
| `02_Literature/` | Papers, summaries, research gaps, and claims. |
| `03_Datasets/` | Dataset tracking (`DS0001`–`DS0005`), splits, and metadata pointers. |
| `04_Preprocessing/` | Versioned data preprocessing pipelines (`PP0001`–`PP0006`). |
| `05_Models/` | Model definitions and Model Registry (`MODEL0001`, `MODEL0008`–`MODEL0012`). |
| `06_Experiments/` | Individual experiment environments (`EXP0001`–`EXP0006`) & registry. |
| `07_Checkpoints/` | Manifests and policies for recoverable training state. |
| `08_Evaluation/` | Evaluation metrics, robustness, cross-dataset generalization, statistics, and gate audits. |
| `09_Figures/` | Specifications and generation provenance (`FIGxxxx`) for all figures. |
| `10_Tables/` | Specifications and rendered data (`TABxxxx`) for all tables. |
| `11_AI_Forensic_System/` | The 18-module AI Forensic Analyst (`MOD001`–`MOD018`) and registries. |
| `12_Web/` | React + Vite + Tailwind frontend application (`MOD014`). |
| `13_Backend/` | Django + DRF REST API backend (`MOD013`). |
| `14_Deployment/` | Deployment configuration (`gunicorn/`, `nginx/`). |
| `15_Writing/` | Thesis and journal drafts, writing evidence database. |
| `16_Documentation/` | System, API, developer, user, installation, and workflow documentation. |
| `17_Automation/` | Reproducible training, Kaggle sync, integration, and test/UAT automation. |
| `18_Templates/` | Canonical templates for all structured files. |
| `19_Prompts/` | Versioned prompts for all AI agents. |
| `20_Archive/` | Immutable storage of completed/superseded artifacts. |
| `environment/` | Dependency locks (`versions.lock.md`, `requirements.txt`, `kaggle-requirements.txt`). |

## Workflow Strategy
We operate a specialized multi-platform workflow ([`§10.1`](./MASTER_RESEARCH_OPERATING_SYSTEM.md#101-core-philosophy--platform-responsibilities)):
- **Cursor** = Planning only.
- **Antigravity** = Implementation & Testing.
- **GitHub** = Version control / single source of truth.
- **Kaggle** = Heavy model training & GPU evaluation.
- **Human** = Scientific decisions & Gate approvals.

## Dependencies
- **Core ML:** Python (`3.11`–`3.13`), PyTorch `2.11.0`, torchvision `0.26.0`, FastAI `2.8.12`, Pillow `12.1.1`
- **Web App:** Django `5.2.19`, Django REST Framework `3.18.3`, React `18.3`, Vite `6.0`, Tailwind CSS `3.4`
- **Storage:** Kaggle Datasets (processed datasets & model exports), GitHub (source of truth, registries, and specs)

## License
[MIT License](./LICENSE)

## Citation
*(To be finalized upon thesis & manuscript submission in Part 14.)*

## Contact
Chief Research Architect (`Assaduzzaman`)
