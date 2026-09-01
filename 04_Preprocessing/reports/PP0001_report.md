# Preprocessing Report: PP0001

> Template 6 — Phase D11  
> **Date:** 2026-08-27  
> **Status:** GENERATED  
> **Research question:** How can we improve the cross-generator generalization of image-based AI face detection models to maintain high accuracy on unseen generative architectures?

## Identifiers
| Field | Value |
|-------|-------|
| Pipeline ID | `PP0001` |
| Dataset ID | `DS0001` |
| Output | `DS0001_PP0001` |
| Processed root | `/kaggle/working/processed/DS0001_PP0001` |
| Kaggle pointer | `kaggle:isthisdeception/ds0001-pp0001` |

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
  "pipeline_id": "PP0001",
  "dataset_id": "DS0001",
  "target_size": 224,
  "output_format": "PNG",
  "norm_mode": "imagenet",
  "apply_on_disk": false,
  "exclude_list": null,
  "random_seed": 42,
  "purpose": "Primary train processed (face packs default)"
}
```

## Counts
| Metric | Value |
|--------|------:|
| Input candidates | 50000 |
| Kept | 50000 |
| Excluded | 0 |
| Errors | 0 |

## Exclusions by reason
| Reason | Count |
|--------|------:|
| (none) | 0 |

## Output class distribution
| Class | Count |
|-------|------:|
| `fake` | 25000 |
| `real` | 25000 |

## Output generator distribution
| Generator | Count |
|-----------|------:|
| `cips` | 1923 |
| `face_synthetics` | 1923 |
| `gansformer` | 1923 |
| `lama` | 1923 |
| `mat` | 1923 |
| `none` | 25000 |
| `projected_gan` | 1923 |
| `sfhq` | 1923 |
| `stable_diffusion` | 1923 |
| `stargan` | 1923 |
| `stylegan1` | 1923 |
| `stylegan2` | 1924 |
| `stylegan3` | 1923 |
| `taming_transformer` | 1923 |

## Error summary
See `metadata/errors.csv` (0 rows).

## Integrity
| Artifact | SHA-256 |
|----------|---------|
| `metadata/index.csv` | `9391b5cdd2e8b9696f9872e11e9f50b02c9b0d0509e9886cb83d888d03c6bdff` |
| `config/pipeline.json` | `08d0617cc601726bb695749a49ba72019f954a0249566238786930b4957c645a` |

## Notes
- Raw data was read-only.
- Processed image bytes live in the data tier (Kaggle); Git holds this report + pointer only.
- New parameters require a **new** `PPxxxx` (never overwrite).
