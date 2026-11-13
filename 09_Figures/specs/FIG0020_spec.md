# Figure Spec: FIG0020

**Purpose:** Ablation chart (Phase E10): how each one-factor change moves the test metrics of the ResNet-50 baseline, against the seed-to-seed variation.  
**Required data:** Per experiment `delta_roc_auc`, `delta_balanced_accuracy`, `delta_mcc`, `delta_ece` and the matching `beyond_seed_*` flags; the seed replicate's absolute deltas give the noise band.  
**Recommended chart type:** Horizontal dot plot, one panel per metric (small multiples), one row per ablation.  
**Exact axes:** Y = ablation (factor name, EXP ID in brackets), seed replicate first. X = change against EXP0001 (metric units; ECE: lower is better, so invert the axis or note it). Shaded band: ± |seed replicate delta| for that metric. Vertical line at 0.  
**Legend:** Beyond seed noise (filled), within seed noise (hollow), noise band.  
**Caption:** One-factor ablations of the EXP0001 ResNet-50 baseline on the SPLIT0001 test split, each at its own val-chosen threshold. The band shows the change caused by the training seed alone (EXP0003). Single runs; paired tests are in `08_Evaluation/statistics/statistics_report.md` and do not support a superiority claim.  
**Color recommendations:** dots `#1F618D`; band `#D5DBDB`; zero line `#566573`.  
**Data source path:** `08_Evaluation/ablations/ablation_results.csv`.  
**Responsible notebook:** `06_Experiments/ablations/STEP048_ablations.ipynb` (training) → `python -m ablation evaluate`.  
**Manual creation instructions:** Same X range within a panel. Label the no-pretraining row as "same epoch budget, untuned".  
**Expected output filename:** `09_Figures/assets/FIG0020_v1.png`
