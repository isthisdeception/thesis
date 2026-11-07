"""End-to-end tests: the real pipeline on a tiny synthetic dataset (CPU, seconds per run)."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest
import yaml

pytest.importorskip("fastai")
pytest.importorskip("torchvision")

import torch  # noqa: E402

from training import find_lr, run_experiment  # noqa: E402
from training.callbacks import EpochCheckpointer  # noqa: E402
from training.checkpoints import capture_rng, restore_rng, sha256_file  # noqa: E402
from training.logs import PipelineStepError  # noqa: E402
from training.pipeline import OutputsExistError  # noqa: E402

from training_fixtures import build_tiny_repo  # noqa: E402

EXP = "06_Experiments/EXP0001"
CKPT = f"{EXP}/notebook/checkpoints"


def _manifest(root: Path) -> dict:
    return json.loads((root / CKPT / "checkpoint_manifest.json").read_text(encoding="utf-8"))


def _set_epochs(config_path: Path, epochs: int) -> None:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    config["epochs"] = epochs
    config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")


class SimulatedTermination(RuntimeError):
    pass


def _interrupt_after(monkeypatch, global_epoch: int) -> None:
    """Make the session 'die' right after the given epoch's recovery checkpoint is saved."""

    original = EpochCheckpointer.after_epoch

    def dying(self):
        original(self)
        if not self.skipped and self.global_epoch == global_epoch + 1:
            raise SimulatedTermination(f"simulated Kaggle session end after epoch {global_epoch}")

    monkeypatch.setattr(EpochCheckpointer, "after_epoch", dying)


# --- uninterrupted run ------------------------------------------------------------


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
    assert summary["resumed_from_epoch"] is None
    assert summary["best_epoch"] in (0, 1)
    saved = json.loads((root / EXP / "metrics/run_summary.json").read_text(encoding="utf-8"))
    assert saved["experiment_id"] == "EXP0001"


def test_checkpoints_use_canonical_names(smoke_run) -> None:
    root, _, summary = smoke_run
    ckpt = root / CKPT
    for name in ("EXP0001_epoch_000.pth", "EXP0001_epoch_001.pth", "EXP0001_best.pth", "EXP0001_last.pth",
                 "MODEL0001_export.pkl", "MODEL0001_weights.pth", "checkpoint_manifest.json"):
        assert (ckpt / name).is_file(), name
    assert not list(ckpt.glob("*.partial"))
    assert set(summary["artifacts"]) == {"best", "last", "export_pkl", "weights_pth"}


def test_manifest_checksums_verify(smoke_run) -> None:
    root, _, _ = smoke_run
    manifest = _manifest(root)
    kinds = [e["kind"] for e in manifest["entries"]]
    assert kinds.count("recovery") == 2
    assert {"best", "last", "export_pkl", "weights_pth"} <= set(kinds)
    for entry in manifest["entries"]:
        assert sha256_file(root / CKPT / entry["name"]) == entry["sha256"], entry["name"]
    best = next(e for e in manifest["entries"] if e["kind"] == "best")
    assert best["copied_from"] == f"EXP0001_epoch_{best['epoch']:03d}.pth"


def test_git_side_manifest_written(smoke_run) -> None:
    root, _, _ = smoke_run
    text = (root / "07_Checkpoints/EXP0001_checkpoints.md").read_text(encoding="utf-8")
    for entry in _manifest(root)["entries"]:
        assert entry["sha256"] in text
    assert "binaries never go to Git" in text


def test_recovery_checkpoint_holds_full_state(smoke_run) -> None:
    root, _, _ = smoke_run
    state = torch.load(root / CKPT / "EXP0001_epoch_001.pth", weights_only=False)
    assert {"model", "opt", "rng", "schedule", "experiment", "epoch", "phase", "phase_epoch"} <= set(state)
    assert state["opt"]["state"], "optimizer state must not be empty"
    assert {"python", "numpy", "torch", "cuda"} <= set(state["rng"])
    assert state["experiment"]["checkpointer"]["training_complete"] is True
    assert len(state["experiment"]["tracker"]["epochs"]) == 2


def test_export_pkl_loads(smoke_run) -> None:
    from fastai.learner import load_learner

    root, _, _ = smoke_run
    learn = load_learner(root / CKPT / "MODEL0001_export.pkl")
    assert list(learn.dls.vocab) == ["fake", "real"]


def test_predictions_metrics_and_curves(smoke_run) -> None:
    root, _, summary = smoke_run
    exp = root / EXP
    assert len(pd.read_csv(exp / "predictions/val_predictions.csv")) == 8
    test = pd.read_csv(exp / "predictions/test_predictions.csv")
    assert len(test) == 8
    assert {"prob_fake", "prob_real", "prob_positive", "pred_positive", "threshold"} <= set(test.columns)
    for split in ("val", "test"):
        metrics = json.loads((exp / f"metrics/{split}_metrics.json").read_text(encoding="utf-8"))
        assert {"roc_auc", "pr_auc", "f1", "mcc", "ece", "brier"} <= set(metrics)
        assert (exp / f"metrics/{split}_calibration.csv").is_file()
    assert summary["metrics"]["threshold"]["policy"] == "validation_only"
    epochs = pd.read_csv(exp / "learning_curves/epochs.csv")
    assert list(epochs["phase"]) == ["frozen", "unfrozen"]
    assert len(pd.read_csv(exp / "learning_curves/batches.csv")) > 0
    assert list((exp / "logs").glob("EXP0001_train_*.log"))


def _events(root: Path) -> list[dict]:
    path = root / EXP / "logs/EXP0001_events.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_live_logs_and_event_log(smoke_run) -> None:
    root, _, summary = smoke_run
    logs = root / EXP / "logs"
    live = pd.read_csv(logs / "EXP0001_epochs.csv")
    assert list(live.columns[:6]) == ["session", "epoch", "phase", "phase_epoch", "train_loss", "valid_loss"]
    assert list(live.columns[-4:]) == ["seconds", "lr_head", "gpu_peak_allocated_mb", "gpu_peak_reserved_mb"]
    assert list(live["epoch"]) == [0, 1]
    assert len(pd.read_csv(logs / "EXP0001_batches.csv")) == len(pd.read_csv(root / EXP / "learning_curves/batches.csv"))
    names = [e["event"] for e in _events(root)]
    for expected in ("session_start", "run_start", "run_mode", "environment", "epoch", "checkpoint_saved",
                     "run_complete"):
        assert expected in names, expected
    assert names.count("epoch") == 2
    assert summary["logs"]["events"].endswith("EXP0001_events.jsonl")
    assert isinstance(summary["warnings_logged"], int) and summary["errors_logged"] == 0


def test_hyperparameter_record(smoke_run) -> None:
    root, _, summary = smoke_run
    record = json.loads((root / summary["logs"]["hyperparameters"]).read_text(encoding="utf-8"))
    assert record["config_sha256"] == summary["config_sha256"]
    assert record["resolved_config"]["random_seed"] == 42
    assert [p["phase"] for p in record["phases"]] == ["frozen", "unfrozen"]
    assert record["phases"][1]["lr_max"] == pytest.approx([5e-6, 5e-4])
    assert record["data"]["partitions"] == {"train": 16, "valid": 8, "test": 8}
    assert record["train_monitors"]


def test_metrics_summary_csv(smoke_run) -> None:
    root, _, _ = smoke_run
    table = pd.read_csv(root / EXP / "metrics/metrics_summary.csv")
    assert list(table["split"]) == ["val", "test"]
    assert list(table.columns[:4]) == ["split", "threshold", "roc_auc", "pr_auc"]


def test_rerun_of_complete_experiment_refuses(smoke_run) -> None:
    root, config_path, _ = smoke_run
    with pytest.raises(PipelineStepError) as excinfo:
        run_experiment(config_path, repo_root=root, check_registries=False)
    assert isinstance(excinfo.value.__cause__, OutputsExistError)


# --- interruption + resume --------------------------------------------------------


def test_interrupted_run_resumes_without_overwriting(tmp_path: Path, monkeypatch) -> None:
    config_path = build_tiny_repo(tmp_path)
    _set_epochs(config_path, 2)  # 1 frozen + 2 unfrozen = epochs 0, 1, 2
    _interrupt_after(monkeypatch, global_epoch=1)  # dies mid unfrozen phase
    with pytest.raises(PipelineStepError) as excinfo:
        run_experiment(config_path, repo_root=tmp_path, check_registries=False)
    assert isinstance(excinfo.value.__cause__, SimulatedTermination)

    ckpt = tmp_path / CKPT
    before = {p.name: sha256_file(p) for p in ckpt.glob("EXP0001_epoch_*.pth")}
    assert sorted(before) == ["EXP0001_epoch_000.pth", "EXP0001_epoch_001.pth"]
    assert not (tmp_path / EXP / "metrics/run_summary.json").exists()

    monkeypatch.undo()
    summary = run_experiment(config_path, repo_root=tmp_path, check_registries=False)

    assert summary["resumed_from_epoch"] == 1
    assert summary["epochs_run"] == 3
    for name, digest in before.items():
        assert sha256_file(ckpt / name) == digest, f"{name} was overwritten"
    assert (ckpt / "EXP0001_epoch_002.pth").is_file()
    epochs = pd.read_csv(tmp_path / EXP / "learning_curves/epochs.csv")
    assert list(epochs["epoch"]) == [0, 1, 2]
    assert list(epochs["phase"]) == ["frozen", "unfrozen", "unfrozen"]
    state = torch.load(ckpt / "EXP0001_epoch_002.pth", weights_only=False)
    assert state["phase_epoch"] == 1

    # Both sessions left evidence: the failure, the resume, and live rows tagged by session.
    events = _events(tmp_path)
    failed = [e for e in events if e["event"] == "run_failed"]
    assert len(failed) == 1 and "SimulatedTermination" in failed[0]["error"]
    assert any(e["event"] == "resume" and e["epoch"] == 1 for e in events)
    live = pd.read_csv(tmp_path / EXP / "logs/EXP0001_epochs.csv")
    assert list(live["epoch"]) == [0, 1, 2]
    assert live["session"].nunique() == 2
    assert len(summary["sessions"]) == 2


def test_resumed_schedule_matches_uninterrupted_run(tmp_path: Path, monkeypatch) -> None:
    straight_root, resumed_root = tmp_path / "straight", tmp_path / "resumed"
    for root in (straight_root, resumed_root):
        root.mkdir()
        _set_epochs(build_tiny_repo(root), 2)
    run_experiment(straight_root / EXP / "config.yaml", repo_root=straight_root, check_registries=False)

    _interrupt_after(monkeypatch, global_epoch=1)
    with pytest.raises(PipelineStepError):
        run_experiment(resumed_root / EXP / "config.yaml", repo_root=resumed_root, check_registries=False)
    monkeypatch.undo()
    run_experiment(resumed_root / EXP / "config.yaml", repo_root=resumed_root, check_registries=False)

    straight = pd.read_csv(straight_root / EXP / "learning_curves/batches.csv")
    resumed = pd.read_csv(resumed_root / EXP / "learning_curves/batches.csv")
    assert list(resumed["epoch"]) == list(straight["epoch"])
    assert resumed["lr"].to_numpy() == pytest.approx(straight["lr"].to_numpy(), rel=1e-9)


def test_resume_quarantines_corrupt_latest_checkpoint(tmp_path: Path, monkeypatch) -> None:
    config_path = build_tiny_repo(tmp_path)
    _set_epochs(config_path, 2)
    _interrupt_after(monkeypatch, global_epoch=1)
    with pytest.raises(PipelineStepError):
        run_experiment(config_path, repo_root=tmp_path, check_registries=False)
    monkeypatch.undo()

    ckpt = tmp_path / CKPT
    corrupt = ckpt / "EXP0001_epoch_001.pth"
    corrupt.write_bytes(corrupt.read_bytes()[:100])  # simulate a damaged upload

    summary = run_experiment(config_path, repo_root=tmp_path, check_registries=False)
    assert summary["resumed_from_epoch"] == 0
    assert summary["epochs_run"] == 3
    quarantined = list((ckpt / "quarantine").glob("EXP0001_epoch_001.pth.*"))
    assert len(quarantined) == 1 and quarantined[0].stat().st_size == 100
    statuses = [(e["name"], e["status"]) for e in _manifest(tmp_path)["entries"] if e["kind"] == "recovery"]
    assert ("EXP0001_epoch_001.pth", "quarantined") in statuses
    assert ("EXP0001_epoch_001.pth", "valid") in statuses


def test_resume_refuses_changed_config(tmp_path: Path, monkeypatch) -> None:
    config_path = build_tiny_repo(tmp_path)
    _interrupt_after(monkeypatch, global_epoch=0)
    with pytest.raises(PipelineStepError):
        run_experiment(config_path, repo_root=tmp_path, check_registries=False)
    monkeypatch.undo()
    _set_epochs(config_path, 3)
    with pytest.raises(Exception, match="config.yaml changed"):
        run_experiment(config_path, repo_root=tmp_path, check_registries=False)


def test_rng_capture_restore_roundtrip() -> None:
    import random

    import numpy as np

    state = capture_rng()
    first = (random.random(), float(np.random.rand()), float(torch.rand(1)))
    restore_rng(state)
    assert (random.random(), float(np.random.rand()), float(torch.rand(1))) == first


def test_lr_finder_records_suggestion(tmp_path: Path) -> None:
    config_path = build_tiny_repo(tmp_path)
    result = find_lr(config_path, repo_root=tmp_path, check_registries=False)
    assert result["suggested_lr"] > 0
    assert (tmp_path / result["curve"]).is_file()
    ckpt = tmp_path / CKPT
    assert not ckpt.exists() or not list(ckpt.glob("*.pth"))
