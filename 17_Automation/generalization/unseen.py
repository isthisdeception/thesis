"""Phase E9 unseen-generator evaluation from a held-out experiment's saved predictions (no new inference).

The held-out generators come from the split's split_config.json. Thresholds are the experiment's val-chosen one.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from failure_analysis.analysis import wilson_interval


class GeneratorLeakageError(ValueError):
    """A held-out generator appears in train or val, so the result would not measure an unseen generator."""


def held_out_generators(split_dir: Path) -> list[str]:
    held = json.loads((split_dir / "split_config.json").read_text(encoding="utf-8")).get("held_out_generators") or []
    if not held:
        raise ValueError(f"{split_dir}: split_config.json lists no held_out_generators")
    return list(held)


def check_no_leakage(assignments: pd.DataFrame, held: list[str]) -> dict:
    counts = {p: assignments[assignments["partition"] == p]["generator"].value_counts().to_dict() for p in ("train", "val", "test")}
    leaked = {p: {g: counts[p][g] for g in held if g in counts[p]} for p in ("train", "val")}
    if any(leaked.values()):
        raise GeneratorLeakageError(f"held-out generator(s) found outside test: {leaked}")
    test_gens = set(counts["test"])
    return {"held_out": held, "train_generators": sorted(set(counts["train"]) - {"none"}),
            "test_generators": sorted(test_gens), "test_only_held_out_fakes": test_gens <= set(held) | {"none"}}


def load_predictions(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Val and test rows of a STEP-041 predictions.csv; `id` becomes the processed path for cross-model joins."""

    frame = pd.read_csv(path).assign(generator=lambda f: f["generator"].astype(str))
    frame = frame.rename(columns={"id": "content_hash"}).assign(id=lambda f: f["processed_path"])
    val = frame[frame["split"] == "val"].reset_index(drop=True)
    test = frame[frame["split"] == "test"].reset_index(drop=True)
    if val.empty or test.empty:
        raise ValueError(f"{path}: needs both val and test rows")
    return val, test


def _rate(name: str, kind: str, role: str, g: pd.DataFrame) -> dict:
    n = len(g)
    correct = int((g["y_pred"] == g["y_true"]).sum())
    low, high = wilson_interval(correct, n)
    return {"group": name, "true_label": kind, "role": role, "n": n, "correct": correct,
            "rate": correct / n, "ci_low": low, "ci_high": high,
            "mean_prob": float(g["y_prob"].mean()), "median_prob": float(g["y_prob"].median())}


def detection_frame(val: pd.DataFrame, test: pd.DataFrame, held: list[str]) -> pd.DataFrame:
    """Recall per generator (fake) and specificity (real). Unseen rows come from test, seen rows from val."""

    rows = []
    for gen in held:
        g = test[(test["generator"] == gen) & (test["y_true"] == 1)]
        if len(g):
            rows.append(_rate(gen, "fake", "unseen (test)", g))
    seen = val[val["y_true"] == 1]
    for gen, g in seen.groupby("generator", sort=True):
        rows.append(_rate(gen, "fake", "seen (val)", g))
    rows.append(_rate("all seen generators", "fake", "seen (val)", seen))
    real = val[val["y_true"] == 0]
    if len(real):
        rows.append(_rate("real", "real", "real (val)", real))
    return pd.DataFrame(rows)


def paired_frame(test: pd.DataFrame, reference: pd.DataFrame, held: list[str]) -> pd.DataFrame:
    """Same images, two models: the reference model saw the generator in training, the held-out model did not."""

    ref = reference[(reference["generator"].isin(held)) & (reference["y_true"] == 1)]
    both = ref.merge(test, on="processed_path", suffixes=("_ref", "_held"))
    rows = []
    for gen, g in both.groupby("generator_ref", sort=True):
        r, h = g["y_pred_ref"].astype(bool), g["y_pred_held"].astype(bool)
        rows.append({
            "generator": gen, "n": len(g),
            "recall_reference": float(r.mean()), "recall_held_out": float(h.mean()),
            "both_detected": int((r & h).sum()), "only_reference": int((r & ~h).sum()),
            "only_held_out": int((~r & h).sum()), "neither": int((~r & ~h).sum()),
            "mean_prob_reference": float(g["y_prob_ref"].mean()), "mean_prob_held_out": float(g["y_prob_held"].mean()),
        })
    return pd.DataFrame(rows)


def ranking_auc(val: pd.DataFrame, test: pd.DataFrame, held: list[str]) -> float:
    """ROC-AUC of unseen test fakes against val real images. Val reals also set the threshold: indicative only."""

    fakes = test[(test["generator"].isin(held)) & (test["y_true"] == 1)]["y_prob"]
    reals = val[val["y_true"] == 0]["y_prob"]
    if fakes.empty or reals.empty:
        return float("nan")
    y = np.r_[np.ones(len(fakes)), np.zeros(len(reals))]
    return float(roc_auc_score(y, np.r_[fakes.to_numpy(), reals.to_numpy()]))
