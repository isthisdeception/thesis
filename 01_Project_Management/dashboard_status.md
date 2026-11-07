# Project Dashboard

## Active Phase
- Current Phase: Environment & Model Foundation (PART 6)
- Active Step: **STEP-037** — Checkpoint system
- Registered Datasets: DS0001–DS0005 (`Ready=yes`, version v1.0)
- Registered Pipelines: PP0001–PP0003, PP0005–PP0006 (`complete`); PP0004 superseded
- Registered Splits: 10 splits across 5 outputs (`dataset_registry.csv` + `split_registry.csv`)

## Progress
- Literature Gate (Checklist 2): PASS
- Dataset Readiness (Checklist 3): PASS (human-confirmed 2026-09-01)
- Preprocessing (Checklist 4): PASS (human-confirmed 2026-09-01)
- Preprocessing design (STEP-025): COMPLETE
- Preprocessing modules (STEP-026): COMPLETE (34 unit tests)
- Preprocessing execution (STEP-027): COMPLETE
- Split generation (STEP-028): COMPLETE — leakage checks PASS
- FastAI prep + versioning + master registry (STEP-029): COMPLETE
- Environment lock (STEP-030): COMPLETE — Kaggle GPU v170 (Python 3.12, torch 2.10.0+cu128, fastai 2.8.7)
- Kaggle dataset upload + sync setup (STEP-031): COMPLETE — dry-run verified; shared artifact dataset created
- Candidate model discovery (STEP-032): COMPLETE — approved shortlist = ResNet-50, Xception, EfficientNet-B4
- Baseline strategy + fairness invariants (STEP-033): COMPLETE — EXP0001 fixed to ResNet-50 on DS0001/v1.0/PP0001/SPLIT0001
- Config system + FastAI training standard (STEP-034): COMPLETE — `config.yaml` template finalized; config validator (47 unit tests)
- Experiment readiness (STEP-035): COMPLETE — `EXP0001` scaffolded, config validator PASS, Checklist 5 PASS, registry `Status=ready`
- Training pipeline package (STEP-036): COMPLETE — `17_Automation/training/`, thin EXP0001 notebook, end-to-end smoke test PASS (CPU)
- `Ready=yes`

## Health
- Risk Indicators: Amber on DS0002 (processed 51452 after 5608 PP exclusions; raw untouched)
- Storage Tier Compliance: Enforced (processed images → Kaggle only)
- Publication Readiness: Dataset + Preprocessing phases complete (Checklists 3 & 4 PASS)
