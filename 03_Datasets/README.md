# 03_Datasets

**Purpose:** The Dataset Operating System (OS) for AI Digital Forensics.

## Phase Status
- **Phase D1 — Dataset Discovery (STEP-018):** `COMPLETED`
  - Registered 17 candidate datasets (`CAND0001`–`CAND0017`) in `03_Datasets/metadata/dataset_candidates.csv`.
- **Phase D2 — Dataset Evaluation & Selection (STEP-019):** `COMPLETED`
  - Evaluated and scored all 17 candidates across 16 Phase D2 dimensions (`dataset_evaluation.csv`).
  - Strict Public-Only Policy approved and locked in `01_Project_Management/decision_log/DEC0004.md` (resolving `DEF-003`).
- **Phase D3 — Dataset Registration (STEP-020):** `COMPLETED`
  - Registered `DS0001`–`DS0005` in `03_Datasets/metadata/datasets.csv` with metadata.
  - License files saved in `03_Datasets/licenses/DS0001_license.txt` ... `DS0005_license.txt`.
  - **DS0005 reassigned** from AI-Face-FairnessBench (EULA-restricted) to FairFace (CC BY 4.0) per `DEC0005.md`.
- **Phases D4–D5 — Dataset Download & Raw-Lock (STEP-021):** `IN PROGRESS`
  - **Status:** Planning artifacts completed; data download NOT yet executed.
  - Remote dataset storage pointers corrected in `03_Datasets/metadata/dataset_pointers.md`.
  - Download priority: DS0003 (Kaggle-native) → DS0001 → DS0004 → DS0002 → DS0005.
  - `03_Datasets/reports/download_instructions.md` — Human Task instructions per A.8.
  - Integrity module upgraded in `17_Automation/dataset_checksum_verifier.py` (3 modes: full/sample/archive).
  - `03_Datasets/reports/integrity_report.csv` — header-only (awaiting real checksums from Kaggle).
  - **Next action:** Human downloads datasets per `download_instructions.md`, then runs checksum verifier on Kaggle.

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
- `03_Datasets/metadata/dataset_registry.csv` (Phase D8)

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
