"""Deterministic Thesis Assembler (STEP-073 / Phase W18).

Assembles all 10 approved thesis manuscript files (15_Writing/thesis/*.md),
rendered publication tables (10_Tables/rendered/TAB0001.md-TAB0003.md),
figure catalog & captions parsed directly from 09_Figures/specs/FIG*_spec.md,
and bibliography provenance from 15_Writing/references/references.bib into
15_Writing/thesis/assembled_thesis.md.

Strictly obeys Policy A.9: never renders or fabricates figure images. If human-
exported assets exist in 09_Figures/assets/FIGxxxx_v1.png, links them directly;
otherwise emits an explicit Policy A.9 figure placement block referencing the
exact figure specification and human runbook.

Usage (from repository root):
    python 17_Automation/assemble_thesis.py
"""

from __future__ import annotations

import csv
import re
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THESIS_DIR = ROOT / "15_Writing" / "thesis"
OUTPUT_PATH = THESIS_DIR / "assembled_thesis.md"

CHAPTER_ORDER = [
    ("abstract.md", "Abstract"),
    ("chapter1_introduction.md", "Chapter 1: Introduction"),
    ("chapter2_literature_review.md", "Chapter 2: Literature Review"),
    ("chapter3_methodology.md", "Chapter 3: Methodology"),
    ("chapter4_implementation.md", "Chapter 4: Implementation"),
    ("chapter5_evaluation.md", "Chapter 5: Evaluation"),
    ("chapter6_results.md", "Chapter 6: Results"),
    ("chapter7_discussion.md", "Chapter 7: Discussion"),
    ("chapter8_conclusion.md", "Chapter 8: Conclusion"),
    ("appendices_and_references.md", "Appendices and References"),
]

ABBREVIATIONS = [
    ("API", "Application Programming Interface"),
    ("BA", "Balanced Accuracy"),
    ("CI", "Confidence Interval"),
    ("CNN", "Convolutional Neural Network"),
    ("CORS", "Cross-Origin Resource Sharing"),
    ("CSV", "Comma-Separated Values"),
    ("DCT", "Discrete Cosine Transform"),
    ("DL", "Deep Learning"),
    ("DOI", "Digital Object Identifier"),
    ("DRF", "Django REST Framework"),
    ("ECE", "Expected Calibration Error"),
    ("EDA", "Exploratory Data Analysis"),
    ("EM", "Expectation-Maximization"),
    ("EV", "Canonical Forensic Evidence Identifier (`EVxxxxxx`)"),
    ("EXIF", "Exchangeable Image File Format"),
    ("FFT", "Fast Fourier Transform"),
    ("FNR", "False Negative Rate"),
    ("FPR", "False Positive Rate"),
    ("GAN", "Generative Adversarial Network"),
    ("Grad-CAM", "Gradient-weighted Class Activation Mapping"),
    ("JSON", "JavaScript Object Notation"),
    ("LOGO", "Leave-One-Generator-Out"),
    ("MCC", "Matthews Correlation Coefficient"),
    ("MCE", "Maximum Calibration Error"),
    ("PR-AUC", "Area Under the Precision-Recall Curve"),
    ("REST", "Representational State Transfer"),
    ("RNG", "Random Number Generator"),
    ("ROC-AUC", "Area Under the Receiver Operating Characteristic Curve"),
    ("SemVer", "Semantic Versioning (`MAJOR.MINOR.PATCH`)"),
    ("SHA-256", "Secure Hash Algorithm 256-bit"),
    ("UAT", "User Acceptance Testing"),
    ("UI", "User Interface"),
    ("ViT", "Vision Transformer"),
    ("XAI", "Explainable Artificial Intelligence"),
]


def get_git_head() -> str:
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True)
            .strip()
        )
    except Exception:
        return "unknown"


def strip_draft_banner(text: str) -> str:
    """Keep chapter heading and body; drop top blockquote metadata banner + divider."""
    lines = text.splitlines()
    out: list[str] = []
    idx = 0
    if lines and lines[0].startswith("# "):
        out.append(lines[0])
        idx = 1
    # Skip blank lines, blockquote metadata lines, and first horizontal rule
    while idx < len(lines) and (
        lines[idx].strip() == "" or lines[idx].startswith("> ") or lines[idx].strip() == "---"
    ):
        if lines[idx].strip() == "---":
            idx += 1
            break
        idx += 1
    out.append("")
    out.extend(lines[idx:])
    return "\n".join(out).strip()


def parse_figure_spec(spec_path: Path) -> dict[str, str]:
    txt = spec_path.read_text(encoding="utf-8")
    fid = spec_path.name.split("_")[0]

    def extract(label: str) -> str:
        m = re.search(rf"\*\*{re.escape(label)}:\*\*\s*(.+)", txt)
        return m.group(1).strip() if m else ""

    assets_dir = ROOT / "09_Figures" / "assets"
    png_exists = (assets_dir / f"{fid}_v1.png").exists()
    pdf_exists = (assets_dir / f"{fid}_v1.pdf").exists()
    status = "Exported (PNG + PDF)" if (png_exists and pdf_exists) else (
        "Exported (partial)" if (png_exists or pdf_exists) else "Awaiting Human Policy A.9 Export"
    )
    return {
        "id": fid,
        "purpose": extract("Purpose"),
        "caption": extract("Caption"),
        "data_source": extract("Data source path"),
        "script": extract("Responsible notebook"),
        "output": extract("Expected output filename"),
        "status": status,
        "png_exists": "yes" if png_exists else "no",
    }


def load_table_specs() -> list[dict[str, str]]:
    tables = []
    for tid in ["TAB0001", "TAB0002", "TAB0003"]:
        md_path = ROOT / "10_Tables" / "rendered" / f"{tid}.md"
        csv_path = ROOT / "10_Tables" / "data" / f"{tid}.csv"
        md_text = md_path.read_text(encoding="utf-8").strip()
        first_h = next((ln.lstrip("# ").strip() for ln in md_text.splitlines() if ln.startswith("#")), tid)
        tables.append(
            {
                "id": tid,
                "title": first_h,
                "csv_rel": f"10_Tables/data/{tid}.csv",
                "md_rel": f"10_Tables/rendered/{tid}.md",
                "content": md_text,
            }
        )
    return tables


def main() -> int:
    git_rev = get_git_head()
    today = date.today().isoformat()

    # Load figure specs FIG0001-FIG0030
    fig_specs = [
        parse_figure_spec(p)
        for p in sorted((ROOT / "09_Figures" / "specs").glob("FIG*_spec.md"))
    ]
    exported_count = sum(1 for f in fig_specs if f["png_exists"] == "yes")

    # Load rendered tables TAB0001-TAB0003
    tables = load_table_specs()

    # Load BibTeX entry count
    bib_text = (ROOT / "15_Writing" / "references" / "references.bib").read_text(encoding="utf-8")
    bib_count = len(re.findall(r"@\w+\{[^,]+,", bib_text))

    # Load writing progress versions
    sec_versions: list[tuple[str, str, str]] = []
    with open(ROOT / "15_Writing/shared/writing_progress.csv", encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            sec_versions.append((r["Section ID"], r["Section"], r["Version"]))

    parts: list[str] = []

    # 1. Title Page & Front Matter
    parts.append(
        "\n".join(
            [
                "# AI Forensic Analyst: Evidence-Driven Cross-Generator Synthetic Face Forensics",
                "",
                "## Assembled Complete Thesis Manuscript (`v1.0.0-rc1`)",
                "",
                "| Metadata Field | Value |",
                "|---|---|",
                "| **Manuscript Version** | `1.0.0-rc1` (Assembled from Checklist 13 Approved Chapters) |",
                f"| **Assembly Date** | `{today}` |",
                f"| **Source Git Revision** | `{git_rev}` |",
                "| **Research Direction** | Direction 1 (`DEC0003`): System-Level AI Forensic Analyst + Generalization Focus (`DEC0002`) |",
                "| **Quality Gates Passed** | Checklists 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13 (Human-Confirmed) |",
                "| **Bibliography Source** | `15_Writing/references/references.bib` (`" + str(bib_count) + "` verified entries, `P0001`–`P0028`) |",
                "| **Rendered Tables Included** | `TAB0001`–`TAB0003` (`10_Tables/rendered/`, Checklist 15 PASS) |",
                f"| **Figure Catalog Status (Policy A.9)** | `{len(fig_specs)}` specified (`FIG0001`–`FIG0030`), `{exported_count}` exported in `09_Figures/assets/` |",
                "| **Assembler Script** | `17_Automation/assemble_thesis.py` (deterministic rebuild) |",
                "| **License** | MIT (`DEC0001`; strictly public-only datasets `DS0001`–`DS0005`, `DEC0004`) |",
                "",
                "---",
                "",
                "## Declaration of Originality and Reproducibility Statement",
                "",
                "This thesis manuscript is compiled deterministically from the ten Checklist 13 approved section files in `15_Writing/thesis/`, grounded exclusively in verified repository registries (`papers.csv`, `claim_database.csv`, `research_gap.csv`, `datasets.csv`, `preprocessing_registry.csv`, `split_registry.csv`, `model_registry.csv`, `experiment_registry.csv`, `evaluation_registry.csv`, `module_registry.csv`, `decision_log/DEC0001`–`DEC0010`, `knowledge_index.csv`, and `writing_database.csv`) (`WR0001`–`WR0040`). All statistical comparisons enforce `superiority_claim=none` where single-seed constraints apply (`TAB0003`), baseline detector `MODEL0001` is honestly disclosed as `Deployment Ready=no`, and all 30 publication figures (`FIG0001`–`FIG0030`) adhere strictly to Policy A.9 (`09_Figures/FIGURE_RENDERING_RUNBOOK.md`).",
                "",
                "---",
                "",
                "## Table of Contents",
                "",
                "1. Front Matter: Declaration, List of Figures (`FIG0001`–`FIG0030`), List of Tables (`TAB0001`–`TAB0003`), List of Abbreviations",
                "2. Abstract (`WR0001`)",
                "3. Chapter 1: Introduction (`WR0002`–`WR0006`)",
                "4. Chapter 2: Literature Review (`WR0007`–`WR0012`)",
                "5. Chapter 3: Methodology (`WR0013`–`WR0018`)",
                "6. Chapter 4: Implementation (`WR0019`–`WR0024`)",
                "7. Chapter 5: Evaluation (`WR0025`–`WR0028`)",
                "8. Chapter 6: Results (`WR0029`–`WR0034`)",
                "9. Chapter 7: Discussion (`WR0035`–`WR0036`)",
                "10. Chapter 8: Conclusion (`WR0037`–`WR0038`)",
                "11. Appendices and Verified References (`WR0039`–`WR0040`)",
                "12. Appendix C: Compiled Publication Tables (`TAB0001`–`TAB0003`)",
                "13. Appendix D: Master Publication Figure Catalog & Policy A.9 Placement Index (`FIG0001`–`FIG0030`)",
                "",
                "### Assembled Source Chapter Versions",
                "",
                "| Section ID | Section | Approved SemVer |",
                "|---|---|---|",
                *[f"| `{sid}` | {name} | `{ver}` |" for sid, name, ver in sec_versions],
                "",
                "---",
                "",
                "## List of Tables (`TAB0001`–`TAB0003`)",
                "",
                "| Table ID | Title | CSV Source | Rendered Markdown |",
                "|---|---|---|---|",
                *[
                    f"| `{t['id']}` | {t['title']} | `{t['csv_rel']}` | `{t['md_rel']}` |"
                    for t in tables
                ],
                "",
                "---",
                "",
                "## List of Figures (`FIG0001`–`FIG0030`)",
                "",
                "| Figure ID | Caption Summary | Source Spec / Script | Policy A.9 Asset Status |",
                "|---|---|---|---|",
                *[
                    f"| `{f['id']}` | {f['caption'][:140]}{'...' if len(f['caption']) > 140 else ''} | `09_Figures/specs/{f['id']}_spec.md` | {f['status']} |"
                    for f in fig_specs
                ],
                "",
                "---",
                "",
                "## List of Abbreviations",
                "",
                "| Abbreviation | Expansion |",
                "|---|---|",
                *[f"| `{abbr}` | {exp} |" for abbr, exp in ABBREVIATIONS],
                "",
                "---",
                "",
            ]
        )
    )

    # 2. Assemble Abstract, Chapters 1-8, Appendices & References verbatim
    for fname, _label in CHAPTER_ORDER:
        chapter_text = (THESIS_DIR / fname).read_text(encoding="utf-8")
        parts.append(strip_draft_banner(chapter_text))
        parts.append("\n---\n")

    # 3. Appendix C — Compiled Rendered Publication Tables (TAB0001-TAB0003)
    table_section = [
        "# Appendix C: Compiled Publication Tables (`TAB0001`–`TAB0003`)",
        "",
        "All three publication tables (`TAB0001`–`TAB0003`) are embedded verbatim from `10_Tables/rendered/` and correspond 1:1 to their machine-readable CSV datasets in `10_Tables/data/` (Checklist 15 PASS) (`WR0007`; `WR0027`; `WR0033`).",
        "",
    ]
    for t in tables:
        # Demote heading levels inside compiled appendix by 1
        demoted = "\n".join(
            ("#" + ln if ln.startswith("#") else ln) for ln in t["content"].splitlines()
        )
        table_section.append(demoted)
        table_section.append("")
        table_section.append("---")
        table_section.append("")
    parts.append("\n".join(table_section))

    # 4. Appendix D — Master Figure Catalog & Policy A.9 Placement Blocks (FIG0001-FIG0030)
    fig_section = [
        "# Appendix D: Master Publication Figure Catalog & Policy A.9 Placement Index (`FIG0001`–`FIG0030`)",
        "",
        "Every figure referenced in this thesis is cataloged below with its canonical `FIG` ID, full publication caption, data/diagram provenance, and Policy A.9 human-export status (`09_Figures/FIGURE_RENDERING_RUNBOOK.md`) (`WR0013`–`WR0036`).",
        "",
    ]
    for f in fig_specs:
        fid = f["id"]
        fig_section.append(f"## {fid}")
        fig_section.append("")
        if f["png_exists"] == "yes":
            fig_section.append(f"![{fid}](../../09_Figures/assets/{fid}_v1.png)")
            fig_section.append("")
        else:
            fig_section.append(
                f"> **Policy A.9 Figure Placement (`{fid}`):** Human-exported asset expected at `09_Figures/assets/{fid}_v1.png` (and vector `.pdf`). Generate via `09_Figures/FIGURE_RENDERING_RUNBOOK.md` and re-run `python 17_Automation/assemble_thesis.py` to auto-embed."
            )
            fig_section.append("")
        fig_section.append(f"- **Caption:** {f['caption']}")
        fig_section.append(f"- **Specification:** `09_Figures/specs/{fid}_spec.md`")
        fig_section.append(f"- **Data / Diagram Source:** {f['data_source']}")
        fig_section.append(f"- **Responsible Script / Source:** {f['script']}")
        fig_section.append("")
    parts.append("\n".join(fig_section))

    assembled = "\n".join(parts).strip() + "\n"
    OUTPUT_PATH.write_text(assembled, encoding="utf-8")
    words = len(assembled.split())
    print(
        f"Assembled {OUTPUT_PATH.relative_to(ROOT)} | {words:,} words | "
        f"10 sections | {len(tables)} embedded tables | {len(fig_specs)} cataloged figures ({exported_count} exported)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
