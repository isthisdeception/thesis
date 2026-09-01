# Preprocessing Quality Audit — Checklist 4

> **Audit Type:** Quality Gate — Preprocessing (Checklist 4)  
> **Audit Date:** 2026-09-01  
> **Auditor:** Preprocessing Agent / Dataset Auditor Agent  
> **Handbook Reference:** §13.2 / Checklist 4; Phases D9–D11, D13; STEP-025–029  
> **Overall result:** **PASS** (human-confirmed 2026-09-01)

---

## Summary

All active preprocessing pipelines are registered, parameterized, reported, and versioned. Raw datasets were not modified. Processed outputs live on Kaggle (data tier) with Git holding configs, reports, and `index.csv`. FastAI normalization/size parameters are stored as config (`apply_on_disk=false`). Dataset version **v1.0** is assigned in `dataset_versions.csv`.

Checklist 4 items: pipeline registered, parameters recorded, outputs documented, version assigned, raw untouched, processed reproducible, config stored.

---

## Passed Items

### 1. Pipeline registered

| Item | Status | Evidence |
|------|--------|----------|
| PP IDs in registry | ✅ PASS | `04_Preprocessing/preprocessing_registry.csv` |
| Active complete pipelines | ✅ PASS | PP0001 (DS0001), PP0002 (DS0002), PP0003 (DS0003), PP0005 (DS0005), PP0006 (DS0004) |
| Retired pipeline not used for splits | ✅ PASS | PP0004 `superseded_by_PP0006` (RAISE `max_side` fix) |
| Module sequence recorded | ✅ PASS | `PPMOD01>PPMOD10>PPMOD08>PPMOD07>PPMOD09>PPMOD05>PPMOD06` |

### 2. Parameters recorded

| Item | Status | Evidence |
|------|--------|----------|
| Registry JSON parameters | ✅ PASS | `preprocessing_registry.csv` `Parameters` column |
| Per-run dump | ✅ PASS | `04_Preprocessing/reports/PPxxxx_report.md` + `reports/metadata/*/pipeline.json` |
| Design catalog | ✅ PASS | `04_Preprocessing/design/parameters_catalog.md` |
| Shared defaults | ✅ PASS | `target_size=224`, `norm_mode=imagenet`, `apply_on_disk=false`, `random_seed=42`, face modules off |

### 3. Outputs documented

| Output | Kept | Kaggle slug | Report |
|--------|-----:|-------------|--------|
| DS0001_PP0001 | 50000 | `isthisdeception/ds0001-pp0001` | `reports/PP0001_report.md` |
| DS0002_PP0002 | 51452 | `isthisdeception/ds0002-pp0002` | `reports/PP0002_report.md` |
| DS0003_PP0003 | 140000 | `isthisdeception/ds0003-pp0003` | `reports/PP0003_report.md` |
| DS0004_PP0006 | 9999 | `isthisdeception/ds0004-pp0006` | `reports/PP0006_report.md` |
| DS0005_PP0005 | 97698 | `isthisdeception/ds0005-pp0005` | `reports/PP0005_report.md` |

Pointers: `03_Datasets/metadata/dataset_pointers.md`.  
Git holds `index.csv`, `normalization_stats.json`, `pipeline.json` under `04_Preprocessing/reports/metadata/` — **not** image bytes.

### 4. Version assigned

| Item | Status | Evidence |
|------|--------|----------|
| Pipeline version | ✅ PASS | Registry `Version=1.0` per PP |
| Dataset version v1.0 | ✅ PASS | `03_Datasets/metadata/dataset_versions.csv` |
| Master links DS→PP | ✅ PASS | `dataset_registry.csv` |

### 5. Raw untouched

| Item | Status | Evidence |
|------|--------|----------|
| Raw lock honored | ✅ PASS | PP reports: “Raw data was read-only”; writes only under `processed/DSxxxx_PPxxxx` |
| DS0002 exclusions at PP only | ✅ PASS | `exclude_lists/exclude_list_DS0002.csv` + runtime `exclude_applied.csv`; raw unchanged |
| Never overwrite processed | ✅ PASS | DS0004 fix = new PP0006 (PP0004 retained as superseded) |

### 6. Processed reproducible

| Item | Status | Evidence |
|------|--------|----------|
| Seeded pipeline | ✅ PASS | `random_seed=42` in every complete PP |
| Index checksums | ✅ PASS | SHA-256 of `metadata/index.csv` in each `PPxxxx_report.md` |
| Split fingerprints | ✅ PASS | `split_config.json` `fingerprint_sha256`; unit tests `17_Automation/tests/test_dataset_split.py` |
| Modules + tests | ✅ PASS | STEP-026 `04_Preprocessing/modules/` (34 unit tests) |

### 7. Config stored (FastAI-ready)

| Item | Status | Evidence |
|------|--------|----------|
| PP config JSON | ✅ PASS | `reports/metadata/*/pipeline.json` |
| Normalization stats | ✅ PASS | ImageNet mean/std; `apply_on_disk=false` |
| FastAI DataBlock parameters | ✅ PASS | `05_Models/config/fastai_dataset.yaml` (not hidden in notebooks) |
| Image size / batch / augs | ✅ PASS | Spec `04_Preprocessing/specs/FASTAI_DATABLOCK_SPEC.md` |

---

## Failed Items

| Item | Status | Notes |
|------|--------|-------|
| — | none | No Checklist 4 failures |

---

## Known (non-failing) notes

| Item | Severity | Notes |
|------|----------|-------|
| DS0002 exclude-list vs run counts | Amber | STEP-022 exclude list = 1593 `CORRUPT_IMAGE`; PP0002 report excluded **5608** (5607 `EXCLUDED_CORRUPT` + 1 `UNREADABLE`). Extra failures were recorded at PP time (`exclude_applied.csv`). Raw untouched; processed count **51452** is the v1.0 dataset. |
| PP0004 | Info | Superseded; not in `dataset_registry.csv`; do not train on `DS0004_PP0004`. |

---

## Evidence

| Artifact | Path |
|----------|------|
| Registry | `04_Preprocessing/preprocessing_registry.csv` |
| Reports | `04_Preprocessing/reports/PP0001_report.md` … `PP0006_report.md` |
| Metadata | `04_Preprocessing/reports/metadata/DS000*_PP000*/` |
| Exclude list | `04_Preprocessing/exclude_lists/exclude_list_DS0002.csv` |
| Design | `04_Preprocessing/design/PREPROCESSING_PIPELINE_DESIGN.md` |
| FastAI config | `05_Models/config/fastai_dataset.yaml` |
| Dataset versions | `03_Datasets/metadata/dataset_versions.csv` |

---

## Recommendations

1. Human **[H]** confirmation recorded 2026-09-01 (Checklists 3 and 4 PASS).
2. Keep DS0002 amber on the dashboard until training docs explicitly use the 51,452 filtered set.
3. Any PP parameter change ⇒ new `PPxxxx` + new dataset version (not an edit of v1.0).

---

## Approval Status

| Role | Status | Date |
|------|--------|------|
| Preprocessing / Dataset Auditor Agent | Checklist 4 **PASS** recommended | 2026-09-01 |
| Human (Checklist 3 + 4 confirm) | **CONFIRMED** | 2026-09-01 |

**Gate decision:** ✅ **PASS** — preprocessing is registered, parameterized, reproducible, and FastAI-config-ready.
