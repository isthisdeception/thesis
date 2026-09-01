"""Core splitting logic — grouped assignments + leakage assertions."""

from __future__ import annotations

import hashlib
import json
import random
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PARTITIONS = ("train", "val", "test")


@dataclass
class SplitConfig:
    split_id: str
    output_id: str
    dataset_id: str
    pipeline_id: str
    scheme: str
    seed: int = 42
    ratios: tuple[float, float, float] = (0.7, 0.15, 0.15)
    group_by: list[str] = field(default_factory=lambda: ["identity", "generator"])
    held_out_generators: list[str] = field(default_factory=list)
    official_test_column: str | None = None
    official_test_values: list[str] = field(default_factory=list)
    train_val_ratio: tuple[float, float] = (0.85, 0.15)
    notes: str = ""


def group_key(row: dict[str, str], group_by: list[str]) -> str:
    parts: list[str] = []
    for col in group_by:
        val = (row.get(col) or "").strip()
        if not val and col == "identity":
            val = Path(row.get("relative_path", "")).stem
        if val:
            parts.append(f"{col}={val}")
    if not parts:
        parts.append(f"hash={row.get('content_hash', '')}")
    return "|".join(parts)


def _allocate_groups(
    groups: list[str],
    ratios: tuple[float, float, float],
    rng: random.Random,
) -> dict[str, str]:
    shuffled = list(groups)
    rng.shuffle(shuffled)
    n = len(shuffled)
    n_train = int(n * ratios[0])
    n_val = int(n * ratios[1])
    n_test = n - n_train - n_val
    if n >= 3 and n_test == 0:
        n_test = 1
        n_train = max(1, n_train - 1)
    assignment: dict[str, str] = {}
    for g in shuffled[:n_train]:
        assignment[g] = "train"
    for g in shuffled[n_train : n_train + n_val]:
        assignment[g] = "val"
    for g in shuffled[n_train + n_val :]:
        assignment[g] = "test"
    return assignment


def merge_groups_by_hash(rows: list[dict[str, str]], group_by: list[str]) -> dict[str, str]:
    """Map each processed_path to a merged group id (union groups sharing content_hash)."""
    parent: dict[str, str] = {}

    def find(x: str) -> str:
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    path_group: dict[str, str] = {}
    hash_anchor: dict[str, str] = {}
    for row in rows:
        gk = group_key(row, group_by)
        path = row["processed_path"]
        path_group[path] = gk
        h = (row.get("content_hash") or "").strip()
        if not h:
            continue
        if h in hash_anchor:
            union(gk, hash_anchor[h])
        else:
            hash_anchor[h] = gk

    return {path: find(gk) for path, gk in path_group.items()}


def _assign_rows_from_groups(
    rows: list[dict[str, str]],
    group_partition: dict[str, str],
    merged_groups: dict[str, str],
) -> dict[str, str]:
    return {
        row["processed_path"]: group_partition[merged_groups[row["processed_path"]]]
        for row in rows
    }


def split_grouped_random(
    rows: list[dict[str, str]],
    cfg: SplitConfig,
) -> dict[str, str]:
    rng = random.Random(cfg.seed)
    merged = merge_groups_by_hash(rows, cfg.group_by)
    unique_groups = sorted(set(merged.values()))
    group_partition = _allocate_groups(unique_groups, cfg.ratios, rng)
    return _assign_rows_from_groups(rows, group_partition, merged)


def split_logo(
    rows: list[dict[str, str]],
    cfg: SplitConfig,
) -> dict[str, str]:
    rng = random.Random(cfg.seed)
    held = {g.lower() for g in cfg.held_out_generators}
    merged = merge_groups_by_hash(rows, cfg.group_by)

    group_partition: dict[str, str] = {}
    for row in rows:
        gk = merged[row["processed_path"]]
        gen = (row.get("generator") or "").lower()
        if gen in held:
            group_partition[gk] = "test"

    rest_groups = [g for g in set(merged.values()) if group_partition.get(g) != "test"]
    sub = _allocate_groups(rest_groups, (cfg.train_val_ratio[0], cfg.train_val_ratio[1], 0.0), rng)
    for g in rest_groups:
        if g not in group_partition:
            part = sub.get(g, "train")
            group_partition[g] = "val" if part == "test" else part

    return _assign_rows_from_groups(rows, group_partition, merged)


def split_official_holdout(
    rows: list[dict[str, str]],
    cfg: SplitConfig,
) -> dict[str, str]:
    """Respect dataset-native holdout (e.g. DS0003 valid, DS0005 val) then subsplit train."""
    rng = random.Random(cfg.seed)
    col = cfg.official_test_column or "split"
    test_vals = {v.lower() for v in cfg.official_test_values}
    merged = merge_groups_by_hash(rows, cfg.group_by)

    group_partition: dict[str, str] = {}
    for row in rows:
        gk = merged[row["processed_path"]]
        if (row.get(col) or "").lower() in test_vals:
            group_partition[gk] = "test"

    rest_groups = [g for g in set(merged.values()) if group_partition.get(g) != "test"]
    sub = _allocate_groups(rest_groups, (cfg.train_val_ratio[0], cfg.train_val_ratio[1], 0.0), rng)
    for g in rest_groups:
        if g not in group_partition:
            part = sub.get(g, "train")
            group_partition[g] = "val" if part == "test" else part

    return _assign_rows_from_groups(rows, group_partition, merged)


def assert_no_leakage(
    rows: list[dict[str, str]],
    assignments: dict[str, str],
    *,
    group_by: list[str],
    logo_generators: list[str] | None = None,
) -> dict[str, Any]:
    """Fail loudly if identity/generator/hash crosses partitions."""
    issues: list[str] = []

    id_parts: dict[str, set[str]] = defaultdict(set)
    gen_parts: dict[str, set[str]] = defaultdict(set)
    hash_parts: dict[str, set[str]] = defaultdict(set)

    for row in rows:
        path = row["processed_path"]
        part = assignments[path]
        gk = group_key(row, group_by)
        id_parts[gk].add(part)
        gen = (row.get("generator") or "none").lower()
        gen_parts[gen].add(part)
        h = row.get("content_hash", "")
        if h:
            hash_parts[h].add(part)

    for gk, parts in id_parts.items():
        if len(parts) > 1:
            issues.append(f"group {gk} spans {sorted(parts)}")

    for h, parts in hash_parts.items():
        if len(parts) > 1:
            issues.append(f"hash {h[:12]}... spans {sorted(parts)}")

    if logo_generators:
        held = {g.lower() for g in logo_generators}
        for gen, parts in gen_parts.items():
            if gen in held and "train" in parts:
                issues.append(f"held-out generator {gen} appears in train")

    return {
        "passed": len(issues) == 0,
        "issues": issues,
        "group_count": len(id_parts),
        "generator_count": len(gen_parts),
    }


def fingerprint(assignments: dict[str, str]) -> str:
    payload = json.dumps(assignments, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


def summarize(assignments: dict[str, str], rows: list[dict[str, str]]) -> dict[str, Any]:
    by_part: Counter[str] = Counter(assignments.values())
    class_by_part: dict[str, Counter[str]] = {p: Counter() for p in PARTITIONS}
    gen_by_part: dict[str, Counter[str]] = {p: Counter() for p in PARTITIONS}
    row_map = {r["processed_path"]: r for r in rows}
    for path, part in assignments.items():
        row = row_map[path]
        class_by_part[part][row.get("class_label") or "unknown"] += 1
        gen_by_part[part][row.get("generator") or "none"] += 1
    return {
        "counts": dict(by_part),
        "class_by_partition": {k: dict(v) for k, v in class_by_part.items() if v},
        "generator_by_partition": {k: dict(v) for k, v in gen_by_part.items() if v},
    }
