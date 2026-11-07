# Checkpoint Policy

**Step:** STEP-037  
**Handbook:** Phase M7 (Checkpoint Management); §10 Phase 8 (Checkpoint Recovery); Checklist 7; A.2 naming; A.6 storage tiers  
**Implementation:** `17_Automation/training/checkpoints.py`, `callbacks.py` (`EpochCheckpointer`), `pipeline.py` (`run_experiment`)

## Purpose

Kaggle sessions end without warning. Every experiment must be recoverable from its last completed epoch, with nothing ever overwritten and every file verifiable by checksum.

## What is saved

| File (A.2) | Kind | When | Contents |
|------------|------|------|----------|
| `EXPxxxx_epoch_NNN.pth` | recovery | after every epoch (`NNN` = run-wide epoch across frozen + unfrozen phases) | full training state (below) |
| `EXPxxxx_best.pth` | best | once, after training | byte-identical copy of the recovery checkpoint with the best `save_model.monitor` value |
| `EXPxxxx_last.pth` | last | once, after training | byte-identical copy of the final recovery checkpoint |
| `MODELxxxx_export.pkl` | export_pkl | once, after training | FastAI `learn.export` of the best weights (inference) |
| `MODELxxxx_weights.pth` | weights_pth | once, after training | plain PyTorch `state_dict` of the best weights |

**Full training state** in every recovery checkpoint:
- model weights and optimizer state (FastAI `Optimizer.state_dict`, including Adam moments);
- scheduler state: phase, epoch within the phase, phase length, and the schedule parameters (`lr`, `lr_mult`, `pct_start`, `div`, frozen-phase constants). The one-cycle schedule is a pure function of these, so resuming with `fit_one_cycle(start_epoch=…)` reproduces it exactly;
- run-wide epoch number;
- random state: Python, NumPy, PyTorch CPU, and every CUDA device;
- experiment state: best-model tracking, early-stopping counter, completion flags, and the learning-curve history so far;
- format version, experiment ID, and the SHA-256 of `config.yaml`.

## Frequency

Every epoch (`fastai.callbacks.save_model.every_epoch: true` and `with_opt: true` are required; the pipeline refuses to run otherwise). An interruption loses at most the epoch in progress.

## Never overwrite

- Each file is written to `<name>.partial` and atomically renamed. A crash mid-write leaves only a `.partial` file, never a truncated checkpoint under its real name.
- If a file with the target name already exists, the save fails with an error.
- Damaged files are moved to `quarantine/<name>.<timestamp>` and marked `quarantined` in the manifest. Nothing is deleted.
- Leftover `.partial` files are quarantined the next time that name is written.

## Manifests and checksums

- `checkpoint_manifest.json` lives next to the binaries (it travels with them to the artifact tier) and lists every file: name, kind, epoch, phase, monitor value, SHA-256, size, creation time, status.
- `07_Checkpoints/EXPxxxx_checkpoints.md` is generated from it after every write and is the Git-side record.
- Before finalizing, every valid entry is re-verified against its SHA-256; any mismatch fails the run.

## Resume policy

`run_experiment(config.yaml)` resumes automatically when the manifest contains recovery checkpoints (`resume=False` makes it refuse instead):

1. Refuse if `run_summary.json` exists (the experiment is complete), or if post-training outputs from an incomplete attempt are present (move them aside first).
2. Refuse if `config.yaml` differs from the config hash in the manifest; the config is immutable after launch, and a changed run needs a new `EXP` ID.
3. Take the newest recovery checkpoint whose SHA-256 verifies. Corrupt or unreadable ones are quarantined, and the next older one is tried.
4. Restore the freeze state, weights, optimizer, and callback state; restore the RNG state right before training resumes.
5. Continue at the next epoch, in the same phase (`start_epoch`) or at the start of the next phase. If the checkpoint marks training as complete, go straight to finalize/export/metrics.

The resumed run follows the same LR/momentum schedule as an uninterrupted run (tested batch by batch). It is not bit-identical: the DataLoader shuffle order after resume and the mixed-precision `GradScaler` (re-initialized per fit) can differ.

## Early stopping

Configured by `fastai.callbacks.early_stopping` and active only in the unfrozen phase. The counter lives in the checkpoint state, so a resume continues it instead of resetting. The epoch that triggers the stop is checkpointed before training stops.

## Storage and retention

- Binaries stay in `outputs.checkpoint_dir` during the session (`*.pth` / `*.pkl` are Git-ignored) and are published to the artifact tier (`outputs.artifact_dataset_slug`) with `python -m kaggle_sync publish-artifacts`. A later session mounts them and copies them back with `resume-checkpoints`.
- Git holds only `checkpoint_manifest.json`'s Markdown rendering in `07_Checkpoints/` (pushed by `push-metadata`).
- Retention: every recovery checkpoint is kept for the life of the experiment. Size per checkpoint is roughly 3× the model weights with Adam (ResNet-50 ≈ 0.3 GB, so 11 epochs ≈ 3.3 GB, within Kaggle's 20 GB working limit).

## Failure handling

| Situation | Behaviour |
|-----------|-----------|
| Session ends mid-epoch | Resume from the last completed epoch |
| Session ends during a checkpoint write | Only `.partial` exists; resume from the previous epoch |
| Latest checkpoint corrupt (checksum mismatch) | Quarantined; resume from the previous valid one and re-run the lost epoch under the freed name |
| Config edited after launch | Refused; create a new `EXP` ID |
| Run completed | Refused; outputs are final |
| A checkpoint was overwritten (should be impossible) | Treat prior state as lost, write a `failure_report.md` (Template 9), fix the code |
