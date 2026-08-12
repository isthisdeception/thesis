# 17_Automation

**Purpose:** Reproducible scripts and pipeline automation.

## Contents
Environment scripts, Kaggle sync scripts, Git automation, health checks, dataset integrity + **STEP-022 validation**.

## Dataset validation (Phase D6)
- Package: `17_Automation/dataset_validation/`
- Spec: `dataset_validation/SPEC.md`
- Kaggle instructions: `04_Preprocessing/notebooks/STEP022_KAGGLE_VALIDATION.md`
- Entrypoint: `python -m dataset_validation --roots ... --out ...` or `step022_run_validation.py`

## Dataset EDA (Phase D7 / STEP-023)
- Package: `17_Automation/dataset_eda/`
- Spec: `dataset_eda/SPEC.md`
- Kaggle instructions: `04_Preprocessing/notebooks/STEP023_KAGGLE_EDA.md`
- Entrypoint: `python -m dataset_eda --roots ... --out ...` or `step023_run_eda.py`
- Outputs: `03_Datasets/reports/eda_*.csv` + figure specs in `09_Figures/specs/` (A.9 — no rendered figures)

## Workflow
Automation agents write, all workflows consume. No automated scientific decisions.

## Owner
Automation/DevOps Agents

## Related Folders
10_Github_Kaggle_Antigravity, 13_Quality_Assurance

## Expected Outputs
automation scripts

> *This folder follows the canonical repository hygiene and naming rules defined in `MASTER_RESEARCH_OPERATING_SYSTEM.md`. Please refer to the handbook for full policy details.*
