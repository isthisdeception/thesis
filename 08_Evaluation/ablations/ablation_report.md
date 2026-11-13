# Ablation Study: STEP-048

**Baseline:** EXP0001 (MODEL0001)  
**Phase:** E10  
**Date:** 2026-11-13

Every ablation changes exactly one factor of EXP0001 (checked when the experiment was created; DEC0008). All use DS0001 / v1.0 / PP0001 / SPLIT0001, the same epoch budget, and the same threshold rule (max balanced accuracy on val). Metrics are on the SPLIT0001 test partition at each model's own val-chosen threshold.

**Noise floor:** EXP0003 changes only the training seed. Its differences from EXP0001 are the run-to-run variation. A difference no larger than that is marked `within seed noise`.

## Test metrics

| Experiment | Factor | roc_auc | balanced_accuracy | mcc | fnr | fpr | ece | Best epoch | Minutes |
|---|---|---|---|---|---|---|---|---|---|
| EXP0001 | baseline | 0.9261 | 0.8483 | 0.6978 | 0.1829 | 0.1205 | 0.0525 | 7 | 36.7 |
| EXP0003 | random_seed | 0.9272 | 0.8481 | 0.6978 | 0.1881 | 0.1157 | 0.0545 | 9 | 56.5 |
| EXP0004 | augmentation | 0.8925 | 0.8059 | 0.6120 | 0.2056 | 0.1825 | 0.0378 | 3 | 20.1 |
| EXP0005 | pretraining | 0.7017 | 0.6452 | 0.2912 | 0.3162 | 0.3935 | 0.0230 | 10 | 33.1 |
| EXP0006 | image_size | 0.8885 | 0.8039 | 0.6082 | 0.2170 | 0.1753 | 0.0944 | 10 | 25.2 |

## Differences from EXP0001

| Experiment | Factor | Δroc_auc | Δbalanced_accuracy | Δmcc | Δfnr | Δfpr | Δece |
|---|---|---|---|---|---|---|---|
| EXP0003 | random_seed | +0.0011 | -0.0002 | -0.0000 | +0.0053 | -0.0048 | +0.0021 |
| EXP0004 | augmentation | -0.0336 | -0.0424 | -0.0858 | +0.0228 | +0.0620 | -0.0147 |
| EXP0005 | pretraining | -0.2243 | -0.2032 | -0.4065 | +0.1334 | +0.2729 | -0.0295 |
| EXP0006 | image_size | -0.0376 | -0.0444 | -0.0896 | +0.0341 | +0.0548 | +0.0420 |

`(noise)`: the difference is no larger than the seed replicate's for that metric.

## Answers

- **random_seed** (EXP0003): How much do the metrics change when only the training seed changes? ROC-AUC changes by +0.0011, balanced accuracy by -0.0002, MCC by -0.0000.
- **augmentation** (EXP0004): Does training-time augmentation (flip, rotate, zoom, lighting) change performance? Beyond seed noise: roc_auc worse (-0.0336), balanced_accuracy worse (-0.0424), mcc worse (-0.0858), fnr worse (+0.0228), fpr worse (+0.0620), ece better (-0.0147).
- **pretraining** (EXP0005): How much does ImageNet pretraining contribute under the same 11-epoch budget? Beyond seed noise: roc_auc worse (-0.2243), balanced_accuracy worse (-0.2032), mcc worse (-0.4065), fnr worse (+0.1334), fpr worse (+0.2729), ece better (-0.0295).
- **image_size** (EXP0006): Does reducing the model input from 224 to 160 pixels change performance? Beyond seed noise: roc_auc worse (-0.0376), balanced_accuracy worse (-0.0444), mcc worse (-0.0896), fnr worse (+0.0341), fpr worse (+0.0548), ece worse (+0.0420).

Per-metric values and flags for all metrics: `ablation_results.csv`. Figure spec: FIG0020.

## Limits

- One seed per configuration; the noise floor comes from a single seed pair. Formal tests are STEP-049 (Phase E11).
- EXP0004 stopped at epoch 3 under the baseline early-stopping rule (patience 3). The other runs used more of the 11-epoch budget. That is the configured rule firing, not a second changed factor.
- In-distribution test only (SPLIT0001). Robustness and cross-dataset behaviour of the ablations were not measured.
- Every ablation reuses EXP0001's learning rate and schedule. For the no-pretraining run this keeps one factor changed, but it is not a tuned from-scratch training.
- Evidence-module, confidence, and explainability ablations wait until those modules exist (DEC0008).
