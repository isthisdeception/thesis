#!/usr/bin/env python3
"""STEP-027 — Register & run preprocessing pipelines (Kaggle / local).

Copy ``04_Preprocessing/`` (+ ``17_Automation/dataset_eda`` for labels) to the
notebook working dir, attach raw datasets, then:

  python step027_run_preprocessing.py
  # or single pipeline:
  STEP027_PIPELINE=PP0001 python step027_run_preprocessing.py

Environment:
  STEP027_PIPELINE   — PP0001..PP0005 or ALL (default ALL)
  STEP027_MAX_IMAGES — optional cap for smoke tests
  STEP027_SEARCH     — comma-separated search roots (default /kaggle/input)
"""

from __future__ import annotations

import os
import shutil
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
# Label inference reuse
_AUTOMATION = HERE.parents[0] / "17_Automation"
if not _AUTOMATION.is_dir():
    _AUTOMATION = Path("/kaggle/working/17_Automation")
if _AUTOMATION.is_dir() and str(_AUTOMATION) not in sys.path:
    sys.path.insert(0, str(_AUTOMATION))

from modules.discovery import discover_image_paths  # noqa: E402
from modules.format_conversion import FormatConversionParams  # noqa: E402
from modules.image_verification import ImageVerificationParams  # noqa: E402
from modules.metadata_extraction import MetadataExtractionParams  # noqa: E402
from modules.normalization import NormalizationParams  # noqa: E402
from modules.quality_filtering import QualityFilteringParams  # noqa: E402
from modules.report_writer import write_preprocessing_report  # noqa: E402
from modules.resize import ResizeParams  # noqa: E402
from pipeline_runner import PipelineConfig, run_pipeline  # noqa: E402

try:
    from dataset_validation.adapters import discover_layout  # type: ignore
except ImportError:  # pragma: no cover
    discover_layout = None  # type: ignore

RESEARCH_Q = (
    "How can we improve the cross-generator generalization of "
    "image-based AI face detection models to maintain high accuracy "
    "on unseen generative architectures?"
)

DEFAULT_OPS = [
    "PPMOD01",
    "PPMOD10",
    "PPMOD08",
    "PPMOD07",
    "PPMOD09",
    "PPMOD05",
    "PPMOD06",
]

# Planned profiles from STEP-025 design
PIPELINES: dict[str, dict] = {
    "PP0001": {
        "dataset_id": "DS0001",
        "purpose": "Primary train processed (face packs default)",
        "require_identity": False,
        "require_generator": False,
        "exclude_list": None,
    },
    "PP0002": {
        "dataset_id": "DS0002",
        "purpose": "Primary eval processed (+ CORRUPT_IMAGE exclude)",
        "require_identity": True,
        "require_generator": True,
        "exclude_list": "exclude_lists/exclude_list_DS0002.csv",
    },
    "PP0003": {
        "dataset_id": "DS0003",
        "purpose": "Quick baseline processed",
        "require_identity": False,
        "require_generator": False,
        "exclude_list": None,
    },
    "PP0004": {
        "dataset_id": "DS0004",
        "purpose": "Frequency supplementary processed",
        "require_identity": False,
        "require_generator": False,
        "exclude_list": None,
    },
    "PP0005": {
        "dataset_id": "DS0005",
        "purpose": "Bias eval processed (FairFace)",
        "require_identity": False,
        "require_generator": False,
        "exclude_list": None,
    },
}


def _search_roots() -> list[Path]:
    env = os.environ.get("STEP027_SEARCH", "").strip()
    if env:
        return [Path(p) for p in env.split(",") if p.strip()]
    kaggle = Path("/kaggle/input")
    if kaggle.exists():
        return [kaggle]
    return [
        Path("_staging/DS0001_artifact/kaggle_upload"),
        Path("_staging/DS0002_diff/kaggle_upload"),
        Path("_staging/DS0004_synthbuster/kaggle_upload"),
        Path("_staging/DS0005_fairface/kaggle_upload"),
        Path("_staging/DS0003_140k"),
        Path("03_Datasets/raw"),
    ]


def _collect_images(
    dataset_id: str,
    search_roots: list[Path],
    max_images: int | None,
) -> tuple[Path, list[tuple[Path, str]]]:
    """Return (primary_raw_root, image list) using STEP-022 layout discovery when available."""
    images: list[tuple[Path, str]] = []
    primary: Path | None = None
    seen: set[str] = set()

    def _add(path: Path, rel: str) -> bool:
        key = rel.replace("\\", "/")
        if key in seen:
            return False
        seen.add(key)
        images.append((path, rel))
        return max_images is not None and len(images) >= max_images

    if discover_layout is not None:
        layout = discover_layout(dataset_id, search_roots)
        for root in layout.roots:
            if primary is None:
                primary = root
            for path, rel in discover_image_paths(root, include_zips=False):
                if _add(path, rel):
                    return primary or root, images
        for zpath in layout.archives:
            if primary is None:
                primary = zpath.parent
            for path, rel in discover_image_paths(zpath.parent, include_zips=True):
                if path != zpath:
                    continue
                if _add(path, rel):
                    return primary or zpath.parent, images
        if images and primary is not None:
            return primary, images

    raw_root = _find_raw_root_fallback(dataset_id, search_roots)
    return raw_root, discover_image_paths(raw_root, max_images=max_images, include_zips=True)


def _find_raw_root_fallback(dataset_id: str, search_roots: list[Path]) -> Path:
    for root in search_roots:
        for hit in [root / "raw" / dataset_id, root / dataset_id]:
            if hit.is_dir():
                return hit
        try:
            for hit in root.rglob(dataset_id):
                if hit.is_dir() and hit.name == dataset_id:
                    return hit
        except OSError:
            continue
    raise FileNotFoundError(f"Could not locate raw root for {dataset_id} under {search_roots}")


def _find_raw_root(dataset_id: str, search_roots: list[Path]) -> Path:
    primary, _ = _collect_images(dataset_id, search_roots, max_images=1)
    return primary

def _find_optional_csv(raw_root: Path, names: list[str]) -> Path | None:
    for name in names:
        direct = raw_root / name
        if direct.is_file():
            return direct
    for name in names:
        try:
            hits = list(raw_root.rglob(name))
        except OSError:
            hits = []
        if hits:
            return hits[0]
    return None


def build_config(
    pipeline_id: str,
    raw_root: Path,
    processed_root: Path,
    spec: dict,
) -> PipelineConfig:
    exclude = None
    if spec.get("exclude_list"):
        excl_path = HERE / spec["exclude_list"]
        if not excl_path.is_file():
            # Kaggle upload may place exclude list next to modules
            alt = Path("/kaggle/working") / spec["exclude_list"]
            excl_path = alt if alt.is_file() else excl_path
        exclude = excl_path if excl_path.is_file() else None
        if exclude is None:
            raise FileNotFoundError(f"exclude list missing for {pipeline_id}: {spec['exclude_list']}")

    meta_csv = None
    fairface = []
    if spec["dataset_id"] == "DS0001":
        meta_csv = _find_optional_csv(raw_root, ["metadata.csv"])
    if spec["dataset_id"] == "DS0005":
        for n in ("fairface_label_train.csv", "fairface_label_val.csv"):
            p = _find_optional_csv(raw_root, [n])
            if p:
                fairface.append(p)

    return PipelineConfig(
        pipeline_id=pipeline_id,
        dataset_id=spec["dataset_id"],
        raw_root=raw_root,
        processed_root=processed_root,
        random_seed=42,
        module_sequence=list(DEFAULT_OPS),
        verification=ImageVerificationParams(),
        metadata=MetadataExtractionParams(
            require_class_label=spec["dataset_id"] in {"DS0001", "DS0003", "DS0004"},
            require_generator=bool(spec["require_generator"]),
            require_identity=bool(spec["require_identity"]),
            metadata_csv_path=meta_csv,
            fairface_label_csvs=fairface,
        ),
        quality=QualityFilteringParams(
            exclude_list_path=exclude,
            exclude_codes=["CORRUPT_IMAGE"],
            dedupe_policy="off",
            min_side=64,
        ),
        resize=ResizeParams(target_size=224, keep_aspect=False, interpolation="bilinear"),
        format_conversion=FormatConversionParams(force_rgb=True, output_format="PNG"),
        normalization=NormalizationParams(
            norm_mode="imagenet",
            apply_on_disk=False,
            random_seed=42,
        ),
    )


def run_one(pipeline_id: str, max_images: int | None) -> dict:
    spec = PIPELINES[pipeline_id]
    dataset_id = spec["dataset_id"]
    output_id = f"{dataset_id}_{pipeline_id}"
    search_roots = _search_roots()
    raw_root, images = _collect_images(dataset_id, search_roots, max_images)

    working = Path("/kaggle/working") if Path("/kaggle/working").exists() else HERE / "_runs"
    processed_root = working / "processed" / output_id
    if processed_root.exists():
        # Never overwrite — refuse and ask for a new PP id
        raise SystemExit(
            f"Refusing to overwrite existing processed output: {processed_root}. "
            "Use a new PPxxxx for new parameters."
        )

    cfg = build_config(pipeline_id, raw_root, processed_root, spec)
    if not images:
        raise SystemExit(f"No images discovered for {dataset_id} under {search_roots}")

    print(f"[{pipeline_id}] raw={raw_root} n={len(images)} -> {processed_root}")
    summary = run_pipeline(images, cfg)

    # Sync report copy for Git download
    git_reports = working / "git_sync" / "reports"
    git_reports.mkdir(parents=True, exist_ok=True)
    write_preprocessing_report(
        pipeline_id=pipeline_id,
        dataset_id=dataset_id,
        output_id=output_id,
        processed_root=processed_root,
        summary=summary,
        config={
            "module_sequence": cfg.module_sequence,
            "pipeline_id": pipeline_id,
            "dataset_id": dataset_id,
            "target_size": 224,
            "output_format": "PNG",
            "norm_mode": "imagenet",
            "apply_on_disk": False,
            "exclude_list": str(cfg.quality.exclude_list_path) if cfg.quality.exclude_list_path else None,
            "random_seed": 42,
            "purpose": spec["purpose"],
        },
        research_question=RESEARCH_Q,
        kaggle_pointer="PENDING_UPLOAD",
        dest=git_reports / f"{pipeline_id}_report.md",
    )
    # Also copy index/exclude/errors for Git (small metadata)
    meta_sync = working / "git_sync" / "metadata" / output_id
    meta_sync.mkdir(parents=True, exist_ok=True)
    for name in ("index.csv", "exclude_applied.csv", "errors.csv", "normalization_stats.json"):
        src = processed_root / "metadata" / name
        if src.is_file():
            shutil.copy2(src, meta_sync / name)
    cfg_src = processed_root / "config" / "pipeline.json"
    if cfg_src.is_file():
        shutil.copy2(cfg_src, meta_sync / "pipeline.json")

    print(summary)
    return summary


def main() -> int:
    which = os.environ.get("STEP027_PIPELINE", "ALL").strip().upper()
    max_images = os.environ.get("STEP027_MAX_IMAGES", "").strip()
    cap = int(max_images) if max_images else None

    ids = list(PIPELINES) if which in {"ALL", "*"} else [which]
    for pid in ids:
        if pid not in PIPELINES:
            print(f"Unknown pipeline {pid}")
            return 2
        run_one(pid, cap)
    print("STEP-027 run complete", date.today().isoformat())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
