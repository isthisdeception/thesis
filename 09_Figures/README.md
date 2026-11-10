# 09_Figures

**Purpose:** Every figure used anywhere plus its specification and generation provenance.

## Contents
Figure specs, generation scripts, assets (png/svg/pdf), captions.

## Workflow
Human / Figure agents write, Writing / Web consume.

## Owner
Figure specification agents / Human

## Related Folders
08_Evaluation, 15_Writing

## Expected Outputs
specs/FIGxxxx_spec.md, assets/FIGxxxx_v1.png

## STEP-023 / Phase D7 figure specs (data only)
| FIG ID | Topic | Data path |
|--------|-------|-----------|
| FIG0001 | DS0001 class balance | `03_Datasets/reports/eda_class_distribution.csv` |
| FIG0002 | DS0001 generator mix | `eda_generator_distribution.csv` |
| FIG0003 | DS0002 generator × condition | `eda_generator_distribution.csv` |
| FIG0004 | DS0003 class balance | `eda_class_distribution.csv` |
| FIG0005 | DS0004 generator mix | `eda_generator_distribution.csv` |
| FIG0006 | DS0005 race demographics | `eda_demographic_distribution.csv` |
| FIG0007 | Resolution comparison | `eda_resolution_distribution.csv` |
| FIG0008 | Brightness comparison | `eda_brightness_stats.csv` |
| FIG0009 | Contrast comparison | `eda_contrast_stats.csv` |
| FIG0010 | Compression / format | `eda_compression_stats.csv` |

## STEP-044 / Phases E4–E5 figure specs (data only)
| FIG ID | Topic | Data path |
|--------|-------|-----------|
| FIG0011 | Reliability diagram (EVAL0001 test) | `08_Evaluation/EVAL0001/reliability.csv` |
| FIG0012 | Confidence distribution vs accuracy | `08_Evaluation/EVAL0001/confidence_distribution.csv` |
| FIG0013 | Threshold trade-off with operating points | `08_Evaluation/EVAL0001/threshold_sweep.csv`, `operating_points.csv` |

## STEP-045 / Phases E6, E12 figure specs (data only)
| FIG ID | Topic | Data path |
|--------|-------|-----------|
| FIG0014 | Confusion matrix (EVAL0001 test) | `08_Evaluation/EVAL0001/confusion_matrix.csv` |
| FIG0015 | Error rate by generator and real source | `08_Evaluation/EVAL0001/error_by_group.csv` |

Specs live in `09_Figures/specs/`. **Do not commit AI-rendered publication figures** ([A.9](../MASTER_RESEARCH_OPERATING_SYSTEM.md#a9-canonical-figure-policy)).

> *This folder follows the canonical repository hygiene and naming rules defined in `MASTER_RESEARCH_OPERATING_SYSTEM.md`. Please refer to the handbook for full policy details.*
