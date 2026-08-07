# STEP-022 / Phase D6 — Dataset Validation Module Spec

**Module path:** `17_Automation/dataset_validation/`  
**Reads:** raw dataset roots (directories and/or ZIP archives) **read-only**  
**Writes:** `validation_report.csv`, `quality_report.csv`, appends sample rows to `integrity_report.csv`

## Checks (Phase D6)

| Check | Issue codes | Report |
|-------|-------------|--------|
| Unreadable / corrupt image | `CORRUPT_IMAGE` | validation |
| Unsupported format | `UNSUPPORTED_FORMAT` | validation |
| Invalid / empty filename | `INVALID_FILENAME` | validation |
| Missing label / metadata row | `MISSING_LABEL` | validation |
| Label path missing on disk | `MISSING_FILE_FOR_LABEL` | validation |
| Duplicate content (SHA-256) | `DUPLICATE_HASH` | validation |
| Zero-byte file | `EMPTY_FILE` | validation |
| Channel / mode anomalies | `UNEXPECTED_MODE` | validation (info) |

## Quality aggregates (`quality_report.csv`)

Per dataset: image counts by split/label/generator (when known), corrupt count/rate, duplicate group count, resolution min/max/mean, aspect-ratio min/max/mean, format histogram, channel-mode histogram.

## Acceptance thresholds (default)

| Metric | Pass if |
|--------|---------|
| Corrupt rate | ≤ 0.1% of readable candidates |
| Empty files | = 0 |
| Missing labels (when labels required) | = 0 |
| Duplicate exact-hash pairs | logged; **not** auto-fail (filter in preprocessing) |

If thresholds fail: keep `Validated=no`, log plan; do **not** modify raw.

## Determinism

- Fixed walk order (sorted paths)
- Duplicate detection uses full-file SHA-256
- Optional `--max-images` for smoke tests (non-DoD); full run for DoD

## Kaggle dataset attach map

| ID | Input slug |
|----|------------|
| DS0001 | `isthisdeception/ds0001-artifact-face-subset` |
| DS0002 | `isthisdeception/ds0002-diff-official-test` |
| DS0003 | `xhlulu/140k-real-and-fake-faces` |
| DS0004 | `isthisdeception/ds0004-synthbuster` |
| DS0005 | `isthisdeception/ds0005-fairface` |
