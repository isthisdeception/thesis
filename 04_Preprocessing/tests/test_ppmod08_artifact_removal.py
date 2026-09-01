"""Unit tests — PPMOD08 artifact removal."""

from __future__ import annotations

from io import BytesIO

import numpy as np
import pytest
from PIL import Image

from modules.artifact_removal import ArtifactRemovalParams, strip_artifacts
from modules.types import ImageRecord, ModuleError
from modules.validation import validate_artifact_removal


def _jpeg_with_exif() -> Image.Image:
    im = Image.new("RGB", (32, 32), color=(12, 34, 56))
    # Pillow may not round-trip arbitrary EXIF easily; stamp via info then reload
    buf = BytesIO()
    im.save(buf, format="JPEG", quality=95)
    buf.seek(0)
    return Image.open(buf)


def test_strip_exif_pixels_stable() -> None:
    im = _jpeg_with_exif()
    before = np.asarray(im.convert("RGB"), dtype=np.float64)
    rec = ImageRecord(relative_path="a.jpg", image=im)
    out = strip_artifacts(rec, ArtifactRemovalParams(strip_exif=True))
    assert out.exif_stripped
    after = np.asarray(out.ensure_image().convert("RGB"), dtype=np.float64)
    # PNG re-encode of JPEG may differ slightly; allow small MSE
    mse = float(((before - after) ** 2).mean())
    assert mse < 25.0
    validate_artifact_removal(True)


def test_forbidden_denoise_raises() -> None:
    rec = ImageRecord(relative_path="a.png", image=Image.new("RGB", (8, 8)))
    with pytest.raises(ModuleError) as ei:
        strip_artifacts(
            rec,
            ArtifactRemovalParams(),
            requested_ops={"denoise": True},
        )
    assert ei.value.reason_code == "FORBIDDEN_OP"


def test_forbid_flag_cannot_be_false() -> None:
    rec = ImageRecord(relative_path="a.png", image=Image.new("RGB", (8, 8)))
    with pytest.raises(ModuleError):
        strip_artifacts(rec, ArtifactRemovalParams(forbid_generative_denoising=False))
    with pytest.raises(ModuleError):
        validate_artifact_removal(False)
