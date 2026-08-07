"""Orchestrate Phase D6 validation and write report CSVs."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Sequence

from .adapters import DatasetLayout, debug_layout, discover_layout
from .schemas import (
    DEFAULT_THRESHOLDS,
    INTEGRITY_COLUMNS,
    QUALITY_COLUMNS,
    VALIDATION_COLUMNS,
)
from .scanner import (
    ScanAccumulator,
    check_label_csv,
    finalize_duplicates,
    scan_directory,
    scan_zip,
)


def _mean(xs: list[float] | list[int]) -> float:
    return float(mean(xs)) if xs else 0.0


def build_quality_rows(dataset_id: str, acc: ScanAccumulator, layout: DatasetLayout) -> list[dict]:
    dup_groups = sum(1 for paths in acc.hash_to_paths.values() if len(paths) > 1)
    corrupt_rate = (acc.corrupt / acc.scanned_images) if acc.scanned_images else 0.0
    rows = [
        {"Dataset ID": dataset_id, "Metric": "scanned_images", "Value": acc.scanned_images, "Notes": ""},
        {"Dataset ID": dataset_id, "Metric": "corrupt_count", "Value": acc.corrupt, "Notes": ""},
        {
            "Dataset ID": dataset_id,
            "Metric": "corrupt_rate",
            "Value": f"{corrupt_rate:.6f}",
            "Notes": "corrupt / scanned_images",
        },
        {"Dataset ID": dataset_id, "Metric": "empty_files", "Value": acc.empty, "Notes": ""},
        {"Dataset ID": dataset_id, "Metric": "unsupported_format", "Value": acc.unsupported, "Notes": ""},
        {"Dataset ID": dataset_id, "Metric": "duplicate_hash_groups", "Value": dup_groups, "Notes": ""},
        {
            "Dataset ID": dataset_id,
            "Metric": "width_min",
            "Value": min(acc.widths) if acc.widths else "",
            "Notes": "",
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "width_max",
            "Value": max(acc.widths) if acc.widths else "",
            "Notes": "",
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "width_mean",
            "Value": f"{_mean(acc.widths):.2f}" if acc.widths else "",
            "Notes": "",
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "height_min",
            "Value": min(acc.heights) if acc.heights else "",
            "Notes": "",
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "height_max",
            "Value": max(acc.heights) if acc.heights else "",
            "Notes": "",
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "height_mean",
            "Value": f"{_mean(acc.heights):.2f}" if acc.heights else "",
            "Notes": "",
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "aspect_ratio_min",
            "Value": f"{min(acc.aspects):.4f}" if acc.aspects else "",
            "Notes": "width/height",
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "aspect_ratio_max",
            "Value": f"{max(acc.aspects):.4f}" if acc.aspects else "",
            "Notes": "width/height",
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "aspect_ratio_mean",
            "Value": f"{_mean(acc.aspects):.4f}" if acc.aspects else "",
            "Notes": "width/height",
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "format_histogram",
            "Value": json.dumps(dict(acc.formats)),
            "Notes": "",
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "mode_histogram",
            "Value": json.dumps(dict(acc.modes)),
            "Notes": "",
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "archives_scanned",
            "Value": len(layout.archives),
            "Notes": ",".join(p.name for p in layout.archives[:20]),
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "roots_scanned",
            "Value": len(layout.roots),
            "Notes": ";".join(str(p) for p in layout.roots[:10]),
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "label_csvs",
            "Value": len(layout.label_csvs),
            "Notes": ",".join(p.name for p in layout.label_csvs),
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "built_utc",
            "Value": datetime.now(timezone.utc).isoformat(),
            "Notes": "Phase D6",
        },
    ]
    return rows


def evaluate_thresholds(
    dataset_id: str,
    acc: ScanAccumulator,
    findings_rows: list[dict],
    thresholds: dict,
) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    scanned = max(acc.scanned_images, 1)
    corrupt_rate = acc.corrupt / scanned if acc.scanned_images else (1.0 if acc.corrupt else 0.0)
    if acc.scanned_images == 0:
        reasons.append("no_images_scanned")
    if corrupt_rate > thresholds["max_corrupt_rate"]:
        reasons.append(f"corrupt_rate={corrupt_rate:.6f}>{thresholds['max_corrupt_rate']}")
    if acc.empty > thresholds["max_empty_files"]:
        reasons.append(f"empty_files={acc.empty}")
    missing_labels = sum(1 for r in findings_rows if r["Issue Code"] == "MISSING_LABEL")
    missing_files = sum(1 for r in findings_rows if r["Issue Code"] == "MISSING_FILE_FOR_LABEL")
    if missing_labels > thresholds["max_missing_labels"]:
        reasons.append(f"missing_labels={missing_labels}")
    if missing_files > thresholds["max_missing_files_for_labels"]:
        reasons.append(f"missing_files_for_labels={missing_files}")
    return (len(reasons) == 0 and acc.scanned_images > 0), reasons


def validate_dataset(
    dataset_id: str,
    search_roots: Sequence[Path],
    *,
    max_images: int | None = None,
    integrity_sample_every: int = 500,
    thresholds: dict | None = None,
) -> dict:
    thresholds = thresholds or DEFAULT_THRESHOLDS
    layout = discover_layout(dataset_id, list(search_roots))
    acc = ScanAccumulator()

    # Prefer directories if present; else scan archives
    if layout.roots:
        for root in layout.roots:
            scan_directory(
                dataset_id,
                root,
                acc,
                max_images=max_images,
                integrity_sample_every=integrity_sample_every,
            )
            if max_images is not None and acc.scanned_images >= max_images:
                break
    if (not layout.roots or acc.scanned_images == 0) and layout.archives:
        for zp in layout.archives:
            scan_zip(
                dataset_id,
                zp,
                acc,
                max_images=max_images,
                integrity_sample_every=integrity_sample_every,
            )
            if max_images is not None and acc.scanned_images >= max_images:
                break
    elif layout.archives and dataset_id in {"DS0002", "DS0004"}:
        # Always scan archives for zip-packaged datasets even if roots exist
        for zp in layout.archives:
            if max_images is not None and acc.scanned_images >= max_images:
                break
            scan_zip(
                dataset_id,
                zp,
                acc,
                max_images=max_images,
                integrity_sample_every=integrity_sample_every,
            )

    finalize_duplicates(dataset_id, acc)

    available_relpaths: set[str] = set()
    for paths in acc.hash_to_paths.values():
        for p in paths:
            available_relpaths.add(p)
            if "::" in p:
                inner = p.split("::", 1)[1]
                available_relpaths.add(inner)
                available_relpaths.add(Path(inner).name)
            available_relpaths.add(Path(p).name)

    for csv_path in layout.label_csvs:
        # Only enforce file-presence vs labels on full scans (smoke caps would false-fail).
        check_label_csv(
            dataset_id,
            csv_path,
            acc,
            available_relpaths=None
            if max_images is not None
            else (available_relpaths if available_relpaths else None),
        )

    findings_rows = [
        {
            "Dataset ID": f.dataset_id,
            "Relative Path": f.relative_path,
            "Issue Code": f.issue_code,
            "Issue Detail": f.issue_detail,
            "Severity": f.severity,
            "Source Container": f.source_container,
        }
        for f in acc.findings
    ]
    quality_rows = build_quality_rows(dataset_id, acc, layout)
    passed, reasons = evaluate_thresholds(dataset_id, acc, findings_rows, thresholds)
    quality_rows.append(
        {
            "Dataset ID": dataset_id,
            "Metric": "threshold_pass",
            "Value": "yes" if passed else "no",
            "Notes": ";".join(reasons) if reasons else "ok",
        }
    )

    return {
        "dataset_id": dataset_id,
        "layout": layout,
        "findings": findings_rows,
        "quality": quality_rows,
        "integrity_samples": acc.integrity_rows,
        "passed": passed,
        "fail_reasons": reasons,
        "scanned_images": acc.scanned_images,
    }


def write_csv(path: Path, columns: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns)
        w.writeheader()
        for row in rows:
            w.writerow({c: row.get(c, "") for c in columns})


def merge_integrity(existing: Path, new_rows: list[dict]) -> list[dict]:
    rows: list[dict] = []
    if existing.is_file():
        with existing.open(newline="", encoding="utf-8") as f:
            rows.extend(csv.DictReader(f))
    # drop previous sample_ok rows for datasets we are rewriting samples for
    ds_ids = {r["Dataset ID"] for r in new_rows}
    rows = [
        r
        for r in rows
        if not (
            r.get("Dataset ID") in ds_ids
            and r.get("Integrity Status") == "sample_ok"
        )
    ]
    rows.extend(new_rows)
    return rows


def run_validation(
    dataset_ids: Sequence[str],
    search_roots: Sequence[Path],
    output_dir: Path,
    *,
    max_images: int | None = None,
    integrity_sample_every: int = 500,
    thresholds: dict | None = None,
) -> dict:
    """Validate multiple datasets; write combined reports into output_dir."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_findings: list[dict] = []
    all_quality: list[dict] = []
    all_integrity_samples: list[dict] = []
    summary: dict[str, dict] = {}

    for ds in dataset_ids:
        print(f"[STEP-022] Validating {ds} ...", flush=True)
        result = validate_dataset(
            ds,
            search_roots,
            max_images=max_images,
            integrity_sample_every=integrity_sample_every,
            thresholds=thresholds,
        )
        all_findings.extend(result["findings"])
        all_quality.extend(result["quality"])
        all_integrity_samples.extend(result["integrity_samples"])
        summary[ds] = {
            "passed": result["passed"],
            "fail_reasons": result["fail_reasons"],
            "scanned_images": result["scanned_images"],
            "archives": [str(p) for p in result["layout"].archives],
            "roots": [str(p) for p in result["layout"].roots],
            "layout_notes": result["layout"].notes,
        }
        if result["scanned_images"] == 0:
            print(f"  DEBUG {result['layout'].notes}", flush=True)
            print(
                f"  DEBUG archives={summary[ds]['archives']} roots={summary[ds]['roots']}",
                flush=True,
            )
        print(
            f"  scanned={result['scanned_images']} passed={result['passed']} "
            f"findings={len(result['findings'])}",
            flush=True,
        )

    write_csv(output_dir / "validation_report.csv", VALIDATION_COLUMNS, all_findings)
    write_csv(output_dir / "quality_report.csv", QUALITY_COLUMNS, all_quality)

    integrity_path = output_dir / "integrity_report.csv"
    # Prefer merging with repo integrity if present beside output
    merged = merge_integrity(integrity_path, all_integrity_samples)
    # If merge target empty and repo path provided via env-less default: still write samples + keep header
    if not merged and all_integrity_samples:
        merged = all_integrity_samples
    write_csv(integrity_path, INTEGRITY_COLUMNS, merged)

    summary_path = output_dir / "validation_summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "built_utc": datetime.now(timezone.utc).isoformat(),
                "dataset_ids": list(dataset_ids),
                "max_images": max_images,
                "results": summary,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return summary


__all__ = ["run_validation", "validate_dataset", "DEFAULT_THRESHOLDS"]
