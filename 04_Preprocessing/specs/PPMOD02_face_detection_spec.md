# Module Spec: PPMOD02 — Face Detection

**Purpose:** Locate face bounding box(es) in an image when the source is **not** already a tight face crop.  
**Single responsibility:** Detection boxes + scores only.

**Inputs:**
- RGB image (in-memory or path under processed staging — never write into raw)
- Parameters: `enabled`, `assume_single_face_crop`, `detector_name`, `min_face_confidence`, `max_faces_keep`, `fail_if_no_face`

**Outputs:**
- List of boxes `(x1,y1,x2,y2,score)`; selected primary face index
- If `assume_single_face_crop=true` and `enabled=false`: passthrough sentinel `FULL_FRAME`

**Dependencies:** Chosen detector library (pinned in environment lock at STEP-026/030).

**Configuration:** Default **disabled** for DS0001–DS0005 (already face-centric). Enable only for future uncropped sources.

**Testing:**
- Unit: synthetic image with known box → IoU ≥ threshold
- Unit: `assume_single_face_crop` short-circuit returns FULL_FRAME without loading detector
- Validation module: `PPMOD02V` — box coordinates within image bounds; score in [0,1]

**Future Extensions:** Multi-face forensic cases; landmark outputs shared with alignment.

**Validation module:** `PPMOD02V`.
