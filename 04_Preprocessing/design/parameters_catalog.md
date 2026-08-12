# Preprocessing Parameters Catalog (STEP-025)

> Every parameter below **must** be recorded in `pipeline.yaml`, `preprocessing_registry.csv`, and `preprocessing_report.md` when a `PPxxxx` runs.  
> Types are implementation hints for STEP-026.

## Global / IO

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `pipeline_id` | str | required | e.g. `PP0001` |
| `dataset_id` | str | required | `DSxxxx` |
| `raw_root` | path | required | Kaggle raw mount (read-only) |
| `processed_root` | path | required | `processed/DSxxxx_PPxxxx/` |
| `random_seed` | int | `42` | Deterministic sampling/ties |
| `git_commit` | str | auto | Recorded at run time |
| `pillow_version` | str | auto | Environment lock |
| `numpy_version` | str | auto | Environment lock |

## PPMOD01 — Image verification

| Parameter | Type | Default |
|-----------|------|---------|
| `allowed_extensions` | list[str] | `[.jpg,.jpeg,.png,.bmp,.webp]` |
| `reject_macos_junk` | bool | `true` |
| `reject_zero_byte` | bool | `true` |
| `open_verify` | bool | `true` | Pillow open+verify |
| `hash_algorithm` | str | `sha256` | Optional content hash for dedupe later |

## PPMOD02 — Face detection

| Parameter | Type | Default |
|-----------|------|---------|
| `enabled` | bool | `false` |
| `assume_single_face_crop` | bool | `true` |
| `detector_name` | str | `retinaface` \| `mtcnn` \| `opencv_haar` |
| `min_face_confidence` | float | `0.9` |
| `max_faces_keep` | int | `1` | Largest/highest-score face |
| `fail_if_no_face` | bool | `true` when enabled |

## PPMOD03 — Face alignment

| Parameter | Type | Default |
|-----------|------|---------|
| `enabled` | bool | `false` |
| `align_method` | str | `five_point` \| `eyes_horizontal` |
| `output_template_size` | int | `112` | Intermediate align canvas |

## PPMOD04 — Cropping

| Parameter | Type | Default |
|-----------|------|---------|
| `enabled` | bool | `false` |
| `crop_margin` | float | `0.25` | Relative to face box (FairFace-like) |
| `square_crop` | bool | `true` |

## PPMOD05 — Resize

| Parameter | Type | Default |
|-----------|------|---------|
| `target_size` | int\|[h,w] | `224` |
| `interpolation` | str | `bilinear` |
| `keep_aspect` | bool | `false` | If true, letterbox |
| `pad_value` | int | `0` |

## PPMOD06 — Normalization

| Parameter | Type | Default |
|-----------|------|---------|
| `norm_mode` | str | `imagenet` |
| `imagenet_mean` | [f,f,f] | `[0.485,0.456,0.406]` |
| `imagenet_std` | [f,f,f] | `[0.229,0.224,0.225]` |
| `dataset_stats_path` | path\|null | computed → `normalization_stats.json` |
| `apply_on_disk` | bool | `false` | Prefer stats for FastAI; optional float tensors |
| `stats_sample_n` | int | `3000` | If computing dataset stats |

## PPMOD07 — Quality filtering

| Parameter | Type | Default |
|-----------|------|---------|
| `exclude_list_path` | path\|null | e.g. DS0002 corrupt CSV |
| `exclude_codes` | list[str] | `[CORRUPT_IMAGE]` |
| `dedupe_policy` | str | `keep_first` \| `exclude_all_dupes` \| `off` |
| `min_side` | int | `64` |
| `max_side` | int | `4096` |
| `min_file_bytes` | int | `100` |
| `max_file_bytes` | int\|null | `null` |
| `blur_var_threshold` | float\|null | `null` (disabled unless set) |
| `min_brightness` | float\|null | `null` |
| `max_brightness` | float\|null | `null` |

## PPMOD08 — Artifact removal (junk only)

| Parameter | Type | Default |
|-----------|------|---------|
| `strip_exif` | bool | `true` |
| `drop_alpha` | bool | `true` | Via RGB convert in MOD09 if preferred |
| `remove_sidecar_files` | bool | `true` | Do not copy `.txt`/`.json` sidecars unless metadata module needs them |
| `forbid_generative_denoising` | bool | `true` | Hard constraint |

## PPMOD09 — Format conversion

| Parameter | Type | Default |
|-----------|------|---------|
| `force_rgb` | bool | `true` |
| `output_format` | str | `PNG` \| `JPEG` |
| `jpeg_quality` | int | `95` |
| `png_compress_level` | int | `3` |

## PPMOD10 — Metadata extraction

| Parameter | Type | Default |
|-----------|------|---------|
| `label_source` | str | `auto` | path rules / CSV / folder |
| `require_class_label` | bool | `true` for DS0001/3/4 |
| `require_generator` | bool | `true` when available |
| `require_identity` | bool | `true` for DS0002 |
| `fairface_label_csvs` | list[path] | DS0005 train/val labels |
| `metadata_csv_path` | path\|null | DS0001 `metadata.csv` |

## Derived outputs (always written)

| Artifact | Description |
|----------|-------------|
| `metadata/index.csv` | Kept images + attributes |
| `metadata/exclude_applied.csv` | Skips + reason codes |
| `metadata/errors.csv` | Hard failures |
| `metadata/normalization_stats.json` | Channel mean/std if computed |
| `config/pipeline.yaml` | Frozen parameters |
| `reports/preprocessing_report.md` | Template 6 instance |
