# Module Spec: PPMOD08 — Artifact Removal (Junk Only)

**Purpose:** Remove **non-content** junk that harms training hygiene (EXIF, sidecars), **without** destroying generative forensic traces.  
**Single responsibility:** Metadata/sidecar hygiene.

**Inputs:**
- Image file bytes / Pillow image
- Parameters: `strip_exif`, `remove_sidecar_files`, `forbid_generative_denoising=true`

**Outputs:**
- Cleaned image pixels unchanged except EXIF stripped on save
- Flag `exif_stripped` in metadata

**Dependencies:** Pillow.

**Configuration:** Hard rule: **no** denoising, sharpening, JPEG recompress-for-cleanup, or GAN-artifact “cleaning.” Those would confound detection research.

**Testing:**
- Unit: JPEG with EXIF → output EXIF empty; pixel MSE≈0 vs re-encoded baseline without EXIF
- Unit: attempting a forbidden denoise op in config → configuration error
- Validation module: `PPMOD08V` — asserts `forbid_generative_denoising` cannot be false in production profiles

**Future Extensions:** Optional ICC profile handling; privacy redaction of GPS tags (subset of EXIF strip).

**Validation module:** `PPMOD08V`.
