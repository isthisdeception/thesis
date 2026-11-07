# STEP-035 — Create the Experiment & Pass Readiness

**Status:** COMPLETE — **Checklist 5 = PASS** (2026-11-06)  
**Handbook:** Phase M5; 06_Experiments contract; Template 7; Checklist 5

## Output created
- [x] `06_Experiments/EXP0001/` with `config.yaml`, `README.md` (Template 7), `checkpoints_info.md`, `observations.md`, and `logs/`, `metrics/`, `predictions/`, `learning_curves/`, `notebook/`
- [x] Config validation: `python -m config_validation ../06_Experiments/EXP0001/config.yaml` → PASS
- [x] `06_Experiments/experiment_registry.csv` row `EXP0001`, `Status=ready`

## Checklist 5 — Experiment Readiness

| Item | Result | Evidence |
|------|--------|----------|
| Dataset version | PASS | `DS0001` v1.0 / `PP0001` registered `ready` in `dataset_registry.csv` |
| Split version | PASS | `SPLIT0001` on `DS0001_PP0001`, `grouped_random`, leakage PASS in `split_registry.csv`; `assignments.csv` present |
| Config | PASS | `EXP0001/config.yaml` complete; validator PASS |
| Random seed | PASS | `random_seed: 42` |
| Model version | PASS | `MODEL0001` ResNet-50, matches `candidate_models.csv` |
| Experiment ID | PASS | `EXP0001` |
| Hardware | PASS | Kaggle GPU T4, image v170 |
| Checkpoint location | PASS | `EXP0001/notebook/checkpoints`; artifact tier `isthisdeception/thesis-experiment-artifacts`; manifest `07_Checkpoints/EXP0001_checkpoints.md` |
| Output folders | PASS | `logs/`, `metrics/`, `predictions/`, `learning_curves/`, `notebook/` |
| Expected metrics | PASS | `expected_outcome`: test ROC-AUC ≥ 0.95, balanced accuracy ≥ 0.90 (sanity expectation) |
| Research question | PASS | recorded in config, README, and registry |

## Before launch (STEP-039)
- Record the LR Finder suggestion in `learning_rate.value`.
- Refresh `git_commit` and `timestamp`, re-run the validator, then train. After training starts the config is immutable.

## Next step
**STEP-036** — Implement the training pipeline package.
