"""End-to-end smoke test: the real pipeline on a tiny synthetic dataset (CPU, seconds)."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

pytest.importorskip("fastai")
pytest.importorskip("torchvision")

from training import find_lr, run_experiment  # noqa: E402
from training.pipeline import OutputsExistError  # noqa: E402

from training_fixtures import build_tiny_repo  # noqa: E402


@pytest.fixture(scope="module")
def smoke_run(tmp_path_factory):
    root = tmp_path_factory.mktemp("smoke_repo")
    config_path = build_tiny_repo(root)
    summary = run_experiment(config_path, repo_root=root, check_registries=False)
    return root, config_path, summary


def test_summary_reports_complete_run(smoke_run) -> None:
    root, _, summary = smoke_run
    assert summary["status"] == "complete"
    assert summary["epochs_run"] == 2
    assert summary["best_epoch"] in (0, 1)
    saved = json.loads((root / "06_Experiments/EXP0001/metrics/run_summary.json").read_text(encoding="utf-8"))
    assert saved["experiment_id"] == "EXP0001"


def test_checkpoints_and_exports_written(smoke_run) -> None:
    root, _, summary = smoke_run
    ckpt = root / "06_Experiments/EXP0001/notebook/checkpoints"
    for name in ("epoch_000.pth", "epoch_001.pth", "best_model.pth", "last_checkpoint.pth", "export.pkl",
                 "weights.pth"):
        assert (ckpt / name).is_file(), name
    assert set(summary["artifacts"]) == {"best_model", "last_checkpoint", "export_pkl", "weights_pth"}
    assert all(len(a["sha256"]) == 64 for a in summary["artifacts"].values())


def test_export_pkl_loads(smoke_run) -> None:
    from fastai.learner import load_learner

    root, _, _ = smoke_run
    learn = load_learner(root / "06_Experiments/EXP0001/notebook/checkpoints/export.pkl")
    assert list(learn.dls.vocab) == ["fake", "real"]


def test_predictions_metrics_and_curves(smoke_run) -> None:
    root, _, summary = smoke_run
    exp = root / "06_Experiments/EXP0001"
    val = pd.read_csv(exp / "predictions/val_predictions.csv")
    test = pd.read_csv(exp / "predictions/test_predictions.csv")
    assert len(val) == 8 and len(test) == 8
    assert {"prob_fake", "prob_real", "prob_positive", "pred_positive", "threshold"} <= set(test.columns)
    for split in ("val", "test"):
        metrics = json.loads((exp / f"metrics/{split}_metrics.json").read_text(encoding="utf-8"))
        assert {"roc_auc", "pr_auc", "f1", "mcc", "ece", "brier"} <= set(metrics)
        assert (exp / f"metrics/{split}_calibration.csv").is_file()
    assert summary["metrics"]["threshold"]["policy"] == "validation_only"
    epochs = pd.read_csv(exp / "learning_curves/epochs.csv")
    assert list(epochs["phase"]) == ["frozen", "unfrozen"]
    assert {"train_loss", "valid_loss"} <= set(epochs.columns)
    assert len(pd.read_csv(exp / "learning_curves/batches.csv")) > 0
    assert (exp / "logs/history.csv").is_file()
    assert list((exp / "logs").glob("train_*.log"))


def test_rerun_refuses_to_overwrite(smoke_run) -> None:
    root, config_path, _ = smoke_run
    with pytest.raises(Exception) as excinfo:
        run_experiment(config_path, repo_root=root, check_registries=False)
    assert isinstance(excinfo.value.__cause__, OutputsExistError)


def test_lr_finder_records_suggestion(tmp_path: Path) -> None:
    config_path = build_tiny_repo(tmp_path)
    result = find_lr(config_path, repo_root=tmp_path, check_registries=False)
    assert result["suggested_lr"] > 0
    assert (tmp_path / result["curve"]).is_file()
    ckpt = tmp_path / "06_Experiments/EXP0001/notebook/checkpoints"
    assert not list(ckpt.glob("*.pth")) if ckpt.exists() else True
