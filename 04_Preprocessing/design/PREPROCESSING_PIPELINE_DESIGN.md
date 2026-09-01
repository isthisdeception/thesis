# Preprocessing Pipeline Design (STEP-025 / Phase D9)

> **Status:** DESIGN APPROVED — implemented in STEP-026 (`modules/`, `pipeline_runner.py`, `tests/`).  
> **Date:** 2026-08-12  
> **Owner:** Preprocessing Agent (Cursor design)  
> **Handbook:** Phase D9–D11; `04_Preprocessing` folder contract  
> **Research question:** Cross-generator generalization of image-based AI face detection  
> **Evidence inputs:** STEP-022 validation, STEP-023 EDA, `dataset_report.md`, DS0002 issues plan

---

## 1. Design principles (binding)

1. **No monolith** — each Phase D9 step is an independent, importable module with its own unit tests.
2. **Raw is sacred** — modules **read** `raw/DSxxxx/` (Kaggle data tier) read-only; **write** only under `processed/DSxxxx_PPxxxx/`.
3. **Every parameter recorded** — values live in pipeline `config` + `preprocessing_registry.csv` + `preprocessing_report.md`.
4. **Fail loudly** — no silent skips; exclusions and errors go to explicit CSVs (§1.7).
5. **Preserve forensic signal** — do **not** denoise/smooth away generative artifacts; “artifact removal” means non-content junk only (EXIF strip, macOS forks, sidecar trash).
6. **Composable profiles** — a `PPxxxx` is an ordered list of module IDs + parameters, not new code.

---

## 2. Findings that shape the design

| Finding | Source | Design impact |
|---------|--------|---------------|
| DS0002 ~2.8% corrupt + duplicates | STEP-022 / `DS0002_issues_plan.md` | `PPMOD01` + `PPMOD07` consume exclude lists |
| macOS `__MACOSX` / `._*` junk in DiFF zips | STEP-023 | Reject in `PPMOD01` / `PPMOD10` |
| DS0002 has **143 identities** | EDA | Metadata must retain `identity`; splits (STEP-027) group by id |
| Resolutions vary (DS0002/DS0004) vs fixed (DS0001/3/5) | EDA/quality | Configurable `target_size` in `PPMOD05` |
| DS0004 RGBA modes | quality_report | `PPMOD09` forces RGB |
| DS0001/3/5 already face crops | EDA | `assume_single_face_crop=true` bypasses heavy detect/align by default |
| Class imbalance DS0004 (1:9) | EDA | Documented; rebalance is **not** a PP module (split/sampler later) |
| Brightness ~0.45 mean across sets | EDA | Optional dataset stats for `PPMOD06`; training may still normalize in FastAI |

---

## 3. Module catalog

| ID | Module | Spec | Default for face packs |
|----|--------|------|------------------------|
| PPMOD01 | Image verification | `specs/PPMOD01_image_verification_spec.md` | **ON** |
| PPMOD02 | Face detection | `specs/PPMOD02_face_detection_spec.md` | OFF if `assume_single_face_crop` |
| PPMOD03 | Face alignment | `specs/PPMOD03_face_alignment_spec.md` | OFF if assume crop |
| PPMOD04 | Cropping | `specs/PPMOD04_cropping_spec.md` | ON when detect/align ran |
| PPMOD05 | Resize | `specs/PPMOD05_resize_spec.md` | **ON** (e.g. 224) |
| PPMOD06 | Normalization | `specs/PPMOD06_normalization_spec.md` | Stats **ON**; apply optional |
| PPMOD07 | Quality filtering | `specs/PPMOD07_quality_filtering_spec.md` | **ON** (exclude lists + thresholds) |
| PPMOD08 | Artifact removal (junk only) | `specs/PPMOD08_artifact_removal_spec.md` | **ON** (EXIF/sidecar) |
| PPMOD09 | Format conversion | `specs/PPMOD09_format_conversion_spec.md` | **ON** → RGB PNG/JPEG |
| PPMOD10 | Metadata extraction | `specs/PPMOD10_metadata_extraction_spec.md` | **ON** |

Each module has a paired **validation** checklist in its `Testing` section (unit + smoke). Shared orchestrator rules are in §5 (not a scientific module — thin glue only).

---

## 4. Planned pipeline profiles (registry stubs — registered at STEP-026/011)

| Pipeline ID | Dataset | Purpose | Module sequence (proposed) |
|-------------|---------|---------|----------------------------|
| PP0001 | DS0001 | Primary train processed | 01→10→08→07→09→05→06 |
| PP0002 | DS0002 | Primary eval processed (+ corrupt exclude) | 01→10→08→07→09→05→06 |
| PP0003 | DS0003 | Quick baseline processed | 01→10→08→07→09→05→06 |
| PP0004 | DS0004 | Frequency supp. processed | 01→10→08→07→09→05→06 |
| PP0005 | DS0005 | Bias eval processed | 01→10→08→07→09→05→06 |

Face detect/align/crop (02–04) remain available for future raw uncropped sources; **not** in default PP0001–PP0005 because current packs are already face-centric.

---

## 5. Orchestration contract (glue, not a monolith)

**Allowed glue responsibilities:** load pipeline YAML → run modules in order → pass `ImageRecord` / paths → write manifests → emit `preprocessing_report.md`.

**Forbidden glue responsibilities:** image math, filtering heuristics, format decisions — those stay inside modules.

### Processed tree layout

```
processed/DSxxxx_PPxxxx/
  images/                 # final tensors/files consumed by training
  metadata/
    index.csv             # one row per kept image (ids, labels, generator, identity, split hints)
    exclude_applied.csv   # paths skipped + reason codes
    errors.csv            # hard failures
    normalization_stats.json
  reports/
    preprocessing_report.md
  config/
    pipeline.yaml         # frozen copy of parameters for this PP run
```

Naming: never overwrite; new params ⇒ new `PPxxxx` (Phase D11).

### `preprocessing_report.md` required contents (Template 6)

- Pipeline ID, Dataset ID, Date, Research question link  
- Ordered operations + **full parameter dump**  
- Input count, kept count, excluded count (by reason)  
- Output class/generator distribution  
- Error summary  
- Checksums of `index.csv` + config hash  
- Pointer to Kaggle processed dataset version (when uploaded)

---

## 6. Master parameter list (must be recorded)

See also `design/parameters_catalog.md`. Summary groups:

| Group | Examples |
|-------|----------|
| IO | `dataset_id`, `raw_root`, `processed_root`, `pipeline_id` |
| Verification | `allowed_extensions`, `reject_macos_junk`, `max_corrupt_retry` |
| Exclude lists | `exclude_list_path` (DS0002 CORRUPT_IMAGE), `dedupe_policy` |
| Face (optional) | `assume_single_face_crop`, `detector_name`, `min_face_confidence`, `align_method`, `crop_margin` |
| Geometry | `target_size`, `interpolation`, `keep_aspect`, `pad_value` |
| Quality | `min_side`, `max_side`, `min_file_bytes`, `blur_var_threshold` (if used) |
| Format | `output_format`, `jpeg_quality`, `force_rgb` |
| Normalization | `norm_mode` (`imagenet`\|`dataset`\|`none`), `apply_on_disk`, channel means/stds |
| Repro | `random_seed`, `library_versions`, `git_commit` |

All appear in `pipeline.yaml` and registry `Parameters` cell (JSON or semicolon key=value).

---

## 7. Data-flow diagram

```
raw/DSxxxx (read-only)
    │
    ▼
PPMOD01 verify ──► reject junk/unreadable
    │
    ▼
PPMOD10 metadata ──► labels, generator, identity
    │
    ▼
PPMOD08 junk artifact strip (EXIF/sidecar)
    │
    ▼
PPMOD07 quality filter + exclude lists
    │
    ├─ optional PPMOD02→03→04 (uncropped sources only)
    │
    ▼
PPMOD09 format → RGB
    │
    ▼
PPMOD05 resize
    │
    ▼
PPMOD06 stats (+ optional apply)
    │
    ▼
processed/DSxxxx_PPxxxx/
```

---

## 8. Implementation handoff (STEP-026)

Antigravity must:

1. Implement each `PPMOD##` as `04_Preprocessing/modules/<name>.py` (snake_case, type hints, docstrings).
2. Add `tests/test_ppmod##_*.py` per Testing section.
3. Provide thin `pipeline_runner.py` that only sequences modules.
4. Never modify raw; never commit image bytes to Git.
5. Register first successful runs in `preprocessing_registry.csv`.

---

## 9. Verification (STEP-025 DoD)

- [x] Ten independent module specs (no monolith)
- [x] Validation/testing specified per module
- [x] Parameter catalog enumerated for config/registry
- [x] `processed/DSxxxx_PPxxxx` layout + report contract defined
- [x] Raw read-only enforced in design

**Next:** STEP-026 — implement modules against these specs.
