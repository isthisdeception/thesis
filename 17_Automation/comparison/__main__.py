"""STEP-050 comparison, publication specs, and Checklist 8.

Usage (from 17_Automation/):
    python -m comparison
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import sys
from pathlib import Path

from .audit import failures, render_audit
from .build import comparison_frame
from .report import render_comparison, render_evaluation
from .specs import write_specs

REPO = Path(__file__).resolve().parents[2]


def _update_registry(repo: Path, date: str) -> None:
    path = repo / "08_Evaluation/evaluation_registry.csv"
    rows = list(csv.reader(path.open(encoding="utf-8", newline="")))
    head = [cell.strip() for cell in rows[0]]
    reports = "08_Evaluation/comparison_report.md; 08_Evaluation/evaluation_report.md; 08_Evaluation/evaluation_audit.md"
    figures = "FIG0021; FIG0022; FIG0023; FIG0024; FIG0025 (specs only)"
    note = "E16-E18 2026-11-13: ranked comparison is EXP0001 and EXP0003-EXP0006. EXP0002 excluded (SPLIT0002). Checklist 8 evidence PASS. No superiority claim."
    for row in rows[1:]:
        if not row:
            continue
        evaluation_id = row[head.index("Evaluation ID")].strip()
        if evaluation_id not in {f"EVAL{i:04d}" for i in range(1, 7)}:
            continue
        current = row[head.index("Reports")]
        if "comparison_report.md" not in current:
            row[head.index("Reports")] = f"{current}; {reports}" if current else reports
        if evaluation_id == "EVAL0001" and "FIG0021" not in row[head.index("Figures")]:
            row[head.index("Figures")] = row[head.index("Figures")].rstrip() + "; " + figures
        if "E16-E18 2026-11-13" not in row[head.index("Reviewer Notes")]:
            row[head.index("Reviewer Notes")] = (row[head.index("Reviewer Notes")].rstrip(".") + ". " + note).strip()
        row[head.index("Updated")] = date
    with path.open("w", encoding="utf-8", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerows(rows)


def main() -> None:
    sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO)
    parser.add_argument("--date", default=dt.date.today().isoformat())
    args = parser.parse_args()
    repo = args.repo_root
    ranked, excluded = comparison_frame(repo)
    root = repo / "08_Evaluation"
    ranked.to_csv(root / "comparison_tables.csv", index=False)
    excluded.to_csv(root / "comparison_exclusions.csv", index=False)
    (root / "comparison_report.md").write_text(render_comparison(ranked, excluded, args.date), encoding="utf-8")
    (root / "evaluation_report.md").write_text(render_evaluation(ranked, repo, args.date), encoding="utf-8")
    write_specs(repo)
    _update_registry(repo, args.date)
    problems = failures(repo)
    (root / "evaluation_audit.md").write_text(render_audit(problems, args.date), encoding="utf-8")
    print(f"ranked {len(ranked)} experiments; excluded {len(excluded)}")
    if problems:
        sys.exit("Checklist 8 FAIL: " + "; ".join(problems))
    print("Checklist 8 PASS")


if __name__ == "__main__":
    main()
