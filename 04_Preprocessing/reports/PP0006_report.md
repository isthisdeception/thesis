# Preprocessing Report: PP0006

> Template 6 — Phase D11  
> **Date:** 2026-08-31  
> **Status:** GENERATED  
> **Research question:** How can we improve the cross-generator generalization of image-based AI face detection models to maintain high accuracy on unseen generative architectures?

## Identifiers
| Field | Value |
|-------|-------|
| Pipeline ID | `PP0006` |
| Dataset ID | `DS0004` |
| Output | `DS0004_PP0006` |
| Processed root | `/kaggle/working/processed/DS0004_PP0006` |
| Kaggle pointer | `kaggle:isthisdeception/ds0004-pp0006` |

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
  "pipeline_id": "PP0006",
  "dataset_id": "DS0004",
  "target_size": 224,
  "output_format": "PNG",
  "norm_mode": "imagenet",
  "apply_on_disk": false,
  "exclude_list": null,
  "random_seed": 42,
  "purpose": "Frequency supplementary processed (RAISE max_side fix)"
}
```

## Counts
| Metric | Value |
|--------|------:|
| Input candidates | 9999 |
| Kept | 9999 |
| Excluded | 0 |
| Errors | 0 |

## Exclusions by reason
| Reason | Count |
|--------|------:|
| (none) | 0 |

## Output class distribution
| Class | Count |
|-------|------:|
| `fake` | 9000 |
| `real` | 999 |

## Output generator distribution
| Generator | Count |
|-----------|------:|
| `dalle2` | 1000 |
| `dalle3` | 1000 |
| `firefly` | 1000 |
| `glide` | 1000 |
| `midjourney-v5` | 1000 |
| `raise_1k_jpeg` | 999 |
| `stable-diffusion-1-3` | 1000 |
| `stable-diffusion-1-4` | 1000 |
| `stable-diffusion-2` | 1000 |
| `stable-diffusion-xl` | 1000 |

## Error summary
See `metadata/errors.csv` (0 rows).

## Integrity
| Artifact | SHA-256 |
|----------|---------|
| `metadata/index.csv` | `6b9999a15b0e523e347623c575f1549767efb9c8e31931b800ea3fa0c3d1e379` |
| `config/pipeline.json` | `7517f23c87fea585a6e632181b52b4e94526ac3f011fb32bf4bf5143af0ee34b` |

## Notes
- Raw data was read-only.
- Processed image bytes live in the data tier (Kaggle); Git holds this report + pointer only.
- New parameters require a **new** `PPxxxx` (never overwrite).
