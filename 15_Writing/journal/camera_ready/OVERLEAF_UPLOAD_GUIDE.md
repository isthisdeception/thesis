# Camera-Ready Journal & Thesis Export Guide (Zero Internal Jargon)

All files in this folder (`15_Writing/journal/camera_ready/`) and `15_Writing/thesis/camera_ready/` are **100% clean, submission-ready academic prose** with **zero internal repository tags** (no `EXP0001`, `DS0001`, `DEC0001`, `KI0001`, `WR0001`, `CLAIM0001`, `GAP0001`, `EVAL0007`, `PP0001`, `SPLIT0001`, `Checklist`, or `Policy A.9`).

---

## Option 1: Instant Q1 Elsevier Journal PDF via Overleaf (Recommended — Zero Install!)

1. Go to **https://www.overleaf.com** and log in (free account works).
2. Click **New Project** → **Upload Project**.
3. Upload **`15_Writing/journal/camera_ready/overleaf_bundle.zip`** (already pre-bundled with `manuscript_elsevier.tex`, `references.bib`, and all 8 vector `.pdf` figures inside `figures/`!).
4. Edit lines 18–26 of `manuscript_elsevier.tex` to insert your real **Author Name**, **Email**, **Department/University**, **City**, and **Country**.
5. Click **Recompile** → click **Download PDF**!
   - *(Tip: Line 2 is single-column Elsevier review format `preprint,12pt`. Uncomment line 3 `final,5p,times,twocolumn` to preview the published two-column journal layout!)*

---

## Option 2: Word `.docx` Export via Pandoc (Journal + Supplementary + Full Clean Thesis)

Install Pandoc once:
```powershell
winget install --id JohnMacFarlane.Pandoc -e
```
Restart terminal, then run:
```powershell
# 1. Clean Journal Manuscript (.docx)
pandoc 15_Writing/journal/camera_ready/manuscript_clean.md --resource-path=15_Writing/journal/camera_ready -o journal_manuscript_clean.docx

# 2. Clean Journal Supplementary (.docx)
pandoc 15_Writing/journal/camera_ready/supplementary_clean.md --resource-path=15_Writing/journal/camera_ready -o journal_supplementary_clean.docx

# 3. Clean Full Thesis (.docx)
pandoc 15_Writing/thesis/camera_ready/thesis_clean.md --resource-path=15_Writing/thesis/camera_ready --toc -o thesis_clean.docx
```
Open in Microsoft Word → add your cover page → **File → Save As → PDF**.
