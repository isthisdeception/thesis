#!/usr/bin/env python3
"""STEP-028 — Create leakage-safe train/val/test splits."""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from dataset_split.runner import find_repo_root, run_splits  # noqa: E402


def main() -> int:
    repo = find_repo_root(Path(__file__).resolve())
    summary = run_splits(repo_root=repo)
    print(summary)
    print("STEP-028 split generation complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
