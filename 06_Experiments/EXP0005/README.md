# Experiment: EXP0005

**Status:** ready. Waiting for the STEP-048 Kaggle session (`06_Experiments/ablations/KAGGLE_RUNBOOK.md`).

**Type:** Phase E10 ablation of `EXP0001` (DEC0008). Factor: **pretraining**.

**Question:** How much does ImageNet pretraining contribute under the same 11-epoch budget?

**Change from EXP0001** (nothing else differs except identity fields):

| Key | Value |
|-----|-------|
| `model.pretrained` | `False` |
| `model.pretrained_weights` | `none` |

**Dataset / split:** `DS0001` v1.0 / `PP0001` / `SPLIT0001`, as EXP0001.

**Model:** `MODEL0011` — ResNet-50, a separately trained instance.

**Expected outcome:** Lower than EXP0001 is likely; no sanity bar, because training from scratch within the baseline budget may stay far below it. Reported as observed.

**Results:** pending. Comparison: `08_Evaluation/ablations/ablation_report.md`.

**Artifacts:** Kaggle dataset `isthisdeception/thesis-exp0005-artifacts`.
