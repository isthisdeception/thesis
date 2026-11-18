# Backend Architecture Specification (STEP-060)

**Date:** 2026-11-18  
**Status:** specified  
**Version:** 0.1.0  
**Scope:** `13_Backend/` (Django + Django REST Framework). No application code is written in this step; implementation begins in STEP-061.

---

## 1. Binding Separation of Concerns (§8.1)

1. **The backend owns the investigation; the frontend owns the experience.** The React frontend (`12_Web/`) never performs inference, never imports model weights, and never interprets probabilities or thresholds.
2. **Zero duplicated forensic logic.** `13_Backend/` does not re-implement image validation, evidence collection, evidence validation, fusion, confidence calibration, decision rules, explainability, reasoning, report rendering, or audit logging. Instead, the `forensic_engine` app is the sole bridge that calls `11_AI_Forensic_System/pipeline.py` (`run_investigation`) and reads the records it wrote.
3. **No model training code.** Training, checkpointing, and Kaggle synchronization live exclusively in `05_Models/`, `06_Experiments/`, and `17_Automation/`.
4. **No hardcoded URLs or paths.** Every host, CORS origin, media path, registry path, and model artifact location is injected via environment variables.

---

## 2. Django Project & App Layout (§8.4)

Project package: `13_Backend/forensic_backend/`  
Apps directory: `13_Backend/apps/`

Each Django app has exactly **one responsibility**:

| App | Single Responsibility | Reads / Calls | Writes |
|---|---|---|---|
| `core` | Environment-based configuration loader (`dev`/`test`/`prod`), structured logging setup, shared DRF exception handler (maps errors to `MOD016`-compatible JSON without stack traces), and path resolution | Environment variables, `.env` | Server log streams (`logs/`) |
| `api` | Canonical URL routing (`/cases`, `/cases/{id}/...`, `/health`, `/version`), request/response serializers, and DRF viewsets/views that transport records written by the pipeline | `forensic_engine`, `evidence`, `reports`, `health`, `versioning` | HTTP JSON/Markdown/HTML responses |
| `forensic_engine` | Wraps `11_AI_Forensic_System` (`run_investigation`, `receive_upload`, `next_case_id`). Manages asynchronous/background case execution and live progress stage state (`MOD014` labels) | `11_AI_Forensic_System/pipeline.py` | Per-case job state file (`job_status.json`) and invokes the forensic pipeline |
| `evidence` | Read-only query adapter over `evidence_registry.csv` and per-case `decision.json`, `explanation.json`, and `reasoning.json` for a given `case_id` | `evidence_registry.csv`, case directory | None (read-only transport) |
| `reports` | Read-only query and format selector (`json`, `markdown`, `html`) over `{case_id}_report.json`, `{case_id}_report.md`, and `{case_id}_report.html` produced by `MOD012` | `cases/{case_id}/reports/` | None (read-only transport) |
| `health` | Serves `GET /health` by checking filesystem/registry accessibility and worker readiness without loading a case or model weights (`MOD013_spec.md`) | `core` config paths | Health status JSON |
| `versioning` | Serves `GET /version` using `11_AI_Forensic_System/reports/generator.py` (`resolve_version_stamps`, `resolve_git_commit`) and `05_Models/model_registry.csv` | `model_registry.csv`, Git HEAD | Version provenance JSON |

**Reserved future apps (§8.4, §8.10):** `accounts` (authentication/profiles), `history` (cross-case search), `analytics` (usage telemetry). None is enabled in v0.1.0.

---

## 3. Asynchronous Investigation Job Flow (§8.2)

```
POST /cases                  → assigns CASE000001, creates case dir, writes initial job_status.json (stage="Created")
POST /cases/{id}/upload      → runs MOD001 intake check immediately:
                                - if rejected (e.g., unsupported_format, empty, >20 MB): writes MOD016 record + failed case_registry.csv row, returns HTTP 400 with MOD016 JSON
                                - if accepted: stores CASE000001-input-01/original.<ext>, starts background investigation job, returns HTTP 202 Accepted
GET  /cases/{id}/status      → returns current MOD014 progress stage:
                                Uploading → Validating → Detecting Face → Running Analysis →
                                Collecting Evidence → Evaluating Confidence → Generating Explanation →
                                Preparing Report → Complete (or Failed with MOD016 failure record)
GET  /cases/{id}/evidence    → returns MOD005/MOD006 evidence rows for CASE000001
GET  /cases/{id}/decision    → returns decision.json (MOD008) unchanged
GET  /cases/{id}/explanation → returns explanation.json (MOD010) + reasoning.json (MOD011)
GET  /cases/{id}/report      → returns {case_id}_report.json | .md | .html (MOD012)
```

In `dev` and `test` profiles, `FORENSIC_ASYNC_MODE` supports `"thread"` (background `ThreadPoolExecutor` worker, default for interactive web polling) and `"eager"` (synchronous execution within `POST /cases/{id}/upload` for deterministic unit tests).

---

## 4. File Storage & Media Handling (§8.6)

- **Root directory:** `FORENSIC_MEDIA_ROOT` (defaults to `13_Backend/media/cases/`).
- **Per-case layout:**
  - `13_Backend/media/cases/{case_id}/job_status.json` — current `MOD014` stage label, timestamps, input id, and terminal status.
  - `13_Backend/media/cases/{case_id}/{case_id}-input-{seq}/original.{ext}` — immutable uploaded image (`MOD001`). A second upload to the same case receives `-input-02` and **never overwrites** `-input-01`.
  - `13_Backend/media/cases/{case_id}/{case_id}-input-{seq}/input_metadata.json` & `validation.json` (`MOD001`, `MOD002`).
  - `13_Backend/media/cases/{case_id}/decision.json` (`MOD008`), `explanation.json` (`MOD010`), `reasoning.json` (`MOD011`).
  - `13_Backend/media/cases/{case_id}/reports/{case_id}_report.{json,md,html}` (`MOD012`).
  - `13_Backend/media/cases/{case_id}/failures/{case_id}-fail-{seq}.json` (`MOD016`).
- **Git hygiene:** `13_Backend/media/*` (except `.gitkeep`) is ignored in `.gitignore` and never committed.
- **Retention & cleanup:** Configurable `FORENSIC_MEDIA_RETENTION_DAYS` (default `30` days for temporary case media) while preserving `evidence_registry.csv` and `case_registry.csv` audit trails.

---

## 5. Error Handling Contract (§8.7 & MOD016)

1. **No stack traces in HTTP responses.** Custom DRF exception handler catches any unhandled exception, logs the full traceback to the server-side `error` logger, writes a `MOD016` `unexpected_error` record when a `case_id` is in scope, and returns a clean JSON error envelope:
   ```json
   {
     "error": {
       "failure_id": "CASE000001-fail-01",
       "name": "unsupported_format",
       "reported_name": "unsupported_format",
       "module_id": "MOD001",
       "case_id": "CASE000001",
       "input_id": "CASE000001-input-01",
       "detail": "extension bmp is not in jpg, jpeg, png, webp",
       "timestamp": "2026-11-18T22:50:00+06:00"
     }
   }
   ```
2. **Canonical failure names (`MOD016`):** `no_face`, `multiple_faces`, `corrupted_image`, `unsupported_format`, `model_unavailable`, `low_confidence`, `timeout`, `unexpected_error`.

---

## 6. Right-Sized Security Plan (§8.8)

| Control | Specification |
|---|---|
| **Upload validation** | Enforced by `MOD001` (extension allowlist: `jpg`, `jpeg`, `png`, `webp`; non-empty; max `20 MB` via `FORENSIC_MAX_UPLOAD_BYTES`) and `MOD002` (PIL decode + format match + channel/resolution/noise checks + face gate). Rejected files are never written to disk. |
| **Request size limits** | Django `DATA_UPLOAD_MAX_MEMORY_SIZE` and `FILE_UPLOAD_MAX_MEMORY_SIZE` set from `FORENSIC_MAX_UPLOAD_BYTES` (`20971520` bytes). |
| **Rate limiting** | DRF throttling enabled (`DEFAULT_THROTTLE_RATES`): `upload` scope (`30/minute`), `anon` read/poll scope (`240/minute`), configurable via environment variables. |
| **CORS & CSRF** | `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS` read strictly from environment variables (no wildcard `*` in production). |
| **Secrets management** | `DJANGO_SECRET_KEY` loaded from environment; `.env` is gitignored; `.env.example` contains placeholder values only. |
| **HTTP headers** | `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, and `Referrer-Policy: same-origin` enabled in middleware. |

---

## 7. Configuration & Logging Plan (§8.9)

### 7.1 Environment Variables (`.env.example`)

| Variable | Purpose | Default (dev/test only) |
|---|---|---|
| `DJANGO_ENV` | Profile selector (`dev`, `test`, `prod`) | `dev` |
| `DJANGO_SECRET_KEY` | Django cryptographic key (required in `prod`) | `dev-insecure-placeholder-change-me` |
| `DJANGO_DEBUG` | Debug mode (`false` in `prod`) | `true` in `dev`, `false` otherwise |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hosts | `127.0.0.1,localhost` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated frontend origins | `http://localhost:5173,http://127.0.0.1:5173` |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated trusted origins | `http://localhost:5173,http://127.0.0.1:5173` |
| `FORENSIC_MEDIA_ROOT` | Case storage root | `13_Backend/media/cases` |
| `FORENSIC_EVIDENCE_REGISTRY` | Path to `evidence_registry.csv` | `11_AI_Forensic_System/evidence_registry.csv` |
| `FORENSIC_CASE_REGISTRY` | Path to `case_registry.csv` | `11_AI_Forensic_System/case_registry.csv` |
| `FORENSIC_MODEL_ID` | Default registered detector ID | `MODEL0001` |
| `FORENSIC_ARTIFACT_ROOT` | Directory holding exported `.pkl` weights | `` (optional local path) |
| `FORENSIC_ASYNC_MODE` | `"thread"` or `"eager"` | `thread` |
| `FORENSIC_MAX_UPLOAD_BYTES` | Max upload size in bytes | `20971520` |
| `FORENSIC_THROTTLE_UPLOAD` | Upload rate limit | `30/min` |
| `FORENSIC_THROTTLE_ANON` | General API rate limit | `240/min` |

### 7.2 Seven Structured Log Channels (§8.9)

Logs are written under `FORENSIC_LOG_DIR` (`13_Backend/media/logs/`, gitignored) with rotating file handlers:
1. `application.log` — Django lifecycle and startup configuration.
2. `api.log` — HTTP method, route, status code, and latency per request.
3. `inference.log` — `MOD004` detector model ID, execution time, and status.
4. `case.log` — `MOD014` stage transitions (`Uploading` → `Complete`/`Failed`) per `case_id`.
5. `error.log` — Server-side tracebacks and `MOD016` failure records.
6. `audit.log` — `MOD005` `EV` registrations and `MOD015` `case_registry.csv` appends.
7. `performance.log` — End-to-end case execution time and per-stage latency.
