"""Robustness config: perturbations and levels come from YAML, never from code."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .perturbations import KINDS, check_level

CLEAN = "clean"


class RobustnessConfigError(ValueError):
    """The robustness config is missing a field or names an unknown perturbation."""


@dataclass(frozen=True)
class Condition:
    id: str
    perturbation: str
    kind: str
    level: Any
    rank: int  # 0 = clean, 1 = mildest level


@dataclass(frozen=True)
class RobustnessConfig:
    raw: dict
    path: Path
    sha256: str

    def get(self, dotted: str):
        node: Any = self.raw
        for key in dotted.split("."):
            if not isinstance(node, dict) or key not in node:
                raise RobustnessConfigError(f"{self.path}: missing {dotted}")
            node = node[key]
        return node

    @property
    def conditions(self) -> list[Condition]:
        out = [Condition(CLEAN, CLEAN, CLEAN, None, 0)]
        for p in self.raw["perturbations"]:
            for rank, level in enumerate(p["levels"], start=1):
                out.append(Condition(f"{p['name']}@{level_label(level)}", p["name"], p["kind"], level, rank))
        return out


def level_label(level) -> str:
    if isinstance(level, (list, tuple)):
        return "_".join(level_label(x) for x in level)
    return f"{level:g}" if isinstance(level, float) else str(level)


REQUIRED = [
    "evaluation_id", "experiment_id", "seed",
    "model.model_id", "model.export_name", "model.export_sha256", "model.positive_class",
    "data.predictions", "data.split", "data.metadata_index", "data.processed_root",
    "inference.image_size", "inference.resize_interpolation", "inference.mean", "inference.std",
    "inference.batch_size", "inference.num_workers", "inference.clean_check_atol",
    "analysis.tolerance", "analysis.ranking_kept",
]


def load_config(path: str | Path) -> RobustnessConfig:
    path = Path(path)
    text = path.read_bytes()
    raw = yaml.safe_load(text)
    if not isinstance(raw, dict):
        raise RobustnessConfigError(f"{path}: not a mapping")
    config = RobustnessConfig(raw, path, hashlib.sha256(text).hexdigest())
    for dotted in REQUIRED:
        config.get(dotted)
    perturbations = raw.get("perturbations")
    if not isinstance(perturbations, list) or not perturbations:
        raise RobustnessConfigError(f"{path}: perturbations must be a non-empty list")
    names = set()
    for p in perturbations:
        name, kind, levels = p.get("name"), p.get("kind"), p.get("levels")
        if not name or name == CLEAN or "@" in str(name):
            raise RobustnessConfigError(f"{path}: invalid perturbation name {name!r}")
        if name in names:
            raise RobustnessConfigError(f"{path}: duplicate perturbation name {name!r}")
        names.add(name)
        if kind not in KINDS:
            raise RobustnessConfigError(f"{path}: {name}: unknown kind {kind!r}; known: {sorted(KINDS)}")
        if not isinstance(levels, list) or not levels:
            raise RobustnessConfigError(f"{path}: {name}: levels must be a non-empty list")
        for level in levels:
            try:
                check_level(kind, level)
            except ValueError as exc:
                raise RobustnessConfigError(f"{path}: {name}: {exc}") from exc
    ids = [c.id for c in config.conditions]
    if len(ids) != len(set(ids)):
        raise RobustnessConfigError(f"{path}: condition ids are not unique")
    return config
