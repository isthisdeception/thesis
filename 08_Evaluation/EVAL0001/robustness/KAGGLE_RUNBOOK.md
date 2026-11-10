# STEP-046 — Robustness Kaggle Runbook

**Handbook:** Phase E7  
**Notebook:** `08_Evaluation/EVAL0001/robustness/STEP046_robustness.ipynb` (thin caller)  
**Config:** `08_Evaluation/EVAL0001/robustness/config.yaml` (54 conditions: clean + 53 perturbed, 7505 test images each)

## One-time preparation

1. Import the notebook: *Kaggle → Create → New Notebook → File → Import Notebook*, then paste the GitHub URL of `STEP046_robustness.ipynb` on `main` (or upload the file).
2. Notebook settings:
   - *Accelerator*: `GPU T4 x2`
   - *Internet*: `On`
   - *Add Input*: `isthisdeception/ds0001-pp0001` (processed images) and `isthisdeception/thesis-experiment-artifacts` (the MODEL0001 export).
3. *Add-ons → Secrets*: `GITHUB_TOKEN` (the same fine-grained token as EXP0001, *Contents: Read and write* on `isthisdeception/thesis`). Turn it on for this notebook.

## Session (one sitting, about 30–60 min)

1. Run **0 Setup** (four cells). Expect:
   - `GITHUB_TOKEN loaded`
   - bootstrap finishes without `required Kaggle input missing`
   - a GPU name and `54 conditions (config SHA-256 …)`
2. Run **A**. Expect, in order:
   - `export: /kaggle/input/.../MODEL0001_export.pkl`
   - `clean check PASS: max |diff| …, decision mismatches …`
   - one line per condition with seconds and mean P(fake)
3. Run **B**. It prints one row per perturbation.
4. Run **C**. It prints `pushed to kaggle/robustness-<time>`.
5. Tell the repository side the branch name. Stop the session.

## If something goes wrong

| Message | Meaning | What to do |
|---------|---------|------------|
| `required Kaggle input missing` | An input is not attached | Add the input named in the message, run 0 again |
| `MODEL0001_export.pkl not found` | Artifact dataset not attached | Add `isthisdeception/thesis-experiment-artifacts` |
| `none matches SHA-256` | A different export file | Stop and report; do not continue |
| `CleanCheckError` | Clean inference does not reproduce the saved predictions | Stop and report the full message; no perturbed results are kept |
| `no GPU visible` | Accelerator off | Set *Accelerator* to GPU, restart, run 0 again |
| Session interrupted during A | Finished conditions are saved in `/kaggle/working/robustness_work` | In the same session, run 0 and A again; finished conditions are skipped. A new session starts over |
| `push-metadata` authentication error | Token missing or expired | Fix the secret, rerun only C |

## What goes where

| Output | Location |
|--------|----------|
| `robustness_probs.csv`, `run_manifest.json` (inference) | `08_Evaluation/EVAL0001/robustness/` → pushed to Git |
| `robustness_metrics.csv`, `robustness_flips.csv`, `robustness_by_group.csv`, `robustness_summary.csv`, `robustness_report.md` | same folder → pushed to Git |
| Per-condition work files | `/kaggle/working/robustness_work/` (not pushed) |
| Perturbed images | never written to disk |
