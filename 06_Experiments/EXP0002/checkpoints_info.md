# EXP0002 — Checkpoint Info

**Status:** not trained yet.

## Locations

| Item | Location |
|------|----------|
| Local checkpoint directory (Kaggle session) | `06_Experiments/EXP0002/notebook/checkpoints` |
| Machine manifest (travels with binaries) | `06_Experiments/EXP0002/notebook/checkpoints/checkpoint_manifest.json` |
| Git-side manifest + checksums | `07_Checkpoints/EXP0002_checkpoints.md` (written by the training pipeline) |
| Resume input mount | `/kaggle/input/datasets/isthisdeception/thesis-exp0002-artifacts/notebook/checkpoints` (`17_Automation/kaggle_sync/sync_plan.exp0002.yaml`) |
| Artifact tier (binaries) | Kaggle dataset `isthisdeception/thesis-exp0002-artifacts` (created by the first publish) |

## Files this experiment will produce

- `EXP0002_epoch_000.pth` … one full-state recovery checkpoint per epoch
- `EXP0002_best.pth`, `EXP0002_last.pth`
- `MODEL0008_export.pkl`, `MODEL0008_weights.pth`

Policy and resume rules: [`07_Checkpoints/checkpoint_policy.md`](../../07_Checkpoints/checkpoint_policy.md).
