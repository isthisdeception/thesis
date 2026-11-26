# Comparison Study: STEP-050

**Baseline:** EXP0001 (MODEL0001)  
**Phase:** E16  
**Date:** 2026-11-13

A row is ranked only when it keeps the baseline data invariants: dataset DS0001, version v1.0, pipeline PP0001, split SPLIT0001. Labeled one-factor ablations stay in that set. Accuracy is one column of the metric set, never the comparison by itself.

The ROC-AUC difference column is challenger minus baseline. Its interval and `run difference` come from STEP-049. `superiority_claim` is `none` on every row. A difference between two saved runs is not a claim that one method is superior.

## Ranked experiments

| Experiment | Factor | roc_auc | pr_auc | balanced_accuracy | mcc | fnr | fpr | ece | Delta ROC-AUC | Run difference |
|---|---|---|---|---|---|---|---|---|---|---|
| EXP0001 | baseline | 0.9261 | 0.9348 | 0.8483 | 0.6978 | 0.1829 | 0.1205 | 0.0525 | +0.0000 | — |
| EXP0003 | random_seed | 0.9272 | 0.9363 | 0.8481 | 0.6978 | 0.1881 | 0.1157 | 0.0545 | +0.0011 | not_supported |
| EXP0004 | augmentation | 0.8925 | 0.9042 | 0.8059 | 0.6120 | 0.2056 | 0.1825 | 0.0378 | -0.0336 | challenger_lower |
| EXP0005 | pretraining | 0.7017 | 0.7092 | 0.6452 | 0.2912 | 0.3162 | 0.3935 | 0.0230 | -0.2243 | challenger_lower |
| EXP0006 | image_size | 0.8885 | 0.9053 | 0.8039 | 0.6082 | 0.2170 | 0.1753 | 0.0944 | -0.0376 | challenger_lower |

## Not ranked

| Experiment | Reason |
|---|---|
| EXP0002 | different split_id |

EXP0002 trains and tests on SPLIT0002, with Stable Diffusion held out. Its unseen-generator result stays in `08_Evaluation/EVAL0002/unseen_generator/unseen_report.md` and is not a row of the ranked table.

Reading the ranked deltas: the seed replicate's ROC-AUC interval includes zero. The three factor runs are lower than EXP0001 on this test split, and each adjusted interval excludes zero. That supports a difference between those saved runs. It does not support a superiority claim, because each configuration has one seed.

## Multi-Backbone Comparator Study (EXP0001, EXP0007, EXP0008)

Under the identical `DS0001 / v1.0 / PP0001 / SPLIT0001` (`224 x 224` px, 1 frozen + 10 unfrozen epochs, seed 42, validation-only threshold selection) fairness contract, two additional architectures from `05_Models/candidate_models.csv` were trained on Kaggle Tesla T4 GPUs and evaluated across `DS0001`–`DS0005` (`46,369` test images per model; `08_Evaluation/cross_backbone_generalization.csv`; `08_Evaluation/statistics/backbone_paired_tests.csv`):

| Experiment | Model | Architecture | Threshold | Test ROC-AUC | PR-AUC | Balanced Acc. | MCC | ECE | Delta ROC-AUC vs EXP0001 (95% CI) | Exact McNemar p (b / c) | DiFF FNR | 140k ROC-AUC / FPR | Synthbuster FNR / FPR | FairFace FPR |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|---|---|
| EXP0008 | MODEL0004 | ViT-B/16 | 0.4906 | 0.9750 | 0.9775 | 0.9153 | 0.8311 | 0.0211 | +0.0489 `[+0.0439, +0.0541]` | `5.20e-53` (`285 / 788`) | 0.6403 | 0.9893 / 0.0099 | 0.8207 / 0.0867 | 0.6252 |
| EXP0001 | MODEL0001 | ResNet-50 | 0.3951 | 0.9261 | 0.9348 | 0.8483 | 0.6978 | 0.0525 | +0.0000 | — | 0.5024 | 0.9012 / 0.3037 | 0.2370 / 0.7667 | 0.8259 |
| EXP0007 | MODEL0003 | EfficientNet-B4 | 0.5161 | 0.8247 | 0.8424 | 0.7429 | 0.4914 | 0.0272 | -0.1014 `[-0.1100, -0.0930]` | `7.43e-81` (`1,264 / 470`) | 0.6820 | 0.7414 / 0.2209 | 0.0978 / 0.9400 | 0.7653 |

Key empirical findings (`superiority_claim = none`, single-seed saved runs):
1. **In-distribution discrimination:** Patch-based Vision Transformer `MODEL0004` (`ViT-B/16`) exceeds the `DEC0006` sanity bar (`0.9750 > 0.95` ROC-AUC; `0.9153 > 0.90` balanced accuracy; `ECE 0.0211`), whereas compound-scaled `MODEL0003` (`EfficientNet-B4`, native pretraining input `320/380 px`) experiences spatial receptive-field compression at `224 x 224` (`0.8247` ROC-AUC).
2. **Persistent OOD fragility & directional polarization:** Despite `0.9750` in-distribution ROC-AUC and `0.9893` ROC-AUC (`0.99%` FPR) on `DS0003` 140k Faces, `ViT-B/16` still misses `64.03%` of unseen `DS0002` DiFF diffusion faces, `82.07%` of `DS0004` Synthbuster diffusion images (`ECE = 0.6806`), and falsely flags `62.52%` of `DS0005` FairFace authentic portraits. Notably, CNNs (`MODEL0001`, `MODEL0003`) and `ViT-B/16` (`MODEL0004`) polarize in opposite directions on OOD benchmarks, enabling `MOD007` (`K = 3`) multi-specialist fusion to cut silent erroneous verdicts to `3.00%` on `ArtiFact` clean, `1.33%` on `140k Faces`, `3.00%` on `Synthbuster`, `22.33%` on `FairFace`, and `33.33%` on `DiFF` (`EVAL0008`).
