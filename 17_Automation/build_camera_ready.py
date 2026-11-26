"""Build Zero-Jargon Camera-Ready Thesis & Overleaf Q1 Journal Bundle.

1. Generates 15_Writing/thesis/camera_ready/thesis_clean.md by deterministically
   translating internal repository identifiers (P0001-P0028, DS0001-DS0005,
   EXP0001-EXP0006, MODEL0001-MODEL0012, MOD001-MOD018, etc.) into clean academic
   prose and standard numbered [1]-[28] references, stripping internal audit tags
   (WR/KI/DEC/CLAIM/GAP/EVAL/PP/SPLIT/Checklist/Policy A.x) cleanly.
2. Packages 15_Writing/journal/camera_ready/overleaf_bundle.zip containing
   manuscript_elsevier.tex, references.bib, and all 8 vector PDF figures.
3. Audits all camera-ready files for ZERO internal jargon, ZERO em-dashes,
   ZERO broken figure paths, and 28/28 matched BibTeX citation keys.

Usage (from repository root):
    python 17_Automation/build_camera_ready.py
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THESIS_IN = ROOT / "15_Writing" / "thesis" / "assembled_thesis.md"
THESIS_OUT = ROOT / "15_Writing" / "thesis" / "camera_ready" / "thesis_clean.md"
JOURNAL_DIR = ROOT / "15_Writing" / "journal" / "camera_ready"
BIB_PATH = ROOT / "15_Writing" / "references" / "references.bib"
ASSETS_DIR = ROOT / "09_Figures" / "assets"

JOURNAL_FIGS = [
    "FIG0011_v1.pdf",
    "FIG0015_v1.pdf",
    "FIG0016_v1.pdf",
    "FIG0018_v1.pdf",
    "FIG0019_v1.pdf",
    "FIG0020_v1.pdf",
    "FIG0031_v1.pdf",
    "FIG0033_v1.pdf",
    "FIG0034_v1.pdf",
]

FORBIDDEN_JARGON_RE = re.compile(
    r"\b(?:WR\d{4}|KI\d{4}|DEC\d{4}|CLAIM\d{4}|GAP\d{4}|EXP\d{4}|EVAL\d{4}|"
    r"DS\d{4}|PP\d{4}|SPLIT\d{4}|MODEL\d{4}|MOD\d{3}|SEC\d{4}|DEF-\d{3}|"
    r"STEP-\d{3}|Checklist\s+\d+|Policy\s+A\.\d|Template\s+\d+)\b"
)


def clean_thesis_text(text: str) -> str:
    """Deterministically translate internal tags in assembled_thesis.md to clean prose."""
    # Rewrite relative image links for nested camera_ready/ folder
    text = text.replace("(../../09_Figures/assets/", "(../../../09_Figures/assets/")

    # Remove parenthetical blocks containing ONLY internal IDs / file paths / semicolons
    internal_token = (
        r"(?:`?(?:WR\d{4}|KI\d{4}|DEC\d{4}|CLAIM\d{4}|GAP\d{4}|EVAL\d{4}|"
        r"PP\d{4}|SPLIT\d{4}|SEC\d{4}|DEF-\d{3}|STEP-\d{3}|"
        r"Checklists?\s+\d+(?:[–\-]\d+)?|Policy\s+A\.\d|Template\s+\d+|"
        r"Phase\s+E\d+(?:[–\-]E?\d+)?|Phase\s+W\d+|"
        r"[0-9]{2}_[A-Za-z0-9_./-]+)`?(?:[–\-]`?(?:WR\d{4}|KI\d{4}|DEC\d{4}|"
        r"CLAIM\d{4}|GAP\d{4}|EVAL\d{4}|PP\d{4}|SPLIT\d{4}|SEC\d{4}|P\d{4}|"
        r"EXP\d{4}|MODEL\d{4}|MOD\d{3}|FIG\d{4}|TAB\d{4})`?)?)"
    )

    # First replace Pxxxx citations with standard [N] numbers
    def p_repl(m: re.Match[str]) -> str:
        num = int(m.group(1))
        return f"[{num}]"

    text = re.sub(r"`P(\d{4})`", p_repl, text)
    text = re.sub(r"\bP(\d{4})\b", p_repl, text)

    # Replace dataset, experiment, model, module, figure, table IDs with clean names
    replacements = [
        (r"`?DS0001`?", "ArtiFact"),
        (r"`?DS0002`?", "DiFF"),
        (r"`?DS0003`?", "140k Real and Fake Faces"),
        (r"`?DS0004`?", "Synthbuster"),
        (r"`?DS0005`?", "FairFace"),
        (r"`?EXP0001`?", "Baseline ResNet-50"),
        (r"`?EXP0002`?", "LOGO Holdout"),
        (r"`?EXP0003`?", "Seed-43 Replicate"),
        (r"`?EXP0004`?", "No-Augmentation Ablation"),
        (r"`?EXP0005`?", "No-Pretraining Ablation"),
        (r"`?EXP0006`?", "160px Resolution Ablation"),
        (r"`?EXP0007`?", "EfficientNet-B4 Comparator"),
        (r"`?EXP0008`?", "ViT-B/16 Comparator"),
        (r"`?MODEL0001`?", "Baseline ResNet-50"),
        (r"`?MODEL0002`?", "Xception"),
        (r"`?MODEL0003`?", "EfficientNet-B4"),
        (r"`?MODEL0004`?", "ViT-B/16"),
        (r"`?MODEL0005`?", "ResNet-101"),
        (r"`?MODEL0006`?", "ConvNeXt"),
        (r"`?MODEL0007`?", "Swin Transformer"),
        (r"`?MODEL0008`?", "LOGO Holdout ResNet-50"),
        (r"`?MODEL0009`?", "Seed-43 ResNet-50"),
        (r"`?MODEL0010`?", "No-Augmentation ResNet-50"),
        (r"`?MODEL0011`?", "No-Pretraining ResNet-50"),
        (r"`?MODEL0012`?", "160px ResNet-50"),
        (r"`?SPLIT0001`?", "grouped random split"),
        (r"`?SPLIT0002`?", "leave-one-generator-out split"),
        (r"`?PP0001`?[–\-]`?PP0006`?", "deterministic preprocessing pipeline"),
        (r"`?PP000[1-6]`?", "preprocessing pipeline"),
        (r"`?EVAL0007`?", "whole-platform verification"),
        (r"`?EVAL0008`?", "large-scale governance benchmark"),
        (r"`?EVAL0009`?", "EfficientNet-B4 evaluation"),
        (r"`?EVAL0010`?", "ViT-B/16 evaluation"),
        (r"`?EVAL000[1-8]`?[–\-]`?EVAL00(?:0[1-9]|10)`?", "evaluation suite"),
        (r"`?EVAL000[1-6]`?", "evaluation suite"),
        (r"(?<![A-Za-z0-9_/])`?FIG00(\d{2})`?(?!_)", lambda m: f"Figure {int(m.group(1))}"),
        (r"(?<![A-Za-z0-9_/])`?TAB000(\d)`?(?![_.])", lambda m: f"Table {int(m.group(1))}"),
        (r"`?MOD0(\d{2})`?", lambda m: f"M{int(m.group(1))}"),
        (r"`?SEC000(\d)`?", lambda m: f"Section {int(m.group(1))}"),
    ]
    for pat, rep in replacements:
        text = re.sub(pat, rep, text)

    # Strip remaining internal governance tags cleanly
    strip_patterns = [
        r"`?WR\d{4}`?(?:[–\-]`?WR\d{4}`?)?",
        r"`?KI\d{4}`?(?:[–\-]`?KI\d{4}`?)?",
        r"`?DEC\d{4}`?(?:[–\-]`?DEC\d{4}`?)?",
        r"`?CLAIM\d{4}`?(?:[–\-]`?CLAIM\d{4}`?)?",
        r"`?GAP\d{4}`?(?:[–\-]`?GAP\d{4}`?)?",
        r"`?DEF-\d{3}`?",
        r"`?STEP-\d{3}`?",
        r"Checklists?\s+\d+(?:[–\-, ]+\d+)*",
        r"Policy\s+A\.\d+",
        r"Template\s+\d+",
    ]
    for pat in strip_patterns:
        text = re.sub(pat, "", text)

    # Clean up punctuation artifacts left after stripping internal tags
    text = re.sub(r"\(\s*[;,\s–\-]+\)", "", text)
    text = re.sub(r"\(\s*\)", "", text)
    text = re.sub(r"\(\s*[;,]\s*", "(", text)
    text = re.sub(r"\s*[;,]\s*\)", ")", text)
    text = re.sub(r"(;\s*){2,}", "; ", text)
    text = re.sub(r"(,\s*){2,}", ", ", text)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r" \.", ".", text)
    text = re.sub(r" ,", ",", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    text = text.replace("\u2014", " - ")
    return text.strip() + "\n"


def build_overleaf_zip() -> Path:
    zip_path = JOURNAL_DIR / "overleaf_bundle.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(JOURNAL_DIR / "manuscript_elsevier.tex", arcname="manuscript_elsevier.tex")
        zf.write(BIB_PATH, arcname="references.bib")
        for fname in JOURNAL_FIGS:
            src = ASSETS_DIR / fname
            if not src.exists():
                raise FileNotFoundError(f"Missing vector PDF figure for Overleaf bundle: {src}")
            zf.write(src, arcname=f"figures/{fname}")
    return zip_path


def audit_camera_ready() -> list[str]:
    issues: list[str] = []
    targets = [
        JOURNAL_DIR / "manuscript_elsevier.tex",
        JOURNAL_DIR / "manuscript_clean.md",
        JOURNAL_DIR / "supplementary_clean.md",
        THESIS_OUT,
    ]
    for fp in targets:
        txt = fp.read_text(encoding="utf-8")
        hits = sorted(set(FORBIDDEN_JARGON_RE.findall(txt)))
        if hits:
            issues.append(f"Internal jargon found in {fp.relative_to(ROOT)}: {hits[:15]}")
        if "\u2014" in txt:
            issues.append(f"Em-dash found in {fp.relative_to(ROOT)}")
        if fp.suffix == ".md":
            for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", txt):
                img = (fp.parent / m.group(1)).resolve()
                if not img.exists():
                    issues.append(f"Broken image link '{m.group(1)}' in {fp.relative_to(ROOT)}")

    # Verify all \cite{...} keys in manuscript_elsevier.tex match references.bib 1:1
    bib_keys = set(re.findall(r"@\w+\{([^,]+),", BIB_PATH.read_text(encoding="utf-8")))
    tex_txt = (JOURNAL_DIR / "manuscript_elsevier.tex").read_text(encoding="utf-8")
    cited_keys: set[str] = set()
    for grp in re.findall(r"\\cite\{([^}]+)\}", tex_txt):
        for k in grp.split(","):
            cited_keys.add(k.strip())
    unknown_keys = sorted(cited_keys - bib_keys)
    missing_keys = sorted(bib_keys - cited_keys)
    if unknown_keys:
        issues.append(f"Unknown BibTeX keys in manuscript_elsevier.tex: {unknown_keys}")
    if missing_keys:
        issues.append(f"Uncited BibTeX keys in manuscript_elsevier.tex: {missing_keys}")
    return issues


def main() -> int:
    # 1. Build clean camera-ready thesis
    THESIS_OUT.parent.mkdir(parents=True, exist_ok=True)
    cleaned = clean_thesis_text(THESIS_IN.read_text(encoding="utf-8"))
    THESIS_OUT.write_text(cleaned, encoding="utf-8")
    print(f"Wrote {THESIS_OUT.relative_to(ROOT)} ({len(cleaned.split()):,} words)")

    # 2. Build Overleaf zip bundle
    zpath = build_overleaf_zip()
    print(f"Wrote {zpath.relative_to(ROOT)} ({zpath.stat().st_size:,} bytes, {len(JOURNAL_FIGS)} vector PDFs + .tex + .bib)")

    # 3. Run strict zero-jargon & BibTeX audit
    issues = audit_camera_ready()
    if issues:
        for i in issues:
            print("ISSUE:", i)
        return 1
    bib_count = len(re.findall(r"@\w+\{([^,]+),", BIB_PATH.read_text(encoding="utf-8")))
    print(f"Camera-ready audit: PASS (0 internal jargon hits, 0 em-dashes, 0 broken images, {bib_count}/{bib_count} BibTeX keys matched)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
