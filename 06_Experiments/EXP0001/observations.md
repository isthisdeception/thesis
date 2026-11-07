# EXP0001 — Observations

## 2026-11-06 — Readiness (STEP-035)

- Config validated (PASS) against the dataset, preprocessing, split, and candidate-model registries.
- SPLIT0001 is class-balanced in every partition, so no class weighting or resampling is configured.
- `learning_rate.value` (1.0e-3) is a placeholder; the LR Finder suggestion must be recorded in `config.yaml` before training starts.
- `git_commit` and `timestamp` record the readiness state and must be refreshed at Kaggle session start, followed by re-validation.
- Kaggle environment smoke check from STEP-030 is still outstanding; paste its output into `logs/` at the first session.
