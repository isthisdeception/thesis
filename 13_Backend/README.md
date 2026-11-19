# 13_Backend

**Purpose:** Django + DRF backend that owns the investigation.

## Contents
Django apps, media config, static config, API specs.

STEP-060 (2026-11-18): `architecture.md` specifies the single-responsibility Django apps (`core`, `api`, `forensic_engine`, `evidence`, `reports`, `health`, `versioning`; reserved future `accounts`, `history`, `analytics`), asynchronous investigation job flow, per-case media storage policy, `MOD016` error envelope (zero stack traces exposed), right-sized security controls, environment-variable configuration, and 7 log channels. `api_spec/api_spec.md` specifies all 10 canonical REST endpoints (`POST /cases`, `GET /cases/{id}`, `POST /cases/{id}/upload`, `GET /cases/{id}/status`, `/evidence`, `/decision`, `/explanation`, `/report`, `GET /health`, `GET /version`) via Template 16. Implementation begins at STEP-061.

STEP-061 (2026-11-18): `forensic_backend/` and `apps/` scaffold the Django + DRF project (`apps.core`, `apps.forensic_engine`, `apps.evidence`, `apps.reports`, `apps.health`, `apps.versioning`, `apps.api`), `.env.example`, `requirements.txt`, 7 structured rotating log channels (`apps/core/logging_config.py`), and `apps/forensic_engine/service.py` wrapping `11_AI_Forensic_System/pipeline.py` as an asynchronous/eager job with zero duplicated forensic logic. Check & tests: `python manage.py check` and `python -m pytest` from this folder.

STEP-062 (2026-11-19): `apps/api/` (`views.py`, `serializers.py`, `urls.py`, `throttles.py`) implements all 10 canonical REST endpoints (`POST /cases`, `GET /cases/{id}`, `POST /cases/{id}/upload`, `GET /cases/{id}/status`, `/evidence`, `/decision`, `/explanation`, `/report`, `GET /health`, `GET /version`) matching `api_spec/api_spec.md` and `MOD013_spec.md`. `backend_audit.md` records the Checklist 11 gate audit (`PASS`). Tests: `python -m pytest tests/test_api_endpoints.py` from this folder.

## Workflow
Antigravity writes, frontend consumes. No model training code.

## Owner
Antigravity

## Related Folders
11_AI_Forensic_System, 12_Web

## Expected Outputs
Backend API code, api_spec/

> *This folder follows the canonical repository hygiene and naming rules defined in `MASTER_RESEARCH_OPERATING_SYSTEM.md`. Please refer to the handbook for full policy details.*

## Cross-Linked Agents

The following agents operate within this domain:
- [Frontend Architect](../../19_Prompts/agents/web/frontend_architect.md)
- [Backend Architect](../../19_Prompts/agents/web/backend_architect.md)
- [API Designer](../../19_Prompts/agents/web/api_designer.md)
- [Component Designer](../../19_Prompts/agents/web/component_designer.md)
- [State Manager](../../19_Prompts/agents/web/state_manager.md)
- [Documentation](../../19_Prompts/agents/web/documentation.md)
- [Testing](../../19_Prompts/agents/web/testing.md)
- [Deployment](../../19_Prompts/agents/web/deployment.md)
- [Security Review](../../19_Prompts/agents/web/security_review.md)
