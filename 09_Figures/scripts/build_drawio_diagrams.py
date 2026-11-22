"""Build publication-grade Draw.io (.drawio) diagrams for FIG0026-FIG0030.

Outputs editable diagrams.net XML files under 09_Figures/diagrams/ using a
cohesive, colorblind-safe IEEE/Elsevier double-column palette with universal
scientific terminology (free of internal workflow/checklist tags) and explicit
orthogonal waypoints to prevent arrow overlaps. Per Policy A.9, these are
editable diagram sources; the human inspects and exports vector PDF and 600 DPI
PNG files into 09_Figures/assets/.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "09_Figures" / "diagrams"

# IEEE / Elsevier colorblind-safe palette
SLATE = ("#EBF3F9", "#1F618D", "#154360")
TEAL = ("#E8F6F3", "#117A65", "#0E6251")
AMBER = ("#FEF5E7", "#B9770E", "#7E5109")
CRIMSON = ("#FDEDEC", "#922B21", "#641E16")
NEUTRAL = ("#F4F6F9", "#566573", "#212F3C")
WHITE = ("#FFFFFF", "#2C3E50", "#1C2833")


class DrawioBuilder:
    def __init__(self, name: str, width: int = 1280, height: int = 620) -> None:
        self.name = name
        self.width = width
        self.height = height
        self._id = 2
        self.cells: list[ET.Element] = []

    def _next_id(self) -> str:
        val = str(self._id)
        self._id += 1
        return val

    def group_box(
        self,
        title: str,
        x: int,
        y: int,
        w: int,
        h: int,
        palette=NEUTRAL,
        dashed: bool = True,
        align: str = "left",
        valign: str = "top",
    ) -> str:
        fill, stroke, font = palette
        cid = self._next_id()
        vpad = "spacingBottom=6;" if valign == "bottom" else "spacingTop=6;"
        hpad = "spacingLeft=10;" if align == "left" else ("spacingRight=10;" if align == "right" else "")
        style = (
            f"rounded=1;arcSize=4;whiteSpace=wrap;html=1;align={align};verticalAlign={valign};"
            f"{vpad}{hpad}fontFamily=Helvetica;fontSize=12;fontStyle=1;"
            f"fillColor={fill};strokeColor={stroke};fontColor={font};strokeWidth=1.5;"
            f"{'dashed=1;dashPattern=6 4;' if dashed else ''}"
        )
        cell = ET.Element(
            "mxCell",
            id=cid,
            value=title,
            style=style,
            vertex="1",
            parent="1",
        )
        ET.SubElement(
            cell, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), **{"as": "geometry"}
        )
        self.cells.append(cell)
        return cid

    def box(
        self,
        label: str,
        x: int,
        y: int,
        w: int,
        h: int,
        palette=WHITE,
        bold: bool = False,
        font_size: int = 11,
    ) -> str:
        fill, stroke, font = palette
        cid = self._next_id()
        style = (
            f"rounded=1;arcSize=8;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
            f"spacing=6;fontFamily=Helvetica;fontSize={font_size};fontStyle={'1' if bold else '0'};"
            f"fillColor={fill};strokeColor={stroke};fontColor={font};strokeWidth=1.4;"
        )
        cell = ET.Element("mxCell", id=cid, value=label, style=style, vertex="1", parent="1")
        ET.SubElement(
            cell, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), **{"as": "geometry"}
        )
        self.cells.append(cell)
        return cid

    def pill(
        self,
        label: str,
        x: int,
        y: int,
        w: int,
        h: int,
        palette=SLATE,
        font_size: int = 10,
    ) -> str:
        fill, stroke, font = palette
        cid = self._next_id()
        style = (
            f"rounded=1;arcSize=50;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
            f"fontFamily=Helvetica;fontSize={font_size};fontStyle=1;"
            f"fillColor={fill};strokeColor={stroke};fontColor={font};strokeWidth=1.3;"
        )
        cell = ET.Element("mxCell", id=cid, value=label, style=style, vertex="1", parent="1")
        ET.SubElement(
            cell, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), **{"as": "geometry"}
        )
        self.cells.append(cell)
        return cid

    def edge(
        self,
        src: str,
        dst: str,
        label: str = "",
        color: str = "#34495E",
        dashed: bool = False,
        exit_x: float | None = None,
        exit_y: float | None = None,
        entry_x: float | None = None,
        entry_y: float | None = None,
        waypoints: list[tuple[int, int]] | None = None,
    ) -> str:
        cid = self._next_id()
        pts = ""
        if exit_x is not None and exit_y is not None:
            pts += f"exitX={exit_x};exitY={exit_y};exitDx=0;exitDy=0;"
        if entry_x is not None and entry_y is not None:
            pts += f"entryX={entry_x};entryY={entry_y};entryDx=0;entryDy=0;"
        lbl_bg = "labelBackgroundColor=#FFFFFF;labelBorderColor=none;" if label else ""
        style = (
            f"edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;"
            f"fontFamily=Helvetica;fontSize=10;fontColor={color};strokeColor={color};strokeWidth=1.4;"
            f"{lbl_bg}endArrow=block;endFill=1;{'dashed=1;dashPattern=5 3;' if dashed else ''}{pts}"
        )
        cell = ET.Element(
            "mxCell",
            id=cid,
            value=label,
            style=style,
            edge="1",
            parent="1",
            source=src,
            target=dst,
        )
        geom = ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
        if waypoints:
            arr = ET.SubElement(geom, "Array", **{"as": "points"})
            for wx, wy in waypoints:
                ET.SubElement(arr, "mxPoint", x=str(wx), y=str(wy))
        self.cells.append(cell)
        return cid

    def save(self, path: Path) -> None:
        mxfile = ET.Element("mxfile", host="app.diagrams.net", modified="2026-11-22", version="24.0.0")
        diagram = ET.SubElement(mxfile, "diagram", id=self.name, name=self.name)
        model = ET.SubElement(
            diagram,
            "mxGraphModel",
            dx="1200",
            dy="800",
            grid="1",
            gridSize="10",
            guides="1",
            tooltips="1",
            connect="1",
            arrows="1",
            fold="1",
            page="1",
            pageScale="1",
            pageWidth=str(self.width),
            pageHeight=str(self.height),
            background="#FFFFFF",
        )
        root = ET.SubElement(model, "root")
        ET.SubElement(root, "mxCell", id="0")
        ET.SubElement(root, "mxCell", id="1", parent="0")
        for c in self.cells:
            root.append(c)
        ET.indent(mxfile, space="  ")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(ET.tostring(mxfile, encoding="unicode", xml_declaration=True), encoding="utf-8")


def build_fig0026() -> None:
    """FIG0026: End-to-End Research & Evaluation Methodology Pipeline."""
    d = DrawioBuilder("FIG0026_Methodology_Pipeline", 1360, 560)
    d.group_box("1. Public Multi-Dataset Benchmark", 20, 40, 230, 395, SLATE)
    ds1 = d.box("<b>ArtiFact Faces</b> (In-Dist.)<br/>50,000 (25k/25k, 13 gens)", 35, 80, 200, 55, WHITE)
    ds2 = d.box("<b>DiFF Official Test</b><br/>51,452 proc. (13 diffusion gens)", 35, 150, 200, 55, WHITE)
    ds3 = d.box("<b>140k Real &amp; Fake Faces</b><br/>70k FFHQ / 70k StyleGAN", 35, 220, 200, 55, WHITE)
    ds4 = d.box("<b>Synthbuster</b><br/>9k diffusion + 999 RAISE real", 35, 290, 200, 55, WHITE)
    ds5 = d.box("<b>FairFace</b> (Real Faces)<br/>97,698 images (7 demographics)", 35, 360, 200, 55, WHITE)

    d.group_box("2. Preprocessing & Splits", 285, 40, 240, 395, SLATE)
    pp = d.box(
        "<b>7-Stage Deterministic Pipeline</b><br/>Fixed Seed (42) | Verify Integrity<br/>Extract Meta -&gt; Strip EXIF<br/>Filter &gt;=64px -&gt; RGB PNG<br/>Resize 224x224 (no denoising)",
        300, 90, 210, 120, WHITE
    )
    sp1 = d.box("<b>Grouped Random Split</b><br/>ArtiFact: 34,993 / 7,502 / 7,505<br/>Zero Overlap Verified", 300, 240, 210, 75, WHITE)
    sp2 = d.box("<b>Leave-One-Generator-Out</b><br/>Stable Diffusion held out (1,923)<br/>Zero Overlap Verified", 300, 335, 210, 75, WHITE)

    d.group_box("3. Controlled Model Training", 560, 40, 240, 395, TEAL)
    exp1 = d.box("<b>ResNet-50 Baseline</b><br/>ImageNet-1k Pretrained (T4 GPU)<br/>Val-Frozen Threshold: 0.3951", 575, 95, 210, 75, WHITE)
    exp2 = d.box("<b>Unseen-Generator Holdout</b><br/>ResNet-50 LOGO Training<br/>(Stable Diffusion Excluded)", 575, 195, 210, 75, WHITE)
    expa = d.box("<b>One-Factor Ablation Suite</b><br/>4 Controlled Variants:<br/>Seed | No-Aug | No-Pre | 160px", 575, 295, 210, 85, WHITE)

    d.group_box("4. Multi-Axis Evaluation", 835, 40, 230, 395, AMBER)
    ev1 = d.box("<b>Calibration &amp; Error Profile</b><br/>ROC-AUC, PR-AUC, ECE (0.0525)<br/>Per-Generator FNR / FPR", 850, 85, 200, 70, WHITE)
    ev2 = d.box("<b>Perturbation Robustness</b><br/>53 Conditions: JPEG, Blur,<br/>Noise, Resize, Social Upload", 850, 170, 200, 68, WHITE)
    ev3 = d.box("<b>Cross-Dataset &amp; LOGO</b><br/>4 External Corpora + Paired<br/>Unseen Diffusion Recall", 850, 253, 200, 68, WHITE)
    ev4 = d.box("<b>Paired Statistical Tests</b><br/>10k Bootstrap + Exact McNemar<br/>(Bonferroni 98.3% CI)", 850, 336, 200, 75, WHITE)

    d.group_box("5. AI Forensic Platform", 1120, 40, 220, 395, CRIMSON)
    fa = d.box("<b>AI Forensic Analyst Core</b><br/>18 Modular Stages<br/>Rule Fusion + 4D Confidence", 1135, 100, 190, 85, WHITE)
    e14 = d.box("<b>System-Level Verification</b><br/>16 End-to-End Scenarios<br/>135 Evidence-Verified Sentences", 1135, 210, 190, 80, WHITE)
    web = d.box("<b>Full-Stack Web Platform</b><br/>Django REST API + React UI<br/>85 Automated + 6 UAT Tests", 1135, 315, 190, 80, WHITE)

    gov = d.pill(
        "Reproducibility & Scientific Integrity: Immutable Configs & Audit Registries  |  Public Open-License Data  |  Leakage-Checked Splits  |  No Overclaiming",
        20, 465, 1320, 45, NEUTRAL, 11
    )

    d.edge(ds1, pp, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.2, waypoints=[(268, 107), (268, 114)])
    d.edge(ds2, pp, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.4, waypoints=[(268, 177), (268, 138)])
    d.edge(ds3, pp, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.6, waypoints=[(268, 247), (268, 162)])
    d.edge(ds4, pp, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.8, waypoints=[(268, 317), (268, 186)])
    d.edge(ds5, pp, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.95, waypoints=[(268, 387), (268, 204)])
    d.edge(pp, sp1, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(sp1, sp2, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(sp1, exp1, exit_x=1, exit_y=0.3, entry_x=0, entry_y=0.5, waypoints=[(542, 262), (542, 132)])
    d.edge(sp1, expa, exit_x=1, exit_y=0.7, entry_x=0, entry_y=0.5, waypoints=[(542, 292), (542, 337)])
    d.edge(sp2, exp2, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5, waypoints=[(548, 372), (548, 232)])
    d.edge(exp1, ev1, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(exp1, ev2, exit_x=1, exit_y=0.75, entry_x=0, entry_y=0.5, waypoints=[(818, 151), (818, 204)])
    d.edge(exp2, ev3, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5, waypoints=[(818, 232), (818, 287)])
    d.edge(expa, ev4, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(ev1, fa, label="Val Bins", exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.4, waypoints=[(1092, 120), (1092, 134)])
    d.edge(fa, e14, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(e14, web, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    _ = gov
    d.save(OUT_DIR / "FIG0026.drawio")


def build_fig0027() -> None:
    """FIG0027: 18-Module AI Forensic Analyst Pipeline & Trust Boundaries (Zero Overlaps)."""
    d = DrawioBuilder("FIG0027_Forensic_Analyst_Architecture", 1440, 635)

    # Trust Boundary A: x=20..580 (w=560)
    # Left column holds M1 (top) and Early Validation Stops F1 (bottom)
    # Right column holds M2 (top), M3 (middle), M4 (bottom) -> ZERO line crossings!
    d.group_box("TRUST BOUNDARY A: Image-Reading Layer (Isolated Collectors, Zero Decision Authority)", 20, 30, 560, 405, SLATE, dashed=True)
    m1 = d.box("<b>M1: Input Intake</b><br/>Format &amp; Size (&lt;=20 MB)<br/>SHA-256 + Metadata", 40, 78, 175, 90, WHITE)
    m2 = d.box("<b>M2: Image Validation</b><br/>Decode, RGB, Noise,<br/>Single-Face Gate", 285, 78, 275, 90, WHITE)
    f1 = d.box(
        "<b>Early Validation Stops</b><br/><br/>unsupported_format<br/>corrupted_image<br/>no_face | multiple_faces<br/><br/><i>Halt before collectors;<br/>omit verdict; log failed case</i>",
        40, 218, 175, 195, CRIMSON, font_size=10
    )
    m3 = d.box(
        "<b>M3: 9 Independent Signal Collectors</b><br/>Metadata | Image Statistics | Face Detection<br/>Face Quality | Frequency (FFT) | Compression<br/>Color Distribution | Texture | XAI Input<br/><i>(Zero inter-collector coupling)</i>",
        285, 208, 275, 102, WHITE, font_size=10
    )
    m4 = d.box("<b>M4: Deep Learning Specialist</b><br/>ResNet-50 Detector — Emits P(fake) only<br/><i>(Isolated specialist; never decides)</i>", 285, 330, 275, 83, AMBER)

    # 85px open gutter x=580..665 for clean "EV items" crossing into Trust Boundary B
    # Trust Boundary B: x=665..1420 (w=755)
    d.group_box("TRUST BOUNDARY B: Image-Blind Evidence, Reasoning, Decision & Reporting Layer (Evidence IDs Only)", 665, 30, 755, 405, TEAL, dashed=True)
    m5 = d.box("<b>M5: Evidence Ledger</b><br/>Append-Only EV IDs<br/>Immutable Storage", 685, 78, 155, 90, WHITE)
    m6 = d.box("<b>M6: Evidence Validator</b><br/>High / Med / Low / Unusable<br/>Conflict Cross-Citation", 870, 78, 160, 90, WHITE)
    m7 = d.box("<b>M7: Evidence Fusion</b><br/>Pluggable FusionStrategy<br/>Rule-Based Aggregation<br/>Fused Conclusion", 1060, 78, 160, 90, WHITE)
    m9 = d.box("<b>M9: 4D Confidence</b><br/>Val-Calibrated Bins<br/>Pred, Ev, Sys &amp; Decision", 1250, 78, 150, 90, AMBER)

    m8 = d.box("<b>M8: Decision Engine</b><br/><i>Sole Verdict Authority</i><br/>Real | Fake | Inconclusive | Unknown<br/>(Reads EV IDs only; never images)", 685, 224, 235, 95, CRIMSON)
    m10 = d.box("<b>M10: Explainability</b><br/>Structured Data-Only JSON<br/>Grad-CAM / Saliency / no_data<br/>(Zero fabricated visual maps)", 945, 224, 215, 95, WHITE)
    m11 = d.box("<b>M11: Grounded Reasoning</b><br/>Programmatic Verification<br/>Checks every cited EV ID<br/>&amp; numeric value", 1185, 224, 215, 95, WHITE)

    m12 = d.box("<b>M12: Forensic Report Generator</b><br/>Reproducible JSON, Markdown &amp; HTML Case Reports Stamped with System, Model, Dataset, Experiment &amp; Git Commit Provenance", 685, 350, 715, 62, WHITE)

    # 45px open corridor y=435..480 between upper layers and Delivery Layer
    d.group_box("DELIVERY, AUDIT & EXTENSIBILITY LAYER (M13-M18)", 20, 475, 1400, 140, NEUTRAL, dashed=False)
    m13 = d.box("<b>M13: REST API Backend</b><br/>7 Django/DRF Apps<br/>10 Endpoints (/api/v1)", 40, 518, 215, 75, SLATE)
    m14 = d.box("<b>M14: Interactive Web UI</b><br/>14 Pages, 24 Components<br/>9 Stages + 4 Conf. Gauges", 290, 518, 225, 75, SLATE)
    m15 = d.box("<b>M15: Case Audit Trail</b><br/>Append-Only Case IDs<br/>Immutable Case Ledger", 685, 518, 190, 75, WHITE)
    m16 = d.box("<b>M16: Failure Handler</b><br/>8 Canonical Failure Modes<br/>Zero Silent Failures", 900, 518, 175, 75, CRIMSON)
    m17 = d.box("<b>M17: Module Registry</b><br/>Interface &amp; Contract<br/>Integrity Validator", 1095, 518, 145, 75, WHITE)
    m18 = d.box("<b>M18: Extensibility</b><br/>Audio / Video / Text<br/>Collector &amp; Fusion Hooks", 1260, 518, 140, 75, TEAL)

    # Trust Boundary A edges (ZERO crossings!)
    d.edge(m1, m2, label="accept", exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(m1, f1, label="reject", color="#922B21", dashed=True, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    # Route M2 fail cleanly into top-right of F1 through the open center channel (x=240, y=183)
    d.edge(m2, f1, label="fail", color="#922B21", dashed=True, exit_x=0.12, exit_y=1, entry_x=1, entry_y=0.18, waypoints=[(318, 183), (240, 183), (240, 253)])
    # Route M2 pass straight down into M3, and cleanly down channel (x=262, y=197) into M4 left side
    d.edge(m2, m3, label="pass", exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(m2, m4, label="pass", exit_x=0.25, exit_y=1, entry_x=0, entry_y=0.5, waypoints=[(354, 197), (262, 197), (262, 371)])

    # M3 & M4 -> M5 cleanly through the 85px Trust Boundary gutter on separate vertical tracks (x=612 & x=632)
    d.edge(m3, m5, label="EV items", exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.4, waypoints=[(618, 259), (618, 114)])
    d.edge(m4, m5, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.75, waypoints=[(638, 371), (638, 145)])

    # Trust Boundary B internal edges
    d.edge(m5, m6, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(m6, m7, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(m7, m9, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(m9, m8, label="validated EV IDs", exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0, waypoints=[(1325, 196), (802, 196)])
    d.edge(m8, m10, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(m10, m11, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(m11, m12, exit_x=0.5, exit_y=1, entry_x=0.85, entry_y=0)
    d.edge(m8, m12, exit_x=0.5, exit_y=1, entry_x=0.16, entry_y=0)

    # Delivery & Audit edges (non-overlapping separate tracks!)
    d.edge(m12, m13, exit_x=0.06, exit_y=1, entry_x=0.5, entry_y=0, waypoints=[(728, 455), (147, 455)])
    d.edge(m13, m14, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(m12, m15, exit_x=0.13, exit_y=1, entry_x=0.5, entry_y=0)
    _ = (m16, m17, m18)
    d.save(OUT_DIR / "FIG0027.drawio")


def build_fig0028() -> None:
    """FIG0028 (Journal Fig. 1): Evidence Fusion, 4D Calibrated Confidence & 4-Way Decision."""
    d = DrawioBuilder("FIG0028_Fusion_Confidence_Decision", 1440, 585)

    # Stage 1: x=20..275 (w=255), 55px gutter to Stage 2
    d.group_box("Stage 1: Validated Evidence Ledger", 20, 30, 255, 500, SLATE)
    e1 = d.box("<b>Directional DL Evidence</b><br/>ResNet-50 Output P(fake) = p<br/>Val-Frozen Threshold t = 0.3951<br/>(or model_unavailable / timeout)", 35, 80, 225, 95, WHITE)
    e2 = d.box("<b>Contextual Forensic Evidence</b><br/>9 Non-Detector Collectors<br/>(Stats, FFT, Compression, Meta,<br/>Face, Color, Texture, XAI Input)<br/><i>Cited as context; no directional vote</i>", 35, 195, 225, 115, WHITE)
    e3 = d.box("<b>Reliability Weights (w_i)</b><br/>high = 1.0  |  medium = 0.6<br/>low = 0.3  |  unusable = 0.0<br/>+ Conflict Cross-Citation Flag", 35, 330, 225, 100, AMBER)
    e4 = d.pill("Invariant: Source rows never mutated", 35, 460, 225, 42, NEUTRAL, 10)

    # Stage 2: x=330..615 (w=285), 55px gutter to Stage 3
    d.group_box("Stage 2: Reliability-Weighted Fusion", 330, 30, 285, 500, TEAL)
    f_cfg = d.box("<b>Pluggable FusionStrategy</b><br/>Active: Rule-Based (v0.1.0)<br/>Reserved: Weighted, Bayesian<br/>(Unknown ID -&gt; Structured Error)", 345, 80, 255, 85, WHITE)
    f_rule = d.box(
        "<b>Weighted Directional Aggregation</b><br/>p &gt;= t -&gt; +w_i (positive_class)<br/>p &lt;  t -&gt; -w_i (negative_class)<br/>Unusable items excluded (w = 0)",
        345, 188, 255, 92, WHITE
    )
    f_out = d.box(
        "<b>Fused Conclusion Record</b><br/>1. positive_class (clear lean)<br/>2. negative_class (clear lean)<br/>3. contested (both sides, |bal| &lt; 0.5)<br/>4. no_directional_evidence<br/><i>Zero verdict words emitted</i>",
        345, 305, 255, 125, WHITE
    )
    f_val = d.pill("Logged &amp; Graded Before Downstream Use", 345, 460, 255, 42, NEUTRAL, 10)

    # Stage 3: x=670..995 (w=325), 75px gutter to Stage 4 for "EV IDs" label
    d.group_box("Stage 3: 4D Calibrated Confidence", 670, 30, 325, 500, AMBER)
    c1 = d.box("<b>1. Prediction Confidence (C_pred)</b><br/>r = p if p &gt;= t else 1 - p<br/>Lookup val reliability bin accuracy A_val(r)<br/>C_pred = w_det * A_val(r)  (null if absent)", 685, 76, 295, 84, WHITE, font_size=10)
    c2 = d.box("<b>2. Evidence Confidence (C_ev)</b><br/>Mean reliability weight (unusable = 0.0)<br/>x 0.50 if evidence conflict flagged", 685, 176, 295, 68, WHITE, font_size=10)
    c3 = d.box("<b>3. System Confidence (C_sys)</b><br/>Usable Items / (Attempts + Refused + Errors)", 685, 260, 295, 58, WHITE, font_size=10)
    c4 = d.box(
        "<b>4. Decision Confidence (C_dec)</b><br/>C_base = 0.5*C_pred + 0.3*C_ev + 0.2*C_sys<br/>Cap at min(C_ev, C_sys) if either &lt;= 0.50<br/>or zero usable non-DL collectors;<br/>x 0.85 single-source | x 0.50 contested | null if C_pred null",
        685, 334, 295, 106, WHITE, font_size=10
    )
    c5 = d.pill("Safety Override: p=0.99 -&gt; C_dec=0.3333", 685, 460, 295, 42, CRIMSON, 10)

    # Stage 4: x=1070..1420 (w=350) with wide 35px left/right routing channels around pills!
    d.group_box("Stage 4: Image-Blind 4-Way Decision", 1070, 30, 350, 500, CRIMSON)
    d_in = d.box("<b>Decision Engine (Sole Arbiter)</b><br/>Reads ONLY validated fused conclusion<br/>and calibrated confidence EV IDs<br/><i>(Zero image or weight access)</i>", 1110, 80, 265, 85, WHITE)
    o_fake = d.pill("FAKE  (positive_class, no conflict, C_dec &gt;= 0.50)", 1110, 206, 265, 54, CRIMSON, 10)
    o_real = d.pill("REAL  (negative_class, no conflict, C_dec &gt;= 0.50)", 1110, 282, 265, 54, TEAL, 10)
    o_inc = d.pill("INCONCLUSIVE  (contested, conflict, or C_dec &lt; 0.50)", 1110, 358, 265, 54, AMBER, 10)
    o_unk = d.pill("UNKNOWN  (no_directional_evidence; C_dec = null)", 1110, 434, 265, 54, NEUTRAL, 10)

    # Clean non-overlapping edges in wide white gutters
    d.edge(e1, f_rule, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.25, waypoints=[(302, 127), (302, 211)])
    d.edge(e2, f_rule, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.55, waypoints=[(302, 252), (302, 239)])
    d.edge(e3, f_rule, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.85, waypoints=[(302, 380), (302, 266)])
    d.edge(f_cfg, f_rule, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(f_rule, f_out, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(f_out, c1, exit_x=1, exit_y=0.3, entry_x=0, entry_y=0.5, waypoints=[(642, 342), (642, 118)])
    d.edge(f_out, c4, exit_x=1, exit_y=0.7, entry_x=0, entry_y=0.5)
    d.edge(c4, d_in, label="EV IDs", exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.35, waypoints=[(1032, 387), (1032, 110)])

    # Distinct, well-separated output channels inside Stage 4 (zero crowding!)
    d.edge(d_in, o_fake, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(d_in, o_real, exit_x=0, exit_y=0.72, entry_x=0, entry_y=0.5, waypoints=[(1088, 141), (1088, 309)])
    d.edge(d_in, o_inc, exit_x=1, exit_y=0.35, entry_x=1, entry_y=0.5, waypoints=[(1390, 110), (1390, 385)])
    d.edge(d_in, o_unk, dashed=True, exit_x=1, exit_y=0.72, entry_x=1, entry_y=0.5, waypoints=[(1406, 141), (1406, 461)])
    _ = (e4, f_val, c2, c3, c5)
    d.save(OUT_DIR / "FIG0028.drawio")


def build_fig0029() -> None:
    """FIG0029: Three-Tier Full-Stack Web Architecture (Zero Overlapping Edges)."""
    d = DrawioBuilder("FIG0029_Three_Tier_Web_Architecture", 1420, 570)

    # Tier 1: x=20..320 (w=300), clean vertical chain w1 -> w2 -> w3
    d.group_box("Tier 1: React Frontend Presentation Layer", 20, 30, 300, 495, SLATE)
    w1 = d.box("<b>React 18.3 + Vite 6 + Tailwind 3.4</b><br/>14 Investigation &amp; Docs Pages<br/>24 Accessible Components (ARIA)<br/>9 Real-Time Pipeline Stage Labels", 35, 78, 270, 92, WHITE)
    w2 = d.box("<b>Scoped Client State</b><br/>SystemContext (/health, /version)<br/>ThemeContext (light/dark + alerts)<br/>useInvestigation(caseId) Polling Hook", 35, 198, 270, 88, WHITE)
    w3 = d.box("<b>Centralized API Client (src/api/)</b><br/>forensicApi.js | http.js | errors.js<br/>Env Base URL + Dev Proxy<br/><i>Zero direct fetch() outside src/api/</i>", 35, 314, 270, 92, AMBER)
    w4 = d.pill("Forbidden: Inference &amp; Threshold Logic", 35, 440, 270, 45, CRIMSON, 10)

    # Wide gutter x=320..405 (85px) for HTTP JSON / Multipart arrow + label
    # Tier 2: x=405..845 (w=440)
    # Right column holds Forensic Job Service (top-right) & Evidence/Report Adapters (bottom-right)
    # so EVERY outbound call to Tier 3 exits cleanly into the wide gutter without crossing ANY box!
    d.group_box("Tier 2: Django 5.2 + DRF 3.18 REST API Layer", 405, 30, 440, 495, TEAL)
    b1 = d.box("<b>REST API Router (10 Canonical Endpoints)</b><br/>POST /cases | GET /cases/{id} | POST /upload<br/>GET /status, /evidence, /decision, /explanation, /report<br/>GET /health | GET /version (mounted at / and /api/v1/)", 425, 78, 400, 92, WHITE, font_size=10)
    b4 = d.box("<b>Health &amp; Provenance</b><br/>Readiness Probe (no model load)<br/>Live Git + Model Metadata", 425, 198, 185, 88, WHITE, font_size=10)
    b2 = d.box("<b>Forensic Job Service</b><br/>ThreadPoolExecutor (Async / Sync)<br/>Thread-Safe Lock Serialization<br/>Per-Case Stage Status Tracking", 635, 198, 190, 88, WHITE, font_size=10)
    b5 = d.box("<b>Security &amp; Operations</b><br/>dev/test/prod .env | 20 MB Cap<br/>Rate Throttles | Structured Errors<br/>7 Rotating Log Channels", 425, 314, 185, 92, WHITE, font_size=10)
    b3 = d.box("<b>Evidence &amp; Report Adapters</b><br/>Read-Only Artifact Readers<br/>Byte-Identical decision.json<br/>JSON / MD / HTML Output", 635, 314, 190, 92, WHITE, font_size=10)
    b6 = d.pill("Forbidden: Duplicated Forensic Logic &amp; Stack Traces", 425, 440, 400, 45, CRIMSON, 10)

    # Wide gutter x=845..955 (110px) for clean Tier 2 -> Tier 3 labeled arrows
    # Tier 3: x=955..1400 (w=445); right margin x=1380 reserved for c1 -> c3 bypass!
    d.group_box("Tier 3: AI Forensic Core & Persistent Storage", 955, 30, 445, 495, AMBER)
    c1 = d.box("<b>Forensic Pipeline Orchestrator</b><br/>run_investigation() Core Engine (18 Modules)<br/>Isolated DL Specialist + Evidence Fusion + Decision<br/>(60.02 ms Mean End-to-End Latency)", 975, 78, 385, 92, WHITE)
    c2 = d.box("<b>Append-Only Audit Registries (CSV)</b><br/>Model Registry (Weights &amp; Frozen Thresholds)<br/>Evidence Ledger (Immutable EV IDs &amp; Validation)<br/>Case Audit Registry (Completed &amp; Failed Cases)", 975, 198, 385, 88, SLATE, font_size=10)
    c3 = d.box("<b>Versioned Per-Case Media Storage</b><br/>Immutable Uploads (-input-01, -input-02)<br/>decision.json | explanation.json | reasoning.json<br/>Case Reports (.json, .md, .html) | Failure Logs", 975, 314, 385, 92, NEUTRAL, font_size=10)
    c4 = d.pill("Verified: 85 Automated Tests + Live Integration + 6 UAT", 975, 440, 385, 45, TEAL, 10)

    # Tier 1 vertical flow: w1 -> w2 -> w3 (zero overlap!)
    d.edge(w1, w2, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(w2, w3, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    # Tier 1 -> Tier 2 cleanly through the 85px white gutter
    d.edge(w3, b1, label="HTTP JSON /<br/>Multipart", exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5, waypoints=[(362, 360), (362, 124)])

    # Tier 2 internal routing (zero box crossings!)
    d.edge(b1, b4, exit_x=0.23, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(b1, b2, exit_x=0.76, exit_y=1, entry_x=0.5, entry_y=0)
    # Route b1 -> b3 down the open center channel (x=622) between left & right columns
    d.edge(b1, b3, exit_x=0.49, exit_y=1, entry_x=0, entry_y=0.5, waypoints=[(622, 184), (622, 360)])

    # Tier 2 -> Tier 3 cleanly through the 110px white gutter (zero overlap!)
    d.edge(b2, c1, label="run_investigation()", exit_x=1, exit_y=0.35, entry_x=0, entry_y=0.5, waypoints=[(900, 229), (900, 124)])
    d.edge(b3, c2, label="read-only", dashed=True, exit_x=1, exit_y=0.28, entry_x=0, entry_y=0.5, waypoints=[(892, 340), (892, 242)])
    d.edge(b3, c3, label="read-only", dashed=True, exit_x=1, exit_y=0.72, entry_x=0, entry_y=0.72)

    # Tier 3 internal storage writes: c1 -> c2 straight down; c1 -> c3 cleanly around right channel (x=1380)
    d.edge(c1, c2, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(c1, c3, exit_x=1, exit_y=0.5, entry_x=1, entry_y=0.5, waypoints=[(1380, 124), (1380, 360)])

    _ = (w4, b5, b6, c4)
    d.save(OUT_DIR / "FIG0029.drawio")


def build_fig0030() -> None:
    """FIG0030: Reproducible Training, SHA-256 Checkpointing & Storage Architecture."""
    d = DrawioBuilder("FIG0030_Training_Checkpoint_Sync", 1380, 580)

    # Swimlane 1: y=20..160 (title at top-left: zero arrows cross top edge)
    d.group_box("Swimlane 1: Git Source & Metadata Tier (Code, Configs & Lightweight Metrics — Zero Large Binaries)", 20, 20, 1340, 140, SLATE)
    g1 = d.box("<b>Immutable Run Config</b><br/>Declarative YAML Spec<br/>47 Schema Validation Tests", 45, 66, 220, 74, WHITE)
    g2 = d.box("<b>Frozen Splits &amp; Env Lock</b><br/>Grouped &amp; LOGO Splits<br/>Python 3.12 | PyTorch 2.10 | FastAI 2.8", 305, 66, 260, 74, WHITE)
    g3 = d.box("<b>Synced Lightweight Outputs</b><br/>Test/Val Predictions (CSV)<br/>Epoch Logs &amp; Metric Summaries", 635, 66, 275, 74, WHITE)
    g4 = d.box("<b>Auditable Registries</b><br/>Experiment &amp; Model Registries<br/>SHA-256 Checkpoint Manifests", 995, 66, 340, 74, WHITE)

    # 55px open corridor y=160..215 for labeled arrows between Swimlanes 1 & 2
    # Swimlane 2: y=215..395 (title at top-center x=420..960: arrows cross only at x<=220 and x=1120!)
    d.group_box("Swimlane 2: Cloud GPU Training Execution (NVIDIA T4 — Config-Driven FastAI Pipeline)", 20, 215, 1340, 180, TEAL, align="center", valign="top")
    k1 = d.box("<b>Pre-Flight Guards</b><br/>Config Hash + Git Revision<br/>Fresh vs. Resume Guard<br/>Dataset &amp; Leakage Verification", 45, 265, 215, 105, WHITE)
    k2 = d.box("<b>LR Finder &amp; Training Loop</b><br/>ResNet-50 (ImageNet-1k)<br/>Adam (wd=0.01) + FP16<br/>Fine-Tune (1 Frozen + 10 Unfrozen)", 305, 265, 245, 105, WHITE)
    # 95px open horizontal gap between k2 (ends 550) and k3 (starts 645) for "every epoch" / "resume"
    k3 = d.box("<b>Atomic Checkpoint Store</b><br/>Never-Overwritten Epoch Files<br/>Weights + Opt + RNG + SHA-256<br/>Auto-Quarantine Corrupt Resume", 645, 265, 255, 105, AMBER)
    k4 = d.box("<b>Finalize &amp; Val-Only Threshold</b><br/>Restore Best Epoch (valid_loss)<br/>Freeze Threshold on Validation ONLY<br/>Export Predictions, ECE &amp; Summary", 965, 265, 370, 105, WHITE)

    # 55px open corridor y=395..450 for labeled dashed arrows between Swimlanes 2 & 3
    # Swimlane 3: y=450..555 (title at bottom-left: zero arrows cross bottom edge!)
    d.group_box("Swimlane 3: External Data & Artifact Storage Tiers (Large Binaries Excluded from Git)", 20, 450, 1340, 105, NEUTRAL, align="left", valign="bottom")
    a1 = d.pill("Data Storage Tier: Preprocessed 224x224 RGB PNG Corpora (5 Public Datasets, ~250k Images)", 45, 470, 560, 44, SLATE, 10)
    a2 = d.pill("Artifact Storage Tier: Best &amp; Last Checkpoints (.pth) | Serialized Inference Exports (.pkl, ~105 MB)", 645, 470, 690, 44, AMBER, 10)

    # Clean non-overlapping edges across wide corridors
    d.edge(g1, k1, exit_x=0.5, exit_y=1, entry_x=0.35, entry_y=0, waypoints=[(155, 188), (120, 188)])
    d.edge(g2, k1, exit_x=0.2, exit_y=1, entry_x=0.8, entry_y=0, waypoints=[(357, 188), (217, 188)])
    d.edge(a1, k1, label="read-only mount", dashed=True, exit_x=0.19, exit_y=0, entry_x=0.5, entry_y=1)
    d.edge(k1, k2, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(k2, k3, label="every epoch", exit_x=1, exit_y=0.3, entry_x=0, entry_y=0.3)
    d.edge(k3, k2, label="resume", dashed=True, color="#B9770E", exit_x=0, exit_y=0.75, entry_x=1, entry_y=0.75)
    d.edge(k3, k4, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(k3, a2, label="checkpoint push", dashed=True, exit_x=0.5, exit_y=1, entry_x=0.18, entry_y=0)
    d.edge(k4, a2, label="model export", dashed=True, exit_x=0.5, exit_y=1, entry_x=0.73, entry_y=0)
    d.edge(k4, g3, label="binary-guarded git sync", exit_x=0.45, exit_y=0, entry_x=0.5, entry_y=1, waypoints=[(1131, 188), (772, 188)])
    d.edge(g3, g4, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.save(OUT_DIR / "FIG0030.drawio")


def main() -> None:
    build_fig0026()
    build_fig0027()
    build_fig0028()
    build_fig0029()
    build_fig0030()
    for fid in ["FIG0026", "FIG0027", "FIG0028", "FIG0029", "FIG0030"]:
        p = OUT_DIR / f"{fid}.drawio"
        ET.parse(p)
        print(f"Verified valid Draw.io XML: {p.relative_to(ROOT)} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
