"""Thin pipeline glue — sequences modules; contains no image math."""

from __future__ import annotations

import csv
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

_PREPROC_ROOT = Path(__file__).resolve().parent
if str(_PREPROC_ROOT) not in sys.path:
    sys.path.insert(0, str(_PREPROC_ROOT))

from modules.artifact_removal import ArtifactRemovalParams, strip_artifacts
from modules.cropping import CroppingParams, crop_face
from modules.face_alignment import FaceAlignmentParams, align_face
from modules.face_detection import FaceDetectionParams, detect_faces
from modules.format_conversion import FormatConversionParams, save_processed_image
from modules.image_verification import (
    ImageVerificationParams,
    verify_image_bytes,
    verify_path,
)
from modules.metadata_extraction import MetadataExtractionParams, extract_metadata, to_index_row
from modules.normalization import (
    NormalizationParams,
    apply_normalization,
    compute_dataset_stats,
    write_stats_json,
)
from modules.quality_filtering import QualityFilteringParams, filter_quality, load_exclude_paths
from modules.report_writer import write_preprocessing_report
from modules.resize import ResizeParams, resize_image
from modules.types import ErrorRow, ExcludeRow, ModuleError
import zipfile


@dataclass
class PipelineConfig:
    """Frozen parameter bag for one PPxxxx run (written to config/pipeline.yaml-equivalent JSON)."""

    pipeline_id: str
    dataset_id: str
    raw_root: Path
    processed_root: Path
    random_seed: int = 42
    module_sequence: list[str] = field(
        default_factory=lambda: [
            "PPMOD01",
            "PPMOD10",
            "PPMOD08",
            "PPMOD07",
            "PPMOD09",
            "PPMOD05",
            "PPMOD06",
        ]
    )
    verification: ImageVerificationParams = field(default_factory=ImageVerificationParams)
    metadata: MetadataExtractionParams = field(default_factory=MetadataExtractionParams)
    artifact: ArtifactRemovalParams = field(default_factory=ArtifactRemovalParams)
    quality: QualityFilteringParams = field(default_factory=QualityFilteringParams)
    face_detection: FaceDetectionParams = field(default_factory=FaceDetectionParams)
    face_alignment: FaceAlignmentParams = field(default_factory=FaceAlignmentParams)
    cropping: CroppingParams = field(default_factory=CroppingParams)
    format_conversion: FormatConversionParams = field(default_factory=FormatConversionParams)
    resize: ResizeParams = field(default_factory=ResizeParams)
    normalization: NormalizationParams = field(default_factory=NormalizationParams)


def _assert_raw_readonly(raw_root: Path, processed_root: Path) -> None:
    raw_root = raw_root.resolve()
    processed_root = processed_root.resolve()
    if processed_root == raw_root or raw_root in processed_root.parents:
        # processed must not be inside a path that implies overwriting raw tree root equality
        pass
    if "raw" in processed_root.parts and "processed" not in processed_root.parts:
        raise ModuleError(
            "PIPELINE",
            "RAW_WRITE_FORBIDDEN",
            f"processed_root looks like raw: {processed_root}",
        )


def _ensure_tree(processed_root: Path) -> dict[str, Path]:
    paths = {
        "images": processed_root / "images",
        "metadata": processed_root / "metadata",
        "reports": processed_root / "reports",
        "config": processed_root / "config",
    }
    for p in paths.values():
        p.mkdir(parents=True, exist_ok=True)
    return paths


def _serialize_config(cfg: PipelineConfig) -> dict[str, Any]:
    def conv(obj: Any) -> Any:
        if isinstance(obj, Path):
            return str(obj)
        if hasattr(obj, "__dataclass_fields__"):
            return {k: conv(v) for k, v in asdict(obj).items()}
        if isinstance(obj, (list, tuple)):
            return [conv(x) for x in obj]
        return obj

    return conv(cfg)


def process_one(
    path: Path,
    relative_path: str,
    cfg: PipelineConfig,
    *,
    exclude_map: dict[str, str],
    seen_hashes: dict[str, str],
) -> tuple[Any | None, ExcludeRow | None, ErrorRow | None]:
    """Run module sequence for a single file. Returns (kept_record, exclude, error).

    Zip members use relative_path form ``archive.zip::inner/path.jpg``.
    """
    try:
        member_rel = relative_path
        container = str(path.parent)
        if "::" in relative_path and path.suffix.lower() == ".zip":
            zip_name, member_rel = relative_path.split("::", 1)
            container = str(path)
            with zipfile.ZipFile(path, "r") as zf:
                data = zf.read(member_rel)
            record = verify_image_bytes(
                data,
                member_rel,
                cfg.verification,
                dataset_id=cfg.dataset_id,
            )
            record.extras["size_bytes"] = len(data)
            record.extras["zip_archive"] = zip_name
        else:
            record = verify_path(
                path,
                relative_path,
                cfg.verification,
                dataset_id=cfg.dataset_id,
            )
            member_rel = relative_path

        if not record.kept:
            return None, ExcludeRow(member_rel, record.reason_code), None

        for mod in cfg.module_sequence:
            if mod == "PPMOD01":
                continue  # already done
            if mod == "PPMOD10":
                meta_params = cfg.metadata
                meta_params.source_container = container
                record.relative_path = member_rel
                record = extract_metadata(record, meta_params)
            elif mod == "PPMOD08":
                record = strip_artifacts(record, cfg.artifact)
            elif mod == "PPMOD07":
                record = filter_quality(
                    record,
                    cfg.quality,
                    exclude_map=exclude_map,
                    seen_hashes=seen_hashes,
                )
                if not record.kept:
                    return None, ExcludeRow(member_rel, record.reason_code), None
            elif mod == "PPMOD02":
                record = detect_faces(record, cfg.face_detection)
            elif mod == "PPMOD03":
                record = align_face(record, cfg.face_alignment)
            elif mod == "PPMOD04":
                record = crop_face(record, cfg.cropping)
            elif mod == "PPMOD09":
                from modules.format_conversion import convert_format

                record = convert_format(record, cfg.format_conversion)
            elif mod == "PPMOD05":
                record = resize_image(record, cfg.resize)
            elif mod == "PPMOD06":
                record = apply_normalization(record, cfg.normalization)
            else:
                raise ModuleError("PIPELINE", "UNKNOWN_MODULE", f"unknown module {mod}")

        return record, None, None
    except ModuleError as exc:
        return None, None, ErrorRow(relative_path, exc.module_id, exc.reason_code, str(exc))
    except Exception as exc:  # noqa: BLE001 — surface unexpected failures explicitly
        return None, None, ErrorRow(relative_path, "PIPELINE", "UNEXPECTED", str(exc))


def run_pipeline(
    image_paths: Iterable[tuple[Path, str]],
    cfg: PipelineConfig,
) -> dict[str, Any]:
    """Execute pipeline over (absolute_path, relative_path) pairs.

    Writes only under ``cfg.processed_root``. Never modifies ``cfg.raw_root``.
    """
    _assert_raw_readonly(Path(cfg.raw_root), Path(cfg.processed_root))
    tree = _ensure_tree(Path(cfg.processed_root))

    exclude_map = load_exclude_paths(cfg.quality.exclude_list_path, cfg.quality.exclude_codes)
    seen_hashes: dict[str, str] = {}
    index_rows: list[dict[str, str]] = []
    excludes: list[ExcludeRow] = []
    errors: list[ErrorRow] = []
    kept_images_for_stats: list = []

    config_path = tree["config"] / "pipeline.json"
    config_path.write_text(json.dumps(_serialize_config(cfg), indent=2), encoding="utf-8")

    for abs_path, rel in image_paths:
        kept, excl, err = process_one(
            Path(abs_path),
            rel,
            cfg,
            exclude_map=exclude_map,
            seen_hashes=seen_hashes,
        )
        if err:
            errors.append(err)
            continue
        if excl:
            excludes.append(excl)
            continue
        assert kept is not None
        # Save under processed/images with stable relative layout
        ext = ".png" if (kept.output_format or "PNG") == "PNG" else ".jpg"
        rel_out = kept.relative_path.replace("::", "/").replace("\\", "/")
        dest = tree["images"] / Path(rel_out).with_suffix(ext)
        save_processed_image(kept, dest, cfg.format_conversion)
        row = to_index_row(kept)
        row["processed_path"] = str(dest.relative_to(cfg.processed_root)).replace("\\", "/")
        index_rows.append(row)
        if cfg.normalization.norm_mode.lower() == "dataset":
            # Only retain pixels when dataset stats are required (avoid OOM on 50k+)
            kept_images_for_stats.append(kept.ensure_image().copy())
        # Release pixel buffer from record after save
        kept.image = None

    # Normalization stats artifact
    stats_path = tree["metadata"] / "normalization_stats.json"
    if cfg.normalization.norm_mode.lower() == "dataset" and kept_images_for_stats:
        stats = compute_dataset_stats(kept_images_for_stats, cfg.normalization)
        write_stats_json(stats, stats_path)
    else:
        from modules.normalization import IMAGENET_MEAN, IMAGENET_STD

        write_stats_json(
            {
                "mean": list(cfg.normalization.imagenet_mean or IMAGENET_MEAN),
                "std": list(cfg.normalization.imagenet_std or IMAGENET_STD),
                "norm_mode": cfg.normalization.norm_mode,
                "apply_on_disk": cfg.normalization.apply_on_disk,
            },
            stats_path,
        )

    _write_csv(
        tree["metadata"] / "index.csv",
        index_rows,
        fieldnames=list(index_rows[0].keys()) if index_rows else ["relative_path"],
    )
    _write_csv(
        tree["metadata"] / "exclude_applied.csv",
        [{"relative_path": e.relative_path, "reason_code": e.reason_code, "detail": e.detail} for e in excludes],
        fieldnames=["relative_path", "reason_code", "detail"],
    )
    _write_csv(
        tree["metadata"] / "errors.csv",
        [
            {
                "relative_path": e.relative_path,
                "module_id": e.module_id,
                "reason_code": e.reason_code,
                "message": e.message,
            }
            for e in errors
        ],
        fieldnames=["relative_path", "module_id", "reason_code", "message"],
    )

    summary = {
        "kept": len(index_rows),
        "excluded": len(excludes),
        "errors": len(errors),
        "input_count": len(index_rows) + len(excludes) + len(errors),
        "processed_root": str(cfg.processed_root),
    }
    write_preprocessing_report(
        pipeline_id=cfg.pipeline_id,
        dataset_id=cfg.dataset_id,
        output_id=f"{cfg.dataset_id}_{cfg.pipeline_id}",
        processed_root=Path(cfg.processed_root),
        summary=summary,
        config=_serialize_config(cfg),
        research_question=(
            "How can we improve the cross-generator generalization of "
            "image-based AI face detection models to maintain high accuracy "
            "on unseen generative architectures?"
        ),
        kaggle_pointer=str(getattr(cfg, "kaggle_pointer", "PENDING")),
    )
    return summary


def _write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
