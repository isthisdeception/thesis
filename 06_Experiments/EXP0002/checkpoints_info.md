# EXP0002 — Checkpoint Info

**Status:** exported 2026-11-10. Best epoch 9. Checksums: [`../../07_Checkpoints/EXP0002_checkpoints.md`](../../07_Checkpoints/EXP0002_checkpoints.md). Binaries: Kaggle dataset `isthisdeception/thesis-exp0002-artifacts` (created by the first publish; `notebook/checkpoints/MODEL0008_export.pkl` confirmed present on Kaggle, 2026-11-10).

## Locations

| Item | Location |
|------|----------|
| Local checkpoint directory (Kaggle session) | `06_Experiments/EXP0002/notebook/checkpoints` |
| Machine manifest (travels with binaries) | `06_Experiments/EXP0002/notebook/checkpoints/checkpoint_manifest.json` |
| Git-side manifest + checksums | [`07_Checkpoints/EXP0002_checkpoints.md`](../../07_Checkpoints/EXP0002_checkpoints.md) |
| Resume input mount | `/kaggle/input/datasets/isthisdeception/thesis-exp0002-artifacts/notebook/checkpoints` (`17_Automation/kaggle_sync/sync_plan.exp0002.yaml`) |
| Artifact tier (binaries) | Kaggle dataset `isthisdeception/thesis-exp0002-artifacts` |

## Files produced

- `EXP0002_epoch_000.pth` … `EXP0002_epoch_010.pth` (recovery, one per epoch)
- `EXP0002_best.pth` (epoch 9), `EXP0002_last.pth` (epoch 10)
- `MODEL0008_export.pkl` (SHA-256 `d076875658a8…`), `MODEL0008_weights.pth`

Policy and resume rules: [`07_Checkpoints/checkpoint_policy.md`](../../07_Checkpoints/checkpoint_policy.md).
