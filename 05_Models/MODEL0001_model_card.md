# Model Card: MODEL0001

**Experiment:** EXP0001  
**Status:** trained (2026-11-08). Not deployment ready.  
**Version:** 1.0

**Architecture:** ResNet-50 (`torchvision`, ImageNet-1k pretrained), trained with the FastAI standard in `05_Models/FASTAI_TRAINING_STANDARD.md`. Binary classifier, vocabulary `[fake, real]`, positive class `fake`.

**Training Data:** `DS0001` v1.0, preprocessing `PP0001`, split `SPLIT0001` (`grouped_random`, seed 42, grouped by identity and generator, leakage PASS). Train 34,993 / val 7,502 / test 7,505, class-balanced. Every generator in the test partition also appears in training. This is the primary architecture track, not the generator hold-out track (`SPLIT0002`).

**Training:** 1 frozen epoch then up to 10 unfrozen epochs, `fine_tune`, learning rate `3.311313e-4` from the LR Finder (`valley`). Best epoch 7 by validation loss (0.342). Early stopping (patience 3) fired on epoch 10, which was also the last scheduled epoch. Wall time 36.7 min on a Tesla T4. Code at session HEAD `c300be7`. Config `06_Experiments/EXP0001/config.yaml` (SHA-256 `d3359cf56f11…`).

**Evaluation:** Test partition of `SPLIT0001`, threshold 0.395 chosen on the validation partition only (`max_balanced_accuracy`). Full precision is in `06_Experiments/EXP0001/metrics/test_metrics.json`.

| Metric | Test |
|--------|------|
| ROC-AUC | 0.926 |
| PR-AUC | 0.935 |
| Balanced accuracy | 0.848 |
| F1 | 0.844 |
| MCC | 0.698 |
| Precision / Recall | 0.873 / 0.817 |
| ECE / Brier | 0.052 / 0.113 |

The pre-registered sanity bar (DEC0006) was ROC-AUC ≥ 0.95 and balanced accuracy ≥ 0.90. This run is below that bar and above the 0.90 ROC-AUC line that would have marked a pipeline failure. The result stands as observed.

**Limitations:** Single seed. In-distribution test only. One operating threshold. No compression, perturbation, or cross-dataset evaluation. Calibration error is about 0.05. The sanity bar was missed.

**Bias:** Not measured. `DS0005` (FairFace) was not run. No demographic claim is supported.

**Intended Use:** Fair reference for later architecture comparisons that keep `DS0001 / v1.0 / PP0001 / SPLIT0001`, the same metric set, and the same threshold policy (`05_Models/baseline_plan.md`).

**Not Recommended For:** Deployment, screening, a claim of cross-generator generalization, or a claim about demographic fairness.

**Weights:** Kaggle dataset `isthisdeception/thesis-experiment-artifacts`: `MODEL0001_export.pkl`, `MODEL0001_weights.pth`, `EXP0001_best.pth` (epoch 7). Checksums are in `07_Checkpoints/EXP0001_checkpoints.md`. Weights are not in Git.
