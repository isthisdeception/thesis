# 04_Preprocessing

**Purpose:** Modular, versioned preprocessing pipelines (PPxxxx).

## Phase Status
- **STEP-025 — Pipeline Design (Phase D9 design):** `COMPLETE` (2026-08-12)
  - Design: `design/PREPROCESSING_PIPELINE_DESIGN.md`
  - Parameters: `design/parameters_catalog.md`
  - Module specs: `specs/PPMOD01` … `PPMOD10`
- **STEP-026 — Implement modules:** `NEXT` (no code in STEP-025)

## Contents
Reusable pipeline modules (STEP-026+), registry, reports, validation modules, **design specs**.

## Workflow
Preprocessing agent designs (Cursor) → implements (Antigravity) → Datasets/Experiments consume.  
**No monolithic scripts.** Raw read-only; writes only to `processed/DSxxxx_PPxxxx/`.

## Owner
Preprocessing Agent

## Related Folders
`03_Datasets`

## Expected Outputs
`preprocessing_registry.csv`, `preprocessing_report.md` per `PPxxxx`, packaged modules + tests

> *This folder follows the canonical repository hygiene and naming rules defined in `MASTER_RESEARCH_OPERATING_SYSTEM.md`. Please refer to the handbook for full policy details.*
