# 03_Datasets

**Purpose:** The Dataset Operating System (OS) for AI Digital Forensics.

## Phase Status
- **Phase D1 — Dataset Discovery (STEP-018):** `COMPLETED`
  - Registered 17 candidate datasets (`CAND0001`–`CAND0017`) in `03_Datasets/metadata/dataset_candidates.csv`.
  - Cover Kaggle, Hugging Face, GitHub, Zenodo, OpenML, VGG Oxford, TUM, and project sites.
  - Represent diverse generator families (Diffusion models: SD v1.4/1.5/2.1/XL, DALL-E 2/3, Midjourney v5, GLIDE, Firefly; GANs: ProGAN, StyleGAN, StyleGAN2, StyleGAN3, StarGAN, AttGAN; Swaps: Deepfakes, Face2Face, FaceSwap, NeuralTextures).
  - Licenses recorded at first sight; duplicates flagged (e.g. `CAND0011` -> `CAND0010`).
- **Phase D2 — Dataset Evaluation & Selection (STEP-019):** `COMPLETED`
  - Evaluated and scored all 17 candidates across 16 Phase D2 dimensions (`dataset_evaluation.csv`).
  - Strict Public-Only Policy approved and locked in `01_Project_Management/decision_log/DEC0004.md` (resolving `DEF-003`).
- **Phase D3 — Dataset Registration (STEP-020):** `COMPLETED`
  - Registered `DS0001`–`DS0005` in `03_Datasets/metadata/datasets.csv` with metadata.
  - License files saved in `03_Datasets/licenses/DS0001_license.txt` ... `DS0005_license.txt`.
  - **DS0005 reassigned** from AI-Face-FairnessBench (EULA-restricted) to FairFace (CC BY 4.0) per `DEC0005.md`.
- **Phases D4–D5 — Dataset Download & Raw-Lock (STEP-021):** `COMPLETE`
- **Phase D6 — Dataset Validation (STEP-022):** `COMPLETE`
  - Reports: `03_Datasets/reports/validation_report.csv`, `quality_report.csv`, `integrity_report.csv`, `validation_summary.json`
  - Per-dataset artifacts: `03_Datasets/reports/step022/`
  - DS0002: issues logged + filter plan `reports/step022/DS0002_issues_plan.md` (corrupt filter in STEP-025)
  - Local Kaggle dumps (gitignored): `_staging_dataset_validation/`
- **Phase D7 — Exploratory Dataset Analysis (STEP-023):** `COMPLETE`
  - Module: `17_Automation/dataset_eda/` + Kaggle guide `04_Preprocessing/notebooks/STEP023_KAGGLE_EDA.md`
  - Reports: `03_Datasets/reports/eda_*.csv`, `eda_summary.json`, `reports/step023/`
  - Figure specs (A.9): `09_Figures/specs/FIG0001_spec.md` … `FIG0010_spec.md`
  - Pixel metrics: stratified sample n=3000 seed=42; label/generator/identity fully enumerated
- **Phase D8 — Dataset Documentation + Raw Readiness Gate (STEP-024):** `COMPLETE` (raw-stage PASS, human-confirmed 2026-08-12)
  - `reports/dataset_report.md`, `dataset_card.md`, `dataset_audit.md`
- **Phases D9–D12 — Preprocess + split (STEP-025–028):** `COMPLETE`
- **Phases D13–D15 — FastAI prep, versioning, master registry + gates (STEP-029):** `COMPLETE`
  - Config: `05_Models/config/fastai_dataset.yaml`
  - Spec: `04_Preprocessing/specs/FASTAI_DATABLOCK_SPEC.md`
  - `metadata/dataset_versions.csv` (v1.0)
  - `metadata/dataset_registry.csv` (DS→PP→SPLIT; EXP/MODEL empty)
  - `datasets.csv` `Ready=yes`
  - Audits: `reports/dataset_audit.md` (Checklist 3), `04_Preprocessing/reports/preprocessing_audit.md` (Checklist 4)
  - Status: `STEP029_STATUS.md`
  - **Next:** STEP-030 Environment definition & version lock

## Contents
Raw immutable originals (`raw/`), processed datasets (`processed/`), splits (`splits/`), metadata (`metadata/`), reports (`reports/`), licenses (`licenses/`).

## Workflow
Dataset agents write, Preprocessing and Experiments read. Never modify `raw/`.

## Owner
Dataset Discovery Agent / Dataset Evaluation Agent / Metadata Agent / Human

## Related Folders
`04_Preprocessing`, `08_Evaluation`, `02_Literature`

## Expected Outputs & Registries
- `03_Datasets/metadata/dataset_candidates.csv` (Phase D1)
- `03_Datasets/metadata/dataset_evaluation.csv` (Phase D2)
- `03_Datasets/metadata/datasets.csv` (Phase D3)
- `03_Datasets/metadata/dataset_pointers.md` (Phase D4/D5)
- `03_Datasets/reports/integrity_report.csv` (Phase D4/D5)
- `03_Datasets/reports/download_instructions.md` (Phase D4/D5 — Human Task)
- `03_Datasets/metadata/dataset_registry.csv` (Phase D15)
- `03_Datasets/metadata/dataset_versions.csv` (Phase D14)
- `03_Datasets/reports/dataset_audit.md` (Checklist 3)

> *This folder follows the canonical repository hygiene and naming rules defined in `MASTER_RESEARCH_OPERATING_SYSTEM.md` (§4).*

## Cross-Linked Agents
The following agents operate within this domain:
- [Discovery](../../19_Prompts/agents/dataset/discovery.md)
- [Evaluation](../../19_Prompts/agents/dataset/evaluation.md)
- [Metadata](../../19_Prompts/agents/dataset/metadata.md)
- [Validation](../../19_Prompts/agents/dataset/validation.md)
- [Quality](../../19_Prompts/agents/dataset/quality.md)
- [Preprocessing](../../19_Prompts/agents/dataset/preprocessing.md)
- [Split](../../19_Prompts/agents/dataset/split.md)
- [Statistics](../../19_Prompts/agents/dataset/statistics.md)
- [Documentation](../../19_Prompts/agents/dataset/documentation.md)
- [Registry](../../19_Prompts/agents/dataset/registry.md)
