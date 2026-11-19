# Frontend API Client Specification (STEP-063)

**Date:** 2026-11-19  
**Status:** specified  
**Version:** `0.1.0`  
**Folder Location:** `12_Web/src/api/`  
**Backend Contract:** `13_Backend/api_spec/api_spec.md` (`MOD013`)

---

## 1. Design Rules (§8.1 & `MOD014_spec.md`)

1. **Single source of network I/O.** Every HTTP request in `12_Web/` goes through `12_Web/src/api/forensicApi.js`. No component, hook, or page may call `fetch()` directly.
2. **Environment-configured base URL.** `12_Web/src/api/config.js` reads `import.meta.env.VITE_API_BASE_URL` (defaulting to `"/api/v1"` when served behind a dev proxy or reverse proxy, never a hardcoded production URL).
3. **Structured `MOD016` error normalization.** Every non-2xx response or network/timeout failure is normalized into a `ForensicApiError` object with `{ status, failure_id, name, module_id, case_id, input_id, detail, timestamp, isNetworkError }` so the UI can render `ErrorState` consistently without guessing or showing stack traces.
4. **Zero client-side interpretation.** The API client returns the backend JSON records (`decision.json`, `explanation.json`, `evidence` rows, `report`) unchanged.

---

## 2. Environment Configuration (`12_Web/.env.example` & `src/api/config.js`)

| Variable | Purpose | Default |
|---|---|---|
| `VITE_API_BASE_URL` | Base URL for all backend REST requests | `http://127.0.0.1:8000/api/v1` (in `.env.example`) / `"/api/v1"` fallback |
| `VITE_POLL_INTERVAL_MS` | Status polling interval while `status === "running"` | `600` |
| `VITE_REQUEST_TIMEOUT_MS` | Per-request `AbortController` timeout | `15000` |

---

## 3. Canonical Client Functions (`12_Web/src/api/forensicApi.js`)

| Function | HTTP Method & Path | Parameters | Returns | Error Behavior |
|---|---|---|---|---|
| `createCase(options?)` | `POST /cases` | `{ modelId?, configuration? }` | `{ case_id, status, stage, model_id, configuration, created_timestamp }` | Throws `ForensicApiError` on `400`/`429`/`500` |
| `getCaseDetail(caseId)` | `GET /cases/{id}` | `caseId: string` | `{ case_id, status, stage, input_id, evidence_ids, decision, model_id, version, configuration, execution_time_seconds, errors, warnings, timestamp }` | Throws `ForensicApiError` on `400`/`404` |
| `uploadCaseImage(caseId, file)` | `POST /cases/{id}/upload` | `caseId: string`, `file: File \| Blob` (`multipart/form-data`) | `{ case_id, input_id, intake, job_status, stage }` | Throws `ForensicApiError` with `MOD001` `unsupported_format` or `unexpected_error` on `400` |
| `getCaseStatus(caseId)` | `GET /cases/{id}/status` | `caseId: string` | `{ case_id, status, stage, stage_history, progress_percent, input_id, failures, updated_timestamp }` | Throws `ForensicApiError` on `404` |
| `getCaseEvidence(caseId, options?)` | `GET /cases/{id}/evidence` | `caseId: string`, `{ validatedOnly?: boolean }` | `{ case_id, evidence_ids, count, items }` | Throws `ForensicApiError` on `404` |
| `getCaseDecision(caseId)` | `GET /cases/{id}/decision` | `caseId: string` | Exact `decision.json` payload (`{ case_id, decision, fused_evidence_id, confidence_evidence_id, reasoning_path, decision_metadata }`) | Throws `ForensicApiError` (carrying the case's `MOD016` failure record when stopped at `MOD001`/`MOD002`) on `404` |
| `getCaseExplanation(caseId, options?)` | `GET /cases/{id}/explanation` | `caseId: string`, `{ includeReasoning?: boolean }` | `explanation.json` payload (+ `reasoning` when `includeReasoning: true`) | Throws `ForensicApiError` on `404` |
| `getCaseReport(caseId, format?)` | `GET /cases/{id}/report?format=...` | `caseId: string`, `format: "json" \| "markdown" \| "html"` | Parsed JSON object (when `"json"`) or raw text string (when `"markdown"` or `"html"`) | Throws `ForensicApiError` on `400`/`404` |
| `getHealth()` | `GET /health` | None | `{ status, service, environment, checks, timestamp }` | Throws `ForensicApiError` on `503` or network disconnect |
| `getVersion()` | `GET /version` | None | `{ system_version, api_version, model_id, model_version, dataset_id, experiment_id, git_commit, fusion_strategy_id, confidence_formula_id, timestamp }` | Throws `ForensicApiError` on `500` or network disconnect |

---

## 4. Error Normalization Contract (`12_Web/src/api/errors.js`)

```json
{
  "status": 400,
  "failure_id": "CASE000001-fail-01",
  "name": "unsupported_format",
  "reported_name": "unsupported_format",
  "module_id": "MOD001",
  "case_id": "CASE000001",
  "input_id": "CASE000001-input-01",
  "detail": "extension bmp is not in jpg, jpeg, png, webp",
  "timestamp": "2026-11-19T08:26:00+06:00",
  "isNetworkError": false
}
```

When `fetch()` rejects due to an offline backend or `AbortController` timeout:
- `status`: `0`
- `name`: `"timeout"` (on abort) or `"unexpected_error"` (on network disconnect)
- `module_id`: `"MOD014"`
- `detail`: `"Backend API is unreachable or timed out. No decision was produced."`
- `isNetworkError`: `true`
