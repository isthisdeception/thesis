# Figure Spec: FIG0014

**Purpose:** Confusion matrix for MODEL0001 on EXP0001 test at the frozen threshold.  
**Required data:** `count` and `share_of_true` for `split == test`, all four `true_label` × `predicted_label` cells.  
**Recommended chart type:** 2 × 2 heatmap, coloured by `share_of_true`, annotated with count and percentage.  
**Exact axes:** X = predicted label (fake, real). Y = true label (fake, real), same order. Colour scale 0–1.  
**Legend:** Colour bar "Share of true class".  
**Caption:** Confusion matrix of MODEL0001 on the EXP0001 test split (n = 7505) at threshold 0.395, chosen on val. Cells show count and share of the true class.  
**Color recommendations:** Sequential single hue, white `#FFFFFF` to `#1F618D`; annotation text switches to white above 0.5.  
**Data source path:** `08_Evaluation/EVAL0001/confusion_matrix.csv`.  
**Responsible notebook:** `17_Automation/failure_analysis` (`python -m failure_analysis`).  
**Manual creation instructions:** Keep fake first on both axes so the diagonal is correct decisions. Row shares, not overall shares.  
**Expected output filename:** `09_Figures/assets/FIG0014_v1.png`
