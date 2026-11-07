"""Phase M7 checkpoint store: immutable full-state checkpoints, manifest, checksums, resume lookup."""

from __future__ import annotations

import hashlib
import json
import os
import random
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

from .logs import get_logger
from .settings import TrainingSettings

MANIFEST_NAME = "checkpoint_manifest.json"
QUARANTINE_DIR = "quarantine"
PARTIAL_SUFFIX = ".partial"
STATE_FORMAT_VERSION = 1


class CheckpointError(RuntimeError):
    """A checkpoint operation would break the never-overwrite or integrity rules."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def capture_rng() -> dict:
    import torch

    return {
        "python": random.getstate(),
        "numpy": np.random.get_state(),
        "torch": torch.get_rng_state(),
        "cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else [],
    }


def restore_rng(state: dict) -> None:
    import torch

    random.setstate(state["python"])
    np.random.set_state(state["numpy"])
    torch.set_rng_state(state["torch"].cpu())
    if state["cuda"] and torch.cuda.is_available():
        torch.cuda.set_rng_state_all([s.cpu() for s in state["cuda"]])


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


class CheckpointStore:
    """All checkpoint binaries of one experiment plus their manifest.

    Every file is written once (temp file + atomic rename) and registered with
    its SHA-256. Existing names are never overwritten; corrupt files are moved
    to ``quarantine/`` and marked in the manifest, never deleted.
    """

    def __init__(self, settings: TrainingSettings) -> None:
        self.settings = settings
        self.dir = settings.checkpoint_dir
        self.manifest_path = self.dir / MANIFEST_NAME
        self.markdown_path = settings.repo_root / settings.get("outputs.checkpoint_manifest")
        self.experiment_id = settings.experiment_id
        self.model_id = settings.get("model.model_id")
        self.config_sha256 = sha256_file(settings.config_path)

    # --- names (A.2) ----------------------------------------------------------

    def recovery_name(self, epoch: int) -> str:
        return f"{self.experiment_id}_epoch_{epoch:03d}.pth"

    @property
    def best_name(self) -> str:
        return f"{self.experiment_id}_best.pth"

    @property
    def last_name(self) -> str:
        return f"{self.experiment_id}_last.pth"

    @property
    def export_name(self) -> str:
        return f"{self.model_id}_export.pkl"

    @property
    def weights_name(self) -> str:
        return f"{self.model_id}_weights.pth"

    # --- manifest -------------------------------------------------------------

    def load_manifest(self) -> dict:
        if not self.manifest_path.exists():
            return {
                "experiment_id": self.experiment_id,
                "config_sha256": self.config_sha256,
                "checkpoint_dir": self.dir.relative_to(self.settings.repo_root).as_posix(),
                "artifact_dataset_slug": self.settings.config["outputs"].get("artifact_dataset_slug"),
                "entries": [],
            }
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        if manifest.get("experiment_id") != self.experiment_id:
            raise CheckpointError(
                f"{self.manifest_path} belongs to {manifest.get('experiment_id')}, not {self.experiment_id}"
            )
        return manifest

    def _write_manifest(self, manifest: dict) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        manifest["updated"] = _now()
        tmp = self.manifest_path.with_name(self.manifest_path.name + PARTIAL_SUFFIX)
        tmp.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        os.replace(tmp, self.manifest_path)
        self.write_markdown(manifest)

    def valid_entries(self, kind: str | None = None) -> list[dict]:
        return [
            e for e in self.load_manifest()["entries"]
            if e["status"] == "valid" and (kind is None or e["kind"] == kind)
        ]

    def find(self, name: str) -> dict | None:
        return next((e for e in self.valid_entries() if e["name"] == name), None)

    def path_of(self, entry: dict) -> Path:
        return self.dir / entry["name"]

    def verify(self, entry: dict) -> bool:
        path = self.path_of(entry)
        return path.is_file() and sha256_file(path) == entry["sha256"]

    # --- writing --------------------------------------------------------------

    def reserve(self, name: str) -> Path:
        """Temp path for a new file named ``name``; refuses if ``name`` already exists."""

        target = self.dir / name
        if target.exists():
            raise CheckpointError(f"refusing to overwrite existing checkpoint file {target}")
        self.dir.mkdir(parents=True, exist_ok=True)
        tmp = target.with_name(target.name + PARTIAL_SUFFIX)
        if tmp.exists():
            self._move_to_quarantine(tmp, "leftover partial write")
        return tmp

    def commit(self, tmp: Path, name: str, kind: str, meta: dict | None = None) -> dict:
        """Atomically move a finished temp file into place and register it."""

        target = self.dir / name
        if target.exists():
            raise CheckpointError(f"refusing to overwrite existing checkpoint file {target}")
        if not tmp.is_file():
            raise CheckpointError(f"temp file for {name} was not written: {tmp}")
        os.replace(tmp, target)
        entry = {
            "name": name,
            "kind": kind,
            "sha256": sha256_file(target),
            "bytes": target.stat().st_size,
            "created": _now(),
            "status": "valid",
            **(meta or {}),
        }
        manifest = self.load_manifest()
        manifest["entries"].append(entry)
        self._write_manifest(manifest)
        get_logger().info("checkpoint saved %s (%s, sha256 %s…)", name, kind, entry["sha256"][:12])
        return entry

    def save_state(self, name: str, state: dict, kind: str, meta: dict | None = None) -> dict:
        import torch

        tmp = self.reserve(name)
        torch.save(state, tmp)
        return self.commit(tmp, name, kind, meta)

    def copy_as(self, source: dict, name: str, kind: str) -> dict:
        """Write a named copy (best / last) of a verified checkpoint; idempotent if identical."""

        existing = self.find(name)
        if existing is not None:
            if existing["sha256"] == source["sha256"] and self.verify(existing):
                return existing
            raise CheckpointError(f"{name} already exists with different content; refusing to overwrite")
        if not self.verify(source):
            raise CheckpointError(f"source checkpoint {source['name']} failed checksum verification")
        tmp = self.reserve(name)
        shutil.copy2(self.path_of(source), tmp)
        meta = {k: source[k] for k in ("epoch", "phase", "phase_epoch", "monitor", "monitor_value") if k in source}
        entry = self.commit(tmp, name, kind, {**meta, "copied_from": source["name"]})
        if entry["sha256"] != source["sha256"]:
            raise CheckpointError(f"copy {name} does not match its source checksum")
        return entry

    # --- integrity / resume ---------------------------------------------------

    def _move_to_quarantine(self, path: Path, reason: str) -> Path:
        qdir = self.dir / QUARANTINE_DIR
        qdir.mkdir(parents=True, exist_ok=True)
        target = qdir / f"{path.name}.{datetime.now().strftime('%Y%m%dT%H%M%S%f')}"
        shutil.move(str(path), target)
        get_logger().warning("quarantined %s -> %s (%s)", path.name, target.relative_to(self.dir), reason)
        return target

    def quarantine(self, entry: dict, reason: str) -> None:
        path = self.path_of(entry)
        moved = self._move_to_quarantine(path, reason) if path.exists() else None
        manifest = self.load_manifest()
        for item in manifest["entries"]:
            if item["name"] == entry["name"] and item["status"] == "valid":
                item.update(
                    status="quarantined",
                    reason=reason,
                    quarantined_to=moved.relative_to(self.dir).as_posix() if moved else None,
                )
        self._write_manifest(manifest)

    def latest_valid_recovery(self, map_location: Any = "cpu") -> tuple[dict, dict] | None:
        """Newest recovery checkpoint whose checksum verifies; corrupt ones are quarantined."""

        import torch

        for entry in sorted(self.valid_entries("recovery"), key=lambda e: e["epoch"], reverse=True):
            if not self.verify(entry):
                self.quarantine(entry, "missing file or checksum mismatch")
                continue
            # Checkpoints carry RNG state (numpy arrays, tuples), so weights_only loading cannot read them.
            state = torch.load(self.path_of(entry), map_location=map_location, weights_only=False)
            if state.get("format_version") != STATE_FORMAT_VERSION or state.get("experiment_id") != self.experiment_id:
                self.quarantine(entry, "unexpected checkpoint format or experiment")
                continue
            return entry, state
        return None

    def verify_all(self) -> list[str]:
        """Names of valid manifest entries whose file is missing or fails its checksum."""

        return [e["name"] for e in self.valid_entries() if not self.verify(e)]

    # --- Git-side manifest ----------------------------------------------------

    def write_markdown(self, manifest: dict | None = None) -> None:
        manifest = manifest or self.load_manifest()
        rows = []
        for e in manifest["entries"]:
            monitor = f"{e['monitor']}={e['monitor_value']:.5f}" if e.get("monitor_value") is not None else "—"
            rows.append(
                f"| `{e['name']}` | {e['kind']} | {e.get('epoch', '—')} | {e.get('phase', '—')} | {monitor} | "
                f"`{e['sha256']}` | {e['bytes'] / 2**20:.1f} | {e['created']} | {e['status']} |"
            )
        lines = [
            f"# {self.experiment_id} — Checkpoint Manifest",
            "",
            "Generated by `17_Automation/training` from `checkpoint_manifest.json`; do not edit by hand.",
            "",
            f"- **Updated:** {manifest.get('updated', _now())}",
            f"- **Config SHA-256:** `{manifest['config_sha256']}`",
            f"- **Local checkpoint dir (Kaggle session):** `{manifest['checkpoint_dir']}`",
            f"- **Artifact tier:** Kaggle dataset `{manifest.get('artifact_dataset_slug')}` "
            "(binaries never go to Git)",
            "- **Policy:** `07_Checkpoints/checkpoint_policy.md`",
            "",
            "| File | Kind | Epoch | Phase | Monitor | SHA-256 | MB | Created | Status |",
            "|------|------|-------|-------|---------|---------|----|---------|--------|",
            *(rows or ["| — | — | — | — | — | — | — | — | — |"]),
            "",
        ]
        self.markdown_path.parent.mkdir(parents=True, exist_ok=True)
        self.markdown_path.write_text("\n".join(lines), encoding="utf-8")
