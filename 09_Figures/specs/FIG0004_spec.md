# Figure Spec: FIG0004

**Purpose:** Class balance for quick-baseline DS0003 (140k real-and-fake faces).  
**Required data:** `real` / `fake` counts for DS0003.  
**Recommended chart type:** Bar chart.  
**Exact axes:** X = Class; Y = Count.  
**Legend:** None.  
**Caption:** DS0003 class distribution (StyleGAN fakes vs real faces) used for rapid baseline training on Kaggle.  
**Color recommendations:** Real `#3B6D9A`; Fake `#B85C38`.  
**Data source path:** `03_Datasets/reports/eda_class_distribution.csv` (filter `Dataset ID=DS0003`).  
**Responsible notebook:** `04_Preprocessing/notebooks/STEP023_KAGGLE_EDA.md` / `17_Automation/dataset_eda`.  
**Manual creation instructions:** Two bars with count labels; note 256×256 resolution in caption footnote if needed.  
**Expected output filename:** `09_Figures/assets/FIG0004_v1.png`
