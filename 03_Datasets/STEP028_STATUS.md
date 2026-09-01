# STEP-028 — Train/Validation/Test Split

**Status:** COMPLETE (2026-09-01)  
**Handbook:** Phase D12 (leakage-critical)  
**Guide:** `notebooks/STEP028_KAGGLE_SPLIT.md`

## Done
- [x] `17_Automation/dataset_split/` module (grouped_random, logo, official_holdout)
- [x] Leakage assertions (identity / generator / hash)
- [x] 10 splits across 5 processed outputs (standard + LOGO each)
- [x] `03_Datasets/splits/DSxxxx_PPxxxx_SPLITxxxx/` index files
- [x] `03_Datasets/reports/split_report.md`
- [x] `03_Datasets/metadata/split_registry.csv`
- [x] Unit tests (`17_Automation/tests/test_dataset_split.py`)

## Primary splits for training
| Dataset | Standard split | LOGO split (E9) |
|---------|----------------|-----------------|
| DS0001 | `DS0001_PP0001_SPLIT0001` | `DS0001_PP0001_SPLIT0002` (hold `stable_diffusion`) |
| DS0002 | `DS0002_PP0002_SPLIT0001` | `DS0002_PP0002_SPLIT0002` (hold `Midjourney`) |
| DS0003 | `DS0003_PP0003_SPLIT0001` (native valid→test) | `DS0003_PP0003_SPLIT0002` (hold `stylegan`) |
| DS0004 | `DS0004_PP0006_SPLIT0001` | `DS0004_PP0006_SPLIT0002` (hold `dalle3`) |
| DS0005 | `DS0005_PP0005_SPLIT0001` (native val→test) | `DS0005_PP0005_SPLIT0002` |

## Next step
**STEP-029** — FastAI prep, dataset versioning, master registry + Preprocessing Gate (Checklist 4).
