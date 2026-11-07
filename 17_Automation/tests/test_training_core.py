"""FastAI-free tests for the STEP-036 training package."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

from training import TrainingConfigError, load_settings
from training.data import DatasetValidationError, load_assignments, validate_dataset
from training.evaluation import compute_metrics, expected_calibration_error, select_threshold, thresholded_metrics
from training.checkpoints import CheckpointStore
from training.pipeline import OutputsExistError, StartPoint, plan_run, start_point

from training_fixtures import EXP0001_CONFIG, REPO_ROOT, build_tiny_repo

pytest.importorskip("PIL")


@pytest.fixture()
def tiny(tmp_path: Path):
    config_path = build_tiny_repo(tmp_path)
    return load_settings(config_path, repo_root=tmp_path, check_registries=False)


# --- evaluation ---------------------------------------------------------------

def test_thresholded_metrics_known_values() -> None:
    y = np.array([1, 1, 1, 0, 0, 0, 0, 1])
    p = np.array([0.9, 0.8, 0.3, 0.2, 0.6, 0.1, 0.4, 0.7])
    m = thresholded_metrics(y, p, 0.5)
    assert (m["tp"], m["fn"], m["fp"], m["tn"]) == (3, 1, 1, 3)
    assert m["precision"] == pytest.approx(0.75)
    assert m["recall"] == pytest.approx(0.75)
    assert m["specificity"] == pytest.approx(0.75)
    assert m["fpr"] == pytest.approx(0.25)
    assert m["fnr"] == pytest.approx(0.25)
    assert m["balanced_accuracy"] == pytest.approx(0.75)
    assert m["mcc"] == pytest.approx(0.5)


def test_compute_metrics_has_canonical_set() -> None:
    y = np.array([0, 0, 1, 1])
    p = np.array([0.1, 0.4, 0.35, 0.8])
    m = compute_metrics(y, p, 0.5, calibration_bins=10)
    for key in ("roc_auc", "pr_auc", "f1", "balanced_accuracy", "mcc", "precision", "recall",
                "specificity", "fpr", "fnr", "accuracy", "ece", "brier"):
        assert key in m
    assert m["roc_auc"] == pytest.approx(0.75)
    assert m["brier"] == pytest.approx(np.mean((p - y) ** 2))


def test_ece_is_zero_when_perfectly_calibrated() -> None:
    y = np.array([0, 1] * 50)
    p = np.full(100, 0.5)
    assert expected_calibration_error(y, p, bins=10) == pytest.approx(0.0)


def test_select_threshold_matches_brute_force() -> None:
    rng = np.random.default_rng(0)
    y = rng.integers(0, 2, 300)
    p = np.clip(y * 0.3 + rng.random(300) * 0.7, 0, 1)
    chosen = select_threshold(y, p, "max_balanced_accuracy")
    best = max(thresholded_metrics(y, p, t)["balanced_accuracy"] for t in np.unique(np.append(p, 0.5)))
    assert thresholded_metrics(y, p, chosen)["balanced_accuracy"] == pytest.approx(best)
    assert select_threshold(y, p, "fixed_0.5") == 0.5


def test_metrics_reject_bad_inputs() -> None:
    with pytest.raises(ValueError, match="binary"):
        thresholded_metrics(np.array([0, 2]), np.array([0.1, 0.2]), 0.5)
    with pytest.raises(ValueError, match="\\[0, 1\\]"):
        thresholded_metrics(np.array([0, 1]), np.array([0.1, 1.2]), 0.5)
    with pytest.raises(ValueError, match="unknown threshold criterion"):
        select_threshold(np.array([0, 1]), np.array([0.1, 0.9]), "magic")


# --- settings -----------------------------------------------------------------

def test_exp0001_settings_resolve() -> None:
    settings = load_settings(EXP0001_CONFIG)
    assert settings.experiment_id == "EXP0001"
    assert settings.experiment_dir == REPO_ROOT / "06_Experiments" / "EXP0001"
    assert settings.checkpoint_dir == settings.experiment_dir / "notebook" / "checkpoints"
    assert settings.assignments_csv.is_file()
    assert settings.positive_class == "fake"


def test_invalid_config_is_rejected(tmp_path: Path) -> None:
    config_path = build_tiny_repo(tmp_path)
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    config["random_seed"] = None
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
    with pytest.raises(ValueError, match="random_seed is unset"):
        load_settings(config_path, repo_root=tmp_path, check_registries=False)


def test_config_outside_experiment_dir_is_rejected(tmp_path: Path) -> None:
    config_path = build_tiny_repo(tmp_path)
    moved = tmp_path / "elsewhere" / "config.yaml"
    moved.parent.mkdir()
    moved.write_text(config_path.read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(TrainingConfigError, match="must live in its experiment folder"):
        load_settings(moved, repo_root=tmp_path, check_registries=False)


# --- dataset validation -------------------------------------------------------

def test_dataset_validation_passes_on_tiny_repo(tiny) -> None:
    frames = validate_dataset(tiny, load_assignments(tiny))
    assert (len(frames.train), len(frames.valid), len(frames.test)) == (16, 8, 8)
    assert frames.train_valid()["is_valid"].sum() == 8


def test_missing_images_fail(tiny) -> None:
    frame = load_assignments(tiny)
    (tiny.processed_root / frame.loc[0, "processed_path"]).unlink()
    with pytest.raises(DatasetValidationError, match="1 of 32 image\\(s\\) missing"):
        validate_dataset(tiny, frame)


def test_missing_root_suggests_dataset(tiny) -> None:
    frame = load_assignments(tiny)
    broken = tiny.__class__(**{**tiny.__dict__, "processed_root": tiny.processed_root / "nope"})
    with pytest.raises(DatasetValidationError, match="Attach Kaggle dataset isthisdeception/ds0001-pp0001"):
        validate_dataset(broken, frame)


def test_unknown_label_fails(tiny) -> None:
    frame = load_assignments(tiny)
    frame.loc[0, "class_label"] = "deepfake"
    with pytest.raises(DatasetValidationError, match="not in dataset.vocab"):
        validate_dataset(tiny, frame, check_files=False)


def test_hash_leakage_fails(tiny) -> None:
    frame = load_assignments(tiny)
    test_idx = frame.index[frame["partition"] == "test"][0]
    train_idx = frame.index[frame["partition"] == "train"][0]
    frame.loc[test_idx, "content_hash"] = frame.loc[train_idx, "content_hash"]
    with pytest.raises(DatasetValidationError, match="leakage"):
        validate_dataset(tiny, frame, check_files=False)


def test_missing_class_in_train_fails(tiny) -> None:
    frame = load_assignments(tiny)
    frame = frame[~((frame["partition"] == "train") & (frame["class_label"] == "real"))]
    with pytest.raises(DatasetValidationError, match="no rows for class"):
        validate_dataset(tiny, pd.DataFrame(frame), check_files=False)


# --- output guard -------------------------------------------------------------

def test_plan_run_fresh_on_empty_experiment(tiny) -> None:
    assert plan_run(tiny, CheckpointStore(tiny), resume=True) == "fresh"


def test_plan_run_blocks_unmanifested_checkpoint_files(tiny) -> None:
    tiny.checkpoint_dir.mkdir(parents=True, exist_ok=True)
    (tiny.checkpoint_dir / "stray.pth").write_bytes(b"x")
    with pytest.raises(OutputsExistError, match="not in a checkpoint manifest"):
        plan_run(tiny, CheckpointStore(tiny), resume=True)


def test_plan_run_blocks_completed_experiment(tiny) -> None:
    (tiny.metrics_dir / "run_summary.json").write_text("{}", encoding="utf-8")
    with pytest.raises(OutputsExistError, match="already complete"):
        plan_run(tiny, CheckpointStore(tiny), resume=True)


def test_plan_run_blocks_partial_post_training_outputs(tiny) -> None:
    (tiny.predictions_dir / "test_predictions.csv").write_text("x", encoding="utf-8")
    with pytest.raises(OutputsExistError, match="incomplete run"):
        plan_run(tiny, CheckpointStore(tiny), resume=True)


def _state(phase: str, phase_epoch: int, complete: bool = False) -> dict:
    return {"phase": phase, "phase_epoch": phase_epoch,
            "experiment": {"checkpointer": {"training_complete": complete}}}


def test_start_point_resolution(tiny) -> None:
    # tiny config: 1 frozen epoch, then 1 unfrozen epoch
    assert start_point(tiny, None) == StartPoint(0, 0)
    assert start_point(tiny, _state("frozen", 0)) == StartPoint(1, 0)
    assert start_point(tiny, _state("unfrozen", 0)).done
    assert start_point(tiny, _state("frozen", 0, complete=True)).done
