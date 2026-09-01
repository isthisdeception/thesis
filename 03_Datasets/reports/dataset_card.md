# Dataset Card — DS0001–DS0005 (Template 23 / Phase D8)

> **Date:** 2026-08-12  
> **Owner:** Dataset Registry / Documentation Agent  
> **Companion report:** `03_Datasets/reports/dataset_report.md`  
> **Statistics source:** STEP-022 quality/validation + STEP-023 EDA CSVs (no invented numbers)

---

## DS0001 — ArtiFact face subset

| Field | Value |
|-------|-------|
| **Dataset ID** | DS0001 |
| **Version** | 1.0 |
| **Origin** | ArtiFact face subset (public mirrors → project Kaggle pack) |
| **License** | MIT (`licenses/DS0001_license.txt`) |
| **Collection method** | Curated 50k face subset (25k real + 25k synthetic across 13 generators); hosted as Kaggle Dataset |
| **Statistics** | 50,000 images; balanced real/fake; ~49,786 identity keys; brightness mean ≈ 0.446 (n=3000 sample) |
| **Bias** | Real faces inherit FFHQ/CelebA-HQ-style web/celebrity skew; synthetic generators near-equal |
| **Ethics** | Public research imagery; MIT permits reuse with notice; no private clinical data |
| **Recommended usage** | PRIMARY-TRAIN for face forgery detectors |
| **Limitations** | Subset of full ArtiFact; fixed ~200×200 faces; not a demographic benchmark |
| **Location** | `kaggle:isthisdeception/ds0001-artifact-face-subset` |

---

## DS0002 — DiFF official TEST (synthesized)

| Field | Value |
|-------|-------|
| **Dataset ID** | DS0002 |
| **Version** | 1.0 |
| **Origin** | Cheng et al., ACM MM 2024 — DiFF official TEST synthetics |
| **License** | CC BY-NC 4.0 (`licenses/DS0002_license.txt`) |
| **Collection method** | Project Kaggle pack of official test archives (13 generators × FE/FS/I2I/T2I); pristine excluded |
| **Statistics** | 57,060 usable images after excluding macOS junk; fake-only; 143 identities; ~2.8% corrupt at STEP-022 |
| **Bias** | Synthetic-only; generator/condition size imbalance |
| **Ethics** | Non-commercial license; synthetic faces; cite Cheng et al. 2024 |
| **Recommended usage** | PRIMARY-EVAL / unseen-generator tests after corrupt filtering |
| **Limitations** | No real class; corrupt + duplicate issues logged; identity leakage risk if splits ignore `id_*` |
| **Location** | `kaggle:isthisdeception/ds0002-diff-official-test` |

---

## DS0003 — 140k real-and-fake faces

| Field | Value |
|-------|-------|
| **Dataset ID** | DS0003 |
| **Version** | 1.0 |
| **Origin** | Public Kaggle dataset `xhlulu/140k-real-and-fake-faces` (StyleGAN-era) |
| **License** | CC BY-NC-SA 4.0 (`licenses/DS0003_license.txt`) |
| **Collection method** | Native Kaggle host; attach in notebooks (no project re-upload) |
| **Statistics** | 140,000 images; 70k/70k real/fake; 256×256 JPEG; identity unavailable |
| **Bias** | Single fake generator family (StyleGAN); face-domain web skew |
| **Ethics** | NC + ShareAlike constraints on derivatives; cite dataset page / NVlabs lineage |
| **Recommended usage** | QUICK-BASELINE training and smoke tests |
| **Limitations** | Weak multi-generator evidence; ShareAlike complicates redistribution of derivatives |
| **Location** | `kaggle:xhlulu/140k-real-and-fake-faces` |

---

## DS0004 — Synthbuster + RAISE JPEG

| Field | Value |
|-------|-------|
| **Dataset ID** | DS0004 |
| **Version** | 1.0 |
| **Origin** | Bammey 2024 / Zenodo 10066048 (Synthbuster) + RAISE JPEG real pack |
| **License** | CC BY 4.0 (`licenses/DS0004_license.txt`) |
| **Collection method** | Zenodo download → project Kaggle pack (`raise_1k_jpeg` + synth generators) |
| **Statistics** | 9,999 images; 999 real / 9,000 synth (9×1000); variable resolution |
| **Bias** | Real = camera RAISE JPEGs (not matched web faces); class imbalance ≈1:9 |
| **Ethics** | Permissive CC BY with attribution; JPEG reals differ from original TIFF RAISE release |
| **Recommended usage** | SUPPLEMENTARY-FREQUENCY / cross-generator probes |
| **Limitations** | Imbalance; format mismatch real vs synth; large storage footprint |
| **Location** | `kaggle:isthisdeception/ds0004-synthbuster` |

---

## DS0005 — FairFace (padding 0.25)

| Field | Value |
|-------|-------|
| **Dataset ID** | DS0005 |
| **Version** | 1.0 |
| **Origin** | Karkkainen & Joo, WACV 2021 — FairFace (replaces EULA-restricted alternative per DEC0005) |
| **License** | CC BY 4.0 (`licenses/DS0005_license.txt`) |
| **Collection method** | FairFace margin-0.25 train+val images + label CSVs → project Kaggle pack |
| **Statistics** | 97,698 real faces; train 86,744 / val 10,954; age/gender/race labels; 224×224 |
| **Bias** | Residual race/gender skew; FairFace taxonomy; no synthetic class |
| **Ethics** | Faces of real people with demographic labels — use for evaluation fairness only; cite WACV 2021; avoid re-identification attempts |
| **Recommended usage** | SUPPLEMENTARY-BIAS evaluation of detector/analyst outputs |
| **Limitations** | Cannot train binary real/fake alone; some duplicate hashes |
| **Location** | `kaggle:isthisdeception/ds0005-fairface` |

---

## Portfolio notes

- **Public-only policy:** DEC0004 / strict public licenses.
- **Storage tier:** Images on Kaggle; Git = metadata + reports (`dataset_pointers.md`).
- **Ready flag:** All rows `Ready=yes` as of STEP-029 (Checklist 3 + 4; human confirmation requested).
