# 08_Evaluation

**Purpose:** All evaluation outputs and the Evaluation Registry.

## Contents
Metric CSVs, ROC/PR data, evaluation reports, failure analysis, prediction validation.

STEP-041 inputs for EXP0001 live in `EXP0001/` (predictions, confusion, ROC, PR, calibration, Grad-CAM case list). Schema: `EXP0001/SCHEMA.md`. These are data files. Figures are specified later, not rendered here.

STEP-042: `EVAL0001/prediction_validation_report.md` records the E1–E2 checks. Metrics are not computed there.

STEP-043: `EVAL0001/classification_metrics.csv` holds the full E3 suite for `val` and `test`. `EVAL0001/classification_metrics.md` is the metrics section for the evaluation report, with per-metric notes. Both are written by `python -m classification_metrics` from `17_Automation/`, which refuses to run unless the STEP-042 report passed.

STEP-044: `python -m calibration_threshold` writes `EVAL0001/calibration_summary.csv` (ECE, MCE, Brier), `reliability.csv`, `confidence_distribution.csv`, `threshold_sweep.csv`, `operating_points.csv`, and the report section `calibration_threshold.md`. Thresholds are chosen on `val` only. Figure specs are FIG0011–FIG0013. Status is `calibration_computed` in `evaluation_registry.csv`.

## Workflow
Evaluation agents write, Figures/Tables consume. Do not re-compute metrics without new Evaluation ID.

## Owner
Evaluation Agents

## Related Folders
09_Figures, 10_Tables, 15_Writing

## Expected Outputs
evaluation_report.md, evaluation_registry.csv

> *This folder follows the canonical repository hygiene and naming rules defined in `MASTER_RESEARCH_OPERATING_SYSTEM.md`. Please refer to the handbook for full policy details.*

## Cross-Linked Agents

The following agents operate within this domain:
- [Metric](../../19_Prompts/agents/evaluation/metric.md)
- [Calibration](../../19_Prompts/agents/evaluation/calibration.md)
- [Robustness](../../19_Prompts/agents/evaluation/robustness.md)
- [Generalization](../../19_Prompts/agents/evaluation/generalization.md)
- [Ablation](../../19_Prompts/agents/evaluation/ablation.md)
- [Statistics](../../19_Prompts/agents/evaluation/statistics.md)
- [Comparison](../../19_Prompts/agents/evaluation/comparison.md)
- [Failure Analysis](../../19_Prompts/agents/evaluation/failure_analysis.md)
- [Explainability](../../19_Prompts/agents/evaluation/explainability.md)
- [Reporting](../../19_Prompts/agents/evaluation/reporting.md)
