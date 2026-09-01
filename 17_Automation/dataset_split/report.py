"""Write split artifacts to 03_Datasets/splits/."""

from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path
from typing import Any

from .core import SplitConfig, assert_no_leakage, fingerprint, summarize


def write_split_artifacts(
    cfg: SplitConfig,
    rows: list[dict[str, str]],
    assignments: dict[str, str],
    leakage: dict[str, Any],
    out_root: Path,
) -> Path:
    split_dir = out_root / f"{cfg.output_id}_{cfg.split_id}"
    split_dir.mkdir(parents=True, exist_ok=True)

    summary = summarize(assignments, rows)
    config = {
        "split_id": cfg.split_id,
        "output_id": cfg.output_id,
        "dataset_id": cfg.dataset_id,
        "pipeline_id": cfg.pipeline_id,
        "scheme": cfg.scheme,
        "seed": cfg.seed,
        "ratios": list(cfg.ratios),
        "group_by": cfg.group_by,
        "held_out_generators": cfg.held_out_generators,
        "official_test_column": cfg.official_test_column,
        "official_test_values": cfg.official_test_values,
        "train_val_ratio": list(cfg.train_val_ratio),
        "notes": cfg.notes,
        "fingerprint_sha256": fingerprint(assignments),
        "date": date.today().isoformat(),
        "summary": summary,
        "leakage_check": leakage,
    }
    (split_dir / "split_config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    (split_dir / "leakage_check.json").write_text(json.dumps(leakage, indent=2), encoding="utf-8")

    row_map = {r["processed_path"]: r for r in rows}
    fieldnames = [
        "processed_path",
        "relative_path",
        "partition",
        "class_label",
        "generator",
        "identity",
        "content_hash",
    ]
    with (split_dir / "assignments.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for path in sorted(assignments):
            row = row_map[path]
            writer.writerow(
                {
                    "processed_path": path,
                    "relative_path": row.get("relative_path", ""),
                    "partition": assignments[path],
                    "class_label": row.get("class_label", ""),
                    "generator": row.get("generator", ""),
                    "identity": row.get("identity", ""),
                    "content_hash": row.get("content_hash", ""),
                }
            )

    for part in ("train", "val", "test"):
        part_rows = [p for p, v in assignments.items() if v == part]
        if not part_rows:
            continue
        with (split_dir / f"{part}.csv").open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["processed_path"])
            for p in sorted(part_rows):
                writer.writerow([p])

    return split_dir


def write_split_report(
    results: list[dict[str, Any]],
    dest: Path,
) -> None:
    lines = [
        "# Split Report (STEP-028 / Phase D12)",
        "",
        f"> Generated: {date.today().isoformat()}",
        "",
        "## Summary",
        "",
        "| Split ID | Output | Scheme | Train | Val | Test | Leakage | Fingerprint |",
        "|----------|--------|--------|------:|----:|-----:|---------|-------------|",
    ]
    for r in results:
        c = r["summary"]["counts"]
        leak = "PASS" if r["leakage"]["passed"] else "FAIL"
        lines.append(
            f"| {r['split_id']} | {r['output_id']} | {r['scheme']} | "
            f"{c.get('train', 0)} | {c.get('val', 0)} | {c.get('test', 0)} | "
            f"{leak} | `{r['fingerprint'][:16]}…` |"
        )
    lines.extend(["", "## Per-split notes", ""])
    for r in results:
        lines.append(f"### {r['output_id']}_{r['split_id']}")
        lines.append(f"- Scheme: `{r['scheme']}` (seed={r['seed']})")
        lines.append(f"- Notes: {r['notes']}")
        if r["leakage"]["issues"]:
            lines.append("- Leakage issues:")
            for issue in r["leakage"]["issues"][:10]:
                lines.append(f"  - {issue}")
        lines.append("")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
