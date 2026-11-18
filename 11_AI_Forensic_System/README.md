# 11_AI_Forensic_System

**Purpose:** The AI Forensic Analyst source.

## Contents
Module specs, the shared interfaces, and the module registry. Implementation begins at STEP-052.

STEP-051 (2026-11-17): `architecture.md` states the pipeline and the invariants. `specs/MOD001_spec.md` through `specs/MOD018_spec.md` are the module specs. `specs/interfaces.md` defines `EvidenceCollector`, `FusionStrategy`, and the evidence item tied to `EV` ids. `module_registry.csv` lists MOD001–MOD018 as `specified`. No collector is implemented yet.

## Workflow
Antigravity writes, Backend consumes. No frontend/training code.

## Owner
Antigravity

## Related Folders
13_Backend, 08_Evaluation

## Expected Outputs
module_registry.csv, module source files

> *This folder follows the canonical repository hygiene and naming rules defined in `MASTER_RESEARCH_OPERATING_SYSTEM.md`. Please refer to the handbook for full policy details.*

## Cross-Linked Agents

The following agents operate within this domain:
- [Input](../../19_Prompts/agents/forensic/input.md)
- [Validation](../../19_Prompts/agents/forensic/validation.md)
- [Evidence](../../19_Prompts/agents/forensic/evidence.md)
- [Fusion](../../19_Prompts/agents/forensic/fusion.md)
- [Decision](../../19_Prompts/agents/forensic/decision.md)
- [Explanation](../../19_Prompts/agents/forensic/explanation.md)
- [Report](../../19_Prompts/agents/forensic/report.md)
- [Audit](../../19_Prompts/agents/forensic/audit.md)
- [API](../../19_Prompts/agents/forensic/api.md)
