# Figure Spec: FIG0024

**Purpose:** Validation ROC-AUC across the completed EXP0001 training session.  
**Required data:** `epoch` and `roc_auc_score` for the session listed in `metrics/run_summary.json`.  
**Recommended chart type:** Line chart. Mark the best epoch from `run_summary.json`.  
**Exact axes:** X = epoch (integer). Y = validation ROC-AUC (0.5–1).  
**Legend:** Validation ROC-AUC, best epoch.  
**Caption:** Validation ROC-AUC during the completed EXP0001 session. Earlier sessions in the same log file are abandoned runs and are not plotted.  
**Color recommendations:** Line `#1F618D`; best-epoch marker `#922B21`.  
**Data source path:** `06_Experiments/EXP0001/logs/EXP0001_epochs.csv`; session id from `06_Experiments/EXP0001/metrics/run_summary.json`.  
**Responsible notebook:** The EXP0001 training log. This spec does not refit the model.  
**Manual creation instructions:** Keep only `sessions[0]` from `run_summary.json`.  
**Expected output filename:** `09_Figures/assets/FIG0024_v1.png`
