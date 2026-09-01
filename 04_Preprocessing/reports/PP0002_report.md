# Preprocessing Report: PP0002

> Template 6 — Phase D11  
> **Date:** 2026-08-28  
> **Status:** GENERATED  
> **Research question:** How can we improve the cross-generator generalization of image-based AI face detection models to maintain high accuracy on unseen generative architectures?

## Identifiers
| Field | Value |
|-------|-------|
| Pipeline ID | `PP0002` |
| Dataset ID | `DS0002` |
| Output | `DS0002_PP0002` |
| Processed root | `/kaggle/working/processed/DS0002_PP0002` |
| Kaggle pointer | `kaggle:isthisdeception/ds0002-pp0002` |

## Ordered operations
PPMOD01 → PPMOD10 → PPMOD08 → PPMOD07 → PPMOD09 → PPMOD05 → PPMOD06

## Full parameter dump
```json
{
  "module_sequence": [
    "PPMOD01",
    "PPMOD10",
    "PPMOD08",
    "PPMOD07",
    "PPMOD09",
    "PPMOD05",
    "PPMOD06"
  ],
  "pipeline_id": "PP0002",
  "dataset_id": "DS0002",
  "target_size": 224,
  "output_format": "PNG",
  "norm_mode": "imagenet",
  "apply_on_disk": false,
  "exclude_list": "/kaggle/working/thesis/04_Preprocessing/exclude_lists/exclude_list_DS0002.csv",
  "random_seed": 42,
  "purpose": "Primary eval processed (+ CORRUPT_IMAGE exclude)"
}
```

## Counts
| Metric | Value |
|--------|------:|
| Input candidates | 57060 |
| Kept | 51452 |
| Excluded | 5608 |
| Errors | 0 |

## Exclusions by reason
| Reason | Count |
|--------|------:|
| `EXCLUDED_CORRUPT` | 5607 |
| `UNREADABLE` | 1 |

## Output class distribution
| Class | Count |
|-------|------:|
| `fake` | 51452 |

## Output generator distribution
| Generator | Count |
|-----------|------:|
| `CoDiff` | 4020 |
| `DCFace` | 4629 |
| `DiffFace` | 1576 |
| `DreamBooth` | 3913 |
| `FreeDoM_I` | 2257 |
| `FreeDoM_T` | 2518 |
| `HPS` | 8112 |
| `Imagic` | 4331 |
| `LoRA` | 1592 |
| `Midjourney` | 5647 |
| `SDXL` | 5508 |
| `cycle_diff` | 7349 |

## Error summary
See `metadata/errors.csv` (0 rows).

## Integrity
| Artifact | SHA-256 |
|----------|---------|
| `metadata/index.csv` | `a26afc84363a8b6922a9ff519c3b2bdf31b20b79c2937a2de276bbc7a15bc438` |
| `config/pipeline.json` | `46aec6499ea909f6dc4fe4f51a499774ef813f15530af9ee727fde7046a68dce` |

## Notes
- Raw data was read-only.
- Processed image bytes live in the data tier (Kaggle); Git holds this report + pointer only.
- New parameters require a **new** `PPxxxx` (never overwrite).
