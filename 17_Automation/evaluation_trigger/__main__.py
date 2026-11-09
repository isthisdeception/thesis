"""Write 08_Evaluation/EXPxxxx/ from saved prediction CSVs.

Usage (from 17_Automation/):
    python -m evaluation_trigger --experiment EXP0001 --positive-class fake --negative-class real
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .bundle import write_bundle


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", required=True)
    parser.add_argument("--positive-class", required=True)
    parser.add_argument("--negative-class", required=True)
    parser.add_argument("--repo-root", type=Path, default=None)
    args = parser.parse_args()
    root = args.repo_root or Path(__file__).resolve().parents[2]
    manifest = write_bundle(
        repo_root=root,
        experiment_id=args.experiment,
        positive_class=args.positive_class,
        negative_class=args.negative_class,
    )
    print(json.dumps({"experiment_id": manifest["experiment_id"], "sources": manifest["sources"]}, indent=2))


if __name__ == "__main__":
    main()
