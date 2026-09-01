# Figure Spec: FIG0001

**Purpose:** Show real vs fake class balance for primary training set DS0001 (ArtiFact face subset).  
**Required data:** Counts and proportions of `real` / `fake` for DS0001.  
**Recommended chart type:** Horizontal or vertical bar chart (2 bars).  
**Exact axes:** X = Class (real, fake); Y = Count (images), secondary annotation = Proportion.  
**Legend:** Not required (classes on axis).  
**Caption:** Class distribution of DS0001 (ArtiFact 50k face subset): balanced real/fake split used for primary training.  
**Color recommendations:** Real = slate blue `#3B6D9A`; Fake = rust `#B85C38`; no glow.  
**Data source path:** `03_Datasets/reports/eda_class_distribution.csv` (filter `Dataset ID=DS0001`).  
**Responsible notebook:** `04_Preprocessing/notebooks/STEP023_KAGGLE_EDA.md` / `17_Automation/dataset_eda`.  
**Manual creation instructions:** Plot Count by Class; add text labels for Proportion; title optional (caption carries meaning).  
**Expected output filename:** `09_Figures/assets/FIG0001_v1.png` (human-rendered).
