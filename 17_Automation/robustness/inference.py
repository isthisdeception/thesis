"""Perturbed inference for Phase E7. Runs on Kaggle with the MODEL0001 export and the processed images mounted.

Model input matches training: RGB image -> squish resize to image_size -> /255 -> ImageNet normalisation.
The clean condition runs first and must reproduce predictions.csv before any perturbed result is kept.
"""

from __future__ import annotations

import hashlib
import json
import platform
import time
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd
from PIL import Image

from .config import CLEAN, Condition, RobustnessConfig
from .perturbations import apply, image_seed

PROBS_NAME = "robustness_probs.csv"
MANIFEST_NAME = "run_manifest.json"
_INTERP = {"bilinear": Image.Resampling.BILINEAR, "bicubic": Image.Resampling.BICUBIC, "nearest": Image.Resampling.NEAREST}


class CleanCheckError(RuntimeError):
    """Clean inference does not reproduce the saved predictions; perturbed results would not be comparable."""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def find_export(search_roots: list[Path], name: str, sha256: str) -> Path:
    """Locate the export under the mounted inputs and verify it against the checkpoint manifest."""

    found = [p for root in search_roots if root.is_dir() for p in sorted(root.rglob(name))]
    if not found:
        raise FileNotFoundError(f"{name} not found under {[str(r) for r in search_roots]}; attach the artifact dataset")
    for path in found:
        if sha256_file(path) == sha256:
            return path
    raise ValueError(f"{name} found at {[str(p) for p in found]} but none matches SHA-256 {sha256[:12]}")


def load_model(export_path: Path, device: str):
    """Load the fastai export; returns the torch model in eval mode and the class vocabulary."""

    from fastai.learner import load_learner

    learn = load_learner(export_path, cpu=device == "cpu")
    model = learn.model.to(device).eval()
    return model, list(learn.dls.vocab)


def test_items(config: RobustnessConfig, repo_root: Path) -> pd.DataFrame:
    predictions = pd.read_csv(repo_root / config.get("data.predictions"))
    items = predictions[predictions["split"] == config.get("data.split")].reset_index(drop=True)
    if items.empty or items["id"].duplicated().any():
        raise ValueError("test items are empty or have duplicate ids")
    return items


class PerturbedImages:
    """Map-style dataset: (tensor, index) for one condition. Works with torch DataLoader workers."""

    def __init__(self, root: Path, items: pd.DataFrame, condition: Condition, config: RobustnessConfig):
        self.root = Path(root)
        self.paths = items["processed_path"].tolist()
        self.ids = items["id"].tolist()
        self.condition = condition
        self.seed = int(config.get("seed"))
        self.size = int(config.get("inference.image_size"))
        self.interp = _INTERP[config.get("inference.resize_interpolation")]
        self.mean = np.asarray(config.get("inference.mean"), dtype=np.float32).reshape(3, 1, 1)
        self.std = np.asarray(config.get("inference.std"), dtype=np.float32).reshape(3, 1, 1)

    def __len__(self) -> int:
        return len(self.paths)

    def image(self, index: int) -> Image.Image:
        with Image.open(self.root / self.paths[index]) as im:
            img = im.convert("RGB")
        c = self.condition
        img = apply(c.kind, img, c.level, image_seed(self.seed, c.id, self.ids[index]))
        if img.size != (self.size, self.size):
            img = img.resize((self.size, self.size), self.interp)
        return img

    def __getitem__(self, index: int):
        import torch

        x = np.asarray(self.image(index), dtype=np.float32).transpose(2, 0, 1) / 255.0
        return torch.from_numpy((x - self.mean) / self.std), index


def predict(model, dataset: PerturbedImages, positive_index: int, batch_size: int, num_workers: int, device: str) -> np.ndarray:
    import torch
    from torch.utils.data import DataLoader

    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers,
                        pin_memory=device != "cpu", persistent_workers=False)
    probs = np.empty(len(dataset), dtype=np.float64)
    with torch.inference_mode():
        for x, index in loader:
            out = torch.softmax(model(x.to(device, non_blocking=True)).float(), dim=1)[:, positive_index]
            probs[index.numpy()] = out.cpu().numpy()
    return probs


def clean_check(probs: np.ndarray, items: pd.DataFrame, atol: float) -> dict:
    diff = np.abs(probs - items["y_prob"].to_numpy())
    threshold = float(items["threshold"].iloc[0])
    flips = int(((probs >= threshold).astype(int) != items["y_pred"].to_numpy()).sum())
    result = {"max_abs_diff": float(diff.max()), "mean_abs_diff": float(diff.mean()), "decision_mismatches": flips, "atol": atol}
    if result["max_abs_diff"] > atol:
        raise CleanCheckError(
            f"clean probabilities differ from predictions.csv by up to {result['max_abs_diff']:.2e} (> {atol}); "
            "the input pipeline does not match training"
        )
    return result


def _condition_file(work_dir: Path, condition: Condition) -> Path:
    return work_dir / f"{condition.id}.csv"


def run(
    config: RobustnessConfig,
    repo_root: Path,
    processed_root: Path,
    model,
    vocab: list[str],
    work_dir: Path,
    out_dir: Path,
    *,
    device: str,
    extra_manifest: dict | None = None,
    log: Callable[[str], None] = print,
) -> pd.DataFrame:
    """Run every condition, clean first. Finished conditions in ``work_dir`` are reused."""

    items = test_items(config, repo_root)
    positive = config.get("model.positive_class")
    if positive not in vocab:
        raise ValueError(f"positive class {positive!r} not in model vocab {vocab}")
    pos = vocab.index(positive)
    work_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    bs, workers = int(config.get("inference.batch_size")), int(config.get("inference.num_workers"))

    columns: dict[str, np.ndarray] = {}
    timings: dict[str, float] = {}
    check = None
    for condition in config.conditions:
        path = _condition_file(work_dir, condition)
        if path.is_file():
            done = pd.read_csv(path)
            if done["id"].tolist() == items["id"].tolist():
                columns[condition.id] = done["prob"].to_numpy()
                log(f"{condition.id}: reused {path.name}")
                if condition.id == CLEAN:
                    check = clean_check(columns[CLEAN], items, float(config.get("inference.clean_check_atol")))
                continue
        start = time.perf_counter()
        probs = predict(model, PerturbedImages(processed_root, items, condition, config), pos, bs, workers, device)
        timings[condition.id] = round(time.perf_counter() - start, 1)
        if condition.id == CLEAN:
            check = clean_check(probs, items, float(config.get("inference.clean_check_atol")))
            log(f"clean check PASS: max |diff| {check['max_abs_diff']:.2e}, decision mismatches {check['decision_mismatches']}")
        tmp = path.with_suffix(".tmp")
        pd.DataFrame({"id": items["id"], "prob": probs}).to_csv(tmp, index=False, float_format="%.8f")
        tmp.replace(path)
        columns[condition.id] = probs
        log(f"{condition.id}: {timings[condition.id]} s, mean P({positive}) {probs.mean():.4f}")

    wide = pd.DataFrame({"id": items["id"], **columns})
    wide.to_csv(out_dir / PROBS_NAME, index=False, float_format="%.6f")
    manifest = {
        "evaluation_id": config.get("evaluation_id"),
        "experiment_id": config.get("experiment_id"),
        "model_id": config.get("model.model_id"),
        "export_sha256": config.get("model.export_sha256"),
        "config": config.path.name,
        "config_sha256": config.sha256,
        "split": config.get("data.split"),
        "n_images": len(items),
        "conditions": [c.id for c in config.conditions],
        "clean_check": check,
        "seconds": timings,
        "device": device,
        "python": platform.python_version(),
        **(extra_manifest or {}),
    }
    (out_dir / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return wide
