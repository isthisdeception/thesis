# Dataset Remote Storage Pointers (Storage Tier & Kaggle Sync)

Per Handbook [A.6 Storage Tiers](MASTER_RESEARCH_OPERATING_SYSTEM.md#a6-canonical-storage--synchronization-policy) and [Phase D19 Kaggle Data Workflow](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d19--kaggle-data-workflow), large dataset image files are stored in the Data Tier (Kaggle Datasets / HuggingFace Hub) and NEVER committed directly to GitHub.

---

## Remote Dataset Pointers

### 1. DS0001 — ArtiFact Dataset (Face Subset)
- **Source:** HuggingFace Datasets (`awsaf49/artifact-dataset`)
- **Remote Slug / Pointer:** `huggingface:awsaf49/artifact-dataset`
- **Kaggle Dataset Slug:** *(To be created after download: `<username>/ds0001-artifact-face-subset`)*
- **License:** MIT License
- **Subsampling Rule:** Stratified sample of 50,000 face images (25k real + 25k synthetic across 13 generators).
- **Access Status:** ✅ Public (HuggingFace, no restrictions)
- **Download Status:** ❌ NOT YET DOWNLOADED

### 2. DS0002 — DiFF (Diffusion Facial Forgery Dataset)
- **Source:** ACM MM 2024 / GitHub Repo (`iLearn-Lab/MM24-DiFF`) *(transferred from HarryCheng2000/DiFF in Apr 2026)*
- **Remote Slug / Pointer:** `github:iLearn-Lab/MM24-DiFF`
- **Kaggle Dataset Slug:** *(To be created: `<username>/ds0002-diff-synthesized`)*
- **License:** CC BY-NC 4.0
- **Access Notes:** ⚠️ Synthesized images available via Google Drive (public). Pristine/real images require formal request. **Using synthesized portion only** + real faces from DS0001/DS0003 per Q2 decision.
- **Download Status:** ❌ NOT YET DOWNLOADED

### 3. DS0003 — Real and Fake Face Detection (140k) [Quick Baseline]
- **Source:** Kaggle Datasets (`xhlulu/140k-real-and-fake-faces`)
- **Remote Slug / Pointer:** `kaggle:xhlulu/140k-real-and-fake-faces`
- **Kaggle Dataset Slug:** `xhlulu/140k-real-and-fake-faces` *(already hosted on Kaggle — no upload needed)*
- **License:** CC BY-NC-SA 4.0
- **Purpose:** Instant Kaggle GPU execution for ResNet-34 baseline model for board presentation.
- **Access Status:** ✅ Public (native Kaggle dataset, 1-click access)
- **Download Status:** ❌ NOT YET VERIFIED (exists on Kaggle but not yet checksummed)

### 4. DS0004 — Synthbuster Dataset
- **Source:** Zenodo (`records/10066048`)
- **Remote Slug / Pointer:** `zenodo:10066048`
- **Kaggle Dataset Slug:** *(To be created: `<username>/ds0004-synthbuster`)*
- **License:** CC BY 4.0
- **Access Status:** ✅ Public (Zenodo, confirmed accessible)
- **Download Status:** ❌ NOT YET DOWNLOADED

### 5. DS0005 — FairFace (Demographic Fairness Benchmark)
- **Source:** GitHub (`dchen236/FairFace`) + Kaggle community uploads
- **Remote Slug / Pointer:** `github:dchen236/FairFace`
- **Kaggle Dataset Slug:** *(To be confirmed from Kaggle community uploads or created)*
- **License:** CC BY 4.0
- **Purpose:** Demographic bias evaluation of forensic analyst outputs (GAP0002). Provides 108k real faces annotated with 7 race groups, gender, and age.
- **Replaces:** AI-Face-FairnessBench (excluded — EULA-restricted, violates Public-Only Policy). See DEC0005.
- **Access Status:** ✅ Public (GitHub + Google Drive + Kaggle, CC BY 4.0)
- **Download Status:** ❌ NOT YET DOWNLOADED

---

## Download Priority Order (Per Q3 Decision)

| Priority | Dataset | Reason |
|----------|---------|--------|
| 1 | DS0003 | Already on Kaggle — instant baseline |
| 2 | DS0001 | Primary training dataset |
| 3 | DS0004 | Supplementary frequency-domain evaluation |
| 4 | DS0002 | Primary evaluation (synthesized portion) |
| 5 | DS0005 | Supplementary bias evaluation |

---

## Raw Data Lock Policy (Sacred - Phase D5)
1. Files under `03_Datasets/raw/DSxxxx/` on remote Kaggle sessions are strictly **immutable**.
2. Never rename, modify, or delete original files.
3. All transformations, resizes, and cropping are performed downstream in `03_Datasets/processed/DSxxxx_PPxxxx/`.
