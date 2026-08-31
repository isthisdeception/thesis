# Preprocessing Report: PP0003

> Template 6 — Phase D11  
> **Date:** 2026-08-19  
> **Status:** GENERATED  
> **Research question:** How can we improve the cross-generator generalization of image-based AI face detection models to maintain high accuracy on unseen generative architectures?

## Identifiers
| Field | Value |
|-------|-------|
| Pipeline ID | `PP0003` |
| Dataset ID | `DS0003` |
| Output | `DS0003_PP0003` |
| Processed root | `/kaggle/working/processed/DS0003_PP0003` |
| Kaggle pointer | `kaggle:isthisdeception/ds0003-pp0003` |

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
  "pipeline_id": "PP0003",
  "dataset_id": "DS0003",
  "target_size": 224,
  "output_format": "PNG",
  "norm_mode": "imagenet",
  "apply_on_disk": false,
  "exclude_list": null,
  "random_seed": 42,
  "purpose": "Quick baseline processed"
}
```

## Counts
| Metric | Value |
|--------|------:|
| Input candidates | 140000 |
| Kept | 140000 |
| Excluded | 0 |
| Errors | 0 |

## Exclusions by reason
| Reason | Count |
|--------|------:|
| (none) | 0 |

## Output class distribution
| Class | Count |
|-------|------:|
| `fake` | 70000 |
| `real` | 70000 |

## Output generator distribution
| Generator | Count |
|-----------|------:|
| `none` | 70000 |
| `stylegan` | 70000 |

## Error summary
See `metadata/errors.csv` (0 rows).

## Integrity
| Artifact | SHA-256 |
|----------|---------|
| `metadata/index.csv` | `06535165189def85406864a234284a15713f3577e7d2b0b2e2cfe3c3af4ce044` |
| `config/pipeline.json` | `665c4061fa5e4b0bb74d8f21567cf55c098c5e33c413bae1663154a385291258` |

## Notes
- Raw data was read-only.
- Processed image bytes live in the data tier (Kaggle); Git holds this report + pointer only.
- New parameters require a **new** `PPxxxx` (never overwrite).
