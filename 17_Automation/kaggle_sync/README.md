# `kaggle_sync`

`STEP-031` automation for the canonical Kaggle workflow:

`Start session -> clone repo -> verify environment -> download dataset -> download checkpoints -> verify config -> resume/train -> evaluate -> export -> upload outputs -> push metadata -> shutdown`

## Files

- `sync_plan.example.yaml` — manifest describing repo URL, mounted Kaggle datasets, checkpoints, metadata paths, and artifact publish targets.
- `python -m kaggle_sync bootstrap` — clone/pull the repo on Kaggle, optionally install `environment/kaggle-requirements.txt`, and verify attached datasets.
- `python -m kaggle_sync resume-checkpoints` — copy checkpoint artifacts from mounted Kaggle inputs into the working repo.
- `python -m kaggle_sync publish-artifacts` — stage experiment outputs and publish them to a Kaggle Dataset (artifact tier).
- `python -m kaggle_sync push-metadata` — commit and push source-tier metadata only.

## Safety rules

- Secrets are never stored in the repository. Configure Kaggle/Git credentials through Kaggle Secrets or environment variables.
- Raw and processed image bytes remain in the data tier (`/kaggle/input/...` and Kaggle Datasets).
- Weights, checkpoints, `export.pkl`, and large predictions remain in the artifact tier.
- Only source-tier assets such as configs, registries, logs, and reports are allowed back into Git.

## Typical Kaggle usage

From the repository root inside a Kaggle notebook:

```bash
cd /kaggle/working/thesis/17_Automation
python -m kaggle_sync --plan kaggle_sync/sync_plan.example.yaml bootstrap
python -m kaggle_sync --plan kaggle_sync/sync_plan.example.yaml resume-checkpoints
python -m kaggle_sync --plan kaggle_sync/sync_plan.example.yaml publish-artifacts
python -m kaggle_sync --plan kaggle_sync/sync_plan.example.yaml push-metadata --branch kaggle/exp0001-<time>
```

- `bootstrap` installs `environment/kaggle-requirements.txt` (pins `plum-dispatch==2.5.7`) and fails only for mounts marked `required: true` (for EXP0001: `ds0001-pp0001`).
- `resume-checkpoints` merges mounted checkpoints into the repo; it never deletes and refuses to overwrite differing files.
- `publish-artifacts` versions the artifact dataset (creates it if versioning fails); needs `KAGGLE_USERNAME` / `KAGGLE_KEY`.
- `push-metadata --branch` commits only `metadata_paths`, refuses binaries / files > 20 MB, and pushes to the given branch using `GITHUB_TOKEN` (masked in any error output). Results reach `main` through a PR.

Per-experiment session order: `06_Experiments/EXP0001/KAGGLE_RUNBOOK.md`.

Robustness (STEP-046) uses `sync_plan.robustness.yaml`: both `ds0001-pp0001` and `thesis-experiment-artifacts` are required, and only `08_Evaluation/EVAL0001/robustness` returns to Git. Session order: `08_Evaluation/EVAL0001/robustness/KAGGLE_RUNBOOK.md`.

Use `--dry-run` while validating a new manifest.
