# 16_Documentation

**Purpose:** Developer, user, API, installation, integration, testing, and system architecture documentation.  
**Policy:** Governs [§16_Documentation](../MASTER_RESEARCH_OPERATING_SYSTEM.md#16_documentation) and [Checklist 12](../MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-12--documentation). Links to [MASTER_RESEARCH_OPERATING_SYSTEM.md](../MASTER_RESEARCH_OPERATING_SYSTEM.md) rather than duplicating handbook rules.

## Contents

| File / Folder | Purpose | Step |
|---|---|---|
| [architecture.md](./architecture.md) | System-wide 3-tier architecture, `MOD001`–`MOD018` pipeline invariants, decision logs, and registry map | STEP-068 |
| [api_guide.md](./api_guide.md) | REST API usage guide derived from `13_Backend/api_spec/api_spec.md` (10 endpoints, `MOD016` errors, `curl` walkthrough) | STEP-068 |
| [developer_guide.md](./developer_guide.md) | Developer setup, platform workflow, and `MOD018` extension guides (`EvidenceCollector` & `FusionStrategy`) | STEP-068 |
| [user_guide.md](./user_guide.md) | End-user guide for investigating media in `12_Web` and interpreting decisions, confidences, and errors | STEP-068 |
| [installation.md](./installation.md) | Local Python `.venv`, Node/Vite, `.env` configuration, and test verification commands | STEP-068 |
| [folder_guide.md](./folder_guide.md) | Explanations of all 20 canonical folders (`01_`–`20_`), `environment/`, and root files | STEP-068 |
| [integration_guide.md](./integration_guide.md) | Cross-tier wiring (`12_Web` ↔ `13_Backend` ↔ `11_AI_Forensic_System`) and smoke verification | STEP-066 |
| [test_plan.md](./test_plan.md) | Cross-tier test plan (`55` core, `18` backend, `12` frontend unit/page/regression, live integration, `6` UAT) | STEP-067 |
| [workflow_diagrams/](./workflow_diagrams/README.md) | Mermaid diagrams for 3-tier architecture, 18-module pipeline, and multi-platform dev workflow | STEP-068 |
| [documentation_audit.md](./documentation_audit.md) | Checklist 12 Documentation Gate audit report & consistency verification | STEP-068 |

## Workflow
Documentation agent authors and synchronizes docs; developers, users, and thesis examiners consume them. Do not duplicate the handbook.

## Owner
Documentation Agent

## Related Folders
All sections (`01_`–`20_`, `environment/`)

> *This folder follows the canonical repository hygiene and naming rules defined in [`MASTER_RESEARCH_OPERATING_SYSTEM.md`](../MASTER_RESEARCH_OPERATING_SYSTEM.md).*
