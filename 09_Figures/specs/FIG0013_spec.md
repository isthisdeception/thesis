# Figure Spec: FIG0013

**Purpose:** Threshold trade-off for MODEL0001 on EXP0001 test, with the val-chosen operating points marked.  
**Required data:** Sweep rows for `split == test` (`threshold`, `fpr`, `fnr`, `balanced_accuracy`, `f1`); operating points for `split == test` (`point`, `threshold`).  
**Recommended chart type:** Line chart of error rates and scores against threshold, with vertical markers.  
**Exact axes:** X = threshold (0–1). Y = rate or score (0–1).  
**Legend:** FPR, FNR, Balanced accuracy, F1; markers: frozen, high_sensitivity, high_specificity.  
**Caption:** Error rates and scores on the EXP0001 test split across thresholds. Markers are thresholds chosen on val and applied to test unchanged.  
**Color recommendations:** FPR `#C0392B`; FNR `#B7950B`; Balanced accuracy `#1F618D`; F1 `#566573`; markers black dashed.  
**Data source path:** `08_Evaluation/EVAL0001/threshold_sweep.csv`; `08_Evaluation/EVAL0001/operating_points.csv`.  
**Responsible notebook:** `17_Automation/calibration_threshold` (`python -m calibration_threshold`).  
**Manual creation instructions:** Draw markers at the exact operating-point thresholds, not the nearest sweep value. Omit `max_f1` and `fixed_0.5` markers unless comparing.  
**Expected output filename:** `09_Figures/assets/FIG0013_v1.png`
