"""Builds a tiny, self-contained repo layout + synthetic images for training tests."""

from __future__ import annotations

import csv
import hashlib
import random
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
EXP0001_CONFIG = REPO_ROOT / "06_Experiments" / "EXP0001" / "config.yaml"
SPLIT_REL = "03_Datasets/splits/DS0001_PP0001_SPLIT0001/assignments.csv"
COUNTS = {"train": 8, "val": 4, "test": 4}


def write_images(processed_root: Path, size: int = 32, seed: int = 0) -> list[dict]:
    from PIL import Image

    rng = random.Random(seed)
    rows = []
    for partition, per_class in COUNTS.items():
        for label, base in (("fake", (200, 60, 60)), ("real", (60, 60, 200))):
            for i in range(per_class):
                rel = f"images/{label}/{partition}_{i:03d}.png"
                pixels = bytes(
                    max(0, min(255, channel + rng.randint(-40, 40)))
                    for _ in range(size * size)
                    for channel in base
                )
                target = processed_root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                Image.frombytes("RGB", (size, size), pixels).save(target)
                rows.append(
                    {
                        "processed_path": rel,
                        "relative_path": rel.replace(".png", ".jpg"),
                        "partition": partition,
                        "class_label": label,
                        "generator": "synthetic" if label == "fake" else "none",
                        "identity": f"{label}_{partition}_{i}",
                        "content_hash": hashlib.sha256(pixels).hexdigest(),
                    }
                )
    return rows


def write_assignments(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def smoke_config(processed_root: Path) -> dict:
    """EXP0001's config shrunk to a CPU-sized run: 1 frozen + 1 unfrozen epoch, 32 px, resnet18 from scratch."""

    config = yaml.safe_load(EXP0001_CONFIG.read_text(encoding="utf-8"))
    config["dataset"]["processed_root"] = str(processed_root)
    config["model"].update(backbone="resnet18", pretrained=False)
    config["image_size"] = 32
    config["fastai"]["item_tfms"]["resize"] = 32
    config["fastai"]["mixed_precision"] = False
    config["fastai"]["dataloaders"].update(batch_size_eval=8, num_workers=0)
    config["fastai"]["schedule"]["freeze_epochs"] = 1
    config["fastai"]["lr_finder"]["num_it"] = 5
    config["batch_size"] = 4
    config["epochs"] = 1
    config["git_commit"] = "0" * 40
    return config


def build_tiny_repo(root: Path) -> Path:
    """Create root/{03_Datasets,06_Experiments/EXP0001,...}; return the config path."""

    processed_root = root / "kaggle_input" / "ds0001-pp0001"
    rows = write_images(processed_root)
    write_assignments(root / SPLIT_REL, rows)
    exp_dir = root / "06_Experiments" / "EXP0001"
    for sub in ("logs", "metrics", "predictions", "learning_curves", "notebook"):
        (exp_dir / sub).mkdir(parents=True, exist_ok=True)
    config_path = exp_dir / "config.yaml"
    config_path.write_text(yaml.safe_dump(smoke_config(processed_root), sort_keys=False), encoding="utf-8")
    return config_path
