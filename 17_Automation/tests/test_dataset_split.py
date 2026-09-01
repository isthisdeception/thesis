"""Tests for leakage-safe dataset splitting."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from dataset_split.core import (
    SplitConfig,
    assert_no_leakage,
    fingerprint,
    split_grouped_random,
    split_logo,
)
from dataset_split.runner import run_one_split


def _rows() -> list[dict[str, str]]:
    return [
        {
            "processed_path": f"images/a{i}.png",
            "relative_path": f"a{i}.png",
            "class_label": "fake",
            "generator": "g1",
            "identity": "id1",
            "content_hash": f"h{i}",
        }
        for i in range(6)
    ] + [
        {
            "processed_path": f"images/b{i}.png",
            "relative_path": f"b{i}.png",
            "class_label": "fake",
            "generator": "g2",
            "identity": "id2",
            "content_hash": f"h{i+6}",
        }
        for i in range(6)
    ]


def test_grouped_random_reproducible():
    cfg = SplitConfig(
        split_id="SPLIT0001",
        output_id="DS_TEST",
        dataset_id="DS_TEST",
        pipeline_id="PP_TEST",
        scheme="grouped_random",
        seed=42,
        ratios=(0.5, 0.25, 0.25),
        group_by=["identity", "generator"],
    )
    rows = _rows()
    a1 = split_grouped_random(rows, cfg)
    a2 = split_grouped_random(rows, cfg)
    assert a1 == a2
    assert fingerprint(a1) == fingerprint(a2)


def test_logo_holds_out_generator():
    cfg = SplitConfig(
        split_id="SPLIT0002",
        output_id="DS_TEST",
        dataset_id="DS_TEST",
        pipeline_id="PP_TEST",
        scheme="logo",
        seed=42,
        held_out_generators=["g2"],
        group_by=["identity", "generator"],
    )
    rows = _rows()
    assignments = split_logo(rows, cfg)
    for row in rows:
        if row["generator"] == "g2":
            assert assignments[row["processed_path"]] == "test"
    leakage = assert_no_leakage(rows, assignments, group_by=cfg.group_by, logo_generators=["g2"])
    assert leakage["passed"]


def test_run_one_split_writes_artifacts(tmp_path: Path):
    cfg = SplitConfig(
        split_id="SPLIT0001",
        output_id="DS_TEST_PP",
        dataset_id="DS_TEST",
        pipeline_id="PP_TEST",
        scheme="grouped_random",
        seed=7,
        ratios=(0.6, 0.2, 0.2),
        group_by=["identity", "generator"],
    )
    rows = _rows()
    result = run_one_split(cfg, rows, tmp_path)
    split_dir = tmp_path / "DS_TEST_PP_SPLIT0001"
    assert split_dir.is_dir()
    assert (split_dir / "assignments.csv").is_file()
    assert (split_dir / "split_config.json").is_file()
    assert result["leakage"]["passed"]
