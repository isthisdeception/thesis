# STEP-048 — Ablation Kaggle Runbook

**Notebook:** `06_Experiments/ablations/STEP048_ablations.ipynb` (thin caller)  
**Plan:** `06_Experiments/ablations/STEP048_plan.yaml` (DEC0008)  
**Experiments:** EXP0003 (seed 43), EXP0004 (no augmentation), EXP0005 (no ImageNet pretraining), EXP0006 (image size 160)

## One-time preparation

1. Import the notebook: *Kaggle → Create → New Notebook → File → Import Notebook*, paste the GitHub URL of `STEP048_ablations.ipynb` on `main`.
2. Notebook settings: *Accelerator* `GPU T4 x2`, *Internet* `On`, *Add Input* `isthisdeception/ds0001-pp0001`.
3. *Add-ons → Secrets*: tick `GITHUB_TOKEN`, `KAGGLE_USERNAME`, `KAGGLE_KEY`.

## Session (about 2.5–3 hours, one sitting)

1. Run **0 Setup** (four cells). Expect three `… loaded` lines, a GPU name, four `PASS …/config.yaml` lines, and the `ablation list` table.
2. Run **A** and leave it. For each experiment it prints `== EXP000N: training`, the training log, `== EXP000N: pushing results`, `pushed metadata to branch kaggle/ablations-<time>`, `== EXP000N: publishing checkpoints`, then the upload log.
3. When it prints `ALL DONE. Results branch: kaggle/ablations-<time>`, send that branch name to the repository side.
4. Check *Your Work → Datasets*: `thesis-exp0003-artifacts` … `thesis-exp0006-artifacts`, each with `notebook/checkpoints/MODEL00NN_export.pkl`. Then stop the session.

## Expected messages that are not errors

| Message | Meaning |
|---------|---------|
| `403 Client Error … CreateDatasetVersion` then `trying to create …` | First publish of a new dataset |
| `KaggleObject.from_dict() got an unexpected keyword argument 'token'` | Old kaggle CLI cache bug; uploads still succeed |
| EXP0005 metrics well below EXP0001 | Training from scratch in 11 epochs; this is the result |

## If something goes wrong

| Situation | What to do |
|-----------|------------|
| A stops with `command failed … training` | Send the last 20 lines. Experiments already pushed are safe |
| A stops at publishing | Results are already pushed. Run A again: finished experiments are skipped, and the failed publish can be repeated by hand with the command printed in the error |
| The session ended part-way | New session: in the setup cell, remove the experiments already on the results branch from `RUN`, run 0 and A. Send both branch names |
