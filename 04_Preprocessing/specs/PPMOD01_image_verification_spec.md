# Module Spec: PPMOD01 — Image Verification

**Purpose:** Confirm each candidate file is a readable image under policy; reject junk/unreadable inputs **without modifying raw**.  
**Single responsibility:** Intake verification only (no resize, no labels).

**Inputs:**
- Raw image path or zip member reference (read-only)
- Parameters: `allowed_extensions`, `reject_macos_junk`, `reject_zero_byte`, `open_verify`

**Outputs:**
- Pass/fail flag + reason code (`OK`, `UNSUPPORTED_FORMAT`, `MACOS_JUNK`, `EMPTY_FILE`, `UNREADABLE`)
- Optional SHA-256 if hashing enabled

**Dependencies:** Pillow; may reuse patterns from `17_Automation/dataset_validation` (import, do not fork logic silently).

**Configuration:** See `design/parameters_catalog.md` → PPMOD01.

**Testing:**
- Unit: reject `._foo.png`, `__MACOSX/...`, zero-byte, truncated JPEG
- Unit: accept valid RGB JPEG/PNG
- Validation module: `validate_image_verification` asserts reason codes are never empty on failure

**Future Extensions:** AVIF/HEIC allow-list; streaming verify for huge zips.

**Validation module:** `PPMOD01V` — property tests on reason-code enum completeness.
