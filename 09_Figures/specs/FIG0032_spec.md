# Figure Spec: FIG0032

**Purpose:** Criterion-selected ten-panel (`2 x 5`) forensic error-mode contrast pairing lowest-error baseline cases `(a)`–`(e)` against highest-error cross-generator and demographic failure cases `(f)`–`(j)` across `DS0001`–`DS0005`.  
**Required data:** Ten newly selected `224 x 224` lossless PNG assets from `_processed_dataset/` distinct from `FIG0031`, contrasting low-error vs. high-error subgroups across ArtiFact, DiFF, 140k Faces, Synthbuster, and FairFace.  
**Recommended chart type:** Two-row by five-column (`2 x 5`) diagnostic image grid with dataset column headers and `(a)`–`(j)` error-rate sublabels.  
**Exact axes:** Ticks hidden; colorblind-safe frame (`#3B6D9A` Real, `#B85C38` Fake).  
**Caption:** Criterion-selected lowest-error `(a)`–`(e)` versus highest-error `(f)`–`(j)` diagnostic samples (`224 x 224` px) across `DS0001`–`DS0005`.  
**Data source path:** `_processed_dataset/processed_DS0001_PP0001` through `processed_DS0005_PP0005`.  
**Responsible notebook:** `09_Figures/scripts/render_figures.py` (`--only FIG0032`).  
**Expected output filename:** `09_Figures/assets/FIG0032_v1.png` and `09_Figures/assets/FIG0032_v1.pdf`
