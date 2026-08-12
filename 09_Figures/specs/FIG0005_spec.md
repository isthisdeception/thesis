# Figure Spec: FIG0005

**Purpose:** Synthbuster generator mix plus RAISE real pack for frequency-domain evaluation (DS0004).  
**Required data:** Generator counts for DS0004 (`raise_1k_jpeg` + 9 synthetic generators).  
**Recommended chart type:** Horizontal bar chart.  
**Exact axes:** Y = Generator; X = Count.  
**Legend:** Class (real vs fake) via bar color.  
**Caption:** DS0004 Synthbuster composition: ~1k RAISE JPEG reals and 1k images per synthetic generator.  
**Color recommendations:** Real `#3B6D9A`; Synthetic generators shared `#5D6D7E`.  
**Data source path:** `03_Datasets/reports/eda_generator_distribution.csv` (filter `Dataset ID=DS0004`).  
**Responsible notebook:** `04_Preprocessing/notebooks/STEP023_KAGGLE_EDA.md` / `17_Automation/dataset_eda`.  
**Manual creation instructions:** Separate real bar visually; keep generator names as published (e.g. `stable-diffusion-xl`).  
**Expected output filename:** `09_Figures/assets/FIG0005_v1.png`
