"""Evaluation-input tables derived from saved probabilities. No model, no figures."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_curve, roc_curve

from training.evaluation import calibration_table


def _as_binary(frame: pd.DataFrame, positive_class: str) -> pd.DataFrame:
    missing = [c for c in ("content_hash", "class_label", "prob_positive", "pred_positive", "threshold", "processed_path") if c not in frame.columns]
    if missing:
        raise ValueError(f"prediction file is missing column(s): {', '.join(missing)}")
    out = pd.DataFrame(
        {
            "id": frame["content_hash"].astype(str),
            "processed_path": frame["processed_path"].astype(str),
            "generator": frame["generator"].astype(str) if "generator" in frame.columns else "",
            "y_true": (frame["class_label"].astype(str) == positive_class).astype(int),
            "y_prob": frame["prob_positive"].astype(float),
            "y_pred": frame["pred_positive"].astype(int),
            "threshold": frame["threshold"].astype(float),
        }
    )
    if out["id"].duplicated().any():
        raise ValueError(f"{int(out['id'].duplicated().sum())} duplicate prediction id(s)")
    if not out["y_prob"].between(0.0, 1.0).all() or out["y_prob"].isna().any():
        raise ValueError("y_prob must be finite and inside [0, 1]")
    if not set(out["y_true"]).issubset({0, 1}) or not set(out["y_pred"]).issubset({0, 1}):
        raise ValueError("y_true and y_pred must be 0 or 1")
    thresholds = out["threshold"].unique()
    if len(thresholds) != 1:
        raise ValueError(f"a prediction file must use one threshold, found {thresholds.tolist()}")
    expected = (out["y_prob"] >= float(thresholds[0])).astype(int)
    disagree = out["y_pred"] != expected
    # The CSV stores rounded probabilities, so a saved decision can sit a few
    # billionths on the other side of the threshold. Far disagreements are real errors.
    far = disagree & (out["y_prob"] - float(thresholds[0])).abs().gt(1e-5)
    if far.any():
        raise ValueError(f"{int(far.sum())} prediction(s) disagree with the threshold by more than 1e-5")
    return out


def confusion_rows(split: str, frame: pd.DataFrame, positive_class: str, negative_class: str) -> list[dict]:
    names = {1: positive_class, 0: negative_class}
    rows = []
    for true_value, true_name in names.items():
        for pred_value, pred_name in names.items():
            count = int(((frame["y_true"] == true_value) & (frame["y_pred"] == pred_value)).sum())
            rows.append(
                {
                    "split": split,
                    "true_label": true_name,
                    "predicted_label": pred_name,
                    "threshold": float(frame["threshold"].iloc[0]),
                    "count": count,
                }
            )
    return rows


def roc_rows(split: str, frame: pd.DataFrame) -> list[dict]:
    fpr, tpr, thresholds = roc_curve(frame["y_true"], frame["y_prob"])
    return [
        {"split": split, "fpr": float(f), "tpr": float(t), "threshold": float(th)}
        for f, t, th in zip(fpr, tpr, thresholds)
    ]


def pr_rows(split: str, frame: pd.DataFrame) -> list[dict]:
    precision, recall, thresholds = precision_recall_curve(frame["y_true"], frame["y_prob"])
    # precision_recall_curve returns one more precision/recall point than thresholds.
    rows = [
        {"split": split, "precision": float(p), "recall": float(r), "threshold": float(th)}
        for p, r, th in zip(precision[:-1], recall[:-1], thresholds)
    ]
    rows.append({"split": split, "precision": float(precision[-1]), "recall": float(recall[-1]), "threshold": float("nan")})
    return rows


def calibration_rows(split: str, frame: pd.DataFrame, bins: int) -> list[dict]:
    table = calibration_table(frame["y_true"].to_numpy(), frame["y_prob"].to_numpy(), bins)
    for row in table:
        row["split"] = split
    return table


def gradcam_sample(frame: pd.DataFrame, per_role: int = 2) -> pd.DataFrame:
    """A fixed, small set of cases for a later Grad-CAM run. No maps are computed here.

    Ties break by image id, so the same prediction file always selects the same rows.
    """

    roles = {
        "true_positive": frame[(frame["y_true"] == 1) & (frame["y_pred"] == 1)].sort_values(["y_prob", "id"], ascending=[False, True]),
        "true_negative": frame[(frame["y_true"] == 0) & (frame["y_pred"] == 0)].sort_values(["y_prob", "id"], ascending=[True, True]),
        "false_positive": frame[(frame["y_true"] == 0) & (frame["y_pred"] == 1)].sort_values(["y_prob", "id"], ascending=[False, True]),
        "false_negative": frame[(frame["y_true"] == 1) & (frame["y_pred"] == 0)].sort_values(["y_prob", "id"], ascending=[True, True]),
    }
    chosen = []
    for role, rows in roles.items():
        for _, row in rows.head(per_role).iterrows():
            chosen.append({**row.to_dict(), "role": role, "target_layer": "layer4"})
    if not chosen:
        raise ValueError("no rows available for a Grad-CAM sample")
    return pd.DataFrame(chosen)
