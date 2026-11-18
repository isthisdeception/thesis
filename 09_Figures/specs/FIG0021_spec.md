# Figure Spec: FIG0021

**Purpose:** ROC curves on the SPLIT0001 test split for the fairness-compatible runs.  
**Required data:** `fpr`, `tpr` where `split == test`, one curve per experiment.  
**Recommended chart type:** Line chart, one curve per experiment, plus the diagonal.  
**Exact axes:** X = false positive rate (0–1). Y = true positive rate (0–1). Equal aspect.  
**Legend:** EXP0001 baseline, EXP0003 seed, EXP0004 augmentation off, EXP0005 no pretraining, EXP0006 image size 160, chance.  
**Caption:** Test ROC curves for EXP0001 and the one-factor runs on the same split. Intervals and the decision to make no superiority claim are in the STEP-049 statistics report.  
**Color recommendations:** EXP0001 `#1F618D`; other runs `#117A65`, `#B9770E`, `#922B21`, `#5D6D7E`; diagonal `#566573` dashed.  
**Data source path:** `08_Evaluation/EXP0001/roc_curve.csv` and the same filename under `EXP0003` … `EXP0006`.  
**Responsible notebook:** `python -m evaluation_trigger` wrote the curves; this spec does not recompute them.  
**Manual creation instructions:** Filter `split == test`. Do not draw a marker for a winning model.  
**Expected output filename:** `09_Figures/assets/FIG0021_v1.png`
