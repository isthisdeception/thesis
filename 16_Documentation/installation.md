# Installation & Local Environment Setup

**Version:** `0.1.0`  
**Date:** 2026-11-19  
**Environment Lock Reference:** [environment/versions.lock.md](../environment/versions.lock.md)

---

## 1. Prerequisites

| Tool | Recommended Version | Purpose |
|---|---|---|
| **Python** | `3.11`–`3.13` (Kaggle lock: `3.13.16`; local `.venv` validated with Python `3.11`+) | Runs `11_AI_Forensic_System`, `13_Backend`, and `17_Automation` |
| **Node.js & npm** | Node `>= 18` + npm | Builds, runs, and tests `12_Web` (React `18` / Vite `6`) |
| **Git** | `>= 2.30` | Version control & commit SHA resolution in `/version` and `MOD012` reports |
| **PyTorch + FastAI (Optional for real weight inference)** | `torch==2.11.0`, `torchvision==0.26.0`, `fastai==2.8.12`, `plum-dispatch==2.5.7` | Loads `MODEL0001_export.pkl`. Without weights, `MOD004` emits `model_unavailable` and `MOD008` returns `Unknown`. |

> **Version Pinning Policy:** Do not upgrade ML packages in-place for experiments. Follow [environment/versions.lock.md](../environment/versions.lock.md) and [§10.2 Phase 16](../MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-16--environment-management).

---

## 2. Python Virtual Environment Setup (`.venv`)

From the repository root:

```powershell
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip

# Linux / macOS
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
```

### Install Pinned Backend & Core Dependencies

```bash
# Core pinned stack (PyTorch/FastAI/Pillow/PyYAML/Pytest)
.venv/Scripts/pip.exe install -r environment/requirements.txt

# Django & DRF web backend dependencies (Django 5.2.19, DRF 3.18.3, cors-headers 4.9.0)
.venv/Scripts/pip.exe install -r 13_Backend/requirements.txt
```

> **Note:** On CPU-only machines running `environment/requirements.txt`, install `torch==2.11.0` and `torchvision==0.26.0` first using `--index-url https://download.pytorch.org/whl/cpu` (or `--index-url https://download.pytorch.org/whl/cu130` for CUDA 13.0 GPUs) per [environment/versions.lock.md](../environment/versions.lock.md).

---

## 3. Frontend Setup (`12_Web`)

```bash
cd 12_Web
npm ci   # or: npm install
```

This installs React `18.3`, React Router `6.28`, Tailwind CSS `3.4`, Vite `6.0`, Vitest `2.1`, and Testing Library from `12_Web/package-lock.json`.

---

## 4. Environment Variables (`.env`)

Never commit `.env` files with secrets (see [Policy A.7](../MASTER_RESEARCH_OPERATING_SYSTEM.md#a7-canonical-ignore-policy)). Copy the checked-in templates:

### 4.1 Backend (`13_Backend/.env.example` → `13_Backend/.env`)
- `DJANGO_ENV=dev` (`dev` | `test` | `prod`)
- `DJANGO_SECRET_KEY=<unique-local-secret>`
- `DJANGO_DEBUG=true`
- `DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost`
- `CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173`
- `FORENSIC_MEDIA_ROOT=13_Backend/media/cases`
- `FORENSIC_LOG_DIR=13_Backend/media/logs`
- `FORENSIC_EVIDENCE_REGISTRY=11_AI_Forensic_System/evidence_registry.csv`
- `FORENSIC_CASE_REGISTRY=11_AI_Forensic_System/case_registry.csv`
- `FORENSIC_MODEL_ID=MODEL0001`
- `FORENSIC_ARTIFACT_ROOT=` *(optional folder holding `MODEL0001_export.pkl`)*
- `FORENSIC_ASYNC_MODE=thread` (`thread` for async UI polling; `eager` for synchronous unit tests)
- `FORENSIC_MAX_UPLOAD_BYTES=20971520` (`20 MB`)

### 4.2 Frontend (`12_Web/.env.example` → `12_Web/.env`)
- `VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1` *(or omit `.env` to use the built-in `/api/v1` Vite proxy to `VITE_PROXY_TARGET`)*
- `VITE_PROXY_TARGET=http://127.0.0.1:8000`
- `VITE_POLL_INTERVAL_MS=600`
- `VITE_REQUEST_TIMEOUT_MS=15000`

---

## 5. Starting & Verifying the Platform

### Option A — Two Terminals (Local Development)

Terminal 1 (Backend):
```bash
.venv/Scripts/python.exe 13_Backend/manage.py check
.venv/Scripts/python.exe 13_Backend/manage.py runserver 127.0.0.1:8000
```

Terminal 2 (Frontend):
```bash
cd 12_Web
npm run dev
```

Open `http://localhost:5173` in a browser (confirm health at `http://127.0.0.1:8000/api/v1/health`).

### Option B — Consolidated Cross-Tier Verification Suite

Run all automated suites (forensic core, Django check & API pytest, Vitest, Vite production build, live React-to-Django integration, and 6 UAT scenarios) in one command:

```bash
.venv/Scripts/python.exe 17_Automation/run_all_tests.py
```

See [test_plan.md](./test_plan.md) for suite details, isolated temporary media handling, and host-specific environment notes.
