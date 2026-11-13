"""Ablation plan: one entry per experiment, each changing exactly one factor of the baseline."""

from __future__ import annotations

import copy
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

# Keys every experiment sets for itself. They are bookkeeping, not training factors.
IDENTITY_KEYS = {
    "experiment_id", "model.model_id", "purpose", "expected_outcome", "study_track", "notes",
    "outputs.experiment_dir", "outputs.checkpoint_dir", "outputs.checkpoint_manifest", "outputs.artifact_dataset_slug",
    "git_commit", "timestamp",
    # The value is reused unchanged; only its provenance label changes (no new LR Finder run).
    "learning_rate.source",
}


class AblationPlanError(ValueError):
    """The ablation plan is inconsistent or would change more than one factor."""


@dataclass(frozen=True)
class Ablation:
    experiment_id: str
    model_id: str
    evaluation_id: str
    factor: str
    question: str
    changes: dict
    expected_outcome: str


@dataclass(frozen=True)
class AblationPlan:
    raw: dict
    path: Path
    baseline: str
    noise_reference: str
    artifact_slug_pattern: str
    ablations: list[Ablation]

    def artifact_slug(self, experiment_id: str) -> str:
        return self.artifact_slug_pattern.format(exp=experiment_id.lower())


def get(config: dict, dotted: str) -> Any:
    node: Any = config
    for key in dotted.split("."):
        if not isinstance(node, dict) or key not in node:
            raise KeyError(dotted)
        node = node[key]
    return node


def set_key(config: dict, dotted: str, value: Any) -> None:
    *head, last = dotted.split(".")
    node = config
    for key in head:
        node = node[key]
    if last not in node:
        raise KeyError(dotted)
    node[last] = value


def flatten(config: Any, prefix: str = "") -> dict[str, Any]:
    if not isinstance(config, dict):
        return {prefix: config}
    out: dict[str, Any] = {}
    for key, value in config.items():
        out.update(flatten(value, f"{prefix}.{key}" if prefix else str(key)))
    return out


def changed_keys(base: dict, other: dict) -> set[str]:
    a, b = flatten(base), flatten(other)
    return {k for k in set(a) | set(b) if a.get(k, object()) != b.get(k, object())}


def check_one_factor(base: dict, config: dict, ablation: Ablation) -> None:
    """Every difference from the baseline is an identity key or one of this ablation's planned changes."""

    extra = changed_keys(base, config) - IDENTITY_KEYS - set(ablation.changes)
    if extra:
        raise AblationPlanError(f"{ablation.experiment_id} changes more than its factor {ablation.factor!r}: {sorted(extra)}")
    unchanged = [k for k in ablation.changes if get(config, k) == get(base, k)]
    if unchanged:
        raise AblationPlanError(f"{ablation.experiment_id}: planned change(s) equal the baseline: {unchanged}")


def load_plan(path: str | Path) -> AblationPlan:
    path = Path(path)
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not raw.get("ablations"):
        raise AblationPlanError(f"{path}: needs a non-empty 'ablations' list")
    ablations, seen = [], set()
    patterns = {"experiment_id": r"EXP\d{4}", "model_id": r"MODEL\d{4}", "evaluation_id": r"EVAL\d{4}"}
    for entry in raw["ablations"]:
        for field, pattern in patterns.items():
            value = entry.get(field)
            if not isinstance(value, str) or not re.fullmatch(pattern, value):
                raise AblationPlanError(f"{path}: {field} {value!r} does not match {pattern}")
            if value in seen:
                raise AblationPlanError(f"{path}: {value} is used twice")
            seen.add(value)
        for field in ("factor", "question", "expected_outcome"):
            if not str(entry.get(field) or "").strip():
                raise AblationPlanError(f"{path}: {entry['experiment_id']} needs {field}")
        changes = entry.get("changes")
        if not isinstance(changes, dict) or not changes:
            raise AblationPlanError(f"{path}: {entry['experiment_id']} needs a non-empty 'changes' mapping")
        if set(changes) & IDENTITY_KEYS:
            raise AblationPlanError(f"{path}: {entry['experiment_id']} changes identity keys {sorted(set(changes) & IDENTITY_KEYS)}")
        ablations.append(Ablation(entry["experiment_id"], entry["model_id"], entry["evaluation_id"], entry["factor"],
                                  " ".join(str(entry["question"]).split()), copy.deepcopy(changes),
                                  " ".join(str(entry["expected_outcome"]).split())))
    noise = raw.get("noise_reference")
    if noise not in {a.experiment_id for a in ablations}:
        raise AblationPlanError(f"{path}: noise_reference {noise!r} is not one of the ablations")
    return AblationPlan(raw, path, raw["baseline"], noise, raw["artifact_slug_pattern"], ablations)
