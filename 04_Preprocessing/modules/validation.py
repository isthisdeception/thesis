"""Validation helpers PPMOD01V–PPMOD10V (property checks, not full pipeline runs)."""

from __future__ import annotations

from . import artifact_removal as m08
from . import face_alignment as m03
from . import face_detection as m02
from . import format_conversion as m09
from . import image_verification as m01
from . import metadata_extraction as m10
from . import normalization as m06
from .types import ImageRecord, ModuleError


def validate_image_verification(record: ImageRecord) -> None:
    """PPMOD01V — failure rows must carry a non-empty known reason code."""
    if record.kept:
        if record.reason_code != m01.REASON_OK:
            raise ModuleError("PPMOD01V", "INVALID_OK", "kept record must have reason OK")
        return
    if not record.reason_code:
        raise ModuleError("PPMOD01V", "EMPTY_REASON", "failed verification missing reason")
    if record.reason_code not in m01.REASON_CODES:
        raise ModuleError(
            "PPMOD01V",
            "UNKNOWN_REASON",
            f"reason_code {record.reason_code!r} not in enum",
        )


def validate_face_detection(record: ImageRecord, width: int, height: int) -> None:
    """PPMOD02V — boxes in bounds; scores in [0,1]."""
    if record.face_sentinel == m02.FULL_FRAME:
        return
    for box in record.face_boxes:
        if not m02.box_within_bounds(box, width, height):
            raise ModuleError(
                "PPMOD02V",
                "BOX_OOB",
                f"box out of bounds or bad score: {box.as_tuple()}",
                path=record.relative_path,
            )


def validate_face_alignment(record: ImageRecord, enabled: bool, template: int) -> None:
    """PPMOD03V — matrix finite; size matches template when enabled."""
    if not m03.matrix_is_finite(record.affine_matrix):
        raise ModuleError("PPMOD03V", "BAD_MATRIX", "affine matrix missing/non-finite")
    if enabled:
        im = record.ensure_image()
        if im.width != template or im.height != template:
            raise ModuleError(
                "PPMOD03V",
                "SIZE_MISMATCH",
                f"expected {template}x{template}, got {im.width}x{im.height}",
            )


def validate_cropping(record: ImageRecord, enabled: bool) -> None:
    """PPMOD04V — positive dims; crop box inside original when present."""
    im = record.ensure_image()
    if im.width <= 0 or im.height <= 0:
        raise ModuleError("PPMOD04V", "EMPTY_CROP", "crop produced empty image")
    if enabled and record.crop_box and record.original_size:
        x1, y1, x2, y2 = record.crop_box
        ow, oh = record.original_size
        if not (0 <= x1 < x2 <= ow and 0 <= y1 < y2 <= oh):
            raise ModuleError("PPMOD04V", "CROP_OOB", f"crop_box {record.crop_box} oob")


def validate_resize(record: ImageRecord, target_h: int, target_w: int) -> None:
    """PPMOD05V — exact output size."""
    im = record.ensure_image()
    if im.height != target_h or im.width != target_w:
        raise ModuleError(
            "PPMOD05V",
            "SIZE_MISMATCH",
            f"expected {target_h}x{target_w}, got {im.height}x{im.width}",
        )


def validate_normalization(stats: dict, mode: str) -> None:
    """PPMOD06V — finite stats; std > 0; mode recognized."""
    if mode.lower() not in {"imagenet", "dataset", "none"}:
        raise ModuleError("PPMOD06V", "BAD_MODE", f"invalid norm_mode={mode!r}")
    if mode.lower() != "none" and not m06.stats_are_valid(
        stats
        if "mean" in stats
        else {"mean": stats.get("mean", m06.IMAGENET_MEAN), "std": stats.get("std", m06.IMAGENET_STD)}
    ):
        # For imagenet mode without dataset stats dict, synthesize check
        check = {
            "mean": list(m06.IMAGENET_MEAN),
            "std": list(m06.IMAGENET_STD),
        }
        if mode.lower() == "imagenet":
            if not m06.stats_are_valid(check):
                raise ModuleError("PPMOD06V", "BAD_STATS", "imagenet stats invalid")
        elif not m06.stats_are_valid(stats):
            raise ModuleError("PPMOD06V", "BAD_STATS", "stats not finite / std<=0")


def validate_quality_exclusion(record: ImageRecord) -> None:
    """PPMOD07V — every exclusion has non-empty reason."""
    if not record.kept and not record.reason_code:
        raise ModuleError("PPMOD07V", "EMPTY_REASON", "exclusion missing reason code")


def validate_artifact_removal(params_forbid: bool) -> None:
    """PPMOD08V — production profiles cannot disable forbid flag."""
    if not params_forbid:
        raise ModuleError(
            "PPMOD08V",
            "FORBIDDEN_CONFIG",
            "forbid_generative_denoising cannot be false",
        )


def validate_format_conversion(record: ImageRecord) -> None:
    """PPMOD09V — RGB mode; format recorded."""
    im = record.ensure_image()
    if im.mode != "RGB":
        raise ModuleError("PPMOD09V", "NOT_RGB", f"mode={im.mode}")
    if not record.output_format:
        raise ModuleError("PPMOD09V", "NO_FORMAT", "output_format missing")


def validate_metadata_row(row: dict) -> None:
    """PPMOD10V — canonical schema columns present."""
    missing = [c for c in m10.CANONICAL_FIELDS if c not in row]
    if missing:
        raise ModuleError("PPMOD10V", "SCHEMA", f"missing columns: {missing}")
