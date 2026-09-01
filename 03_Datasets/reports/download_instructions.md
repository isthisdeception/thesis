# Dataset Download Instructions — STEP-021

> Per [A.8 Human Task Protocol](../../MASTER_RESEARCH_OPERATING_SYSTEM.md#a8-human-task-protocol), each dataset download is a **Human Task** because it requires manual interaction with external platforms (Kaggle, HuggingFace, Zenodo, GitHub/Google Drive).

---

## General Rules (Phase D4 + D5)
1. **Large image data lives in Kaggle Datasets / the Data Tier, NEVER in Git.** Only metadata, pointers, and reports go to Git ([A.6 Storage Tiers](../../MASTER_RESEARCH_OPERATING_SYSTEM.md#a6-canonical-storage--synchronization-policy)).
2. **Raw data is immutable (sacred).** Once placed in `raw/DSxxxx/`, never rename, modify, or delete files ([Phase D5](../../MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d5--raw-dataset-policy-sacred)).
3. **Record SHA-256 checksums** for every downloaded archive before extraction.
4. **Verify file counts and sizes** against the dataset documentation after extraction.

---

## PRIORITY 1: DS0003 — Real and Fake Face Detection (140k)

> **Action Required:** Verify access — NO download needed (already on Kaggle).

### Why First
Instant baseline — this dataset is natively hosted on Kaggle. A Kaggle notebook can attach it in 1 click and begin training a ResNet-34 baseline for the board presentation immediately.

### Steps
1. **Verify access:** Go to [kaggle.com/datasets/xhlulu/140k-real-and-fake-faces](https://www.kaggle.com/datasets/xhlulu/140k-real-and-fake-faces) and confirm it is accessible.
2. **Examine structure:** In a Kaggle notebook, add this dataset and verify the folder layout:
   ```
   /kaggle/input/140k-real-and-fake-faces/
   ├── real_vs_fake/
   │   └── real-vs-fake/
   │       ├── train/
   │       │   ├── real/
   │       │   └── fake/
   │       ├── valid/
   │       │   ├── real/
   │       │   └── fake/
   │       └── test/
   │           ├── real/
   │           └── fake/
   ```
3. **Run checksum verification:** Execute `dataset_checksum_verifier.py` on a random sample of 100 files to create the first real `integrity_report.csv` entries.
4. **Record in `datasets.csv`:** Set `Downloaded=yes` for DS0003 only after verification passes.

### Expected File Count
- ~70,000 real faces (Flickr/FFHQ source)
- ~70,000 fake faces (StyleGAN-generated)
- Total: ~140,000 images

---

## PRIORITY 2: DS0001 — ArtiFact Dataset (Face Subset)

> **Action Required:** Download from HuggingFace, subsample face subset, upload to Kaggle Dataset.

### Why Second
This is the PRIMARY TRAINING dataset — the core of the project. It requires subsampling from the full 2.5M-image ArtiFact collection.

### Steps
1. **Access the dataset:** Go to [huggingface.co/datasets/awsaf49/artifact-dataset](https://huggingface.co/datasets/awsaf49/artifact-dataset).
   - If the slug is incorrect or requires authentication, search HuggingFace for "ArtiFact" by Rahman et al. 2023 and locate the correct public repository.
   - Record the actual verified slug in `dataset_pointers.md`.

2. **Identify the face subset:** The full ArtiFact dataset contains 25 image categories. We need only the **face/portrait** category images.

3. **Subsample per DEC0004 strategy:**
   - **Target:** 50,000 face images total
   - **Real:** ~25,000 real face images
   - **Synthetic:** ~25,000 synthetic face images, stratified across generators (~2,000 per generator for 13 generators: ProGAN, StyleGAN2, StyleGAN3, SD v1.4, SD v1.5, SD v2.1, Midjourney, VQKD, etc.)
   - **Random seed:** Use seed `42` for reproducibility
   - **Record the subsampling script** (save to `17_Automation/`)

4. **Compute checksums:**
   - SHA-256 of the downloaded archive(s) BEFORE extraction
   - SHA-256 of a random sample of 100 extracted files

5. **Upload to Kaggle Dataset:**
   - Create a new Kaggle Dataset: `<your-username>/ds0001-artifact-face-subset`
   - Upload the 50k subsampled face images
   - Record the Kaggle slug in `dataset_pointers.md`

6. **Verify structure on Kaggle:**
   ```
   /kaggle/input/ds0001-artifact-face-subset/
   ├── raw/DS0001/
   │   ├── real/
   │   │   └── *.png|jpg
   │   └── fake/
   │       ├── progan/
   │       ├── stylegan2/
   │       ├── stylegan3/
   │       ├── sd_v1_4/
   │       ├── sd_v1_5/
   │       ├── sd_v2_1/
   │       ├── midjourney/
   │       ├── vqkd/
   │       └── ...
   ```

7. **Update registries:** Set `Downloaded=yes` in `datasets.csv` after Kaggle upload verification.

### Expected Size
- ~5–8 GB for 50k face images
- Fits within Kaggle Dataset storage limits

---

## PRIORITY 3: DS0004 — Synthbuster Dataset

> **Action Required:** Download from Zenodo, upload to Kaggle Dataset.

### Steps
1. **Download:** Go to [zenodo.org/records/10066048](https://zenodo.org/records/10066048).
   - Download the dataset archive(s) — look for ZIP/TAR files containing the synthetic and real images.
   - Compute SHA-256 of the archive before extraction.

2. **Extract and verify:**
   - Extract to a local staging folder
   - Verify: ~9,000 synthetic images from 9 diffusion models + ~1,000 RAISE-1k uncompressed real images
   - Total: ~10,000 images

3. **Upload to Kaggle Dataset:**
   - Create: `<your-username>/ds0004-synthbuster`
   - Upload extracted files maintaining the generator-level folder structure

4. **Verify structure on Kaggle:**
   ```
   /kaggle/input/ds0004-synthbuster/
   ├── raw/DS0004/
   │   ├── real/     (RAISE-1k uncompressed)
   │   └── synthetic/
   │       ├── dalle2/
   │       ├── dalle3/
   │       ├── midjourney/
   │       ├── stable_diffusion/
   │       └── ...
   ```

5. **Update registries.**

---

## PRIORITY 4: DS0002 — DiFF (Synthesized Portion Only)

> **Action Required:** Download synthesized images from Google Drive, upload to Kaggle Dataset.

### Access Notes
⚠️ Per Q2 decision, we use **only the synthesized images** (publicly available via Google Drive links in the repo README). Pristine/real images require a formal request — we will use real faces from DS0001 and DS0003 instead.

### Steps
1. **Visit the repository:** Go to [github.com/iLearn-Lab/MM24-DiFF](https://github.com/iLearn-Lab/MM24-DiFF).
   - Locate the Google Drive download links for synthesized images in the README.
   - These contain images from 13 diffusion methods.

2. **Download synthesized subset:**
   - Download the synthesized image archives from Google Drive
   - Compute SHA-256 of each archive before extraction

3. **Upload to Kaggle Dataset:**
   - Create: `<your-username>/ds0002-diff-synthesized`
   - Upload maintaining the generator-level folder structure

4. **Verify structure on Kaggle:**
   ```
   /kaggle/input/ds0002-diff-synthesized/
   ├── raw/DS0002/
   │   └── synthesized/
   │       ├── sd_v1_4/
   │       ├── sd_v1_5/
   │       ├── sd_v2_1/
   │       ├── sd_xl/
   │       ├── midjourney/
   │       ├── dalle2/
   │       ├── dalle3/
   │       ├── if/
   │       ├── ldm/
   │       └── ...
   ```

5. **Update registries.** Note in `datasets.csv` metadata that this is the synthesized-only portion.

### Expected Size
- ~500,000 synthesized images (variable sizes)
- May be several GB — verify Kaggle Dataset storage limits

---

## PRIORITY 5: DS0005 — FairFace (Demographic Fairness)

> **Action Required:** Download from GitHub/Google Drive or attach Kaggle community upload.

### Steps
1. **Check Kaggle first:** Search for "FairFace" on Kaggle Datasets. If a complete community upload exists with train/val images + label CSVs, attach that directly.

2. **If downloading from source:** Go to [github.com/dchen236/FairFace](https://github.com/dchen236/FairFace).
   - Follow the README instructions to download images from Google Drive
   - Download both `train` and `val` partitions + label CSV files

3. **Upload to Kaggle Dataset** (if not using a community upload):
   - Create: `<your-username>/ds0005-fairface`
   - Upload images + label CSVs

4. **Verify structure:**
   ```
   /kaggle/input/ds0005-fairface/ (or community slug)
   ├── raw/DS0005/
   │   ├── train/
   │   │   └── *.jpg
   │   ├── val/
   │   │   └── *.jpg
   │   ├── fairface_label_train.csv
   │   └── fairface_label_val.csv
   ```

5. **Update registries.**

### Expected File Count
- 86,744 training images + 10,954 validation images = 97,698 images (padding images bring total to 108,501)

---

## Post-Download Checklist (Per Dataset)

After each download, verify:
- [ ] Data present in Kaggle Dataset (data tier), not Git
- [ ] SHA-256 recorded per archive; `integrity_report.csv` updated with real hashes
- [ ] `raw/DSxxxx/` documented as immutable
- [ ] Git holds only pointers + reports (no images committed)
- [ ] `datasets.csv` `Downloaded=yes` set ONLY after verification
- [ ] `dataset_pointers.md` Kaggle slug updated
- [ ] Folder structure matches the documented layout above

---

## After All Downloads Complete

Run `17_Automation/dataset_checksum_verifier.py` on Kaggle across all datasets to produce the final `integrity_report.csv`, then sync back to GitHub:
```bash
git add 03_Datasets/metadata/ 03_Datasets/reports/
git commit -m "dataset: record verified download checksums and Kaggle dataset pointers for DS0001-DS0005"
git push
```
