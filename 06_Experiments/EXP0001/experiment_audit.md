# Experiment Audit: EXP0001

**Audit date:** 2026-11-09  
**Gate:** Checklist 6 — Training Completion  
**Approval Status:** PASS

## Summary

EXP0001 finished on Kaggle on 2026-11-08. `MODEL0001` is registered, the experiment row is complete, and the dataset row for `DS0001_PP0001_SPLIT0001` points at this experiment and model. The run missed the DEC0006 sanity bar and is recorded as completed, not failed.

## Passed

| Checklist 6 item | Evidence |
|------------------|----------|
| Training finished | `metrics/run_summary.json` status `complete`; 11 epochs; best epoch 7; early stop on the last scheduled epoch |
| Logs saved | `logs/EXP0001_train_20261108T160556990.log`, `logs/EXP0001_events.jsonl`, `logs/EXP0001_epochs.csv` |
| Metrics recorded | `metrics/test_metrics.json`, `metrics/val_metrics.json`, `metrics/metrics_summary.csv`, `metrics/threshold.json` |
| Checkpoints exported | `07_Checkpoints/EXP0001_checkpoints.md`: `EXP0001_best.pth`, `EXP0001_last.pth`, `MODEL0001_export.pkl`, `MODEL0001_weights.pth`, each with a SHA-256. Binaries are in Kaggle dataset `isthisdeception/thesis-experiment-artifacts` |
| Config archived | `config.yaml` unchanged since the run (SHA-256 `d3359cf56f11…`, same value as the manifest and `run_summary.json`) |
| Learning curves generated | `learning_curves/epochs.csv` (11 rows), `learning_curves/batches.csv` |
| Summary written | `metrics/run_summary.json`; `conclusions.md` |
| Registry updated | `05_Models/model_registry.csv`; `05_Models/MODEL0001_model_card.md`; `06_Experiments/experiment_registry.csv` status `completed` |
| Git synchronized | Results merged in PR #32 (`f3e5677`). This audit is the registry commit on top of that |
| Traceability | `dataset_registry.csv` row `DS0001 / v1.0 / PP0001 / DS0001_PP0001_SPLIT0001` links `EXP0001` and `MODEL0001`. Other split rows are untouched |

## Failed

None.

## Evidence not claimed

- Kaggle resume was not exercised. `run_summary.json` has `resumed_from_epoch: null`. Local interruption tests (STEP-037) still stand.
- `claim_database.csv` is unchanged. EXP0001 does not test CLAIM0001–CLAIM0008.
- `DS0001_PP0001_SPLIT0002` is not linked. This run did not use that split.

## Recommendations

1. STEP-041: evaluation inputs from the saved predictions. Do not recompute the published test metrics by hand.
2. Keep `config.yaml` immutable. A different learning rate, seed, or split is a new `EXP` ID.
3. `MODEL0002` waits until this baseline's evaluation record exists, and must use the same track.
