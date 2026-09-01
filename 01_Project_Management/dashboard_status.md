# Project Dashboard

## Active Phase
- Current Phase: Preprocessing (PART 5)
- Active Step: **STEP-029** — FastAI prep, versioning, master registry + Preprocessing Gate
- Registered Datasets: DS0001–DS0005 (raw Checklist 3 PASS)
- Registered Pipelines: PP0001–PP0003, PP0005–PP0006 (`complete`)
- Registered Splits: 10 splits across 5 outputs (`split_registry.csv`)

## Progress
- Literature Gate (Checklist 2): PASS
- Dataset raw gate (Checklist 3 raw-stage): PASS (human-confirmed)
- Preprocessing design (STEP-025): COMPLETE
- Preprocessing modules (STEP-026): COMPLETE (34 unit tests)
- Preprocessing execution (STEP-027): COMPLETE
- Split generation (STEP-028): COMPLETE — leakage checks PASS
- `Ready=no` until STEP-029

## Health
- Risk Indicators: Amber on DS0002 (1593 corrupt paths on exclude list for PP0002)
- Storage Tier Compliance: Enforced (processed images → Kaggle only)
- Publication Readiness: STEP-029 gates pending
