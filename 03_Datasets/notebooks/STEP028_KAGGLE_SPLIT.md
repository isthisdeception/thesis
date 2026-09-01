# STEP-028 — Leakage-Safe Train/Val/Test Split (Kaggle optional)

## Goal
Produce `DSxxxx_PPxxxx_SPLITxxxx` index files + `split_report.md` from preprocessing `index.csv` metadata. **No image bytes in Git.**

Splits can run **locally** from synced index files in `04_Preprocessing/reports/metadata/` (recommended). Kaggle is optional for re-running against mounted processed datasets.

## Local run (recommended)

```bash
cd 17_Automation
python step028_run_splits.py
```

Outputs:
- `03_Datasets/splits/DSxxxx_PPxxxx_SPLITxxxx/` (`assignments.csv`, `train.csv`, `val.csv`, `test.csv`, `split_config.json`, `leakage_check.json`)
- `03_Datasets/reports/split_report.md`

## Kaggle notebook (optional re-run)

```python
!git clone https://github.com/isthisdeception/thesis.git /kaggle/working/thesis
import sys
sys.path.insert(0, "/kaggle/working/thesis/17_Automation")
from pathlib import Path
from dataset_split.runner import run_splits
run_splits(repo_root=Path("/kaggle/working/thesis"))
```

Attach processed Kaggle datasets only if you need to validate `processed_path` files exist; split logic uses `index.csv` only.

## Split schemes (per output)

| Output | SPLIT0001 | SPLIT0002 |
|--------|-----------|-----------|
| DS0001_PP0001 | grouped 70/15/15 (identity+generator) | LOGO: `stable_diffusion` → test |
| DS0002_PP0002 | grouped 70/15/15 | LOGO: `Midjourney` → test |
| DS0003_PP0003 | official `valid` → test | LOGO: `stylegan` → test |
| DS0004_PP0006 | grouped 70/15/15 | LOGO: `dalle3` → test |
| DS0005_PP0005 | official `val` → test | grouped 70/15/15 |

## DoD checklist
- [ ] Standard + LOGO split per primary output
- [ ] Leakage assertion PASS (automated)
- [ ] Same seed reproduces identical fingerprint
- [ ] Only index files in Git
