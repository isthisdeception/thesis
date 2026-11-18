# Figure Spec: FIG0022

**Purpose:** Precision-recall curves on the SPLIT0001 test split for the same runs as FIG0021.  
**Required data:** `precision`, `recall` where `split == test`. The chance level is the fake share in that split.  
**Recommended chart type:** Line chart, one curve per experiment, plus a horizontal chance line.  
**Exact axes:** X = recall (0–1). Y = precision (0–1).  
**Legend:** Same experiments as FIG0021, plus the test fake share.  
**Caption:** Test precision-recall curves for EXP0001 and the one-factor runs. Chance is the fake share of the SPLIT0001 test split, not 0.5.  
**Color recommendations:** Same series colors as FIG0021. Chance line `#566573` dashed.  
**Data source path:** `08_Evaluation/EXP0001/pr_curve.csv` and the same filename under `EXP0003` … `EXP0006`.  
**Responsible notebook:** `python -m evaluation_trigger`.  
**Manual creation instructions:** Filter `split == test`. State the fake share in the caption.  
**Expected output filename:** `09_Figures/assets/FIG0022_v1.png`
