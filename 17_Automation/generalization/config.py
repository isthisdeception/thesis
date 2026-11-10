"""Cross-dataset config: target datasets and generator relations come from YAML, never from code."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

RELATIONS = {"seen", "related", "unseen"}


class GeneralizationConfigError(ValueError):
    """The generalization config is missing a field or is inconsistent."""


@dataclass(frozen=True)
class GeneralizationConfig:
    raw: dict
    path: Path
    sha256: str

    def get(self, dotted: str):
        node: Any = self.raw
        for key in dotted.split("."):
            if not isinstance(node, dict) or key not in node:
                raise GeneralizationConfigError(f"{self.path}: missing {dotted}")
            node = node[key]
        return node

    @property
    def datasets(self) -> list[dict]:
        return self.raw["datasets"]

    def relation(self, dataset: dict, generator: str, label: str) -> str:
        """seen / related / unseen for fake images; 'real' for real ones."""

        if label == "real":
            return "real"
        if generator in self.get("training_generators"):
            return "seen"
        return (dataset.get("relation") or {}).get(generator, "unseen")


REQUIRED = [
    "evaluation_id", "experiment_id", "seed",
    "model.model_id", "model.export_name", "model.export_sha256", "model.positive_class", "model.search",
    "reference.name", "reference.predictions", "reference.split", "reference.processed_root", "training_generators",
    "inference.image_size", "inference.resize_interpolation", "inference.mean", "inference.std",
    "inference.batch_size", "inference.num_workers", "inference.sanity_images", "inference.sanity_atol",
]
DATASET_FIELDS = ["name", "description", "assignments", "partition", "processed_root"]


def load_config(path: str | Path) -> GeneralizationConfig:
    path = Path(path)
    text = path.read_bytes()
    raw = yaml.safe_load(text)
    if not isinstance(raw, dict):
        raise GeneralizationConfigError(f"{path}: not a mapping")
    config = GeneralizationConfig(raw, path, hashlib.sha256(text.replace(b"\r\n", b"\n")).hexdigest())
    for dotted in REQUIRED:
        config.get(dotted)
    datasets = raw.get("datasets")
    if not isinstance(datasets, list) or not datasets:
        raise GeneralizationConfigError(f"{path}: datasets must be a non-empty list")
    names = set()
    for d in datasets:
        missing = [f for f in DATASET_FIELDS if not d.get(f)]
        if missing:
            raise GeneralizationConfigError(f"{path}: dataset {d.get('name')!r} missing {missing}")
        if d["name"] in names:
            raise GeneralizationConfigError(f"{path}: duplicate dataset {d['name']!r}")
        names.add(d["name"])
        cap = d.get("max_images")
        if cap is not None and (not isinstance(cap, int) or isinstance(cap, bool) or cap <= 0):
            raise GeneralizationConfigError(f"{path}: {d['name']}: max_images must be a positive integer or null")
        bad = {g: r for g, r in (d.get("relation") or {}).items() if r not in RELATIONS}
        if bad:
            raise GeneralizationConfigError(f"{path}: {d['name']}: relation values must be in {sorted(RELATIONS)}: {bad}")
    return config
