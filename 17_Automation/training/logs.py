"""Phase M11 logging: per-session log file, append-only event log, warning capture, timed steps."""

from __future__ import annotations

import json
import logging
import platform
import sys
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator

LOGGER_NAME = "training"
WARNINGS_LOGGER = "py.warnings"


class PipelineStepError(RuntimeError):
    """A named pipeline step failed; the original exception is chained."""

    def __init__(self, step: str, cause: BaseException) -> None:
        self.step = step
        super().__init__(f"pipeline step '{step}' failed: {type(cause).__name__}: {cause}")


class _Counter(logging.Handler):
    def __init__(self) -> None:
        super().__init__(level=logging.WARNING)
        self.warnings = 0
        self.errors = 0

    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno >= logging.ERROR:
            self.errors += 1
        else:
            self.warnings += 1


class RunLog:
    """One logging session (a training run or an LR Finder run) of one experiment.

    ``EXPxxxx_<stage>_<time>.log`` is the human-readable log of this session;
    ``EXPxxxx_events.jsonl`` is shared by all sessions and only ever appended to.
    """

    def __init__(self, logs_dir: Path, experiment_id: str, stage: str) -> None:
        stamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")[:-3]
        self.logs_dir = logs_dir
        self.experiment_id = experiment_id
        self.stage = stage
        self.session = f"{stage}_{stamp}"
        self.log_path = logs_dir / f"{experiment_id}_{stage}_{stamp}.log"
        self.events_path = logs_dir / f"{experiment_id}_events.jsonl"
        self.counter = _Counter()

    def path(self, kind: str, suffix: str) -> Path:
        """Per-experiment file in the logs folder, e.g. ``EXP0001_epochs.csv``."""

        return self.logs_dir / f"{self.experiment_id}_{kind}{suffix}"

    def session_path(self, kind: str, suffix: str) -> Path:
        """Per-session file, e.g. ``EXP0001_hyperparameters_train_20261107T101500.json``."""

        return self.logs_dir / f"{self.experiment_id}_{kind}_{self.session}{suffix}"

    def event(self, kind: str, /, **fields) -> None:
        record = {
            "time": datetime.now().astimezone().isoformat(timespec="seconds"),
            "session": self.session,
            "event": kind,
            **fields,
        }
        with self.events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, default=str) + "\n")

    @property
    def warnings(self) -> int:
        return self.counter.warnings

    @property
    def errors(self) -> int:
        return self.counter.errors


_active: RunLog | None = None


def get_logger() -> logging.Logger:
    return logging.getLogger(LOGGER_NAME)


def active_run() -> RunLog | None:
    return _active


def event(kind: str, /, **fields) -> None:
    """Append to the active session's event log; a no-op outside a run."""

    if _active is not None:
        _active.event(kind, **fields)


def _detach(logger: logging.Logger) -> None:
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)


def setup_run_logging(logs_dir: Path, experiment_id: str, stage: str) -> RunLog:
    """Start a session: file + stdout handlers, warning capture, and the event log."""

    global _active
    logs_dir.mkdir(parents=True, exist_ok=True)
    run = RunLog(logs_dir, experiment_id, stage)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    file_handler = logging.FileHandler(run.log_path, encoding="utf-8")
    stream_handler = logging.StreamHandler(sys.stdout)
    for handler in (file_handler, stream_handler):
        handler.setFormatter(fmt)
    logging.captureWarnings(True)
    for name in (LOGGER_NAME, WARNINGS_LOGGER):
        logger = logging.getLogger(name)
        _detach(logger)
        logger.setLevel(logging.INFO)
        logger.propagate = False
        for handler in (file_handler, stream_handler, run.counter):
            logger.addHandler(handler)
    _active = run
    run.event("session_start", stage=stage, log=run.log_path.name)
    return run


def close_run_logging() -> None:
    global _active
    for name in (LOGGER_NAME, WARNINGS_LOGGER):
        _detach(logging.getLogger(name))
    logging.captureWarnings(False)
    _active = None


@contextmanager
def step(name: str) -> Iterator[None]:
    """Log start, duration, and failure of a pipeline step; failures re-raise as PipelineStepError."""

    logger = get_logger()
    logger.info("STEP START %s", name)
    event("step_start", step=name)
    started = time.perf_counter()
    try:
        yield
    except PipelineStepError:
        raise
    except Exception as exc:
        seconds = round(time.perf_counter() - started, 2)
        logger.exception("STEP FAILED %s after %.1fs", name, seconds)
        event("step_failed", step=name, seconds=seconds, error=f"{type(exc).__name__}: {exc}")
        raise PipelineStepError(name, exc) from exc
    seconds = round(time.perf_counter() - started, 2)
    logger.info("STEP DONE %s in %.1fs", name, seconds)
    event("step_done", step=name, seconds=seconds)


def environment_info() -> dict:
    """Library versions and GPU details for the run summary."""

    info: dict = {"python": platform.python_version(), "platform": platform.platform()}
    try:
        import fastai
        import torch
        import torchvision

        info.update(
            torch=torch.__version__,
            torchvision=torchvision.__version__,
            fastai=fastai.__version__,
            cuda_available=torch.cuda.is_available(),
            cuda=torch.version.cuda,
        )
        if torch.cuda.is_available():
            props = torch.cuda.get_device_properties(0)
            info.update(gpu=props.name, gpu_memory_mb=round(props.total_memory / 2**20))
    except ImportError as exc:
        info["import_error"] = str(exc)
    try:
        from importlib.metadata import version

        info["plum_dispatch"] = version("plum-dispatch")
    except Exception as exc:  # metadata lookup must never break a run; record why it is missing
        info["plum_dispatch"] = f"unavailable ({type(exc).__name__})"
    return info
