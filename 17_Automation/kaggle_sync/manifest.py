"""Manifest loading for Kaggle sync automation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass(frozen=True)
class DatasetMount:
    """A Kaggle Dataset expected to be attached to the session."""

    name: str
    slug: str
    mount_path: str
    tier: str = "data"
    required: bool = True


@dataclass(frozen=True)
class CheckpointSource:
    """A mounted artifact source copied into the working repo."""

    name: str
    input_path: str
    target_relpath: str
    required: bool = False


@dataclass(frozen=True)
class PublishTarget:
    """A Kaggle Dataset destination for experiment outputs."""

    dataset_slug: str
    title: str
    upload_dir: str
    version_notes: str = "Update experiment artifacts"
    is_private: bool = True
    convert_to_csv: bool = False


@dataclass(frozen=True)
class SyncPlan:
    """All inputs needed to bootstrap and sync a Kaggle training session."""

    repo_url: str
    repo_branch: str = "develop"
    repo_dir: str = "thesis"
    workspace_root: str = "/kaggle/working"
    kaggle_requirements: str = "environment/kaggle-requirements.txt"
    metadata_paths: list[str] = field(default_factory=list)
    dataset_mounts: list[DatasetMount] = field(default_factory=list)
    checkpoint_sources: list[CheckpointSource] = field(default_factory=list)
    publish_targets: list[PublishTarget] = field(default_factory=list)

    @property
    def workspace_path(self) -> Path:
        return Path(self.workspace_root)

    @property
    def repo_path(self) -> Path:
        return self.workspace_path / self.repo_dir


def _read_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"sync plan must be a mapping: {path}")
    return data


def load_sync_plan(path: str | Path) -> SyncPlan:
    """Load a manifest-driven sync plan from YAML."""

    source = Path(path)
    raw = _read_yaml(source)
    dataset_mounts = [DatasetMount(**item) for item in raw.get("dataset_mounts", [])]
    checkpoint_sources = [CheckpointSource(**item) for item in raw.get("checkpoint_sources", [])]
    publish_targets = [PublishTarget(**item) for item in raw.get("publish_targets", [])]
    return SyncPlan(
        repo_url=raw["repo_url"],
        repo_branch=raw.get("repo_branch", "develop"),
        repo_dir=raw.get("repo_dir", "thesis"),
        workspace_root=raw.get("workspace_root", "/kaggle/working"),
        kaggle_requirements=raw.get("kaggle_requirements", "environment/kaggle-requirements.txt"),
        metadata_paths=list(raw.get("metadata_paths", [])),
        dataset_mounts=dataset_mounts,
        checkpoint_sources=checkpoint_sources,
        publish_targets=publish_targets,
    )
