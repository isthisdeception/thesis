"""PPMOD10 — Metadata extraction (no pixel writes)."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

from .types import ImageRecord, ModuleError

MODULE_ID = "PPMOD10"

# Prefer reuse of STEP-023 label inference (import, do not silently fork).
_REPO_ROOT = Path(__file__).resolve().parents[2]
_AUTOMATION = _REPO_ROOT / "17_Automation"
if str(_AUTOMATION) not in sys.path:
    sys.path.insert(0, str(_AUTOMATION))

from dataset_eda.labels import (  # noqa: E402
    load_ds0001_metadata,
    load_fairface_labels,
    record_from_path,
)

CANONICAL_FIELDS = (
    "dataset_id",
    "relative_path",
    "class_label",
    "generator",
    "condition",
    "identity",
    "split",
    "age",
    "gender",
    "race",
)


@dataclass
class MetadataExtractionParams:
    label_source: str = "auto"
    require_class_label: bool = True
    require_generator: bool = False
    require_identity: bool = False
    fairface_label_csvs: list[Path] = field(default_factory=list)
    metadata_csv_path: Path | None = None
    source_container: str = ""


def extract_metadata(
    record: ImageRecord,
    params: MetadataExtractionParams,
) -> ImageRecord:
    """Fill canonical metadata fields on ``record``. Raises if required fields missing."""
    dataset_id = record.dataset_id
    if not dataset_id:
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="MISSING_DATASET_ID",
            message="dataset_id required for metadata extraction",
            path=record.relative_path,
        )

    ds0001_meta = None
    if params.metadata_csv_path:
        ds0001_meta = load_ds0001_metadata([Path(params.metadata_csv_path)])
    elif dataset_id == "DS0001" and params.label_source == "auto":
        # optional: leave None → path heuristics
        ds0001_meta = None

    fairface = None
    if params.fairface_label_csvs:
        fairface = load_fairface_labels([Path(p) for p in params.fairface_label_csvs])

    container = params.source_container or (
        str(record.source_path.parent) if record.source_path else ""
    )
    inferred = record_from_path(
        dataset_id,
        record.relative_path,
        container,
        size_bytes=int(record.extras.get("size_bytes", 0)),
        ds0001_meta=ds0001_meta,
    )
    if inferred is None:
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="NOT_AN_IMAGE_PATH",
            message="path rejected by label inference (junk or non-image)",
            path=record.relative_path,
        )

    record.class_label = inferred.class_label
    record.generator = inferred.generator
    record.condition = inferred.condition
    record.identity = inferred.identity or None

    if dataset_id == "DS0005" and fairface:
        key = record.relative_path.replace("\\", "/")
        demo = fairface.get(key) or fairface.get(Path(key).name)
        if demo:
            record.age = demo.get("age") or None
            record.gender = demo.get("gender") or None
            record.race = demo.get("race") or None
            record.split = demo.get("split") or record.condition
    elif dataset_id == "DS0003":
        record.split = inferred.condition or None
    elif dataset_id == "DS0005":
        record.split = inferred.condition or None

    _enforce_requirements(record, params)
    return record


def _enforce_requirements(record: ImageRecord, params: MetadataExtractionParams) -> None:
    if params.require_class_label and (
        not record.class_label or record.class_label == "unknown"
    ):
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="MISSING_CLASS_LABEL",
            message="class_label required but missing/unknown",
            path=record.relative_path,
        )
    if params.require_generator and (
        not record.generator or record.generator in {"unknown", ""}
    ):
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="MISSING_GENERATOR",
            message="generator required but missing",
            path=record.relative_path,
        )
    if params.require_identity and not record.identity:
        raise ModuleError(
            module_id=MODULE_ID,
            reason_code="MISSING_IDENTITY",
            message="identity required but missing",
            path=record.relative_path,
        )


def to_index_row(record: ImageRecord) -> dict[str, str]:
    return {
        "dataset_id": record.dataset_id or "",
        "relative_path": record.relative_path,
        "class_label": record.class_label or "",
        "generator": record.generator or "",
        "condition": record.condition or "",
        "identity": record.identity or "",
        "split": record.split or "",
        "age": record.age or "",
        "gender": record.gender or "",
        "race": record.race or "",
        "reason_code": record.reason_code,
        "content_hash": record.content_hash or "",
        "original_size": (
            f"{record.original_size[0]}x{record.original_size[1]}"
            if record.original_size
            else ""
        ),
        "current_size": (
            f"{record.current_size[0]}x{record.current_size[1]}"
            if record.current_size
            else ""
        ),
        "output_format": record.output_format or "",
        "exif_stripped": str(record.exif_stripped).lower(),
    }
