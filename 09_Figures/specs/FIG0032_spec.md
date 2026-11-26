# Figure Spec: FIG0032

**Purpose:** Exhaustive 42-panel (`6 x 7`) visual reference atlas displaying one deterministic preprocessed sample (`224 x 224` px) from every evaluated authentic source and synthetic generator across all five public benchmark corpora (`DS0001`–`DS0005`).  
**Required data:** Forty-two verified `224 x 224` PNG assets from `_processed_dataset/` (`16` ArtiFact subgroups, `12` DiFF unseen diffusion generators, `2` 140k Faces subgroups, `10` Synthbuster subgroups, and `2` FairFace true-negative/false-positive authentic portraits).  
**Recommended chart type:** Six-row by seven-column (`6 x 7`) image grid with numbered `(1)`–`(42)` subgroup headers and class-coded borders.  
**Exact axes:** Ticks hidden; colorblind-safe frame (`#3B6D9A` Real, `#B85C38` Fake).  
**Caption:** Exhaustive 42-panel visual atlas covering all evaluated authentic sources and synthetic generators `(1)` through `(42)` across `DS0001`–`DS0005`.  
**Data source path:** `_processed_dataset/processed_DS0001_PP0001` through `processed_DS0005_PP0005` (`SPLIT0001` test partitions).  
**Responsible notebook:** `09_Figures/scripts/render_figures.py` (`--only FIG0032`).  
**Expected output filename:** `09_Figures/assets/FIG0032_v1.png` and `09_Figures/assets/FIG0032_v1.pdf`
