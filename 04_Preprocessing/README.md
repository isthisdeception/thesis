# 04_Preprocessing

**Purpose:** Modular, versioned preprocessing pipelines (PPxxxx).

## Phase Status
- **STEP-025 — Pipeline Design (Phase D9 design):** `COMPLETE` (2026-08-12)
  - Design: `design/PREPROCESSING_PIPELINE_DESIGN.md`
  - Parameters: `design/parameters_catalog.md`
  - Module specs: `specs/PPMOD01` … `PPMOD10`
- **STEP-026 — Implement modules:** `COMPLETE` (2026-08-12)
  - Package: `modules/` (PPMOD01–10) + `validation.py`
  - Glue: `pipeline_runner.py` (sequence only — no image math)
  - Tests: `tests/` — **34 passed**
- **STEP-027 — Register pipeline & generate processed:** `NEXT`

## Package layout

```
04_Preprocessing/
  modules/
    image_verification.py   # PPMOD01
    face_detection.py        # PPMOD02
    face_alignment.py        # PPMOD03
    cropping.py              # PPMOD04
    resize.py                # PPMOD05
    normalization.py         # PPMOD06
    quality_filtering.py     # PPMOD07
    artifact_removal.py      # PPMOD08
    format_conversion.py     # PPMOD09
    metadata_extraction.py   # PPMOD10
    types.py
    validation.py            # PPMOD01V–10V
  pipeline_runner.py
  tests/
```

## Rules
- **No monolith** — one module per Phase D9 step; parameters injected.
- **Raw read-only** — writes only under `processed/DSxxxx_PPxxxx/`.
- **Fail loudly** — `ModuleError` / exclude CSVs; never silent skips.
- **Artifact removal** = EXIF/sidecar only (`forbid_generative_denoising=true`).

## Run unit tests

```bash
cd 04_Preprocessing
python -m pytest tests/ -v
```

## Owner
Preprocessing Agent

## Related Folders
`03_Datasets`, `17_Automation/dataset_eda` (label inference reuse)

> *This folder follows the canonical repository hygiene and naming rules defined in `MASTER_RESEARCH_OPERATING_SYSTEM.md`.*
