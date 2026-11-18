"""Seven structured log channels (§8.9): application, api, inference, case, error, audit, performance."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_CHANNELS = (
    "application",
    "api",
    "inference",
    "case",
    "error",
    "audit",
    "performance",
)


def build_logging_dict(log_dir: Path) -> dict:
    """Build a Django LOGGING dictionary with rotating file handlers for all 7 required channels."""

    log_dir.mkdir(parents=True, exist_ok=True)
    handlers: dict[str, dict] = {}
    loggers: dict[str, dict] = {}

    for channel in LOG_CHANNELS:
        handler_name = f"{channel}_file"
        handlers[handler_name] = {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(log_dir / f"{channel}.log"),
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 3,
            "encoding": "utf-8",
            "formatter": "forensic_structured",
        }
        loggers[f"forensic.{channel}"] = {
            "handlers": [handler_name],
            "level": "INFO",
            "propagate": False,
        }

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "forensic_structured": {
                "format": "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            },
        },
        "handlers": handlers,
        "loggers": loggers,
    }


def get_channel_logger(channel: str, log_dir: Path | None = None) -> logging.Logger:
    """Return `forensic.<channel>` logger, attaching its file handler if not yet attached."""

    if channel not in LOG_CHANNELS:
        raise ValueError(f"unknown log channel {channel!r}; expected one of {LOG_CHANNELS}")
    logger = logging.getLogger(f"forensic.{channel}")
    logger.setLevel(logging.INFO)
    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        target = str((log_dir / f"{channel}.log").resolve())
        has_target = any(
            isinstance(h, RotatingFileHandler) and str(Path(h.baseFilename).resolve()) == target
            for h in logger.handlers
        )
        if not has_target:
            handler = RotatingFileHandler(target, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
            handler.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s"))
            logger.addHandler(handler)
    return logger
