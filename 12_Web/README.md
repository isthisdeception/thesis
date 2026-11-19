# 12_Web

**Purpose:** React + Vite + Tailwind frontend.

## Contents
Pages, layouts, components, hooks, api, context, assets, styles, docs.

STEP-063 (2026-11-19): `architecture.md` specifies the frontend folder structure (`pages/`, `layouts/`, `components/`, `hooks/`, `api/`, `context/`, `utils/`, `assets/`, `styles/`), the 14 canonical pages and 24 reusable accessible components (§8.3), state management boundaries, and the Module 14 investigation UX (`Uploading → Validating → Detecting Face → Running Analysis → Collecting Evidence → Evaluating Confidence → Generating Explanation → Preparing Report → Complete`, never a bare `"Fake (99.8%)"` verdict). `api_client_spec.md` specifies the centralized API client (`src/api/`, reading `VITE_API_BASE_URL` from environment variables) covering all 10 canonical `MOD013` endpoints and `MOD016` error normalization. Implementation begins at STEP-064.

STEP-064 (2026-11-19): Scaffolds the React + Vite + Tailwind CSS app shell (`package.json`, `vite.config.js`, `tailwind.config.js`, `.env.example`, `src/App.jsx`), the centralized API client (`src/api/`), global and case-scoped state (`src/context/SystemContext.jsx`, `ThemeContext.jsx`, `src/hooks/useInvestigation.js`), layouts (`src/layouts/AppShellLayout.jsx`, `InvestigationLayout.jsx`), and all 24 reusable accessible components + `ErrorBoundary` (`src/components/`). Commands: `npm test` and `npm run build` from this folder.

## Workflow
Antigravity writes, users consume. No AI inference logic.

## Owner
Antigravity

## Related Folders
11_AI_Forensic_System

## Expected Outputs
Frontend application code

> *This folder follows the canonical repository hygiene and naming rules defined in `MASTER_RESEARCH_OPERATING_SYSTEM.md`. Please refer to the handbook for full policy details.*
