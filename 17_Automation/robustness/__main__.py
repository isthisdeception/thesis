"""STEP-046 robustness evaluation.

Usage (from 17_Automation/):
    python -m robustness conditions --config ../08_Evaluation/EVAL0001/robustness/config.yaml
    python -m robustness run --config ... [--processed-root DIR] [--export PATH] [--work-dir DIR]   # Kaggle, GPU
    python -m robustness analyze --config ...                                                      # anywhere
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

from .config import load_config

REPO = Path(__file__).resolve().parents[2]


def _out_dir(config_path: Path) -> Path:
    return config_path.resolve().parent


def cmd_conditions(args) -> None:
    config = load_config(args.config)
    for c in config.conditions:
        print(c.id)
    print(f"{len(config.conditions)} conditions (config SHA-256 {config.sha256[:12]})")


def cmd_run(args) -> None:
    import torch

    from classification_metrics import require_validated

    from .inference import find_export, load_model, run

    config = load_config(args.config)
    require_validated(REPO / "08_Evaluation" / config.get("evaluation_id") / "prediction_validation_report.md")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu" and not args.allow_cpu:
        raise RuntimeError("no GPU visible; set the Kaggle accelerator to GPU, or pass --allow-cpu")
    export = Path(args.export) if args.export else find_export(
        [Path(p) for p in args.search], config.get("model.export_name"), config.get("model.export_sha256"))
    print(f"export: {export}")
    model, vocab = load_model(export, device)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    extra = {"git_commit": commit, "torch": torch.__version__, "export_path": str(export),
             "gpu": torch.cuda.get_device_name(0) if device == "cuda" else None}
    try:
        import fastai

        extra["fastai"] = fastai.__version__
    except ImportError:
        pass
    run(config, REPO, Path(args.processed_root or config.get("data.processed_root")), model, vocab,
        Path(args.work_dir), _out_dir(Path(args.config)), device=device, extra_manifest=extra)


def cmd_analyze(args) -> None:
    from .analysis import flips_frame, group_frame, metrics_frame, summary_frame
    from .inference import MANIFEST_NAME, PROBS_NAME, test_items
    from .report import render_report

    config = load_config(args.config)
    out = _out_dir(Path(args.config))
    wide = pd.read_csv(out / PROBS_NAME)
    manifest = json.loads((out / MANIFEST_NAME).read_text(encoding="utf-8"))
    if manifest["config_sha256"] != config.sha256:
        raise ValueError("config.yaml changed after the Kaggle run; rerun inference or restore the config")
    items = test_items(config, REPO)
    index = pd.read_csv(REPO / config.get("data.metadata_index"))
    metrics = metrics_frame(wide, items, config)
    flips = flips_frame(wide, items, config)
    groups = group_frame(wide, items, index, config)
    summary = summary_frame(metrics, flips, groups, config)
    for name, frame in (("robustness_metrics.csv", metrics), ("robustness_flips.csv", flips),
                        ("robustness_by_group.csv", groups), ("robustness_summary.csv", summary)):
        frame.to_csv(out / name, index=False)
    report = render_report(metrics, flips, summary, manifest, float(config.get("analysis.tolerance")),
                           float(config.get("analysis.ranking_kept")), args.date)
    (out / "robustness_report.md").write_text(report, encoding="utf-8")
    print(f"wrote 4 CSVs and robustness_report.md to {out}")


def main() -> None:
    # Notebook `!` cells read stdout through a pipe; without this, progress lines appear only at the end.
    sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    default_config = REPO / "08_Evaluation/EVAL0001/robustness/config.yaml"

    p = sub.add_parser("conditions")
    p.add_argument("--config", type=Path, default=default_config)
    p.set_defaults(func=cmd_conditions)

    p = sub.add_parser("run")
    p.add_argument("--config", type=Path, default=default_config)
    p.add_argument("--processed-root", default=None)
    p.add_argument("--export", default=None, help="path to the export; default: search --search roots")
    # Not all of /kaggle/input: walking the image dataset on Kaggle's mount takes many minutes.
    p.add_argument("--search", nargs="+", default=["/kaggle/input/datasets/isthisdeception/thesis-experiment-artifacts",
                                                   "/kaggle/input/thesis-experiment-artifacts"])
    p.add_argument("--work-dir", default="/kaggle/working/robustness_work")
    p.add_argument("--allow-cpu", action="store_true")
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("analyze")
    p.add_argument("--config", type=Path, default=default_config)
    p.add_argument("--date", default=dt.date.today().isoformat())
    p.set_defaults(func=cmd_analyze)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
