# Training Logging & Record Schemas (STEP-038, Phase M11)

Everything a run produces is written to files in the experiment folder as it happens, so a Kaggle session that dies loses nothing already logged. All files are small text files that return to Git through `kaggle_sync push-metadata`; binaries stay in the artifact tier, and `push-metadata` refuses to commit them.

## Files

| Path (under `06_Experiments/EXPxxxx/`) | Written | Scope | Contents |
|------|---------|-------|----------|
| `logs/EXPxxxx_<stage>_<time>.log` | continuously | one per session (`stage` = `train` or `lr_find`) | human-readable log: steps, epochs, checkpoints, captured Python warnings, errors with tracebacks |
| `logs/EXPxxxx_events.jsonl` | continuously, append-only | all sessions | one JSON object per event (schema below) |
| `logs/EXPxxxx_epochs.csv` | after every epoch, append-only | all sessions | per-epoch metrics, timing, LR, GPU memory |
| `logs/EXPxxxx_batches.csv` | after every epoch, append-only | all sessions | per-iteration training loss and LR |
| `logs/EXPxxxx_hyperparameters_<session>.json` | at run start | one per training session | resolved config, config SHA-256, per-phase LR arguments, data sizes, model size, monitors, device, seed |
| `logs/EXPxxxx_lr_find_<session>.json`, `..._lr_find_curve_<session>.csv` | after LR Finder | one per LR Finder session | suggestion + LR/loss curve |
| `logs/history.csv` | FastAI `CSVLogger` | raw | FastAI's own per-epoch log (also writes rows for epochs skipped on resume; use `EXPxxxx_epochs.csv` instead) |
| `learning_curves/epochs.csv`, `learning_curves/batches.csv` | end of run | final | same schemas as the live CSVs, rebuilt from checkpoint-backed history: exactly one row per epoch/iteration, even across resumes |
| `metrics/metrics_summary.csv` | end of run | final | one row per split (`val`, `test`) |
| `metrics/run_summary.json` | end of run | final | everything above linked, plus warning/error counts and session list |

A *session* is one call to `run_experiment` or `find_lr`; its ID is `<stage>_<YYYYMMDDTHHMMSSmmm>`. Live CSV rows carry the session ID, so an epoch that was re-run after an interruption appears once per session in the live CSV and once in the final `learning_curves/epochs.csv`.

## `EXPxxxx_epochs.csv` / `learning_curves/epochs.csv`

Column order is fixed for a given config:

| Column | Meaning |
|--------|---------|
| `session` | session that ran the epoch |
| `epoch` | run-wide epoch (0-based, across frozen + unfrozen phases) |
| `phase` | `frozen` or `unfrozen` |
| `phase_epoch` | epoch within the phase |
| `train_loss`, `valid_loss` | FastAI smoothed training loss, validation loss |
| *monitors…* | one column per FastAI monitor, in config order (`metrics.primary` then `metrics.secondary`, those with a FastAI equivalent), named as FastAI reports them, e.g. `roc_auc_score`, `f1_score`, `balanced_accuracy_score`, `matthews_corrcoef`, `precision_score`, `recall_score`, `accuracy` |
| `seconds` | wall time of the epoch |
| `lr_head` | LR of the last parameter group at epoch end |
| `gpu_peak_allocated_mb`, `gpu_peak_reserved_mb` | peak CUDA memory during the epoch (empty on CPU) |

Appending to a file whose header differs from this schema raises `RecordSchemaError`.

## `EXPxxxx_batches.csv` / `learning_curves/batches.csv`

`session, iteration, epoch, phase, loss, lr`: one row per training iteration (`iteration` is run-wide).

## `metrics/metrics_summary.csv`

`split, threshold, roc_auc, pr_auc, f1, balanced_accuracy, mcc, precision, recall, specificity, fpr, fnr, accuracy, ece, brier, tp, tn, fp, fn, n, n_positive`. The threshold is chosen on `val` and applied unchanged to `test`.

## `EXPxxxx_events.jsonl`

Every line has `time` (ISO-8601 with offset), `session`, `event`, plus event fields:

| `event` | Fields |
|---------|--------|
| `session_start` | `stage`, `log` |
| `run_start` | `config_sha256` |
| `run_mode` | `mode` (`fresh` / `resume`) |
| `environment` | versions, GPU, `plum_dispatch` |
| `step_start` / `step_done` / `step_failed` | `step`, `seconds`, `error` (failed) |
| `resume` | `checkpoint`, `epoch`, `phase` |
| `epoch` | the epoch row (as in the CSV) |
| `checkpoint_saved` | `name`, `kind`, `sha256`, `bytes`, `epoch` |
| `checkpoint_quarantined` | `name`, `moved_to`, `reason` |
| `early_stop` | `epoch`, `monitor`, `wait` |
| `lr_find_complete` | `suggested_lr`, `suggest_func` |
| `run_complete` | `best_epoch`, `test_roc_auc`, `warnings`, `errors` |
| `run_failed` | `error`, `warnings`, `errors` |

## Warnings and errors

- Python warnings (`warnings.warn`, e.g. library deprecations) are routed into the session log via `logging.captureWarnings`.
- Every warning/error record is counted; counts appear in `run_complete` / `run_failed` and in `run_summary.json`.
- A failing pipeline step logs its traceback and a `step_failed` event, then re-raises as `PipelineStepError`. A failure outside a step is logged as `RUN FAILED`. Nothing is swallowed.

## What goes to Git

`kaggle_sync/sync_plan.example.yaml` lists the experiment's `logs/`, `metrics/`, `learning_curves/`, `predictions/`, `observations.md`, the checkpoint manifest JSON, and `07_Checkpoints/`. Before committing, `push-metadata` checks every staged file; if any is a binary type (`.pth`, `.pt`, `.pkl`, `.bin`, `.safetensors`, `.ckpt`, `.zip`, `.npy`, `.npz`) or larger than 20 MB, it unstages them all and fails without committing.
