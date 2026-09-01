#!/usr/bin/env python3
"""CLI for STEP-022 dataset validation.

Examples (local):
  python -m dataset_validation --datasets DS0001 --roots ../../_staging/incoming/Artifact --out ../../03_Datasets/reports --max-images 200

Examples (Kaggle):
  python -m dataset_validation --datasets DS0001,DS0002,DS0003,DS0004,DS0005 \\
      --roots /kaggle/input --out /kaggle/working/reports
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running as script from 17_Automation/
_PKG_PARENT = Path(__file__).resolve().parent.parent
if str(_PKG_PARENT) not in sys.path:
    sys.path.insert(0, str(_PKG_PARENT))

from dataset_validation.runner import run_validation  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="STEP-022 / Phase D6 dataset validation")
    p.add_argument(
        "--datasets",
        default="DS0001,DS0002,DS0003,DS0004,DS0005",
        help="Comma-separated dataset IDs",
    )
    p.add_argument(
        "--roots",
        nargs="+",
        required=True,
        help="Search roots (e.g. /kaggle/input or local staging paths)",
    )
    p.add_argument("--out", required=True, help="Output directory for report CSVs")
    p.add_argument(
        "--max-images",
        type=int,
        default=None,
        help="Optional cap per dataset (smoke test only; omit for DoD full run)",
    )
    p.add_argument(
        "--integrity-sample-every",
        type=int,
        default=500,
        help="Append integrity sample every N successfully scanned images (0=disable)",
    )
    args = p.parse_args(argv)

    ds_ids = [x.strip() for x in args.datasets.split(",") if x.strip()]
    roots = [Path(r) for r in args.roots]
    out = Path(args.out)
    sample_every = args.integrity_sample_every

    summary = run_validation(
        ds_ids,
        roots,
        out,
        max_images=args.max_images,
        integrity_sample_every=sample_every,
    )
    failed = [k for k, v in summary.items() if not v["passed"]]
    print("SUMMARY:", {k: v["passed"] for k, v in summary.items()})
    if failed:
        print("FAILED thresholds:", failed)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
