# Figure Spec: FIG0025

**Purpose:** Training and validation loss across the same completed EXP0001 session as FIG0024.  
**Required data:** `epoch`, `train_loss`, `valid_loss` for that session.  
**Recommended chart type:** Two lines on one set of axes.  
**Exact axes:** X = epoch (integer). Y = loss (the logged values, unscaled).  
**Legend:** Train loss, validation loss.  
**Caption:** Train and validation loss for the completed EXP0001 session. The best epoch is chosen by validation ROC-AUC, not by the lowest validation loss.  
**Color recommendations:** Train `#5D6D7E`; validation `#1F618D`.  
**Data source path:** `06_Experiments/EXP0001/logs/EXP0001_epochs.csv`; session id from `06_Experiments/EXP0001/metrics/run_summary.json`.  
**Responsible notebook:** The EXP0001 training log.  
**Manual creation instructions:** Same session filter as FIG0024. Do not add the abandoned sessions.  
**Expected output filename:** `09_Figures/assets/FIG0025_v1.png`
