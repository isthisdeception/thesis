# Figure Spec: FIG0006

**Purpose:** FairFace demographic race distribution for bias evaluation (DS0005).  
**Required data:** Race level counts by split (train/val) for DS0005.  
**Recommended chart type:** Grouped bar chart (race × split) or faceted bars.  
**Exact axes:** X = Race; Y = Count; Legend/facet = Split.  
**Legend:** train, val.  
**Caption:** DS0005 FairFace race distribution (padding 0.25) used for demographic fairness checks of the forensic analyst.  
**Color recommendations:** train `#2E4057`; val `#048A81`.  
**Data source path:** `03_Datasets/reports/eda_demographic_distribution.csv` (filter `Dataset ID=DS0005`, `Attribute=race`).  
**Responsible notebook:** `04_Preprocessing/notebooks/STEP023_KAGGLE_EDA.md` / `17_Automation/dataset_eda`.  
**Manual creation instructions:** Sort races alphabetically; optionally add companion panels for gender (FIG0006b not required).  
**Expected output filename:** `09_Figures/assets/FIG0006_v1.png`
