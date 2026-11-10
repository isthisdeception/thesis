# EXP0002 — Observations

## 2026-11-10 — Readiness (STEP-047)

- Created for Phase E9 (DEC0007): Stable Diffusion is the only held-out generator, using the existing `SPLIT0002`.
- Config copied from EXP0001; only experiment ID, model ID (`MODEL0008`), split, purpose, expected outcome, and outputs changed. Validator PASS against all registries; training settings load and the split validates (train 40873, val 7204, test 1923, test labels `fake` only).
- `learning_rate.source: manual` because the value is EXP0001's LR Finder result, not a new LR Finder run.
- Artifacts publish to `isthisdeception/thesis-exp0002-artifacts`. Publishing to `thesis-experiment-artifacts` would replace MODEL0001's files in that dataset's latest version.
- `git_commit` is `main` at readiness (`faa16a6`); it must stay an ancestor of the commit Kaggle clones, which holds for any later `main`.

## 2026-11-10 — Training (Kaggle T4)

- Ran from `main` at `362e2e2`; git provenance verified. Fresh run, no resume. All 11 epochs, best epoch 9 (valid_loss 0.331), 66.0 min.
- Test metrics printed as `nan` for ROC-AUC/PR-AUC and 0 for specificity: the test split is fake-only. Expected.
- Publish (C): the first `datasets version` call returned 403 because the dataset did not exist; the fallback `datasets create` ran. Its log stops after three small files; the dataset page was checked afterwards and `notebook/checkpoints/MODEL0008_export.pkl` is present. The kaggle CLI 2.0.2 also logged `KaggleObject.from_dict() got an unexpected keyword argument 'token'` per file; uploads still reported success.
- Push (D) ran twice; the first created `kaggle/exp0002-20261110-0656`, the second found nothing new.
