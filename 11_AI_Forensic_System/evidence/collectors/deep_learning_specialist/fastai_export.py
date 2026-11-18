"""Load a FastAI export when a local file is present. Import of FastAI stays inside the function."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


class ModelLoadError(RuntimeError):
    """The export could not be loaded. The caller records model_unavailable and no probability."""


@dataclass(frozen=True)
class Inference:
    fake_probability: float
    embedding: list[float] | None = None
    model_confidence: float | None = None


class FastAIPredictor:
    def __init__(self, learn, positive_class: str) -> None:
        self._learn = learn
        vocab = [str(label) for label in learn.dls.vocab]
        if positive_class not in vocab:
            raise ModelLoadError(f"vocab has no {positive_class!r}")
        self._index = vocab.index(positive_class)

    def predict(self, image: Image.Image) -> Inference:
        _decision, _index, probs = self._learn.predict(image)
        return Inference(fake_probability=float(probs[self._index]))


def load_fastai_predictor(export_path: Path, positive_class: str, device: str = "cpu") -> FastAIPredictor:
    try:
        from fastai.learner import load_learner
    except ImportError as exc:
        raise ModelLoadError("fastai is not installed") from exc
    try:
        learn = load_learner(export_path, cpu=device == "cpu")
    except Exception as exc:
        raise ModelLoadError(exc.__class__.__name__) from exc
    return FastAIPredictor(learn, positive_class)
