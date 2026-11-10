# Figure Spec: FIG0018

**Purpose:** How MODEL0001's error rates change from its own test set to other datasets (Phase E8).  
**Required data:** Per dataset `fnr` (if it has fake images) and `fpr` (if it has real images) with `error_ci_low`/`error_ci_high` from the dataset table; per-generator rows for the second panel.  
**Recommended chart type:** Panel A: grouped dot plot with 95% intervals, one row per dataset, two markers (FNR, FPR). Panel B: dot plot of FNR per fake generator, coloured by `relation`.  
**Exact axes:** Panel A: Y = dataset (DS0001 reference first), X = error rate (0–1). Panel B: Y = generator grouped by dataset, sorted by FNR; X = FNR (0–1); dashed line at DS0001 FNR.  
**Legend:** FNR (missed fakes), FPR (real flagged as fake); relation: seen, related, unseen.  
**Caption:** MODEL0001 (trained on DS0001) at its frozen threshold 0.395 on DS0001 test and four other datasets. Fake-only datasets have no FPR; real-only datasets have no FNR. DS0005 is a fixed 10,000-image sample.  
**Color recommendations:** FNR `#B7950B`; FPR `#1F618D`; relation seen `#1E8449`, related `#B7950B`, unseen `#C0392B`.  
**Data source path:** `08_Evaluation/EVAL0001/generalization/cross_dataset_metrics.csv`; `08_Evaluation/EVAL0001/generalization/cross_dataset_by_generator.csv`.  
**Responsible notebook:** `08_Evaluation/EVAL0001/generalization/STEP047_cross_dataset.ipynb` → `python -m generalization analyze`.  
**Manual creation instructions:** Show n beside each row. Leave missing rates blank, never zero. Omit `small_group` rows from Panel B.  
**Expected output filename:** `09_Figures/assets/FIG0018_v1.png`
