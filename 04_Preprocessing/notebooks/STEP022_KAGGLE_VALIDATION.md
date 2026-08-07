# STEP-022 — Run Dataset Validation on Kaggle

## Goal
Produce `validation_report.csv`, `quality_report.csv`, and sample integrity rows for DS0001–DS0005 (Phase D6). Raw data stays read-only.

## 1. Create notebook
1. Kaggle → New Notebook  
2. **Add data** (Attach datasets):
   - `isthisdeception/ds0001-artifact-face-subset`
   - `isthisdeception/ds0002-diff-official-test`
   - `isthisdeception/ds0004-synthbuster`
   - `isthisdeception/ds0005-fairface`
   - `xhlulu/140k-real-and-fake-faces`
3. Turn on Internet **only if** you need to `pip install` (Pillow is usually preinstalled).

## 2. Upload module
Upload the folder `17_Automation/dataset_validation/` into the notebook (or copy files into `/kaggle/working/dataset_validation/`).

Alternatively paste this setup cell:

```python
# If you synced the GitHub repo into the notebook via dataset or git clone:
# !cp -r /kaggle/input/your-repo/17_Automation/dataset_validation /kaggle/working/
import sys
sys.path.insert(0, "/kaggle/working")
# or: sys.path.insert(0, "/kaggle/input/<repo-slug>/17_Automation")
```

## 3. Run validation (full DoD)

```python
from pathlib import Path
from dataset_validation import run_validation

summary = run_validation(
    dataset_ids=["DS0001", "DS0002", "DS0003", "DS0004", "DS0005"],
    search_roots=[Path("/kaggle/input")],
    output_dir=Path("/kaggle/working/reports"),
    max_images=None,              # FULL run for STEP-022 DoD
    integrity_sample_every=500,
)
print(summary)
```

Smoke test first (optional):

```python
summary = run_validation(
    dataset_ids=["DS0001", "DS0005"],
    search_roots=[Path("/kaggle/input")],
    output_dir=Path("/kaggle/working/reports_smoke"),
    max_images=200,
)
```

## 4. Download outputs
From `/kaggle/working/reports/` download:
- `validation_report.csv`
- `quality_report.csv`
- `integrity_report.csv` (samples)
- `validation_summary.json`

Put them into the GitHub repo at:
- `03_Datasets/reports/validation_report.csv`
- `03_Datasets/reports/quality_report.csv`
- merge integrity samples into `03_Datasets/reports/integrity_report.csv`

Then tell Cursor: **“STEP-022 reports ready”** so registries can be updated (`Validated=yes` / issues logged).

## Expected runtime
- DS0001 (~50k): tens of minutes  
- DS0002 (~60k in zips): 1–3 hours  
- DS0003 (~140k): 1–2 hours  
- DS0004 (~10k in zips): ~30–60 min  
- DS0005 (~98k in zip): ~1 hour  

Run overnight if needed; do not modify anything under the input datasets.
