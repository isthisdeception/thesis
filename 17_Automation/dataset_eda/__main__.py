#!/usr/bin/env python3
"""CLI for STEP-023 dataset EDA.

Examples (local staging packs):
  python -m dataset_eda --datasets DS0001,DS0005 \\
    --roots ../../_staging/DS0001_artifact/kaggle_upload ../../_staging/DS0005_fairface/kaggle_upload \\
    --out ../../03_Datasets/reports --pixel-sample 500

Examples (Kaggle full DoD):
  python -m dataset_eda --datasets DS0001,DS0002,DS0003,DS0004,DS0005 \\
    --roots /kaggle/input --out /kaggle/working/reports --full-pixels
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PKG_PARENT = Path(__file__).resolve().parent.parent
if str(_PKG_PARENT) not in sys.path:
    sys.path.insert(0, str(_PKG_PARENT))

from dataset_eda.runner import run_eda  # noqa: E402
from dataset_eda.schemas import DEFAULT_PIXEL_SAMPLE, DEFAULT_RNG_SEED  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="STEP-023 / Phase D7 dataset EDA")
    p.add_argument("--datasets", default="DS0001,DS0002,DS0003,DS0004,DS0005")
    p.add_argument("--roots", nargs="+", required=True)
    p.add_argument("--out", required=True)
    p.add_argument(
        "--pixel-sample",
        type=int,
        default=DEFAULT_PIXEL_SAMPLE,
        help="Stratified pixel-sample size per dataset (default 3000)",
    )
    p.add_argument(
        "--full-pixels",
        action="store_true",
        help="Measure pixels on every image (slow; Kaggle DoD option)",
    )
    p.add_argument("--seed", type=int, default=DEFAULT_RNG_SEED)
    args = p.parse_args(argv)

    ds_ids = [x.strip() for x in args.datasets.split(",") if x.strip()]
    summary = run_eda(
        ds_ids,
        [Path(r) for r in args.roots],
        Path(args.out),
        pixel_sample=None if args.full_pixels else args.pixel_sample,
        full_pixels=args.full_pixels,
        seed=args.seed,
    )
    print("SUMMARY:", {k: v.get("n_images") for k, v in summary["datasets"].items()})
    missing = [k for k, v in summary["datasets"].items() if v.get("n_images", 0) == 0]
    if missing:
        print("WARNING: no images found for:", missing)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
