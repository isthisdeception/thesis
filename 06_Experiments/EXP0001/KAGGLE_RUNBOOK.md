# EXP0001 — Kaggle Runbook (STEP-039)

**Handbook:** Phase M8; §10 Phases 7–8; O5 Experiment Day; Checklist 7  
**Notebook:** `06_Experiments/EXP0001/notebook/EXP0001_train.ipynb` (thin caller; cell labels below refer to its sections)

## One-time preparation

1. Kaggle account `isthisdeception` with a verified phone number (required for GPU and Internet).
2. Secrets (only needed for publishing and pushing, sections C and D): in the notebook, *Add-ons → Secrets*:
   - `KAGGLE_USERNAME`, `KAGGLE_KEY`: from *Kaggle → Settings → API → Create New Token* (`kaggle.json`).
   - `GITHUB_TOKEN`: GitHub fine-grained personal access token, repository `isthisdeception/thesis` only, permission *Contents: Read and write*.
3. Import the notebook: *Kaggle → Create → New Notebook → File → Import Notebook*, then paste the GitHub URL of `EXP0001_train.ipynb` on `main` (or upload the file).
4. Notebook settings: *Accelerator* `GPU T4 x2`, *Internet* `On`, *Add Input* `isthisdeception/ds0001-pp0001`.

## Session A — LR Finder (~10–15 min)

1. Run **0 Setup** (clone, secrets, bootstrap, environment check, config validation).
2. Run **A**. Record `suggested_lr`.
3. Report: the printed `suggested_lr`, and the environment-check output (versions, `plum-dispatch`, GPU). The session can then be stopped.

Between sessions (repository side, not on Kaggle): write `suggested_lr` into `config.yaml` (`learning_rate.value`, `source: lr_find`), refresh `git_commit` (current `main`) and `timestamp`, validate, merge to `main`, and log the change in `observations.md`. The config is frozen from Session B on.

## Session B — Training (~1 h; GPU-bound)

1. Run **0 Setup** (pulls the updated config).
2. Run **B**. Watch the log:
   - `run mode: fresh`, then one `checkpoint saved EXP0001_epoch_NNN.pth` per epoch.
3. **Interruption check (Checklist 7, once):** after `checkpoint saved EXP0001_epoch_002.pth`, press *Interrupt* (■). Run **B** again. The log must show `run mode: resume` and `resumed from EXP0001_epoch_00N.pth`, and training continues from the next epoch.
4. Let **B** finish. It prints `resumed_from_epoch`, `best_epoch`, and test metrics.
5. Run **C** (publish checkpoints and exports to `isthisdeception/thesis-experiment-artifacts`).
6. Run **D** (push logs, metrics, curves, predictions, manifests to a `kaggle/exp0001-<time>` branch).
7. Stop the session.

## If the session ends before training finishes

1. If possible, run **C** before the session ends. Checkpoints in `/kaggle/working` are lost when the session stops.
2. New session: attach `isthisdeception/thesis-experiment-artifacts` as an extra input, run **0 Setup → R → B → C → D**.
3. If **C** could not run, the run restarts from scratch: the checkpoint folder is empty, so `run mode: fresh`.

## What goes where

| Tier | Contents |
|------|----------|
| Git (via **D**, then PR) | `logs/` (session logs, `EXP0001_events.jsonl`, live epoch/batch CSVs, hyperparameter JSON), `metrics/`, `learning_curves/`, `predictions/`, `observations.md`, `checkpoint_manifest.json`, `07_Checkpoints/EXP0001_checkpoints.md` |
| Artifact tier (via **C**) | `EXP0001_epoch_*.pth`, `EXP0001_best.pth`, `EXP0001_last.pth`, `MODEL0001_export.pkl`, `MODEL0001_weights.pth` |
| Data tier (read-only input) | `isthisdeception/ds0001-pp0001` |

`push-metadata` refuses binaries and files over 20 MB.

## Stop and report instead of improvising

- Setup fails: dataset not found, wrong `processed_root` (the error suggests the right path), GPU missing, `plum-dispatch` check fails.
- Validation or git-provenance failure.
- Loss is NaN, or validation loss rises from the first unfrozen epoch.
- Any `checkpoint_quarantined` or `CheckpointError` in the log.
- Test ROC-AUC < 0.90 (DEC0006: investigate before comparator runs).

## After the session (repository side)

Review the `kaggle/…` branch, merge it, update `observations.md`, and set `experiment_registry.csv` `Status=trained` (STEP-040 handles registration and Checklist 6).
