# System Integration Guide (STEP-066)

**Date:** 2026-11-19  
**Version:** `0.1.0`  
**Scope:** End-to-end wiring of `12_Web` (React + Vite) ↔ `13_Backend` (Django + DRF) ↔ `11_AI_Forensic_System` (AI Forensic Analyst).

---

## 1. End-to-End Data Flow (§8.2)

```
Browser (12_Web React UI)
  └─ src/api/forensicApi.js (VITE_API_BASE_URL)
       ├─ POST /api/v1/cases                  → apps.forensic_engine.allocate_case()
       ├─ POST /api/v1/cases/{id}/upload      → MOD001 receive_upload() + ThreadPoolExecutor job
       ├─ GET  /api/v1/cases/{id}/status      → live MOD014 stage polling (Uploading → Complete)
       ├─ GET  /api/v1/cases/{id}/evidence    → apps.evidence.read_case_evidence()
       ├─ GET  /api/v1/cases/{id}/decision    → apps.evidence.read_case_decision() (unchanged decision.json)
       ├─ GET  /api/v1/cases/{id}/explanation → apps.evidence.read_case_explanation() (A.9 data-only + MOD011)
       ├─ GET  /api/v1/cases/{id}/report      → apps.reports.read_case_report() (Template 24 JSON/MD/HTML)
       ├─ GET  /api/v1/health                 → apps.health.check_system_health()
       └─ GET  /api/v1/version                → apps.versioning.get_version_info() (model + dataset + Git commit)
```

**Binding separation of concerns (§8.1):**
- `12_Web` never runs inference, never interprets probabilities, and performs all HTTP requests exclusively inside `12_Web/src/api/`.
- `13_Backend` owns the investigation via `apps/forensic_engine/service.py`, which delegates directly to `11_AI_Forensic_System/pipeline.py` (`run_investigation`) under `_PIPELINE_LOCK` without duplicating any forensic logic.
- `11_AI_Forensic_System` handles all image validation, evidence collection, `EV` registration, validation, fusion, E4 confidence calibration, decision mapping, explainability, reasoning, report generation, and `MOD015` audit logging.

---

## 2. Environment Configuration (`dev` & `test`)

### 2.1 Backend (`13_Backend/.env.example`)
Copy `13_Backend/.env.example` to `13_Backend/.env` (gitignored) when running locally (`apps/core/config.py` loads `13_Backend/.env` automatically if present):
- `DJANGO_ENV=dev` (`DJANGO_DEBUG=true`)
- `DJANGO_SECRET_KEY` (override in production; never commit `.env`)
- `CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173`
- `FORENSIC_MEDIA_ROOT=13_Backend/media/cases` (gitignored; versioned `-input-01`, `-input-02`, ... per case)
- `FORENSIC_MODEL_ID=MODEL0001`
- `FORENSIC_ARTIFACT_ROOT=` (optional directory holding `MODEL0001_export.pkl`; when unset, `MOD004` records `model_unavailable` and `MOD008` emits explicit `Unknown`)
- `FORENSIC_ASYNC_MODE=thread` (`eager` available for deterministic unit tests)

### 2.2 Frontend (`12_Web/.env.example`)
Two development wiring modes work out of the box:
1. **Direct CORS mode** (set in `12_Web/.env`):
   - `VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1`
2. **Vite Dev Proxy mode** (default when `.env` is omitted):
   - `VITE_API_BASE_URL=/api/v1`
   - `12_Web/vite.config.js` proxies `/api/v1/*` to `VITE_PROXY_TARGET` (default `http://127.0.0.1:8000`).

---

## 3. Running Locally in Development (`dev`)

Terminal 1 — Start Django REST API (`13_Backend`):
```bash
.venv/Scripts/python.exe 13_Backend/manage.py runserver 127.0.0.1:8000
```

Terminal 2 — Start React Frontend (`12_Web`):
```bash
cd 12_Web
npm run dev
```

Open the configured Vite URL (`http://localhost:5173`), navigate to **New Investigation** (`/investigate/upload`), upload a face image (`.png`, `.jpg`, `.jpeg`, `.webp`), observe the 9 `MOD014` stages poll to `Complete`, and inspect `/result`, `/evidence`, `/explanation`, `/report`, and `/system` (`/version` provenance).

---

## 4. Automated Cross-Tier Verification

1. **Live cross-tier runner** (boots Django WSGI server in `thread` async mode and drives real React pages over TCP with zero mocked HTTP calls):
   ```bash
   .venv/Scripts/python.exe 17_Automation/verify_integration.py
   ```
2. **Backend live HTTP + CORS + async polling suite**:
   ```bash
   cd 13_Backend && ../.venv/Scripts/python.exe -m pytest tests/test_system_integration.py -v
   ```

---

## 5. Integration Smoke Checklist

- [x] `GET /api/v1/health` and `GET /api/v1/version` return `200 OK` with CORS headers for `http://localhost:5173` and surface `model_id`, `dataset_id`, `experiment_id`, and `git_commit` in the UI (`Navbar`, `Footer`, `SystemInfoPage`).
- [x] `POST /api/v1/cases` allocates `CASE000001` (`201 Created`).
- [x] `POST /api/v1/cases/{id}/upload` returns `202 Accepted` in `thread` async mode and versions uploads (`-input-01`, `-input-02`) without overwriting.
- [x] `GET /api/v1/cases/{id}/status` polls across `Uploading → … → Complete`.
- [x] `GET /api/v1/cases/{id}/evidence`, `/decision`, `/explanation`, and `/report` (`json`, `markdown`, `html`) render cleanly in React with zero duplicated logic across tiers.
