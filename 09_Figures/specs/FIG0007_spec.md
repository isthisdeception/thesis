# Figure Spec: FIG0007

**Purpose:** Compare resolution diversity across registered datasets.  
**Required data:** Width×Height histograms (or dominant resolutions) per dataset from EDA pixel sample.  
**Recommended chart type:** Faceted bar charts (one panel per Dataset ID) or heatmap of resolution bins.  
**Exact axes:** X = Resolution label `W×H`; Y = Count (sample); Panel = Dataset ID.  
**Legend:** Dataset ID if overlaid; else panel titles.  
**Caption:** Image resolution distributions from STEP-023 EDA pixel samples; DS0001/DS0003/DS0005 are fixed-size while DS0002/DS0004 vary.  
**Color recommendations:** Neutral single hue per panel `#34495E`.  
**Data source path:** `03_Datasets/reports/eda_resolution_distribution.csv`.  
**Responsible notebook:** `04_Preprocessing/notebooks/STEP023_KAGGLE_EDA.md` / `17_Automation/dataset_eda`.  
**Manual creation instructions:** Show top-k resolutions per dataset; note Sample Policy from Notes column.  
**Expected output filename:** `09_Figures/assets/FIG0007_v1.png`
