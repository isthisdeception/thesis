"""Orchestrate STEP-028 splits from preprocessing index.csv files."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .core import (
    SplitConfig,
    assert_no_leakage,
    fingerprint,
    split_grouped_random,
    split_logo,
    split_official_holdout,
)
from .report import write_split_artifacts, write_split_report
from .schemes import SPLIT_PLANS


class SplitError(RuntimeError):
    pass


def _load_index(index_path: Path) -> list[dict[str, str]]:
    with index_path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def find_repo_root(start: Path | None = None) -> Path:
    start = start or Path(__file__).resolve()
    for p in [start, *start.parents]:
        if (p / "MASTER_RESEARCH_OPERATING_SYSTEM.md").is_file():
            return p
    raise FileNotFoundError("Could not locate thesis repo root")


def _resolve_index_path(repo_root: Path, output_id: str) -> Path:
    candidates = [
        repo_root / "04_Preprocessing" / "reports" / "metadata" / output_id / "index.csv",
        repo_root / "_processed_dataset" / f"processed_{output_id}" / "metadata" / "index.csv",
        repo_root / "_processed_dataset" / output_id / output_id / "metadata" / "index.csv",
    ]
    for p in candidates:
        if p.is_file():
            return p
    raise FileNotFoundError(f"No index.csv for {output_id} under {candidates}")


def run_one_split(
    cfg: SplitConfig,
    rows: list[dict[str, str]],
    splits_root: Path,
) -> dict[str, Any]:
    if cfg.scheme == "grouped_random":
        assignments = split_grouped_random(rows, cfg)
        logo_gens = None
    elif cfg.scheme == "logo":
        assignments = split_logo(rows, cfg)
        logo_gens = cfg.held_out_generators
    elif cfg.scheme == "official_holdout":
        assignments = split_official_holdout(rows, cfg)
        logo_gens = None
    else:
        raise SplitError(f"Unknown scheme {cfg.scheme}")

    if len(assignments) != len(rows):
        raise SplitError(f"{cfg.split_id}: assignment count mismatch")

    leakage = assert_no_leakage(
        rows,
        assignments,
        group_by=cfg.group_by,
        logo_generators=logo_gens,
    )
    if not leakage["passed"]:
        raise SplitError(f"{cfg.split_id} leakage failed: {leakage['issues'][:3]}")

    write_split_artifacts(cfg, rows, assignments, leakage, splits_root)
    summary = {
        "split_id": cfg.split_id,
        "output_id": cfg.output_id,
        "scheme": cfg.scheme,
        "seed": cfg.seed,
        "notes": cfg.notes,
        "summary": {
            "counts": {
                p: sum(1 for v in assignments.values() if v == p)
                for p in ("train", "val", "test")
            }
        },
        "leakage": leakage,
        "fingerprint": fingerprint(assignments),
    }
    return summary


def run_splits(
    repo_root: Path | None = None,
    output_ids: list[str] | None = None,
) -> dict[str, Any]:
    repo_root = repo_root or find_repo_root()
    splits_root = repo_root / "03_Datasets" / "splits"
    report_path = repo_root / "03_Datasets" / "reports" / "split_report.md"

    targets = output_ids or list(SPLIT_PLANS)
    all_results: list[dict[str, Any]] = []

    for output_id in targets:
        if output_id not in SPLIT_PLANS:
            raise SplitError(f"No split plan for {output_id}")
        index_path = _resolve_index_path(repo_root, output_id)
        rows = _load_index(index_path)
        for cfg in SPLIT_PLANS[output_id]:
            result = run_one_split(cfg, rows, splits_root)
            all_results.append(result)

    write_split_report(all_results, report_path)
    return {"splits": len(all_results), "report": str(report_path)}
