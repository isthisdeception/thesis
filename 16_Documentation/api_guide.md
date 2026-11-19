# REST API Usage Guide (`MOD013`)

**Version:** `0.1.0`  
**Date:** 2026-11-19  
**Authoritative Contract:** Derived directly from [13_Backend/api_spec/api_spec.md](../13_Backend/api_spec/api_spec.md) and matching client code in [12_Web/src/api/forensicApi.js](../12_Web/src/api/forensicApi.js). All 10 endpoints are served by `13_Backend/apps/api/`.

---

## 1. Base URLs, Transport & Throttling

- **Dual Routing:** All endpoints are mounted identically at `/api/v1/<route>` and `/<route>`. The frontend defaults to `/api/v1` (via `VITE_API_BASE_URL` or the Vite dev proxy).
- **Content Types:**
  - JSON request/response (`application/json`) for 9 endpoints.
  - `multipart/form-data` (field name `file`) for `POST /cases/{id}/upload`.
  - Optional `text/markdown; charset=utf-8` or `text/html; charset=utf-8` via `?format=` on `GET /cases/{id}/report`.
- **Rate Limits (DRF Throttling):** Configured via environment variables (`FORENSIC_THROTTLE_UPLOAD=30/min` on uploads, `FORENSIC_THROTTLE_ANON=240/min` on general anonymous requests).
- **Authentication:** None in `v0.1.0` (single-researcher / local evaluation mode; future auth reserved under `accounts`).

---

## 2. Standard Error Envelope (`MOD016`)

Every `4xx` and `5xx` error returns a structured `MOD016` envelope without exposing stack traces:

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
    "timestamp": "2026-11-19T12:00:00+06:00"
  }
}
```

Canonical failure names: `unsupported_format`, `corrupted_image`, `no_face`, `multiple_faces`, `model_unavailable`, `low_confidence`, `timeout`, `unexpected_error`.

---

## 3. Endpoint Reference (10 Canonical Endpoints)

| # | Method & Path | Purpose | Key Status Codes |
|---|---|---|---|
| 1 | `POST /api/v1/cases` | Allocate immutable `CASExxxxxx` directory and initial `job_status.json` (`stage: "Created"`). Optional JSON body: `model_id`, `configuration`. | `201 Created`, `400`, `429`, `500` |
| 2 | `GET /api/v1/cases/{id}` | Retrieve case summary from `case_registry.csv` merged with live job state (`id` matches `^CASE\d{6}$`). | `200 OK`, `400`, `404` |
| 3 | `POST /api/v1/cases/{id}/upload` | Upload multipart `file` (`jpg`/`jpeg`/`png`/`webp`, non-empty, `<= 20 MB`). Runs `MOD001` intake synchronously and launches the async pipeline (`MOD002`–`MOD012`, `MOD015`). | `202 Accepted` (`200 OK` if `eager`), `400`, `404`, `429` |
| 4 | `GET /api/v1/cases/{id}/status` | Poll `MOD014` stage progress (`0`–`100%`, `stage`, `stage_history`, `failures`). | `200 OK`, `404` |
| 5 | `GET /api/v1/cases/{id}/evidence` | List `EV` rows from `evidence_registry.csv` for `case_id` with server paths stripped. Supports `?validated_only=true`. | `200 OK`, `404` |
| 6 | `GET /api/v1/cases/{id}/decision` | Return `MOD008` `decision.json` **byte-for-byte unchanged** (`Real`, `Fake`, `Inconclusive`, `Unknown`). | `200 OK`, `404` (includes `MOD016` failure if stopped early) |
| 7 | `GET /api/v1/cases/{id}/explanation` | Return data-only `explanation.json` (`MOD010`, Policy A.9). Append `?include_reasoning=true` to attach `MOD011` `reasoning.json`. | `200 OK`, `404` |
| 8 | `GET /api/v1/cases/{id}/report` | Download `MOD012` report via `?format=json` (default), `markdown` (Template 24), or `html`. | `200 OK`, `400`, `404` |
| 9 | `GET /api/v1/health` | Service readiness (`media_root_writable`, registry readability) without loading any case or weights. | `200 OK`, `503` |
| 10 | `GET /api/v1/version` | Provenance metadata (`system_version`, `api_version`, `model_id`, `dataset_id`, `experiment_id`, `git_commit`, `fusion_strategy_id`, `confidence_formula_id`). | `200 OK`, `500` |

Full request/response JSON schemas and field definitions live in [13_Backend/api_spec/api_spec.md](../13_Backend/api_spec/api_spec.md).

---

## 4. End-to-End `curl` Walkthrough

```bash
# 1. Verify backend readiness & model provenance
curl -s http://127.0.0.1:8000/api/v1/health
curl -s http://127.0.0.1:8000/api/v1/version

# 2. Create a case
curl -s -X POST http://127.0.0.1:8000/api/v1/cases \
  -H "Content-Type: application/json" \
  -d '{"model_id": "MODEL0001"}'
# -> {"case_id": "CASE000001", "status": "created", "stage": "Created", ...}

# 3. Upload an image (starts background investigation in thread mode)
curl -s -X POST http://127.0.0.1:8000/api/v1/cases/CASE000001/upload \
  -F "file=@path/to/face.png"
# -> HTTP 202 Accepted {"case_id": "CASE000001", "input_id": "CASE000001-input-01", "job_status": "running", ...}

# 4. Poll until status is "completed" or "failed"
curl -s http://127.0.0.1:8000/api/v1/cases/CASE000001/status

# 5. Fetch unchanged decision, validated evidence, explanation+reasoning, and Markdown report
curl -s http://127.0.0.1:8000/api/v1/cases/CASE000001/decision
curl -s "http://127.0.0.1:8000/api/v1/cases/CASE000001/evidence?validated_only=true"
curl -s "http://127.0.0.1:8000/api/v1/cases/CASE000001/explanation?include_reasoning=true"
curl -s "http://127.0.0.1:8000/api/v1/cases/CASE000001/report?format=markdown"
```

---

## 5. Versioning & Change Policy

- Current REST API version is `0.1.0`. Backward-incompatible changes require updating [api_spec.md](../13_Backend/api_spec/api_spec.md), [12_Web/src/api/forensicApi.js](../12_Web/src/api/forensicApi.js), this guide, and running the cross-tier integration and UAT suite documented in [test_plan.md](./test_plan.md).
