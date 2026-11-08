"""Callbacks whose state survives across fits and across interrupted sessions."""

from __future__ import annotations

import operator
import time
from pathlib import Path
from typing import Callable

import torch
from fastai.callback.core import Callback, CancelFitException
from fastai.learner import Recorder

from .checkpoints import CheckpointStore
from .logs import event, get_logger
from .records import BATCH_COLUMNS, append_rows, epoch_columns


def _recorded(recorder: Recorder) -> dict[str, float]:
    names = list(recorder.metric_names[1:])
    return {n: float(v) for n, v in zip(names, recorder.values[-1]) if n != "time"}


def default_comp(monitor: str) -> str:
    """FastAI's TrackerCallback rule: losses/errors are minimized, everything else maximized."""

    return "min" if "loss" in monitor or "error" in monitor else "max"


class _Best:
    def __init__(self, monitor: str, comp: str) -> None:
        if comp not in {"min", "max"}:
            raise ValueError(f"comp must be 'min' or 'max', got {comp!r}")
        self.monitor = monitor
        self.comp = comp
        self.value: float | None = None
        self.epoch: int | None = None

    def update(self, values: dict[str, float], epoch: int) -> bool:
        if self.monitor not in values:
            raise KeyError(f"monitor {self.monitor!r} not among recorded values {sorted(values)}")
        value = values[self.monitor]
        better = operator.lt if self.comp == "min" else operator.gt
        if self.value is None or better(value, self.value):
            self.value, self.epoch = value, epoch
            return True
        return False

    def state_dict(self) -> dict:
        return {"monitor": self.monitor, "comp": self.comp, "value": self.value, "epoch": self.epoch}

    def load_state_dict(self, state: dict) -> None:
        self.value, self.epoch = state["value"], state["epoch"]


class _PhaseAware(Callback):
    """Knows the current phase and ignores epochs that SkipToEpoch cancels on resume.

    FastAI still fires ``after_epoch`` for skipped epochs, so subclasses must
    check ``skipped`` first.
    """

    def __init__(self) -> None:
        self.phase = "unset"
        self.phase_n_epoch = 0
        self.start_epoch = 0

    def begin_phase(self, phase: str, n_epoch: int, start_epoch: int) -> None:
        self.phase, self.phase_n_epoch, self.start_epoch = phase, n_epoch, start_epoch

    @property
    def skipped(self) -> bool:
        return self.epoch < self.start_epoch


class EpochCheckpointer(_PhaseAware):
    """Saves an immutable full-state recovery checkpoint after every epoch.

    Also owns best-model tracking and early stopping, so both resume exactly:
    the saved state already reflects the epoch's outcome before any stop.
    """

    order = Recorder.order + 10

    def __init__(
        self,
        store: CheckpointStore,
        state_builder: Callable[["EpochCheckpointer"], dict],
        monitor: str,
        comp: str,
        early_stopping: dict | None,
    ) -> None:
        super().__init__()
        self.store = store
        self.state_builder = state_builder
        self.best = _Best(monitor, comp)
        self.early_cfg = early_stopping if early_stopping and early_stopping.get("enabled") else None
        self.early = _Best(self.early_cfg["monitor"], default_comp(self.early_cfg["monitor"])) if self.early_cfg else None
        self.wait = 0
        self.early_active = False
        self.global_epoch = 0
        self.early_stopped = False
        self.training_complete = False
        self.last_values: dict[str, float] = {}

    def begin_phase(self, phase: str, n_epoch: int, start_epoch: int, early_active: bool = False) -> None:
        super().begin_phase(phase, n_epoch, start_epoch)
        self.early_active = early_active and self.early is not None
        if self.early_active and start_epoch == 0:
            self.early.value, self.early.epoch, self.wait = None, None, 0

    def after_epoch(self) -> None:
        if self.skipped:
            return
        values = _recorded(self.recorder)
        self.last_values = values
        improved = self.best.update(values, self.global_epoch)
        if improved:
            get_logger().info("new best %s=%.5f at epoch %d", self.best.monitor, self.best.value, self.global_epoch)
        stop = False
        if self.early_active:
            if self.early.update(values, self.global_epoch):
                self.wait = 0
            else:
                self.wait += 1
            stop = self.wait >= int(self.early_cfg["patience"])
        last_of_run = self.phase == "unfrozen" and self.epoch == self.phase_n_epoch - 1
        self.early_stopped = stop
        self.training_complete = stop or last_of_run

        meta = {
            "epoch": self.global_epoch,
            "phase": self.phase,
            "phase_epoch": int(self.epoch),
            "monitor": self.best.monitor,
            "monitor_value": values[self.best.monitor],
            "is_best_so_far": improved,
        }
        self.store.save_state(self.store.recovery_name(self.global_epoch), self.state_builder(self), "recovery", meta)
        self.global_epoch += 1
        if stop:
            get_logger().info("early stopping: no %s improvement for %d epoch(s)", self.early.monitor, self.wait)
            event("early_stop", epoch=self.global_epoch - 1, monitor=self.early.monitor, wait=self.wait)
            raise CancelFitException()

    def state_dict(self) -> dict:
        return {
            "next_global_epoch": self.global_epoch + 1,
            "best": self.best.state_dict(),
            "early": self.early.state_dict() if self.early else None,
            "wait": self.wait,
            "early_stopped": self.early_stopped,
            "training_complete": self.training_complete,
        }

    def load_state_dict(self, state: dict) -> None:
        self.global_epoch = state["next_global_epoch"]
        self.best.load_state_dict(state["best"])
        if self.early and state["early"]:
            self.early.load_state_dict(state["early"])
        self.wait = state["wait"]
        self.early_stopped = state["early_stopped"]
        self.training_complete = state["training_complete"]


class HistoryTracker(_PhaseAware):
    """Per-epoch and per-batch learning-curve data plus timing and GPU memory (M11).

    Rows are appended to the live CSVs (``live_epochs`` / ``live_batches``) as
    each epoch ends, so they survive a session that dies before the run ends.
    The in-memory history (restored from checkpoints on resume) is the
    authoritative record used for the final learning-curve files.
    """

    order = Recorder.order + 5

    def __init__(self, session: str = "", live_epochs: Path | None = None, live_batches: Path | None = None) -> None:
        super().__init__()
        self.session = session
        self.live_epochs = live_epochs
        self.live_batches = live_batches
        self.columns: list[str] | None = None
        self.global_epoch = 0
        self.global_iter = 0
        self.epochs: list[dict] = []
        self.batches: list[dict] = []
        self._epoch_batches: list[dict] = []
        self._started = 0.0

    def before_epoch(self) -> None:
        self._started = time.perf_counter()
        self._epoch_batches = []
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()

    def after_batch(self) -> None:
        if not self.training:
            return
        row = {
            "session": self.session,
            "iteration": self.global_iter,
            "epoch": self.global_epoch,
            "phase": self.phase,
            "loss": float(self.learn.loss.detach()),
            "lr": float(self.opt.hypers[-1]["lr"]),
        }
        self.batches.append(row)
        self._epoch_batches.append(row)
        self.global_iter += 1

    def after_epoch(self) -> None:
        if self.skipped:
            return
        recorded = _recorded(self.recorder)
        if self.columns is None:
            self.columns = epoch_columns(recorded)
        cuda = torch.cuda.is_available()
        row = {
            "session": self.session,
            "epoch": self.global_epoch,
            "phase": self.phase,
            "phase_epoch": int(self.epoch),
            **recorded,
            "seconds": round(time.perf_counter() - self._started, 2),
            "lr_head": float(self.opt.hypers[-1]["lr"]),
            "gpu_peak_allocated_mb": round(torch.cuda.max_memory_allocated() / 2**20, 1) if cuda else None,
            "gpu_peak_reserved_mb": round(torch.cuda.max_memory_reserved() / 2**20, 1) if cuda else None,
        }
        self.epochs.append(row)
        if self.live_epochs is not None:
            append_rows(self.live_epochs, self.columns, [row])
        if self.live_batches is not None:
            append_rows(self.live_batches, BATCH_COLUMNS, self._epoch_batches)
        get_logger().info("epoch %s", row)
        event("epoch", **row)
        self.global_epoch += 1

    def state_dict(self) -> dict:
        return {
            "global_epoch": self.global_epoch,
            "global_iter": self.global_iter,
            "columns": self.columns,
            "epochs": list(self.epochs),
            "batches": list(self.batches),
        }

    def load_state_dict(self, state: dict) -> None:
        self.global_epoch = state["global_epoch"]
        self.global_iter = state["global_iter"]
        self.columns = state["columns"]
        self.epochs = list(state["epochs"])
        self.batches = list(state["batches"])
