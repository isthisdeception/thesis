"""Write EVAL0001 classification metrics from validated predictions.

Usage (from 17_Automation/):
    python -m classification_metrics --experiment EXP0001 --evaluation EVAL0001
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
from pathlib import Path

from .compute import render_report, require_validated, write_metrics


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", default="EXP0001")
    parser.add_argument("--evaluation", default="EVAL0001")
    parser.add_argument("--positive-class", default="fake")
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--date", default=dt.date.today().isoformat())
    args = parser.parse_args()
    root = args.repo_root or Path(__file__).resolve().parents[2]
    eval_dir = root / "08_Evaluation" / args.evaluation
    predictions = root / "08_Evaluation" / args.experiment / "predictions.csv"

    require_validated(eval_dir / "prediction_validation_report.md")
    frame = write_metrics(predictions, eval_dir / "classification_metrics.csv", args.positive_class)
    sha = hashlib.sha256(predictions.read_bytes()).hexdigest()
    report = render_report(frame, args.evaluation, args.experiment, sha, args.date)
    (eval_dir / "classification_metrics.md").write_text(report, encoding="utf-8")
    print(f"wrote {len(frame)} split(s) to {eval_dir}")


if __name__ == "__main__":
    main()
