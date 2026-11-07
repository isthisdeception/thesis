# EXP0001 — Observations

## 2026-11-06 — Readiness (STEP-035)

- Config validated (PASS) against the dataset, preprocessing, split, and candidate-model registries.
- SPLIT0001 is class-balanced in every partition, so no class weighting or resampling is configured.
- `learning_rate.value` (1.0e-3) is a placeholder; the LR Finder suggestion must be recorded in `config.yaml` before training starts.
- `git_commit` and `timestamp` record the readiness state and must be refreshed at Kaggle session start, followed by re-validation.
- Kaggle environment smoke check from STEP-030 is still outstanding; paste its output into `logs/` at the first session.

## 2026-11-06 — Training pipeline (STEP-036)

- Config gained explicit keys that were previously implicit (positive class, threshold criterion, calibration bins, `fine_tune` schedule numbers, LR Finder iterations). Training has not started, so the config is still editable; re-validated PASS.
- Check `plum-dispatch` on the Kaggle image at first session; the pipeline stops before training if `export.pkl` would be unpicklable.

## 2026-11-07 — Expected outcome approved

- Human accepted the proposed expected outcome (test ROC-AUC ≥ 0.95, balanced accuracy ≥ 0.90; investigate below ROC-AUC 0.90). Recorded in `01_Project_Management/decision_log/DEC0006.md`.
