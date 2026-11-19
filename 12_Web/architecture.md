# Frontend Architecture Specification (STEP-063 / MOD014)

**Date:** 2026-11-19  
**Status:** specified  
**Version:** `0.1.0`  
**Scope:** `12_Web/` (React + Vite + Tailwind CSS). No application code is written in this step; scaffolding and implementation begin in STEP-064 and STEP-065.

---

## 1. Binding Separation of Concerns (§8.1 & MOD014)

1. **The frontend owns the experience; the backend owns the investigation.** The frontend (`12_Web/`) never performs inference, never loads model weights, never computes image measurements, and never applies a threshold to a probability to choose `Real`, `Fake`, `Inconclusive`, or `Unknown`.
2. **All network requests live in `src/api/`.** React pages and components never call `fetch()` or `XMLHttpRequest` directly and never hardcode an API hostname or port. The base URL is read exclusively from `import.meta.env.VITE_API_BASE_URL` (via `src/api/config.js`).
3. **An investigation, never a bare verdict (`MOD014_spec.md`).** The UI never displays a bare `"Fake (99.8%)"` banner as the result. Every result screen displays:
   - The four-way decision word (`Real`, `Fake`, `Inconclusive`, or `Unknown`) from `decision.json`.
   - All four distinct confidence fields (`prediction_confidence`, `evidence_confidence`, `system_confidence`, `decision_confidence`) with their documented interpretations, explicitly showing `Empty (not estimated)` whenever a field is `null`.
   - The cited `EVxxxxxx` evidence IDs (`reasoning_path`) and per-item `MOD006` reliability qualities (`high`, `medium`, `low`, `unusable`).
   - The case `limitations` and `version_stamps` (`system_version`, `model_id`, `dataset_id`, `experiment_id`, `git_commit`).
4. **Error & uncertainty honesty.** If an investigation returns `Inconclusive` or `Unknown`, or if a `confidence` value is `null`, the UI renders that state explicitly. If the API is unreachable or returns a `MOD016` error envelope (`unsupported_format`, `corrupted_image`, `no_face`, `multiple_faces`, `model_unavailable`, `low_confidence`, `timeout`, `unexpected_error`), the UI shows the `MOD016` message and never substitutes a guessed verdict.

---

## 2. Folder Structure (`12_Web/src/`, §8.3)

```
12_Web/
├── .env.example                 # VITE_API_BASE_URL, VITE_POLL_INTERVAL_MS, VITE_REQUEST_TIMEOUT_MS
├── architecture.md              # This specification (STEP-063)
├── api_client_spec.md           # Centralized API client contract (STEP-063)
├── index.html                   # Entry HTML
├── package.json                 # React + Vite + Tailwind + Vitest dependencies (STEP-064)
├── vite.config.js               # Vite bundler + test config (STEP-064)
└── src/
    ├── api/                     # ONLY location allowed to perform HTTP fetch calls
    │   ├── config.js            # Reads VITE_API_BASE_URL & timeout/poll settings from env
    │   ├── errors.js            # Parses MOD016 error envelopes & network/timeout errors
    │   ├── http.js              # Low-level fetch wrapper with AbortController timeout
    │   └── forensicApi.js       # 10 typed endpoint functions matching 13_Backend/api_spec/api_spec.md
    ├── assets/                  # Static icons and SVGs (no committed case media)
    ├── components/              # 24 reusable, accessible UI components (§8.3)
    ├── context/                 # Global state providers (SystemContext, ThemeContext)
    ├── hooks/                   # Custom hooks (useInvestigation, usePolling, useSystemMeta)
    ├── layouts/                 # AppShellLayout, InvestigationLayout
    ├── pages/                   # 14 canonical pages (§8.3)
    ├── styles/                  # Tailwind directives & forensic theme tokens
    └── utils/                   # Pure formatting helpers (formatTimestamp, formatConfidence, never decisions)
```

---

## 3. Investigation UX & Progress Sequence (Module 14 / `MOD014_spec.md`)

When an image is uploaded to `POST /cases/{id}/upload`, the investigation progresses through the **nine canonical Module 14 stages** in exact order:

| Step | Exact `MOD014` Stage Label | Source Pipeline Stage | What the User Sees |
|---|---|---|---|
| 1 | `Uploading` | `MOD001` Input Management | File intake metadata (`input_id`, format, byte size) |
| 2 | `Validating` | `MOD002` Image Validation | Format decode, resolution, channels, noise check |
| 3 | `Detecting Face` | `MOD002` Face Gate | Single-face availability check |
| 4 | `Running Analysis` | `MOD004` Deep Learning Specialist | Registered detector execution (`MODEL0001`) |
| 5 | `Collecting Evidence` | `MOD003` + `MOD005` + `MOD006` | 9 independent collectors + `EV` ID registration & reliability scoring |
| 6 | `Evaluating Confidence` | `MOD007` + `MOD009` + `MOD008` | Rule-based fusion, E4-calibrated 4-way confidence, and 4-way decision |
| 7 | `Generating Explanation` | `MOD010` + `MOD011` | Data-only explanation record + `EV`-grounded reasoning sentences |
| 8 | `Preparing Report` | `MOD012` + `MOD015` | Template 24 JSON/Markdown/HTML report + `case_registry.csv` audit row |
| 9 | `Complete` | Terminal state | Full investigation workspace unlocked (`Result Summary`, `Evidence`, `Explanation`, `Report`) |

If any stage stops with a `MOD016` failure (`stage: "Failed"`), the progress timeline highlights the stopping step and renders the structured `MOD016` failure card (`failure_id`, `name`, `module_id`, `detail`, `timestamp`) with no decision card.

---

## 4. Page Inventory (14 Canonical Pages + Reserved Future Pages, §8.3)

| # | Page (`src/pages/`) | Route | Purpose | Key Components | API Dependencies (`src/api/forensicApi.js`) | Navigation Flow | Future Extensions |
|---|---|---|---|---|---|---|---|
| 1 | `LandingPage` | `/` | Introduce the AI Forensic Analyst as an evidence-driven investigation platform and show live system/model provenance | `Navbar`, `Card`, `Button`, `VersionBadge`, `StatusBadge`, `Footer` | `getHealth()`, `getVersion()` | CTAs to `/investigate/upload`, `/investigate`, `/about`, `/docs` | Quick-start demo case selector |
| 2 | `AboutProjectPage` | `/about` | Explain the research thesis, architectural invariants (detector never decides; evidence-only decision; E4 calibration), and evaluation findings (E7/E8/E9/E14) | `Card`, `Accordion`, `Table`, `MetricCard`, `VersionBadge` | `getVersion()` | Links to `/docs`, `/api-docs`, `/system` | Interactive architecture diagram |
| 3 | `InvestigationDashboardPage` | `/investigate` | Hub for active and recent in-session investigations, showing case ID, stage, decision badge, and quick links to sub-views | `CaseSummary`, `StatusBadge`, `Table`, `Button`, `EmptyState`, `Card` | `createCase()`, `getCaseDetail(id)`, `getCaseStatus(id)` | Starts new case → `/investigate/upload` or opens `/cases/:caseId/*` | Cross-session database history (`history` app) |
| 4 | `ImageUploadPage` | `/investigate/upload` (and `/cases/:caseId/upload`) | Allocate a case (if not yet allocated) and upload an image (`jpg`, `jpeg`, `png`, `webp`, ≤ 20 MB) with client-side preview and `MOD001` error display | `UploadArea`, `ImageViewer`, `Alert`, `Button`, `Card`, `ErrorState` | `createCase()`, `uploadCaseImage(caseId, file)` | On accepted upload → `/cases/:caseId/progress` | Batch upload (`MOD001` future extension) |
| 5 | `InvestigationProgressPage` | `/cases/:caseId/progress` | Poll `GET /cases/{id}/status` and display the 9 ordered `MOD014` progress stages (`Uploading` → `Complete`) or any `MOD016` stop record | `ProgressIndicator`, `Timeline`, `StatusBadge`, `Alert`, `ErrorState`, `LoadingSpinner` | `getCaseStatus(caseId)` | Auto-enables or navigates to `/cases/:caseId/result` on `Complete` | Server-Sent Events / WebSocket stream |
| 6 | `EvidenceViewerPage` | `/cases/:caseId/evidence` | Inspect all `MOD005` collector rows and `MOD006` validation rows (`EVxxxxxx`), filter by reliability (`high`/`medium`/`low`/`unusable`), and view dependency links | `EvidenceCard`, `Table`, `StatusBadge`, `Accordion`, `EmptyState` | `getCaseEvidence(caseId, { validatedOnly })` | Tabs to `/cases/:caseId/result`, `/explanation`, `/report` | Multimodal evidence tabs (audio/video/text) |
| 7 | `ResultSummaryPage` | `/cases/:caseId/result` | Present the evidence-based 4-way decision (`Real`/`Fake`/`Inconclusive`/`Unknown`), all 4 confidence gauges, `reasoning_path` `EV` citations, and limitations | `CaseSummary`, `ConfidenceGauge`, `StatusBadge`, `Timeline`, `Alert`, `Card`, `VersionBadge` | `getCaseDetail(caseId)`, `getCaseDecision(caseId)`, `getCaseReport(caseId, 'json')` | Links to `/cases/:caseId/evidence`, `/explanation`, `/report` | Side-by-side specialist comparison |
| 8 | `ExplanationViewerPage` | `/cases/:caseId/explanation` | Display data-only explainability records (`MOD010` `grad_cam`, `attention_maps`, `saliency`, `integrated_gradients`, `status: recorded | no_data`) and `MOD011` `EV`-grounded reasoning sentences | `Card`, `Table`, `Accordion`, `StatusBadge`, `Alert`, `EmptyState` | `getCaseExplanation(caseId, { includeReasoning: true })` | Links tocited `EV` rows in `/cases/:caseId/evidence` | SHAP, LIME, and counterfactual data panels |
| 9 | `ReportViewerPage` | `/cases/:caseId/report` | View and download the reproducible `MOD012` Template 24 forensic report in `JSON`, `Markdown`, or `HTML`, including full version and Git commit stamps | `ReportViewer`, `VersionBadge`, `Button`, `Card`, `Table` | `getCaseReport(caseId, format)` | Switch between `json`, `markdown`, `html`; back to `/cases/:caseId/result` | PDF export (`MOD012` future extension) |
| 10 | `SystemInfoPage` | `/system` | Display live `/health` checks (`media_root_writable`, registries readable) and `/version` provenance (`system_version`, `model_id`, `dataset_id`, `experiment_id`, `git_commit`, `fusion_strategy_id`, `confidence_formula_id`) | `MetricCard`, `VersionBadge`, `StatusBadge`, `Table`, `Card`, `Button` | `getHealth()`, `getVersion()` | Refresh health/version; links to `/api-docs` | Worker queue telemetry |
| 11 | `DocumentationPage` | `/docs` | User and researcher guide covering the 18 forensic modules, the 4 confidence definitions, the 4 decision words, and limitations | `Accordion`, `Card`, `Table` | None (static documentation + version badge from `SystemContext`) | Links to `/api-docs`, `/about`, `/investigate` | Searchable knowledge base |
| 12 | `ApiDocumentationPage` | `/api-docs` | Interactive reference for the 10 canonical `MOD013` REST endpoints (`POST /cases` through `GET /version`) and the `MOD016` error envelope | `Table`, `Accordion`, `Card`, `StatusBadge` | `getVersion()` | Links to `/system`, `/docs` | Live read-only endpoint tester |
| 13 | `NotFoundPage` | `*` (404) | Clear 404 page when a user visits an unknown route | `EmptyState`, `Button`, `Card` | None | Button back to `/` or `/investigate` | Suggested routes |
| 14 | `ErrorPage` | Error boundary fallback / `/error` | Catch unexpected UI rendering errors or unrecoverable API errors without exposing raw stack traces | `ErrorState`, `Alert`, `Button`, `Card` | None | Reset state and return to `/investigate` | Client error telemetry hook |

**Reserved future pages (§8.3):** `LoginPage` (`/login`), `CaseHistoryPage` (`/history`), `AdminPage` (`/admin`) — reserved until `accounts` and `history` backend apps are enabled.

---

## 5. Reusable Component Library Inventory (24 Components, §8.3)

Every component in `12_Web/src/components/` is pure, reusable, keyboard-accessible, and free of direct API `fetch` calls:

| # | Component | Purpose | Props Contract | Accessibility (WCAG / ARIA) | Extensibility |
|---|---|---|---|---|---|
| 1 | `Navbar` | Top navigation bar with brand, main route links, API health indicator, and version badge | `{ healthStatus, systemVersion, activePath }` | `<nav aria-label="Primary">`, `aria-current="page"`, keyboard focus ring | Auth menu slot |
| 2 | `Footer` | Page footer displaying system/model/dataset/experiment/Git-commit provenance | `{ versionInfo }` | `<footer>`, semantic `<dl>` for version stamps | Link columns |
| 3 | `Sidebar` | Case-level navigation sidebar across `Progress`, `Result`, `Evidence`, `Explanation`, and `Report` | `{ caseId, currentStage, decision, activeTab }` | `<aside aria-label="Case navigation">`, disabled state for unready tabs | Collapsible mobile drawer |
| 4 | `Button` | Standard action button (`primary`, `secondary`, `outline`, `danger`) | `{ variant, size, disabled, loading, type, onClick, children }` | Native `<button>`, `aria-busy={loading}`, visible focus outline | Icon prefix/suffix |
| 5 | `Card` | Framed surface container for forensic sections | `{ title, subtitle, actions, children, className }` | `<section>` with heading association | Collapsible header |
| 6 | `UploadArea` | Drag-and-drop and file-picker input for `.png`, `.jpg`, `.jpeg`, `.webp` up to 20 MB | `{ onFileSelect, disabled, maxBytes, acceptedFormats, error }` | `<label>` bound to `<input type="file">`, keyboard Enter/Space support, `aria-invalid` | Multi-file dropzone |
| 7 | `ProgressIndicator` | Visual 9-stage `MOD014` progress bar and current stage banner | `{ stage, stageHistory, status, progressPercent }` | `role="progressbar"`, `aria-valuenow`, `aria-valuemin="0"`, `aria-valuemax="100"`, `aria-live="polite"` | Sub-step timing |
| 8 | `StatusBadge` | Semantic badge for decisions (`Real`, `Fake`, `Inconclusive`, `Unknown`), qualities (`high`..`unusable`), and statuses | `{ label, tone, size }` | High-contrast text + icon/prefix (never color-only) | Custom tone map |
| 9 | `EvidenceCard` | Displays one `EVxxxxxx` row (`evidence_type`, `source_module`, `quality`, `status`, `confidence`, `description`, `processed_output`, `dependencies`) | `{ item, onSelectDependency }` | `<article aria-labelledby>`, explicit `Empty (null)` badge when confidence is `null` | Expandable raw JSON drawer |
| 10 | `ConfidenceGauge` | Renders one of the 4 `MOD009` confidence values (`0`–`1` or `null`) with its documented interpretation | `{ label, fieldKey, value, interpretation }` | `role="meter"` when numeric; explicit `"Not estimated (null)"` badge when `value === null` | Uncertainty interval band |
| 11 | `Timeline` | Ordered vertical step trace for `stage_history` or `MOD008` `reasoning_steps` | `{ steps, currentStep, failedStep }` | `<ol aria-label="Investigation timeline">`, `aria-current="step"` | Clickable `EV` step anchors |
| 12 | `Accordion` | Expandable disclosure panels for limitations, reasoning details, and docs | `{ items: [{ id, title, content, defaultOpen }] }` | `<button aria-expanded aria-controls>`, region `role="region"` | Controlled open state |
| 13 | `Table` | Structured data table for evidence registries, version stamps, and API specs | `{ columns, rows, caption, emptyMessage }` | `<table>`, `<caption>`, `<th scope="col">` | Column sorting & CSV export |
| 14 | `Modal` | Accessible dialog for inspecting full `EV` JSON payloads | `{ isOpen, title, onClose, children }` | `role="dialog"`, `aria-modal="true"`, Escape key handler, focus trap | Action footer |
| 15 | `Toast` | Non-blocking transient notification for copy/download events | `{ message, tone, onDismiss }` | `role="status"`, `aria-live="polite"` | Stacked toast queue |
| 16 | `Alert` | Inline callout for `MOD016` warnings (`low_confidence`), limitations, and notices | `{ title, tone, children, failureRecord }` | `role="alert"` for errors/warnings | Action links |
| 17 | `LoadingSpinner` | Accessible loading indicator with descriptive text | `{ label, size }` | `role="status"`, `aria-live="polite"` | Skeleton variant |
| 18 | `EmptyState` | Placeholder when a list or artifact is empty (`no_data` explanations, no cases yet) | `{ title, description, action }` | Semantic heading + action button | Illustration slot |
| 19 | `ErrorState` | Structured display of a `MOD016` `FailureRecord` or network error without stack traces | `{ error, onRetry }` | `role="alert"`, lists `failure_id`, `name`, `module_id`, `detail` | Diagnostic copy button |
| 20 | `ReportViewer` | Multi-format viewer (`JSON`, `Markdown`, `HTML`) and downloader for `MOD012` reports | `{ caseId, reportJson, reportMarkdown, reportHtml, activeFormat, onFormatChange }` | Tablist `role="tablist"`, `role="tab"`, `aria-selected` | Print stylesheet |
| 21 | `ImageViewer` | Local preview of the user-selected file prior to/during investigation (never fabricates heatmaps) | `{ fileUrl, filename, metadata }` | `<figure>`, `<img alt>`, dimensions caption | Zoom controls |
| 22 | `MetricCard` | Key-value summary card for latency, evidence count, and health status | `{ label, value, unit, detail, tone }` | Semantic `<dl>` / `<dt>` / `<dd>` | Trend indicator |
| 23 | `VersionBadge` | Compact provenance pill showing `system_version`, `model_id`, and short `git_commit` | `{ systemVersion, modelId, gitCommit, datasetId, experimentId }` | `title` + `aria-label` with full provenance string | Popover breakdown |
| 24 | `CaseSummary` | Header card summarizing `case_id`, `decision`, `stage`, `model_id`, and `reasoning_path` IDs | `{ caseDetail, decisionRecord }` | Semantic `<header>`, never shows a bare probability as the decision | Quick-jump links |

---

## 6. State Management Boundaries (§8.3)

| Scope | Holder | State Owned | Rule |
|---|---|---|---|
| **Global State** | `SystemContext` (`src/context/SystemContext.jsx`) | `/health` status, `/version` provenance (`system_version`, `model_id`, `dataset_id`, `experiment_id`, `git_commit`), configured API base URL | Read once on app mount + refreshable on `/system`. Avoids global storage of per-case payloads. |
| **Global UI State** | `ThemeContext` (`src/context/ThemeContext.jsx`) | High-contrast forensic theme mode (`light` / `dark` token toggle) and active toast notifications | Pure UI presentation state. |
| **Local / Case State** | `useInvestigation(caseId)` (`src/hooks/useInvestigation.js`) | `caseDetail`, `jobStatus` (`stage`, `stage_history`, `progress_percent`, `failures`), `evidence`, `decision`, `explanation`, `report`, `loading`, and `error` (`MOD016` normalized error) | Scoped to the active `caseId`. Polls `getCaseStatus(caseId)` while `status === "running"` and loads `decision`, `evidence`, `explanation`, and `report` once `stage === "Complete"`. |
