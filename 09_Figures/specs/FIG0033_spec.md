# Figure Spec: FIG0033

**Purpose:** Quantify end-to-end `M1`–`M18` silent error suppression comparing standalone binary detectors, single-specialist governance (`K = 1`), and cross-paradigm multi-specialist fusion (`K = 3`: ResNet-50 + EfficientNet-B4 + ViT-B/16) across 2,700 cases (9 tracks), alongside selective risk-coverage trajectories.  
**Required data:** `08_Evaluation/EVAL0008/abstention_by_track.csv` and `08_Evaluation/EVAL0008/selective_risk_coverage.csv`.  
**Recommended chart type:** Two-panel composite `(a)` grouped bar chart across 9 clean, degraded, and cross-dataset tracks (`n = 2,700`) and `(b)` selective risk-coverage line plot (`n = 1,500`).  
**Exact axes:** Panel `(a)` X = 9 benchmark tracks, Y = Percentage of cases (`0`–`108%`); Panel `(b)` X = Coverage (`%`), Y = Selective error rate on decided cases (`%`).  
**Caption:** End-to-end `M1`–`M18` governance across 2,700 cases comparing `(a)` standalone, single-specialist (`K = 1`), and multi-specialist (`K = 3`) erroneous verdict rates and `(b)` selective risk-coverage trajectories.  
**Data source path:** `08_Evaluation/EVAL0008/abstention_by_track.csv` and `08_Evaluation/EVAL0008/selective_risk_coverage.csv`.  
**Responsible notebook:** `09_Figures/scripts/render_figures.py` (`--only FIG0033`).  
**Expected output filename:** `09_Figures/assets/FIG0033_v1.png` and `09_Figures/assets/FIG0033_v1.pdf`
