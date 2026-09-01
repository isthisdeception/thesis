# DS0002 — STEP-022 Issues Plan

**Dataset:** DS0002 DiFF official TEST (PRIMARY-EVAL)  
**Kaggle:** `isthisdeception/ds0002-diff-official-test`  
**Validation run:** 2026-08-11 (Kaggle)  
**Threshold result:** FAIL (`corrupt_rate=0.027918 > 0.001`)  
**Registry:** `Validated=yes` with issues logged (Phase D6 / STEP-022 allows this when a filter plan exists)

## Findings summary

| Issue | Count | Severity |
|-------|------:|----------|
| `CORRUPT_IMAGE` | 1593 | error |
| `DUPLICATE_HASH` | 461 | warning |
| Scanned images | 57059 | — |

Source detail: `03_Datasets/reports/step022/DS0002_validation_report.csv` and `validation_report.csv` (combined).

## Policy (sacred raw)

- **Do not delete or modify** files under Kaggle `raw/DS0002/`.
- Corrupt / duplicate paths are **excluded downstream** in preprocessing (STEP-025), not excised from raw.

## STEP-025 filter plan

1. Build `exclude_list_DS0002.csv` from `Issue Code=CORRUPT_IMAGE` rows in the validation report (relative path + container).
2. Optionally exclude one side of each `DUPLICATE_HASH` pair (keep first occurrence).
3. Processed dataset `DS0002_PPxxxx` reads raw read-only and skips exclude-list paths.
4. Document excluded counts in `preprocessing_report.md`.
5. Re-run a smoke validation over the **processed** tree before splits/training.

## Acceptance for evaluation (E9)

- Primary DiFF metrics are reported on the **filtered** usable test set.
- Paper/methods state: N images excluded as unreadable at intake validation; raw archive unchanged.

## Owner

Dataset Validation / Preprocessing agents + Human approval at STEP-025.
