# Submission Checklist — Thesis Submission `v1.0` (Checklist 17 / Template 25)

**Submission Target:** Thesis Submission (`v1.0`) — *AI Forensic Analyst: Evidence-Driven Cross-Generator Synthetic Face Forensics*  
**Date Prepared:** 2026-11-22  
**Owner:** Human (Repository Owner)  
**Runbook:** `15_Writing/THESIS_SUBMISSION_RUNBOOK.md` (Policy A.8)  
**Release Notes:** `15_Writing/RELEASE_NOTES_v1.0.md`  
**Prior Gates:** Checklists 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, and 19 (`94.69 / 100.00` PASS, human-confirmed `2026-11-22`).

---

## Requirements (Checklist 17 — Thesis Submission)

1. All chapters, abstract, front matter, and appendices complete and assembled (`15_Writing/thesis/assembled_thesis.md`).
2. All publication tables (`TAB0001`–`TAB0003`) rendered, verified, and embedded (Checklist 15).
3. All publication figures (`FIG0001`–`FIG0030`) finalized and exported by the human into `09_Figures/assets/` (Checklist 14 / Policy A.9).
4. All citations and bibliography entries (`P0001`–`P0028` in `15_Writing/references/references.bib`) verified with zero duplicates or unknown IDs.
5. Grammar, US-English spelling, terminology, and Markdown formatting reviewed (Phase W13 / Checklist 13).
6. Supervisor / human sign-off recorded (`15_Writing/writing_audit.md`, `15_Writing/reviewer_responses/review_response.md`).
7. Institutional similarity / plagiarism check completed and within university threshold.
8. Final university-formatted thesis PDF compiled from `assembled_thesis.md` (with exported figures embedded).
9. Final read-only thesis PDF archived into `20_Archive/thesis_v1.0/` (Phase W19 — immutable after placement).
10. Repository `CHANGELOG.md` updated, `v1.0` release notes prepared, and annotated Git tag `v1.0` + GitHub Release published by human (Phase 12).

---

## Completed

- [x] **All Chapters, Abstract & Appendices Assembled:** `15_Writing/thesis/assembled_thesis.md` (`24,552` words; 10 Checklist 13 approved sections + Front Matter + List of Tables + List of Figures + List of Abbreviations + Appendices A–D) generated deterministically by `17_Automation/assemble_thesis.py`.
- [x] **Tables Rendered & Embedded (Checklist 15):** `TAB0001`–`TAB0003` verified in `10_Tables/data/*.csv`, `10_Tables/rendered/*.md`, and embedded verbatim in Appendix C of `assembled_thesis.md`.
- [x] **Citations, Claims & References Verified:** `28/28` papers (`P0001`–`P0028`) matched 1:1 in `15_Writing/references/references.bib` (`0` duplicate keys, `0` duplicate DOIs), `8/8` claims marked `verified` in `02_Literature/claims/claim_database.csv`, `100%` canonical ID coverage across all 12 registered prefixes (`0` hard issues in `15_Writing/shared/consistency_and_verification_report.md`).
- [x] **Grammar, Spelling & Consistency Reviewed:** Phase W13 revision completed (`REV0001`–`REV0004` resolved, `0` em-dashes, `0` AI filler, `0` US/UK spelling mismatches, SemVer synced across all 10 files).
- [x] **Writing Readiness, Figure Quality & Publication Readiness Gates Passed:** Checklist 13 (`15_Writing/writing_audit.md`), Checklist 14 (`30/30` figures `FIG0001_v1`–`FIG0030_v1` PNG + vector PDF exported into `09_Figures/assets/` and embedded in `assembled_thesis.md`), and Checklist 19 (`15_Writing/publication_readiness_report.md`, **`95.97 / 100.00` PASS**) completed and human-confirmed `2026-11-22`.
- [x] **Release Changelog & Notes Prepared:** `CHANGELOG.md` updated with `v1.0` thesis release entry; `15_Writing/RELEASE_NOTES_v1.0.md` and `15_Writing/THESIS_SUBMISSION_RUNBOOK.md` finalized.

---

## Pending (Human & Institutional Actions Required Before Final Sign-Off)

- [ ] **Institutional Similarity / Plagiarism Check:** Run university similarity check (Turnitin / iThenticate) on the compiled thesis document and record the verified score below: `Similarity Score = ____% (Date: ____-__-__)`.
- [ ] **Final Formatted PDF Compilation:** Compile `thesis_v1.0.pdf` per institutional template (Pandoc/LaTeX/Word — instructions in `15_Writing/THESIS_SUBMISSION_RUNBOOK.md`) and verify page numbering, margins, figure legibility (600 DPI / vector), and bibliography rendering.
- [ ] **Read-Only Archival to `20_Archive/` (Phase W19):** Place final submitted `thesis_v1.0.pdf` (and optional similarity receipt) into `20_Archive/thesis_v1.0/` and treat the folder as strictly read-only thereafter.
- [ ] **Institutional Portal Upload & `v1.0` Release Tag (Phase 12):** Submit final PDF to the university portal, record submission confirmation ID, and run the human `v1.0` Git tag + GitHub Release command in `15_Writing/THESIS_SUBMISSION_RUNBOOK.md`.

---

## Evidence

- Assembled manuscript: `15_Writing/thesis/assembled_thesis.md` (`17_Automation/assemble_thesis.py`)
- Publication Readiness Report (Checklist 19 PASS): `15_Writing/publication_readiness_report.md` (`17_Automation/compute_publication_readiness.py`)
- Writing Readiness Audit (Checklist 13 PASS): `15_Writing/writing_audit.md`
- Automated Consistency Report (`0` hard issues): `15_Writing/shared/consistency_and_verification_report.md`
- Bibliography & Rendered Tables: `15_Writing/references/references.bib`, `10_Tables/rendered/TAB0001.md`–`TAB0003.md`
- Figure Runbook & Sources: `09_Figures/FIGURE_RENDERING_RUNBOOK.md`, `09_Figures/diagrams/FIG0026.drawio`–`FIG0030.drawio`, `09_Figures/scripts/render_figures.py`
- Submission Runbook & Release Notes: `15_Writing/THESIS_SUBMISSION_RUNBOOK.md`, `15_Writing/RELEASE_NOTES_v1.0.md`, `CHANGELOG.md`
- Archive Policy: `20_Archive/README.md`

---

## Approval

- **Pre-Submission Kit & Verification (AI / Auditor):** PASS (`2026-11-22`) — all repository-side writing, verification, assembly, changelog, and release preparation artifacts complete with 0 hard issues.
- **Final Checklist 17 Submission Sign-Off (Human / Supervisor):** `PENDING HUMAN EXECUTION` *(Check off the 5 pending human items above after PDF export, similarity check, archival, and `v1.0` tagging, then mark `PASS — Human-Confirmed YYYY-MM-DD`).*

---

## Status

**READY FOR HUMAN SUBMISSION EXECUTION (`PENDING FINAL PDF, SIMILARITY CHECK, 20_Archive PLACEMENT & v1.0 TAG`)**
