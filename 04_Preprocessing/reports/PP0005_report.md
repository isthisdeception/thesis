# Preprocessing Report: PP0005

> Template 6 — Phase D11  
> **Date:** 2026-08-30  
> **Status:** GENERATED  
> **Research question:** How can we improve the cross-generator generalization of image-based AI face detection models to maintain high accuracy on unseen generative architectures?

## Identifiers
| Field | Value |
|-------|-------|
| Pipeline ID | `PP0005` |
| Dataset ID | `DS0005` |
| Output | `DS0005_PP0005` |
| Processed root | `/kaggle/working/processed/DS0005_PP0005` |
| Kaggle pointer | `kaggle:isthisdeception/ds0005-pp0005` |

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
  "pipeline_id": "PP0005",
  "dataset_id": "DS0005",
  "target_size": 224,
  "output_format": "PNG",
  "norm_mode": "imagenet",
  "apply_on_disk": false,
  "exclude_list": null,
  "random_seed": 42,
  "purpose": "Bias eval processed (FairFace)"
}
```

## Counts
| Metric | Value |
|--------|------:|
| Input candidates | 97698 |
| Kept | 97698 |
| Excluded | 0 |
| Errors | 0 |

## Exclusions by reason
| Reason | Count |
|--------|------:|
| (none) | 0 |

## Output class distribution
| Class | Count |
|-------|------:|
| `real` | 97698 |

## Output generator distribution
| Generator | Count |
|-----------|------:|
| `none` | 97698 |

## Error summary
See `metadata/errors.csv` (0 rows).

## Integrity
| Artifact | SHA-256 |
|----------|---------|
| `metadata/index.csv` | `4e1126b8dc9ff75dc1017e15ee5d2d136b3afc9ea383d9af3516f407a9bd787c` |
| `config/pipeline.json` | `df11344002f6a7de91f656449ab70a21833774fa6c10aa0aad94a1718d270a38` |

## Notes
- Raw data was read-only.
- Processed image bytes live in the data tier (Kaggle); Git holds this report + pointer only.
- New parameters require a **new** `PPxxxx` (never overwrite).
