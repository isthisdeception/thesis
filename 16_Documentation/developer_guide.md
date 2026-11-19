# Developer Guide — AI Digital Forensics Platform

**Version:** `0.1.0`  
**Date:** 2026-11-19  
**Handbook Governance:** All engineering rules, identifier schemas ([A.1](../MASTER_RESEARCH_OPERATING_SYSTEM.md#a1-canonical-identifier-scheme)), naming policies ([A.2](../MASTER_RESEARCH_OPERATING_SYSTEM.md#a2-canonical-file-naming-rules)), Definition of Done ([A.5](../MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done)), and contributor rules ([CONTRIBUTING.md](../CONTRIBUTING.md)) live in the handbook and root docs; this guide covers how developers work in and extend the codebase.  
**Workflow Diagram:** [research_dev_workflow.md](./workflow_diagrams/research_dev_workflow.md)

---

## 1. Multi-Platform Engineering Workflow

The repository follows the strict single-responsibility workflow defined in [§10.1](../MASTER_RESEARCH_OPERATING_SYSTEM.md#101-core-philosophy--platform-responsibilities):

```
Cursor (Plan & Spec) ─▶ Antigravity (Implement & Test) ─▶ GitHub (Branch / PR / Review) ─▶ Kaggle (GPU Train / Eval) ─▶ Human (DECxxxx & Gates)
```

Key operational rules ([§10.3](../MASTER_RESEARCH_OPERATING_SYSTEM.md)):
1. All code edits happen on feature/experiment/docs branches (never push untested experiments directly into `main`).
2. Never edit code exclusively inside Kaggle notebooks — Kaggle consumes repository modules via `17_Automation/kaggle_sync/`.
3. Never mutate completed experiment configs (`06_Experiments/EXPxxxx/config.yaml`) or past decision logs ([01_Project_Management/decision_log/](../01_Project_Management/decision_log/)).
4. Keep [11_AI_Forensic_System/module_registry.csv](../11_AI_Forensic_System/module_registry.csv), [06_Experiments/experiment_registry.csv](../06_Experiments/experiment_registry.csv), and [05_Models/model_registry.csv](../05_Models/model_registry.csv) synchronized with code changes.

---

## 2. Codebase Map for Engineers

| Area | Entrypoint & Key Modules | Purpose |
|---|---|---|
| **Forensic Core** | `11_AI_Forensic_System/pipeline.py` (`run_investigation`), `evidence/`, `fusion/`, `confidence/`, `decision/`, `explainability/`, `reasoning/`, `reports/`, `audit/`, `failure_handling/` | Domain-pure investigation pipeline (`MOD001`–`MOD018`) |
| **Django Backend** | `13_Backend/forensic_backend/`, `13_Backend/apps/{core,forensic_engine,evidence,reports,health,versioning,api}/` | HTTP REST transport (`MOD013`) & thread-locked job runner |
| **React Frontend** | `12_Web/src/App.jsx`, `src/api/forensicApi.js`, `src/components/`, `src/pages/`, `src/hooks/` | 14-page `MOD014` UI consuming `MOD013` exclusively via `src/api/` |
| **Automation** | `17_Automation/run_all_tests.py`, `run_uat.py`, `verify_integration.py`, `training/`, `kaggle_sync/` | Cross-tier testing, UAT, training, & Kaggle synchronization |

---

## 3. How to Extend the Platform (`MOD018` Extension Contracts)

Per [11_AI_Forensic_System/specs/MOD018_spec.md](../11_AI_Forensic_System/specs/MOD018_spec.md) and invariant #5 of [architecture.md](./architecture.md), adding new forensic capabilities **never alters the pipeline stages** or allows `MOD008` to read image bytes. Extensions plug into two protocols:

### 3.1 Adding a New `EvidenceCollector` (`MOD003` / `MOD018`)

Every collector implements the `EvidenceCollector` Protocol defined in `11_AI_Forensic_System/evidence/item.py`:

```python
from evidence.item import CollectorContext, CollectorOutcome, EvidenceCollector, make_item

class ExampleSpectralCollector:
    evidence_type = "example_spectral"  # unique snake_case evidence_type

    def collect(self, context: CollectorContext) -> CollectorOutcome:
        # Allowed inputs: context.image (PIL.Image), context.stored_path, context.case_id, context.input_id
        # Forbidden: importing other collectors, writing EV ids, or emitting Real/Fake/Inconclusive/Unknown
        score = 0.0  # compute deterministic measurement
        item = make_item(
            evidence_type=self.evidence_type,
            description="Deterministic spectral measurement summary",
            raw_output={"case_id": context.case_id, "input_id": context.input_id, "metric": score},
            value=score,
            unit="ratio",
            confidence=None,  # keep None unless explicitly calibrated
        )
        return CollectorOutcome.one(item)
```

Checklist before merging a new collector:
1. Create its module under `11_AI_Forensic_System/evidence/collectors/` (no sibling collector imports).
2. Register it in `11_AI_Forensic_System/evidence/collectors/__init__.py` (`builtin_collectors`) and add validation rules if needed in `evidence/validation/`.
3. Update `MOD003` / `MOD018` documentation and [module_registry.csv](../11_AI_Forensic_System/module_registry.csv).
4. Add unit tests verifying failure isolation (using `CollectorOutcome.failed(name, detail)`) and downstream `MOD005`–`MOD008` compatibility.

### 3.2 Adding a New `FusionStrategy` (`MOD007` / `MOD018`)

Every fusion strategy implements `FusionStrategy` defined in `11_AI_Forensic_System/fusion/interface.py`:

```python
from typing import Sequence
from fusion.interface import FusionOutput, FusionStrategy, Unresolved, ValidatedEvidence, safe_raw

class ExampleWeightedStrategy:
    strategy_id = "weighted"  # reserved ids in fusion/interface.py: rule_based, weighted, bayesian
    version = "0.1.0"

    def fuse(self, evidence: Sequence[ValidatedEvidence]) -> FusionOutput:
        # Read ONLY validated MOD006 rows (never open files; never emit Real/Fake/Inconclusive/Unknown words)
        supporting = [row.evidence_id for row in evidence if row.quality != "unusable"]
        return FusionOutput(
            strategy_id=self.strategy_id,
            strategy_version=self.version,
            supporting_ids=supporting,
            summary={"lean": "no_directional_evidence", "rationale": "Custom weighted aggregation."},
            unresolved=[],
        )
```

Checklist before enabling a new fusion strategy:
1. Implement the strategy under `11_AI_Forensic_System/fusion/strategies/`.
2. Register it cleanly via `register_strategy(strategy_id, factory)` in `11_AI_Forensic_System/fusion/strategies/__init__.py` (never overwrite an existing ID or silently fall back if unknown).
3. Ensure `states_a_decision()` returns `False` on all fused outputs (`MOD007` emits `lean`, never `Real`/`Fake`/`Inconclusive`/`Unknown`).
4. Obtain a human-approved decision log (`DECxxxx` — follow [DEC0009](../01_Project_Management/decision_log/DEC0009.md)) before changing the active `strategy_id` in `fusion/fusion_config.json`.

---

## 4. Testing, Code Quality & Debugging

- **Before committing any code change**, run the consolidated verification harness ([test_plan.md](./test_plan.md)):
  ```bash
  .venv/Scripts/python.exe 17_Automation/run_all_tests.py
  ```
- **API-only backend test run (`eager` or `thread`):**
  ```bash
  cd 13_Backend && ../.venv/Scripts/python.exe -m pytest -q
  ```
- **Frontend Vitest + production Vite build check:**
  ```bash
  cd 12_Web && npm test && npm run build
  ```
- **Logs & Diagnostics:** Backend logs rotate across 7 named channels under `FORENSIC_LOG_DIR` (`application`, `api`, `inference`, `case`, `error`, `audit`, `performance`). Never expose internal logs or stack traces directly in HTTP responses (`MOD016` handles safe public envelopes).
- **Important Windows Host Note:** When running scripts inside `17_Automation/`, keep `17_Automation/` out of `sys.path` prior to stdlib/Django imports because `17_Automation/statistics/` shadows Python's stdlib `statistics` module (see [test_plan.md §6](./test_plan.md)).
