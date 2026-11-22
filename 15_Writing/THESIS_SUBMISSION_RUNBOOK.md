# Human Thesis Submission, Archival & `v1.0` Release Runbook (STEP-074 / Policy A.8)

**Purpose:** Exact step-by-step instructions for the repository owner (`Human`) to finalize Policy A.9 figure exports, compile the institutional PDF, complete similarity checking, archive the read-only final thesis into `20_Archive/`, and publish the `v1.0` GitHub Release (Checklist 17 / Phase 12 / Phase W19).

---

## Step 1 — Complete Policy A.9 Human Figure Export (Checklist 14)

1. Follow `09_Figures/FIGURE_RENDERING_RUNBOOK.md`:
   - Export all 5 Draw.io architectural diagrams (`09_Figures/diagrams/FIG0026.drawio`–`FIG0030.drawio`) as cropped vector PDF (`FIGxxxx_v1.pdf`) and 600 DPI PNG (`FIGxxxx_v1.png`) into `09_Figures/assets/`.
   - Generate all 25 data plots (`FIG0001`–`FIG0025`) locally:
     ```powershell
     python 09_Figures/scripts/render_figures.py
     ```
2. Rebuild the assembled thesis so all 30 figures auto-embed, then re-verify consistency and readiness score:
   ```powershell
   python 17_Automation/assemble_thesis.py
   python 17_Automation/verify_writing_consistency.py
   python 17_Automation/compute_publication_readiness.py
   ```
   - Expected result: `30/30` figures exported, `0` hard issues, Publication Readiness Score **`95.97 / 100.00`**.

---

## Step 2 — Compile the Final Formatted Thesis PDF

Choose the export path required by your university template:

### Option A: Pandoc → LaTeX / XeLaTeX PDF (Recommended for IEEE / Academic Formatting)
```powershell
pandoc 15_Writing/thesis/assembled_thesis.md `
  --from=markdown+tex_math_dollars `
  --pdf-engine=xelatex `
  --bibliography=15_Writing/references/references.bib `
  --citeproc `
  --toc --number-sections `
  -V geometry:margin=1in `
  -V fontsize=11pt `
  -o thesis_v1.0.pdf
```

### Option B: Pandoc → Word `.docx` (For University Word Templates) → Export PDF
```powershell
pandoc 15_Writing/thesis/assembled_thesis.md `
  --bibliography=15_Writing/references/references.bib `
  --citeproc `
  --toc `
  -o thesis_v1.0.docx
```
Apply your university's official `.docx` cover page / header / footer styles in Microsoft Word, verify every figure (`FIG0001`–`FIG0030`) and table (`TAB0001`–`TAB0003`), and export as `thesis_v1.0.pdf`.

---

## Step 3 — Institutional Similarity Check & Supervisor Final Approval

1. Upload `thesis_v1.0.pdf` (or `.docx`) to your institution's similarity tool (Turnitin / iThenticate).
2. Confirm similarity is within university limits (excluding bibliography and properly cited quotations).
3. Obtain final supervisor approval signature on the university submission form.
4. Record the similarity percentage and approval date inside `15_Writing/submission_checklist.md`.

---

## Step 4 — Read-Only Archival into `20_Archive/` (Phase W19)

Per Phase W19 (*Archiving Policy*), final submitted documents move to `20_Archive/` and are **never modified after placement** (any post-defense revision creates a new read-only folder such as `20_Archive/thesis_v1.1/`):

```powershell
New-Item -ItemType Directory -Force -Path 20_Archive/thesis_v1.0 | Out-Null
Copy-Item thesis_v1.0.pdf 20_Archive/thesis_v1.0/thesis_v1.0.pdf
Get-FileHash 20_Archive/thesis_v1.0/thesis_v1.0.pdf -Algorithm SHA256 | Out-File 20_Archive/thesis_v1.0/SHA256SUMS.txt
```

Update `15_Writing/submission_checklist.md` (check off all 5 pending items and mark `PASS — Human-Confirmed YYYY-MM-DD`) and commit the archival snapshot on `main` (via PR):
```powershell
git add 09_Figures/assets/ 15_Writing/thesis/assembled_thesis.md 15_Writing/publication_readiness_report.md 15_Writing/shared/consistency_and_verification_report.md 15_Writing/submission_checklist.md 20_Archive/thesis_v1.0/
git commit -m "release: archive final thesis PDF and pass Checklist 17"
git push origin main
```

---

## Step 5 — Tag & Publish the `v1.0` GitHub Release (Phase 12)

Once `main` contains the archived final PDF and completed `submission_checklist.md`, create the annotated `v1.0` tag and GitHub Release:

```powershell
git tag -a v1.0 -m "release: thesis submission v1.0"
git push origin v1.0
gh release create v1.0 `
  20_Archive/thesis_v1.0/thesis_v1.0.pdf `
  20_Archive/thesis_v1.0/SHA256SUMS.txt `
  15_Writing/references/references.bib `
  --title "v1.0 — Thesis Submission: AI Forensic Analyst" `
  --notes-file 15_Writing/RELEASE_NOTES_v1.0.md
```

*(Policy A.6 reminder: trained `.pth`/`.pkl` model weights and processed image datasets remain exclusively in the Kaggle Artifact/Data Tier and are never attached directly to Git commits.)*

---

## Step 6 — Submit & Confirm

1. Upload `20_Archive/thesis_v1.0/thesis_v1.0.pdf` to your university thesis submission portal.
2. Save the portal confirmation receipt ID in `15_Writing/submission_checklist.md` (or outside Git if it contains private student IDs).
3. Proceed to **STEP-075 — Journal Manuscript & Journal Submission Gate (Checklist 16)**.
