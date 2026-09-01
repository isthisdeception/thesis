# Figure Spec: FIG0009

**Purpose:** Compare contrast (luma std) across datasets to flag low/high-contrast packs.  
**Required data:** Overall contrast Mean/P05/P50/P95 per Dataset ID (`Stratum=ALL`).  
**Recommended chart type:** Interval / error-bar chart.  
**Exact axes:** X = Dataset ID; Y = Contrast (luma std, [0,1]).  
**Legend:** Mean vs median.  
**Caption:** Per-dataset contrast summary from stratified EDA pixel samples.  
**Color recommendations:** Interval `#7F8C8D`; mean `#AF601A`; median `#1A5276`.  
**Data source path:** `03_Datasets/reports/eda_contrast_stats.csv` (filter `Stratum=ALL`).  
**Responsible notebook:** `04_Preprocessing/notebooks/STEP023_KAGGLE_EDA.md` / `17_Automation/dataset_eda`.  
**Manual creation instructions:** Match FIG0008 layout for easy cross-reading.  
**Expected output filename:** `09_Figures/assets/FIG0009_v1.png`
