<!--
================================================================================
TEMPLATE NAME: Template 16 — API Specification
PURPOSE: Document backend REST endpoints (§8.5 & Module 13).
WHEN USED: STEP-060, before backend scaffold and endpoint implementation.
OWNER: API Designer
INPUTS: MASTER_RESEARCH_OPERATING_SYSTEM.md (§8.1–§8.9), 11_AI_Forensic_System/specs/MOD013_spec.md
OUTPUTS: api_spec.md (this file)
REQUIRED SECTIONS: Endpoint, Method, Purpose, Request, Response, Errors, Authentication, Examples, Version
OPTIONAL SECTIONS: None
VALIDATION RULES: Must specify errors. No stack traces exposed to users.
NAMING CONVENTION: api_spec.md
FOLDER LOCATION: 13_Backend/api_spec
DEFINITION OF DONE: All 10 canonical endpoints specified with Request, Response, Errors, Authentication, Examples, Version.
COMMON MISTAKES: Missing error responses; frontend/inference logic in the API layer; hardcoded URLs.
RELATED TEMPLATES: Template 17
================================================================================
-->

# Canonical REST API Specification (STEP-060 / MOD013)

**Date:** 2026-11-18  
**Version:** `0.1.0`  
**Base Path:** Configured via environment variable (`VITE_API_BASE_URL` on client; `/` or `/api/v1` routed identically on backend; never hardcoded).  
**Content-Type:** `application/json` (except `POST /cases/{id}/upload` which accepts `multipart/form-data`, and `GET /cases/{id}/report?format=markdown|html`).

---

## Global Error Envelope (§8.7 & MOD016)

Every `4xx` or `5xx` response returns a structured JSON error envelope and **never** includes a Python stack trace:

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

---

## 1. API Spec: `POST /cases`

**Method:** `POST`  
**Purpose:** Allocate a new immutable `CASExxxxxx` identifier, initialize the per-case storage directory, and create the initial job status record (`stage: "Created"`).  
**Request:**
- Headers: `Content-Type: application/json` (optional body)
- Body (optional JSON):
  - `model_id` (optional `string`, defaults to `FORENSIC_MODEL_ID` = `"MODEL0001"`)
  - `configuration` (optional `string`, defaults to `"rule_based/e4_calibrated_v1"`)

**Response:** `201 Created`
- `case_id` (`string`, `CASE` + 6 digits)
- `status` (`"created"`)
- `stage` (`"Created"`)
- `model_id` (`string`)
- `configuration` (`string`)
- `created_timestamp` (ISO-8601 `string`)

**Errors:**
- `400 Bad Request` (`unexpected_error`): Invalid `model_id` format or malformed JSON body.
- `429 Too Many Requests` (`unexpected_error`): Rate limit exceeded.
- `500 Internal Server Error` (`unexpected_error`): Storage directory or case registry could not be accessed.

**Authentication:** None in v0.1.0 (reserved for future `accounts` app per §8.5).  
**Examples:**
```http
POST /cases HTTP/1.1
Content-Type: application/json

{"model_id": "MODEL0001"}
```
```json
{
  "case_id": "CASE000001",
  "status": "created",
  "stage": "Created",
  "model_id": "MODEL0001",
  "configuration": "rule_based/e4_calibrated_v1",
  "created_timestamp": "2026-11-18T22:50:00+06:00"
}
```
**Version:** `0.1.0`

---

## 2. API Spec: `GET /cases/{id}`

**Method:** `GET`  
**Purpose:** Return the case record from `case_registry.csv` (`MOD015`) together with the live job status for `case_id`.  
**Request:**
- Path parameter: `id` (`string`, matching `^CASE\d{6}$`)

**Response:** `200 OK`
- `case_id` (`string`)
- `status` (`"created" | "running" | "completed" | "failed"`)
- `stage` (`string`, current `MOD014` stage label)
- `input_id` (`string | null`)
- `evidence_ids` (`list[string]`)
- `decision` (`"Real" | "Fake" | "Inconclusive" | "Unknown" | ""`)
- `model_id` (`string`)
- `version` (`string`)
- `configuration` (`string`)
- `execution_time_seconds` (`number | null`)
- `errors` (`list[string]`, `MOD016` failure IDs)
- `warnings` (`list[string]`, `MOD016` warning IDs)
- `timestamp` (ISO-8601 `string`)

**Errors:**
- `400 Bad Request` (`unexpected_error`): `id` does not match `^CASE\d{6}$`.
- `404 Not Found` (`unexpected_error`): `case_id` does not exist.

**Authentication:** None in v0.1.0.  
**Examples:**
```http
GET /cases/CASE000001 HTTP/1.1
```
```json
{
  "case_id": "CASE000001",
  "status": "completed",
  "stage": "Complete",
  "input_id": "CASE000001-input-01",
  "evidence_ids": ["EV000001", "EV000002", "EV000003", "EV000004", "EV000005", "EV000006"],
  "decision": "Fake",
  "model_id": "MODEL0001",
  "version": "0.1.0",
  "configuration": "rule_based/e4_calibrated_v1",
  "execution_time_seconds": 0.0621,
  "errors": [],
  "warnings": [],
  "timestamp": "2026-11-18T22:50:02+06:00"
}
```
**Version:** `0.1.0`

---

## 3. API Spec: `POST /cases/{id}/upload`

**Method:** `POST`  
**Purpose:** Upload one image file for `case_id`, run `MOD001` intake immediately, and—if accepted—trigger the asynchronous `forensic_engine` investigation pipeline (`MOD002`–`MOD012`, `MOD015`).  
**Request:**
- Path parameter: `id` (`string`, matching `^CASE\d{6}$`)
- Headers: `Content-Type: multipart/form-data`
- Form fields:
  - `file` (required binary file; allowed extensions `jpg`, `jpeg`, `png`, `webp`; max `20 MB`)

**Response:** `202 Accepted` (or `200 OK` when `FORENSIC_ASYNC_MODE=eager` completes synchronously)
- `case_id` (`string`)
- `input_id` (`string`, `{case_id}-input-{seq}`)
- `intake` (`input_metadata.json` written by `MOD001`, without exposing server filesystem paths)
- `job_status` (`"running" | "completed" | "failed"`)
- `stage` (`string`, `MOD014` stage label)

**Errors:**
- `400 Bad Request` (`unsupported_format` or `unexpected_error`): Missing `file`, empty file (`0` bytes), unsupported extension, or file size exceeding `20 MB`. Returns the `MOD016` record; the rejected file is not stored on disk.
- `404 Not Found` (`unexpected_error`): `case_id` does not exist.
- `429 Too Many Requests` (`unexpected_error`): Upload rate limit exceeded.

**Authentication:** None in v0.1.0.  
**Examples:**
```http
POST /cases/CASE000001/upload HTTP/1.1
Content-Type: multipart/form-data; boundary=---boundary

-----boundary
Content-Disposition: form-data; name="file"; filename="suspect.png"
Content-Type: image/png

<binary image bytes>
-----boundary--
```
```json
{
  "case_id": "CASE000001",
  "input_id": "CASE000001-input-01",
  "intake": {
    "input_id": "CASE000001-input-01",
    "case_id": "CASE000001",
    "declared_filename": "suspect.png",
    "byte_size": 12840,
    "declared_format": "png",
    "received_timestamp": "2026-11-18T22:50:01+06:00",
    "status": "accepted",
    "failure_id": null
  },
  "job_status": "running",
  "stage": "Uploading"
}
```
**Version:** `0.1.0`

---

## 4. API Spec: `GET /cases/{id}/status`

**Method:** `GET`  
**Purpose:** Poll the current investigation progress stage (`MOD014`) and any structured `MOD016` failures/warnings for `case_id`.  
**Request:**
- Path parameter: `id` (`string`, matching `^CASE\d{6}$`)

**Response:** `200 OK`
- `case_id` (`string`)
- `status` (`"created" | "running" | "completed" | "failed"`)
- `stage` (`string`, one of `"Created"`, `"Uploading"`, `"Validating"`, `"Detecting Face"`, `"Running Analysis"`, `"Collecting Evidence"`, `"Evaluating Confidence"`, `"Generating Explanation"`, `"Preparing Report"`, `"Complete"`, `"Failed"`)
- `stage_history` (`list[string]`, ordered `MOD014` labels completed so far)
- `progress_percent` (`integer`, `0`–`100` derived from `stage_history`)
- `input_id` (`string | null`)
- `failures` (`list[object]`, structured `MOD016` records if any occurred)
- `updated_timestamp` (ISO-8601 `string`)

**Errors:**
- `404 Not Found` (`unexpected_error`): `case_id` does not exist.

**Authentication:** None in v0.1.0.  
**Examples:**
```http
GET /cases/CASE000001/status HTTP/1.1
```
```json
{
  "case_id": "CASE000001",
  "status": "completed",
  "stage": "Complete",
  "stage_history": [
    "Uploading",
    "Validating",
    "Detecting Face",
    "Running Analysis",
    "Collecting Evidence",
    "Evaluating Confidence",
    "Generating Explanation",
    "Preparing Report",
    "Complete"
  ],
  "progress_percent": 100,
  "input_id": "CASE000001-input-01",
  "failures": [],
  "updated_timestamp": "2026-11-18T22:50:02+06:00"
}
```
**Version:** `0.1.0`

---

## 5. API Spec: `GET /cases/{id}/evidence`

**Method:** `GET`  
**Purpose:** Return all `MOD005`-registered and `MOD006`-validated evidence rows belonging to `case_id` from `evidence_registry.csv` (`MOD013_spec.md`), with server filesystem paths stripped.  
**Request:**
- Path parameter: `id` (`string`, matching `^CASE\d{6}$`)
- Query parameter (optional): `validated_only` (`"true" | "false"`, default `"false"`)

**Response:** `200 OK`
- `case_id` (`string`)
- `evidence_ids` (`list[string]`)
- `count` (`integer`)
- `items` (`list[object]`, each containing `evidence_id`, `evidence_type`, `source_module`, `timestamp`, `confidence`, `description`, `raw_output`, `processed_output`, `quality`, `dependencies`, `owner`, `version`, `status`, `created`, `updated`)

**Errors:**
- `404 Not Found` (`unexpected_error`): `case_id` does not exist.

**Authentication:** None in v0.1.0.  
**Examples:**
```http
GET /cases/CASE000001/evidence?validated_only=true HTTP/1.1
```
```json
{
  "case_id": "CASE000001",
  "evidence_ids": ["EV000011"],
  "count": 1,
  "items": [
    {
      "evidence_id": "EV000011",
      "evidence_type": "face_detection",
      "source_module": "MOD006",
      "timestamp": "2026-11-18T22:50:01+06:00",
      "confidence": null,
      "description": "1 face detected | validation: no_reliability_concern",
      "raw_output": {
        "case_id": "CASE000001",
        "collector_evidence_id": "EV000001",
        "collector_source_module": "MOD003",
        "face_count": 1,
        "input_id": "CASE000001-input-01"
      },
      "processed_output": {
        "reliability": "high",
        "unit": "count",
        "validation_reason": "no_reliability_concern",
        "value": 1
      },
      "quality": "high",
      "dependencies": ["EV000001"],
      "owner": "MOD006",
      "version": "0.1.0",
      "status": "validated",
      "created": "2026-11-18T22:50:01+06:00",
      "updated": "2026-11-18T22:50:01+06:00"
    }
  ]
}
```
**Version:** `0.1.0`

---

## 6. API Spec: `GET /cases/{id}/decision`

**Method:** `GET`  
**Purpose:** Return `decision.json` written by `MOD008` **unchanged** (`MOD013_spec.md`: *"A later API test checks that `GET /cases/{id}/decision` returns `decision.json` unchanged and does not add a label."*).  
**Request:**
- Path parameter: `id` (`string`, matching `^CASE\d{6}$`)

**Response:** `200 OK`
- Exact contents of `decision.json` (`case_id`, `decision`, `fused_evidence_id`, `confidence_evidence_id`, `reasoning_path`, `decision_metadata`).

**Errors:**
- `404 Not Found` (`unexpected_error`): `case_id` does not exist, or `decision.json` was not produced (e.g., investigation still running or stopped at intake/validation; if stopped, the `MOD016` failure record is returned).

**Authentication:** None in v0.1.0.  
**Examples:**
```http
GET /cases/CASE000001/decision HTTP/1.1
```
```json
{
  "case_id": "CASE000001",
  "decision": "Fake",
  "fused_evidence_id": "EV000022",
  "confidence_evidence_id": "EV000024",
  "reasoning_path": ["EV000011", "EV000020", "EV000022", "EV000024"],
  "decision_metadata": {
    "module_id": "MOD008",
    "version": "0.1.0",
    "strategy_id": "rule_based",
    "rule_id": "validated_positive_lean_fake",
    "rule_version": "0.1.0",
    "rule_status": "approved in DEC0010 (Human, 2026-11-18)",
    "lean": "positive_class",
    "confidence": {
      "prediction_confidence": 0.971745,
      "evidence_confidence": 0.9,
      "system_confidence": 0.9,
      "decision_confidence": 0.795492
    },
    "reasoning_steps": [],
    "warning_failure_ids": [],
    "timestamp": "2026-11-18T22:50:02+06:00"
  }
}
```
**Version:** `0.1.0`

---

## 7. API Spec: `GET /cases/{id}/explanation`

**Method:** `GET`  
**Purpose:** Return `explanation.json` written by `MOD010` (data only, per Canonical Figure Policy A.9) together with the grounded reasoning record (`reasoning.json` from `MOD011`) when requested.  
**Request:**
- Path parameter: `id` (`string`, matching `^CASE\d{6}$`)
- Query parameter (optional): `include_reasoning` (`"true" | "false"`, default `"false"` — when `"false"`, returns `explanation.json` unchanged).

**Response:** `200 OK`
- `case_id` (`string`)
- `module_id` (`"MOD010"`)
- `version` (`"0.1.0"`)
- `figure_policy` (`"A.9_data_only_no_rendered_images"`)
- `methods` (`list[object]`, each with `method`, `status`, `evidence_id`, `collector_evidence_id`, `quality`, `model_id`, `data`)
- `supporting_ids` (`list[string]`)
- `unresolved` (`list[object]`)
- `timestamp` (ISO-8601 `string`)
- `reasoning` (included only when `?include_reasoning=true`: contents of `reasoning.json` from `MOD011`)

**Errors:**
- `404 Not Found` (`unexpected_error`): `case_id` does not exist or `explanation.json` has not been generated.

**Authentication:** None in v0.1.0.  
**Examples:**
```http
GET /cases/CASE000001/explanation HTTP/1.1
```
```json
{
  "case_id": "CASE000001",
  "module_id": "MOD010",
  "version": "0.1.0",
  "figure_policy": "A.9_data_only_no_rendered_images",
  "methods": [
    {
      "method": "grad_cam",
      "status": "no_data",
      "evidence_id": "EV000019",
      "collector_evidence_id": "EV000009",
      "quality": "high",
      "model_id": null,
      "data": null
    },
    {
      "method": "attention_maps",
      "status": "no_data",
      "evidence_id": null,
      "collector_evidence_id": null,
      "quality": null,
      "model_id": null,
      "data": null
    },
    {
      "method": "saliency",
      "status": "no_data",
      "evidence_id": null,
      "collector_evidence_id": null,
      "quality": null,
      "model_id": null,
      "data": null
    },
    {
      "method": "integrated_gradients",
      "status": "no_data",
      "evidence_id": null,
      "collector_evidence_id": null,
      "quality": null,
      "model_id": null,
      "data": null
    }
  ],
  "supporting_ids": ["EV000019"],
  "unresolved": [],
  "timestamp": "2026-11-18T22:50:02+06:00"
}
```
**Version:** `0.1.0`

---

## 8. API Spec: `GET /cases/{id}/report`

**Method:** `GET`  
**Purpose:** Return the reproducible forensic case report generated by `MOD012` (`{case_id}_report.json`, `{case_id}_report.md`, or `{case_id}_report.html`).  
**Request:**
- Path parameter: `id` (`string`, matching `^CASE\d{6}$`)
- Query parameter (optional): `format` (`"json" | "markdown" | "html"`, default `"json"`)

**Response:** `200 OK`
- When `format=json` (`Content-Type: application/json`): exact contents of `{case_id}_report.json` (`case_id`, `module_id`, `input_summary`, `evidence_summary`, `model_results`, `decision`, `confidence`, `reasoning`, `explanation`, `limitations`, `recommendations`, `execution_stats`, `version_stamps`, `timestamp`).
- When `format=markdown` (`Content-Type: text/markdown; charset=utf-8`): exact contents of `{case_id}_report.md` (Template 24).
- When `format=html` (`Content-Type: text/html; charset=utf-8`): exact contents of `{case_id}_report.html`.

**Errors:**
- `400 Bad Request` (`unexpected_error`): Unsupported `format` query value.
- `404 Not Found` (`unexpected_error`): `case_id` does not exist or report was not generated.

**Authentication:** None in v0.1.0.  
**Examples:**
```http
GET /cases/CASE000001/report?format=json HTTP/1.1
```
```json
{
  "case_id": "CASE000001",
  "module_id": "MOD012",
  "input_summary": {
    "input_id": "CASE000001-input-01",
    "intake_status": "accepted",
    "validation_status": "passed",
    "declared_format": "png",
    "byte_size": 12840
  },
  "evidence_summary": [],
  "model_results": {
    "evidence_id": "EV000020",
    "collector_evidence_id": "EV000010",
    "model_id": "MODEL0001",
    "probability": 0.95,
    "threshold": 0.3950566053390503,
    "quality": "high"
  },
  "decision": {
    "decision": "Fake",
    "fused_evidence_id": "EV000022",
    "confidence_evidence_id": "EV000024",
    "reasoning_path": ["EV000011", "EV000020", "EV000022", "EV000024"],
    "strategy_id": "rule_based",
    "rule_id": "validated_positive_lean_fake",
    "warning_failure_ids": []
  },
  "confidence": {
    "evidence_id": "EV000024",
    "formula_id": "e4_calibrated_v1",
    "prediction_confidence": 0.971745,
    "evidence_confidence": 0.9,
    "system_confidence": 0.9,
    "decision_confidence": 0.795492
  },
  "reasoning": {},
  "explanation": {},
  "limitations": [],
  "recommendations": [],
  "execution_stats": {
    "execution_time_seconds": 0.0621,
    "evidence_count": 24,
    "error_count": 0,
    "warning_count": 0
  },
  "version_stamps": {
    "system_version": "0.1.0",
    "model_id": "MODEL0001",
    "model_version": "1.0",
    "dataset_id": "DS0001/v1.0/PP0001",
    "experiment_id": "EXP0001",
    "git_commit": "bfaa07d"
  },
  "timestamp": "2026-11-18T22:50:02+06:00"
}
```
**Version:** `0.1.0`

---

## 9. API Spec: `GET /health`

**Method:** `GET`  
**Purpose:** Lightweight service health check (`MOD013_spec.md`: *"GET /health and GET /version do not load a case."*). Verifies that the backend process is alive and that configured storage and registry paths are reachable.  
**Request:** None.  
**Response:** `200 OK`
- `status` (`"ok" | "degraded"`)
- `service` (`"ai-forensic-analyst-backend"`)
- `environment` (`"dev" | "test" | "prod"`)
- `checks`:
  - `media_root_writable` (`boolean`)
  - `evidence_registry_readable` (`boolean`)
  - `case_registry_readable` (`boolean`)
  - `model_registry_readable` (`boolean`)
- `timestamp` (ISO-8601 `string`)

**Errors:**
- `503 Service Unavailable` (`unexpected_error`): One or more required registry or storage paths are inaccessible.

**Authentication:** None.  
**Examples:**
```http
GET /health HTTP/1.1
```
```json
{
  "status": "ok",
  "service": "ai-forensic-analyst-backend",
  "environment": "dev",
  "checks": {
    "media_root_writable": true,
    "evidence_registry_readable": true,
    "case_registry_readable": true,
    "model_registry_readable": true
  },
  "timestamp": "2026-11-18T22:50:00+06:00"
}
```
**Version:** `0.1.0`

---

## 10. API Spec: `GET /version`

**Method:** `GET`  
**Purpose:** Return full reproducibility version provenance (`system_version`, `api_version`, `model_id`, `model_version`, `dataset_id`, `experiment_id`, `git_commit`, `fusion_strategy_id`, `confidence_formula_id`) without loading a case or model weights (`MOD013_spec.md`).  
**Request:** None.  
**Response:** `200 OK`
- `system_version` (`string`, `"0.1.0"`)
- `api_version` (`string`, `"0.1.0"`)
- `model_id` (`string`, e.g. `"MODEL0001"`)
- `model_version` (`string`, e.g. `"1.0"`)
- `dataset_id` (`string`, e.g. `"DS0001/v1.0/PP0001"`)
- `experiment_id` (`string`, e.g. `"EXP0001"`)
- `git_commit` (`string`)
- `fusion_strategy_id` (`string`, `"rule_based"`)
- `confidence_formula_id` (`string`, `"e4_calibrated_v1"`)
- `timestamp` (ISO-8601 `string`)

**Errors:**
- `500 Internal Server Error` (`unexpected_error`): Model registry entry for the configured `FORENSIC_MODEL_ID` could not be resolved.

**Authentication:** None.  
**Examples:**
```http
GET /version HTTP/1.1
```
```json
{
  "system_version": "0.1.0",
  "api_version": "0.1.0",
  "model_id": "MODEL0001",
  "model_version": "1.0",
  "dataset_id": "DS0001/v1.0/PP0001",
  "experiment_id": "EXP0001",
  "git_commit": "bfaa07d",
  "fusion_strategy_id": "rule_based",
  "confidence_formula_id": "e4_calibrated_v1",
  "timestamp": "2026-11-18T22:50:00+06:00"
}
```
**Version:** `0.1.0`
