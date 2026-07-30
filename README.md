# AI Digital Forensics

## Purpose
An evidence-driven forensic system (AI Forensic Analyst) designed to evaluate, classify, and explain AI-generated vs. real media. This repository contains the full research pipeline from literature review and dataset generation, through model training, to the deployment of the forensic analysis web application.

## Project Description
The AI Forensic Analyst is not a simple classifier, but an evidence-driven system. It aggregates independent evidence from multiple specialists (deep learning, metadata, frequency artifacts, etc.) to arrive at a reasoned, explainable conclusion about the authenticity of digital media. This repository strictly adheres to the research workflows and architecture defined in the `MASTER_RESEARCH_OPERATING_SYSTEM.md`.

## Repository Structure Map

| Folder | Purpose |
|---|---|
| `01_Project_Management/` | Governance, decision logs, research diaries, and reviews. |
| `02_Literature/` | Papers, summaries, research gaps, and claims. |
| `03_Datasets/` | Dataset tracking, metadata, and raw/processed data pointers. |
| `04_Preprocessing/` | Versioned data preprocessing pipelines. |
| `05_Models/` | Model definitions and Model Registry. |
| `06_Experiments/` | Individual experiment environments (`EXPxxxx`). |
| `07_Checkpoints/` | Manifests and policies for recoverable training state. |
| `08_Evaluation/` | Evaluation metrics, statistics, and Evaluation Registry. |
| `09_Figures/` | Specifications and generation provenance for all figures. |
| `10_Tables/` | Specifications and rendered data for all tables. |
| `11_AI_Forensic_System/` | The AI Forensic Analyst core logic and evidence registry. |
| `12_Web/` | React frontend application. |
| `13_Backend/` | Django REST API backend. |
| `14_Deployment/` | Deployment configuration (Docker, Nginx, Gunicorn). |
| `15_Writing/` | Thesis and journal drafts, writing database. |
| `16_Documentation/` | System, API, and workflow documentation. |
| `17_Automation/` | Reproducible scripts and automation pipelines. |
| `18_Templates/` | Canonical templates for all structured files. |
| `19_Prompts/` | Versioned prompts for all AI agents. |
| `20_Archive/` | Immutable storage of completed/superseded artifacts. |
| `environment/` | Dependency locks and Kaggle setup scripts. |

## Quick Start & Installation
*(TBD - as the system is developed in Phase 8 & 12, explicit installation and startup commands will be placed here.)*

## Workflow Strategy
We operate a specialized multi-platform workflow:
- **Cursor** = Planning only.
- **Antigravity** = Implementation.
- **GitHub** = Version control / single source of truth.
- **Kaggle** = Heavy model training.
- **Human** = Scientific decisions.

## Dependencies
- **Core ML:** Python, PyTorch, FastAI
- **Web App:** Django, React, Vite, TailwindCSS
- **Storage:** Kaggle Datasets (data), GitHub LFS/Releases (artifacts)

## License
[MIT License](./LICENSE)

## Citation
*(Placeholder for final DOI/Citation)*

## Contact
Chief Research Architect (Assaduzzaman)
