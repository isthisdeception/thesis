"""Callbacks that persist across the frozen and unfrozen fits of one run."""

from __future__ import annotations

import operator
import time

import torch
from fastai.callback.core import Callback
from fastai.learner import Recorder

from .logs import get_logger


def _monitor_value(recorder: Recorder, monitor: str) -> float:
    names = list(recorder.metric_names[1:])
    if monitor not in names:
        raise KeyError(f"monitor {monitor!r} not among recorded values {names}")
    return float(recorder.values[-1][names.index(monitor)])


class EpochCheckpointer(Callback):
    """Save every epoch under a run-global epoch number and keep the best model.

    Epoch files are never overwritten; ``best_model.pth`` tracks the best
    monitored value across all phases of the run.
    """

    order = Recorder.order + 10

    def __init__(self, monitor: str, comp: str, with_opt: bool, every_epoch: bool) -> None:
        if comp not in {"min", "max"}:
            raise ValueError(f"comp must be 'min' or 'max', got {comp!r}")
        self.monitor = monitor
        self.better = operator.lt if comp == "min" else operator.gt
        self.with_opt = with_opt
        self.every_epoch = every_epoch
        self.global_epoch = 0
        self.best_value: float | None = None
        self.best_epoch: int | None = None
        self.saved: list[str] = []

    def _save(self, name: str, *, overwrite: bool) -> None:
        target = self.learn.path / self.learn.model_dir / f"{name}.pth"
        if target.exists() and not overwrite:
            raise FileExistsError(f"refusing to overwrite checkpoint {target}")
        self.learn.save(name, with_opt=self.with_opt)

    def after_epoch(self) -> None:
        value = _monitor_value(self.recorder, self.monitor)
        if self.every_epoch:
            name = f"epoch_{self.global_epoch:03d}"
            self._save(name, overwrite=False)
            self.saved.append(name)
        if self.best_value is None or self.better(value, self.best_value):
            self.best_value, self.best_epoch = value, self.global_epoch
            self._save("best_model", overwrite=True)
            get_logger().info("new best %s=%.5f at epoch %d", self.monitor, value, self.global_epoch)
        self.global_epoch += 1


class HistoryTracker(Callback):
    """Per-epoch and per-batch learning-curve data plus timing and GPU memory (M11)."""

    order = Recorder.order + 5

    def __init__(self) -> None:
        self.phase = "unset"
        self.global_epoch = 0
        self.global_iter = 0
        self.epochs: list[dict] = []
        self.batches: list[dict] = []
        self._started = 0.0

    def before_epoch(self) -> None:
        self._started = time.perf_counter()
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()

    def after_batch(self) -> None:
        if not self.training:
            return
        self.batches.append(
            {
                "iteration": self.global_iter,
                "epoch": self.global_epoch,
                "phase": self.phase,
                "loss": float(self.learn.loss),
                "lr": float(self.opt.hypers[-1]["lr"]),
            }
        )
        self.global_iter += 1

    def after_epoch(self) -> None:
        names = list(self.recorder.metric_names[1:])
        row = {"epoch": self.global_epoch, "phase": self.phase}
        for name, value in zip(names, self.recorder.values[-1]):
            if name != "time":
                row[name] = float(value)
        row["seconds"] = round(time.perf_counter() - self._started, 2)
        row["lr_head"] = float(self.opt.hypers[-1]["lr"])
        if torch.cuda.is_available():
            row["gpu_peak_mb"] = round(torch.cuda.max_memory_allocated() / 2**20, 1)
        self.epochs.append(row)
        get_logger().info("epoch %s", row)
        self.global_epoch += 1
