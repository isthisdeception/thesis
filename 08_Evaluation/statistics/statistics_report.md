# Statistical Testing: STEP-049

**Baseline:** EXP0001  
**Phase:** E11  
**Date:** 2026-11-13

Tests use the saved 7505 SPLIT0001 test predictions of EXP0001 and the STEP-048 runs. Images are paired by id. Thresholded metrics use each run's own saved decisions. Bootstrap intervals are percentiles of 10000 resamples (seed 49).

**What a result can support.** A 98.3% interval for the primary metric (roc_auc) that excludes zero supports a difference between those two trained runs, after a Bonferroni adjustment for the 3 factor comparisons (family-wise alpha 0.05). The seed replicate is reported at 95% and is not part of that family. None of these results is a superiority claim. Each configuration was trained once, so the tests do not separate a factor from run-to-run variation.

## Primary metric, challenger minus baseline

| Challenger | Factor | Delta ROC-AUC | 95% CI | Adjusted CI | Runs differ | Larger than the seed pair |
|---|---|---|---|---|---|---|
| EXP0003 | random_seed | +0.0011 | [-0.0012, +0.0035] | [-0.0012, +0.0035] | not_supported | False |
| EXP0004 | augmentation | -0.0336 | [-0.0385, -0.0287] | [-0.0396, -0.0279] | challenger_lower | True |
| EXP0005 | pretraining | -0.2243 | [-0.2359, -0.2127] | [-0.2383, -0.2101] | challenger_lower | True |
| EXP0006 | image_size | -0.0376 | [-0.0434, -0.0319] | [-0.0447, -0.0307] | challenger_lower | True |

`Runs differ` uses the adjusted interval for a factor and the 95% interval for the seed replicate. `Larger than the seed pair` compares the absolute delta with |EXP0003 − EXP0001| on that metric. That comparison is one pair of runs, not a test.

## Decisions (exact McNemar)

b counts images the baseline got right and the challenger got wrong. c counts the reverse. A small adjusted p-value means the saved decisions disagree. It does not say which run is better.

| Challenger | Factor | Agree | b | c | Accuracy delta | Odds c/b | p | Adjusted p | Decisions differ |
|---|---|---|---|---|---|---|---|---|---|
| EXP0003 | random_seed | 7005 | 251 | 249 | -0.0003 | 0.992 | 0.964 | 0.964 | False |
| EXP0004 | augmentation | 6478 | 672 | 355 | -0.0422 | 0.528 | 2.78e-23 | 8.34e-23 | True |
| EXP0005 | pretraining | 5002 | 2012 | 491 | -0.2027 | 0.244 | 2.37e-217 | 7.1e-217 | True |
| EXP0006 | image_size | 6308 | 765 | 432 | -0.0444 | 0.565 | 4.52e-22 | 1.36e-21 | True |

## Seed variance and repeatability

Decision agreement 0.9334, Cohen's kappa 0.8662, probability Pearson 0.9662, mean absolute probability difference 0.0601 (EXP0001 vs EXP0003, n=7505).

| Metric | EXP0001 | EXP0003 | Mean | Absolute difference | Sample SD (n=2) | Wilcoxon |
|---|---|---|---|---|---|---|
| roc_auc | 0.9261 | 0.9272 | 0.9266 | 0.0011 | 0.0008 | not_run |
| balanced_accuracy | 0.8483 | 0.8481 | 0.8482 | 0.0002 | 0.0002 | not_run |
| mcc | 0.6978 | 0.6978 | 0.6978 | 0.0000 | 0.0000 | not_run |

Sample SD with two observations is the absolute difference divided by sqrt(2). Wilcoxon signed-rank across seeds was not run: Two seeds are two observations. A two-sided signed-rank test at alpha 0.05 needs at least 6 non-zero pairs. Further seeds would be new experiment IDs.

## Other metrics

Balanced accuracy and MCC are in `paired_tests.csv` and `bootstrap_cis.csv` with the same intervals. They are descriptive. The pre-specified primary metric is ROC-AUC, so they are not a second family of claims.

## Limits

- No superiority claim is made. `superiority_claim` is `none` on every row.
- One seed per configuration. A factor-versus-seed test needs new experiment IDs, at least six seeds.
- McNemar uses each run's own validation-chosen threshold, so decision differences mix ranking and operating point.
- EXP0004 stopped at epoch 3. That early stop is part of the saved run being compared.
- EXP0002 is a different split and is outside this comparison.
- Intervals are percentile bootstrap intervals of these test images, not of a new population of images.
