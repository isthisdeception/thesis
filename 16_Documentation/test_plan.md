# Consolidated Testing Plan & UAT Protocol (STEP-067 / §8.9)

**Date:** 2026-11-19  
**Version:** `0.1.0`  
**Runner:** `17_Automation/run_all_tests.py`

---

## 1. Testing Tiers & Coverage Matrix (§8.9)

| Tier | Scope | Location | Determinism / Isolation |
|---|---|---|---|
| **AI Forensic Analyst Unit & Integration** | `MOD001`–`MOD012`, `MOD015`–`MOD018` (`intake`, `validation`, `9+1` collectors, `EV` registry, fusion strategies, E4 confidence calibration, evidence-only decision, A.9 explainability, `EV`-grounded reasoning, Template 24 reports, E2E `pipeline.py`) | `11_AI_Forensic_System/tests/` (8 test files, 55 tests) | Temp registries & injected `FaceCounter`/`Predictor` stubs; zero external network calls |
| **Backend Unit & API** | Django `manage.py check`, 7 single-responsibility apps, env config (`dev`/`test`/`prod`), 7 log channels, all 10 `MOD013` REST endpoints, serializers, throttles, `MOD016` error envelopes without stack traces | `13_Backend/tests/test_scaffold_and_engine.py`, `test_api_endpoints.py` (9 tests) | `APIClient` + temp `FORENSIC_MEDIA_ROOT` & CSVs (`async_mode=eager`) |
| **Backend Smoke & Regression** | Health/version smoke, 6-scenario failure/decision regression matrix (`Fake`, `Real`, `Unknown`, `no_face`, `multiple_faces`, `corrupted_image`), empty & unsupported uploads, `case_registry.csv` append-only invariant | `13_Backend/tests/test_smoke_regression.py` (8 tests) | Parametrized deterministic cases |
| **Live HTTP & CORS Integration** | Ephemeral Django WSGI server (`async_mode=thread`), CORS preflight for `http://localhost:5173`, `202 Accepted` async polling, `-input-01` & `-input-02` media versioning, `/version` & `/health` | `13_Backend/tests/test_system_integration.py` (1 test) | Isolated temp storage + loopback TCP only |
| **Frontend Component & Page Suites** | Static zero-direct-`fetch` enforcement, API client normalization, 24 reusable accessible components, `ErrorBoundary`, all 14 canonical pages, `MOD014` `Inconclusive`/`Unknown` + offline API checks, regression failure paths | `12_Web/src/__tests__/scaffold_and_components.test.jsx`, `investigation_pages.test.jsx`, `regression_and_errors.test.jsx` (12 tests) | `jsdom` + mocked `fetch()` + `vite build` check |
| **Live Cross-Tier React-to-Django** | Real Django WSGI server + real React pages (`SystemInfoPage` → `ImageUploadPage` → `InvestigationProgressPage` → `ResultSummaryPage` → `EvidenceViewerPage` → `ExplanationViewerPage` → `ReportViewerPage`) over HTTP | `17_Automation/verify_integration.py` + `12_Web/src/__tests__/live_integration.test.jsx` (1 test) | Live loopback HTTP (`VITE_API_BASE_URL` dynamically injected) |
| **Automated User Acceptance Testing (UAT)** | 6 end-to-end acceptance scenarios against live Django API (real fake, real authentic, corrupted PNG, no-face, unsupported `.bmp`, missing model `MODEL9999`) | `17_Automation/run_uat.py` (6 scenarios) | Live loopback WSGI server + temp storage |

> **Environment Note (Research Pipeline Suites):** Standalone dataset preprocessing and offline experiment-analysis test suites (`04_Preprocessing/tests/`, `17_Automation/tests/`) depend on `pandas` C-extension `.pyd` binaries (and `17_Automation/statistics/` shadowing stdlib `statistics` when invoked from inside `17_Automation/`). On hosts where Windows Application Control restricts `pandas` `.pyd` DLL loading, those offline experiment tests are run inside the locked Kaggle/conda runtime (`environment/versions.lock.md`), while the full forensic + backend + frontend platform suites run locally without `pandas`.

---

## 2. UAT Scenario Matrix (`17_Automation/run_uat.py`)

| UAT ID | Input / Condition | Expected HTTP & Pipeline Behavior | Expected Decision / Outcome |
|---|---|---|---|
| **UAT-01** | Valid 64×64 PNG, 1 face, `MODEL0001` (`P(fake)=0.95`) | `POST /upload` → `202 Accepted`; polls to `Complete`; Template 24 JSON/MD/HTML reports with `git_commit` | `Fake`; all 4 confidences populated |
| **UAT-02** | Valid 64×64 PNG, 1 face, `MODEL0001` (`P(fake)=0.02`) | `POST /upload` → `202 Accepted`; polls to `Complete` | `Real`; `prediction_confidence != 0.02` (E4 calibrated) |
| **UAT-03** | Corrupted PNG byte stream | `POST /upload` → `202`; stops at `MOD002`; zero `decision.json`; `case_registry.csv` row has `Decision=""` | `failed` (`corrupted_image`) |
| **UAT-04** | Valid PNG with 0 faces | `POST /upload` → `202`; stops at `MOD002`; zero `decision.json` | `failed` (`no_face`) |
| **UAT-05** | Unsupported `.bmp` file | `POST /upload` → `400 Bad Request`; no image written to disk | `failed` (`unsupported_format`, `MOD001`) |
| **UAT-06** | Valid PNG with unregistered `MODEL9999` | `POST /upload` → `202`; `MOD004` records `model_unavailable`; pipeline recovers via `MOD008` | `Unknown`; `prediction_confidence=null`, `decision_confidence=null` |

---

## 3. Running the Consolidated Test Suite

```bash
.venv/Scripts/python.exe 17_Automation/run_all_tests.py
```
