# Figure Spec: FIG0010

**Purpose:** File-format / compression footprint overview (JPEG vs PNG sizes).  
**Required data:** Format counts and mean/median bytes per dataset.  
**Recommended chart type:** Grouped bars (Format × Dataset) for counts; optional twin panel for Median Bytes.  
**Exact axes:** Panel A: X = Dataset ID, Y = Count, Legend = Format; Panel B: X = Dataset ID, Y = Median Bytes, Legend = Format.  
**Legend:** JPEG, PNG, other.  
**Caption:** Compression and container formats observed in STEP-023 EDA pixel samples.  
**Color recommendations:** JPEG `#B7950B`; PNG `#1F618D`; other `#566573`.  
**Data source path:** `03_Datasets/reports/eda_compression_stats.csv`.  
**Responsible notebook:** `04_Preprocessing/notebooks/STEP023_KAGGLE_EDA.md` / `17_Automation/dataset_eda`.  
**Manual creation instructions:** Keep byte axis in KB if values are large; note sample policy.  
**Expected output filename:** `09_Figures/assets/FIG0010_v1.png`
