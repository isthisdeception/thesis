# EXP0001 — Checkpoint Info

**Status:** no checkpoints yet (training not started)

## Locations

| Item | Location |
|------|----------|
| Local checkpoint directory (Kaggle session) | `06_Experiments/EXP0001/notebook/checkpoints` |
| Machine manifest (travels with binaries) | `06_Experiments/EXP0001/notebook/checkpoints/checkpoint_manifest.json` |
| Git-side manifest + checksums | [`07_Checkpoints/EXP0001_checkpoints.md`](../../07_Checkpoints/EXP0001_checkpoints.md) |
| Resume input mount | `/kaggle/input/datasets/isthisdeception/thesis-experiment-artifacts/notebook/checkpoints` (`17_Automation/kaggle_sync/sync_plan.example.yaml`; unverified until the first Kaggle round trip) |
| Artifact tier (binaries) | Kaggle dataset `isthisdeception/thesis-experiment-artifacts` |

## Files this experiment will produce

- `EXP0001_epoch_000.pth` … one full-state recovery checkpoint per epoch (frozen epoch 0, then unfrozen epochs 1–10 unless early stopping triggers)
- `EXP0001_best.pth`, `EXP0001_last.pth`
- `MODEL0001_export.pkl`, `MODEL0001_weights.pth`

Policy, resume rules, and failure handling: [`07_Checkpoints/checkpoint_policy.md`](../../07_Checkpoints/checkpoint_policy.md).

## Resuming after a session ends

1. Publish the checkpoint folder before the session ends: `python -m kaggle_sync --plan … publish-artifacts`.
2. In the new session, attach the artifact dataset and run `resume-checkpoints`.
3. Run `run_experiment(CONFIG)` again; it resumes from the newest checksum-valid recovery checkpoint.
