"""After the Kaggle run: register each finished ablation, validate its predictions, and compare with the baseline.

Each experiment is scored from its STEP-041 predictions at its own val-chosen threshold (the baseline's rule).
Differences are read against the seed replicate: a difference no larger than the seed's is not distinguishable from noise.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd

from classification_metrics import classification_row
from training.evaluation import expected_calibration_error

from .plan import Ablation, AblationPlan

METRICS = ["roc_auc", "pr_auc", "balanced_accuracy", "mcc", "f1", "recall", "specificity", "fnr", "fpr", "accuracy", "ece", "brier"]
LOWER_IS_BETTER = {"fnr", "fpr", "ece", "brier"}
BINS = 15


def run_summary(repo: Path, experiment_id: str) -> dict | None:
    path = repo / "06_Experiments" / experiment_id / "metrics" / "run_summary.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def _update(path: Path, key_col: str, key: str, changes: dict) -> None:
    rows = list(csv.reader(path.open(encoding="utf-8", newline="")))
    head = [h.strip() for h in rows[0]]
    row = next(r for r in rows[1:] if r and r[head.index(key_col)].strip() == key)
    for col, val in changes.items():
        row[head.index(col)] = val
    with path.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)


def register_results(repo: Path, plan: AblationPlan, a: Ablation, summary: dict, date: str) -> None:
    """STEP-040 registration from run_summary.json: experiment completed, model trained."""

    val, test = summary["metrics"]["val"], summary["metrics"]["test"]
    minutes = round(summary["training_seconds"] / 60, 1)
    results = (f"test ROC-AUC {test['roc_auc']:.3f}; balanced accuracy {test['balanced_accuracy']:.3f}; MCC {test['mcc']:.3f}; "
               f"val ROC-AUC {val['roc_auc']:.3f} (threshold {summary['metrics']['threshold']['value']:.3f}, validation only)")
    _update(repo / "06_Experiments/experiment_registry.csv", "Experiment ID", a.experiment_id, {
        "Results": results, "Best Epoch": str(summary["best_epoch"]), "Training Time": f"{minutes} min ({summary['training_seconds']} s)",
        "Status": "completed", "Next Actions": "Compared in 08_Evaluation/ablations/ablation_report.md.", "Updated": date})
    best = summary["artifacts"]["best"]
    _update(repo / "05_Models/model_registry.csv", "Model ID", a.model_id, {
        "Training Time": f"{minutes} min ({summary['training_seconds']} s)", "GPU": str(summary["environment"].get("gpu") or ""),
        "Metrics": results, "Checkpoint": f"{plan.artifact_slug(a.experiment_id)}:{best['name']} (epoch {summary['best_epoch']}, sha256 {best['sha256'][:12]}...)",
        "Git Commit": summary["git"]["head"] or summary["git"]["recorded"],
        "Export Path": f"{plan.artifact_slug(a.experiment_id)}:{summary['artifacts']['export_pkl']['name']}",
        "Status": "trained", "Updated": date})


def score(predictions: pd.DataFrame, split: str) -> dict:
    part = predictions[predictions["split"] == split]
    y, p = part["y_true"].to_numpy(), part["y_prob"].to_numpy()
    row = classification_row(split, y, p, part["y_pred"].to_numpy(), float(part["threshold"].iloc[0]), "fake")
    row["ece"] = expected_calibration_error(y, p, BINS)
    row["brier"] = float(np.mean((p - y) ** 2))
    return row


def comparison_frame(repo: Path, plan: AblationPlan) -> pd.DataFrame:
    rows = []
    entries = [(plan.baseline, "baseline", "", "")] + [(a.experiment_id, a.factor, a.question, a.model_id) for a in plan.ablations]
    for exp, factor, question, model in entries:
        predictions = pd.read_csv(repo / "08_Evaluation" / exp / "predictions.csv")
        summary = run_summary(repo, exp) or {}
        test, val = score(predictions, "test"), score(predictions, "val")
        rows.append({
            "experiment_id": exp, "factor": factor, "question": question, "model_id": model or "MODEL0001",
            "threshold": test["threshold"], "best_epoch": summary.get("best_epoch"),
            "training_minutes": round(summary.get("training_seconds", float("nan")) / 60, 1),
            "early_stopped": summary.get("early_stopped"),
            **{m: test[m] for m in METRICS}, "val_roc_auc": val["roc_auc"], "val_balanced_accuracy": val["balanced_accuracy"],
        })
    frame = pd.DataFrame(rows)
    base = frame.iloc[0]
    noise = frame[frame["experiment_id"] == plan.noise_reference].iloc[0]
    for m in METRICS:
        frame[f"delta_{m}"] = frame[m] - base[m]
    for m in METRICS:
        floor = abs(noise[m] - base[m])
        frame[f"beyond_seed_{m}"] = [
            bool(abs(d) > floor) if exp not in {plan.baseline, plan.noise_reference} else None
            for exp, d in zip(frame["experiment_id"], frame[f"delta_{m}"])
        ]
    return frame


def direction(metric: str, delta: float) -> str:
    if delta == 0:
        return "same"
    better = delta < 0 if metric in LOWER_IS_BETTER else delta > 0
    return "better" if better else "worse"
