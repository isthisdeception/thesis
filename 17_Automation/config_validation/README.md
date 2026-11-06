# config_validation (STEP-034, Phase M4)

Validates an experiment `config.yaml` before training. Every failure is reported with an explicit message; there is no silent pass.

## Usage

Run from `17_Automation/`:

```
python -m config_validation ../06_Experiments/EXP0001/config.yaml
python -m config_validation ../18_Templates/config.yaml --template
```

Exit code is `0` when every file passes and `1` otherwise. `--repo-root` overrides auto-detection (the folder containing `MASTER_RESEARCH_OPERATING_SYSTEM.md`).

From Python:

```python
from config_validation import validate_config_file

validate_config_file("06_Experiments/EXP0001/config.yaml").raise_if_failed()
```

## Modes

- **Ready (default):** for `06_Experiments/EXPxxxx/config.yaml`. Requires a real `EXP####` ID, a hex `git_commit`, and a timezone-aware ISO-8601 `timestamp`.
- **Template (`--template`):** for `18_Templates/config.yaml`. Allows `EXPxxxx` and unset `git_commit` / `timestamp`; every other check still runs.

## Checks

| Area | Fails when |
|------|-----------|
| Structure | `schema_version` is not 1; any M4 section or required nested field is missing |
| IDs | `EXP`, `DS`, `PP`, `SPLIT`, `MODEL` IDs don't match their patterns; `output_id` ≠ `DS_PP`; `assignments_csv` path doesn't match the output and split |
| Dataset registry | Dataset ID, version, or the DS/version/PP/split combination is not in `dataset_registry.csv` or not `ready` |
| Preprocessing registry | Pipeline ID is missing, not `complete` (e.g. superseded PP0004), or belongs to another dataset |
| Split registry | Split/output pair is missing, leakage is not `PASS`, or the scheme differs; `assignments.csv` is missing on disk |
| Model | Model ID is in neither `model_registry.csv` nor `candidate_models.csv`; architecture differs from the registry |
| Seed | `random_seed` is unset, not an integer, or negative |
| Training values | `image_size`, `batch_size`, `epochs` not positive integers; `fastai.item_tfms.resize` ≠ `image_size`; LR not a positive number (string `1e-3` gets a hint to write `1.0e-3`); unknown schedule, LR source, model source, or study track |
| Metrics | Any canonical primary metric from `05_Models/baseline_plan.md` is missing; threshold policy is not `validation_only` |
| Outputs | `experiment_dir` is not `06_Experiments/<experiment_id>`; `checkpoint_dir` is not scoped to the experiment |

## Tests

```
cd 17_Automation
python -m pytest tests/test_config_validation.py -q
```

The tests run against the real registries and assert that the shipped template passes in template mode.
