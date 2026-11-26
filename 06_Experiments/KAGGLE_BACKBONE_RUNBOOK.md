# Kaggle Multi-Backbone Upgrade Guide (`EXP0007` EfficientNet-B4 & `EXP0008` ViT-B/16)

You can run **both** notebooks simultaneously in **2 browser tabs** on Kaggle (`~60–85 minutes` total wall-clock time):

1. **Notebook 1 (`EfficientNet-B4` / `MODEL0003`):**
   `06_Experiments/EXP0007/notebook/EXP0007_train_and_eval.ipynb`
2. **Notebook 2 (`ViT-B/16` Vision Transformer / `MODEL0004`):**
   `06_Experiments/EXP0008/notebook/EXP0008_train_and_eval.ipynb`

---

## Step-by-Step Instructions (Identical for Both Tabs)

1. Open **https://www.kaggle.com/code** -> **New Notebook** -> **File -> Import Notebook** and upload the `.ipynb` file.
2. In the right-hand **Notebook Options** panel:
   - **Accelerator:** select **`GPU T4 x2`** *(never select P100)*.
   - **Internet:** toggle **`On`**.
3. Click **`+ Add Input`** -> **Your Datasets** (or search `isthisdeception/`) and attach all 5 processed datasets:
   - `isthisdeception/ds0001-pp0001` *(required)*
   - `isthisdeception/ds0002-pp0002`
   - `isthisdeception/ds0003-pp0003`
   - `isthisdeception/ds0004-pp0006`
   - `isthisdeception/ds0005-pp0005`
4. Click **`Run All`**!
   - Cell 0 bootstraps the repository and validates the `config.yaml` schema.
   - Cell A trains the model on `DS0001 SPLIT0001` (`224x224`, 1 frozen + up to 10 unfrozen epochs, early stopping, validation-only threshold freezing) and exports `val_predictions.csv` + `test_predictions.csv`.
   - Cell B automatically runs zero-shot cross-dataset evaluation across `DS0002` (DiFF), `DS0003` (140k Faces), `DS0004` (Synthbuster), and `DS0005` (FairFace).
   - Cell C creates a compact ~4 MB file in `/kaggle/working/`:
     - **`EXP0007_results_bundle.zip`** (in Tab 1)
     - **`EXP0008_results_bundle.zip`** (in Tab 2)
5. When finished, download `EXP0007_results_bundle.zip` and `EXP0008_results_bundle.zip` into the repository root (or any folder) and tell Antigravity! Running:
   ```powershell
   .\.venv\Scripts\python.exe 17_Automation\integrate_new_backbones.py EXP0007_results_bundle.zip EXP0008_results_bundle.zip
   ```
   will automatically unpack all metrics/predictions, run 10,000-resample paired bootstrap + exact McNemar tests, run multi-specialist (`K = 3`: ResNet-50 + EfficientNet-B4 + ViT-B/16) `M1`–`M18` fusion across `EVAL0008`, and regenerate all figures!
