# STEP-027 — Register Pipeline & Generate Processed Dataset

**Status:** REGISTERED — **awaiting Kaggle execution** (2026-08-12)  
**Handbook:** Phase D10–D11  
**Guide:** `notebooks/STEP027_KAGGLE_PREPROCESS.md`

## Done in Git
- [x] `PP0001`–`PP0005` rows in `preprocessing_registry.csv` (full parameters)
- [x] DS0002 exclude list: `exclude_lists/exclude_list_DS0002.csv` (1593 `CORRUPT_IMAGE`)
- [x] Kaggle runner: `step027_run_preprocessing.py` + report writer
- [x] Template-6 report stubs: `reports/PP0001_report.md` … `PP0005_report.md`
- [x] Processed pointers section (PENDING slugs) in `03_Datasets/metadata/dataset_pointers.md`

## Pending (human / Kaggle)
- [ ] Run smoke (`PP0003`, `MAX_IMAGES=50`) then full PP0001–PP0005
- [ ] Upload each `processed/DSxxxx_PPxxxx` as a Kaggle Dataset
- [ ] Download `git_sync/reports` + metadata → replace report stubs
- [ ] Reply with Kaggle slugs → finalize pointers + set registry `Status=complete`

## Policy
- Never overwrite processed outputs; new params ⇒ new `PPxxxx`
- Raw read-only; no processed image bytes in Git
