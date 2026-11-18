"""MOD001 and MOD002: accepted files, and structured failures that do not continue."""

from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path

from PIL import Image

from image_validation import ValidationConfig, validate_stored_input
from input_management import IntakeConfig, receive_upload


class _Faces:
    def __init__(self, count: int) -> None:
        self.count = count

    def count_faces(self, image: Image.Image) -> int:
        return self.count


def _png(size: int = 64) -> bytes:
    image = Image.new("RGB", (size, size))
    pixels = [(x % 251, y % 251, (x + y) % 251) for y in range(size) for x in range(size)]
    image.putdata(pixels)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def _accept(tmp_path: Path, data: bytes, filename: str = "photo.png", **kwargs):
    return receive_upload(case_id="CASE000001", filename=filename, data=data, storage_root=tmp_path, **kwargs)


def test_accepted_upload_writes_metadata_and_keeps_the_next_file(tmp_path: Path) -> None:
    original = _png()
    first = _accept(tmp_path, original)
    second = _accept(tmp_path, _png(48), filename="other.png")
    assert first.accepted and first.metadata["input_id"] == "CASE000001-input-01"
    assert second.metadata["input_id"] == "CASE000001-input-02"
    assert Path(first.metadata["stored_path"]).read_bytes() == original
    saved = json.loads((tmp_path / "CASE000001" / first.metadata["input_id"] / "input_metadata.json").read_text(encoding="utf-8"))
    assert saved["status"] == "accepted" and saved["failure_id"] is None


def test_empty_oversized_and_unsupported_do_not_store_an_image(tmp_path: Path) -> None:
    empty = _accept(tmp_path, b"")
    oversized = _accept(tmp_path, _png(), filename="big.png", config=IntakeConfig(max_bytes=10))
    text = _accept(tmp_path, b"hello", filename="notes.txt")
    assert empty.failure is not None and empty.failure.name == "unexpected_error" and not empty.image_stored
    assert oversized.failure is not None and "byte_size=" in oversized.failure.detail and not oversized.image_stored
    assert text.failure is not None and text.failure.name == "unsupported_format"
    assert list((tmp_path / "CASE000001").glob("*/original.*")) == []
    assert empty.metadata["status"] == "rejected"


def test_valid_image_passes_and_does_not_decide(tmp_path: Path) -> None:
    intake = _accept(tmp_path, _png())
    result = validate_stored_input(tmp_path / "CASE000001" / intake.metadata["input_id"], _Faces(1), storage_root=tmp_path)
    assert result.passed
    assert result.record["face_availability"] == "single"
    assert result.record["compression"] == "png"
    assert "Fake" not in json.dumps(result.record) and "Real" not in json.dumps(result.record)


def test_corrupted_and_mislabeled_files_fail(tmp_path: Path) -> None:
    broken = _accept(tmp_path, b"\xff\xd8\xffnot-an-image", filename="photo.jpg")
    png_as_jpg = _accept(tmp_path, _png(), filename="photo.jpg")
    broken_result = validate_stored_input(tmp_path / "CASE000001" / broken.metadata["input_id"], _Faces(1), storage_root=tmp_path)
    labeled_result = validate_stored_input(tmp_path / "CASE000001" / png_as_jpg.metadata["input_id"], _Faces(1), storage_root=tmp_path)
    assert broken_result.failure is not None and broken_result.failure.name == "corrupted_image"
    assert labeled_result.failure is not None and labeled_result.failure.name == "unsupported_format"
    assert broken_result.record["status"] == "failed"


def test_no_face_multiple_faces_and_tiny_image(tmp_path: Path) -> None:
    alone = _accept(tmp_path, _png())
    many = _accept(tmp_path, _png())
    tiny = _accept(tmp_path, _png(8), config=IntakeConfig(min_edge=32))
    none = validate_stored_input(tmp_path / "CASE000001" / alone.metadata["input_id"], _Faces(0), storage_root=tmp_path)
    extra = validate_stored_input(tmp_path / "CASE000001" / many.metadata["input_id"], _Faces(2), storage_root=tmp_path)
    small = validate_stored_input(tmp_path / "CASE000001" / tiny.metadata["input_id"], _Faces(1), storage_root=tmp_path)
    assert none.failure is not None and none.failure.name == "no_face"
    assert extra.failure is not None and extra.failure.name == "multiple_faces"
    assert small.failure is not None and "resolution" in small.failure.detail
    assert none.record["status"] == "failed"


def test_rejected_intake_is_not_validated_as_an_image(tmp_path: Path) -> None:
    rejected = _accept(tmp_path, b"", filename="empty.png")
    result = validate_stored_input(tmp_path / "CASE000001" / rejected.metadata["input_id"], _Faces(1), storage_root=tmp_path)
    assert result.passed is False
    assert result.failure is not None and "did not read an image" in result.failure.detail


def test_noise_limit_rejects_a_varying_image(tmp_path: Path) -> None:
    intake = _accept(tmp_path, _png())
    result = validate_stored_input(
        tmp_path / "CASE000001" / intake.metadata["input_id"],
        _Faces(1),
        storage_root=tmp_path,
        config=ValidationConfig(max_noise_stddev=0.1),
    )
    assert result.failure is not None and result.record["noise_stddev"] > 0.1
