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
