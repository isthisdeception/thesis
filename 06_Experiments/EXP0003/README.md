# Experiment: EXP0003

**Status:** ready. Waiting for the STEP-048 Kaggle session (`06_Experiments/ablations/KAGGLE_RUNBOOK.md`).

**Type:** Phase E10 ablation of `EXP0001` (DEC0008). Factor: **random_seed**.

**Question:** How much do the metrics change when only the training seed changes?

**Change from EXP0001** (nothing else differs except identity fields):

| Key | Value |
|-----|-------|
| `random_seed` | `43` |

**Dataset / split:** `DS0001` v1.0 / `PP0001` / `SPLIT0001`, as EXP0001.

**Model:** `MODEL0009` — ResNet-50, a separately trained instance.

**Expected outcome:** No directional expectation. The differences from EXP0001 are the run-to-run variation that every other ablation is compared against.

**Results:** pending. Comparison: `08_Evaluation/ablations/ablation_report.md`.

**Artifacts:** Kaggle dataset `isthisdeception/thesis-exp0003-artifacts`.
