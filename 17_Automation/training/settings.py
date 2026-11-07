"""Resolve a validated config.yaml into typed training settings."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from config_validation import find_repo_root, validate_config


class TrainingConfigError(ValueError):
    """The config is unusable for training (failed validation or missing key)."""


def require(config: dict, dotted: str) -> Any:
    """Return ``config[a][b]...`` for ``"a.b"``; raise if any part is missing or null."""

    node: Any = config
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node or node[part] is None:
            raise TrainingConfigError(f"config is missing required key '{dotted}'")
        node = node[part]
    return node


@dataclass(frozen=True)
class TrainingSettings:
    """Everything the pipeline needs, resolved to absolute paths."""

    config: dict
    config_path: Path
    repo_root: Path
    experiment_id: str
    experiment_dir: Path
    checkpoint_dir: Path
    assignments_csv: Path
    processed_root: Path

    def get(self, dotted: str) -> Any:
        return require(self.config, dotted)

    @property
    def logs_dir(self) -> Path:
        return self.experiment_dir / "logs"

    @property
    def metrics_dir(self) -> Path:
        return self.experiment_dir / "metrics"

    @property
    def predictions_dir(self) -> Path:
        return self.experiment_dir / "predictions"

    @property
    def curves_dir(self) -> Path:
        return self.experiment_dir / "learning_curves"

    @property
    def vocab(self) -> list[str]:
        return list(self.get("dataset.vocab"))

    @property
    def positive_class(self) -> str:
        return self.get("metrics.positive_class")


def load_settings(
    config_path: str | Path,
    *,
    repo_root: str | Path | None = None,
    check_registries: bool = True,
) -> TrainingSettings:
    """Parse and validate (ready mode) a config, then resolve its paths.

    ``check_registries=False`` skips registry lookups; it exists for the smoke
    test and must not be used for a real experiment.
    """

    path = Path(config_path).resolve()
    if not path.is_file():
        raise TrainingConfigError(f"config not found: {path}")
    try:
        config = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise TrainingConfigError(f"config YAML does not parse: {path}: {exc}") from exc

    root = Path(repo_root).resolve() if repo_root is not None else find_repo_root(path.parent)
    report = validate_config(config, repo_root=root if check_registries else None, path=str(path))
    report.raise_if_failed()

    experiment_dir = root / require(config, "outputs.experiment_dir")
    if experiment_dir.resolve() != path.parent:
        raise TrainingConfigError(
            f"config must live in its experiment folder {experiment_dir}, found at {path}"
        )
    return TrainingSettings(
        config=config,
        config_path=path,
        repo_root=root,
        experiment_id=require(config, "experiment_id"),
        experiment_dir=experiment_dir,
        checkpoint_dir=root / require(config, "outputs.checkpoint_dir"),
        assignments_csv=root / require(config, "split.assignments_csv"),
        processed_root=Path(require(config, "dataset.processed_root")),
    )
