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
- **Phases D4–D5 — Dataset Download & Raw-Lock (STEP-021):** `COMPLETE` (hosting)
  - DS0001/2/4/5 on private Kaggle (`isthisdeception/…`); DS0003 = [`xhlulu/140k-real-and-fake-faces`](https://www.kaggle.com/datasets/xhlulu/140k-real-and-fake-faces).
  - Pointers + archive SHA-256 recorded for project uploads; DS0003 marked access-confirmed.
  - **Next:** STEP-022 Dataset Validation (`Validated` still `no` for all).

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
