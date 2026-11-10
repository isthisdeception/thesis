# Figure Spec: FIG0016

**Purpose:** Robustness curves for MODEL0001 on EXP0001 test: how balanced accuracy and ROC-AUC change as each perturbation gets stronger.  
**Required data:** Per condition `perturbation`, `rank` (0 = clean, 1 = mildest), `level`, `balanced_accuracy`, `roc_auc`; clean row repeated as rank 0 of every perturbation; `tolerance` from the config.  
**Recommended chart type:** Small multiples, one panel per perturbation, two lines per panel.  
**Exact axes:** X = level (categorical, mild → strong, clean first, tick labels from `level`). Y = metric (0.5–1.0). Shaded band: clean balanced accuracy ± tolerance.  
**Legend:** Balanced accuracy, ROC-AUC, Tolerance band.  
**Caption:** Balanced accuracy (frozen threshold 0.395) and ROC-AUC of MODEL0001 under graded perturbations of the EXP0001 test split (n = 7505 per condition). Where ROC-AUC holds while balanced accuracy falls, the probabilities shifted rather than the ranking.  
**Color recommendations:** Balanced accuracy `#1F618D`; ROC-AUC `#B7950B`; band `#D5DBDB`.  
**Data source path:** `08_Evaluation/EVAL0001/robustness/robustness_metrics.csv`; tolerance in `08_Evaluation/EVAL0001/robustness/config.yaml`.  
**Responsible notebook:** `08_Evaluation/EVAL0001/robustness/STEP046_robustness.ipynb` → `python -m robustness analyze`.  
**Manual creation instructions:** Same Y range in every panel. Order panels as in the config. Do not connect levels of different perturbations.  
**Expected output filename:** `09_Figures/assets/FIG0016_v1.png`
