# Module Spec: PPMOD03 — Face Alignment

**Purpose:** Geometric alignment of a detected face (eyes/landmarks) to a canonical template.  
**Single responsibility:** Alignment transform only.

**Inputs:**
- Image + face box / landmarks from PPMOD02
- Parameters: `enabled`, `align_method`, `output_template_size`

**Outputs:**
- Aligned face image (same color mode as input)
- Affine matrix recorded in metadata sidecar fields

**Dependencies:** PPMOD02 outputs when enabled; NumPy/Pillow or detector landmark API.

**Configuration:** Default **disabled** when `assume_single_face_crop=true`.

**Testing:**
- Unit: known landmark set → eyes approximately horizontal after align
- Unit: disabled path returns input unchanged
- Validation module: `PPMOD03V` — output size equals `output_template_size` when enabled; matrix finite

**Future Extensions:** 3D alignment; detector-specific landmark schemas.

**Validation module:** `PPMOD03V`.
