# 04_Preprocessing

**Purpose:** Modular, versioned preprocessing pipelines (PPxxxx).

## Phase Status
- **STEP-025 — Pipeline Design:** `COMPLETE`
- **STEP-026 — Implement modules:** `COMPLETE` (`modules/`, 34 tests)
- **STEP-027 — Register & generate processed:** `IN PROGRESS`
  - Registry: `preprocessing_registry.csv` (PP0001–PP0005)
  - Exclude list: `exclude_lists/exclude_list_DS0002.csv`
  - Kaggle guide: `notebooks/STEP027_KAGGLE_PREPROCESS.md`
  - Runner: `step027_run_preprocessing.py`
  - Reports: `reports/PPxxxx_report.md` (stubs until Kaggle sync)
  - Status: `STEP027_STATUS.md`

## Package layout

```
04_Preprocessing/
  modules/                 # PPMOD01–10 + discovery + report_writer
  pipeline_runner.py       # thin sequencer
  step027_run_preprocessing.py
  exclude_lists/
  reports/
  tests/
```

## Rules
- **No monolith** — one module per Phase D9 step; parameters injected.
- **Raw read-only** — writes only under `processed/DSxxxx_PPxxxx/`.
- **Fail loudly** — `ModuleError` / exclude CSVs; never silent skips.
- **Never overwrite** processed outputs; new params ⇒ new `PPxxxx`.
- **No processed image bytes in Git.**

## Run unit tests
```bash
cd 04_Preprocessing
python -m pytest tests/ -v
```

## Owner
Preprocessing Agent

## Related Folders
`03_Datasets`, `17_Automation/dataset_eda`, `17_Automation/dataset_validation`
