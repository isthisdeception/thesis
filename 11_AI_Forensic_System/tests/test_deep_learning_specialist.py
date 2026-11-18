"""MOD004 returns a probability from the registry row and never a decision."""

from __future__ import annotations

import ast
import json
import time
from io import BytesIO
from pathlib import Path

from PIL import Image

from evidence.collectors.deep_learning_specialist import DeepLearningCollector, Inference
from evidence.item import CollectorContext
from evidence.layer import run_collectors
from image_validation import validate_stored_input
from input_management import receive_upload

REPO = Path(__file__).resolve().parents[2]
DECISIONS = ("Real", "Fake", "Inconclusive", "Unknown")


class _Fixed:
    def __init__(self, probability: float, confidence: float | None = None, embedding: list[float] | None = None, delay: float = 0.0) -> None:
        self.probability = probability
        self.confidence = confidence
        self.embedding = embedding
        self.delay = delay

    def predict(self, image: Image.Image) -> Inference:
        if self.delay:
            time.sleep(self.delay)
        return Inference(fake_probability=self.probability, embedding=self.embedding, model_confidence=self.confidence)


class _Faces:
    def count_faces(self, image: Image.Image) -> int:
        return 1


def _context(image: Image.Image) -> CollectorContext:
    return CollectorContext("CASE000001", "CASE000001-input-01", image, Path("original.png"), "passed")


def _image() -> Image.Image:
    return Image.new("RGB", (32, 32), color=(20, 40, 60))


def test_package_does_not_hardcode_an_export_path() -> None:
    root = Path(__file__).resolve().parents[1] / "evidence" / "collectors" / "deep_learning_specialist"
    text = "\n".join(path.read_text(encoding="utf-8") for path in root.glob("*.py"))
    assert "thesis-experiment-artifacts" not in text
    assert "MODEL0001_export.pkl" not in text
    tree = ast.parse((root / "collector.py").read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        modules = []
        if isinstance(node, ast.ImportFrom) and node.module:
            modules.append(node.module)
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        for name in modules:
            assert "collectors.face" not in name and "image_statistics" not in name


def test_swapping_the_registry_row_swaps_the_probability() -> None:
    image = _image()
    first = DeepLearningCollector("MODEL0001", repo=REPO, predictor=_Fixed(0.2)).collect(_context(image))
    second = DeepLearningCollector("MODEL0008", repo=REPO, predictor=_Fixed(0.7, embedding=[0.1, 0.2])).collect(_context(image))
    assert first.failure_name is None and second.failure_name is None
    one, two = first.items[0], second.items[0]
    assert one.raw_output["model_id"] == "MODEL0001"
    assert two.raw_output["model_id"] == "MODEL0008"
    assert one.raw_output["export_pointer"] != two.raw_output["export_pointer"]
    assert one.processed_output["value"] == 0.2 and two.processed_output["value"] == 0.7
    recorded = json.loads((REPO / "06_Experiments/EXP0001/metrics/threshold.json").read_text(encoding="utf-8"))
    assert one.processed_output["threshold"] == recorded["value"]
    assert one.confidence is None
    assert two.raw_output["embedding"] == [0.1, 0.2]
    assert one.raw_output["execution_time_seconds"] >= 0
    assert one.source_module == "MOD004"
    for item in (one, two):
        blob = item.description + str(item.processed_output)
        for word in DECISIONS:
            assert word not in blob


def test_model_confidence_is_not_the_probability() -> None:
    outcome = DeepLearningCollector("MODEL0001", repo=REPO, predictor=_Fixed(0.2, confidence=0.4)).collect(_context(_image()))
    item = outcome.items[0]
    assert item.confidence == 0.4
    assert item.processed_output["value"] == 0.2


def test_missing_model_and_missing_file_produce_no_probability(tmp_path: Path) -> None:
    missing = DeepLearningCollector("MODEL9999", repo=REPO).collect(_context(_image()))
    absent = DeepLearningCollector("MODEL0001", repo=REPO, artifact_root=tmp_path).collect(_context(_image()))
    assert missing.failure_name == "model_unavailable" and missing.items == ()
    assert absent.failure_name == "model_unavailable" and "missing" in (absent.failure_detail or "")
    assert absent.items == ()


def test_timeout_and_bad_probability_drop_the_item() -> None:
    slow = DeepLearningCollector("MODEL0001", repo=REPO, predictor=_Fixed(0.2, delay=0.05), timeout_seconds=0.01)
    illegal = DeepLearningCollector("MODEL0001", repo=REPO, predictor=_Fixed(1.5))
    assert slow.collect(_context(_image())).failure_name == "timeout"
    assert illegal.collect(_context(_image())).failure_name == "unexpected_error"


def test_specialist_runs_beside_another_collector(tmp_path: Path) -> None:
    image = Image.new("RGB", (64, 64))
    image.putdata([(x % 251, y % 251, (x + y) % 251) for y in range(64) for x in range(64)])
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    intake = receive_upload(case_id="CASE000001", filename="photo.png", data=buffer.getvalue(), storage_root=tmp_path)
    input_dir = tmp_path / "CASE000001" / intake.metadata["input_id"]
    assert validate_stored_input(input_dir, _Faces(), storage_root=tmp_path).passed
    from evidence.collectors.image_statistics import ImageStatisticsCollector

    result = run_collectors(input_dir, tmp_path, [
        ImageStatisticsCollector(),
        DeepLearningCollector("MODEL0001", repo=REPO, predictor=_Fixed(0.25)),
    ])
    kinds = [item.evidence_type for item in result.items]
    assert kinds == ["image_statistics", "deep_learning_prediction"]
    assert result.failures == []
