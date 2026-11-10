# EXP0002 — Kaggle Runbook (STEP-047, Part 2)

**Notebook:** `06_Experiments/EXP0002/notebook/EXP0002_train.ipynb` (thin caller)  
**What it does:** trains MODEL0008 exactly like EXP0001 but on `SPLIT0002` (no Stable Diffusion in train or val), exports it, and writes val/test predictions.

## One-time preparation

1. Import the notebook: *Kaggle → Create → New Notebook → File → Import Notebook*, paste the GitHub URL of `EXP0002_train.ipynb` on `main`.
2. Notebook settings: *Accelerator* `GPU T4 x2`, *Internet* `On`, *Add Input* `isthisdeception/ds0001-pp0001`.
3. *Add-ons → Secrets*: tick `GITHUB_TOKEN`, `KAGGLE_USERNAME`, `KAGGLE_KEY` for this notebook (the same secrets as EXP0001).

## Session (about 1 hour)

1. Run **0 Setup** (five cells). Expect three `… loaded` lines, a GPU name, and `config PASS: …/EXP0002/config.yaml`.
2. Run **B**. The log shows `run mode: fresh`, one `checkpoint saved EXP0002_epoch_NNN.pth` per epoch, then validation and test metrics. Test ROC-AUC prints as `nan`: the test split has fake images only. That is expected.
3. Run **C** (publish). The first time, `dataset version failed … trying to create isthisdeception/thesis-exp0002-artifacts` is expected; the dataset is then created.
4. Run **D** (push). It prints `pushed metadata to branch kaggle/exp0002-<time>`. Send that branch name to the repository side.
5. Stop the session.

## If the session ends before training finishes

1. If possible, run **C** before it ends.
2. New session: attach `isthisdeception/thesis-exp0002-artifacts` as an extra input, run **0 Setup → R → B → C → D**.
3. If **C** could not run, the run restarts from scratch.

## After the push (repository side)

Register MODEL0008 and complete EXP0002 (as STEP-040), then run, from `17_Automation/`:

```text
python -m evaluation_trigger --experiment EXP0002 --positive-class fake --negative-class real
python -m prediction_validation --experiment EXP0002 --evaluation EVAL0002
python -m generalization unseen --experiment EXP0002 --evaluation EVAL0002
```
