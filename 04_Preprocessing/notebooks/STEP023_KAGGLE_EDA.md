# STEP-023 — Run Exploratory Dataset Analysis on Kaggle

## Goal
Produce Phase D7 EDA CSVs for DS0001–DS0005 (class/generator/identity/resolution/brightness/contrast/channels/compression/balance/demographics). **Do not render publication figures** — figure specs live in Git under `09_Figures/specs/`.

## 1. Create notebook
1. Kaggle → New Notebook  
2. **Add data** (Attach datasets):
   - `isthisdeception/ds0001-artifact-face-subset`
   - `isthisdeception/ds0002-diff-official-test`
   - `isthisdeception/ds0004-synthbuster`
   - `isthisdeception/ds0005-fairface`
   - `xhlulu/140k-real-and-fake-faces`
3. Internet off (Pillow/numpy are preinstalled).

## 2. Upload modules
Upload into `/kaggle/working/`:
- `17_Automation/dataset_eda/`
- `17_Automation/dataset_validation/` (adapters reused)
- optional: `17_Automation/step023_run_eda.py`

```python
import sys
sys.path.insert(0, "/kaggle/working")
# or: sys.path.insert(0, "/kaggle/input/<repo-slug>/17_Automation")
```

## 3. Run EDA

**Recommended DoD (stratified pixel sample n=3000; full label enumeration):**

```python
from pathlib import Path
from dataset_eda import run_eda

summary = run_eda(
    dataset_ids=["DS0001", "DS0002", "DS0003", "DS0004", "DS0005"],
    search_roots=[Path("/kaggle/input")],
    output_dir=Path("/kaggle/working/reports"),
    pixel_sample=3000,
    full_pixels=False,
    seed=42,
)
print(summary)
```

**Optional population pixel scan (slow):**

```python
summary = run_eda(
    dataset_ids=["DS0001", "DS0002", "DS0003", "DS0004", "DS0005"],
    search_roots=[Path("/kaggle/input")],
    output_dir=Path("/kaggle/working/reports_full"),
    full_pixels=True,
)
```

## 4. Download outputs → GitHub
From `/kaggle/working/reports/` sync:

- `eda_class_distribution.csv`
- `eda_generator_distribution.csv`
- `eda_identity_distribution.csv`
- `eda_resolution_distribution.csv`
- `eda_brightness_stats.csv`
- `eda_contrast_stats.csv`
- `eda_channel_stats.csv`
- `eda_compression_stats.csv`
- `eda_balance_summary.csv`
- `eda_demographic_distribution.csv`
- `eda_errors.csv`
- `eda_summary.json`
- `step023/` (per-dataset copies)

Into repo: `03_Datasets/reports/`.

Strip notebook outputs before any notebook commit (A.7). Never commit image bytes.

## Expected runtime
- Label enumeration: minutes  
- Pixel sample (3k/dataset): ~30–90 min total  
- Full pixels: several hours (overnight)

Raw inputs stay read-only.
