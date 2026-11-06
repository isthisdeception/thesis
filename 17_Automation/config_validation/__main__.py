"""CLI: python -m config_validation <config.yaml> [--template] [--repo-root PATH]."""

from __future__ import annotations

import argparse
import sys

from .validator import validate_config_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="config_validation", description=__doc__)
    parser.add_argument("configs", nargs="+", help="config.yaml file(s) to validate")
    parser.add_argument(
        "--template",
        action="store_true",
        help="allow the EXPxxxx placeholder and unset git_commit/timestamp",
    )
    parser.add_argument("--repo-root", default=None, help="repo root (auto-detected if omitted)")
    args = parser.parse_args(argv)

    failed = False
    for path in args.configs:
        report = validate_config_file(path, repo_root=args.repo_root, template=args.template)
        if report.ok:
            print(f"PASS {path}")
        else:
            failed = True
            print(f"FAIL {path} ({len(report.errors)} error(s))")
            for error in report.errors:
                print(f"  - {error}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
