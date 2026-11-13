# Experiment: EXP0006

**Status:** ready. Waiting for the STEP-048 Kaggle session (`06_Experiments/ablations/KAGGLE_RUNBOOK.md`).

**Type:** Phase E10 ablation of `EXP0001` (DEC0008). Factor: **image_size**.

**Question:** Does reducing the model input from 224 to 160 pixels change performance?

**Change from EXP0001** (nothing else differs except identity fields):

| Key | Value |
|-----|-------|
| `image_size` | `160` |
| `fastai.item_tfms.resize` | `160` |

**Dataset / split:** `DS0001` v1.0 / `PP0001` / `SPLIT0001`, as EXP0001.

**Model:** `MODEL0012` — ResNet-50, a separately trained instance.

**Expected outcome:** No directional expectation. Validation ROC-AUC >= 0.90 as a pipeline sanity check.

**Results:** pending. Comparison: `08_Evaluation/ablations/ablation_report.md`.

**Artifacts:** Kaggle dataset `isthisdeception/thesis-exp0006-artifacts`.
