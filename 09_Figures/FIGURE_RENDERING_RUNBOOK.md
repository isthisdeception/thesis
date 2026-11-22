# Human Figure-Rendering Runbook (STEP-071 / Policy A.8 & A.9)

> **Policy A.9 Notice:** Under `MASTER_RESEARCH_OPERATING_SYSTEM.md` §A.9, the AI never renders or commits publication figures. All 30 figure specifications (`FIG0001`–`FIG0030`), editable Draw.io architectural diagram sources (`FIG0026.drawio`–`FIG0030.drawio`), and the deterministic pure-`csv` Matplotlib renderer (`render_figures.py`) have been prepared for **human execution and visual approval**.

---

## 1. Why Human Action Is Required
- Ensures every published chart and architectural diagram is visually inspected for legibility, zero overlapping labels, print-width typography, and adherence to **Checklist 14 (Figure Quality)**.
- Preserves Policy A.9 governance across thesis submission (STEP-074) and high-impact journal submission (STEP-075).

---

## 2. Part A — Export Architecture & Methodology Diagrams (`FIG0026`–`FIG0030`, Draw.io)

### Exactly What to Do
1. Open **app.diagrams.net** (web) or the **Draw.io Integration** extension in VS Code.
2. Open each of the five pre-styled IEEE/ACM double-column `.drawio` files in `09_Figures/diagrams/`:
   - `09_Figures/diagrams/FIG0026.drawio` — End-to-End Research & Evaluation Methodology Pipeline (Ch. 3)
   - `09_Figures/diagrams/FIG0027.drawio` — 18-Module AI Forensic Analyst Architecture & Trust Boundaries (Ch. 3)
   - `09_Figures/diagrams/FIG0028.drawio` — Evidence Fusion, 4D E4 Confidence & 4-Way Decision Logic (**Journal Fig. 1**, Ch. 3)
   - `09_Figures/diagrams/FIG0029.drawio` — Three-Tier Full-Stack Web Architecture (`12_Web` / `13_Backend` / Core, Ch. 4)
   - `09_Figures/diagrams/FIG0030.drawio` — Reproducible FastAI Training, SHA-256 Checkpointing & Policy A.6 Sync (Ch. 4)
3. Inspect text alignment, arrow spacing, and readability at 100% print scale (`7.16 in` / `182 mm` double-column width). Adjust any label if desired.
4. For each diagram, export **both**:
   - **Vector PDF (for Overleaf/LaTeX):** `File -> Export as -> PDF...` (check **Crop**, Border `4`) → save as `09_Figures/assets/FIG00XX_v1.pdf`.
   - **600 DPI PNG (for Word/Markdown):** `File -> Export as -> PNG...` (Zoom `300%` or `600 DPI`, Border `4`, Background `#FFFFFF`) → save as `09_Figures/assets/FIG00XX_v1.png`.

---

## 3. Part B — Render Data Plots (`FIG0001`–`FIG0025`, Matplotlib)

### Exactly What to Do
1. From the repository root (in an environment with `matplotlib` and `numpy` — e.g., local `.venv` or Kaggle/Colab if Windows Application Control restricts local compiled `.pyd` binaries), run:
   ```bash
   python 09_Figures/scripts/render_figures.py
   ```
   *(To render a subset, e.g., key journal figures: `python 09_Figures/scripts/render_figures.py --only FIG0011 FIG0014 FIG0015 FIG0016 FIG0018 FIG0019 FIG0020 FIG0021`.)*
2. Visually inspect every generated `FIG0001_v1.png`–`FIG0025_v1.png` and `.pdf` in `09_Figures/assets/` against its matching spec in `09_Figures/specs/FIGxxxx_spec.md`.

---

## 4. Expected Output Location & Naming
- **Directory:** `09_Figures/assets/`
- **Expected Files:** `FIG0001_v1.png` through `FIG0030_v1.png` (plus matching vector `FIG0001_v1.pdf` through `FIG0030_v1.pdf` for journal LaTeX submission).

---

## 5. How to Confirm Success (Checklist 14 Verification)
Run the automated STEP-071 verification script from the repository root:
```bash
python 17_Automation/verify_writing_consistency.py
```
Confirm:
- All 30 figure specs (`FIG0001`–`FIG0030`) show `Asset Rendered: YES`.
- Visual inspection confirms crisp labels, units, legends, and zero overlapping text across all exported PNG/PDF assets.
