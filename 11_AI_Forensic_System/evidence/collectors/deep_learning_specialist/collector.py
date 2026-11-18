"""MOD004 inference. The probability is evidence. This collector does not choose a decision."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Protocol

from evidence.item import SOURCE_MODULE, CollectorContext, CollectorOutcome, make_item

from .fastai_export import Inference, ModelLoadError, load_fastai_predictor
from .lookup import REPO, RegistryError, export_filename, lookup_model

EVIDENCE_TYPE = "deep_learning_prediction"
MODULE_ID = "MOD004"
DECISIONS = ("Real", "Fake", "Inconclusive", "Unknown")


class Predictor(Protocol):
    def predict(self, image) -> Inference: ...


class DeepLearningCollector:
    """One registered detector. Swap `model_id` or pass another predictor; the evidence type stays the same."""

    evidence_type = EVIDENCE_TYPE

    def __init__(
        self,
        model_id: str,
        *,
        repo: Path = REPO,
        predictor: Predictor | None = None,
        artifact_root: Path | None = None,
        timeout_seconds: float | None = None,
        device: str = "cpu",
    ) -> None:
        self.model_id = model_id
        self.repo = repo
        self.predictor = predictor
        self.artifact_root = artifact_root
        self.timeout_seconds = timeout_seconds
        self.device = device

    def collect(self, context: CollectorContext) -> CollectorOutcome:
        try:
            registered = lookup_model(self.repo, self.model_id)
        except RegistryError as exc:
            return CollectorOutcome.failed("model_unavailable", str(exc))
        if registered.status != "trained":
            return CollectorOutcome.failed("model_unavailable", f"{self.model_id} status is {registered.status or 'empty'}")
        try:
            predictor = self.predictor or self._load(registered.export_pointer, registered.positive_class or "fake")
        except ModelLoadError as exc:
            return CollectorOutcome.failed("model_unavailable", str(exc))
        started = time.perf_counter()
        try:
            inference = predictor.predict(context.image)
        except Exception as exc:
            return CollectorOutcome.failed("unexpected_error", f"inference failed: {exc.__class__.__name__}")
        elapsed = time.perf_counter() - started
        if self.timeout_seconds is not None and elapsed > self.timeout_seconds:
            return CollectorOutcome.failed("timeout", f"inference took {elapsed:.3f}s")
        probability = inference.fake_probability
        if not isinstance(probability, (int, float)) or not 0.0 <= float(probability) <= 1.0:
            return CollectorOutcome.failed("unexpected_error", "probability is outside 0-1")
        confidence = inference.model_confidence
        if confidence is not None and not 0.0 <= float(confidence) <= 1.0:
            return CollectorOutcome.failed("unexpected_error", "model confidence is outside 0-1")
        if confidence is not None and float(confidence) == float(probability):
            confidence = None
        raw = {
            "input_id": context.input_id,
            "case_id": context.case_id,
            "model_id": registered.model_id,
            "experiment_id": registered.experiment_id,
            "architecture": registered.architecture,
            "export_pointer": registered.export_pointer,
            "fake_probability": float(probability),
            "positive_class": registered.positive_class,
            "threshold": registered.threshold,
            "embedding": inference.embedding,
            "execution_time_seconds": elapsed,
            "device": self.device,
        }
        description = f"{registered.model_id} probability {float(probability):.4f}"
        if any(word in description for word in DECISIONS):
            return CollectorOutcome.failed("unexpected_error", "description would state a decision")
        item = make_item(
            evidence_type=self.evidence_type,
            description=description,
            raw_output=raw,
            value=float(probability),
            unit="probability",
            confidence=None if confidence is None else float(confidence),
            extra_processed={
                "model_id": registered.model_id,
                "threshold": registered.threshold,
                "execution_time_seconds": elapsed,
                "embedding": inference.embedding,
            },
            source_module=MODULE_ID,
        )
        if item.source_module == SOURCE_MODULE:
            return CollectorOutcome.failed("unexpected_error", "detector evidence was tagged as the acquisition layer")
        return CollectorOutcome.one(item)

    def _load(self, pointer: str, positive_class: str):
        if self.artifact_root is None:
            raise ModelLoadError(f"no local file for {pointer}")
        path = self.artifact_root / export_filename(pointer)
        if not path.is_file():
            raise ModelLoadError(f"export file is missing: {path.name}")
        return load_fastai_predictor(path, positive_class, self.device)
