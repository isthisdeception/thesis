# STEP-036 — Training Pipeline Package

**Status:** COMPLETE — smoke test passes locally (CPU); Kaggle smoke run still recommended before EXP0001  
**Handbook:** Phase M6; Phase M3; Phase M11; Phase M15; Phase M16

## Output created
- [x] `17_Automation/training/` package: config-driven, typed, every step logged with explicit failures
- [x] `06_Experiments/EXP0001/notebook/EXP0001_train.ipynb` — thin caller (imports, `find_lr`, `run_experiment`); no outputs
- [x] Produces per-epoch checkpoints, `best_model.pth`, `last_checkpoint.pth`, `export.pkl`, `weights.pth`, val/test predictions, canonical metrics, calibration data, learning-curve data, and `run_summary.json`
- [x] Tests: `tests/test_training_core.py` (15, no FastAI) and `tests/test_training_smoke.py` (6, end-to-end on 32 synthetic images); full suite 78 passed with the pinned CPU stack (torch 2.10.0, torchvision 0.25.0, fastai 2.8.7)

## Config changes (pre-training, EXP0001 still `ready`)
Values that had been implicit are now explicit in `config.yaml` and checked by the validator: `metrics.positive_class` (`fake`), `metrics.threshold_criterion` (`max_balanced_accuracy`), `metrics.calibration_bins` (15), `fastai.schedule.{lr_mult, pct_start, div}` (100, 0.3, 5.0 — FastAI defaults), `fastai.lr_finder.num_it` (100).

## Environment finding
`plum-dispatch` ≥ 2.6 adds an RLock to FastAI transforms, so `learn.export` fails. `environment/requirements.txt` now pins `plum-dispatch==2.5.7`; the pipeline checks picklability before training. The Kaggle v170 version of `plum-dispatch` is unverified — the first Kaggle session will report it.

## Next step
**STEP-037** — Checkpoint system (resume, manifests, checksums in `07_Checkpoints/`).
