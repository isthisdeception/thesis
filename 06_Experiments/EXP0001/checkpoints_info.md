# EXP0001 — Checkpoint Info

**Status:** no checkpoints yet (training not started)

## Locations

| Item | Location |
|------|----------|
| Local checkpoint directory (Kaggle session) | `06_Experiments/EXP0001/notebook/checkpoints` |
| Resume input mount | `/kaggle/input/exp0001-checkpoints` (from `17_Automation/kaggle_sync/sync_plan.example.yaml`) |
| Artifact tier (binaries) | Kaggle dataset `isthisdeception/thesis-experiment-artifacts` |
| Manifest + checksums | `07_Checkpoints/EXP0001_checkpoints.md` (created when the first checkpoint is saved) |

## Policy (Phase M7)

- `SaveModelCallback(every_epoch=True, with_opt=True)` saves every epoch with optimizer state, so a terminated session resumes from the last epoch.
- Captured state: model weights, optimizer state, scheduler state, epoch number, random state.
- Kept artifacts: best model (lowest `valid_loss`), last epoch, recovery checkpoint, FastAI `export.pkl`, PyTorch `weights.pth`.
- Nothing is overwritten. Binaries (`*.pth`, `*.pkl`) are Git-ignored and live only in the artifact tier; Git holds this file and the manifest.

## Checkpoints

| Kind | Epoch | File | SHA-256 | Artifact version |
|------|-------|------|---------|------------------|
| — | — | — | — | — |
