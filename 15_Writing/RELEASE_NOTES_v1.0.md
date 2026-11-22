# Release Notes — `v1.0` (Thesis Submission)

**Release Tag:** `v1.0`  
**Release Date:** 2026-11-22  
**Milestone:** Thesis Submission — *AI Forensic Analyst: Evidence-Driven Cross-Generator Synthetic Face Forensics*  
**Publication Readiness Score (Checklist 19):** `94.69 / 100.00` PASS (auto-advances to `95.97 / 100.00` upon human Policy A.9 figure export)

---

## Highlights

1. **Systematic Diffusion-Era Literature Synthesis (Checklist 2 PASS):** 28 registered papers (`P0001`–`P0028`), 8 verified claims (`CLAIM0001`–`CLAIM0008`), 8 evidence-backed research gaps (`GAP0001`–`GAP0008`), comparison table `TAB0001`, and clean BibTeX catalog (`15_Writing/references/references.bib`).
2. **Public-Only Multi-Dataset Benchmark & Leakage-Free Splits (Checklists 3–4 PASS):** 5 open-license datasets (`DS0001`–`DS0005`: ArtiFact face subset, DiFF official test, 140k Real and Fake Faces, Synthbuster, FairFace), 6 versioned preprocessing pipelines (`PP0001`–`PP0006`), and 10 leakage-verified grouped/LOGO splits (`SPLIT0001`–`SPLIT0002`).
3. **Controlled Baseline & 18-Phase Evaluation Suite (Checklists 5, 6, 8 PASS):** 6 controlled Kaggle GPU experiments (`EXP0001`–`EXP0006`; `MODEL0001`, `MODEL0008`–`MODEL0012`) across calibration (`ECE 0.0525`), operating points (`0.3951` frozen, `0.089` screening, `0.629` flag-for-review), subgroup failures (`43.7%` StyleGAN3 FNR), 53 image perturbations, 4 external datasets (`82.6%` FairFace FPR; `50.2%` DiFF FNR), controlled `stable_diffusion` holdout (`96.3%` seen → `13.7%` unseen on identical 299 test images), 4 one-factor ablations, and paired 10,000-resample bootstrap + exact McNemar tests (`TAB0002`–`TAB0003`, `superiority_claim=none`).
4. **18-Module AI Forensic Analyst Platform (Checklist 9 PASS):** Full implementation of `MOD001`–`MOD018` in `11_AI_Forensic_System/` featuring isolated `MOD004` specialist inference, append-only `EV` registry (`MOD005`), non-destructive reliability validation (`MOD006`), swappable rule-based fusion (`MOD007`; `DEC0009`), E4 validation-calibrated four-dimensional confidence (`MOD009`; `DEC0010`), image-blind four-way Decision Engine (`MOD008`: `Real`, `Fake`, `Inconclusive`, `Unknown`), Policy A.9 data-only explainability (`MOD010`), programmatically `EV`-verified reasoning (`MOD011`), Template 24 reporting (`MOD012`), audit logging (`MOD015`), 8 canonical failure modes (`MOD016`), and Phase E14 verification (`EVAL0007`: 9/9 dimensions, 16/16 scenarios, 135 verified sentences, 0 ungrounded leaks, mean latency `60.02 ms`).
5. **Full-Stack Web Application & Verification Suite (Checklists 10–12 PASS):** 7-app Django/DRF REST API (`13_Backend/`, `MOD013`, 10 canonical endpoints, zero duplicated forensic logic), 14-page / 24-component React + Vite + Tailwind frontend (`12_Web/`, `MOD014`), 85 automated unit/API/frontend tests, live cross-tier HTTP integration test, 6 live UAT scenarios (`UAT-01`–`UAT-06`), and full `16_Documentation/` suite.
6. **Complete Assembled Thesis & Verification Tooling (Checklists 13 & 19 PASS):** Deterministic thesis assembly (`15_Writing/thesis/assembled_thesis.md`, `24,552` words, `100%` canonical ID coverage across all 12 prefixes, `0` hard consistency issues), 3 rendered publication tables (`TAB0001`–`TAB0003`), 30 figure specifications (`FIG0001`–`FIG0030`) with 5 editable Draw.io XML architectural sources and human Matplotlib renderer (`09_Figures/scripts/render_figures.py`).

---

## Included Release Artifacts & Storage Tiers (Policy A.6)

- **GitHub Source Snapshot (`v1.0`):** Complete code (`11_AI_Forensic_System/`, `12_Web/`, `13_Backend/`, `17_Automation/`), registries, decision logs (`DEC0001`–`DEC0010`), evaluation CSVs/reports, documentation (`16_Documentation/`), writing sources (`15_Writing/`), rendered tables (`10_Tables/`), and figure specs/scripts/Draw.io sources (`09_Figures/`).
- **GitHub Release Attachments (Human-Uploaded on Tagging):** `20_Archive/thesis_v1.0/thesis_v1.0.pdf`, `20_Archive/thesis_v1.0/SHA256SUMS.txt`, and `15_Writing/references/references.bib`.
- **Kaggle Data & Artifact Tier (Not Stored in Git per Policy A.6):** Processed datasets (`DS0001`–`DS0005` via `PP0001`–`PP0006`), trained FastAI/PyTorch model exports (`MODEL0001`, `MODEL0008`–`MODEL0012`), and SHA-256 recovery checkpoints referenced via `05_Models/model_registry.csv`.

---

## Reproducibility Quick Check

```powershell
python 17_Automation/run_all_tests.py
python 17_Automation/verify_writing_consistency.py
python 17_Automation/compute_publication_readiness.py
```
