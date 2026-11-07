# STEP-038 — Logging System

**Status:** COMPLETE (verified locally on CPU)  
**Handbook:** Phase M11; Phase M16; A.2 log naming

## Output created
- [x] `training/logs.py`: per-session `EXPxxxx_<stage>_<time>.log`, append-only `EXPxxxx_events.jsonl`, Python-warning capture, warning/error counts, step start/done/failed events, run_failed logging outside steps
- [x] `training/records.py`: fixed CSV schemas; append refuses header mismatches
- [x] Live per-epoch records written as each epoch ends: `logs/EXPxxxx_epochs.csv` (metrics, timing, LR, GPU peak allocated/reserved), `logs/EXPxxxx_batches.csv`; session-tagged so interrupted + resumed sessions are distinguishable
- [x] `logs/EXPxxxx_hyperparameters_<session>.json`: config echo + derived per-phase LR arguments, data sizes, model size, monitors, device
- [x] `metrics/metrics_summary.csv`; `run_summary.json` now links all log files and reports warning/error counts and sessions
- [x] `kaggle_sync push-metadata`: refuses binaries / files > 20 MB (unstages and fails); skips missing paths. Sync plan lists EXP0001 logs, metrics, learning curves, predictions, observations, checkpoint manifest
- [x] Fix: logs from an attempt that died before its first checkpoint no longer block a fresh rerun
- [x] Docs: `training/LOGGING.md` (file list, CSV + event schemas)

## Verification
- Per-epoch metrics, GPU memory, timing, hyperparameters: `test_live_logs_and_event_log`, `test_hyperparameter_record`
- Warnings/errors explicit: `test_python_warnings_are_captured_and_counted`, `test_step_failure_is_logged_with_traceback`; interrupted run leaves a `run_failed` event and live rows from both sessions
- Learning-curve data: `learning_curves/*.csv` with the documented schemas
- No binaries to Git: `test_push_metadata_refuses_binaries`
- Suite: 101 passed (pinned CPU stack)

## Next step
**STEP-039** — Run EXP0001 on Kaggle.
