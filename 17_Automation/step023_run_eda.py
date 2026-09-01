#!/usr/bin/env python3
"""Kaggle-oriented entry script for STEP-023 EDA.

Copy this file + dataset_eda/ + dataset_validation/ to /kaggle/working and run:
  python step023_run_eda.py
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from dataset_eda import run_eda  # noqa: E402


def main() -> int:
    kaggle_input = Path("/kaggle/input")
    local_roots = [
        Path("_staging/DS0001_artifact/kaggle_upload"),
        Path("_staging/DS0002_diff/kaggle_upload"),
        Path("_staging/DS0004_synthbuster/kaggle_upload"),
        Path("_staging/DS0005_fairface/kaggle_upload"),
        Path("_staging/DS0003_140k"),
        Path("03_Datasets/raw"),
    ]
    roots = [kaggle_input] if kaggle_input.exists() else [p for p in local_roots if p.exists()]
    if not roots:
        print("No search roots found.")
        return 1

    out = Path("/kaggle/working/reports") if Path("/kaggle/working").exists() else Path("03_Datasets/reports")
    # On Kaggle prefer larger sample; set FULL=1 env for population scan
    import os

    full = os.environ.get("STEP023_FULL_PIXELS", "").strip() in {"1", "true", "yes"}
    sample = int(os.environ.get("STEP023_PIXEL_SAMPLE", "3000"))
    summary = run_eda(
        ["DS0001", "DS0002", "DS0003", "DS0004", "DS0005"],
        roots,
        out,
        pixel_sample=None if full else sample,
        full_pixels=full,
    )
    print(summary)
    missing = [k for k, v in summary["datasets"].items() if v.get("n_images", 0) == 0]
    return 2 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
