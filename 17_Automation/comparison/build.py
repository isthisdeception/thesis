"""Phase E16 comparison of experiments that keep the baseline data invariants.

A labeled one-factor ablation stays in the table. A different split does not.
Numbers are copied from the STEP-048 comparison and the STEP-049 tests. Nothing is rescored.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

from ablation.plan import get, load_plan

PLAN = Path("06_Experiments/ablations/STEP048_plan.yaml")
INVARIANT_KEYS = ("dataset.dataset_id", "dataset.version", "dataset.pipeline_id", "split.split_id")
METRIC_COLUMNS = [
    "roc_auc", "pr_auc", "balanced_accuracy", "mcc", "f1", "recall", "specificity", "fnr", "fpr",
    "accuracy", "ece", "brier",
]


def invariants(repo: Path, experiment_id: str) -> dict[str, str]:
    config = yaml.safe_load((repo / "06_Experiments" / experiment_id / "config.yaml").read_text(encoding="utf-8"))
    return {key: str(get(config, key)) for key in INVARIANT_KEYS}


def _completed_experiments(repo: Path) -> list[str]:
    return sorted(path.parent.name for path in (repo / "06_Experiments").glob("EXP*/config.yaml"))


def comparison_frame(repo: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    plan = load_plan(repo / PLAN)
    baseline = invariants(repo, plan.baseline)
    allowed = [plan.baseline, *[a.experiment_id for a in plan.ablations]]
    for experiment_id in allowed:
        found = invariants(repo, experiment_id)
        if found != baseline:
            raise ValueError(f"{experiment_id} breaks a data invariant: {found} vs {baseline}")

    results = pd.read_csv(repo / "08_Evaluation/ablations/ablation_results.csv")
    if set(results["experiment_id"]) != set(allowed):
        raise ValueError("ablation_results.csv is not exactly the fairness-compatible set")
    paired = pd.read_csv(repo / "08_Evaluation/statistics/paired_tests.csv")
    primary = paired[(paired["metric"] == "roc_auc") & (paired["primary"])]
    if set(primary["superiority_claim"]) != {"none"}:
        raise ValueError("a paired test carries a superiority claim")

    rows = []
    for record in results.to_dict(orient="records"):
        experiment_id = record["experiment_id"]
        stats = primary[primary["challenger_id"] == experiment_id]
        if experiment_id == plan.baseline:
            difference, ci_low, ci_high, level = "", float("nan"), float("nan"), float("nan")
        elif len(stats) != 1:
            raise ValueError(f"{experiment_id} has {len(stats)} primary paired tests")
        else:
            one = stats.iloc[0]
            difference, ci_low, ci_high, level = one.run_difference, one.claim_ci_low, one.claim_ci_high, one.claim_ci_level
        role = "baseline" if experiment_id == plan.baseline else ("seed_replicate" if experiment_id == plan.noise_reference else "ablation")
        rows.append({
            "experiment_id": experiment_id,
            "model_id": record["model_id"],
            "factor": record["factor"],
            "role": role,
            "fairness_compatible": True,
            "ranked": True,
            **{key.split(".")[-1]: baseline[key] for key in INVARIANT_KEYS},
            "threshold": record["threshold"],
            **{metric: record[metric] for metric in METRIC_COLUMNS},
            "delta_roc_auc": record["delta_roc_auc"],
            "roc_auc_run_difference": difference,
            "roc_auc_claim_ci_low": ci_low,
            "roc_auc_claim_ci_high": ci_high,
            "roc_auc_claim_ci_level": level,
            "superiority_claim": "none",
        })
    ranked = pd.DataFrame(rows)

    excluded = []
    for experiment_id in _completed_experiments(repo):
        if experiment_id in allowed:
            continue
        found = invariants(repo, experiment_id)
        changed = [key for key in INVARIANT_KEYS if found[key] != baseline[key]]
        excluded.append({
            "experiment_id": experiment_id,
            "ranked": False,
            "reason": "different " + ", ".join(key.split(".")[-1] for key in changed) if changed else "not in the fair comparison set",
            **{f"found_{key.split('.')[-1]}": found[key] for key in INVARIANT_KEYS},
        })
    if not excluded:
        raise ValueError("no excluded experiment; the split check has nothing to refuse")
    return ranked, pd.DataFrame(excluded)
