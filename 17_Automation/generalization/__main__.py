"""STEP-047 generalization: cross-dataset (E8) and unseen-generator (E9) evaluation.

Usage (from 17_Automation/):
    python -m generalization datasets                         # list targets and image counts
    python -m generalization run                              # Kaggle GPU: MODEL0001 on every target dataset
    python -m generalization analyze                          # anywhere: E8 CSVs + cross_dataset_report.md
    python -m generalization unseen --experiment EXP0002 --evaluation EVAL0002   # anywhere, after EXP0002 syncs
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import yaml

from .config import load_config

REPO = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = REPO / "08_Evaluation/EVAL0001/generalization/config.yaml"


def cmd_datasets(args) -> None:
    from .inference import target_items

    config = load_config(args.config)
    for d in config.datasets:
        items = target_items(config, d, REPO)
        print(f"{d['name']}: {len(items)} images ({int(items['y_true'].sum())} fake / {int((items['y_true'] == 0).sum())} real), "
              f"{items['generator'].nunique()} generator value(s)")
    print(f"config SHA-256 {config.sha256[:12]}")


def cmd_run(args) -> None:
    import torch

    from classification_metrics import require_validated
    from robustness.inference import find_export, load_model

    from .inference import run

    config = load_config(args.config)
    require_validated(REPO / "08_Evaluation" / config.get("evaluation_id") / "prediction_validation_report.md")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu" and not args.allow_cpu:
        raise RuntimeError("no GPU visible; set the Kaggle accelerator to GPU, or pass --allow-cpu")
    export = find_export([Path(p) for p in config.get("model.search")], config.get("model.export_name"), config.get("model.export_sha256"))
    print(f"export: {export}")
    model, vocab = load_model(export, device)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    extra = {"git_commit": commit, "torch": torch.__version__, "export_path": str(export),
             "gpu": torch.cuda.get_device_name(0) if device == "cuda" else None}
    run(config, REPO, model, vocab, Path(args.config).resolve().parent, Path(config.get("reference.processed_root")),
        device=device, extra_manifest=extra)


def cmd_analyze(args) -> None:
    from .cross_dataset import dataset_frame, frozen_threshold, group_frame, reference_frame, relation_frame
    from .inference import MANIFEST_NAME, PREDICTIONS_DIR
    from .report import render_cross_dataset

    config = load_config(args.config)
    out = Path(args.config).resolve().parent
    manifest = json.loads((out / MANIFEST_NAME).read_text(encoding="utf-8"))
    if manifest["config_sha256"] != config.sha256:
        raise ValueError("config.yaml changed after the Kaggle run; rerun inference or restore the config")
    frames = {d["name"]: pd.read_csv(out / PREDICTIONS_DIR / f"{d['name']}.csv", keep_default_na=False) for d in config.datasets}
    threshold = frozen_threshold(config, REPO)
    reference = reference_frame(config, REPO)
    datasets = dataset_frame(frames, threshold, reference)
    groups = group_frame(frames, threshold, reference, config)
    relations = relation_frame(groups)
    for name, frame in (("cross_dataset_metrics.csv", datasets), ("cross_dataset_by_generator.csv", groups),
                        ("cross_dataset_by_relation.csv", relations)):
        frame.to_csv(out / name, index=False)
    (out / "cross_dataset_report.md").write_text(render_cross_dataset(datasets, groups, relations, manifest, config.raw, args.date), encoding="utf-8")
    print(f"wrote 3 CSVs and cross_dataset_report.md to {out}")


def cmd_unseen(args) -> None:
    from classification_metrics import require_validated

    from .report import render_unseen
    from .unseen import check_no_leakage, detection_frame, held_out_generators, load_predictions, paired_frame, ranking_auc

    exp_config = yaml.safe_load((REPO / "06_Experiments" / args.experiment / "config.yaml").read_text(encoding="utf-8"))
    split_csv = REPO / exp_config["split"]["assignments_csv"]
    eval_dir = REPO / "08_Evaluation" / args.evaluation
    require_validated(eval_dir / "prediction_validation_report.md")
    held = held_out_generators(split_csv.parent)
    leakage = check_no_leakage(pd.read_csv(split_csv, dtype=str, keep_default_na=False), held)
    source = REPO / "08_Evaluation" / args.experiment / "predictions.csv"
    val, test = load_predictions(source)
    reference = pd.read_csv(REPO / args.reference)
    reference = reference[reference["split"] == "test"]
    detection = detection_frame(val, test, held)
    paired = paired_frame(test, reference, held)
    auc = ranking_auc(val, test, held)
    out = eval_dir / "unseen_generator"
    out.mkdir(parents=True, exist_ok=True)
    detection.to_csv(out / "unseen_detection.csv", index=False)
    paired.to_csv(out / "unseen_paired.csv", index=False)
    summary = {"held_out": held, "leakage": leakage, "ranking_auc_vs_val_real": auc, "threshold": float(val["threshold"].iloc[0])}
    (out / "unseen_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    info = {"evaluation_id": args.evaluation, "experiment_id": args.experiment, "model_id": exp_config["model"]["model_id"],
            "split": f"{exp_config['dataset']['output_id']}_{exp_config['split']['split_id']}", "threshold": summary["threshold"],
            "source": source.relative_to(REPO).as_posix(), "reference_name": args.reference_name}
    (out / "unseen_report.md").write_text(render_unseen(detection, paired, leakage, auc, info, args.date), encoding="utf-8")
    print(f"wrote unseen-generator results to {out}")


def main() -> None:
    sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name, func in (("datasets", cmd_datasets), ("run", cmd_run), ("analyze", cmd_analyze)):
        p = sub.add_parser(name)
        p.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
        p.set_defaults(func=func)
        if name == "run":
            p.add_argument("--allow-cpu", action="store_true")
        if name == "analyze":
            p.add_argument("--date", default=dt.date.today().isoformat())
    p = sub.add_parser("unseen")
    p.add_argument("--experiment", default="EXP0002")
    p.add_argument("--evaluation", default="EVAL0002")
    p.add_argument("--reference", default="08_Evaluation/EXP0001/predictions.csv")
    p.add_argument("--reference-name", default="MODEL0001 (EXP0001)")
    p.add_argument("--date", default=dt.date.today().isoformat())
    p.set_defaults(func=cmd_unseen)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
