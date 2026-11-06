"""Read-only access to the canonical registries referenced by config.yaml."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .schema import REGISTRY_PATHS


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        # Some registries use ", " separators in the header row.
        return [
            {(key or "").strip(): (value or "").strip() for key, value in row.items()}
            for row in reader
        ]


@dataclass(frozen=True)
class Registries:
    dataset: list[dict[str, str]]
    split: list[dict[str, str]]
    preprocessing: list[dict[str, str]]
    candidate_models: list[dict[str, str]]
    model: list[dict[str, str]]

    def models(self) -> list[dict[str, str]]:
        """Registered models first, then approved candidates."""

        return [*self.model, *self.candidate_models]


def load_registries(repo_root: str | Path) -> Registries:
    """Load every registry used for ID checks; a missing file is an error."""

    root = Path(repo_root)
    missing = [rel for rel in REGISTRY_PATHS.values() if not (root / rel).is_file()]
    if missing:
        raise FileNotFoundError(f"registry file(s) not found under {root}: {', '.join(missing)}")
    return Registries(**{name: _read_rows(root / rel) for name, rel in REGISTRY_PATHS.items()})
