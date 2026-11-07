# 17_Automation

**Purpose:** Reproducible scripts and pipeline automation.

## Contents
Environment scripts, Kaggle sync scripts, Git automation, health checks, dataset integrity + **STEP-022 validation**.

## Kaggle sync (STEP-031)
- Package: `17_Automation/kaggle_sync/`
- Session template: `06_Experiments/KAGGLE_SESSION_TEMPLATE.ipynb`
- Entrypoint: `python -m kaggle_sync --plan kaggle_sync/sync_plan.example.yaml <command>`
- Commands: `bootstrap`, `resume-checkpoints`, `publish-artifacts`, `push-metadata`
- Policy: data tier stays on Kaggle Datasets, artifact tier stays in Kaggle outputs/datasets, only source-tier metadata returns to Git

## Training pipeline (Phase M6 / STEP-036)
- Package: `17_Automation/training/` (docs: `training/README.md`)
- Entrypoints: `from training import find_lr, run_experiment` or `python -m training {lr-find,train} --config ...`
- Thin caller: `06_Experiments/EXP0001/notebook/EXP0001_train.ipynb`
- Tests: `tests/test_training_core.py` (no FastAI), `tests/test_training_smoke.py` (end-to-end, CPU, including interruption + resume)
- Checkpoint system (STEP-037): `training/checkpoints.py`; policy in `07_Checkpoints/checkpoint_policy.md`. `kaggle_sync resume-checkpoints` merges mounted checkpoints without deleting or overwriting local files.

## Config validation (Phase M4 / STEP-034)
- Package: `17_Automation/config_validation/`
- Docs: `config_validation/README.md`; training workflow in `05_Models/FASTAI_TRAINING_STANDARD.md`
- Entrypoint: `python -m config_validation ../06_Experiments/EXPxxxx/config.yaml` (template: add `--template`)
- Fails on missing M4 sections, unknown DS/PP/SPLIT/MODEL IDs, and unset seed

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
