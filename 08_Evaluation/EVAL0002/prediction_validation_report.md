# Prediction Validation: EVAL0002

**Experiment:** EXP0002
**Status:** PASS
**Date:** 2026-11-10

Phases E1 and E2 only. This report does not recompute ROC-AUC or any other metric.

| Phase | Check | Result | Detail |
|-------|-------|--------|--------|
| E1 | experiment registered | PASS | status=completed |
| E1 | model exported and registered | PASS | status=trained, export=isthisdeception/thesis-exp0002-artifacts:MODEL0008_export.pkl |
| E1 | dataset and split linked | PASS | DS0001_PP0001_SPLIT0002 status=ready |
| E1 | config archived | PASS | SHA-256 matches run_summary.json |
| E1 | checkpoint and export archived | PASS | EXP0002_checkpoints.md |
| E1 | git commit recorded | PASS | faa16a67836b52b7f87dda4fcf8d09ef3bd97997 |
| E1 | evaluation id reserved | PASS | EVAL0002 |
| E2 | prediction files present | PASS | 9127 rows |
| E2 | source file integrity | PASS | SHA-256 matches the manifest |
| E2 | prediction columns | PASS | present |
| E2 | no duplicate ids | PASS | 0 duplicate id(s) |
| E2 | probabilities in [0, 1] | PASS | all in range |
| E2 | class labels binary | PASS | y_true is 0/1 |
| E2 | val count | PASS | predictions=7204 ground_truth=7204 missing=0 extra=0 |
| E2 | val labels and paths | PASS | label mismatches=0, path mismatches=0 |
| E2 | test count | PASS | predictions=1923 ground_truth=1923 missing=0 extra=0 |
| E2 | test labels and paths | PASS | label mismatches=0, path mismatches=0 |

No metrics were computed. STEP-043 may use these predictions.
