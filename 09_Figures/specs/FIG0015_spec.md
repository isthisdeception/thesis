# Figure Spec: FIG0015

**Purpose:** Where MODEL0001 fails on EXP0001 test: FNR per fake generator and FPR per real source.  
**Required data:** `group`, `group_type`, `error_rate`, `ci_low`, `ci_high`, `n` for `split == test` and `small_group == False`; overall FNR and FPR from `per_class_stats.csv`.  
**Recommended chart type:** Horizontal dot plot with 95% interval bars, two panels.  
**Exact axes:** Panel A: Y = generator, sorted by error rate; X = FNR (0–1). Panel B: Y = real source; X = FPR (0–1). Dashed vertical line at the overall rate in each panel.  
**Legend:** Error rate, Wilson 95% interval, Overall rate.  
**Caption:** Error rates by generator (false negatives) and real source (false positives) on the EXP0001 test split at threshold 0.395. Intervals are per group, not corrected for multiple comparisons.  
**Color recommendations:** Generators `#B7950B`; real sources `#1F618D`; overall line `#566573` dashed.  
**Data source path:** `08_Evaluation/EVAL0001/error_by_group.csv`; `08_Evaluation/EVAL0001/per_class_stats.csv`.  
**Responsible notebook:** `17_Automation/failure_analysis` (`python -m failure_analysis`).  
**Manual creation instructions:** Show n next to each label. Do not label any group a "cause"; the figure shows where errors occur.  
**Expected output filename:** `09_Figures/assets/FIG0015_v1.png`
