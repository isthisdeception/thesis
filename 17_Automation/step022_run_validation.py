#!/usr/bin/env python3
"""Kaggle-oriented entry script for STEP-022.

Copy this file + the dataset_validation package to /kaggle/working and run:
  python step022_run_validation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# repo layout: 17_Automation/step022_run_validation.py + dataset_validation/
sys.path.insert(0, str(HERE))

from dataset_validation import run_validation  # noqa: E402


def main() -> int:
    kaggle_input = Path("/kaggle/input")
    local_fallback = [
        Path("03_Datasets/raw"),
        Path("_staging/incoming"),
    ]
    roots = [kaggle_input] if kaggle_input.exists() else [p for p in local_fallback if p.exists()]
    if not roots:
        print("No search roots found. Pass data under /kaggle/input or local staging.")
        return 1

    out = Path("/kaggle/working/reports") if Path("/kaggle/working").exists() else Path("03_Datasets/reports")
    summary = run_validation(
        ["DS0001", "DS0002", "DS0003", "DS0004", "DS0005"],
        roots,
        out,
        max_images=None,
        integrity_sample_every=500,
    )
    print(summary)
    failed = [k for k, v in summary.items() if not v["passed"]]
    return 2 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
