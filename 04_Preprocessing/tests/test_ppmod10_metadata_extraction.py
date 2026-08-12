"""Unit tests — PPMOD10 metadata extraction."""

from __future__ import annotations

import pytest

from modules.metadata_extraction import (
    MetadataExtractionParams,
    extract_metadata,
    to_index_row,
)
from modules.types import ImageRecord, ModuleError
from modules.validation import validate_metadata_row


def test_ds0003_folder_labels() -> None:
    rec = ImageRecord(
        relative_path="train/fake/stylegan/img001.png",
        dataset_id="DS0003",
    )
    out = extract_metadata(
        rec,
        MetadataExtractionParams(require_class_label=True, require_identity=False),
    )
    assert out.class_label == "fake"
    row = to_index_row(out)
    validate_metadata_row(row)


def test_ds0002_requires_identity() -> None:
    rec = ImageRecord(
        relative_path="CoDiff/FE/no_id_here/img.png",
        dataset_id="DS0002",
    )
    with pytest.raises(ModuleError) as ei:
        extract_metadata(
            rec,
            MetadataExtractionParams(
                require_class_label=True,
                require_identity=True,
                source_container="CoDiff.zip",
            ),
        )
    assert ei.value.reason_code == "MISSING_IDENTITY"


def test_ds0002_with_identity() -> None:
    rec = ImageRecord(
        relative_path="DCFace/id_012/img_01.png",
        dataset_id="DS0002",
    )
    out = extract_metadata(
        rec,
        MetadataExtractionParams(
            require_class_label=True,
            require_identity=True,
            source_container="DCFace.zip",
        ),
    )
    assert out.identity and "id" in out.identity.lower()
    validate_metadata_row(to_index_row(out))


def test_ds0001_path_heuristic() -> None:
    rec = ImageRecord(relative_path="real/celebahq_img42.png", dataset_id="DS0001")
    out = extract_metadata(rec, MetadataExtractionParams(require_class_label=True))
    assert out.class_label == "real"
