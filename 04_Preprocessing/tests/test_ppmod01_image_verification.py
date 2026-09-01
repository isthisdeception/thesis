"""Unit tests — PPMOD01 image verification."""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from modules.image_verification import ImageVerificationParams, verify_path
from modules.validation import validate_image_verification


@pytest.fixture()
def tmp_img(tmp_path: Path) -> Path:
    p = tmp_path / "ok.png"
    Image.new("RGB", (32, 32), color=(10, 20, 30)).save(p)
    return p


def test_accept_valid_png(tmp_img: Path) -> None:
    rec = verify_path(tmp_img, "ok.png", ImageVerificationParams())
    assert rec.kept and rec.reason_code == "OK"
    assert rec.image is not None
    validate_image_verification(rec)


def test_reject_macos_junk(tmp_path: Path) -> None:
    p = tmp_path / "._foo.png"
    p.write_bytes(b"not-an-image")
    rec = verify_path(p, ".__MACOSX/._foo.png", ImageVerificationParams())
    assert not rec.kept and rec.reason_code == "MACOS_JUNK"
    validate_image_verification(rec)


def test_reject_macos_folder(tmp_path: Path) -> None:
    p = tmp_path / "x.png"
    Image.new("RGB", (8, 8)).save(p)
    rec = verify_path(p, "__MACOSX/x.png", ImageVerificationParams())
    assert not rec.kept and rec.reason_code == "MACOS_JUNK"


def test_reject_zero_byte(tmp_path: Path) -> None:
    p = tmp_path / "empty.png"
    p.write_bytes(b"")
    rec = verify_path(p, "empty.png", ImageVerificationParams())
    assert not rec.kept and rec.reason_code == "EMPTY_FILE"
    validate_image_verification(rec)


def test_reject_truncated_jpeg(tmp_path: Path) -> None:
    p = tmp_path / "bad.jpg"
    p.write_bytes(b"\xff\xd8\xff\xe0truncated")
    rec = verify_path(p, "bad.jpg", ImageVerificationParams())
    assert not rec.kept and rec.reason_code == "UNREADABLE"
    validate_image_verification(rec)


def test_reject_unsupported_ext(tmp_path: Path) -> None:
    p = tmp_path / "x.gif"
    p.write_bytes(b"GIF89a")
    rec = verify_path(p, "x.gif", ImageVerificationParams())
    assert not rec.kept and rec.reason_code == "UNSUPPORTED_FORMAT"
