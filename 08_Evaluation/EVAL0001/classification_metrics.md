# Classification Metrics: EVAL0001

**Experiment:** EXP0001
**Phase:** E3
**Date:** 2026-11-10

Source: `08_Evaluation/EXP0001/predictions.csv` (SHA-256 `4553498081ef7da8574c6742f0f5fbec08993556b6ef0b25abcd76c313c1cc90`), validated in `prediction_validation_report.md`. Values: `classification_metrics.csv`.

Positive class: `fake`. Thresholded metrics use the saved decisions at threshold 0.3951. The threshold was chosen on `val`, so `val` values are optimistic. Report `test`.

## Counts

| Split | n | fake | real | TP | TN | FP | FN |
|-------|---|------|------|----|----|----|----|
| test | 7505 | 3779 | 3726 | 3088 | 3277 | 449 | 691 |
| val | 7502 | 3719 | 3783 | 3084 | 3343 | 440 | 635 |

## Metrics

| Metric | test | val |
|--------|------|------|
| accuracy | 0.8481 | 0.8567 |
| precision | 0.8731 | 0.8751 |
| recall | 0.8171 | 0.8293 |
| sensitivity | 0.8171 | 0.8293 |
| specificity | 0.8795 | 0.8837 |
| f1 | 0.8442 | 0.8516 |
| balanced_accuracy | 0.8483 | 0.8565 |
| mcc | 0.6978 | 0.7142 |
| roc_auc | 0.9261 | 0.9341 |
| pr_auc | 0.9348 | 0.9399 |
| fpr | 0.1205 | 0.1163 |
| fnr | 0.1829 | 0.1707 |
| precision_macro | 0.8495 | 0.8578 |
| precision_micro | 0.8481 | 0.8567 |
| precision_weighted | 0.8496 | 0.8576 |
| recall_macro | 0.8483 | 0.8565 |
| recall_micro | 0.8481 | 0.8567 |
| recall_weighted | 0.8481 | 0.8567 |
| f1_macro | 0.8480 | 0.8565 |
| f1_micro | 0.8481 | 0.8567 |
| f1_weighted | 0.8480 | 0.8566 |

## Reading the table

- Fake share in `test` is 0.504. That is the chance level for PR-AUC.
- FNR is 0.1829 and FPR is 0.1205 on `test`. Missed fakes are the larger error.
- Micro averages equal accuracy in binary classification. They are not separate results.
- Accuracy is never reported without balanced accuracy, MCC, ROC-AUC, and PR-AUC.
- No confidence intervals here. Statistical testing is Phase E11.

## Metric notes

| Metric | When appropriate | How to interpret | Common mistakes | Publication recommendation |
|--------|------------------|------------------|-----------------|----------------------------|
| accuracy | Only alongside the rest of this table, on near-balanced data. | Share of all images classified correctly. | Reporting it alone; a constant classifier scores the majority share. | Report with balanced accuracy and MCC, never alone. |
| precision | When a false fake alarm is costly. | Of images flagged fake, the share that are fake. | Depends on the fake share in the test set; does not transfer to other prevalences. | Report with recall and the threshold used. |
| recall | When a missed fake is costly. | Of fake images, the share flagged fake. | Can be pushed to 1.0 by flagging everything; read it with specificity. | Report with precision or specificity. |
| sensitivity | Same as recall; the term used next to specificity. | True positive rate for the fake class. Equal to recall by definition. | Listing it as a separate result from recall. | Use one name per table; pair with specificity. |
| specificity | When real images must not be flagged. | Of real images, the share classified real. | Omitting it, which hides how often real images are flagged. | Report with sensitivity. |
| f1 | One thresholded score for the fake class. | Harmonic mean of precision and recall for the fake class. | Ignores true negatives; changes when the positive class is swapped. | Report with MCC and state which class is positive. |
| balanced_accuracy | Always; it is robust to class imbalance. | Mean of sensitivity and specificity. 0.5 is chance. | Comparing values computed at thresholds tuned on different data. | Primary thresholded metric (DEC0006 sanity bar). |
| mcc | Always; uses all four confusion cells. | Correlation between prediction and label, from -1 to 1. 0 is chance. | Reading it on the 0-1 scale of accuracy; 0.7 is strong, not mediocre. | Report as the imbalance-aware summary of the confusion matrix. |
| roc_auc | Threshold-free ranking quality. | Probability that a random fake scores above a random real image. | Can look high under heavy imbalance while precision is poor. | Primary threshold-free metric; report with PR-AUC. |
| pr_auc | Threshold-free quality for the fake class, especially under imbalance. | Average precision over recall levels. Chance level is the fake share. | Comparing across test sets with different fake shares. | Report with ROC-AUC and the fake share. |
| fpr | When the cost of flagging a real image matters. | Share of real images flagged fake. Equal to 1 - specificity. | Confusing it with the false discovery rate (1 - precision). | Report with FNR at the same threshold. |
| fnr | When the cost of missing a fake matters. | Share of fake images classified real. Equal to 1 - recall. | Reporting FPR without FNR, which hides one error type. | Report with FPR at the same threshold. |
| macro averages | Class-symmetric view; each class counts equally. | Unweighted mean of the per-class real and fake scores. | Mixing it up with weighted averages. | Report macro F1 when the two classes matter equally. |
| micro averages | Rarely useful in binary classification. | Pools all decisions. In binary tasks every micro score equals accuracy. | Presenting micro F1 as a separate result from accuracy. | Keep in the CSV for completeness; do not report as its own result. |
| weighted averages | When per-class scores should follow class frequency. | Per-class scores averaged by class support. | Hiding weak minority-class scores behind the majority class. | Report only with macro averages. |
