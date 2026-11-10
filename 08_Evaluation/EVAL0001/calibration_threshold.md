# Calibration and Threshold Analysis: EVAL0001

**Experiment:** EXP0001
**Phases:** E4, E5
**Date:** 2026-11-10

Source: `08_Evaluation/EXP0001/predictions.csv` (SHA-256 `4553498081ef7da8574c6742f0f5fbec08993556b6ef0b25abcd76c313c1cc90`), validated in `prediction_validation_report.md`. No figures are rendered (A.9); specs are FIG0011–FIG0013.

## Probability, confidence, reliability

- **Probability** is the model's P(fake) for an image. It is a score, not forensic certainty.
- **Confidence** is the probability of the predicted class, max(p, 1 − p) at the decision taken.
- **Reliability** is how often predictions at a given probability or confidence are right. Calibration compares probability with the observed fake share; the confidence table compares confidence with accuracy.

## Calibration (E4)

Equal-width bins: 15. `brier_reference` is the Brier score of always predicting the fake share.

| Metric | test | val |
|--------|------|------|
| n | 7505 | 7502 |
| ece | 0.0525 | 0.0510 |
| mce | 0.1544 | 0.1535 |
| brier | 0.1128 | 0.1069 |
| brier_reference | 0.2500 | 0.2500 |
| log_loss | 0.3672 | 0.3427 |
| mean_probability | 0.4511 | 0.4466 |
| fraction_positive | 0.5035 | 0.4957 |
| mean_confidence | 0.8785 | 0.8804 |
| accuracy | 0.8481 | 0.8567 |

- On `test`, the mean P(fake) is 0.451, below the fake share of 0.504.
- The largest bin gap is +0.154 in [0.200, 0.267] (298 images). A positive gap means more fakes than the probability implies.
- Confidence exceeds accuracy by more than 0.02 in 6 of 10 confidence bins.
- 49.4% of `test` decisions have confidence ≥ 0.95; their accuracy is 0.962.

Bins are in `reliability.csv` and `confidence_distribution.csv`. Bin `-1` holds decisions whose confidence is below 0.5, which happens because the threshold is not 0.5.

## Threshold analysis (E5)

Every threshold is chosen on `val`, then applied to `test` unchanged. Sweep: `threshold_sweep.csv` (0.00–1.00, step 0.01).

| Point | Criterion | threshold | recall | specificity | precision | fpr | fnr | balanced_accuracy | f1 | mcc |
|-------|-----------|------|------|------|------|------|------|------|------|------|
| frozen | max balanced accuracy on val (rule set in config before training) | 0.3951 | 0.8171 | 0.8795 | 0.8731 | 0.1205 | 0.1829 | 0.8483 | 0.8442 | 0.6978 |
| max_f1 | max F1 on val | 0.3099 | 0.8513 | 0.8333 | 0.8382 | 0.1667 | 0.1487 | 0.8423 | 0.8447 | 0.6848 |
| fixed_0.5 | 0.5 | 0.5000 | 0.7788 | 0.9155 | 0.9033 | 0.0845 | 0.2212 | 0.8471 | 0.8364 | 0.7003 |
| high_specificity | lowest threshold with FPR <= 0.05 on val | 0.6288 | 0.7211 | 0.9444 | 0.9294 | 0.0556 | 0.2789 | 0.8328 | 0.8121 | 0.6820 |
| high_sensitivity | highest threshold with FNR <= 0.05 on val | 0.0894 | 0.9447 | 0.6151 | 0.7134 | 0.3849 | 0.0553 | 0.7799 | 0.8129 | 0.5938 |

Recomputed decisions use `prob >= threshold`. One `val` row sits within 1e-5 of the frozen threshold because the CSV rounded its probability, so `val` counts for `frozen` can differ from `classification_metrics.csv` by one image. `test` counts match.

## Recommended operating points

- **Reporting:** `frozen` (threshold 0.3951). Its selection rule was set in the EXP0001 config before training, and §7.2 forbids changing the evaluation after seeing results. It equals the ROC (Youden J) optimum on `val`.
- **Flag for review:** `high_specificity` (threshold 0.6288). On `test`: FNR 0.279, FPR 0.056, versus FNR 0.183, FPR 0.121 for `frozen`.
- **Screening:** `high_sensitivity` (threshold 0.0894). On `test`: FNR 0.055, FPR 0.385, versus FNR 0.183, FPR 0.121 for `frozen`.
- `max_f1` and `fixed_0.5` are listed for comparison only.

## For Module 9

Raw P(fake) is not shown as certainty. ECE is 0.052 and MCE is 0.154 on `test`. Post-hoc calibration fitted on `val` (for example temperature scaling) has not been applied; any later use needs a new Evaluation ID.
