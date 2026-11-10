"""Phase E7 image perturbations. Each takes an RGB PIL image, a level, and a seeded generator.

JPEG encoding and resizing reuse the preprocessing modules (PPMOD09, PPMOD05).
"""

from __future__ import annotations

import hashlib
import sys
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

_PREPROCESSING = Path(__file__).resolve().parents[2] / "04_Preprocessing"


def _preprocessing():
    if str(_PREPROCESSING) not in sys.path:
        sys.path.insert(0, str(_PREPROCESSING))
    from modules.format_conversion import FormatConversionParams, encode_bytes
    from modules.resize import ResizeParams, resize_image
    from modules.types import ImageRecord

    return FormatConversionParams, encode_bytes, ResizeParams, resize_image, ImageRecord


def image_seed(seed: int, condition: str, image_id: str) -> int:
    digest = hashlib.sha256(f"{seed}|{condition}|{image_id}".encode()).digest()
    return int.from_bytes(digest[:8], "little")


def _jpeg(img: Image.Image, quality: int) -> Image.Image:
    Params, encode, _, _, Record = _preprocessing()
    data = encode(Record(relative_path="robustness", image=img), Params(output_format="JPEG", jpeg_quality=int(quality)))
    return Image.open(BytesIO(data)).convert("RGB")


def _scale(img: Image.Image, factor: float) -> Image.Image:
    _, _, Params, resize, Record = _preprocessing()
    h = max(1, round(img.height * factor))
    w = max(1, round(img.width * factor))
    return resize(Record(relative_path="robustness", image=img), Params(target_size=(h, w), interpolation="bilinear")).image


def jpeg(img, level, rng):
    return _jpeg(img, level)


def gaussian_noise(img, level, rng):
    x = np.asarray(img, dtype=np.float32) / 255.0
    x = np.clip(x + rng.normal(0.0, float(level), x.shape).astype(np.float32), 0.0, 1.0)
    return Image.fromarray(np.round(x * 255.0).astype(np.uint8), "RGB")


def gaussian_blur(img, level, rng):
    return img.filter(ImageFilter.GaussianBlur(radius=float(level)))


def brightness(img, level, rng):
    return ImageEnhance.Brightness(img).enhance(float(level))


def contrast(img, level, rng):
    return ImageEnhance.Contrast(img).enhance(float(level))


def saturation(img, level, rng):
    return ImageEnhance.Color(img).enhance(float(level))


def resolution(img, level, rng):
    return _scale(img, float(level))


def scaling(img, level, rng):
    return _scale(img, float(level))


def crop(img, level, rng):
    w, h = img.size
    cw, ch = max(1, round(w * float(level))), max(1, round(h * float(level)))
    left, top = (w - cw) // 2, (h - ch) // 2
    return img.crop((left, top, left + cw, top + ch))


def rotation(img, level, rng):
    return img.rotate(float(level), resample=Image.Resampling.BILINEAR, fillcolor=(0, 0, 0))


def occlusion(img, level, rng):
    w, h = img.size
    side = max(1, round(np.sqrt(float(level)) * min(w, h)))
    left = int(rng.integers(0, w - side + 1))
    top = int(rng.integers(0, h - side + 1))
    out = img.copy()
    out.paste((128, 128, 128), (left, top, left + side, top + side))
    return out


def low_quality(img, level, rng):
    factor, quality = level
    return _jpeg(_scale(img, float(factor)), int(quality))


KINDS = {
    "jpeg": jpeg,
    "gaussian_noise": gaussian_noise,
    "gaussian_blur": gaussian_blur,
    "brightness": brightness,
    "contrast": contrast,
    "saturation": saturation,
    "resolution": resolution,
    "scaling": scaling,
    "crop": crop,
    "rotation": rotation,
    "occlusion": occlusion,
    "low_quality": low_quality,
}


def check_level(kind: str, level) -> None:
    def number(x) -> float:
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise ValueError(f"{kind} level must be a number, got {x!r}")
        return float(x)

    if kind == "low_quality":
        if not isinstance(level, (list, tuple)) or len(level) != 2:
            raise ValueError(f"low_quality level must be [factor, quality], got {level!r}")
        check_level("resolution", level[0])
        check_level("jpeg", level[1])
        return
    v = number(level)
    ok = {
        "jpeg": 1 <= v <= 100 and float(level).is_integer(),
        "gaussian_noise": v > 0,
        "gaussian_blur": v > 0,
        "brightness": v >= 0,
        "contrast": v >= 0,
        "saturation": v >= 0,
        "resolution": 0 < v < 1,
        "scaling": v > 1,
        "crop": 0 < v < 1,
        "rotation": -360 < v < 360,
        "occlusion": 0 < v < 1,
    }[kind]
    if not ok:
        raise ValueError(f"{kind} level out of range: {level!r}")


def apply(kind: str, img: Image.Image, level, seed: int) -> Image.Image:
    if kind == "clean":
        return img
    out = KINDS[kind](img.convert("RGB"), level, np.random.default_rng(seed))
    return out.convert("RGB")
