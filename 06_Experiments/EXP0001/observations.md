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

## 2026-11-08 — Kaggle Session A (LR Finder), first attempt

- Dataset validation stopped before any training: all 50,000 images missing under `/kaggle/input/datasets/isthisdeception/ds0001-pp0001`. The upload keeps its top-level `DS0001_PP0001/` folder; the pipeline located the files and suggested the path. `dataset.processed_root` changed to `/kaggle/input/datasets/isthisdeception/ds0001-pp0001/DS0001_PP0001` (config, template, `05_Models/config/fastai_dataset.yaml`). Pre-training change; validator PASS.
- The traceback shows the Kaggle image runs Python 3.13 (`/usr/lib/python3.13`), not 3.12 as in `environment/versions.lock.md`. Full versions to be recorded from the environment-check cell; update the lock if they differ.

## 2026-11-08 — Kaggle Session A (LR Finder), completed

- LR Finder (`valley`, 100 iterations, frozen body): suggested `0.000331131302240938` (`3.311313e-4`). Recorded in `learning_rate.value` (`source: lr_find`). Phase LRs: frozen `lr_max` 3.31e-4; unfrozen `slice(1.66e-6, 1.66e-4)`.
- Environment (pipeline log): Python 3.13.16, torch 2.11.0+cu130, torchvision 0.26.0+cu130, fastai 2.8.12, CUDA 13.0, Tesla T4 (14,912 MB), plum-dispatch 2.5.7. This differs from the v170 lock, so a new lock (2026-11-08) was added before training; the full test suite passes on these versions (CPU). `hardware.kaggle_image` → `kaggle-gpu-2026-11-08`.
- Dataset validation took 1,199 s on the Kaggle mount (one file check per image). Replaced by one directory listing per folder; same checks, same failure messages.
- **Aborted run, discarded:** "Run All" also started cell B, so training began with the pre-LR-Finder value 1.0e-3 before the suggestion was recorded. It was interrupted within minutes; its checkpoints and logs lived only in that session's `/kaggle/working`, were never published or pushed, and were discarded by stopping the session. No results from it exist or are used.
- `git_commit` → `0f7c613` (code + lock commit), `timestamp` refreshed. The config is frozen from Session B on.
