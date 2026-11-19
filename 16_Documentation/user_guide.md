# User Guide — AI Forensic Analyst Web Platform (`MOD014`)

**Version:** `0.1.0`  
**Date:** 2026-11-19  
**Prerequisites:** Backend and frontend running locally per [installation.md](./installation.md) (default UI: `http://localhost:5173`).

---

## 1. Running an Investigation Step-by-Step

1. **Start at Home or New Investigation (`/investigate/upload`):**
   - Check the top navigation bar or footer to confirm backend health (`/api/v1/health`) and active model provenance (`MODEL0001`, dataset `DS0001/v1.0/PP0001`).
   - Select one image file (`.jpg`, `.jpeg`, `.png`, or `.webp`; non-empty; maximum `20 MB`).
   - Submit the upload. The UI calls `POST /api/v1/cases` followed by `POST /api/v1/cases/{id}/upload` and navigates automatically to the live progress view.

2. **Monitor Live Investigation Stages (`/cases/:caseId/progress`):**
   - The UI polls `GET /api/v1/cases/{id}/status` across the 9 canonical `MOD014` stages:
     `Uploading` → `Validating` → `Detecting Face` → `Running Analysis` → `Collecting Evidence` → `Evaluating Confidence` → `Generating Explanation` → `Preparing Report` → `Complete`.
   - If intake or validation stops the case (for example `no_face` or `corrupted_image`), progress stops cleanly and displays the structured `MOD016` failure banner with diagnostic detail.

3. **Review the Case Decision & Confidence (`/cases/:caseId/result`):**
   - Every completed case presents an investigation summary rather than a single percentage banner.
   - Review the **Decision** badge (`Real`, `Fake`, `Inconclusive`, or `Unknown`), all **four confidence meters**, cited **`EV` IDs**, system limitations, and version provenance.

4. **Inspect Individual Evidence Items (`/cases/:caseId/evidence`):**
   - Filter items by `MOD006` reliability quality (`high`, `medium`, `low`, `unusable`) or inspect raw/processed measurements per `EVxxxxxx` row (e.g., frequency artifacts, metadata, face detection count, deep learning specialist probability and frozen threshold `0.3951`).

5. **Inspect Explainability & Grounded Reasoning (`/cases/:caseId/explanation`):**
   - View per-method explainability data (`grad_cam`, `attention_maps`, `saliency`, `integrated_gradients`). Unpopulated methods display explicitly as `no_data` (`data: null`) rather than placeholder heatmaps.
   - Read the `MOD011` forensic reasoning narrative, where every statement cites the exact `EVxxxxxx` record(s) backing it.

6. **Export or Read the Reproducible Report (`/cases/:caseId/report`):**
   - Switch between **JSON**, **Markdown** (Template 24), and **HTML** views served by `GET /cases/{id}/report?format=...` and download or inspect the full stamped report.

---

## 2. Interpreting Decisions & Confidence Values

### 2.1 The Four Decision Outcomes (`MOD008`)

| Decision | When It Applies | How to Interpret |
|---|---|---|
| **`Fake`** | Fused lean is `positive_class`, no unresolved evidence conflicts, and `decision_confidence >= 0.50` | Validated evidence supports synthetic/manipulated origin at the calibrated threshold |
| **`Real`** | Fused lean is `negative_class`, no unresolved evidence conflicts, and `decision_confidence >= 0.50` | Validated evidence supports authentic capture, subject to known cross-dataset limitations |
| **`Inconclusive`** | Evidence items conflict (`contested` lean) OR `decision_confidence < 0.50` | Signals disagree or lack sufficient reliability for a binary conclusion — manual review required |
| **`Unknown`** | Directional detector evidence is missing (`no_directional_evidence`, e.g., `model_unavailable`) | No model score could be validated; UI displays `Empty (not estimated)` where applicable |

### 2.2 The Four Confidence Metrics (`MOD009`)

Raw detector probability $P(\text{fake})$ is **not** diagnostic certainty. The interface displays four separate values (`0.0`–`1.0` or `Empty (not estimated)` when `null`):

1. **`prediction_confidence`:** E4 empirical accuracy calibrated on the `EVAL0001` validation split around the frozen threshold (`0.3951`).
2. **`evidence_confidence`:** Aggregate `MOD006` reliability across validated collector rows.
3. **`system_confidence`:** Pipeline completion health score across collectors and inference stages.
4. **`decision_confidence`:** Combined certainty metric evaluated by `MOD008` when determining `Real`/`Fake` vs. `Inconclusive`.

---

## 3. Navigation Reference (`12_Web` Routes)

| Route | Page | Purpose |
|---|---|---|
| `/` | Landing Page | System overview and entry into investigations |
| `/investigate` | Dashboard | Look up an existing `CASExxxxxx` ID or view recent status |
| `/investigate/upload` | Image Upload | Allocate a case (`POST /cases`) and upload media |
| `/cases/:caseId/progress` | Investigation Progress | Live 9-stage `MOD014` polling view |
| `/cases/:caseId/result` | Result Summary | Decision badge, 4 confidence gauges, cited `EV` IDs, limitations |
| `/cases/:caseId/evidence` | Evidence Viewer | Filterable `EVxxxxxx` table by `MOD006` quality |
| `/cases/:caseId/explanation` | Explanation & Reasoning | Data-only explainability methods + `EV`-grounded prose |
| `/cases/:caseId/report` | Report Viewer | Interactive `JSON`, `Markdown`, and `HTML` case report |
| `/system` | System Info | Live `/health` checks and `/version` provenance |
| `/docs`, `/api-docs`, `/about` | Platform Docs | Interactive reference for `MOD001`–`MOD018` and REST endpoints |

---

## 4. Troubleshooting Common Errors (`MOD016`)

- **`unsupported_format`:** Upload a `.jpg`, `.jpeg`, `.png`, or `.webp` image within `20 MB` and non-empty bytes. Rejected files are never written to disk.
- **`corrupted_image`:** The file header/extension did not match valid decodable image bytes; re-export the image cleanly and retry.
- **`no_face` / `multiple_faces`:** `MOD002` requires a single detectable face before forensic collectors execute. Crop to a single subject face and start a new case.
- **`model_unavailable` (yields `Unknown` decision):** `FORENSIC_ARTIFACT_ROOT` is unset or `MODEL0001_export.pkl` is absent locally. Either mount the trained FastAI export directory or continue inspecting non-DL forensic evidence collectors (`frequency_domain`, `compression_artifacts`, `texture_analysis`, etc.).
- **`Network / Backend Unreachable`:** Verify Django is running (`13_Backend/manage.py runserver 127.0.0.1:8000`) and check CORS settings in `13_Backend/.env`.
