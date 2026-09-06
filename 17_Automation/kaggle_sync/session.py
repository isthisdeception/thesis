"""Idempotent Kaggle sync actions for STEP-031."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

from .manifest import SyncPlan


def _run(cmd: list[str], *, cwd: Path | None = None, dry_run: bool = False) -> None:
    if dry_run:
        print("$", " ".join(cmd))
        return
    subprocess.run(cmd, cwd=cwd, check=True)


def _copy_tree(src: Path, dst: Path) -> None:
    if src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.rglob("*"):
        rel = item.relative_to(src)
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _verify_dataset_mounts(plan: SyncPlan) -> dict[str, dict[str, str | bool]]:
    mounts: dict[str, dict[str, str | bool]] = {}
    for mount in plan.dataset_mounts:
        present = Path(mount.mount_path).exists()
        if mount.required and not present:
            raise FileNotFoundError(
                f"required Kaggle input missing for {mount.name}: {mount.mount_path}"
            )
        mounts[mount.name] = {
            "slug": mount.slug,
            "mount_path": mount.mount_path,
            "tier": mount.tier,
            "present": present,
        }
    return mounts


def bootstrap_repo(plan: SyncPlan, *, dry_run: bool = False) -> Path:
    """Clone or update the repo and verify environment inputs."""

    workspace = plan.workspace_path
    repo_path = plan.repo_path
    workspace.mkdir(parents=True, exist_ok=True)

    if repo_path.exists():
        _run(["git", "fetch", "origin"], cwd=repo_path, dry_run=dry_run)
        _run(["git", "checkout", plan.repo_branch], cwd=repo_path, dry_run=dry_run)
        _run(["git", "pull", "--ff-only", "origin", plan.repo_branch], cwd=repo_path, dry_run=dry_run)
    else:
        _run(
            ["git", "clone", "--branch", plan.repo_branch, plan.repo_url, str(repo_path)],
            cwd=workspace,
            dry_run=dry_run,
        )

    requirements_path = repo_path / plan.kaggle_requirements
    if requirements_path.exists() and requirements_path.read_text(encoding="utf-8").strip():
        _run([sys.executable, "-m", "pip", "install", "-r", str(requirements_path)], dry_run=dry_run)

    mounts = _verify_dataset_mounts(plan)
    payload = {
        "generated_utc": datetime.now(UTC).isoformat(),
        "repo_url": plan.repo_url,
        "repo_branch": plan.repo_branch,
        "repo_path": str(repo_path),
        "dataset_mounts": mounts,
    }
    if dry_run:
        print(f"would write bootstrap report to {repo_path / '17_Automation' / 'kaggle_sync' / 'session_bootstrap.json'}")
    else:
        _write_json(repo_path / "17_Automation" / "kaggle_sync" / "session_bootstrap.json", payload)
    return repo_path


def resume_checkpoints(plan: SyncPlan, *, dry_run: bool = False) -> list[str]:
    """Copy mounted checkpoints into the working repo."""

    repo_path = plan.repo_path
    copied: list[str] = []
    for source in plan.checkpoint_sources:
        src = Path(source.input_path)
        dst = repo_path / source.target_relpath
        if not src.exists():
            if source.required:
                raise FileNotFoundError(f"required checkpoint source missing: {src}")
            continue
        if dry_run:
            print(f"copy {src} -> {dst}")
        else:
            if dst.exists():
                shutil.rmtree(dst) if dst.is_dir() else dst.unlink()
            _copy_tree(src, dst)
        copied.append(str(dst))

    if dry_run:
        print(f"would write checkpoint report to {repo_path / '17_Automation' / 'kaggle_sync' / 'checkpoint_resume.json'}")
    else:
        _write_json(
            repo_path / "17_Automation" / "kaggle_sync" / "checkpoint_resume.json",
            {"generated_utc": datetime.now(UTC).isoformat(), "copied_targets": copied},
        )
    return copied


def publish_artifacts(plan: SyncPlan, *, dry_run: bool = False) -> list[str]:
    """Stage and optionally upload artifact-tier outputs to Kaggle Datasets."""

    repo_path = plan.repo_path
    staged: list[str] = []
    for target in plan.publish_targets:
        source_dir = repo_path / target.upload_dir
        if not source_dir.exists():
            raise FileNotFoundError(f"artifact source does not exist: {source_dir}")
        slug_leaf = target.dataset_slug.split("/")[-1]
        stage_dir = plan.workspace_path / "_kaggle_publish" / slug_leaf
        if not dry_run and stage_dir.exists():
            shutil.rmtree(stage_dir)
        if dry_run:
            print(f"stage {source_dir} -> {stage_dir}")
        else:
            _copy_tree(source_dir, stage_dir)
            metadata = {
                "title": target.title,
                "id": target.dataset_slug,
                "licenses": [{"name": "CC0-1.0"}],
                "isPrivate": target.is_private,
            }
            (stage_dir / "dataset-metadata.json").write_text(
                json.dumps(metadata, indent=2), encoding="utf-8"
            )

        cmd = [
            "kaggle",
            "datasets",
            "version",
            "-p",
            str(stage_dir),
            "-m",
            target.version_notes,
            "-r",
            "zip",
        ]
        if target.convert_to_csv:
            cmd.extend(["--keep-tabular"])
        _run(cmd, dry_run=dry_run)
        staged.append(str(stage_dir))

    if dry_run:
        print(f"would write publish report to {repo_path / '17_Automation' / 'kaggle_sync' / 'artifact_publish.json'}")
    else:
        _write_json(
            repo_path / "17_Automation" / "kaggle_sync" / "artifact_publish.json",
            {"generated_utc": datetime.now(UTC).isoformat(), "staged_targets": staged},
        )
    return staged


def push_metadata(
    plan: SyncPlan,
    *,
    commit_message: str = "sync: update experiment metadata from Kaggle",
    dry_run: bool = False,
) -> None:
    """Commit and push source-tier metadata back to GitHub."""

    repo_path = plan.repo_path
    if not plan.metadata_paths:
        raise ValueError("metadata_paths is empty; nothing is allowed to return to Git")
    if dry_run:
        for relpath in plan.metadata_paths:
            print(f"git add {repo_path / relpath}")
        print(f"git commit -m {commit_message}")
        print(f"git push origin {plan.repo_branch}")
        return

    _run(["git", "config", "user.name", os.environ.get("GIT_AUTHOR_NAME", "Kaggle Automation")], cwd=repo_path, dry_run=dry_run)
    _run(
        ["git", "config", "user.email", os.environ.get("GIT_AUTHOR_EMAIL", "kaggle-automation@local")],
        cwd=repo_path,
        dry_run=dry_run,
    )
    for relpath in plan.metadata_paths:
        _run(["git", "add", relpath], cwd=repo_path, dry_run=dry_run)

    status = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=repo_path,
        check=False,
        capture_output=True,
    )
    if status.returncode == 0:
        print("No metadata changes staged; skipping commit.")
        return
    if status.returncode not in (0, 1):
        raise RuntimeError(status.stderr.decode("utf-8", errors="replace"))

    _run(["git", "commit", "-m", commit_message], cwd=repo_path, dry_run=dry_run)
    _run(["git", "push", "origin", plan.repo_branch], cwd=repo_path, dry_run=dry_run)
