# Figure Spec: FIG0011

**Purpose:** Reliability diagram for MODEL0001 on EXP0001 test: does P(fake) match the observed fake share?  
**Required data:** Per-bin `mean_confidence` (mean P(fake)), `fraction_positive`, `count`, for `split == test`; ECE and MCE from the summary.  
**Recommended chart type:** Reliability curve with the diagonal, plus a count histogram underneath.  
**Exact axes:** Panel A: X = mean P(fake) in bin (0–1), Y = fraction fake in bin (0–1), equal aspect, dashed diagonal y = x. Panel B: X = same bins, Y = image count (log scale allowed).  
**Legend:** Test, Perfect calibration. Optional second curve: Val.  
**Caption:** Reliability of MODEL0001 P(fake) on the EXP0001 test split, 15 equal-width bins. ECE and MCE in the caption come from `calibration_summary.csv`.  
**Color recommendations:** Test `#1F618D`; Val `#B7950B`; diagonal `#566573` dashed.  
**Data source path:** `08_Evaluation/EVAL0001/reliability.csv`; `08_Evaluation/EVAL0001/calibration_summary.csv`.  
**Responsible notebook:** `17_Automation/calibration_threshold` (`python -m calibration_threshold`).  
**Manual creation instructions:** Skip empty bins (`count == 0`). Plot points at bin means, not bin centres. Label axes "P(fake)", not "confidence".  
**Expected output filename:** `09_Figures/assets/FIG0011_v1.png`
