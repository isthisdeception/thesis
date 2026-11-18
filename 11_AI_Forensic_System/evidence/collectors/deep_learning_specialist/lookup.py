"""Read one model row from the model registry. The export location is the row, not a constant."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
REGISTRY = Path("05_Models/model_registry.csv")


@dataclass(frozen=True)
class RegisteredModel:
    model_id: str
    experiment_id: str
    export_pointer: str
    architecture: str
    status: str
    threshold: float | None
    positive_class: str | None


class RegistryError(LookupError):
    """The registry has no usable row for the requested model."""


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = [name.strip() for name in next(reader)]
        return [{header[i]: value.strip() for i, value in enumerate(row)} for row in reader if row]


def export_filename(pointer: str) -> str:
    if ":" not in pointer or not pointer.split(":")[-1]:
        raise RegistryError(f"export pointer has no filename: {pointer}")
    return pointer.split(":")[-1]


def lookup_model(repo: Path, model_id: str) -> RegisteredModel:
    path = repo / REGISTRY
    if not path.is_file():
        raise RegistryError(f"model registry is missing: {path}")
    rows = [row for row in _rows(path) if row.get("Model ID", "") == model_id]
    if len(rows) != 1:
        raise RegistryError(f"{model_id} has {len(rows)} registry rows")
    row = rows[0]
    pointer = row.get("Export Path", "")
    if not pointer:
        raise RegistryError(f"{model_id} has no export path")
    experiment_id = row["Experiment"]
    threshold, positive = _threshold(repo, experiment_id)
    return RegisteredModel(
        model_id=model_id,
        experiment_id=experiment_id,
        export_pointer=pointer,
        architecture=row.get("Architecture", ""),
        status=row.get("Status", ""),
        threshold=threshold,
        positive_class=positive,
    )


def _threshold(repo: Path, experiment_id: str) -> tuple[float | None, str | None]:
    path = repo / "06_Experiments" / experiment_id / "metrics" / "threshold.json"
    if not path.is_file():
        return None, None
    payload = json.loads(path.read_text(encoding="utf-8"))
    value = payload.get("value")
    positive = payload.get("positive_class")
    return (float(value) if value is not None else None), (str(positive) if positive else None)
