"""Write 08_Evaluation/EVAL0001/prediction_validation_report.md.

Usage (from 17_Automation/):
    python -m prediction_validation --experiment EXP0001 --evaluation EVAL0001
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .validate import write_report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", default="EXP0001")
    parser.add_argument("--evaluation", default="EVAL0001")
    parser.add_argument("--repo-root", type=Path, default=None)
    args = parser.parse_args()
    root = args.repo_root or Path(__file__).resolve().parents[2]
    checks = write_report(root, args.evaluation, args.experiment)
    print(f"PASS {args.evaluation}: {len(checks)} checks")


if __name__ == "__main__":
    main()
