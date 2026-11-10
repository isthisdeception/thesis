"""Write EVAL0001 confusion data and failure_analysis.md from validated predictions.

Usage (from 17_Automation/):
    python -m failure_analysis --experiment EXP0001 --evaluation EVAL0001
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
from pathlib import Path

import pandas as pd

from classification_metrics import require_validated

from .analysis import (
    confusion_frame,
    error_cases_frame,
    error_summary_frame,
    group_frame,
    join_metadata,
    metadata_coverage,
    per_class_frame,
)
from .report import render_report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", default="EXP0001")
    parser.add_argument("--evaluation", default="EVAL0001")
    parser.add_argument("--metadata", default="04_Preprocessing/reports/metadata/DS0001_PP0001/index.csv", help="relative to the repo root")
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--date", default=dt.date.today().isoformat())
    args = parser.parse_args()
    root = args.repo_root or Path(__file__).resolve().parents[2]
    eval_dir = root / "08_Evaluation" / args.evaluation
    source = root / "08_Evaluation" / args.experiment / "predictions.csv"

    require_validated(eval_dir / "prediction_validation_report.md")
    frame = join_metadata(pd.read_csv(source), pd.read_csv(root / args.metadata))
    outputs = {
        "confusion_matrix.csv": confusion_frame(frame),
        "per_class_stats.csv": per_class_frame(frame),
        "error_by_group.csv": group_frame(frame),
        "error_summary.csv": error_summary_frame(frame),
        "error_cases.csv": error_cases_frame(frame),
    }
    for name, out in outputs.items():
        out.to_csv(eval_dir / name, index=False)
    sha = hashlib.sha256(source.read_bytes()).hexdigest()
    report = render_report(
        outputs["confusion_matrix.csv"],
        outputs["per_class_stats.csv"],
        outputs["error_by_group.csv"],
        outputs["error_summary.csv"],
        outputs["error_cases.csv"],
        metadata_coverage(frame, "test"),
        args.evaluation,
        args.experiment,
        sha,
        args.date,
    )
    (eval_dir / "failure_analysis.md").write_text(report, encoding="utf-8")
    print(f"wrote {len(outputs)} CSVs and failure_analysis.md to {eval_dir}")


if __name__ == "__main__":
    main()
