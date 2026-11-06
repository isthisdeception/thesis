"""Assignments loading, dataset validation (fastai-free), and the FastAI DataLoaders builder."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .logs import get_logger
from .settings import TrainingSettings


class DatasetValidationError(ValueError):
    """The split assignments or processed images are not usable for training."""


@dataclass(frozen=True)
class SplitFrames:
    train: pd.DataFrame
    valid: pd.DataFrame
    test: pd.DataFrame

    def train_valid(self, flag_column: str = "is_valid") -> pd.DataFrame:
        """Train + valid rows with a boolean column consumed by ColSplitter."""

        frame = pd.concat([self.train.assign(**{flag_column: False}), self.valid.assign(**{flag_column: True})])
        return frame.reset_index(drop=True)


def load_assignments(settings: TrainingSettings) -> pd.DataFrame:
    path = settings.assignments_csv
    if not path.is_file():
        raise DatasetValidationError(f"split assignments not found: {path}")
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def _suggest_root(root: Path, sample: str) -> str:
    """Find where `sample` actually lives below `root` (or /kaggle/input) to make the error actionable."""

    first = Path(sample).parts[0]
    for base in (root, Path("/kaggle/input")):
        if not base.is_dir():
            continue
        for dirpath, dirnames, _ in os.walk(base):
            if len(Path(dirpath).relative_to(base).parts) > 4:
                dirnames[:] = []
                continue
            if first in dirnames and (Path(dirpath) / sample).is_file():
                return f" Found it under {dirpath}; set dataset.processed_root to that path."
    return ""


def validate_dataset(settings: TrainingSettings, frame: pd.DataFrame, *, check_files: bool = True) -> SplitFrames:
    """Phase M6 dataset validation: columns, partitions, labels, leakage, and image files."""

    logger = get_logger()
    path_col = settings.get("dataset.path_column")
    label_col = settings.get("dataset.label_column")
    part_col = settings.get("dataset.partition_column")
    names = {
        "train": settings.get("split.train_name"),
        "valid": settings.get("split.valid_name"),
        "test": settings.get("split.test_name"),
    }

    missing_cols = [c for c in (path_col, label_col, part_col) if c not in frame.columns]
    if missing_cols:
        raise DatasetValidationError(f"assignments missing column(s): {', '.join(missing_cols)}")

    unknown_parts = sorted(set(frame[part_col]) - set(names.values()))
    if unknown_parts:
        raise DatasetValidationError(f"unexpected partition value(s): {unknown_parts}")

    vocab = settings.vocab
    unknown_labels = sorted(set(frame[label_col]) - set(vocab))
    if unknown_labels:
        raise DatasetValidationError(f"label(s) not in dataset.vocab {vocab}: {unknown_labels}")

    parts = {key: frame[frame[part_col] == value].reset_index(drop=True) for key, value in names.items()}
    for key, part in parts.items():
        if part.empty:
            raise DatasetValidationError(f"partition '{names[key]}' is empty")
    for key in ("train", "valid"):
        absent = sorted(set(vocab) - set(parts[key][label_col]))
        if absent:
            raise DatasetValidationError(f"partition '{names[key]}' has no rows for class(es) {absent}")

    if "content_hash" in frame.columns:
        hashes = {key: set(part["content_hash"]) - {""} for key, part in parts.items()}
        for a, b in (("train", "valid"), ("train", "test"), ("valid", "test")):
            overlap = hashes[a] & hashes[b]
            if overlap:
                raise DatasetValidationError(
                    f"leakage: {len(overlap)} identical image hash(es) in both '{names[a]}' and '{names[b]}'"
                )

    if check_files:
        root = settings.processed_root
        if not root.is_dir():
            raise DatasetValidationError(
                f"dataset.processed_root does not exist: {root}. Attach Kaggle dataset "
                f"{settings.get('dataset.processed_kaggle_slug')} to the session."
            )
        missing = [p for p in frame[path_col] if not (root / p).is_file()]
        if missing:
            hint = _suggest_root(root, missing[0])
            raise DatasetValidationError(
                f"{len(missing)} of {len(frame)} image(s) missing under {root}; first: {missing[0]}.{hint}"
            )

    for key, part in parts.items():
        counts = part[label_col].value_counts().to_dict()
        logger.info("partition %s: %d rows %s", names[key], len(part), counts)
    return SplitFrames(train=parts["train"], valid=parts["valid"], test=parts["test"])


def build_dataloaders(settings: TrainingSettings, frames: SplitFrames):
    """DataBlock → DataLoaders exactly as configured (FastAI standard stages 2–5)."""

    from fastai.vision.all import (
        CategoryBlock,
        ColReader,
        ColSplitter,
        DataBlock,
        ImageBlock,
        Normalize,
        Resize,
        aug_transforms,
    )

    item = settings.get("fastai.item_tfms")
    batch_tfms = []
    aug = settings.get("augmentations.aug_transforms")
    if aug.get("enabled"):
        if not aug.get("train_only"):
            raise DatasetValidationError("augmentations.aug_transforms.train_only must be true")
        batch_tfms.extend(
            aug_transforms(
                do_flip=aug["do_flip"],
                flip_vert=aug["flip_vert"],
                max_rotate=aug["max_rotate"],
                max_zoom=aug["max_zoom"],
                max_lighting=aug["max_lighting"],
                max_warp=aug["max_warp"],
                min_scale=aug["min_scale"],
                pad_mode=aug["pad_mode"],
            )
        )
    norm = settings.get("fastai.normalize")
    batch_tfms.append(Normalize.from_stats(norm["mean"], norm["std"]))

    root = str(settings.processed_root).rstrip("/\\") + "/"
    block = DataBlock(
        blocks=(ImageBlock, CategoryBlock(vocab=settings.vocab)),
        get_x=ColReader(settings.get("dataset.path_column"), pref=root),
        get_y=ColReader(settings.get("dataset.label_column")),
        splitter=ColSplitter("is_valid"),
        item_tfms=Resize(item["resize"], method=item["method"]),
        batch_tfms=batch_tfms,
        n_inp=settings.get("fastai.datablock.n_inp"),
    )
    loader = settings.get("fastai.dataloaders")
    return block.dataloaders(
        frames.train_valid(),
        bs=settings.get("batch_size"),
        val_bs=loader["batch_size_eval"],
        num_workers=loader["num_workers"],
        shuffle=(bool(loader["shuffle_train"]), False),
        drop_last=(bool(loader["drop_last"]), False),
    )
