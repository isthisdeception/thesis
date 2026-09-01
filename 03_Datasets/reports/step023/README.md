# STEP-023 — Exploratory Dataset Analysis (Phase D7)

**Status:** COMPLETE (2026-08-12)  
**Module:** `17_Automation/dataset_eda/`  
**Kaggle guide:** `04_Preprocessing/notebooks/STEP023_KAGGLE_EDA.md`  
**Figure specs:** `09_Figures/specs/FIG0001_spec.md` … `FIG0010_spec.md` (A.9 — no rendered figures)

## Policy
- Raw data read-only.
- Label/generator/identity distributions: **full enumeration**.
- Brightness/contrast/channels/resolution/compression: **stratified pixel sample n=3000, seed=42** (thumbnail ≤256 px).
- macOS junk (`__MACOSX/`, `._*`) excluded from image counts.

## Headline counts

| Dataset | Images | Class balance | Generators | Identity |
|---------|-------:|---------------|------------|----------|
| DS0001 | 50000 | 25k/25k | 13 fake + `none` | 49786 ids (near 1:1) |
| DS0002 | 57060 | fake only | 13 × FE/FS/I2I/T2I | 143 ids (leakage-critical) |
| DS0003 | 140000 | 70k/70k | stylegan / none | unavailable |
| DS0004 | 9999 | 999/9000 | RAISE + 9 synth | 1000 stems (~10 imgs) |
| DS0005 | 97698 | real only | none | unavailable; demographics in FairFace labels |

## Combined CSVs (repo root reports/)
`eda_class_distribution.csv`, `eda_generator_distribution.csv`, `eda_identity_distribution.csv`, `eda_resolution_distribution.csv`, `eda_brightness_stats.csv`, `eda_contrast_stats.csv`, `eda_channel_stats.csv`, `eda_compression_stats.csv`, `eda_balance_summary.csv`, `eda_demographic_distribution.csv`, `eda_errors.csv`, `eda_summary.json`

Per-dataset copies under `step023/DSxxxx/`.

## Implications for later steps
- **STEP-025:** filter DS0002 corrupt list (from STEP-022); also ignore macOS junk if present in archives.
- **STEP-027 splits:** group by identity for DS0002 (143 ids); DS0001 identities are nearly unique per image.
- **E9 unseen-generator:** generator tables in `eda_generator_distribution.csv` are the planning source.
