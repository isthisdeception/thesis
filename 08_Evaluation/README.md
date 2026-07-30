# 08_Evaluation

**Purpose:** All evaluation outputs and the Evaluation Registry.

## Contents
Metric CSVs, ROC/PR data, evaluation reports, failure analysis, prediction validation.

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
