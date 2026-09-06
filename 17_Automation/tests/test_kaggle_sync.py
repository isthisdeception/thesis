"""Tests for STEP-031 Kaggle sync automation."""

from __future__ import annotations

from pathlib import Path

import pytest

from kaggle_sync.manifest import load_sync_plan
from kaggle_sync.session import bootstrap_repo, resume_checkpoints


def test_load_sync_plan_parses_yaml(tmp_path: Path) -> None:
    plan_path = tmp_path / "sync_plan.yaml"
    plan_path.write_text(
        """
repo_url: https://github.com/example/thesis.git
repo_branch: develop
repo_dir: thesis
metadata_paths:
  - 06_Experiments/experiment_registry.csv
dataset_mounts:
  - name: ds0003_raw
    slug: xhlulu/140k-real-and-fake-faces
    mount_path: /kaggle/input/140k-real-and-fake-faces
checkpoint_sources:
  - name: exp0001
    input_path: /kaggle/input/exp0001-checkpoints
    target_relpath: 06_Experiments/EXP0001/notebook/checkpoints
publish_targets:
  - dataset_slug: isthisdeception/exp0001-artifacts
    title: EXP0001 Artifact Tier
    upload_dir: 06_Experiments/EXP0001
""".strip(),
        encoding="utf-8",
    )

    plan = load_sync_plan(plan_path)

    assert plan.repo_url.endswith("/thesis.git")
    assert plan.dataset_mounts[0].slug == "xhlulu/140k-real-and-fake-faces"
    assert plan.checkpoint_sources[0].target_relpath.endswith("checkpoints")
    assert plan.publish_targets[0].dataset_slug == "isthisdeception/exp0001-artifacts"


def test_bootstrap_repo_requires_declared_mounts(tmp_path: Path) -> None:
    plan_path = tmp_path / "sync_plan.yaml"
    plan_path.write_text(
        f"""
repo_url: https://github.com/example/thesis.git
repo_dir: thesis
workspace_root: {tmp_path.as_posix()}
dataset_mounts:
  - name: missing
    slug: owner/missing
    mount_path: {tmp_path.as_posix()}/does-not-exist
""".strip(),
        encoding="utf-8",
    )
    plan = load_sync_plan(plan_path)

    with pytest.raises(FileNotFoundError):
        bootstrap_repo(plan, dry_run=True)


def test_resume_checkpoints_copies_attached_tree(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    repo_root = workspace / "thesis"
    source_root = tmp_path / "mounted-checkpoints"
    source_root.mkdir(parents=True)
    repo_root.mkdir(parents=True)
    artifact = source_root / "model.pth"
    artifact.write_text("weights", encoding="utf-8")

    plan_path = tmp_path / "sync_plan.yaml"
    plan_path.write_text(
        f"""
repo_url: https://github.com/example/thesis.git
repo_dir: thesis
workspace_root: {workspace.as_posix()}
checkpoint_sources:
  - name: exp0001
    input_path: {source_root.as_posix()}
    target_relpath: 06_Experiments/EXP0001/notebook/checkpoints
    required: true
""".strip(),
        encoding="utf-8",
    )
    plan = load_sync_plan(plan_path)

    copied = resume_checkpoints(plan)

    target = repo_root / "06_Experiments" / "EXP0001" / "notebook" / "checkpoints" / "model.pth"
    assert copied == [str(repo_root / "06_Experiments" / "EXP0001" / "notebook" / "checkpoints")]
    assert target.read_text(encoding="utf-8") == "weights"
