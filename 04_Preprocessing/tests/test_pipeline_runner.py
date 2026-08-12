"""Smoke test — thin pipeline_runner glue (no monolith math)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from pipeline_runner import PipelineConfig, run_pipeline
from modules.metadata_extraction import MetadataExtractionParams


def test_run_pipeline_writes_processed_only(tmp_path: Path) -> None:
    raw = tmp_path / "raw" / "DS0003"
    processed = tmp_path / "processed" / "DS0003_PP0003"
    raw.mkdir(parents=True)
    img_rel = "train/fake/x.png"
    abs_path = raw / img_rel
    abs_path.parent.mkdir(parents=True)
    Image.new("RGB", (128, 128), color=(20, 40, 60)).save(abs_path)

    cfg = PipelineConfig(
        pipeline_id="PP0003",
        dataset_id="DS0003",
        raw_root=raw,
        processed_root=processed,
        metadata=MetadataExtractionParams(require_class_label=True, require_identity=False),
    )
    summary = run_pipeline([(abs_path, img_rel)], cfg)
    assert summary["kept"] == 1
    assert summary["errors"] == 0
    assert (processed / "metadata" / "index.csv").is_file()
    assert (processed / "config" / "pipeline.json").is_file()
    assert (processed / "metadata" / "normalization_stats.json").is_file()
    # raw untouched (same mtime content still exists)
    assert abs_path.is_file()
    assert list((processed / "images").rglob("*.png"))
