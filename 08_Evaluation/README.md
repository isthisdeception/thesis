# 08_Evaluation

**Purpose:** All evaluation outputs and the Evaluation Registry.

## Contents
Metric CSVs, ROC/PR data, evaluation reports, failure analysis, prediction validation.

STEP-041 inputs for EXP0001 live in `EXP0001/` (predictions, confusion, ROC, PR, calibration, Grad-CAM case list). Schema: `EXP0001/SCHEMA.md`. These are data files. Figures are specified later, not rendered here.

STEP-042: `EVAL0001/prediction_validation_report.md` records the E1–E2 checks. Metrics are not computed there.

STEP-043: `EVAL0001/classification_metrics.csv` holds the full E3 suite for `val` and `test`. `EVAL0001/classification_metrics.md` is the metrics section for the evaluation report, with per-metric notes. Both are written by `python -m classification_metrics` from `17_Automation/`, which refuses to run unless the STEP-042 report passed.

STEP-044: `python -m calibration_threshold` writes `EVAL0001/calibration_summary.csv` (ECE, MCE, Brier), `reliability.csv`, `confidence_distribution.csv`, `threshold_sweep.csv`, `operating_points.csv`, and the report section `calibration_threshold.md`. Thresholds are chosen on `val` only. Figure specs are FIG0011–FIG0013.

STEP-045: `python -m failure_analysis` joins the predictions to the DS0001/PP0001 preprocessing index and writes `EVAL0001/confusion_matrix.csv`, `per_class_stats.csv`, `error_by_group.csv` (per generator and real source, Wilson 95% intervals), `error_summary.csv`, `error_cases.csv` (most confident errors for manual review), and `failure_analysis.md`. Causes are hypotheses only. Figure specs are FIG0014–FIG0015. Status is `failure_analysis_complete` in `evaluation_registry.csv`.

STEP-046: `EVAL0001/robustness/` holds the perturbation config (`config.yaml`), the Kaggle notebook and runbook, and, after the Kaggle run, `robustness_probs.csv`, `run_manifest.json`, the analysis CSVs, and `robustness_report.md`. Inference needs the MODEL0001 export and the processed images, so it runs on Kaggle only. Figure specs are FIG0016–FIG0017. Ran on Kaggle 2026-11-10; status is `robustness_complete` in `evaluation_registry.csv`.

STEP-047 (DEC0007):
- E8 cross-dataset, `EVAL0001/generalization/`: config, Kaggle notebook and runbook. After the Kaggle run: `predictions/DS000N.csv`, `run_manifest.json`, `cross_dataset_*.csv`, and `cross_dataset_report.md`. MODEL0001 runs unchanged at its frozen threshold on DS0002–DS0005 test (DS0005: fixed 10,000 sample).
- E9 unseen generator, `EVAL0002/`: evaluates EXP0002 / MODEL0008, trained without Stable Diffusion. STEP-041 inputs in `EXP0002/`, the E1–E2 report in `EVAL0002/`, and `EVAL0002/unseen_generator/` from `python -m generalization unseen`. Status `unseen_generator_complete`.
- Figure specs FIG0018–FIG0019.

STEP-048 (DEC0008): `ablations/` will hold `ablation_results.csv` and `ablation_report.md` from `python -m ablation evaluate`, comparing EXP0003–EXP0006 with EXP0001. EVAL0003–EVAL0006 are reserved for their E1–E2 checks; their STEP-041 inputs go to `EXP0003/` … `EXP0006/`. Figure spec FIG0020.

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
