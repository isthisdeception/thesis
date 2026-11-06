"""Phase M11 logging: one log file per run plus timed, failure-aware pipeline steps."""

from __future__ import annotations

import logging
import platform
import sys
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator

LOGGER_NAME = "training"


class PipelineStepError(RuntimeError):
    """A named pipeline step failed; the original exception is chained."""

    def __init__(self, step: str, cause: BaseException) -> None:
        self.step = step
        super().__init__(f"pipeline step '{step}' failed: {type(cause).__name__}: {cause}")


def get_logger() -> logging.Logger:
    return logging.getLogger(LOGGER_NAME)


def setup_run_logging(logs_dir: Path, run_name: str) -> Path:
    """Attach a fresh file handler (and a stdout handler) for one run."""

    logs_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    log_path = logs_dir / f"{run_name}_{stamp}.log"
    logger = get_logger()
    logger.setLevel(logging.INFO)
    logger.propagate = False
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    for handler in (logging.FileHandler(log_path, encoding="utf-8"), logging.StreamHandler(sys.stdout)):
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    return log_path


def close_run_logging() -> None:
    logger = get_logger()
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)


@contextmanager
def step(name: str) -> Iterator[None]:
    """Log start, duration, and failure of a pipeline step; failures re-raise as PipelineStepError."""

    logger = get_logger()
    logger.info("STEP START %s", name)
    started = time.perf_counter()
    try:
        yield
    except PipelineStepError:
        raise
    except Exception as exc:
        logger.exception("STEP FAILED %s after %.1fs", name, time.perf_counter() - started)
        raise PipelineStepError(name, exc) from exc
    logger.info("STEP DONE %s in %.1fs", name, time.perf_counter() - started)


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
    return info
