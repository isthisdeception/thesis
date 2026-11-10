"""Write EVAL0001 calibration and threshold data from validated predictions.

Usage (from 17_Automation/):
    python -m calibration_threshold --experiment EXP0001 --evaluation EVAL0001
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
from pathlib import Path

import pandas as pd

from classification_metrics import require_validated

from .calibration import calibration_frames
from .report import render_report
from .threshold import operating_frame, sweep_frame


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", default="EXP0001")
    parser.add_argument("--evaluation", default="EVAL0001")
    parser.add_argument("--bins", type=int, default=15, help="must match calibration_bins in the experiment config")
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--date", default=dt.date.today().isoformat())
    args = parser.parse_args()
    root = args.repo_root or Path(__file__).resolve().parents[2]
    eval_dir = root / "08_Evaluation" / args.evaluation
    source = root / "08_Evaluation" / args.experiment / "predictions.csv"

    require_validated(eval_dir / "prediction_validation_report.md")
    predictions = pd.read_csv(source)
    summary, reliability, confidence = calibration_frames(predictions, args.bins)
    sweep, points = sweep_frame(predictions), operating_frame(predictions)
    outputs = {
        "calibration_summary.csv": summary,
        "reliability.csv": reliability,
        "confidence_distribution.csv": confidence,
        "threshold_sweep.csv": sweep,
        "operating_points.csv": points,
    }
    for name, frame in outputs.items():
        frame.to_csv(eval_dir / name, index=False)
    sha = hashlib.sha256(source.read_bytes()).hexdigest()
    report = render_report(summary, reliability, confidence, points, args.evaluation, args.experiment, sha, args.date)
    (eval_dir / "calibration_threshold.md").write_text(report, encoding="utf-8")
    print(f"wrote {len(outputs)} CSVs and calibration_threshold.md to {eval_dir}")


if __name__ == "__main__":
    main()
