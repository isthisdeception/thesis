# environment

**Purpose:** Dependency and environment definitions (Phase 16). Training must match the Kaggle GPU image.

## Contents
- `requirements.txt` — local/CI pins (`==` only)
- `environment.yml` — conda wrapper around those pins
- `kaggle-requirements.txt` — packages **missing** from the Kaggle base image (currently none)
- `versions.lock.md` — Python / FastAI / PyTorch / CUDA / Kaggle image + date

## Current lock
**Kaggle GPU v170** (2026-06-29): Python 3.12, `torch==2.10.0+cu128`, `torchvision==0.25.0`, `fastai==2.8.7`, CUDA 12.8. See `versions.lock.md`.

## Workflow
1. DevOps updates pins only when the Kaggle image changes (new lock section, never silent upgrade).
2. Local: `pip install -r environment/requirements.txt` (GPU: install torch from the cu128 index first — commands in `versions.lock.md`).
3. Kaggle: do **not** reinstall torch/fastai. Install `kaggle-requirements.txt` only if it lists packages.
4. Every experiment `config.yaml` copies versions + git commit from this lock (Phase M4).

## Smoke (Kaggle GPU)
See the Python block in `versions.lock.md`. Requires a T4 (not P100).

## Owner
DevOps Agent

## Related Folders
`05_Models`, `06_Experiments`

## Expected Outputs
`requirements.txt`, `environment.yml`, `kaggle-requirements.txt`, `versions.lock.md`

> *This folder follows the canonical repository hygiene and naming rules defined in `MASTER_RESEARCH_OPERATING_SYSTEM.md`. Please refer to the handbook for full policy details.*
