# Evaluation Audit

**Audit date:** 2026-11-13  
**Gate:** Checklist 8 — Evaluation  
**Approval Status:** PASS

## Summary

Checklist 8 covers EVAL0001–EVAL0006. The ranked comparison is EXP0001 and the STEP-048 one-factor runs. EXP0002 stays out of that table because it uses SPLIT0002. No publication figure was rendered.

## Passed

| Checklist 8 item | Evidence |
|---|---|
| Metrics complete | `08_Evaluation/EVAL0001/classification_metrics.csv` |
| ROC and PR data | `08_Evaluation/EXP0001/roc_curve.csv; 08_Evaluation/EXP0001/pr_curve.csv` |
| Confusion data | `08_Evaluation/EVAL0001/confusion_matrix.csv` |
| Calibration | `08_Evaluation/EVAL0001/calibration_summary.csv` |
| Statistical testing | `08_Evaluation/statistics/statistics_report.md` |
| Robustness | `08_Evaluation/EVAL0001/robustness/robustness_report.md` |
| Generalization and unseen generator | `08_Evaluation/EVAL0001/generalization/cross_dataset_report.md; 08_Evaluation/EVAL0002/unseen_generator/unseen_report.md` |
| Ablation | `08_Evaluation/ablations/ablation_report.md` |
| Failure analysis | `08_Evaluation/EVAL0001/failure_analysis.md` |
| Fair comparison only | `08_Evaluation/comparison_report.md` |
| Figure specs, data only | `FIG0011, FIG0013, FIG0014, FIG0016, FIG0020–FIG0025` |
| Table specs | `TAB0002, TAB0003` |
| Evaluation registry | `08_Evaluation/evaluation_registry.csv` |

## Failed

None.

## Evidence

The comparison module refuses a ranked row whose dataset, version, pipeline, or split differs from EXP0001. Metric values are the STEP-048 table. Intervals are the STEP-049 table. Neither file is recomputed here.

## Recommendations

1. Human confirmation of Checklist 8 was given on 2026-11-17. STEP-051 may start.
2. A new metric or a new test set needs a new EVAL ID.
3. More seeds, if a seed-level Wilcoxon test is wanted, are new EXP IDs.
