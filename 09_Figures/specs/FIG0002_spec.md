# Figure Spec: FIG0002

**Purpose:** Generator composition of synthetic images in DS0001 (13 generators + real/`none`).  
**Required data:** Per-generator image counts for DS0001.  
**Recommended chart type:** Horizontal bar chart sorted by count descending.  
**Exact axes:** Y = Generator name; X = Count (images).  
**Legend:** Optional color split by Class (real vs fake).  
**Caption:** Generator distribution in DS0001: real images labeled `none`; synthetic faces span 13 generators at near-equal counts.  
**Color recommendations:** Single ink `#2F4F4F` for fake bars; real/`none` in `#3B6D9A`.  
**Data source path:** `03_Datasets/reports/eda_generator_distribution.csv` (filter `Dataset ID=DS0001`).  
**Responsible notebook:** `04_Preprocessing/notebooks/STEP023_KAGGLE_EDA.md` / `17_Automation/dataset_eda`.  
**Manual creation instructions:** Sort generators by Count; place `none` (real) at top or bottom with distinct color.  
**Expected output filename:** `09_Figures/assets/FIG0002_v1.png`
