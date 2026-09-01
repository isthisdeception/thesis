# Module Spec: PPMOD04 — Cropping

**Purpose:** Crop (and optional margin pad) around a face box or aligned template.  
**Single responsibility:** Spatial crop only.

**Inputs:**
- Image + box from PPMOD02/03
- Parameters: `enabled`, `crop_margin`, `square_crop`

**Outputs:**
- Cropped image
- Crop box written to metadata

**Dependencies:** PPMOD02/03 when enabled.

**Configuration:** Default **disabled** for current packs; when enabled, `crop_margin=0.25` matches FairFace padding practice (DS0005 already padded at source).

**Testing:**
- Unit: square_crop forces equal sides
- Unit: margin expands box and clips to image bounds without crash
- Validation module: `PPMOD04V` — output dimensions > 0; box within original frame

**Future Extensions:** Subject-aware crop for non-face objects (out of thesis scope).

**Validation module:** `PPMOD04V`.
