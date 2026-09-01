# STEP-030 — Environment Definition & Version Lock

**Status:** COMPLETE (files locked 2026-09-01) — Kaggle smoke check still recommended before first `EXP`  
**Handbook:** §10 Phase 16; §1.4 stack

## Done
- [x] `environment/requirements.txt` (exact `==` pins)
- [x] `environment/environment.yml`
- [x] `environment/kaggle-requirements.txt` (no extras on v170)
- [x] `environment/versions.lock.md` (Python 3.12, torch 2.10.0+cu128, fastai 2.8.7, CUDA 12.8, Kaggle GPU **v170**)
- [x] `environment/README.md` updated

## Lock summary
| Item | Pin |
|------|-----|
| Kaggle image | `gcr.io/kaggle-private-byod/python:v170` (2026-06-29) |
| Python | 3.12 |
| PyTorch | 2.10.0 + CUDA 12.8 (`+cu128`) |
| torchvision | 0.25.0 |
| FastAI | 2.8.7 |
| fastcore | 1.12.42 |
| NumPy | 2.0.2 |

Use **T4**, not P100 (`cu128` dropped sm_60).

## Remaining (optional smoke)
Run the smoke cell in `versions.lock.md` on a Kaggle GPU session and paste stdout into the first experiment log. If versions differ, update the lock before training.

## Next step
**STEP-031** — Kaggle dataset upload & sync setup.
