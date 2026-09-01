# Figure Spec: FIG0008

**Purpose:** Compare brightness (mean luma) across datasets for preprocessing decisions.  
**Required data:** Overall brightness Mean/P05/P50/P95 per Dataset ID (`Stratum=ALL`).  
**Recommended chart type:** Box-like interval plot or error-bar chart (P05–P95 whiskers, P50 marker, Mean marker).  
**Exact axes:** X = Dataset ID; Y = Brightness (luma, unitless [0,1]).  
**Legend:** Mean vs median markers.  
**Caption:** Per-dataset brightness summary from stratified EDA pixel samples (thumbnail ≤256 px).  
**Color recommendations:** Interval `#7F8C8D`; mean `#C0392B`; median `#2980B9`.  
**Data source path:** `03_Datasets/reports/eda_brightness_stats.csv` (filter `Stratum=ALL`).  
**Responsible notebook:** `04_Preprocessing/notebooks/STEP023_KAGGLE_EDA.md` / `17_Automation/dataset_eda`.  
**Manual creation instructions:** One interval per dataset; state N and sample policy in caption.  
**Expected output filename:** `09_Figures/assets/FIG0008_v1.png`
