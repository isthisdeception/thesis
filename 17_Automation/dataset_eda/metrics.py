"""Pixel / file metric helpers for Phase D7 EDA (read-only)."""

from __future__ import annotations

import io
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO

import numpy as np

try:
    from PIL import Image

    HAS_PIL = True
except ImportError:  # pragma: no cover
    HAS_PIL = False


@dataclass
class PixelStats:
    width: int
    height: int
    mode: str
    format: str
    brightness: float  # mean luma in [0,1]
    contrast: float  # std of luma in [0,1]
    mean_r: float
    mean_g: float
    mean_b: float
    size_bytes: int


def _luma(arr: np.ndarray) -> np.ndarray:
    """arr HxWxC float in [0,1] -> luma HxW."""
    if arr.ndim == 2:
        return arr
    if arr.shape[2] >= 3:
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    return arr[:, :, 0]


def compute_pixel_stats(fp: BinaryIO, size_bytes: int = 0, max_side: int = 256) -> PixelStats:
    if not HAS_PIL:
        raise RuntimeError("Pillow is required for pixel EDA metrics")
    with Image.open(fp) as im:
        im.load()
        width, height = im.size
        mode = im.mode
        fmt = (im.format or Path(getattr(fp, "name", "")).suffix.lstrip(".") or "UNKNOWN").upper()
        # Downscale for speed; stats are approximate but stable for EDA
        thumb = im.copy()
        thumb.thumbnail((max_side, max_side))
        rgb = thumb.convert("RGB")
        arr = np.asarray(rgb, dtype=np.float32) / 255.0
        luma = _luma(arr)
        brightness = float(luma.mean())
        contrast = float(luma.std())
        mean_r = float(arr[:, :, 0].mean())
        mean_g = float(arr[:, :, 1].mean())
        mean_b = float(arr[:, :, 2].mean())
        return PixelStats(
            width=width,
            height=height,
            mode=mode,
            format=fmt,
            brightness=brightness,
            contrast=contrast,
            mean_r=mean_r,
            mean_g=mean_g,
            mean_b=mean_b,
            size_bytes=size_bytes,
        )


def stats_from_path(path: Path) -> PixelStats:
    size = path.stat().st_size
    with path.open("rb") as f:
        return compute_pixel_stats(f, size_bytes=size)


def stats_from_zip_member(zf: zipfile.ZipFile, member: str) -> PixelStats:
    info = zf.getinfo(member)
    with zf.open(member, "r") as raw:
        data = raw.read()
    bio = io.BytesIO(data)
    bio.name = member  # type: ignore[attr-defined]
    return compute_pixel_stats(bio, size_bytes=info.file_size)


def percentile(xs: list[float], q: float) -> float:
    if not xs:
        return float("nan")
    return float(np.percentile(np.asarray(xs, dtype=np.float64), q))


def mean_std(xs: list[float]) -> tuple[float, float]:
    if not xs:
        return float("nan"), float("nan")
    a = np.asarray(xs, dtype=np.float64)
    return float(a.mean()), float(a.std())
