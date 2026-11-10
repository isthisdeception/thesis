# Figure Spec: FIG0017

**Purpose:** Which generators and real sources lose most under each perturbation (worst level), for MODEL0001 on EXP0001 test.  
**Required data:** `delta_error_rate` for every `group` (non-`small_group`) at each perturbation's `worst_level` (from `robustness_summary.csv`), plus the clean `error_rate`.  
**Recommended chart type:** Heatmap.  
**Exact axes:** X = perturbation at its worst level (config order). Y = group: fake generators (sorted by clean FNR), then real sources. Colour = change in error rate against clean (diverging, centred on 0).  
**Legend:** Colour bar "Δ error rate vs clean" (FNR for generators, FPR for real sources).  
**Caption:** Change in error rate per generator and real source at each perturbation's worst level, EXP0001 test split, threshold 0.395. Clean rates are in FIG0015.  
**Color recommendations:** Diverging `#1F618D` (better) – `#FFFFFF` (0) – `#C0392B` (worse), symmetric limits.  
**Data source path:** `08_Evaluation/EVAL0001/robustness/robustness_by_group.csv`; `08_Evaluation/EVAL0001/robustness/robustness_summary.csv`.  
**Responsible notebook:** `08_Evaluation/EVAL0001/robustness/STEP046_robustness.ipynb` → `python -m robustness analyze`.  
**Manual creation instructions:** Separate generators from real sources with a line. Annotate cells with |Δ| ≥ 0.05. Do not label any cell as a cause.  
**Expected output filename:** `09_Figures/assets/FIG0017_v1.png`
