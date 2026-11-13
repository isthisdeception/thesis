# Experiment: EXP0004

**Status:** ready. Waiting for the STEP-048 Kaggle session (`06_Experiments/ablations/KAGGLE_RUNBOOK.md`).

**Type:** Phase E10 ablation of `EXP0001` (DEC0008). Factor: **augmentation**.

**Question:** Does training-time augmentation (flip, rotate, zoom, lighting) change performance?

**Change from EXP0001** (nothing else differs except identity fields):

| Key | Value |
|-----|-------|
| `augmentations.aug_transforms.enabled` | `False` |

**Dataset / split:** `DS0001` v1.0 / `PP0001` / `SPLIT0001`, as EXP0001.

**Model:** `MODEL0010` — ResNet-50, a separately trained instance.

**Expected outcome:** No directional expectation. Validation ROC-AUC >= 0.90 as a pipeline sanity check.

**Results:** pending. Comparison: `08_Evaluation/ablations/ablation_report.md`.

**Artifacts:** Kaggle dataset `isthisdeception/thesis-exp0004-artifacts`.
