# STEP-047 — Cross-Dataset Kaggle Runbook (Part 1, Phase E8)

**Notebook:** `08_Evaluation/EVAL0001/generalization/STEP047_cross_dataset.ipynb` (thin caller)  
**Config:** `08_Evaluation/EVAL0001/generalization/config.yaml`  
**Images:** 500 DS0001 sanity images, then DS0002 7364, DS0003 20000, DS0004 1500, DS0005 10000 (fixed sample)

## One-time preparation

1. Import the notebook: *Kaggle → Create → New Notebook → File → Import Notebook*, paste the GitHub URL of `STEP047_cross_dataset.ipynb` on `main`.
2. Notebook settings: *Accelerator* `GPU T4 x2`, *Internet* `On`.
3. *Add Input* (six datasets): `isthisdeception/ds0001-pp0001`, `isthisdeception/ds0002-pp0002`, `isthisdeception/ds0003-pp0003`, `isthisdeception/ds0004-pp0006`, `isthisdeception/ds0005-pp0005`, `isthisdeception/thesis-experiment-artifacts`.
4. *Add-ons → Secrets*: tick `GITHUB_TOKEN` for this notebook.

## Session (about 1 hour)

1. Run **0 Setup** (four cells). Expect `GITHUB_TOKEN loaded`, a bootstrap without `required Kaggle input missing`, a GPU name, and four dataset lines ending in `config SHA-256 …`.
2. Run **A**. Expect `export: …MODEL0001_export.pkl`, `sanity check PASS: 500 reference images …`, then one line per dataset. Reading images dominates; lines appear as each dataset finishes.
3. Run **B**. It prints one row per dataset.
4. Run **C**. It prints `pushed to kaggle/cross-dataset-<time>`. Send that branch name to the repository side.

## If something goes wrong

| Message | Meaning | What to do |
|---------|---------|------------|
| `required Kaggle input missing for dsXXXX_processed` | That dataset is not attached | Add it, run 0 again |
| `… not found under …; attach the processed dataset` | The dataset is attached but its folder layout differs | Report the message and the folder names shown in the input panel |
| `CleanCheckError` | The sanity images do not match the saved predictions | Stop and report; nothing else is kept |
| Session interrupted during A | Finished datasets are in `08_Evaluation/EVAL0001/generalization/predictions/` | In the same session, run 0 and A again |

## What goes where

| Output | Location |
|--------|----------|
| `predictions/DS000N.csv` (per-image P(fake)), `run_manifest.json` | `08_Evaluation/EVAL0001/generalization/` → pushed to Git |
| `cross_dataset_metrics.csv`, `cross_dataset_by_generator.csv`, `cross_dataset_by_relation.csv`, `cross_dataset_report.md` | same folder → pushed to Git |
