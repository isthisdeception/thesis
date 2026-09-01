# STEP-023 / Phase D7 — Exploratory Dataset Analysis Module Spec

**Module path:** `17_Automation/dataset_eda/`  
**Reads:** raw dataset roots / ZIP archives **read-only** (reuses `dataset_validation.adapters`)  
**Writes:** EDA CSVs under `03_Datasets/reports/` (+ optional `reports/step023/`)  
**Figures:** specs only in `09_Figures/specs/` (A.9 — never render publication figures)

## Analyses (Phase D7)

| Analysis | Output CSV | Notes |
|----------|------------|-------|
| Class distribution | `eda_class_distribution.csv` | real/fake (or real-only for DS0005) |
| Generator distribution | `eda_generator_distribution.csv` | path or metadata; `none` for real |
| Identity distribution | `eda_identity_distribution.csv` | summary + optional top identities; `unavailable` when unknown |
| Resolution | `eda_resolution_distribution.csv` | width×height histogram |
| Brightness | `eda_brightness_stats.csv` | mean luma; population or stratified sample |
| Contrast | `eda_contrast_stats.csv` | per-image pixel std; population or sample |
| Color channels | `eda_channel_stats.csv` | mode histogram + mean RGB |
| Compression / size | `eda_compression_stats.csv` | format + byte-size stats |
| Balance | `eda_balance_summary.csv` | imbalance ratios, missing attrs |
| Demographics (if available) | `eda_demographic_distribution.csv` | DS0005 age/gender/race |
| Run summary | `eda_summary.json` | scanned counts, sample policy, data paths |

## Label / attribute inference

| Dataset | Class | Generator | Identity | Demographics |
|---------|-------|-----------|----------|--------------|
| DS0001 | `metadata.csv` / `real`\|`fake` path | metadata `generator` | source id from filename/`original_path` | n/a |
| DS0002 | always `fake` (official test synth) | zip parent / folder (e.g. `DCFace`) | `id_*` folder when present | n/a |
| DS0003 | `real`\|`fake` folder under split | `stylegan` for fake (dataset docs); `none` for real | unavailable | n/a |
| DS0004 | `real` (RAISE) / `fake` (synth) | RAISE / synth generator folder | RAISE stem / synth stem | n/a |
| DS0005 | `real` | `none` | unavailable | FairFace label CSVs |

## Pixel sampling policy

- **Distributions from paths/metadata:** always full enumeration (no image decode).
- **Pixel metrics** (brightness/contrast/channels/resolution confirm):  
  - default `--pixel-sample 3000` stratified by (class, generator) when possible;  
  - `--full-pixels` for DoD-equivalent population scan on Kaggle.
- Corrupt/unreadable images: recorded in `eda_errors.csv` (no silent skip).

## Determinism

- Sorted walk / zip namelist order  
- Fixed RNG seed `42` for stratified sampling  
- Reports overwrite atomically per run

## Constraints

- Never modify raw files  
- Never render/save publication figures  
- Notebook outputs stripped before commit (A.7)
