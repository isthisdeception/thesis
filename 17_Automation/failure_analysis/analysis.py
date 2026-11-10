"""Phase E6 confusion data and Phase E12 failure grouping from validated predictions.

Decisions are the saved `y_pred`, as in STEP-043. Nothing here asserts a cause; groups only show where errors occur.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

LABELS = {0: "real", 1: "fake"}
MIN_GROUP = 30
TOP_CASES = 20
NEAR_THRESHOLD = 0.1
HIGH_CONFIDENCE = 0.9


def wilson_interval(errors: int, n: int, z: float = 1.959964) -> tuple[float, float]:
    if n == 0:
        return float("nan"), float("nan")
    p = errors / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return float(max(0.0, centre - half)), float(min(1.0, centre + half))


def join_metadata(predictions: pd.DataFrame, index: pd.DataFrame) -> pd.DataFrame:
    """Attach identity and source fields from the preprocessing index by content hash."""

    meta = index[["content_hash", "identity", "original_size", "relative_path"]].drop_duplicates("content_hash")
    frame = predictions.merge(meta, left_on="id", right_on="content_hash", how="left", validate="one_to_one")
    missing = int(frame["content_hash"].isna().sum())
    if missing:
        raise ValueError(f"{missing} prediction(s) have no metadata row")
    frame = frame.drop(columns="content_hash")
    frame["source_format"] = frame["relative_path"].str.rsplit(".", n=1).str[-1].str.lower()
    # Real images have generator "none"; their source dataset is the identity prefix (ffhq, celebahq, metfaces).
    real_source = frame["identity"].astype(str).str.split("_").str[0]
    frame["subgroup"] = np.where(frame["y_true"] == 1, frame["generator"], real_source)
    frame["error"] = frame["y_pred"] != frame["y_true"]
    frame["confidence"] = np.where(frame["y_pred"] == 1, frame["y_prob"], 1 - frame["y_prob"])
    return frame


def confusion_frame(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for split, part in frame.groupby("split", sort=True):
        total = len(part)
        for t in (1, 0):
            support = int((part["y_true"] == t).sum())
            for p in (1, 0):
                count = int(((part["y_true"] == t) & (part["y_pred"] == p)).sum())
                rows.append({
                    "split": split,
                    "true_label": LABELS[t],
                    "predicted_label": LABELS[p],
                    "count": count,
                    "share_of_true": count / support if support else float("nan"),
                    "share_of_all": count / total,
                })
    return pd.DataFrame(rows)


def per_class_frame(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for split, part in frame.groupby("split", sort=True):
        for c in (1, 0):
            support = int((part["y_true"] == c).sum())
            predicted = int((part["y_pred"] == c).sum())
            correct = int(((part["y_true"] == c) & (part["y_pred"] == c)).sum())
            precision = correct / predicted if predicted else 0.0
            recall = correct / support if support else 0.0
            rows.append({
                "split": split,
                "class": LABELS[c],
                "support": support,
                "predicted": predicted,
                "correct": correct,
                "errors": support - correct,
                "precision": precision,
                "recall": recall,
                "f1": 2 * precision * recall / (precision + recall) if precision + recall else 0.0,
                "error_rate": (support - correct) / support if support else float("nan"),
            })
    return pd.DataFrame(rows)


def group_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Error rate per generator (fake) and per source dataset (real), with Wilson 95% intervals."""

    rows = []
    for (split, label), part in frame.groupby(["split", "y_true"], sort=True):
        class_errors = int(part["error"].sum())
        for name, g in part.groupby("subgroup", sort=True):
            n, errors = len(g), int(g["error"].sum())
            low, high = wilson_interval(errors, n)
            rows.append({
                "split": split,
                "true_label": LABELS[int(label)],
                "group_type": "generator" if label == 1 else "real_source",
                "group": name,
                "n": n,
                "errors": errors,
                "error_rate": errors / n,
                "ci_low": low,
                "ci_high": high,
                "share_of_class_errors": errors / class_errors if class_errors else 0.0,
                "mean_prob": float(g["y_prob"].mean()),
                "median_prob": float(g["y_prob"].median()),
                "small_group": n < MIN_GROUP,
            })
    return pd.DataFrame(rows)


def error_summary_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """FP and FN counts split by how far the probability sits from the threshold."""

    rows = []
    for split, part in frame.groupby("split", sort=True):
        threshold = float(part["threshold"].iloc[0])
        for kind, label in (("false_positive", 0), ("false_negative", 1)):
            e = part[part["error"] & (part["y_true"] == label)]
            near = (e["y_prob"] - threshold).abs() < NEAR_THRESHOLD
            high = e["confidence"] >= HIGH_CONFIDENCE
            rows.append({
                "split": split,
                "error_type": kind,
                "count": len(e),
                "near_threshold": int(near.sum()),
                "high_confidence": int(high.sum()),
                "near_threshold_share": float(near.mean()) if len(e) else float("nan"),
                "high_confidence_share": float(high.mean()) if len(e) else float("nan"),
                "mean_prob": float(e["y_prob"].mean()) if len(e) else float("nan"),
                "mean_confidence": float(e["confidence"].mean()) if len(e) else float("nan"),
            })
    return pd.DataFrame(rows)


def error_cases_frame(frame: pd.DataFrame, top: int = TOP_CASES) -> pd.DataFrame:
    """Most confident FP and FN per split, for manual review (E12). Ties break by id."""

    parts = []
    for split, part in frame.groupby("split", sort=True):
        for kind, label in (("false_positive", 0), ("false_negative", 1)):
            e = part[part["error"] & (part["y_true"] == label)]
            e = e.sort_values(["confidence", "id"], ascending=[False, True]).head(top)
            parts.append(e.assign(error_type=kind, rank=range(1, len(e) + 1)))
    cols = ["split", "error_type", "rank", "id", "processed_path", "subgroup", "identity", "y_true", "y_prob", "y_pred", "confidence", "threshold"]
    return pd.concat(parts, ignore_index=True)[cols]


def metadata_coverage(frame: pd.DataFrame, split: str) -> dict:
    """What the metadata can and cannot support for the E12 categories."""

    part = frame[frame["split"] == split]
    counts = part["identity"].value_counts()
    repeated = part[part["identity"].isin(counts[counts > 1].index)]
    return {
        "original_sizes": sorted(part["original_size"].unique().tolist()),
        "source_formats": sorted(part["source_format"].unique().tolist()),
        "repeated_identity_images": int(len(repeated)),
        "repeated_identity_groups": sorted(repeated["subgroup"].unique().tolist()),
        "repeated_identity_error_rate": float(repeated["error"].mean()) if len(repeated) else float("nan"),
    }
