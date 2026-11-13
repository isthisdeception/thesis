"""STEP-049 statistical tests for the baseline and the STEP-048 ablations.

Usage (from 17_Automation/):
    python -m statistics
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

from .analyze import run, update_registry, write_outputs
from .core import BOOT_SEED, N_BOOT_DEFAULT
from .report import render_report

REPO = Path(__file__).resolve().parents[2]


def main() -> None:
    sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO)
    parser.add_argument("--n-bootstrap", type=int, default=N_BOOT_DEFAULT)
    parser.add_argument("--seed", type=int, default=BOOT_SEED)
    parser.add_argument("--date", default=dt.date.today().isoformat())
    args = parser.parse_args()
    if args.n_bootstrap < 100:
        raise SystemExit("n-bootstrap must be at least 100 for a percentile interval")
    print(f"STEP-049: {args.n_bootstrap} bootstrap resamples, seed {args.seed}")
    frames = run(args.repo_root, n_boot=args.n_bootstrap, seed=args.seed)
    out = write_outputs(args.repo_root, frames, n_boot=args.n_bootstrap, seed=args.seed)
    (out / "statistics_report.md").write_text(render_report(frames, args.date), encoding="utf-8")
    update_registry(args.repo_root, args.date)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
