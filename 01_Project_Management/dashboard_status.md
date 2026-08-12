# Project Dashboard

## Active Phase
- Current Phase: Dataset Operating System (PART 4 → PART 5)
- Active Step: **STEP-024 COMPLETE (raw gate)** → next **STEP-025 — Preprocessing Pipeline Design**
- Registered Datasets: DS0001–DS0005
- Kaggle: `isthisdeception/ds0001-artifact-face-subset`, `…/ds0002-diff-official-test`, `…/ds0004-synthbuster`, `…/ds0005-fairface`; DS0003 = `xhlulu/140k-real-and-fake-faces`

## Progress
- Deferred Decisions: DEC0001–DEC0005
- Literature Gate (Checklist 2): PASS
- Dataset raw gate (Checklist 3 raw-stage): **PASS** (human-confirmed 2026-08-12; `reports/dataset_audit.md`)
- `Downloaded=yes` / `Validated=yes`: DS0001–DS0005
- `Ready=no` (set only at STEP-029)
- Docs: `dataset_report.md`, `dataset_card.md`, EDA + validation reports present

## Health
- Risk Indicators: Amber on DS0002 (~2.8% corrupt — filter in STEP-025; 143 identities → leakage-safe splits)
- Storage Tier Compliance: Enforced
- Publication Readiness: Dataset Preparation → Preprocessing
