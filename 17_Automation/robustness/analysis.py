"""Phase E7 degradation, recovery, and failure patterns from the per-condition probabilities.

Decisions use the frozen threshold from predictions.csv; no threshold is chosen on perturbed data.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from classification_metrics import classification_row
from failure_analysis.analysis import MIN_GROUP, join_metadata
from training.evaluation import expected_calibration_error

from .config import CLEAN, RobustnessConfig, level_label

DELTA_FIELDS = ["roc_auc", "pr_auc", "balanced_accuracy", "mcc", "f1", "recall", "specificity", "fpr", "fnr", "ece", "brier", "mean_prob"]
CALIBRATION_BINS = 15


def _frame(wide: pd.DataFrame, items: pd.DataFrame, index: pd.DataFrame) -> pd.DataFrame:
    if wide["id"].tolist() != items["id"].tolist():
        raise ValueError("robustness_probs.csv ids do not match the test items in order")
    return join_metadata(items.copy(), index)


def metrics_frame(wide: pd.DataFrame, items: pd.DataFrame, config: RobustnessConfig) -> pd.DataFrame:
    y = items["y_true"].to_numpy().astype(int)
    threshold = float(items["threshold"].iloc[0])
    rows = []
    for c in config.conditions:
        if c.id not in wide.columns:
            raise ValueError(f"condition {c.id} missing from robustness_probs.csv")
        p = wide[c.id].to_numpy(dtype=float)
        row = classification_row(c.id, y, p, (p >= threshold).astype(int), threshold, config.get("model.positive_class"))
        row.pop("split")
        rows.append({
            "condition": c.id,
            "perturbation": c.perturbation,
            "kind": c.kind,
            "level": "" if c.level is None else level_label(c.level),
            "rank": c.rank,
            **row,
            "ece": expected_calibration_error(y, p, CALIBRATION_BINS),
            "brier": float(np.mean((p - y) ** 2)),
            "mean_prob": float(p.mean()),
        })
    frame = pd.DataFrame(rows)
    clean = frame[frame["condition"] == CLEAN].iloc[0]
    for name in DELTA_FIELDS:
        frame[f"delta_{name}"] = frame[name] - clean[name]
    return frame


def flips_frame(wide: pd.DataFrame, items: pd.DataFrame, config: RobustnessConfig) -> pd.DataFrame:
    """Decision changes against the clean run, split by direction and correctness."""

    y = items["y_true"].to_numpy().astype(int)
    threshold = float(items["threshold"].iloc[0])
    base_p = wide[CLEAN].to_numpy(dtype=float)
    base = base_p >= threshold
    rows = []
    for c in config.conditions:
        p = wide[c.id].to_numpy(dtype=float)
        pred = p >= threshold
        shift = p - base_p
        rows.append({
            "condition": c.id,
            "perturbation": c.perturbation,
            "rank": c.rank,
            "flips": int((pred != base).sum()),
            "flip_rate": float((pred != base).mean()),
            "to_fake": int((pred & ~base).sum()),
            "to_real": int((~pred & base).sum()),
            "newly_wrong": int(((pred != y) & (base == y)).sum()),
            "newly_right": int(((pred == y) & (base != y)).sum()),
            "mean_shift": float(shift.mean()),
            "mean_shift_real": float(shift[y == 0].mean()),
            "mean_shift_fake": float(shift[y == 1].mean()),
        })
    return pd.DataFrame(rows)


def group_frame(wide: pd.DataFrame, items: pd.DataFrame, index: pd.DataFrame, config: RobustnessConfig) -> pd.DataFrame:
    """Error rate per generator (FNR) and real source (FPR) under every condition."""

    meta = _frame(wide, items, index)
    threshold = float(items["threshold"].iloc[0])
    y = meta["y_true"].to_numpy().astype(int)
    rows = []
    for c in config.conditions:
        err = (wide[c.id].to_numpy(dtype=float) >= threshold).astype(int) != y
        part = pd.DataFrame({"subgroup": meta["subgroup"], "y_true": y, "error": err})
        for (label, group), g in part.groupby(["y_true", "subgroup"], sort=True):
            rows.append({
                "condition": c.id,
                "perturbation": c.perturbation,
                "rank": c.rank,
                "true_label": "fake" if label == 1 else "real",
                "group": group,
                "n": len(g),
                "errors": int(g["error"].sum()),
                "error_rate": float(g["error"].mean()),
                "small_group": len(g) < MIN_GROUP,
            })
    frame = pd.DataFrame(rows)
    clean = frame[frame["condition"] == CLEAN].set_index(["true_label", "group"])["error_rate"]
    frame["delta_error_rate"] = frame["error_rate"] - [clean[(t, g)] for t, g in zip(frame["true_label"], frame["group"])]
    return frame


def summary_frame(metrics: pd.DataFrame, flips: pd.DataFrame, groups: pd.DataFrame, config: RobustnessConfig) -> pd.DataFrame:
    """One row per perturbation: tolerance level, worst level, failure pattern, most affected group."""

    tol = float(config.get("analysis.tolerance"))
    kept = float(config.get("analysis.ranking_kept"))
    rows = []
    for p in config.raw["perturbations"]:
        m = metrics[metrics["perturbation"] == p["name"]].sort_values("rank")
        within = m["delta_balanced_accuracy"] >= -tol
        tolerated = m[within.cumprod().astype(bool)]
        worst = m.loc[m["balanced_accuracy"].idxmin()]
        f = flips[flips["condition"] == worst["condition"]].iloc[0]
        g = groups[(groups["condition"] == worst["condition"]) & ~groups["small_group"]]
        g = g.sort_values(["delta_error_rate", "group"], ascending=[False, True]).iloc[0]
        if worst["delta_balanced_accuracy"] >= -tol:
            pattern = "robust"
        elif worst["delta_roc_auc"] >= -kept:
            pattern = "threshold_shift"
        else:
            pattern = "ranking_loss"
        rows.append({
            "perturbation": p["name"],
            "kind": p["kind"],
            "levels": ", ".join(level_label(x) for x in p["levels"]),
            "tolerance_level": tolerated["level"].iloc[-1] if len(tolerated) else "",
            "worst_level": worst["level"],
            "worst_balanced_accuracy": worst["balanced_accuracy"],
            "delta_balanced_accuracy": worst["delta_balanced_accuracy"],
            "delta_roc_auc": worst["delta_roc_auc"],
            "delta_fnr": worst["delta_fnr"],
            "delta_fpr": worst["delta_fpr"],
            "delta_ece": worst["delta_ece"],
            "flip_rate": f["flip_rate"],
            "flip_direction": "to_fake" if f["to_fake"] > f["to_real"] else ("to_real" if f["to_real"] > f["to_fake"] else "even"),
            "pattern": pattern,
            "most_affected_group": f"{g['true_label']}:{g['group']}",
            "most_affected_delta": g["delta_error_rate"],
        })
    return pd.DataFrame(rows)
