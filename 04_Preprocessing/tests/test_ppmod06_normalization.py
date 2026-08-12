"""Unit tests — PPMOD06 normalization."""

from __future__ import annotations

import numpy as np
from PIL import Image

from modules.normalization import (
    IMAGENET_MEAN,
    IMAGENET_STD,
    NormalizationParams,
    apply_normalization,
    compute_dataset_stats,
)
from modules.types import ImageRecord
from modules.validation import validate_normalization


def test_imagenet_apply_known_mean() -> None:
    # Constant image at ImageNet mean → normalized ≈ 0
    rgb = tuple(int(round(m * 255)) for m in IMAGENET_MEAN)
    im = Image.new("RGB", (16, 16), color=rgb)
    rec = ImageRecord(relative_path="a.png", image=im)
    out = apply_normalization(
        rec,
        NormalizationParams(norm_mode="imagenet", apply_on_disk=True),
    )
    arr = out.extras["normalized_array"]
    assert abs(float(arr.mean())) < 0.05
    validate_normalization(
        {"mean": list(IMAGENET_MEAN), "std": list(IMAGENET_STD)},
        "imagenet",
    )


def test_dataset_stats_deterministic() -> None:
    imgs = [
        Image.new("RGB", (8, 8), color=(i * 10, i * 10, i * 10)) for i in range(5)
    ]
    params = NormalizationParams(norm_mode="dataset", stats_sample_n=5, random_seed=42)
    a = compute_dataset_stats(imgs, params)
    b = compute_dataset_stats(imgs, params)
    assert a["mean"] == b["mean"] and a["std"] == b["std"]
    imgs2 = [
        Image.fromarray(
            np.random.default_rng(i).integers(0, 255, (8, 8, 3), dtype=np.uint8)
        )
        for i in range(10)
    ]
    stats = compute_dataset_stats(imgs2, params)
    validate_normalization(stats, "dataset")
    assert all(s > 0 for s in stats["std"])
