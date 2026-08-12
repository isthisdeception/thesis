# Module Spec: PPMOD05 — Resize

**Purpose:** Resize images to a fixed training/eval resolution.  
**Single responsibility:** Geometric resize / letterbox only.

**Inputs:**
- RGB image
- Parameters: `target_size`, `interpolation`, `keep_aspect`, `pad_value`

**Outputs:**
- Resized image of exact target HxW
- Record original and new shapes in metadata

**Dependencies:** Pillow or torchvision; interpolation name mapped explicitly.

**Configuration:** Default `target_size=224`, `keep_aspect=false` (stretch) for detector backbones; letterbox optional for frequency studies (DS0004).

**Testing:**
- Unit: 256×256 → 224×224
- Unit: letterbox path preserves aspect and pads with `pad_value`
- Validation module: `PPMOD05V` — output size == target; dtype/mode unchanged except size

**Future Extensions:** Multi-scale pyramids; random resized crop (augmentation — belongs in training config, not PP).

**Validation module:** `PPMOD05V`.
