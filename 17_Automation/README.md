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
- Logging (STEP-038): `training/logs.py`, `training/records.py`; schemas in `training/LOGGING.md`. `kaggle_sync push-metadata` refuses binaries and files over 20 MB.
- Checkpoint system (STEP-037): `training/checkpoints.py`; policy in `07_Checkpoints/checkpoint_policy.md`. `kaggle_sync resume-checkpoints` merges mounted checkpoints without deleting or overwriting local files.

## Ablations (Phase E10 / STEP-048)
- Package: `17_Automation/ablation/`
- Plan: `06_Experiments/ablations/STEP048_plan.yaml` (one entry per ablation: experiment, model, evaluation IDs, factor, question, and the config keys of that one factor).
- Entrypoints: `python -m ablation list`, `create` (generates each experiment from the baseline config; refuses any difference beyond identity fields and the planned keys; never overwrites; writes docs, sync plans, registry rows), `evaluate` (after Kaggle: STEP-040 registration from `run_summary.json`, STEP-041 inputs, E1–E2, then `08_Evaluation/ablations/ablation_results.csv` and `ablation_report.md`, read against the seed replicate).
- Kaggle: `06_Experiments/ablations/STEP048_ablations.ipynb`, push plan `kaggle_sync/sync_plan.ablations.yaml`, one publish plan per experiment.

## Generalization (Phases E8–E9 / STEP-047)
- Package: `17_Automation/generalization/`
- Config (E8): `08_Evaluation/EVAL0001/generalization/config.yaml` (target datasets, samples, generator relations; nothing hardcoded)
- Entrypoints: `python -m generalization datasets` (plan), `run` (Kaggle GPU: sanity pass on 500 DS0001 images, then MODEL0001 on each target; resumable per dataset), `analyze` (E8 CSVs + `cross_dataset_report.md`), `unseen --experiment EXP0002 --evaluation EVAL0002` (E9 from the held-out experiment's STEP-041 predictions; leakage check from the split's `split_config.json`).
- Reuses the robustness input pipeline and export lookup. Kaggle: `sync_plan.generalization.yaml` (E8), `sync_plan.exp0002.yaml` (EXP0002 training).
- `prediction_validation` now reads the model ID and split from the experiment config and requires the evaluation ID in `evaluation_registry.csv`, so it serves EVAL0002 as well as EVAL0001.

## Robustness evaluation (Phase E7 / STEP-046)
- Package: `17_Automation/robustness/`
- Config: `08_Evaluation/EVAL0001/robustness/config.yaml` (perturbations and levels; nothing hardcoded)
- Entrypoints: `python -m robustness conditions` (list), `python -m robustness run` (Kaggle GPU: perturbed inference, clean check first, resumable), `python -m robustness analyze` (anywhere: metrics, flips, per-group errors, summary, `robustness_report.md`).
- JPEG and resizing reuse PPMOD09 and PPMOD05 from `04_Preprocessing/modules`. Per-image seeds make every perturbation deterministic.
- Kaggle session: `08_Evaluation/EVAL0001/robustness/KAGGLE_RUNBOOK.md`, sync plan `kaggle_sync/sync_plan.robustness.yaml`.

## Confusion and failure analysis (Phases E6, E12 / STEP-045)
- Package: `17_Automation/failure_analysis/`
- Entrypoint: `python -m failure_analysis --experiment EXP0001 --evaluation EVAL0001`
- Refuses to run unless `prediction_validation_report.md` passed. Joins predictions to the preprocessing index by content hash, then writes confusion, per-class, per-group error, and error-case CSVs plus `failure_analysis.md` to `08_Evaluation/EVAL0001/`. Causes are written as hypotheses.

## Calibration and threshold analysis (Phases E4–E5 / STEP-044)
- Package: `17_Automation/calibration_threshold/`
- Entrypoint: `python -m calibration_threshold --experiment EXP0001 --evaluation EVAL0001`
- Refuses to run unless `prediction_validation_report.md` passed. Writes calibration (ECE, MCE, Brier, reliability bins, confidence distribution), a threshold sweep, and val-chosen operating points to `08_Evaluation/EVAL0001/`, plus `calibration_threshold.md`. No figures are rendered.

## Classification metrics (Phase E3 / STEP-043)
- Package: `17_Automation/classification_metrics/`
- Entrypoint: `python -m classification_metrics --experiment EXP0001 --evaluation EVAL0001`
- Refuses to run unless `prediction_validation_report.md` passed. Writes the full E3 suite to `08_Evaluation/EVAL0001/classification_metrics.csv` and the metrics section with per-metric notes to `classification_metrics.md`. Accuracy is never written alone.

## Prediction validation (Phase E1–E2 / STEP-042)
- Package: `17_Automation/prediction_validation/`
- Entrypoint: `python -m prediction_validation --experiment EXP0001 --evaluation EVAL0001`
- Rejects an incomplete experiment and any prediction whose id, count, label, path, or probability does not match the split. Writes `08_Evaluation/EVAL0001/prediction_validation_report.md`.

## Evaluation inputs (Phase M16 / STEP-041)
- Package: `17_Automation/evaluation_trigger/`
- Entrypoint: `python -m evaluation_trigger --experiment EXP0001 --positive-class fake --negative-class real`
- Writes `08_Evaluation/EXPxxxx/` from the saved prediction CSVs. Does not run the model and does not render figures.

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
