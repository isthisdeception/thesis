"""PPMOD08 — Artifact removal (junk / EXIF only — never denoise)."""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

from PIL import Image

from .types import ImageRecord, ModuleError

MODULE_ID = "PPMOD08"


@dataclass
class ArtifactRemovalParams:
    strip_exif: bool = True
    drop_alpha: bool = True
    remove_sidecar_files: bool = True
    forbid_generative_denoising: bool = True


FORBIDDEN_OPS = frozenset(
    {
        "denoise",
        "smooth",
        "sharpen",
        "jpeg_recompress_cleanup",
        "gan_artifact_clean",
    }
)


def _assert_no_forbidden(params: ArtifactRemovalParams, extras_flags: dict | None) -> None:
    if not params.forbid_generative_denoising:
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="FORBIDDEN_CONFIG",
            message="forbid_generative_denoising must remain true (forensic signal)",
        )
    if extras_flags:
        bad = FORBIDDEN_OPS.intersection(k for k, v in extras_flags.items() if v)
        if bad:
            raise ModuleError(
                module_id=MODULE_ID,
                reason_code="FORBIDDEN_OP",
                message=f"generative cleanup ops not allowed: {sorted(bad)}",
            )


def strip_artifacts(
    record: ImageRecord,
    params: ArtifactRemovalParams,
    *,
    requested_ops: dict | None = None,
) -> ImageRecord:
    """Strip EXIF / prepare for clean save. Pixels unchanged aside from mode drop."""
    _assert_no_forbidden(params, requested_ops)

    im = record.ensure_image()
    if params.drop_alpha and im.mode in {"RGBA", "LA", "PA"}:
        # Alpha drop is hygiene; full RGB force is PPMOD09 — here convert via composite
        background = Image.new("RGB", im.size, (0, 0, 0))
        rgba = im.convert("RGBA")
        background.paste(rgba, mask=rgba.split()[-1])
        im = background
        record.source_mode = record.source_mode or "RGBA"

    if params.strip_exif:
        # Rebuild image without EXIF by saving to memory without exif= kw
        buf = BytesIO()
        save_im = im.convert("RGB") if im.mode not in {"RGB", "L"} else im
        fmt = "PNG"
        save_im.save(buf, format=fmt)
        buf.seek(0)
        clean = Image.open(buf)
        clean.load()
        record.image = clean.copy()
        record.exif_stripped = True
    else:
        record.image = im

    record.extras["remove_sidecar_files"] = params.remove_sidecar_files
    record.sync_size_from_image()
    return record


def is_sidecar_filename(name: str) -> bool:
    lower = name.lower()
    return lower.endswith((".txt", ".json", ".xml", ".csv", ".html"))
