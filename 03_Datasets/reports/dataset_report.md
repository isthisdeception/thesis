# Dataset Report — DS0001–DS0005 (Phase D8 / STEP-024)

> **Document type:** Template 5 — Dataset Report (master raw-dataset report)  
> **Date:** 2026-08-12  
> **Owner:** Dataset Documentation Agent  
> **Scope:** Raw, validated, documented datasets. Preprocess + split + FastAI prep completed at STEP-029 (`Ready=yes`).  
> **Evidence sources:** `datasets.csv`, `dataset_pointers.md`, `licenses/`, `reports/{validation,quality,integrity}_report.csv`, `reports/step022/`, `reports/eda_*.csv`, `reports/step023/`

---

## 1. Portfolio overview

| ID | Role | Images (EDA enum.) | Real/Fake | License | Validated | Ready |
|----|------|-------------------:|-----------|---------|-----------|-------|
| DS0001 | PRIMARY-TRAIN | 50,000 | 25k / 25k | MIT | yes | yes |
| DS0002 | PRIMARY-EVAL | 57,060 usable (51,452 processed) | 0 / 57,060 | CC BY-NC 4.0 | yes (issues logged) | yes |
| DS0003 | QUICK-BASELINE | 140,000 | 70k / 70k | CC BY-NC-SA 4.0 | yes | yes |
| DS0004 | SUPPLEMENTARY-FREQUENCY | 9,999 | 999 / 9,000 | CC BY 4.0 | yes | yes |
| DS0005 | SUPPLEMENTARY-BIAS | 97,698 | 97,698 / 0 | CC BY 4.0 | yes | yes |

Remote locations: `03_Datasets/metadata/dataset_pointers.md`. Image bytes live in the Kaggle data tier (A.6); Git holds metadata/reports only.

---

## 2. DS0001 — ArtiFact face subset (PRIMARY-TRAIN)

### Origin & purpose
Face-oriented 50k subset prepared from public ArtiFact mirrors for **primary training** of image-based AI-generated face detectors. Supports generator-diverse synthetic faces plus real faces.

### Location
- Kaggle: `isthisdeception/ds0001-artifact-face-subset` (private)
- License file: `03_Datasets/licenses/DS0001_license.txt` (MIT)

### Citation
Rahman et al., 2023 (OpenML / ArtiFact lineage). Registry: `datasets.csv` row DS0001.

### Validation results (STEP-022)
- Scanned: 50,000; corrupt: 0; threshold_pass: **yes**  
- Sources: `quality_report.csv`, `reports/step022/DS0001_*`

### Statistics (STEP-023 EDA)
- Class: real 25,000 / fake 25,000 (`eda_class_distribution.csv`)
- Generators: 13 synthetic + `none` for real (`eda_generator_distribution.csv`)
- Identity: ~49,786 unique ids; near 1 image/id (`eda_identity_distribution.csv`)
- Brightness (sample n=3000): mean luma ≈ 0.446 (`eda_brightness_stats.csv`)
- Resolution: fixed 200×200 in quality/EDA samples

### Strengths
Balanced classes; multi-generator fakes; MIT license; clean validation.

### Weaknesses / known problems
Subset (not full ArtiFact); faces already cropped/resized; identity nearly unique so identity-grouped splits add little beyond random.

### Known biases
Generator mix is near-uniform across 13 fakes; real sources include FFHQ/CelebA-HQ style faces (Western-skewed celebrity/web faces common in those corpora).

### Recommended usage
Primary train/val for detector backbones; hold out generators for E9-style unseen-generator tests when paired with DS0002/DS0004.

### Research relevance
Core training corpus for the thesis direction (AI Forensic Analyst over image face forgeries).

---

## 3. DS0002 — DiFF official TEST (PRIMARY-EVAL)

### Origin & purpose
ACM MM 2024 DiFF **official synthesized TEST** split only (pristine/real excluded). Primary **cross-generator evaluation** set.

### Location
- Kaggle: `isthisdeception/ds0002-diff-official-test` (private)
- License: `03_Datasets/licenses/DS0002_license.txt` (CC BY-NC 4.0)

### Citation
Cheng et al., 2024, ACM MM (DiFF / MM24-DiFF).

### Validation results (STEP-022)
- Scanned ≈ 57,059; corrupt 1,593 (rate ≈ 2.79%); threshold_pass: **no**  
- `Validated=yes` with issues plan: `reports/step022/DS0002_issues_plan.md` (filter in STEP-025; raw untouched)

### Statistics (STEP-023 EDA)
- Usable enumerated images: **57,060** (macOS `__MACOSX` / `._*` junk excluded)
- Class: fake only
- 13 generators × conditions FE / FS / I2I / T2I (`eda_generator_distribution.csv`)
- **143 identities**; mean ≈ 399 images/id — **leakage-critical for splits**
- Brightness sample mean ≈ 0.446

### Strengths
Official test protocol; diffusion-heavy generators; identity structure for grouped evaluation.

### Weaknesses / known problems
No real class in this pack; ~2.8% corrupt files; archive manifests list ~60,244 members including junk; CC BY-NC restricts commercial use.

### Known biases
Synthetic-only eval; condition/generator imbalance (e.g. HPS/T2I and cycle_diff/FE larger than DiffFace/FS).

### Recommended usage
Primary evaluation / E9 unseen-generator reporting **after** STEP-025 corrupt filter. Pair with DS0001/DS0003 reals for binary metrics.

### Research relevance
Primary evidence for generalization beyond training generators.

---

## 4. DS0003 — 140k real-and-fake faces (QUICK-BASELINE)

### Origin & purpose
Public Kaggle pack for **fast baseline** training (e.g. ResNet-34 board demos). StyleGAN fakes vs real faces at 256×256.

### Location
- Kaggle (native): `xhlulu/140k-real-and-fake-faces` (public)
- License: `03_Datasets/licenses/DS0003_license.txt` (CC BY-NC-SA 4.0)

### Citation
Kaggle / NVlabs lineage, 2020 (per `datasets.csv`).

### Validation results (STEP-022)
- Scanned: 140,000; corrupt: 0; threshold_pass: **yes**

### Statistics (STEP-023 EDA)
- Class: 70,000 real / 70,000 fake
- Generator: `none` (real) / `stylegan` (fake)
- Identity: unavailable
- Resolution: 256×256 JPEG

### Strengths
Large, balanced, instantly attachable on Kaggle; clean validation.

### Weaknesses / known problems
Single fake generator family; ShareAlike + NC license; weaker for multi-generator claims.

### Known biases
StyleGAN-era artifacts only; face domain similar to CelebA-HQ/FFHQ-derived sets.

### Recommended usage
Quick baselines and engineering smoke tests — **not** sole evidence for unseen-generator claims.

### Research relevance
Enables rapid iteration before heavier DS0001/DS0002 runs.

---

## 5. DS0004 — Synthbuster + RAISE JPEG (SUPPLEMENTARY-FREQUENCY)

### Origin & purpose
Zenodo Synthbuster synthetics + RAISE JPEG reals for **frequency-domain / multi-generator** supplementary evaluation.

### Location
- Kaggle: `isthisdeception/ds0004-synthbuster` (private)
- License: `03_Datasets/licenses/DS0004_license.txt` (CC BY 4.0)
- Note: real pack is RAISE **JPEG**, not uncompressed TIFF (`dataset_pointers.md`)

### Citation
Bammey, 2024, IEEE OJSP; Zenodo record 10066048.

### Validation results (STEP-022)
- Unique images ≈ 9,999; corrupt: 0; threshold_pass: **yes** (nested re-scan historically inflated duplicate warnings; leaf-root policy applied)

### Statistics (STEP-023 EDA)
- 999 real (`raise_1k_jpeg`) / 9,000 synthetic (9 generators × 1,000)
- Identity stems: 1,000 unique (~10 images/stem across generators)
- Resolution highly variable (quality_report: width 256–4928)

### Strengths
Diverse modern generators (DALL·E, Firefly, SD family, Midjourney, etc.); permissive CC BY; frequency-research lineage.

### Weaknesses / known problems
Class imbalance (≈1:9); real JPEG vs often-PNG synthetics; large archives.

### Known biases
Real class is RAISE camera photos (not web-face matched); generator set differs from DS0001/DS0002.

### Recommended usage
Supplementary frequency / cross-generator probes; not primary train unless rebalanced.

### Research relevance
Supports robustness and spectral-forensic angles complementary to DiFF.

---

## 6. DS0005 — FairFace margin 0.25 (SUPPLEMENTARY-BIAS)

### Origin & purpose
Demographic fairness benchmark (age/gender/race) for **bias evaluation** of forensic analyst outputs (GAP0002). Replaces EULA-restricted AI-Face-FairnessBench per `DEC0005`.

### Location
- Kaggle: `isthisdeception/ds0005-fairface` (private)
- License: `03_Datasets/licenses/DS0005_license.txt` (CC BY 4.0)
- Padding: **0.25** (train+val)

### Citation
Karkkainen & Joo, WACV 2021 (FairFace).

### Validation results (STEP-022)
- Scanned: 97,698; corrupt: 0; duplicate_hash warnings: 161; threshold_pass: **yes**

### Statistics (STEP-023 EDA)
- All **real**; splits train 86,744 / val 10,954
- Demographics: `eda_demographic_distribution.csv` (race/gender/age)
- Resolution: 224×224 JPEG
- Identity: unavailable

### Strengths
Labeled demographics; CC BY; aligned to bias gap.

### Weaknesses / known problems
No fake class (cannot train binary detector alone); race/gender label taxonomy is FairFace-specific; some hash duplicates.

### Known biases
FairFace aims for race balance but residual skew remains (e.g. White larger share in train); Western annotation taxonomy limits.

### Recommended usage
Fairness / subgroup evaluation of deployed detectors and analyst reports — not primary forgery training.

### Research relevance
Directly supports GAP0002 demographic fairness evaluation.

---

## 7. Cross-cutting validation & integrity

| Artifact | Path | Status |
|----------|------|--------|
| Validation findings | `reports/validation_report.csv`, `reports/step022/` | Present |
| Quality aggregates | `reports/quality_report.csv` | Present |
| Integrity samples | `reports/integrity_report.csv` | Present |
| EDA suite | `reports/eda_*.csv`, `reports/step023/` | Present |
| Figure specs | `09_Figures/specs/FIG0001`–`FIG0010` | Specs only (A.9) |

**Raw lock:** originals immutable on Kaggle; no image bytes in Git.

---

## 8. Known portfolio-level issues

1. DS0002: 5,608 images excluded at PP0002 (see `preprocessing_audit.md`); processed v1.0 count is 51,452. Raw untouched.
2. Checklist 3 (full) and Checklist 4: **PASS** at STEP-029 — see `dataset_audit.md` and `04_Preprocessing/reports/preprocessing_audit.md`.
3. `datasets.csv` `Ready=yes`. Checklists 3 and 4 **PASS** (human-confirmed 2026-09-01).

---

## 9. Definition of Done (this report)

- Origin, purpose, license, statistics, strengths, weaknesses, biases, usage, problems, research relevance, citation, and location recorded for DS0001–DS0005 with evidence citations.
- Aligns with Phase D8; pairs with `dataset_card.md` and `dataset_audit.md`.
