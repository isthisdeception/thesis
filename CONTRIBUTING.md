# Contributing Guidelines

This repository follows a rigorous, multi-agent AI framework directed by a human researcher. Contributions must adhere strictly to the rules laid out in the `MASTER_RESEARCH_OPERATING_SYSTEM.md`.

## Workflow
Development strictly follows:
`Planning (Cursor) → Approved Plan → Implementation (Antigravity) → Testing → Documentation → Commit → Push`

## The Human-in-the-Loop Rule
The AI **never** makes irreversible scientific decisions. Any action affecting dataset integrity, model selection, final metric choice, evaluation thresholds, interpretation of results, or architectural design must be presented to the human for approval. The human assumes full responsibility for the scientific output.

## Branch Strategy
- `main`: Protected, releasable branch.
- `develop`: Integration branch.
- `feature/*`: For feature implementation.
- `experiment/*`: For new models or pipelines.

## Commit Policy
Use conventional-style prefixes:
- `feat:` (New feature)
- `fix:` (Bug fix)
- `docs:` (Documentation changes)
- `refactor:` (Code refactoring)
- `research:` (Literature review/Gap analysis)
- `experiment:` (Training models)
- `dataset:` (Data pipelines)
- `evaluation:` (Metrics/Reports)
- `writing:` (Thesis/Journal)
- `deployment:` (Docker/Config)
- `config:` (YAML/Settings)
- `chore:` (Maintenance)

**Never** commit secrets, virtual environments, caches, raw datasets, or large binary files directly to standard Git tracking.
