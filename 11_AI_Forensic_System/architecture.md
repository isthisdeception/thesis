# AI Forensic Analyst — Architecture (STEP-051)

**Date:** 2026-11-17  
**Status:** specified  
**Scope:** Modules 1–18. No module is implemented in this step.

The system is an evidence-driven investigation. The image detector is one specialist. It does not decide the case.

## Pipeline

`Image Upload → Evidence Collection → Evidence Validation → Evidence Fusion → Reasoning → Decision → Explanation → Forensic Report → API Response → Frontend Visualization`

Module 14 shows that pipeline to the user as: Uploading → Validating → Detecting Face → Running Analysis → Collecting Evidence → Evaluating Confidence → Generating Explanation → Preparing Report → Complete.

## Invariants

1. The detector never decides. Module 4 emits probabilities, optional embeddings, timing, and metadata. It does not emit Real, Fake, Inconclusive, or Unknown.
2. The Decision Engine reads validated evidence only. It does not read the image, a path it could use to open the image, or the model weights.
3. Uncertainty is never hidden. A missing confidence stays null. A low-quality evidence item stays in the record with its quality flag.
4. Explanations are never fabricated. Module 11 may state only what an evidence id records.
5. Future modalities are added by registering a new `EvidenceCollector` and, when the combination rule must change, a new `FusionStrategy`. The pipeline above does not change.

## Who may see the image

| Module | May read image bytes | May decide the case |
|---|---|---|
| MOD001 Input Management | yes, to store the upload | no |
| MOD002 Image Validation | yes, to check the file | no |
| MOD003 collectors, including MOD004 and explainability inputs | yes, inside that collector only | no |
| MOD005–MOD012, MOD015 | no | only MOD008, and only from validated evidence |
| MOD013 API, MOD014 Frontend | no; they transport records | no |

A collector does not call another collector. Face quality does not call face detection. The explainability collector loads the model through the model registry, the same way Module 4 does, and does not import Module 4's private state.

## Fusion

DEF-004 is still deferred. The first configured strategy name is `rule_based`. `weighted` and `bayesian` are reserved names on the same interface and are not selected. This document does not choose the rule table. A later step writes that table for human approval.

## Registries

- Modules: `module_registry.csv` (MOD001–MOD018, status `specified`)
- Evidence items, once investigations exist: `evidence_registry.csv` (EV ids). The schema is `specs/interfaces.md`. No evidence row is invented here.
- Cases, once investigations exist: `case_registry.csv`. No case row is invented here.

Module 19 is the forensic agent set under `19_Prompts/agents/forensic/`. Those agents are not a pipeline stage and are not a row in this registry.

## Specs

One file per module: `specs/MOD001_spec.md` … `specs/MOD018_spec.md`. Shared contracts: `specs/interfaces.md`.
