# EXP0005 — Observations

## 2026-11-13 — Readiness (STEP-048)

- Generated from `EXP0001/config.yaml` by `python -m ablation create`; the one-factor check passed (only identity fields and `model.pretrained`, `model.pretrained_weights` differ).
- `learning_rate.source: manual`: EXP0001's LR Finder value is reused unchanged so that pretraining is the only training difference.
