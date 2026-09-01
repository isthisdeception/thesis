"""PPMOD06 — Normalization stats / optional apply."""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

import numpy as np
from PIL import Image

from .types import ImageRecord, ModuleError

MODULE_ID = "PPMOD06"

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


@dataclass
class NormalizationParams:
    norm_mode: str = "imagenet"
    imagenet_mean: list[float] = field(default_factory=lambda: list(IMAGENET_MEAN))
    imagenet_std: list[float] = field(default_factory=lambda: list(IMAGENET_STD))
    dataset_stats_path: Path | None = None
    apply_on_disk: bool = False
    stats_sample_n: int = 3000
    random_seed: int = 42


def _to_float01(im: Image.Image) -> np.ndarray:
    arr = np.asarray(im.convert("RGB"), dtype=np.float64) / 255.0
    return arr


def resolve_mean_std(params: NormalizationParams) -> tuple[list[float], list[float]]:
    mode = params.norm_mode.lower()
    if mode == "none":
        return [0.0, 0.0, 0.0], [1.0, 1.0, 1.0]
    if mode == "imagenet":
        return list(params.imagenet_mean), list(params.imagenet_std)
    if mode == "dataset":
        if params.dataset_stats_path and Path(params.dataset_stats_path).is_file():
            data = json.loads(Path(params.dataset_stats_path).read_text(encoding="utf-8"))
            return list(data["mean"]), list(data["std"])
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="MISSING_STATS",
            message="norm_mode=dataset requires dataset_stats_path with existing JSON "
            "(call compute_dataset_stats first)",
        )
    raise ModuleError(
        module_id=MODULE_ID,
        reason_code="INVALID_PARAM",
        message=f"unknown norm_mode={params.norm_mode!r}",
    )


def compute_dataset_stats(
    images: Sequence[Image.Image],
    params: NormalizationParams,
) -> dict:
    """Compute channel mean/std over a (possibly sampled) image list."""
    if not images:
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="EMPTY_INPUT",
            message="cannot compute stats on empty image list",
        )
    rng = random.Random(params.random_seed)
    idxs = list(range(len(images)))
    if len(idxs) > params.stats_sample_n:
        idxs = rng.sample(idxs, params.stats_sample_n)
        idxs.sort()

    sums = np.zeros(3, dtype=np.float64)
    sq_sums = np.zeros(3, dtype=np.float64)
    pixels = 0
    for i in idxs:
        arr = _to_float01(images[i])
        sums += arr.reshape(-1, 3).sum(axis=0)
        sq_sums += (arr.reshape(-1, 3) ** 2).sum(axis=0)
        pixels += arr.shape[0] * arr.shape[1]

    mean = (sums / pixels).tolist()
    var = sq_sums / pixels - np.asarray(mean) ** 2
    std = np.sqrt(np.maximum(var, 1e-12)).tolist()
    return {
        "mean": mean,
        "std": std,
        "n_images": len(idxs),
        "n_pixels": int(pixels),
        "random_seed": params.random_seed,
        "norm_mode": "dataset",
    }


def write_stats_json(stats: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(stats, indent=2), encoding="utf-8")


def apply_normalization(record: ImageRecord, params: NormalizationParams) -> ImageRecord:
    """Optionally apply mean/std; default leaves pixels unchanged (FastAI applies later)."""
    mean, std = resolve_mean_std(params)
    record.extras["norm_mean"] = mean
    record.extras["norm_std"] = std
    record.extras["norm_mode"] = params.norm_mode.lower()

    if not params.apply_on_disk or params.norm_mode.lower() == "none":
        return record

    arr = _to_float01(record.ensure_image())
    out = (arr - np.asarray(mean)) / np.asarray(std)
    record.extras["normalized_array"] = out.astype(np.float32)
    # Keep PIL image for pipeline continuity; float tensor lives in extras
    return record


def stats_are_valid(stats: dict) -> bool:
    mean = np.asarray(stats.get("mean", []), dtype=float)
    std = np.asarray(stats.get("std", []), dtype=float)
    if mean.shape != (3,) or std.shape != (3,):
        return False
    if not np.isfinite(mean).all() or not np.isfinite(std).all():
        return False
    return bool((std > 0).all())
