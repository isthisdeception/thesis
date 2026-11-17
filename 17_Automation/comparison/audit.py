"""Checklist 8. The audit passes only when every evidence file is present and the comparison stays fair."""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd

from .specs import FIGURES, REQUIRED_EXISTING_FIGURES, TABLES

EVIDENCE = {
    "metrics": "08_Evaluation/EVAL0001/classification_metrics.csv",
    "roc": "08_Evaluation/EXP0001/roc_curve.csv",
    "pr": "08_Evaluation/EXP0001/pr_curve.csv",
    "confusion": "08_Evaluation/EVAL0001/confusion_matrix.csv",
    "calibration": "08_Evaluation/EVAL0001/calibration_summary.csv",
    "statistics": "08_Evaluation/statistics/statistics_report.md",
    "robustness": "08_Evaluation/EVAL0001/robustness/robustness_report.md",
    "generalization": "08_Evaluation/EVAL0001/generalization/cross_dataset_report.md",
    "unseen_generator": "08_Evaluation/EVAL0002/unseen_generator/unseen_report.md",
    "ablation": "08_Evaluation/ablations/ablation_report.md",
    "failure_analysis": "08_Evaluation/EVAL0001/failure_analysis.md",
    "comparison_table": "08_Evaluation/comparison_tables.csv",
    "comparison_report": "08_Evaluation/comparison_report.md",
    "evaluation_report": "08_Evaluation/evaluation_report.md",
    "registry": "08_Evaluation/evaluation_registry.csv",
}

FAIR_EXPERIMENTS = ["EXP0001", "EXP0003", "EXP0004", "EXP0005", "EXP0006"]


def failures(repo: Path) -> list[str]:
    missing = [f"{name}: {rel}" for name, rel in EVIDENCE.items() if not (repo / rel).is_file()]
    for figure_id in [*REQUIRED_EXISTING_FIGURES.values(), *FIGURES]:
        path = repo / "09_Figures/specs" / f"{figure_id}_spec.md"
        if not path.is_file():
            missing.append(f"figure spec {figure_id}")
        elif (repo / "09_Figures/assets" / f"{figure_id}_v1.png").is_file():
            missing.append(f"{figure_id} has a rendered png; specs only")
    for table_id in TABLES:
        if not (repo / "10_Tables/specs" / f"{table_id}_spec.md").is_file():
            missing.append(f"table spec {table_id}")
    if missing:
        return missing

    ranked = pd.read_csv(repo / EVIDENCE["comparison_table"])
    problems = []
    if set(ranked["experiment_id"]) != set(FAIR_EXPERIMENTS):
        problems.append("ranked experiments are not exactly the fair set")
    if not bool(ranked["fairness_compatible"].all()) or not bool(ranked["ranked"].all()):
        problems.append("a ranked row is not fairness-compatible")
    if ranked["split_id"].nunique() != 1 or ranked["split_id"].iloc[0] != "SPLIT0001":
        problems.append("ranked rows do not share SPLIT0001")
    if set(ranked["superiority_claim"]) != {"none"}:
        problems.append("a comparison row carries a superiority claim")
    for metric in ("roc_auc", "pr_auc", "balanced_accuracy", "mcc", "accuracy"):
        if metric not in ranked.columns:
            problems.append(f"comparison table is missing {metric}")
    report = (repo / EVIDENCE["comparison_report"]).read_text(encoding="utf-8")
    if "EXP0002" not in report or "not ranked" not in report.lower() and "Not ranked" not in report:
        problems.append("comparison report does not record the excluded experiment")
    if "superiority" not in report.lower():
        problems.append("comparison report does not state the superiority rule")
    registry = list(csv.reader((repo / EVIDENCE["registry"]).open(encoding="utf-8", newline="")))
    head = [cell.strip() for cell in registry[0]]
    ids = {row[head.index("Evaluation ID")].strip() for row in registry[1:] if row}
    expected = {f"EVAL{i:04d}" for i in range(1, 7)}
    if not expected <= ids:
        problems.append(f"registry is missing {expected - ids}")
    for curve, experiment in (("roc_curve.csv", exp) for exp in FAIR_EXPERIMENTS):
        if not (repo / "08_Evaluation" / experiment / curve).is_file():
            problems.append(f"{experiment} has no ROC curve")
    for experiment in FAIR_EXPERIMENTS:
        if not (repo / "08_Evaluation" / experiment / "pr_curve.csv").is_file():
            problems.append(f"{experiment} has no PR curve")
    return problems


def render_audit(problems: list[str], date: str) -> str:
    status = "FAIL" if problems else "PASS"
    passed = [
        ("Metrics complete", EVIDENCE["metrics"]),
        ("ROC and PR data", f"{EVIDENCE['roc']}; {EVIDENCE['pr']}"),
        ("Confusion data", EVIDENCE["confusion"]),
        ("Calibration", EVIDENCE["calibration"]),
        ("Statistical testing", EVIDENCE["statistics"]),
        ("Robustness", EVIDENCE["robustness"]),
        ("Generalization and unseen generator", f"{EVIDENCE['generalization']}; {EVIDENCE['unseen_generator']}"),
        ("Ablation", EVIDENCE["ablation"]),
        ("Failure analysis", EVIDENCE["failure_analysis"]),
        ("Fair comparison only", EVIDENCE["comparison_report"]),
        ("Figure specs, data only", "FIG0011, FIG0013, FIG0014, FIG0016, FIG0020–FIG0025"),
        ("Table specs", "TAB0002, TAB0003"),
        ("Evaluation registry", EVIDENCE["registry"]),
    ]
    lines = [
        "# Evaluation Audit",
        "",
        f"**Audit date:** {date}  ",
        "**Gate:** Checklist 8 — Evaluation  ",
        f"**Approval Status:** {status}",
        "",
        "## Summary",
        "",
        "Checklist 8 covers EVAL0001–EVAL0006. The ranked comparison is EXP0001 and the STEP-048 one-factor runs. "
        "EXP0002 stays out of that table because it uses SPLIT0002. No publication figure was rendered.",
        "",
        "## Passed" if not problems else "## Passed before the failures below",
        "",
        "| Checklist 8 item | Evidence |",
        "|---|---|",
    ]
    if not problems:
        for item, evidence in passed:
            lines.append(f"| {item} | `{evidence}` |")
        lines += ["", "## Failed", "", "None.", ""]
    else:
        lines += ["", "## Failed", ""]
        for problem in problems:
            lines.append(f"- {problem}")
        lines.append("")
    lines += [
        "## Evidence",
        "",
        "The comparison module refuses a ranked row whose dataset, version, pipeline, or split differs from EXP0001. "
        "Metric values are the STEP-048 table. Intervals are the STEP-049 table. Neither file is recomputed here.",
        "",
        "## Recommendations",
        "",
        "1. Human confirmation is the [H] item on STEP-050 before STEP-051 starts.",
        "2. A new metric or a new test set needs a new EVAL ID.",
        "3. More seeds, if a seed-level Wilcoxon test is wanted, are new EXP IDs.",
        "",
    ]
    return "\n".join(lines)
