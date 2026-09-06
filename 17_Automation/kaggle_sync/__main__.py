"""CLI entrypoint for STEP-031 Kaggle sync automation."""

from __future__ import annotations

import argparse

from .manifest import load_sync_plan
from .session import bootstrap_repo, publish_artifacts, push_metadata, resume_checkpoints


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Kaggle sync workflow for training sessions.")
    parser.add_argument(
        "--plan",
        default="17_Automation/kaggle_sync/sync_plan.example.yaml",
        help="Path to the sync plan YAML.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print actions without changing files.")

    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("bootstrap", help="Clone/pull the repo, verify inputs, install Kaggle extras.")
    sub.add_parser("resume-checkpoints", help="Copy mounted checkpoint artifacts into the repo.")
    sub.add_parser("publish-artifacts", help="Stage experiment outputs and publish to Kaggle.")

    push = sub.add_parser("push-metadata", help="Commit and push source-tier metadata only.")
    push.add_argument(
        "--commit-message",
        default="sync: update experiment metadata from Kaggle",
        help="Commit message for metadata sync.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    plan = load_sync_plan(args.plan)

    if args.command == "bootstrap":
        bootstrap_repo(plan, dry_run=args.dry_run)
    elif args.command == "resume-checkpoints":
        resume_checkpoints(plan, dry_run=args.dry_run)
    elif args.command == "publish-artifacts":
        publish_artifacts(plan, dry_run=args.dry_run)
    elif args.command == "push-metadata":
        push_metadata(plan, commit_message=args.commit_message, dry_run=args.dry_run)
    else:
        parser.error(f"unknown command: {args.command}")


if __name__ == "__main__":
    main()
