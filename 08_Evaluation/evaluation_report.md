# Evaluation Report

**Evaluation IDs:** EVAL0001–EVAL0006  
**Template:** 10  
**Date:** 2026-11-13

## Metrics

The ranked comparison is EXP0001, EXP0003, EXP0004, EXP0005, EXP0006. Test metrics are in `comparison_tables.csv`. For EXP0001 / MODEL0001 on the SPLIT0001 test split: ROC-AUC 0.9261, PR-AUC 0.9348, balanced accuracy 0.8483, MCC 0.6978, FNR 0.1829, FPR 0.1205. Accuracy is 0.8481 and is reported only inside that set.

The per-split E3 table, including accuracy, is `08_Evaluation/EVAL0001/classification_metrics.csv`.

## Analysis

EXP0003 changes only the training seed. Its test ROC-AUC difference from EXP0001 is inside the 95% interval that includes zero, and the exact McNemar test does not find a decision difference. Removing augmentation, training without ImageNet weights, and reducing the input to 160 pixels each produce a lower test ROC-AUC on this split; the Bonferroni-adjusted intervals exclude zero. Those are differences between the saved runs. `superiority_claim` remains `none`.

## Calibration

EVAL0001 test ECE is 0.0525, MCE is 0.1544, and Brier score is 0.1128 at the frozen threshold. Detail: `08_Evaluation/EVAL0001/calibration_threshold.md`.

## Robustness

Clean balanced accuracy is 0.8483 and clean ROC-AUC is 0.9261. Across 53 perturbed conditions, the lowest balanced accuracy is 0.4999 at `low_quality_upload@0.35_30` (ROC-AUC 0.5314). The full curves are in `08_Evaluation/EVAL0001/robustness/robustness_report.md`.

## Generalization

MODEL0001 at its frozen threshold, from `cross_dataset_metrics.csv`: DS0001 ROC-AUC 0.9261; DS0002 is one class (fake=7364, real=0), so ROC-AUC is undefined; DS0003 ROC-AUC 0.9012; DS0004 ROC-AUC 0.5172; DS0005 is one class (fake=0, real=10000), so ROC-AUC is undefined. On the same 299 `stable_diffusion` images, MODEL0001 recall is 96.3% and MODEL0008 recall is 13.7%. That pair uses SPLIT0002 and is not ranked above.

## Ablation

The one-factor questions and the seed-pair noise floor are in `08_Evaluation/ablations/ablation_report.md`. The statistical reading of those same runs is in `08_Evaluation/statistics/statistics_report.md`.

## Failure analysis

On the EVAL0001 test split the fake miss rate is 0.1829 and the false-fake rate is 0.1205. Where those errors concentrate, and which causes are only hypotheses, is `08_Evaluation/EVAL0001/failure_analysis.md`.

## Statistical testing

Intervals, exact McNemar tests, two-seed variance, and the decision not to run Wilcoxon across seeds are in `08_Evaluation/statistics/`. No superiority claim is made.
