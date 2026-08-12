"""Template-6 preprocessing report writer."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_preprocessing_report(
    *,
    pipeline_id: str,
    dataset_id: str,
    output_id: str,
    processed_root: Path,
    summary: dict[str, Any],
    config: dict[str, Any],
    research_question: str,
    kaggle_pointer: str = "PENDING",
    dest: Path | None = None,
) -> Path:
    """Write Template-6 report under processed/reports and optional Git sync path."""
    processed_root = Path(processed_root)
    meta = processed_root / "metadata"
    index_csv = meta / "index.csv"
    exclude_csv = meta / "exclude_applied.csv"
    errors_csv = meta / "errors.csv"
    config_json = processed_root / "config" / "pipeline.json"

    index_hash = _sha256_file(index_csv) if index_csv.is_file() else ""
    config_hash = _sha256_file(config_json) if config_json.is_file() else ""

    # Distributions from index if present
    class_dist: Counter[str] = Counter()
    gen_dist: Counter[str] = Counter()
    exclude_reasons: Counter[str] = Counter()
    if index_csv.is_file():
        import csv

        with index_csv.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                class_dist[row.get("class_label") or "unknown"] += 1
                gen_dist[row.get("generator") or "unknown"] += 1
    if exclude_csv.is_file():
        import csv

        with exclude_csv.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                exclude_reasons[row.get("reason_code") or "unknown"] += 1

    ops = config.get("module_sequence") or []
    params_dump = json.dumps(config, indent=2, default=str)

    body = f"""# Preprocessing Report: {pipeline_id}

> Template 6 — Phase D11  
> **Date:** {date.today().isoformat()}  
> **Status:** GENERATED  
> **Research question:** {research_question}

## Identifiers
| Field | Value |
|-------|-------|
| Pipeline ID | `{pipeline_id}` |
| Dataset ID | `{dataset_id}` |
| Output | `{output_id}` |
| Processed root | `{processed_root.as_posix()}` |
| Kaggle pointer | `{kaggle_pointer}` |

## Ordered operations
{' → '.join(ops) if ops else '(see config)'}

## Full parameter dump
```json
{params_dump}
```

## Counts
| Metric | Value |
|--------|------:|
| Input candidates | {summary.get('input_count', summary.get('kept', 0) + summary.get('excluded', 0) + summary.get('errors', 0))} |
| Kept | {summary.get('kept', 0)} |
| Excluded | {summary.get('excluded', 0)} |
| Errors | {summary.get('errors', 0)} |

## Exclusions by reason
| Reason | Count |
|--------|------:|
{chr(10).join(f'| `{k}` | {v} |' for k, v in sorted(exclude_reasons.items())) or '| (none) | 0 |'}

## Output class distribution
| Class | Count |
|-------|------:|
{chr(10).join(f'| `{k}` | {v} |' for k, v in sorted(class_dist.items())) or '| (empty) | 0 |'}

## Output generator distribution
| Generator | Count |
|-----------|------:|
{chr(10).join(f'| `{k}` | {v} |' for k, v in sorted(gen_dist.items())[:50]) or '| (empty) | 0 |'}

## Error summary
See `metadata/errors.csv` ({summary.get('errors', 0)} rows).

## Integrity
| Artifact | SHA-256 |
|----------|---------|
| `metadata/index.csv` | `{index_hash}` |
| `config/pipeline.json` | `{config_hash}` |

## Notes
- Raw data was read-only.
- Processed image bytes live in the data tier (Kaggle); Git holds this report + pointer only.
- New parameters require a **new** `PPxxxx` (never overwrite).
"""

    report_dir = processed_root / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    local_path = report_dir / "preprocessing_report.md"
    local_path.write_text(body, encoding="utf-8")

    if dest is not None:
        dest = Path(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(body, encoding="utf-8")
        return dest
    return local_path
