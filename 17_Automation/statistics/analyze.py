"""STEP-049 on the STEP-048 experiments: intervals, McNemar, seed variance, repeatability.

Comparisons come from the ablation plan. EXP0002 is a different split and is not included.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from ablation.plan import AblationPlan, load_plan
from classification_metrics.compute import require_validated

from .core import (
    ALPHA,
    BOOT_SEED,
    HIGHER_IS_BETTER,
    METRICS,
    MIN_WILCOXON_N,
    N_BOOT_DEFAULT,
    PRIMARY_METRIC,
    adjust_p,
    bootstrap_intervals,
    mcnemar,
    metric_value,
    paired_bootstrap,
    run_difference,
)

PLAN = Path("06_Experiments/ablations/STEP048_plan.yaml")
SPLIT = "test"


def _registry_evaluation(repo: Path, experiment_id: str) -> str:
    path = repo / "08_Evaluation/evaluation_registry.csv"
    rows = list(csv.reader(path.open(encoding="utf-8", newline="")))
    head = [h.strip() for h in rows[0]]
    hits = [r[head.index("Evaluation ID")].strip() for r in rows[1:] if r and r[head.index("Experiment")].strip() == experiment_id]
    if len(hits) != 1:
        raise ValueError(f"{experiment_id} has {len(hits)} evaluation rows; expected one")
    return hits[0]


def _checked_predictions(repo: Path, experiment_id: str, evaluation_id: str) -> pd.DataFrame:
    require_validated(repo / "08_Evaluation" / evaluation_id / "prediction_validation_report.md")
    frame = pd.read_csv(repo / "08_Evaluation" / experiment_id / "predictions.csv")
    part = frame[frame["split"] == SPLIT][["id", "y_true", "y_prob", "y_pred", "threshold"]].copy()
    if part.empty:
        raise ValueError(f"{experiment_id} has no {SPLIT} predictions")
    if part["id"].duplicated().any():
        raise ValueError(f"{experiment_id} has duplicate {SPLIT} ids")
    if part["threshold"].nunique() != 1:
        raise ValueError(f"{experiment_id} {SPLIT} has more than one threshold")
    return part


def _align(baseline: pd.DataFrame, other: pd.DataFrame, experiment_id: str) -> pd.DataFrame:
    merged = baseline.merge(other, on="id", suffixes=("_a", "_b"), validate="one_to_one")
    if len(merged) != len(baseline):
        raise ValueError(f"{experiment_id} does not cover every baseline {SPLIT} id")
    if not np.array_equal(merged["y_true_a"].to_numpy(), merged["y_true_b"].to_numpy()):
        raise ValueError(f"{experiment_id} labels disagree with the baseline on {SPLIT}")
    return merged


def _levels(family: int) -> tuple[float, float]:
    return (1.0 - ALPHA, 1.0 - ALPHA / family)


def run(repo: Path, plan: AblationPlan | None = None, *, n_boot: int = N_BOOT_DEFAULT, seed: int = BOOT_SEED) -> dict[str, pd.DataFrame]:
    plan = plan or load_plan(repo / PLAN)
    family = sum(1 for a in plan.ablations if a.experiment_id != plan.noise_reference)
    if family < 1:
        raise ValueError("the plan has no factor comparison to adjust for")
    descriptive, claim_level = _levels(family)
    rng = np.random.default_rng(seed)

    ids = [(plan.baseline, _registry_evaluation(repo, plan.baseline), "baseline")]
    ids += [(a.experiment_id, a.evaluation_id, a.factor) for a in plan.ablations]
    loaded = {exp: _checked_predictions(repo, exp, ev) for exp, ev, _ in ids}
    factors = {exp: factor for exp, _, factor in ids}
    questions = {a.experiment_id: a.question for a in plan.ablations}

    marginal_rows = []
    estimates: dict[tuple[str, str], float] = {}
    for exp, _, factor in ids:
        frame = loaded[exp]
        y, prob, pred = frame["y_true"].to_numpy(), frame["y_prob"].to_numpy(), frame["y_pred"].to_numpy()
        intervals = bootstrap_intervals(y, prob, pred, n_boot=n_boot, rng=rng, levels=(descriptive,))
        for metric in METRICS:
            low, high = intervals[metric][descriptive]
            estimates[(exp, metric)] = intervals[metric]["estimate"]
            marginal_rows.append({
                "experiment_id": exp,
                "factor": factor,
                "split": SPLIT,
                "metric": metric,
                "n": int(y.size),
                "estimate": intervals[metric]["estimate"],
                "ci_level": descriptive,
                "ci_low": low,
                "ci_high": high,
                "n_bootstrap": n_boot,
                "bootstrap_seed": seed,
                "higher_is_better": HIGHER_IS_BETTER[metric],
            })

    paired_rows = []
    mcnemar_rows = []
    for ablation in plan.ablations:
        role = "seed_replicate" if ablation.experiment_id == plan.noise_reference else "ablation"
        level = descriptive if role == "seed_replicate" else claim_level
        merged = _align(loaded[plan.baseline], loaded[ablation.experiment_id], ablation.experiment_id)
        y = merged["y_true_a"].to_numpy()
        intervals = paired_bootstrap(
            y,
            merged["y_prob_a"].to_numpy(),
            merged["y_pred_a"].to_numpy(),
            merged["y_prob_b"].to_numpy(),
            merged["y_pred_b"].to_numpy(),
            n_boot=n_boot,
            rng=rng,
            levels=(descriptive, level) if level != descriptive else (descriptive,),
        )
        table = mcnemar(y, merged["y_pred_a"].to_numpy(), merged["y_pred_b"].to_numpy())
        p_adjusted = table["p_exact"] if role == "seed_replicate" else adjust_p(table["p_exact"], family)
        mcnemar_rows.append({
            "baseline_id": plan.baseline,
            "challenger_id": ablation.experiment_id,
            "factor": ablation.factor,
            "role": role,
            "question": ablation.question,
            "n": table["n"],
            "n_agree": table["n_agree"],
            "b_baseline_only_correct": table["b_a_only_correct"],
            "c_challenger_only_correct": table["c_b_only_correct"],
            "accuracy_delta": table["accuracy_delta"],
            "discordant_odds_ratio": table["discordant_odds_ratio"],
            "p_exact": table["p_exact"],
            "p_adjusted": p_adjusted,
            "alpha": ALPHA,
            "family_size": 1 if role == "seed_replicate" else family,
            "adjustment": "none" if role == "seed_replicate" else f"bonferroni x{family}",
            "decisions_differ": bool(p_adjusted < ALPHA),
            "superiority_claim": "none",
        })
        for metric in METRICS:
            low, high = intervals[metric][descriptive]
            claim_low, claim_high = intervals[metric][level]
            seed_abs = abs(estimates[(plan.noise_reference, metric)] - estimates[(plan.baseline, metric)])
            paired_rows.append({
                "baseline_id": plan.baseline,
                "challenger_id": ablation.experiment_id,
                "factor": ablation.factor,
                "role": role,
                "metric": metric,
                "primary": metric == PRIMARY_METRIC,
                "n": int(y.size),
                "estimate_baseline": estimates[(plan.baseline, metric)],
                "estimate_challenger": estimates[(ablation.experiment_id, metric)],
                "delta": intervals[metric]["delta"],
                "ci_level": descriptive,
                "ci_low": low,
                "ci_high": high,
                "claim_ci_level": level,
                "claim_ci_low": claim_low,
                "claim_ci_high": claim_high,
                "run_difference": run_difference(claim_low, claim_high),
                "seed_pair_abs_delta": seed_abs,
                "larger_than_seed_pair": abs(intervals[metric]["delta"]) > seed_abs,
                "n_bootstrap": n_boot,
                "bootstrap_seed": seed,
                "superiority_claim": "none",
            })

    seed_rows = []
    for metric in METRICS:
        a = estimates[(plan.baseline, metric)]
        b = estimates[(plan.noise_reference, metric)]
        seed_rows.append({
            "metric": metric,
            "experiment_a": plan.baseline,
            "experiment_b": plan.noise_reference,
            "value_a": a,
            "value_b": b,
            "mean": (a + b) / 2.0,
            "abs_diff": abs(b - a),
            "sample_sd": abs(b - a) / np.sqrt(2.0),
            "n_seeds": 2,
            "wilcoxon_status": "not_run",
            "wilcoxon_minimum_n": MIN_WILCOXON_N,
            "wilcoxon_reason": (
                f"Two seeds are two observations. A two-sided signed-rank test at alpha {ALPHA} "
                f"needs at least {MIN_WILCOXON_N} non-zero pairs. Further seeds would be new experiment IDs."
            ),
        })

    base = loaded[plan.baseline]
    other = loaded[plan.noise_reference]
    merged = _align(base, other, plan.noise_reference)
    pred_a = merged["y_pred_a"].to_numpy().astype(bool)
    pred_b = merged["y_pred_b"].to_numpy().astype(bool)
    agree = pred_a == pred_b
    p1_a = float(pred_a.mean())
    p1_b = float(pred_b.mean())
    chance = p1_a * p1_b + (1.0 - p1_a) * (1.0 - p1_b)
    observed = float(agree.mean())
    kappa = 1.0 if chance == 1 else (observed - chance) / (1.0 - chance)
    repeatability = pd.DataFrame([{
        "experiment_a": plan.baseline,
        "experiment_b": plan.noise_reference,
        "split": SPLIT,
        "n": int(len(merged)),
        "decision_agreement": observed,
        "cohen_kappa": float(kappa),
        "prob_pearson": float(np.corrcoef(merged["y_prob_a"], merged["y_prob_b"])[0, 1]),
        "prob_mae": float(np.mean(np.abs(merged["y_prob_a"] - merged["y_prob_b"]))),
        "n_seeds": 2,
    }])

    plan_rows = [
        {
            "test_id": "marginal_bootstrap",
            "procedure": "percentile bootstrap of roc_auc, balanced_accuracy, mcc",
            "comparisons": "each of " + ", ".join(exp for exp, _, _ in ids),
            "alpha": ALPHA,
            "adjustment": "none (interval, not a family of claims)",
            "n_bootstrap": n_boot,
            "bootstrap_seed": seed,
            "multi_seed_required": False,
        },
        {
            "test_id": "paired_bootstrap",
            "procedure": f"percentile bootstrap of challenger minus {plan.baseline}; primary metric {PRIMARY_METRIC}",
            "comparisons": ", ".join(a.experiment_id for a in plan.ablations),
            "alpha": ALPHA,
            "adjustment": f"bonferroni x{family} on the {family} factor runs; seed replicate stays at {1 - ALPHA:.0%}",
            "n_bootstrap": n_boot,
            "bootstrap_seed": seed,
            "multi_seed_required": False,
        },
        {
            "test_id": "mcnemar_exact",
            "procedure": "exact McNemar on saved decisions at each run's own threshold",
            "comparisons": ", ".join(a.experiment_id for a in plan.ablations),
            "alpha": ALPHA,
            "adjustment": f"bonferroni x{family} for factor runs; none for the seed replicate",
            "n_bootstrap": 0,
            "bootstrap_seed": seed,
            "multi_seed_required": False,
        },
        {
            "test_id": "wilcoxon_across_seeds",
            "procedure": "two-sided exact signed-rank on one metric per seed",
            "comparisons": f"{plan.baseline} vs {plan.noise_reference}",
            "alpha": ALPHA,
            "adjustment": "not run",
            "n_bootstrap": 0,
            "bootstrap_seed": seed,
            "multi_seed_required": True,
        },
    ]
    # questions is retained so a missing plan question fails here rather than in the report
    missing = [a.experiment_id for a in plan.ablations if a.experiment_id not in questions]
    if missing:
        raise ValueError(f"missing questions: {missing}")
    return {
        "bootstrap_cis": pd.DataFrame(marginal_rows),
        "paired_tests": pd.DataFrame(paired_rows),
        "mcnemar_tests": pd.DataFrame(mcnemar_rows),
        "seed_variance": pd.DataFrame(seed_rows),
        "repeatability": repeatability,
        "test_plan": pd.DataFrame(plan_rows),
    }


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def point_check(repo: Path, experiment_id: str, metric: str) -> float:
    """Full-sample metric, used by tests that do not need a bootstrap."""

    frame = pd.read_csv(repo / "08_Evaluation" / experiment_id / "predictions.csv")
    part = frame[frame["split"] == SPLIT]
    return metric_value(metric, part["y_true"].to_numpy(), part["y_prob"].to_numpy(), part["y_pred"].to_numpy())


def write_outputs(repo: Path, frames: dict[str, pd.DataFrame], *, n_boot: int, seed: int) -> Path:
    out = repo / "08_Evaluation/statistics"
    out.mkdir(parents=True, exist_ok=True)
    names = {
        "bootstrap_cis": "bootstrap_cis.csv",
        "paired_tests": "paired_tests.csv",
        "mcnemar_tests": "mcnemar_tests.csv",
        "seed_variance": "seed_variance.csv",
        "repeatability": "repeatability.csv",
        "test_plan": "test_plan.csv",
    }
    for key, name in names.items():
        frames[key].to_csv(out / name, index=False)
    plan = load_plan(repo / PLAN)
    manifest = {
        "step": "STEP-049",
        "phase": "E11",
        "split": SPLIT,
        "baseline": plan.baseline,
        "seed_replicate": plan.noise_reference,
        "alpha": ALPHA,
        "primary_metric": PRIMARY_METRIC,
        "n_bootstrap": n_boot,
        "bootstrap_seed": seed,
        "superiority_claim": "none",
        "prediction_sha256": {
            exp: file_sha256(repo / "08_Evaluation" / exp / "predictions.csv")
            for exp in [plan.baseline, *[a.experiment_id for a in plan.ablations]]
        },
    }
    (out / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return out


def update_registry(repo: Path, date: str) -> None:
    path = repo / "08_Evaluation/evaluation_registry.csv"
    tests = (
        "08_Evaluation/statistics/bootstrap_cis.csv; "
        "08_Evaluation/statistics/paired_tests.csv; "
        "08_Evaluation/statistics/mcnemar_tests.csv; "
        "08_Evaluation/statistics/seed_variance.csv; "
        "08_Evaluation/statistics/statistics_report.md"
    )
    note = "E11 2026-11-13: paired bootstrap and exact McNemar on SPLIT0001 test. No superiority claim; Wilcoxon across seeds not run (n=2)."
    rows = list(csv.reader(path.open(encoding="utf-8", newline="")))
    head = [h.strip() for h in rows[0]]
    exp_col = head.index("Experiment")
    targets = {"EXP0001", "EXP0003", "EXP0004", "EXP0005", "EXP0006"}
    seen = set()
    for row in rows[1:]:
        if not row or row[exp_col].strip() not in targets:
            continue
        seen.add(row[exp_col].strip())
        row[head.index("Statistical Tests")] = tests
        row[head.index("Updated")] = date
        notes = row[head.index("Reviewer Notes")]
        if "E11 2026-11-13" not in notes:
            row[head.index("Reviewer Notes")] = (notes.rstrip(".") + ". " + note).strip()
    if seen != targets:
        raise ValueError(f"registry is missing {targets - seen}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerows(rows)
