# Figure Spec: FIG0023

**Purpose:** Metric comparison of the fairness-compatible runs, with the seed replicate visible as the run-to-run pair.  
**Required data:** `roc_auc`, `balanced_accuracy`, `mcc` from the ranked comparison table.  
**Recommended chart type:** Grouped dots, one panel per metric.  
**Exact axes:** Y = experiment (baseline, then seed replicate, then ablations). X = metric value. ROC-AUC and balanced accuracy on 0.5–1; MCC on 0–1.  
**Legend:** Baseline, seed replicate, ablation.  
**Caption:** SPLIT0001 test metrics for experiments that share DS0001 / v1.0 / PP0001 / SPLIT0001. No bar is marked as a winner. Statistical intervals are in `08_Evaluation/statistics/paired_tests.csv`.  
**Color recommendations:** Baseline `#1F618D`; seed `#117A65`; ablations `#922B21`.  
**Data source path:** `08_Evaluation/comparison_tables.csv`.  
**Responsible notebook:** `python -m comparison`.  
**Manual creation instructions:** Omit EXP0002. Do not plot accuracy alone.  
**Expected output filename:** `09_Figures/assets/FIG0023_v1.png`
