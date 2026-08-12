# Module Spec: PPMOD09 — Format Conversion

**Purpose:** Convert images to a consistent color mode and on-disk format for training.  
**Single responsibility:** Mode/format conversion only.

**Inputs:**
- Image (any mode)
- Parameters: `force_rgb`, `output_format`, `jpeg_quality`, `png_compress_level`

**Outputs:**
- RGB image saved as PNG or JPEG under processed `images/`
- Record `source_mode`, `output_format` in metadata

**Dependencies:** Pillow.

**Configuration:** Default `force_rgb=true` (handles DS0004 RGBA), `output_format=PNG` for lossless train caches; JPEG allowed for space with recorded quality.

**Testing:**
- Unit: RGBA → RGB (3 channels)
- Unit: L mode → RGB
- Unit: output format matches parameter
- Validation module: `PPMOD09V` — mode is RGB; file extension matches format

**Future Extensions:** WebP; float TIFF for frequency pipelines.

**Validation module:** `PPMOD09V`.
