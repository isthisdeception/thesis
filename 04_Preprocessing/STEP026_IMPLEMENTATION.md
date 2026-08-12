# STEP-026 — Implement Preprocessing Modules

**Status:** COMPLETE (2026-08-12)  
**Handbook:** Phase D9 implementation  
**Specs:** `specs/PPMOD01`–`PPMOD10` (STEP-025)

## Deliverables
| Artifact | Path |
|----------|------|
| Modules PPMOD01–10 | `modules/*.py` |
| Validators PPMOD01V–10V | `modules/validation.py` |
| Thin orchestrator | `pipeline_runner.py` |
| Unit tests | `tests/test_ppmod*.py` + `test_pipeline_runner.py` |

## Verification checklist
- [x] One packaged module per step; importable; no monolith
- [x] Unit tests pass (34); parameters injected (dataclass params)
- [x] Explicit error handling (`ModuleError` / exclude rows; no silent skips)
- [x] Raw read-only; outputs to `processed/` (runner + save guardrail)
- [x] Spec-aligned defaults (`assume_single_face_crop`, ImageNet norm, etc.)

## Notes
- Face detect/align/crop implemented but **disabled by default** (packs already face-centric).
- `retinaface` / `mtcnn` raise `DETECTOR_NOT_PINNED` until STEP-030 environment lock; `stub` + optional `opencv_haar` available.
- Metadata extraction reuses `17_Automation/dataset_eda/labels.py`.
- Full Kaggle run + registry row = **STEP-027**.

## Test command
```bash
cd 04_Preprocessing && python -m pytest tests/ -v
```
