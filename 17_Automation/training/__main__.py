"""CLI: python -m training {train,lr-find} --config 06_Experiments/EXPxxxx/config.yaml."""

from __future__ import annotations

import argparse
import json
import sys

from . import find_lr, run_experiment


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="training", description=__doc__)
    parser.add_argument("command", choices=["train", "lr-find"])
    parser.add_argument("--config", required=True, help="path to the experiment config.yaml")
    parser.add_argument("--repo-root", default=None, help="repo root (auto-detected if omitted)")
    args = parser.parse_args(argv)

    runner = run_experiment if args.command == "train" else find_lr
    result = runner(args.config, repo_root=args.repo_root)
    if args.command == "train":
        print(json.dumps({"best_epoch": result["best_epoch"], "test": result["metrics"]["test"]}, indent=2))
    else:
        print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
