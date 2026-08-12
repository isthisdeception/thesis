# STEP-027 — Register Pipeline & Generate Processed Dataset (Kaggle)

## Goal
Run registered pipelines **PP0001–PP0005** over raw DS0001–DS0005 to produce `processed/DSxxxx_PPxxxx` on Kaggle. Sync **reports + metadata + pointers** to Git only (no image bytes).

## Registry (already in Git)
See `04_Preprocessing/preprocessing_registry.csv`:
| PP | Dataset | Output |
|----|---------|--------|
| PP0001 | DS0001 | DS0001_PP0001 |
| PP0002 | DS0002 | DS0002_PP0002 (+ corrupt exclude list) |
| PP0003 | DS0003 | DS0003_PP0003 |
| PP0004 | DS0004 | DS0004_PP0004 |
| PP0005 | DS0005 | DS0005_PP0005 |

Operations (all): `PPMOD01→10→08→07→09→05→06` (face detect/align/crop off).

## 1. Create notebook
1. Kaggle → **New Notebook**
2. **Add data** (same raw packs as STEP-022/023):
   - `isthisdeception/ds0001-artifact-face-subset`
   - `isthisdeception/ds0002-diff-official-test`
   - `isthisdeception/ds0004-synthbuster`
   - `isthisdeception/ds0005-fairface`
   - `xhlulu/140k-real-and-fake-faces`
3. Accelerator: **None** (CPU OK). Disk: prefer larger when offered.
4. Internet: off (Pillow/numpy preinstalled).

## 2. Upload code into `/kaggle/working/`
Upload (or clone) these trees:
- `04_Preprocessing/modules/`
- `04_Preprocessing/pipeline_runner.py`
- `04_Preprocessing/step027_run_preprocessing.py`
- `04_Preprocessing/exclude_lists/exclude_list_DS0002.csv`
- `17_Automation/dataset_eda/`
- `17_Automation/dataset_validation/` (for `discover_layout`)

```python
import sys
sys.path.insert(0, "/kaggle/working")
sys.path.insert(0, "/kaggle/working/04_Preprocessing")
sys.path.insert(0, "/kaggle/working/17_Automation")
```

If you uploaded the repo as a Kaggle Dataset, point `sys.path` at that input slug instead.

## 3. Smoke test (recommended first)

```python
import os
os.environ["STEP027_PIPELINE"] = "PP0003"   # smallest / public pack
os.environ["STEP027_MAX_IMAGES"] = "50"
%run /kaggle/working/04_Preprocessing/step027_run_preprocessing.py
# or: !python /kaggle/working/04_Preprocessing/step027_run_preprocessing.py
```

Confirm `/kaggle/working/processed/DS0003_PP0003/` has `images/`, `metadata/`, `reports/preprocessing_report.md`.

**Important:** the runner **refuses to overwrite** an existing `processed/DSxxxx_PPxxxx`. Delete that folder before a full re-run of the *same* PP, or register a new PP ID for new parameters.

## 4. Full runs
Run one pipeline per session if disk is tight (recommended order):

| Order | Env | Notes |
|------:|-----|-------|
| 1 | `STEP027_PIPELINE=PP0003` | public 140k — good full dry-run |
| 2 | `STEP027_PIPELINE=PP0001` | 50k primary train |
| 3 | `STEP027_PIPELINE=PP0005` | FairFace bias |
| 4 | `STEP027_PIPELINE=PP0004` | Synthbuster + RAISE |
| 5 | `STEP027_PIPELINE=PP0002` | DiFF eval + exclude list |

```python
import os
os.environ.pop("STEP027_MAX_IMAGES", None)  # full
os.environ["STEP027_PIPELINE"] = "PP0001"
!python /kaggle/working/04_Preprocessing/step027_run_preprocessing.py
```

Or all in one go (needs enough disk):

```python
os.environ["STEP027_PIPELINE"] = "ALL"
!python /kaggle/working/04_Preprocessing/step027_run_preprocessing.py
```

## 5. Publish processed outputs (data tier)
For each `processed/DSxxxx_PPxxxx`:
1. Kaggle → **New Dataset** from notebook output (or zip the folder and upload).
2. Suggested slugs (private):
   - `isthisdeception/ds0001-pp0001`
   - `isthisdeception/ds0002-pp0002`
   - `isthisdeception/ds0003-pp0003`
   - `isthisdeception/ds0004-pp0004`
   - `isthisdeception/ds0005-pp0005`
3. **Never overwrite** a published processed dataset version for param changes — new params ⇒ new `PPxxxx`.

## 6. Sync back to GitHub (metadata only)
From `/kaggle/working/git_sync/` download:
- `reports/PPxxxx_report.md` → repo `04_Preprocessing/reports/`
- `metadata/DSxxxx_PPxxxx/*` → repo `04_Preprocessing/reports/metadata/DSxxxx_PPxxxx/`

Then reply in Cursor with the five Kaggle slugs so pointers can be finalized in `03_Datasets/metadata/dataset_pointers.md`.

Strip notebook outputs before any notebook commit.

## Expected runtime
- Smoke (50 imgs): minutes  
- Full per dataset: tens of minutes to a few hours (I/O bound)

## DoD checklist
- [ ] Each `PPxxxx` registered (done in Git)
- [ ] `processed/DSxxxx_PPxxxx` exists on Kaggle
- [ ] `PPxxxx_report.md` synced to Git
- [ ] Pointers updated (no image bytes in Git)
