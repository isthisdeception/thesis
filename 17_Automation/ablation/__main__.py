"""STEP-048 ablations.

Usage (from 17_Automation/):
    python -m ablation list        # plan and status of each ablation
    python -m ablation create      # scaffold every planned experiment (never overwrites)
    python -m ablation evaluate    # after the Kaggle run: register, E1-E2, compare, report
"""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path

from .plan import load_plan

REPO = Path(__file__).resolve().parents[2]
DEFAULT_PLAN = REPO / "06_Experiments/ablations/STEP048_plan.yaml"
OUT = REPO / "08_Evaluation/ablations"


def cmd_list(args) -> None:
    from .compare import run_summary

    plan = load_plan(args.plan)
    for a in plan.ablations:
        created = (REPO / "06_Experiments" / a.experiment_id / "config.yaml").is_file()
        trained = run_summary(REPO, a.experiment_id) is not None
        print(f"{a.experiment_id} {a.model_id} {a.factor:<14} created={created} trained={trained}  {a.changes}")


def cmd_create(args) -> None:
    from .scaffold import create

    plan = load_plan(args.plan)
    commit = args.git_commit or subprocess.run(["git", "rev-parse", "main"], cwd=REPO, capture_output=True, text=True, check=True).stdout.strip()
    stamp = args.timestamp or dt.datetime.now().astimezone().replace(microsecond=0).isoformat()
    for exp, written in create(REPO, plan, commit, stamp).items():
        print(f"{exp}: {', '.join(written) or 'nothing new'}")


def cmd_evaluate(args) -> None:
    from evaluation_trigger.bundle import write_bundle
    from prediction_validation import write_report

    from .compare import comparison_frame, register_results, run_summary
    from .report import render_report

    plan = load_plan(args.plan)
    missing = []
    for a in plan.ablations:
        summary = run_summary(REPO, a.experiment_id)
        if summary is None:
            missing.append(a.experiment_id)
            continue
        register_results(REPO, plan, a, summary, args.date)
        write_bundle(repo_root=REPO, experiment_id=a.experiment_id, positive_class="fake", negative_class="real")
        write_report(REPO, a.evaluation_id, a.experiment_id, args.date)
        print(f"{a.experiment_id}: registered, STEP-041 inputs written, {a.evaluation_id} E1-E2 PASS")
    if missing:
        sys.exit(f"not trained yet: {', '.join(missing)}; the comparison needs every ablation")
    frame = comparison_frame(REPO, plan)
    OUT.mkdir(parents=True, exist_ok=True)
    frame.to_csv(OUT / "ablation_results.csv", index=False)
    (OUT / "ablation_report.md").write_text(render_report(frame, plan, args.date), encoding="utf-8")
    print(f"wrote ablation_results.csv and ablation_report.md to {OUT}")


def main() -> None:
    sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name, func in (("list", cmd_list), ("create", cmd_create), ("evaluate", cmd_evaluate)):
        p = sub.add_parser(name)
        p.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
        p.set_defaults(func=func)
        if name == "create":
            p.add_argument("--git-commit", default=None)
            p.add_argument("--timestamp", default=None)
        if name == "evaluate":
            p.add_argument("--date", default=dt.date.today().isoformat())
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
