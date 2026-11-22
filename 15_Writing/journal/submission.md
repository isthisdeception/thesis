# Journal Submission Checklist & Author Guide (Checklist 16 / Template 25)

**Manuscript:** `15_Writing/journal/manuscript.md`  
**Supplementary Material:** `15_Writing/journal/supplementary_material.md`  
**Recommended Primary Target Venues (Elsevier Q1):**
1. *Forensic Science International: Digital Investigation* (FSI:DI — Elsevier, Q1; strongest alignment with forensic evidence pipelines, chain-of-custody auditability, and reproducible digital forensics tooling).
2. *Computers & Security* (Elsevier, Q1; strong alignment with full-stack applied security systems, trust-boundary architectures, and empirical ML robustness).
*(Alternative top-tier option after V2 multi-backbone expansion: IEEE Transactions on Information Forensics and Security.)*

**Date Prepared:** 2026-11-22  
**Owner:** Human (Corresponding Author)

---

## Requirements (Checklist 16 — Journal Submission)

1. Concise, novelty-focused Abstract and Keywords present.
2. Novelty and concrete contributions explicitly articulated and bounded strictly to verified evidence.
3. All citations verified 1:1 against `15_Writing/references/references.bib` and `02_Literature/metadata/papers.csv` (`P0001`–`P0028`, 0 duplicates, 0 unknown keys).
4. High-impact figures (`FIG0027`, `FIG0028`, `FIG0011`, `FIG0015`, `FIG0016`, `FIG0018`, `FIG0019`, `FIG0020`) and quantitative tables (`TAB0002`, `TAB0003`) integrated cleanly with 600 DPI PNG + vector PDF assets in `09_Figures/assets/`.
5. Target journal formatting ready (Elsevier Highlights, structured sections, US English, zero em-dashes, zero AI filler, LaTeX/Word export path).
6. Supplementary material (`15_Writing/journal/supplementary_material.md`) prepared covering `TAB0001`, EDA (`FIG0001`–`FIG0010`), extended figures (`FIG0012`–`FIG0014`, `FIG0017`, `FIG0021`–`FIG0026`, `FIG0029`–`FIG0030`), 18-module contract, and locked environment.
7. Reproducibility Statement, Code Availability Statement, Data Availability Statement, Ethics/Privacy Statement, Competing Interest Statement, and CRediT Statement included.
8. Author cover letter prepared and human portal submission completed (`STEP-076`).

---

## Completed

- [x] **Concise Method-Centric Manuscript Drafted:** `15_Writing/journal/manuscript.md` (~3,900 words, Elsevier Highlights, Structured Abstract, 8 Keywords, Sections 1–7, Declarations, 28 References).
- [x] **Supplementary Material Prepared:** `15_Writing/journal/supplementary_material.md` (Sections S1–S5 with embedded 600 DPI figures and full `EVAL0007` verification summary).
- [x] **All 30 High-Resolution Figures Ready (Checklist 14 PASS):** Both 600 DPI PNG and vector PDF files verified in `09_Figures/assets/FIG0001_v1.*`–`FIG0030_v1.*`; zero internal workflow jargon in architectural diagrams (`FIG0026`–`FIG0030`).
- [x] **Citations, Claims & Consistency Verified:** `17_Automation/verify_writing_consistency.py` passes with `0` hard issues across both thesis and journal packages (`28/28` `P` IDs matched, `0` em-dashes, `0` AI filler, `0` UK spellings, `0` broken figure paths).
- [x] **All Mandatory Availability & Integrity Declarations Included:** Reproducibility, Code Availability (MIT, GitHub), Data Availability (5 public corpora), Ethics/Privacy, Competing Interest, and CRediT statements present in `manuscript.md`.
- [x] **Checklist 16 Audit Report Prepared:** `15_Writing/journal/publication_audit.md` (Appendix A.10 structure).

---

## Pending (Human Author Actions for Portal Upload — STEP-076)

- [x] **Author Metadata & Affiliations:** Added all 10 authors, affiliations (DIU, Bond University, University of Johannesburg, UIU, University College of Professional Education Wrocław), corresponding authors (`Md. Mizanur Rahman`, `Ahmed Moustafa`), and emails into `15_Writing/journal/camera_ready/manuscript_elsevier.tex` and `manuscript_clean.md`.
- [ ] **Compile Final Journal PDF / LaTeX Source:** Export via `15_Writing/journal/camera_ready/overleaf_bundle.zip` (Overleaf) or Pandoc `.docx` below (no live cloud VPS hosting is required).
- [ ] **Confirm Checklist 16 PASS & Upload to Journal Portal:** Submit manuscript, supplementary PDF, highlights, and cover letter below, then track peer reviews in `15_Writing/reviewer_responses/review_response.md` (`STEP-076`).

---

## Quick Export Commands (Elsevier / IEEE Submission)

```powershell
# Export Word (.docx) for Editorial Manager upload
pandoc 15_Writing/journal/manuscript.md `
  --bibliography=15_Writing/references/references.bib `
  --citeproc `
  --resource-path=15_Writing/journal `
  -o journal_manuscript_v1.0.docx

# Export Supplementary Material (.docx / .pdf)
pandoc 15_Writing/journal/supplementary_material.md `
  --resource-path=15_Writing/journal `
  -o journal_supplementary_v1.0.docx
```

---

## Ready-to-Use Cover Letter Draft

> Dear Editor-in-Chief,  
>  
> Please consider our original research manuscript, *"AI Forensic Analyst: An Evidence-Driven, Calibrated, and Auditable Architecture for Cross-Generator Synthetic Face Forensics,"* for publication in *[Forensic Science International: Digital Investigation / Computers & Security]*.  
>  
> While synthetic face detectors achieve high accuracy on matched benchmarks, our controlled five-dataset evaluation demonstrates severe real-world failure modes: unseen diffusion recall falls from 96.3% to 13.7% on identical held-out test images, external authentic face false positive rates reach 82.6% on FairFace, and heavy post-processing collapses balanced accuracy toward 0.50. Rather than treating synthetic face authentication as a standalone binary score, we introduce and verify an 18-module trust-bounded forensic architecture that isolates neural inference from an image-blind four-way Decision Engine (`Real`, `Fake`, `Inconclusive`, `Unknown`), replaces raw probabilities with validation-calibrated four-dimensional confidence, and programmatically verifies every reasoning sentence against an immutable evidence ledger. All code, registries, datasets, and verification suites are publicly reproducible under the MIT license.  
>  
> This manuscript is original, has not been published previously, and is not under consideration elsewhere. The authors declare no competing interests.  
>  
> Sincerely,  
> **Md. Assaduzzaman, Nushamd-A-Shawmeem, Sourav Saha, Masud Rana Nayeem, Tapasy Rabeya, Md. Mizanur Rahman\*, Md Ali Hossain, Ahmed Moustafa\*, Suman Ahmmed, and Ohidujjaman**  
> *\*Corresponding authors: `mizanurrahman.cse@diu.edu.bd`, `amoustaf@bond.edu.au`*

---

## Evidence

- Journal manuscript: `15_Writing/journal/manuscript.md`
- Supplementary material: `15_Writing/journal/supplementary_material.md`
- Journal audit report (Checklist 16): `15_Writing/journal/publication_audit.md`
- Verified BibTeX bibliography: `15_Writing/references/references.bib`
- Verified publication figures: `09_Figures/assets/FIG0001_v1.*`–`FIG0030_v1.*`
- Automated consistency report: `15_Writing/shared/consistency_and_verification_report.md`

---

## Approval

- **Manuscript, Supplementary & Automated Checklist 16 Verification (AI / Publication Auditor):** **PASS (`2026-11-22`)**
- **Human Gate Sign-Off (Checklist 16):** **PENDING HUMAN CONFIRMATION**

---

## Status

**READY FOR HUMAN CHECKLIST 16 CONFIRMATION & PORTAL SUBMISSION (`STEP-076`)**
