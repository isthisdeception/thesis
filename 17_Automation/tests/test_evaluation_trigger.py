"""STEP-041: evaluation inputs derived from saved predictions, plus Grad-CAM maps as numbers."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest
import torch
from sklearn.metrics import roc_auc_score

from evaluation_trigger.bundle import write_bundle
from evaluation_trigger.curves import _as_binary, gradcam_sample
from evaluation_trigger.gradcam import grad_cam_map, maps_to_rows

REPO = Path(__file__).resolve().parents[2]


def test_exp0001_bundle_matches_saved_auc() -> None:
    manifest = write_bundle(repo_root=REPO, experiment_id="EXP0001", positive_class="fake", negative_class="real")
    out = REPO / "08_Evaluation" / "EXP0001"
    predictions = pd.read_csv(out / "predictions.csv")
    stored = json.loads((REPO / "06_Experiments/EXP0001/metrics/test_metrics.json").read_text(encoding="utf-8"))
    test = predictions[predictions["split"] == "test"]
    assert len(test) == stored["n"]
    assert roc_auc_score(test["y_true"], test["y_prob"]) == pytest.approx(stored["roc_auc"])
    assert test["id"].is_unique
    assert test["y_prob"].between(0, 1).all()
    confusion = pd.read_csv(out / "confusion.csv")
    test_counts = confusion[confusion["split"] == "test"].set_index(["true_label", "predicted_label"])["count"]
    assert int(test_counts.loc[("fake", "fake")]) == stored["tp"]
    assert int(test_counts.loc[("real", "real")]) == stored["tn"]
    assert int(test_counts.loc[("real", "fake")]) == stored["fp"]
    assert int(test_counts.loc[("fake", "real")]) == stored["fn"]
    roc = pd.read_csv(out / "roc_curve.csv")
    assert {"fpr", "tpr", "threshold"} <= set(roc.columns)
    assert roc["fpr"].between(0, 1).all() and roc["tpr"].between(0, 1).all()
    sample = pd.read_csv(out / "gradcam_sample.csv")
    assert set(sample["role"]) == {"true_positive", "true_negative", "false_positive", "false_negative"}
    assert sample["target_layer"].eq("layer4").all()
    assert manifest["gradcam"]["status"] == "sample_only"
    assert not list(out.glob("*.png"))


def test_duplicate_ids_are_rejected() -> None:
    frame = pd.DataFrame(
        {
            "content_hash": ["a", "a"],
            "class_label": ["fake", "fake"],
            "prob_positive": [0.2, 0.8],
            "pred_positive": [0, 1],
            "threshold": [0.5, 0.5],
            "processed_path": ["p", "q"],
        }
    )
    with pytest.raises(ValueError, match="duplicate"):
        _as_binary(frame, "fake")


def test_gradcam_sample_is_stable() -> None:
    frame = pd.DataFrame(
        {
            "id": ["b", "a", "c", "d"],
            "y_true": [1, 1, 0, 0],
            "y_prob": [0.9, 0.9, 0.2, 0.8],
            "y_pred": [1, 1, 0, 1],
            "processed_path": ["b", "a", "c", "d"],
            "generator": ["g", "g", "g", "g"],
            "threshold": [0.5, 0.5, 0.5, 0.5],
        }
    )
    first = gradcam_sample(frame, per_role=1)["id"].tolist()
    second = gradcam_sample(frame, per_role=1)["id"].tolist()
    assert first == second
    assert first[0] == "a"  # tie at 0.9 broken by id


def test_grad_cam_map_is_normalized_data() -> None:
    activations = torch.zeros(1, 2, 2, 2)
    activations[0, 0, 0, 0] = 4
    gradients = torch.ones_like(activations)
    maps = grad_cam_map(activations, gradients)
    assert maps.shape == (1, 2, 2)
    assert float(maps.min()) == pytest.approx(0.0)
    assert float(maps.max()) == pytest.approx(1.0)
    rows = maps_to_rows(["img"], maps)
    assert len(rows) == 4 and {row["value"] for row in rows} <= {0.0, 1.0}
