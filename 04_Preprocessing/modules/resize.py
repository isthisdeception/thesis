"""PPMOD05 — Resize / letterbox."""

from __future__ import annotations

from dataclasses import dataclass

from PIL import Image

from .types import ImageRecord, ModuleError

MODULE_ID = "PPMOD05"

_INTERP = {
    "nearest": Image.Resampling.NEAREST,
    "bilinear": Image.Resampling.BILINEAR,
    "bicubic": Image.Resampling.BICUBIC,
    "lanczos": Image.Resampling.LANCZOS,
}


@dataclass
class ResizeParams:
    target_size: int | tuple[int, int] = 224
    interpolation: str = "bilinear"
    keep_aspect: bool = False
    pad_value: int = 0


def _target_hw(target_size: int | tuple[int, int]) -> tuple[int, int]:
    if isinstance(target_size, int):
        return target_size, target_size
    if len(target_size) != 2:
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="INVALID_PARAM",
            message=f"target_size must be int or [h,w], got {target_size!r}",
        )
    return int(target_size[0]), int(target_size[1])


def resize_image(record: ImageRecord, params: ResizeParams) -> ImageRecord:
    """Resize to exact target HxW (stretch or letterbox)."""
    im = record.ensure_image()
    th, tw = _target_hw(params.target_size)
    if th <= 0 or tw <= 0:
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="INVALID_PARAM",
            message=f"non-positive target_size={params.target_size!r}",
            path=record.relative_path,
        )

    interp = _INTERP.get(params.interpolation.lower())
    if interp is None:
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="INVALID_PARAM",
            message=f"unknown interpolation={params.interpolation!r}",
            path=record.relative_path,
        )

    record.original_size = record.original_size or (im.width, im.height)

    if not params.keep_aspect:
        out = im.resize((tw, th), interp)
    else:
        scale = min(tw / im.width, th / im.height)
        nw = max(1, int(round(im.width * scale)))
        nh = max(1, int(round(im.height * scale)))
        resized = im.resize((nw, nh), interp)
        mode = im.mode
        if mode == "RGB":
            fill: int | tuple[int, ...] = (params.pad_value,) * 3
        elif mode == "RGBA":
            fill = (params.pad_value,) * 4
        elif mode == "L":
            fill = params.pad_value
        else:
            fill = params.pad_value
        canvas = Image.new(mode, (tw, th), fill)
        left = (tw - nw) // 2
        top = (th - nh) // 2
        canvas.paste(resized, (left, top))
        out = canvas
        record.extras["letterbox_offset"] = (left, top)
        record.extras["letterbox_inner"] = (nw, nh)

    record.image = out
    record.current_size = (out.width, out.height)
    return record
