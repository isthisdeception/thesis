# Module Spec: PPMOD07 — Quality Filtering

**Purpose:** Exclude low-quality or known-bad images using thresholds and **explicit exclude lists** (DS0002 corrupt plan).  
**Single responsibility:** Keep/exclude decision + reason codes.

**Inputs:**
- Verified image path + optional prior metadata
- `exclude_list_path` (CSV of relative paths + issue codes from STEP-022)
- Parameters: size/byte/brightness/blur thresholds, `dedupe_policy`

**Outputs:**
- Keep boolean + reason (`EXCLUDED_CORRUPT`, `EXCLUDED_DUPLICATE`, `EXCLUDED_TOO_SMALL`, …)
- Rows appended to `exclude_applied.csv`

**Dependencies:** PPMOD01 outputs; STEP-022 validation CSV for DS0002.

**Configuration:** For PP0002/DS0002, `exclude_list_path` **required** pointing at corrupt-path export derived from `validation_report.csv` (`Issue Code=CORRUPT_IMAGE`). Dedupe optional (`keep_first`).

**Testing:**
- Unit: path on exclude list → excluded with correct code
- Unit: below `min_side` → excluded
- Unit: clean image → kept
- Validation module: `PPMOD07V` — every exclusion has non-empty reason; counts reconcile with report

**Future Extensions:** Learned quality scores; generator-specific thresholds.

**Validation module:** `PPMOD07V`.
