# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0] - 2026-11-22 (Thesis Submission Release — STEP-001 through STEP-074)
### Added
- **Literature Operating System (Checklist 2 PASS):** Systematic review of 28 diffusion- and GAN-era papers (`P0001`–`P0028`), 8 verified claims (`CLAIM0001`–`CLAIM0008`), 8 derived research gaps (`GAP0001`–`GAP0008`), comparison table `TAB0001`, and synced BibTeX library (`15_Writing/references/references.bib`).
- **Datasets & Preprocessing (Checklists 3–4 PASS):** Strictly public-only, open-license 5-dataset benchmark (`DS0001`–`DS0005`), 6 versioned preprocessing pipelines (`PP0001`–`PP0006`, 34 unit tests), and 10 leakage-verified grouped and leave-one-generator-out splits (`SPLIT0001`–`SPLIT0002`).
- **Reproducible Model Development & 18-Phase Evaluation (Checklists 5, 6, 8 PASS):** Config-driven FastAI training pipeline (`17_Automation/training/`, 47 config validator tests), SHA-256 atomic checkpoints, 6 controlled Kaggle GPU experiments (`EXP0001`–`EXP0006`), full calibration/operating-point/failure/53-perturbation robustness/4-corpus cross-dataset/controlled `stable_diffusion` holdout/ablation/paired bootstrap + exact McNemar evaluation (`EVAL0001`–`EVAL0006`; `TAB0002`–`TAB0003`, `superiority_claim=none`).
- **AI Forensic Analyst Core (Checklist 9 PASS):** Complete 18-module architecture (`11_AI_Forensic_System/`, `MOD001`–`MOD018`) with isolated deep learning specialist (`MOD004`), append-only `EV` registry (`MOD005`), non-destructive reliability validator (`MOD006`), swappable rule-based fusion (`MOD007`; `DEC0009`), E4 validation-calibrated 4D confidence (`MOD009`; `DEC0010`), image-blind 4-way Decision Engine (`MOD008`), Policy A.9 data-only explainability (`MOD010`), programmatically `EV`-verified reasoning (`MOD011`), Template 24 reporting (`MOD012`), audit trail (`MOD015`), 8 canonical failure modes (`MOD016`), and Phase E14 verification (`EVAL0007`: 16/16 scenarios, 9/9 dimensions PASS).
- **Full-Stack Web Platform & Documentation (Checklists 10–12 PASS):** 7-app Django/DRF REST API (`13_Backend/`, `MOD013`, 10 canonical endpoints), 14-page / 24-component React + Vite + Tailwind web app (`12_Web/`, `MOD014`), consolidated cross-tier testing suite (85 unit/API/frontend tests, live HTTP integration, 6 live UAT scenarios), and full documentation suite (`16_Documentation/`).
- **Thesis Writing, Assembly & Submission Kit (Checklists 13 & 19 PASS):** 10 revised thesis chapters (`19,663` words, `40/40` `WR` units), deterministic thesis assembler (`17_Automation/assemble_thesis.py` → `15_Writing/thesis/assembled_thesis.md`, `24,552` words), 3 rendered tables (`TAB0001`–`TAB0003`), 30 figure specs (`FIG0001`–`FIG0030`) with 5 Draw.io XML sources and human Matplotlib renderer (`09_Figures/scripts/render_figures.py`), automated verifier (`17_Automation/verify_writing_consistency.py`, `0` hard issues), weighted Publication Readiness scorer (`17_Automation/compute_publication_readiness.py`, `94.69/100.00` PASS), submission checklist (`15_Writing/submission_checklist.md`), Policy A.8 submission/archival runbook (`15_Writing/THESIS_SUBMISSION_RUNBOOK.md`), and `v1.0` release notes (`15_Writing/RELEASE_NOTES_v1.0.md`).

## [1.0.0] - 2026-07-30 (Initial Repository Bootstrap — STEP-001)
### Added
- Ratified the MASTER_RESEARCH_OPERATING_SYSTEM.md
- Initialized the canonical 20-folder repository skeleton
- Added top-level folder READMEs per policy
- Added root governance files (README, LICENSE, CONTRIBUTING, CHANGELOG, CODEOWNERS, .gitignore, .gitattributes)
