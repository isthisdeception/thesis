# STEP-031 — Kaggle Dataset Upload & Sync Setup

**Status:** COMPLETE (automation scaffolded 2026-09-06) — dry-run on Kaggle still recommended before first `EXP`  
**Handbook:** Phase D19; §10 Phases 7, 10, 18; A.6

## Done
- [x] `17_Automation/kaggle_sync/` package created
- [x] `17_Automation/kaggle_sync/sync_plan.example.yaml` added with current raw + processed dataset slugs
- [x] Commands implemented for `bootstrap`, `resume-checkpoints`, `publish-artifacts`, and `push-metadata`
- [x] `06_Experiments/KAGGLE_SESSION_TEMPLATE.ipynb` added in canonical session order
- [x] `17_Automation/README.md` updated

## Remaining (recommended first dry-run)
Run the notebook template on Kaggle with a real repo URL, attached datasets, and Kaggle/Git credentials in secrets. Confirm:
- bootstrap clones `develop`
- mounted datasets are detected
- checkpoint copy works for the active `EXPxxxx`
- artifact publish target already exists or is initialized before versioning
- metadata-only push excludes weights and image data

## Next step
**STEP-032** — Candidate model discovery.
