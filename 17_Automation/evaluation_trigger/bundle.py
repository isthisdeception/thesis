"""Write the Phase M16 evaluation inputs for one experiment from its saved predictions."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd

from .curves import _as_binary, calibration_rows, confusion_rows, gradcam_sample, pr_rows, roc_rows

SPLITS = ("val", "test")
BINS = 15


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write(path: Path, frame: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)


def write_bundle(
    *,
    repo_root: Path,
    experiment_id: str,
    positive_class: str,
    negative_class: str,
) -> dict:
    """Derive evaluation tables from the training prediction CSVs. Does not call the model."""

    source_dir = repo_root / "06_Experiments" / experiment_id / "predictions"
    out = repo_root / "08_Evaluation" / experiment_id
    frames = []
    sources = {}
    for split in SPLITS:
        path = source_dir / f"{split}_predictions.csv"
        if not path.is_file():
            raise FileNotFoundError(f"saved predictions not found: {path}")
        frame = _as_binary(pd.read_csv(path), positive_class)
        frame.insert(0, "split", split)
        frames.append(frame)
        sources[split] = {"path": path.relative_to(repo_root).as_posix(), "sha256": _sha256(path), "rows": len(frame)}

    combined = pd.concat(frames, ignore_index=True)
    _write(out / "predictions.csv", combined[["split", "id", "y_true", "y_prob", "y_pred", "threshold", "processed_path", "generator"]])
    _write(out / "confusion.csv", pd.DataFrame([row for frame in frames for row in confusion_rows(frame["split"].iloc[0], frame, positive_class, negative_class)]))
    _write(out / "roc_curve.csv", pd.DataFrame([row for frame in frames for row in roc_rows(frame["split"].iloc[0], frame)]))
    _write(out / "pr_curve.csv", pd.DataFrame([row for frame in frames for row in pr_rows(frame["split"].iloc[0], frame)]))
    _write(out / "calibration.csv", pd.DataFrame([row for frame in frames for row in calibration_rows(frame["split"].iloc[0], frame, BINS)]))
    _write(out / "gradcam_sample.csv", gradcam_sample(frames[SPLITS.index("test")]))

    manifest = {
        "experiment_id": experiment_id,
        "positive_class": positive_class,
        "negative_class": negative_class,
        "calibration_bins": BINS,
        "sources": sources,
        "gradcam": {
            "status": "sample_only",
            "reason": "MODEL0001 weights and the images are in the Kaggle artifact and data tiers, not in Git. gradcam_sample.csv is the case list. Maps are computed by evaluation_trigger.gradcam when that export is mounted.",
            "target_layer": "layer4",
        },
        "feature_importance": {
            "status": "not_applicable",
            "reason": "ResNet-50 has no separate feature-importance output. Case-level attribution is the Grad-CAM sample, not a global importance table.",
        },
        "figures": "none (A.9: data only)",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest
