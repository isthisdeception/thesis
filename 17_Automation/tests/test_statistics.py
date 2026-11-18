"""STEP-049: exact tests, bootstrap intervals, and the no-superiority report rule."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import matthews_corrcoef, roc_auc_score

from statistics.analyze import point_check, run
from statistics.core import (
    binom_test_two_sided,
    confusion_metrics,
    mcnemar,
    paired_bootstrap,
    roc_auc,
    roc_auc_rows,
    run_difference,
    wilcoxon_signed_rank,
)
from statistics.report import render_report

REPO = Path(__file__).resolve().parents[2]


def test_roc_auc_matches_sklearn_including_ties() -> None:
    y = np.array([0, 0, 1, 1, 1, 0])
    scores = np.array([0.2, 0.2, 0.2, 0.8, 0.9, 0.1])
    assert roc_auc(y, scores) == pytest.approx(roc_auc_score(y, scores))
    rows = roc_auc_rows(np.vstack([y, y[::-1]]), np.vstack([scores, scores[::-1]]))
    assert rows[0] == pytest.approx(roc_auc(y, scores))
    assert rows[1] == pytest.approx(roc_auc(y[::-1], scores[::-1]))


def test_mcc_matches_sklearn() -> None:
    y = np.array([0, 1, 1, 0, 1, 0, 0])
    pred = np.array([0, 1, 0, 0, 1, 1, 0])
    _, mcc = confusion_metrics(y, pred)
    assert mcc == pytest.approx(matthews_corrcoef(y, pred))


@pytest.mark.parametrize("k,n,expected", [(0, 6, 2 / 64), (1, 6, 14 / 64), (3, 6, 1.0)])
def test_binom_test_known_small_cases(k: int, n: int, expected: float) -> None:
    assert binom_test_two_sided(k, n) == pytest.approx(expected)
    assert binom_test_two_sided(n - k, n) == pytest.approx(expected)


def test_mcnemar_counts_and_undefined_when_no_discordance() -> None:
    y = np.array([1, 1, 0, 0])
    a = np.array([1, 0, 0, 1])
    b = np.array([0, 0, 0, 0])
    # Image 0: only A correct. Image 3: only B correct. Images 1 and 2: both wrong, or both correct.
    table = mcnemar(y, a, b)
    assert (table["b_a_only_correct"], table["c_b_only_correct"]) == (1, 1)
    assert table["accuracy_delta"] == pytest.approx(0.0)
    same = mcnemar(y, a, a)
    assert same["p_exact"] == 1.0 and same["n_agree"] == 4


def test_wilcoxon_all_positive_n6_and_refuses_too_few() -> None:
    result = wilcoxon_signed_rank(np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]))
    assert result["status"] == "computed"
    assert result["p_value"] == pytest.approx(2 / 64)
    short = wilcoxon_signed_rank(np.array([0.1, -0.2]))
    assert short["status"] == "not_run" and short["n"] == 2


def test_identical_runs_have_a_zero_interval() -> None:
    y = np.array([0, 1, 0, 1, 1, 0, 1, 0])
    prob = np.array([0.1, 0.8, 0.2, 0.7, 0.9, 0.3, 0.6, 0.4])
    pred = (prob >= 0.5).astype(int)
    intervals = paired_bootstrap(y, prob, pred, prob, pred, n_boot=200, rng=np.random.default_rng(0), levels=(0.95,))
    assert intervals["roc_auc"]["delta"] == 0.0
    assert intervals["roc_auc"][0.95] == (0.0, 0.0)
    assert run_difference(0.0, 0.0) == "not_supported"
    assert run_difference(0.1, 0.2) == "challenger_higher"
    assert run_difference(-0.3, -0.1) == "challenger_lower"


def test_report_states_no_superiority_claim() -> None:
    paired = pd.DataFrame([{
        "baseline_id": "EXP0001", "challenger_id": "EXP0005", "factor": "pretraining", "role": "ablation",
        "metric": "roc_auc", "n": 20, "delta": -0.2, "ci_low": -0.3, "ci_high": -0.1,
        "claim_ci_low": -0.28, "claim_ci_high": -0.12, "claim_ci_level": 1 - 0.05 / 3,
        "run_difference": "challenger_lower", "larger_than_seed_pair": True,
        "n_bootstrap": 100, "bootstrap_seed": 49,
    }])
    mcnemar_frame = pd.DataFrame([{
        "challenger_id": "EXP0005", "factor": "pretraining", "role": "ablation", "family_size": 3,
        "n_agree": 10, "b_baseline_only_correct": 8, "c_challenger_only_correct": 2,
        "accuracy_delta": -0.3, "discordant_odds_ratio": 0.25, "p_exact": 0.1, "p_adjusted": 0.3,
        "decisions_differ": False,
    }])
    seeds = pd.DataFrame([{
        "metric": "roc_auc", "value_a": 0.9, "value_b": 0.91, "mean": 0.905, "abs_diff": 0.01,
        "sample_sd": 0.007, "wilcoxon_status": "not_run",
        "wilcoxon_reason": "need at least 6 non-zero pairs",
    }])
    repeat = pd.DataFrame([{
        "decision_agreement": 0.99, "cohen_kappa": 0.98, "prob_pearson": 0.97, "prob_mae": 0.02,
        "experiment_a": "EXP0001", "experiment_b": "EXP0003", "n": 20,
    }])
    text = render_report({
        "paired_tests": paired, "mcnemar_tests": mcnemar_frame, "seed_variance": seeds, "repeatability": repeat,
    }, "2026-11-13")
    assert "No superiority claim is made" in text
    assert "not run" in text
    assert "EXP0005" in text


def test_saved_baseline_auc_matches_the_ablation_table() -> None:
    assert point_check(REPO, "EXP0001", "roc_auc") == pytest.approx(0.926068, abs=5e-5)


def test_repo_protocol_on_a_short_bootstrap() -> None:
    frames = run(REPO, n_boot=100, seed=49)
    paired = frames["paired_tests"]
    assert set(paired["challenger_id"]) == {"EXP0003", "EXP0004", "EXP0005", "EXP0006"}
    assert set(paired["superiority_claim"]) == {"none"}
    assert set(frames["seed_variance"]["wilcoxon_status"]) == {"not_run"}
    pretrain = paired[(paired["challenger_id"] == "EXP0005") & (paired["metric"] == "roc_auc")].iloc[0]
    assert pretrain.delta == pytest.approx(-0.2243, abs=1e-3)
    assert pretrain.role == "ablation" and pretrain.primary
    seed = paired[(paired["challenger_id"] == "EXP0003") & (paired["metric"] == "roc_auc")].iloc[0]
    assert seed.role == "seed_replicate"
    assert seed.claim_ci_level == pytest.approx(0.95)
    assert pretrain.claim_ci_level == pytest.approx(1 - 0.05 / 3)
    assert frames["mcnemar_tests"]["decisions_differ"].dtype == bool
