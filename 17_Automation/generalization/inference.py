"""Cross-dataset inference for Phase E8 on Kaggle. Reuses the robustness input pipeline (clean condition).

A sanity pass re-predicts the first reference images and must match predictions.csv before any target is run.
"""

from __future__ import annotations

import json
import os
import platform
import time
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd

from robustness.config import CLEAN, Condition
from robustness.inference import CleanCheckError, PerturbedImages, predict

from .config import GeneralizationConfig

PREDICTIONS_DIR = "predictions"
MANIFEST_NAME = "run_manifest.json"
_CLEAN = Condition(CLEAN, CLEAN, CLEAN, None, 0)


def target_items(config: GeneralizationConfig, dataset: dict, repo_root: Path) -> pd.DataFrame:
    """Test-partition rows for one target dataset, optionally a seeded sample. `id` is the processed path."""

    frame = pd.read_csv(repo_root / dataset["assignments"], dtype=str, keep_default_na=False)
    frame = frame[frame["partition"] == dataset["partition"]].sort_values("processed_path").reset_index(drop=True)
    if frame.empty:
        raise ValueError(f"{dataset['name']}: partition {dataset['partition']!r} is empty")
    if frame["processed_path"].duplicated().any():
        raise ValueError(f"{dataset['name']}: duplicate processed_path values")
    cap = dataset.get("max_images")
    if cap and len(frame) > cap:
        rng = np.random.default_rng(int(config.get("seed")))
        frame = frame.iloc[np.sort(rng.choice(len(frame), size=cap, replace=False))].reset_index(drop=True)
    label = frame["class_label"]
    if not set(label) <= {"fake", "real"}:
        raise ValueError(f"{dataset['name']}: unexpected class labels {sorted(set(label))}")
    return pd.DataFrame({
        "dataset": dataset["name"],
        "id": frame["processed_path"],
        "processed_path": frame["processed_path"],
        "y_true": (label == config.get("model.positive_class")).astype(int),
        "generator": frame["generator"],
        "content_hash": frame.get("content_hash", ""),
    })


def resolve_root(configured: Path, sample: str, max_depth: int = 3) -> Path:
    """The configured root if `sample` exists under it; else the first folder within the mount that holds it."""

    if (configured / sample).is_file():
        return configured
    mount = configured.parent if configured.parent.is_dir() else configured
    for dirpath, dirnames, _ in os.walk(mount):
        depth = len(Path(dirpath).relative_to(mount).parts)
        if (Path(dirpath) / sample).is_file():
            return Path(dirpath)
        if depth >= max_depth:
            dirnames[:] = []
    raise FileNotFoundError(f"{sample} not found under {configured} or {mount}; attach the processed dataset")


def sanity_check(config: GeneralizationConfig, repo_root: Path, model, pos: int, device: str, reference_root: Path) -> dict:
    ref = pd.read_csv(repo_root / config.get("reference.predictions"))
    ref = ref[ref["split"] == config.get("reference.split")].head(int(config.get("inference.sanity_images"))).reset_index(drop=True)
    probs = predict(model, PerturbedImages(reference_root, ref, _CLEAN, config), pos,
                    int(config.get("inference.batch_size")), int(config.get("inference.num_workers")), device)
    diff = float(np.abs(probs - ref["y_prob"].to_numpy()).max())
    atol = float(config.get("inference.sanity_atol"))
    if diff > atol:
        raise CleanCheckError(f"reference images differ from predictions.csv by up to {diff:.2e} (> {atol})")
    return {"images": len(ref), "max_abs_diff": diff, "atol": atol}


def run(
    config: GeneralizationConfig,
    repo_root: Path,
    model,
    vocab: list[str],
    out_dir: Path,
    reference_root: Path,
    *,
    device: str,
    extra_manifest: dict | None = None,
    log: Callable[[str], None] = print,
) -> dict[str, pd.DataFrame]:
    """Sanity pass, then each target dataset. Finished datasets in ``out_dir/predictions`` are reused."""

    positive = config.get("model.positive_class")
    if positive not in vocab:
        raise ValueError(f"positive class {positive!r} not in model vocab {vocab}")
    pos = vocab.index(positive)
    pred_dir = out_dir / PREDICTIONS_DIR
    pred_dir.mkdir(parents=True, exist_ok=True)
    check = sanity_check(config, repo_root, model, pos, device, reference_root)
    log(f"sanity check PASS: {check['images']} reference images, max |diff| {check['max_abs_diff']:.2e}")

    results, timings, roots = {}, {}, {}
    for dataset in config.datasets:
        items = target_items(config, dataset, repo_root)
        path = pred_dir / f"{dataset['name']}.csv"
        if path.is_file():
            done = pd.read_csv(path, keep_default_na=False)
            if done["id"].tolist() == items["id"].tolist():
                results[dataset["name"]] = done
                log(f"{dataset['name']}: reused {path.name}")
                continue
        root = resolve_root(Path(dataset["processed_root"]), items["processed_path"].iloc[0])
        roots[dataset["name"]] = str(root)
        start = time.perf_counter()
        probs = predict(model, PerturbedImages(root, items, _CLEAN, config), pos,
                        int(config.get("inference.batch_size")), int(config.get("inference.num_workers")), device)
        timings[dataset["name"]] = round(time.perf_counter() - start, 1)
        frame = items.drop(columns="processed_path").assign(y_prob=probs)
        tmp = path.with_suffix(".tmp")
        frame.to_csv(tmp, index=False, float_format="%.6f")
        tmp.replace(path)
        results[dataset["name"]] = pd.read_csv(path, keep_default_na=False)
        log(f"{dataset['name']}: {len(items)} images, {timings[dataset['name']]} s, mean P({positive}) {probs.mean():.4f}")

    manifest = {
        "evaluation_id": config.get("evaluation_id"),
        "model_id": config.get("model.model_id"),
        "export_sha256": config.get("model.export_sha256"),
        "config": config.path.name,
        "config_sha256": config.sha256,
        "sanity_check": check,
        "datasets": {name: len(frame) for name, frame in results.items()},
        "processed_roots": roots,
        "seconds": timings,
        "device": device,
        "python": platform.python_version(),
        **(extra_manifest or {}),
    }
    (out_dir / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return results
