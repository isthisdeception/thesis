"""Phase E8 metrics per target dataset and per generator, at MODEL0001's frozen threshold.

Datasets with one class get the rates that class supports (recall/FNR for fake-only, specificity/FPR for real-only).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from classification_metrics import classification_row
from failure_analysis.analysis import MIN_GROUP, wilson_interval
from training.evaluation import expected_calibration_error

from .config import GeneralizationConfig

REFERENCE = "DS0001"
CALIBRATION_BINS = 15


def reference_frame(config: GeneralizationConfig, repo_root) -> pd.DataFrame:
    ref = pd.read_csv(repo_root / config.get("reference.predictions"))
    ref = ref[ref["split"] == config.get("reference.split")]
    return pd.DataFrame({"dataset": REFERENCE, "id": ref["processed_path"], "y_true": ref["y_true"],
                         "generator": ref["generator"], "y_prob": ref["y_prob"]}).reset_index(drop=True)


def frozen_threshold(config: GeneralizationConfig, repo_root) -> float:
    ref = pd.read_csv(repo_root / config.get("reference.predictions"))
    values = ref["threshold"].unique()
    if len(values) != 1:
        raise ValueError("reference predictions carry more than one threshold")
    return float(values[0])


def _rate_row(name: str, y: np.ndarray, p: np.ndarray, threshold: float) -> dict:
    pred = (p >= threshold).astype(int)
    n_pos, n_neg = int(y.sum()), int((y == 0).sum())
    row: dict = {"dataset": name, "n": len(y), "n_fake": n_pos, "n_real": n_neg, "threshold": threshold, "mean_prob": float(p.mean())}
    if n_pos and n_neg:
        full = classification_row(name, y, p, pred, threshold, "fake")
        row.update({k: full[k] for k in ("recall", "specificity", "fnr", "fpr", "precision", "f1", "balanced_accuracy", "mcc", "roc_auc", "pr_auc", "accuracy")})
        row["ece"] = expected_calibration_error(y, p, CALIBRATION_BINS)
    else:
        row.update({k: float("nan") for k in ("recall", "specificity", "fnr", "fpr", "precision", "f1", "balanced_accuracy", "mcc", "roc_auc", "pr_auc", "accuracy", "ece")})
        correct = int((pred == y).sum())
        row["accuracy"] = correct / len(y)
        if n_pos:
            row["recall"], row["fnr"] = correct / n_pos, 1 - correct / n_pos
        else:
            row["specificity"], row["fpr"] = correct / n_neg, 1 - correct / n_neg
    errors = int((pred != y).sum())
    row["errors"] = errors
    row["error_ci_low"], row["error_ci_high"] = wilson_interval(errors, len(y))
    return row


def dataset_frame(frames: dict[str, pd.DataFrame], threshold: float, reference: pd.DataFrame) -> pd.DataFrame:
    rows = [_rate_row(REFERENCE, reference["y_true"].to_numpy(), reference["y_prob"].to_numpy(), threshold)]
    for name, f in frames.items():
        rows.append(_rate_row(name, f["y_true"].to_numpy().astype(int), f["y_prob"].to_numpy(dtype=float), threshold))
    out = pd.DataFrame(rows)
    out.insert(1, "role", ["in_distribution"] + ["cross_dataset"] * (len(out) - 1))
    return out


def group_frame(frames: dict[str, pd.DataFrame], threshold: float, reference: pd.DataFrame, config: GeneralizationConfig) -> pd.DataFrame:
    """Error rate per (dataset, class, generator): FNR for fake generators, FPR for real sources."""

    by_name = {d["name"]: d for d in config.datasets}
    rows = []
    for name, f in {REFERENCE: reference, **frames}.items():
        dataset = by_name.get(name, {})
        err = (f["y_prob"].to_numpy(dtype=float) >= threshold).astype(int) != f["y_true"].to_numpy().astype(int)
        part = pd.DataFrame({"y_true": f["y_true"].astype(int), "generator": f["generator"].astype(str), "error": err, "p": f["y_prob"]})
        for (label, gen), g in part.groupby(["y_true", "generator"], sort=True):
            n, errors = len(g), int(g["error"].sum())
            low, high = wilson_interval(errors, n)
            klass = "fake" if label == 1 else "real"
            rows.append({
                "dataset": name,
                "true_label": klass,
                "generator": gen,
                "relation": config.relation(dataset, gen, klass) if name != REFERENCE else ("seen" if klass == "fake" else "real"),
                "n": n,
                "errors": errors,
                "error_rate": errors / n,
                "ci_low": low,
                "ci_high": high,
                "mean_prob": float(g["p"].mean()),
                "small_group": n < MIN_GROUP,
            })
    return pd.DataFrame(rows)


def relation_frame(groups: pd.DataFrame) -> pd.DataFrame:
    """Pooled FNR of fake images by relation to the training generators, cross-dataset only."""

    fake = groups[(groups["true_label"] == "fake") & (groups["dataset"] != REFERENCE)]
    rows = []
    for relation, g in fake.groupby("relation", sort=True):
        n, errors = int(g["n"].sum()), int(g["errors"].sum())
        low, high = wilson_interval(errors, n)
        rows.append({"relation": relation, "datasets": ", ".join(sorted(g["dataset"].unique())), "generators": len(g),
                     "n": n, "errors": errors, "fnr": errors / n, "ci_low": low, "ci_high": high})
    return pd.DataFrame(rows)
