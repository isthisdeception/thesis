"""PPMOD07 — Quality filtering + exclude lists."""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

from .types import ImageRecord, ModuleError

MODULE_ID = "PPMOD07"

REASON_OK = "OK"
REASON_CORRUPT = "EXCLUDED_CORRUPT"
REASON_DUPLICATE = "EXCLUDED_DUPLICATE"
REASON_TOO_SMALL = "EXCLUDED_TOO_SMALL"
REASON_TOO_LARGE = "EXCLUDED_TOO_LARGE"
REASON_TOO_FEW_BYTES = "EXCLUDED_TOO_FEW_BYTES"
REASON_TOO_MANY_BYTES = "EXCLUDED_TOO_MANY_BYTES"
REASON_BLUR = "EXCLUDED_BLUR"
REASON_BRIGHTNESS = "EXCLUDED_BRIGHTNESS"


@dataclass
class QualityFilteringParams:
    exclude_list_path: Path | None = None
    exclude_codes: list[str] = field(default_factory=lambda: ["CORRUPT_IMAGE"])
    dedupe_policy: str = "off"  # keep_first | exclude_all_dupes | off
    min_side: int = 64
    max_side: int = 4096
    min_file_bytes: int = 100
    max_file_bytes: int | None = None
    blur_var_threshold: float | None = None
    min_brightness: float | None = None
    max_brightness: float | None = None


def load_exclude_paths(
    path: Path | None,
    exclude_codes: list[str],
) -> dict[str, str]:
    """Load relative_path -> issue code from a STEP-022 style CSV."""
    if path is None:
        return {}
    path = Path(path)
    if not path.is_file():
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="MISSING_EXCLUDE_LIST",
            message=f"exclude_list_path not found: {path}",
        )
    codes = {c.upper() for c in exclude_codes}
    out: dict[str, str] = {}
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = (row.get("Issue Code") or row.get("issue_code") or "").strip().upper()
            if codes and code not in codes:
                continue
            rel = (
                row.get("Relative Path")
                or row.get("relative_path")
                or row.get("path")
                or ""
            ).strip().replace("\\", "/")
            if rel:
                out[rel] = code or "EXCLUDED"
                out[Path(rel).name] = out[rel]
    return out


def _brightness01(im: Image.Image) -> float:
    arr = np.asarray(im.convert("L"), dtype=np.float64) / 255.0
    return float(arr.mean())


def _blur_variance(im: Image.Image) -> float:
    # Laplacian-like via Pillow edge filter variance
    edges = im.convert("L").filter(ImageFilter.FIND_EDGES)
    arr = np.asarray(edges, dtype=np.float64)
    return float(arr.var())


def filter_quality(
    record: ImageRecord,
    params: QualityFilteringParams,
    *,
    exclude_map: dict[str, str] | None = None,
    seen_hashes: dict[str, str] | None = None,
) -> ImageRecord:
    """Decide keep/exclude. Mutates record.kept / reason_code; never silent."""
    rel = record.relative_path.replace("\\", "/")
    emap = exclude_map if exclude_map is not None else load_exclude_paths(
        params.exclude_list_path, params.exclude_codes
    )

    if rel in emap or Path(rel).name in emap:
        code = emap.get(rel) or emap.get(Path(rel).name, "CORRUPT_IMAGE")
        record.kept = False
        record.reason_code = REASON_CORRUPT if "CORRUPT" in code.upper() else f"EXCLUDED_{code}"
        record.extras["exclude_source_code"] = code
        return record

    # Dedupe
    if params.dedupe_policy != "off" and record.content_hash:
        seen = seen_hashes if seen_hashes is not None else {}
        if record.content_hash in seen:
            if params.dedupe_policy in {"keep_first", "exclude_all_dupes"}:
                record.kept = False
                record.reason_code = REASON_DUPLICATE
                record.extras["duplicate_of"] = seen[record.content_hash]
                return record
        else:
            if params.dedupe_policy == "keep_first":
                seen[record.content_hash] = rel
            elif params.dedupe_policy == "exclude_all_dupes":
                seen[record.content_hash] = rel

    size_bytes = None
    if record.source_path and Path(record.source_path).is_file():
        size_bytes = Path(record.source_path).stat().st_size
    elif "size_bytes" in record.extras:
        size_bytes = int(record.extras["size_bytes"])

    if size_bytes is not None:
        if size_bytes < params.min_file_bytes:
            record.kept = False
            record.reason_code = REASON_TOO_FEW_BYTES
            return record
        if params.max_file_bytes is not None and size_bytes > params.max_file_bytes:
            record.kept = False
            record.reason_code = REASON_TOO_MANY_BYTES
            return record

    im = record.ensure_image()
    w, h = im.width, im.height
    min_side = min(w, h)
    max_side = max(w, h)
    if min_side < params.min_side:
        record.kept = False
        record.reason_code = REASON_TOO_SMALL
        return record
    if max_side > params.max_side:
        record.kept = False
        record.reason_code = REASON_TOO_LARGE
        return record

    if params.blur_var_threshold is not None:
        bv = _blur_variance(im)
        record.extras["blur_var"] = bv
        if bv < params.blur_var_threshold:
            record.kept = False
            record.reason_code = REASON_BLUR
            return record

    if params.min_brightness is not None or params.max_brightness is not None:
        b = _brightness01(im)
        record.extras["brightness"] = b
        if params.min_brightness is not None and b < params.min_brightness:
            record.kept = False
            record.reason_code = REASON_BRIGHTNESS
            return record
        if params.max_brightness is not None and b > params.max_brightness:
            record.kept = False
            record.reason_code = REASON_BRIGHTNESS
            return record

    record.kept = True
    record.reason_code = REASON_OK
    return record
