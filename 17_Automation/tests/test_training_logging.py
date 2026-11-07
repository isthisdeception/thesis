"""FastAI-free tests for STEP-038 logging and record schemas."""

from __future__ import annotations

import csv
import json
import logging
import warnings
from pathlib import Path

import pytest

from training.logs import PipelineStepError, close_run_logging, event, get_logger, setup_run_logging, step
from training.records import BATCH_COLUMNS, RecordSchemaError, append_rows, epoch_columns


def _events(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


@pytest.fixture()
def run(tmp_path: Path):
    run = setup_run_logging(tmp_path / "logs", "EXP0001", "train")
    yield run
    close_run_logging()


def test_session_files_use_a2_names(run) -> None:
    assert run.log_path.name.startswith("EXP0001_train_") and run.log_path.suffix == ".log"
    assert run.events_path.name == "EXP0001_events.jsonl"
    assert run.path("epochs", ".csv").name == "EXP0001_epochs.csv"
    assert run.session_path("hyperparameters", ".json").name == f"EXP0001_hyperparameters_{run.session}.json"


def test_steps_and_events_are_recorded(run) -> None:
    with step("dataset validation"):
        get_logger().info("checking")
    event("custom", value=3)
    records = _events(run.events_path)
    names = [r["event"] for r in records]
    assert names == ["session_start", "step_start", "step_done", "custom"]
    assert all(r["session"] == run.session for r in records)
    assert records[-1]["value"] == 3
    text = run.log_path.read_text(encoding="utf-8")
    assert "STEP DONE dataset validation" in text and "checking" in text


def test_step_failure_is_logged_with_traceback(run) -> None:
    with pytest.raises(PipelineStepError, match="pipeline step 'training' failed: ValueError: boom"):
        with step("training"):
            raise ValueError("boom")
    failed = [r for r in _events(run.events_path) if r["event"] == "step_failed"]
    assert failed and failed[0]["error"] == "ValueError: boom"
    text = run.log_path.read_text(encoding="utf-8")
    assert "STEP FAILED training" in text and "Traceback" in text
    assert run.errors == 1


def test_python_warnings_are_captured_and_counted(run) -> None:
    # pytest swaps warnings.showwarning per test; restore logging's hook as a normal run would have it.
    with warnings.catch_warnings():
        warnings.simplefilter("always")
        warnings.showwarning = logging._showwarning
        warnings.warn("deprecated thing", DeprecationWarning, stacklevel=1)
    get_logger().warning("explicit warning")
    assert run.warnings == 2
    text = run.log_path.read_text(encoding="utf-8")
    assert "deprecated thing" in text and "explicit warning" in text


def test_events_append_across_sessions(tmp_path: Path) -> None:
    first = setup_run_logging(tmp_path, "EXP0001", "train")
    close_run_logging()
    second = setup_run_logging(tmp_path, "EXP0001", "train")
    event("x")
    close_run_logging()
    sessions = {r["session"] for r in _events(second.events_path)}
    assert first.events_path == second.events_path
    assert len(_events(second.events_path)) == 3
    assert sessions == {first.session, second.session}
    event("outside a run is a no-op")
    assert len(_events(second.events_path)) == 3


def test_epoch_columns_are_deterministic() -> None:
    cols = epoch_columns(["train_loss", "valid_loss", "roc_auc_score", "f1_score", "time"])
    assert cols == ["session", "epoch", "phase", "phase_epoch", "train_loss", "valid_loss", "roc_auc_score",
                    "f1_score", "seconds", "lr_head", "gpu_peak_allocated_mb", "gpu_peak_reserved_mb"]


def test_append_rows_writes_header_once_and_rejects_mismatch(tmp_path: Path) -> None:
    path = tmp_path / "batches.csv"
    row = {"session": "s", "iteration": 0, "epoch": 0, "phase": "frozen", "loss": 0.5, "lr": 1e-3}
    append_rows(path, BATCH_COLUMNS, [row])
    append_rows(path, BATCH_COLUMNS, [{**row, "iteration": 1}])
    rows = list(csv.reader(path.open(encoding="utf-8")))
    assert rows[0] == BATCH_COLUMNS and len(rows) == 3
    with pytest.raises(RecordSchemaError, match="differs from schema"):
        append_rows(path, ["other"], [{"other": 1}])
    with pytest.raises(RecordSchemaError, match="outside the schema"):
        append_rows(path, BATCH_COLUMNS, [{**row, "surprise": 1}])
