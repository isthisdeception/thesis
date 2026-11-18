"""MOD003 collectors stay independent and do not decide the case."""

from __future__ import annotations

import ast
import json
from io import BytesIO
from pathlib import Path

from PIL import Image

from evidence.collectors import STEP053_TYPES, builtin_collectors
from evidence.item import CollectorContext, CollectorOutcome, make_item
from evidence.layer import run_collectors, run_registered
from image_validation import validate_stored_input
from input_management import receive_upload

DECISIONS = ("Real", "Fake", "Inconclusive", "Unknown")


class _Faces:
    def __init__(self, count: int) -> None:
        self.count = count

    def count_faces(self, image: Image.Image) -> int:
        return self.count


class _Boom:
    evidence_type = "boom"

    def collect(self, context: CollectorContext) -> CollectorOutcome:
        raise RuntimeError("boom")


class _Probe:
    evidence_type = "dummy_probe"

    def collect(self, context: CollectorContext) -> CollectorOutcome:
        item = make_item(
            evidence_type=self.evidence_type,
            description="probe observed the input id",
            raw_output={"input_id": context.input_id},
            value=context.input_id,
            unit="",
        )
        return CollectorOutcome.one(item)


def _png(size: int = 64) -> bytes:
    image = Image.new("RGB", (size, size))
    image.putdata([(x % 251, y % 251, (x + y) % 251) for y in range(size) for x in range(size)])
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def _passed(tmp_path: Path) -> Path:
    intake = receive_upload(case_id="CASE000001", filename="photo.png", data=_png(), storage_root=tmp_path)
    input_dir = tmp_path / "CASE000001" / intake.metadata["input_id"]
    assert validate_stored_input(input_dir, _Faces(1), storage_root=tmp_path).passed
    return input_dir


def test_collectors_do_not_import_each_other() -> None:
    root = Path(__file__).resolve().parents[1] / "evidence" / "collectors"
    for path in root.glob("*.py"):
        if path.name == "__init__.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            modules = []
            if isinstance(node, ast.ImportFrom) and node.module:
                modules.append(node.module)
            if isinstance(node, ast.Import):
                modules.extend(alias.name for alias in node.names)
            for name in modules:
                assert "collectors." not in name, f"{path.name} imports {name}"


def test_each_collector_emits_one_registry_item(tmp_path: Path) -> None:
    input_dir = _passed(tmp_path)
    result = run_registered(input_dir, tmp_path, _Faces(1))
    assert result.ran and result.failures == []
    kinds = [item.evidence_type for item in result.items]
    assert kinds == list(STEP053_TYPES)
    assert "deep_learning_prediction" not in kinds
    for item in result.items:
        assert item.evidence_id is None
        assert item.quality == "unevaluated" and item.status == "recorded"
        assert item.confidence is None
        assert item.dependencies == []
        text = json.dumps(item.to_json())
        for word in DECISIONS:
            assert word not in text
    saved = json.loads((input_dir / "evidence_items.json").read_text(encoding="utf-8"))
    assert [row["evidence_type"] for row in saved] == list(STEP053_TYPES)


def test_a_failing_collector_does_not_change_the_others(tmp_path: Path) -> None:
    input_dir = _passed(tmp_path)
    alone = run_registered(input_dir, tmp_path, _Faces(1), names=("image_statistics",))
    statistics = alone.items[0].to_json()
    mixed = run_collectors(input_dir, tmp_path, [builtin_collectors(_Faces(2))["image_statistics"], _Boom(), _Probe()])
    kinds = [item.evidence_type for item in mixed.items]
    assert kinds == ["image_statistics", "dummy_probe"]
    assert mixed.items[0].to_json()["raw_output"] == statistics["raw_output"]
    assert any(failure.name == "unexpected_error" and "boom" in failure.detail for failure in mixed.failures)


def test_an_unregistered_name_does_not_drop_registered_collectors(tmp_path: Path) -> None:
    input_dir = _passed(tmp_path)
    result = run_registered(
        input_dir,
        tmp_path,
        _Faces(0),
        names=("image_statistics", "not_a_collector", "dummy_probe"),
        extras={"dummy_probe": _Probe()},
    )
    assert [item.evidence_type for item in result.items] == ["image_statistics", "dummy_probe"]
    assert any("not_a_collector is not registered" in failure.detail for failure in result.failures)
    face = next(item for item in run_registered(input_dir, tmp_path, _Faces(0)).items if item.evidence_type == "face_detection")
    quality = next(item for item in run_registered(input_dir, tmp_path, _Faces(0)).items if item.evidence_type == "face_quality")
    assert face.raw_output["face_count"] == 0
    assert quality.raw_output["used_face_box"] is False


def test_failed_validation_runs_no_collector(tmp_path: Path) -> None:
    intake = receive_upload(case_id="CASE000001", filename="photo.png", data=_png(), storage_root=tmp_path)
    input_dir = tmp_path / "CASE000001" / intake.metadata["input_id"]
    assert validate_stored_input(input_dir, _Faces(0), storage_root=tmp_path).passed is False
    result = run_registered(input_dir, tmp_path, _Faces(1))
    assert result.ran is False and result.items == []
    assert "did not pass" in result.failures[0].detail
    assert not (input_dir / "evidence_items.json").exists()
