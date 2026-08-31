# STEP-027 — Register Pipeline & Generate Processed Dataset

**Status:** COMPLETE (2026-09-01)  
**Handbook:** Phase D10–D11  
**Guide:** `notebooks/STEP027_KAGGLE_PREPROCESS.md`

## Done
- [x] `PP0001`–`PP0005` + `PP0006` (DS0004 fix) in `preprocessing_registry.csv`
- [x] DS0002 exclude list: `exclude_lists/exclude_list_DS0002.csv` (1593 `CORRUPT_IMAGE`)
- [x] Kaggle runner: `step027_run_preprocessing.py` + report writer
- [x] Full runs on Kaggle for PP0001–PP0003, PP0005; PP0006 for DS0004
- [x] Reports + metadata synced to `04_Preprocessing/reports/`
- [x] Processed datasets uploaded to Kaggle (pointers in `03_Datasets/metadata/dataset_pointers.md`)

## Kaggle processed datasets
| Output | Slug |
|--------|------|
| DS0001_PP0001 | `isthisdeception/ds0001-pp0001` |
| DS0002_PP0002 | `isthisdeception/ds0002-pp0002` |
| DS0003_PP0003 | `isthisdeception/ds0003-pp0003` |
| DS0004_PP0006 | `isthisdeception/ds0004-pp0006` |
| DS0005_PP0005 | `isthisdeception/ds0005-pp0005` |

## Notes
- PP0004 superseded by PP0006 (RAISE `max_side` fix).
- DS0002 upload required ASCII filename sanitization (42 Unicode paths).
- `Ready=no` until STEP-029 (Checklist 4 gate).

## Next step
**STEP-028** — Train/validation/test split (leakage-safe).
