# Figure Spec: FIG0012

**Purpose:** Confidence distribution and confidence-versus-accuracy for MODEL0001 decisions on EXP0001 test.  
**Required data:** Per-bin `share`, `mean_confidence`, `accuracy` for `split == test`, at the frozen threshold.  
**Recommended chart type:** Bars for share of decisions per confidence bin, with an accuracy line on a second axis.  
**Exact axes:** X = confidence of the predicted class (0.5–1.0, plus one "< 0.5" bar for bin `-1`). Left Y = share of decisions (0–1). Right Y = accuracy (0–1), with mean confidence as a dashed reference.  
**Legend:** Share of decisions, Accuracy, Mean confidence.  
**Caption:** Confidence is max(p, 1 − p) for the predicted class at threshold 0.395. Where accuracy sits below mean confidence, the model is overconfident.  
**Color recommendations:** Bars `#AEB6BF`; accuracy `#1F618D`; mean confidence `#566573` dashed.  
**Data source path:** `08_Evaluation/EVAL0001/confidence_distribution.csv`.  
**Responsible notebook:** `17_Automation/calibration_threshold` (`python -m calibration_threshold`).  
**Manual creation instructions:** Keep bin `-1` visually separate and explain it in the caption (threshold below 0.5). Do not call confidence "probability of being correct".  
**Expected output filename:** `09_Figures/assets/FIG0012_v1.png`
