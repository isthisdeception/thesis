# Figure Spec: FIG0003

**Purpose:** DiFF official-test generator × condition structure for primary evaluation (DS0002).  
**Required data:** Counts by Generator and Condition (FE/FS/I2I/T2I) for DS0002.  
**Recommended chart type:** Grouped or stacked bar chart (conditions as hue/stack).  
**Exact axes:** X = Generator; Y = Count; Legend = Condition.  
**Legend:** FE, FS, I2I, T2I.  
**Caption:** DS0002 DiFF official TEST composition across 13 generators and four synthesis conditions (all synthetic; pristine excluded).  
**Color recommendations:** FE `#1B4F72`, FS `#148F77`, I2I `#B9770E`, T2I `#6C3483` (muted, print-safe).  
**Data source path:** `03_Datasets/reports/eda_generator_distribution.csv` (filter `Dataset ID=DS0002`).  
**Responsible notebook:** `04_Preprocessing/notebooks/STEP023_KAGGLE_EDA.md` / `17_Automation/dataset_eda`.  
**Manual creation instructions:** Facet or stack by Condition; annotate total N from `eda_balance_summary.csv`.  
**Expected output filename:** `09_Figures/assets/FIG0003_v1.png`
