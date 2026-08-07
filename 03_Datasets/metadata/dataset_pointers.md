# Dataset Remote Storage Pointers (Storage Tier & Kaggle Sync)

Per Handbook [A.6 Storage Tiers](MASTER_RESEARCH_OPERATING_SYSTEM.md#a6-canonical-storage--synchronization-policy) and [Phase D19 Kaggle Data Workflow](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d19--kaggle-data-workflow), large dataset image files are stored in the Data Tier (Kaggle Datasets / HuggingFace Hub) and NEVER committed directly to GitHub.

---

## Remote Dataset Pointers

### 1. DS0001 — ArtiFact Dataset (Face Subset)
- **Source:** ArtiFact face subset (50k; prepared from public ArtiFact mirrors)
- **Remote Slug / Pointer:** `kaggle:isthisdeception/ds0001-artifact-face-subset`
- **Kaggle Dataset Slug:** [`isthisdeception/ds0001-artifact-face-subset`](https://www.kaggle.com/datasets/isthisdeception/ds0001-artifact-face-subset) *(private)*
- **License:** MIT License
- **Subsampling Rule:** 50,000 face images (25k real + 25k synthetic across 13 generators).
- **Access Status:** ✅ Uploaded to project Kaggle account (private)
- **Download Status:** ✅ DOWNLOADED / hosted on Kaggle (archive SHA-256 in `integrity_report.csv`)

### 2. DS0002 — DiFF (Diffusion Facial Forgery Dataset)
- **Source:** ACM MM 2024 / GitHub Repo (`iLearn-Lab/MM24-DiFF`)
- **Remote Slug / Pointer:** `kaggle:isthisdeception/ds0002-diff-official-test`
- **Kaggle Dataset Slug:** [`isthisdeception/ds0002-diff-official-test`](https://www.kaggle.com/datasets/isthisdeception/ds0002-diff-official-test) *(private)*
- **License:** CC BY-NC 4.0
- **Access Notes:** **Official `test` split only** (synthesized). Pristine/real images excluded; use DS0001/DS0003 for real faces. Full train/val archives remain local source vault under `_staging/incoming/DiFF/`.
- **Download Status:** ✅ DOWNLOADED / hosted on Kaggle (~60,244 test images; archive SHA-256 in `integrity_report.csv`)

### 3. DS0003 — Real and Fake Face Detection (140k) [Quick Baseline]
- **Source:** Kaggle Datasets (`xhlulu/140k-real-and-fake-faces`)
- **Remote Slug / Pointer:** `kaggle:xhlulu/140k-real-and-fake-faces`
- **Kaggle Dataset Slug:** [`xhlulu/140k-real-and-fake-faces`](https://www.kaggle.com/datasets/xhlulu/140k-real-and-fake-faces) *(public; no project upload — attach in notebooks)*
- **License:** CC BY-NC-SA 4.0
- **Purpose:** Instant Kaggle GPU execution for ResNet-34 baseline model for board presentation.
- **Access Status:** ✅ Confirmed — this is the official DS0003 baseline dataset
- **Download Status:** ✅ CONFIRMED (native Kaggle host; sample checksum still optional for STEP-022)

### 4. DS0004 — Synthbuster Dataset
- **Source:** Zenodo (`records/10066048`)
- **Remote Slug / Pointer:** `kaggle:isthisdeception/ds0004-synthbuster`
- **Kaggle Dataset Slug:** [`isthisdeception/ds0004-synthbuster`](https://www.kaggle.com/datasets/isthisdeception/ds0004-synthbuster) *(private)*
- **License:** CC BY 4.0
- **Access Status:** ✅ Uploaded to project Kaggle account (private)
- **Notes:** Real pack is RAISE **JPEG** (`raise_1k_jpeg.zip`), not uncompressed TIFF.
- **Download Status:** ✅ DOWNLOADED / hosted on Kaggle (archive SHA-256 in `integrity_report.csv`)

### 5. DS0005 — FairFace (Demographic Fairness Benchmark)
- **Source:** GitHub (`dchen236/FairFace`)
- **Remote Slug / Pointer:** `kaggle:isthisdeception/ds0005-fairface`
- **Kaggle Dataset Slug:** [`isthisdeception/ds0005-fairface`](https://www.kaggle.com/datasets/isthisdeception/ds0005-fairface) *(private)*
- **License:** CC BY 4.0
- **Purpose:** Demographic bias evaluation of forensic analyst outputs (GAP0002).
- **Padding:** **0.25** (train+val images + shared label CSVs)
- **Replaces:** AI-Face-FairnessBench (excluded — EULA-restricted). See DEC0005.
- **Access Status:** ✅ Uploaded to project Kaggle account (private)
- **Download Status:** ✅ DOWNLOADED / hosted on Kaggle (archive SHA-256 in `integrity_report.csv`)

---

## Download Priority Order (Per Q3 Decision)

| Priority | Dataset | Reason |
|----------|---------|--------|
| 1 | DS0003 | Already on Kaggle — instant baseline |
| 2 | DS0001 | Primary training dataset |
| 3 | DS0004 | Supplementary frequency-domain evaluation |
| 4 | DS0002 | Primary evaluation (official test) |
| 5 | DS0005 | Supplementary bias evaluation |

---

## Raw Data Lock Policy (Sacred - Phase D5)
1. Files under `03_Datasets/raw/DSxxxx/` on remote Kaggle sessions are strictly **immutable**.
2. Never rename, modify, or delete original files.
3. All transformations, resizes, and cropping are performed downstream in `03_Datasets/processed/DSxxxx_PPxxxx/`.
