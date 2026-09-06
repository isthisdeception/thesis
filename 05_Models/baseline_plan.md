# STEP-033 — Baseline Strategy & Fairness Invariants

## Purpose

Define the first fair baseline experiment and the invariants that every later comparison must preserve. This plan implements Phase M2 and protects Phase M13 / E16 from invalid apples-to-oranges comparisons.

## Baseline Choice

**Approved first baseline architecture:** `MODEL0001` — `ResNet-50`

Why this is the first baseline:
- It is the highest-ranked approved shortlist candidate from `STEP-032`.
- It is fully FastAI-native and low-cost enough for repeated Kaggle runs.
- It provides a strong, interpretable CNN reference before heavier architectures are introduced.

## First Baseline Experiment Definition

Reserve `EXP0001` as the canonical first baseline run with the following frozen IDs:

- **Model ID:** `MODEL0001`
- **Architecture:** `ResNet-50`
- **Dataset ID:** `DS0001`
- **Dataset Version:** `v1.0`
- **Preprocessing ID:** `PP0001`
- **Output ID:** `DS0001_PP0001`
- **Split ID:** `SPLIT0001`
- **Canonical split folder:** `03_Datasets/splits/DS0001_PP0001_SPLIT0001`
- **Split scheme:** `grouped_random`
- **Random seed:** `42`
- **Processed Kaggle dataset:** `isthisdeception/ds0001-pp0001`
- **Primary task:** binary `real` vs `fake` face detection

This run is the reference point for later architecture comparisons. It is not the final backbone decision; it is the baseline anchor required by Phase M2.

## Fairness Invariants

Every experiment that claims to be compared against the baseline in Phase M13 / E16 must keep the following constant unless the comparison is explicitly labeled as a different study track.

### Frozen data invariants

- Same **Dataset ID**: `DS0001`
- Same **Dataset Version**: `v1.0`
- Same **Preprocessing ID**: `PP0001`
- Same **Output ID**: `DS0001_PP0001`
- Same **Split ID**: `SPLIT0001`
- Same split assignments file and the same train/val/test partitions
- No relabeling, filtering, resampling, or replacement of examples after the split is frozen

### Frozen training-policy invariants

- Same experiment family objective: binary `real` vs `fake`
- Same random seed policy: single-seed comparisons use seed `42`
- Same data leakage requirement: `PASS`
- Same train/val/test role semantics from the split registry
- Same augmentation policy family unless the experiment is explicitly an augmentation ablation
- Same optimizer/loss/epoch-budget policy family once `STEP-034` finalizes config rules
- Same checkpoint/recovery policy and artifact handling rules

### Frozen evaluation invariants

- Same prediction target: test partition of `DS0001_PP0001_SPLIT0001`
- Same evaluation pipeline and report structure
- Same metric set for every compared run
- Same threshold-selection policy for thresholded metrics
- Same calibration analysis policy
- Same performance logging fields

## Canonical Metric Set

The baseline and every fairness-compatible comparison must report at least:

- `ROC-AUC`
- `PR-AUC`
- `F1`
- `Balanced Accuracy`
- `MCC`
- `Precision`
- `Recall / Sensitivity`
- `Specificity`
- `FPR`
- `FNR`

Secondary but still required:

- `Accuracy` (never alone)
- calibration metrics: `ECE`, `Brier score`
- performance metrics: training time, inference throughput, GPU memory footprint

## Threshold Policy

To prevent cherry-picking:

- Use the **validation partition only** to choose any operating threshold.
- Freeze that threshold before evaluating the test partition.
- Report threshold-free metrics (`ROC-AUC`, `PR-AUC`) alongside thresholded metrics (`F1`, `Balanced Accuracy`, `Precision`, `Recall`, `Specificity`).

Comparisons are invalid if one model is judged at a hand-tuned threshold and another at a default threshold without the same policy.

## Valid Comparison Types

The following are valid under Phase M13 / E16:

1. `MODEL0002` vs `MODEL0001` on `DS0001 / v1.0 / PP0001 / SPLIT0001` with the same metric set and seed policy.
2. `MODEL0003` vs `MODEL0001` on `DS0001 / v1.0 / PP0001 / SPLIT0001` with the same evaluation pipeline.
3. A later `MODEL0004` transformer comparison on the same frozen dataset/split track, clearly labeled as a higher-compute comparator.
4. Hyperparameter ablations within the same frozen data/split track, provided the study is explicitly labeled as an ablation rather than a pure architecture comparison.
5. A dedicated robustness track using `DS0001 / v1.0 / PP0001 / SPLIT0002`, but only when **all** compared models use that same LOGO split.

## Invalid Comparison Types

The following must be rejected as unfair:

1. Comparing `EXP0001` on `SPLIT0001` against a model trained or tested on `SPLIT0002`.
2. Comparing a run trained on `DS0001` against a run trained on `DS0003` and treating it as the same baseline table.
3. Comparing models that use different preprocessing pipelines (`PP0001` vs `PP0003` or `PP0006`) as if the architecture were the only changed variable.
4. Comparing a single-seed result against a multi-seed average.
5. Changing augmentation policy, loss, or sampling rules and presenting the result as an architecture-only comparison.
6. Using `DS0002` fake-only data as the primary training baseline for binary `real/fake` comparison.
7. Mixing quick-baseline convenience runs with the formal baseline table without a separate label.

## Study Tracks

To keep future comparisons clean, use these labels:

- **Primary architecture track:** `DS0001 / v1.0 / PP0001 / SPLIT0001`
- **Generator hold-out robustness track:** `DS0001 / v1.0 / PP0001 / SPLIT0002`
- **Quick convenience track:** `DS0003 / v1.0 / PP0003 / SPLIT0001` for smoke baselines only, not headline comparison
- **External/difficulty evaluation track:** `DS0002`, `DS0004`, `DS0005` for robustness, diffusion difficulty, and bias analysis after the primary baseline exists

Results from different tracks can be discussed together, but they cannot be merged into a single fairness comparison table.

## Decision Outcome

- `EXP0001` will be created as the `MODEL0001` ResNet-50 baseline on `DS0001_PP0001_SPLIT0001`.
- `MODEL0002` Xception and `MODEL0003` EfficientNet-B4 are the first fairness-compatible architecture comparators.
- `DEF-002` remains open until post-training evidence justifies a final backbone choice.
