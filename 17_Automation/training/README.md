# training (STEP-036, Phase M6)

Config-driven FastAI training pipeline. A Kaggle notebook calls it with one `config.yaml`; every parameter comes from that file, and the notebook holds no logic (see `06_Experiments/EXP0001/notebook/EXP0001_train.ipynb`). The workflow it implements is documented in `05_Models/FASTAI_TRAINING_STANDARD.md`.

## Usage

```python
import sys; sys.path.insert(0, "/kaggle/working/thesis/17_Automation")
from training import find_lr, run_experiment

find_lr("/kaggle/working/thesis/06_Experiments/EXP0001/config.yaml")         # once, before training
summary = run_experiment("/kaggle/working/thesis/06_Experiments/EXP0001/config.yaml")
```

CLI from `17_Automation/`: `python -m training lr-find --config ../06_Experiments/EXP0001/config.yaml`, then `python -m training train --config ...`.

## Run steps (each logged with start, duration, and failure)

| Step | What happens | Fails when |
|------|--------------|-----------|
| config validation | `config_validation` in ready mode, including registry checks | any validator error; config not inside its `outputs.experiment_dir` |
| output guard | chooses **fresh** or **resume**: resumes when the checkpoint manifest has recovery checkpoints | run already complete; partial post-training outputs; unmanifested files in the checkpoint folder; config changed since the checkpoints were written |
| git provenance | `git_commit` must be HEAD or an ancestor of HEAD | commit not in history (warning only if git is unavailable) |
| environment | logs versions + GPU, seeds (`set_seed(reproducible=True)`), checks transforms are picklable | `mixed_precision` without CUDA; `export.pkl` would be unpicklable |
| dataset validation | columns, partitions, labels ⊆ vocab, both classes in train/val, no content-hash overlap, every image file exists | any check; missing images report the count and, when possible, the correct `processed_root` |
| dataloaders / learner | DataBlock, `aug_transforms`, `Normalize`, `vision_learner` with configured loss, optimizer, weight decay, monitors | unknown backbone, loss, or optimizer |
| resume (resume mode only) | newest checksum-valid recovery checkpoint → weights, optimizer, freeze state, callback state, RNG | no recovery checkpoint verifies (corrupt ones are quarantined) |
| training | frozen phase (`freeze_epochs`), then unfrozen `fine_tune` or `fit_one_cycle`; a full-state recovery checkpoint after every epoch; resumed runs continue with `start_epoch` | a checkpoint name already exists |
| learning curves | `learning_curves/epochs.csv` (per epoch, phase, time, GPU peak), `batches.csv` (loss + LR per iteration) | — |
| checkpoint finalize + export | `EXPxxxx_best.pth`, `EXPxxxx_last.pth` (copies of recovery checkpoints), best weights loaded, `MODELxxxx_export.pkl`, `MODELxxxx_weights.pth`; every manifest entry re-verified | a checksum fails or an artifact is missing |
| predictions + metrics | best model → `predictions/{val,test}_predictions.csv`; threshold chosen on validation only; `metrics/{val,test}_metrics.json`, `*_calibration.csv`, `threshold.json` | — |
| summary | `metrics/run_summary.json`: config hash, git provenance, sessions, timing, best epoch, metrics, artifacts, environment, log files, warning/error counts | — |

Throughout the run, each epoch is appended to `logs/EXPxxxx_epochs.csv` / `EXPxxxx_batches.csv`, and events go to `logs/EXPxxxx_events.jsonl` (see `LOGGING.md`).

Checkpointing follows `07_Checkpoints/checkpoint_policy.md`: recovery checkpoints `EXPxxxx_epoch_NNN.pth` are numbered across both phases, written atomically, listed with SHA-256 in `checkpoint_manifest.json` and `07_Checkpoints/EXPxxxx_checkpoints.md`, and never overwritten. Binaries are Git-ignored; they go to the artifact tier. After a session ends, call `run_experiment(config)` again in a new session and it resumes.

## Modules

| Module | FastAI needed | Role |
|--------|---------------|------|
| `settings.py` | no | load + validate config, resolve paths |
| `data.py` | DataLoaders only | assignments loading, dataset validation, DataBlock |
| `evaluation.py` | no | threshold selection, canonical metrics, ECE, calibration table |
| `learner.py` | yes | backbone (torchvision / timm), loss, optimizer, monitors |
| `checkpoints.py` | torch for save/load | `CheckpointStore` (never-overwrite writes, manifest, checksums, quarantine, resume lookup), RNG capture/restore |
| `callbacks.py` | yes | `EpochCheckpointer` (recovery checkpoints, best tracking, resumable early stopping), `HistoryTracker` |
| `pipeline.py` | yes (lazy) | `run_experiment`, `find_lr` |
| `logs.py` | no | session log file, append-only event log, warning capture + counts, timed steps, environment info |
| `records.py` | no | fixed CSV schemas, append-only writers |

Logging outputs and CSV schemas: [`LOGGING.md`](LOGGING.md).

## Environment note

`plum-dispatch` ≥ 2.6 makes FastAI transforms unpicklable, which breaks `learn.export`. `environment/requirements.txt` pins `plum-dispatch==2.5.7`, and the pipeline checks this before training starts.

## Tests

```
cd 17_Automation
python -m pytest tests/test_training_core.py -q        # no FastAI needed
python -m pytest tests/test_training_smoke.py -q       # needs torch/torchvision/fastai; skipped otherwise
```

The smoke tests build a throwaway repo with 32 synthetic 32-px images and run the real pipeline with `resnet18` trained from scratch on CPU: an uninterrupted run, a simulated session termination followed by a resume (existing checkpoints byte-identical afterwards, LR schedule identical to an uninterrupted run batch by batch), a corrupt latest checkpoint (quarantined, previous one used), a config change after launch (refused), and the LR Finder.
