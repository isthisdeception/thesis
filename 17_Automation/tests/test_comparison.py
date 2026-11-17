"""STEP-050: the ranked comparison keeps the data invariants and makes no superiority claim."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from comparison.audit import failures, render_audit
from comparison.build import comparison_frame
from comparison.report import render_comparison

REPO = Path(__file__).resolve().parents[2]


def test_ranked_set_is_the_fair_split_only() -> None:
    ranked, excluded = comparison_frame(REPO)
    assert list(ranked["experiment_id"]) == ["EXP0001", "EXP0003", "EXP0004", "EXP0005", "EXP0006"]
    assert set(ranked["split_id"]) == {"SPLIT0001"}
    assert set(ranked["superiority_claim"]) == {"none"}
    assert "accuracy" in ranked.columns and "mcc" in ranked.columns
    assert set(excluded["experiment_id"]) == {"EXP0002"}
    assert "split_id" in excluded.iloc[0].reason


def test_report_names_the_exclusion_and_refuses_superiority() -> None:
    ranked, excluded = comparison_frame(REPO)
    text = render_comparison(ranked, excluded, "2026-11-13")
    assert "EXP0002" in text
    assert "none" in text
    assert "Not ranked" in text


def test_audit_fails_when_a_ranked_row_is_unfair() -> None:
    text = render_audit(["ranked rows do not share SPLIT0001"], "2026-11-13")
    assert "**Approval Status:** FAIL" in text
    assert "SPLIT0001" in text


def test_repo_audit_passes_after_the_step_outputs_exist() -> None:
    if not (REPO / "08_Evaluation/evaluation_audit.md").is_file():
        return
    assert failures(REPO) == []
    ranked = pd.read_csv(REPO / "08_Evaluation/comparison_tables.csv")
    assert "EXP0002" not in set(ranked["experiment_id"])
