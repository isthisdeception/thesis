# EXP0004 — Observations

## 2026-11-13 — Readiness (STEP-048)

- Generated from `EXP0001/config.yaml` by `python -m ablation create`; the one-factor check passed (only identity fields and `augmentations.aug_transforms.enabled` differ).
- `learning_rate.source: manual`: EXP0001's LR Finder value is reused unchanged so that augmentation is the only training difference.
