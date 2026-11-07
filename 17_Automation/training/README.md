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
| output guard | refuses to run if checkpoints, metrics, predictions, curves, or `logs/history.csv` already exist | any prior output (resume belongs to the checkpoint system; changed reruns need a new `EXP` ID) |
| git provenance | `git_commit` must be HEAD or an ancestor of HEAD | commit not in history (warning only if git is unavailable) |
| environment | logs versions + GPU, seeds (`set_seed(reproducible=True)`), checks transforms are picklable | `mixed_precision` without CUDA; `export.pkl` would be unpicklable |
| dataset validation | columns, partitions, labels ⊆ vocab, both classes in train/val, no content-hash overlap, every image file exists | any check; missing images report the count and, when possible, the correct `processed_root` |
| dataloaders / learner | DataBlock, `aug_transforms`, `Normalize`, `vision_learner` with configured loss, optimizer, weight decay, monitors | unknown backbone, loss, or optimizer |
| training | frozen phase (`freeze_epochs`), then unfrozen `fine_tune` or `fit_one_cycle` | — |
| learning curves | `learning_curves/epochs.csv` (per epoch, phase, time, GPU peak), `batches.csv` (loss + LR per iteration) | — |
| checkpoint save + export | `best_model.pth`, `last_checkpoint.pth`, `export.pkl`, `weights.pth` in `outputs.checkpoint_dir`, SHA-256 recorded | an expected artifact is missing |
| predictions + metrics | best model → `predictions/{val,test}_predictions.csv`; threshold chosen on validation only; `metrics/{val,test}_metrics.json`, `*_calibration.csv`, `threshold.json` | — |
| summary | `metrics/run_summary.json`: config hash, git provenance, timing, best epoch, metrics, artifacts, environment | — |

Per-epoch checkpoints (`epoch_000.pth`, …) are numbered across both phases and are never overwritten. Binaries are Git-ignored; they go to the artifact tier.

## Modules

| Module | FastAI needed | Role |
|--------|---------------|------|
| `settings.py` | no | load + validate config, resolve paths |
| `data.py` | DataLoaders only | assignments loading, dataset validation, DataBlock |
| `evaluation.py` | no | threshold selection, canonical metrics, ECE, calibration table |
| `learner.py` | yes | backbone (torchvision / timm), loss, optimizer, monitors |
| `callbacks.py` | yes | `EpochCheckpointer`, `HistoryTracker` |
| `pipeline.py` | yes (lazy) | `run_experiment`, `find_lr` |
| `logs.py` | no | run log file, timed steps, environment info |

## Environment note

`plum-dispatch` ≥ 2.6 makes FastAI transforms unpicklable, which breaks `learn.export`. `environment/requirements.txt` pins `plum-dispatch==2.5.7`, and the pipeline checks this before training starts.

## Tests

```
cd 17_Automation
python -m pytest tests/test_training_core.py -q        # no FastAI needed
python -m pytest tests/test_training_smoke.py -q       # needs torch/torchvision/fastai; skipped otherwise
```

The smoke test builds a throwaway repo with 32 synthetic 32-px images and runs the real pipeline: one frozen and one unfrozen epoch with `resnet18` trained from scratch on CPU, then the LR Finder.
