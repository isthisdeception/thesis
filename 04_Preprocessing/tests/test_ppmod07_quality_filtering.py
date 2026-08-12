"""Unit tests — PPMOD07 quality filtering."""

from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image

from modules.quality_filtering import QualityFilteringParams, filter_quality
from modules.types import ImageRecord
from modules.validation import validate_quality_exclusion


def _rec(tmp_path: Path, name: str, size: tuple[int, int] = (128, 128)) -> ImageRecord:
    p = tmp_path / name
    Image.new("RGB", size, color=(100, 100, 100)).save(p)
    return ImageRecord(
        relative_path=name,
        dataset_id="DS0002",
        image=Image.open(p),
        source_path=p,
        content_hash="abc",
    )


def test_exclude_list(tmp_path: Path) -> None:
    csv_path = tmp_path / "excl.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["Dataset ID", "Relative Path", "Issue Code"])
        w.writeheader()
        w.writerow(
            {"Dataset ID": "DS0002", "Relative Path": "bad.png", "Issue Code": "CORRUPT_IMAGE"}
        )
    rec = _rec(tmp_path, "bad.png")
    out = filter_quality(
        rec,
        QualityFilteringParams(exclude_list_path=csv_path),
    )
    assert not out.kept
    assert "CORRUPT" in out.reason_code or out.reason_code.startswith("EXCLUDED")
    validate_quality_exclusion(out)


def test_too_small(tmp_path: Path) -> None:
    rec = _rec(tmp_path, "tiny.png", size=(32, 32))
    out = filter_quality(rec, QualityFilteringParams(min_side=64))
    assert not out.kept and out.reason_code == "EXCLUDED_TOO_SMALL"
    validate_quality_exclusion(out)


def test_clean_kept(tmp_path: Path) -> None:
    rec = _rec(tmp_path, "good.png", size=(128, 128))
    out = filter_quality(rec, QualityFilteringParams())
    assert out.kept and out.reason_code == "OK"
