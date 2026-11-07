"""Fixed CSV schemas for training records (documented in training/LOGGING.md)."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

EPOCH_LEADING = ["session", "epoch", "phase", "phase_epoch", "train_loss", "valid_loss"]
EPOCH_TRAILING = ["seconds", "lr_head", "gpu_peak_allocated_mb", "gpu_peak_reserved_mb"]
BATCH_COLUMNS = ["session", "iteration", "epoch", "phase", "loss", "lr"]
METRIC_SUMMARY_COLUMNS = [
    "split", "threshold", "roc_auc", "pr_auc", "f1", "balanced_accuracy", "mcc", "precision", "recall",
    "specificity", "fpr", "fnr", "accuracy", "ece", "brier", "tp", "tn", "fp", "fn", "n", "n_positive",
]


class RecordSchemaError(ValueError):
    """An existing CSV has a different header than the schema being appended."""


def epoch_columns(monitor_names: Iterable[str]) -> list[str]:
    """Leading columns, then the FastAI monitors in config order, then timing/resources."""

    monitors = [m for m in monitor_names if m not in {"epoch", "train_loss", "valid_loss", "time"}]
    return [*EPOCH_LEADING, *monitors, *EPOCH_TRAILING]


def append_rows(path: Path, columns: list[str], rows: Iterable[dict]) -> None:
    """Append rows; write the header for a new file, refuse a header mismatch on an existing one."""

    rows = list(rows)
    if not rows:
        return
    extra = sorted({key for row in rows for key in row} - set(columns))
    if extra:
        raise RecordSchemaError(f"{path.name}: values for columns outside the schema: {extra}")
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists() or path.stat().st_size == 0
    if not new:
        with path.open(newline="", encoding="utf-8") as handle:
            header = next(csv.reader(handle), [])
        if header != columns:
            raise RecordSchemaError(f"{path.name}: existing header {header} differs from schema {columns}")
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        if new:
            writer.writeheader()
        writer.writerows(rows)


def write_rows(path: Path, columns: list[str], rows: Iterable[dict]) -> None:
    """Write a complete CSV (final, end-of-run files)."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
