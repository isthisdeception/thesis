"""Build publication-grade Draw.io (.drawio) diagrams for FIG0026-FIG0030.

Outputs editable diagrams.net XML files under 09_Figures/diagrams/ using a
cohesive, colorblind-safe IEEE/ACM double-column palette. Per Policy A.9,
these are editable diagram sources; the human inspects and exports vector PDF
and 600 DPI PNG files into 09_Figures/assets/.
"""

from __future__ import annotations

import os
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "09_Figures" / "diagrams"

# IEEE/ACM colorblind-safe palette
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
    ) -> str:
        fill, stroke, font = palette
        cid = self._next_id()
        style = (
            f"rounded=1;arcSize=4;whiteSpace=wrap;html=1;align=left;verticalAlign=top;"
            f"spacingTop=6;spacingLeft=10;fontFamily=Helvetica;fontSize=12;fontStyle=1;"
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
    ) -> str:
        cid = self._next_id()
        pts = ""
        if exit_x is not None and exit_y is not None:
            pts += f"exitX={exit_x};exitY={exit_y};exitDx=0;exitDy=0;"
        if entry_x is not None and entry_y is not None:
            pts += f"entryX={entry_x};entryY={entry_y};entryDx=0;entryDy=0;"
        style = (
            f"edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;"
            f"fontFamily=Helvetica;fontSize=10;fontColor={color};strokeColor={color};strokeWidth=1.4;"
            f"endArrow=block;endFill=1;{'dashed=1;dashPattern=5 3;' if dashed else ''}{pts}"
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
        ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
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
    d = DrawioBuilder("FIG0026_Methodology_Pipeline", 1320, 560)
    d.group_box("1. Public-Only Data Tier (DEC0004-DEC0005, Checklist 3 PASS)", 20, 40, 230, 390, SLATE)
    ds1 = d.box("<b>DS0001</b> ArtiFact Faces<br/>50k (25k/25k, 13 gens, MIT)", 35, 85, 200, 55, WHITE)
    ds2 = d.box("<b>DS0002</b> DiFF Official Test<br/>51,452 proc. (13 DMs, fake)", 35, 155, 200, 55, WHITE)
    ds3 = d.box("<b>DS0003</b> 140k Real &amp; Fake<br/>70k FFHQ / 70k StyleGAN", 35, 225, 200, 55, WHITE)
    ds4 = d.box("<b>DS0004</b> Synthbuster<br/>9k DMs + 999 RAISE scenes", 35, 295, 200, 55, WHITE)
    ds5 = d.box("<b>DS0005</b> FairFace (CC BY)<br/>97,698 real (7 race groups)", 35, 365, 200, 55, WHITE)

    d.group_box("2. Preprocessing & Splits (Checklist 4)", 280, 40, 240, 390, SLATE)
    pp = d.box(
        "<b>Versioned 7-Stage Pipeline</b><br/>PP0001-PP0006 (seed 42)<br/>Verify -&gt; Meta -&gt; Strip EXIF<br/>Filter &gt;=64px -&gt; RGB PNG<br/>Resize 224x224 (no denoise)",
        295, 95, 210, 120, WHITE
    )
    sp1 = d.box("<b>SPLIT0001</b> (Grouped Random)<br/>DS0001: 34,993 / 7,502 / 7,505<br/>Leakage Check: PASS", 295, 240, 210, 75, WHITE)
    sp2 = d.box("<b>SPLIT0002</b> (LOGO Holdout)<br/>stable_diffusion held out (1,923)<br/>Leakage Check: PASS", 295, 335, 210, 75, WHITE)

    d.group_box("3. Model Experiments (Checklists 5-6)", 550, 40, 240, 390, TEAL)
    exp1 = d.box("<b>EXP0001 / MODEL0001</b><br/>ResNet-50 Baseline (T4 GPU)<br/>Frozen Val Threshold: 0.3951", 565, 95, 210, 75, WHITE)
    exp2 = d.box("<b>EXP0002 / MODEL0008</b><br/>Unseen-Generator LOGO<br/>(stable_diffusion excluded)", 565, 195, 210, 75, WHITE)
    expa = d.box("<b>EXP0003-EXP0006</b><br/>One-Factor Ablations (DEC0008)<br/>Seed | No-Aug | No-Pre | 160px", 565, 295, 210, 85, WHITE)

    d.group_box("4. 18-Phase Evaluation (Checklist 8)", 820, 40, 230, 390, AMBER)
    ev1 = d.box("<b>E1-E6, E12</b> Metrics &amp; Errors<br/>Calibration (ECE 0.0525)<br/>Subgroup FNR / FPR Analysis", 835, 90, 200, 70, WHITE)
    ev2 = d.box("<b>E7 Robustness</b> (53 Distortions)<br/>JPEG, Blur, Noise, Resize, Upload", 835, 175, 200, 65, WHITE)
    ev3 = d.box("<b>E8-E9 Generalization</b><br/>DS0002-DS0005 + LOGO Paired", 835, 255, 200, 65, WHITE)
    ev4 = d.box("<b>E10-E11 Statistics</b><br/>10k Bootstrap + Exact McNemar<br/>(superiority_claim = none)", 835, 335, 200, 75, WHITE)

    d.group_box("5. Forensic Platform (Checklists 9-12)", 1080, 40, 220, 390, CRIMSON)
    fa = d.box("<b>AI Forensic Analyst</b><br/>18 Modules (MOD001-MOD018)<br/>DEC0009 Fusion + DEC0010 Conf.", 1095, 105, 190, 85, WHITE)
    e14 = d.box("<b>Phase E14 (EVAL0007)</b><br/>16 Scenarios / 9 Dimensions PASS<br/>135 EV-Verified Sentences", 1095, 215, 190, 80, WHITE)
    web = d.box("<b>Full-Stack Web + UAT</b><br/>Django API + React UI<br/>85 Tests + 6 Live UAT PASS", 1095, 320, 190, 80, WHITE)

    gov = d.pill(
        "Reproducibility Governance: GitHub Source Tier (Registries, Configs, Audits)  |  Kaggle Data & Artifact Tiers  |  Decision Logs DEC0001-DEC0010",
        20, 465, 1280, 45, NEUTRAL, 11
    )

    d.edge(ds1, pp, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.3)
    d.edge(ds2, pp, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(ds3, pp, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.7)
    d.edge(pp, sp1, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(sp1, sp2, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(sp1, exp1, exit_x=1, exit_y=0.3, entry_x=0, entry_y=0.5)
    d.edge(sp1, expa, exit_x=1, exit_y=0.7, entry_x=0, entry_y=0.5)
    d.edge(sp2, exp2, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(exp1, ev1, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(exp1, ev2, exit_x=1, exit_y=0.7, entry_x=0, entry_y=0.5)
    d.edge(exp2, ev3, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(expa, ev4, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(ev1, fa, label="E4 Val Bins", exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.4)
    d.edge(fa, e14, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(e14, web, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    _ = (ds4, ds5, gov)
    d.save(OUT_DIR / "FIG0026.drawio")


def build_fig0027() -> None:
    """FIG0027: 18-Module AI Forensic Analyst Pipeline & Trust Boundaries."""
    d = DrawioBuilder("FIG0027_Forensic_Analyst_Architecture", 1360, 620)

    # Trust Boundary 1: Image-Reading Layer
    d.group_box("TRUST BOUNDARY A: Image-Reading Layer (Per-Collector Isolation, Zero Decision Authority)", 20, 30, 520, 380, SLATE, dashed=True)
    m1 = d.box("<b>MOD001</b><br/>Input Management<br/>ext/size &lt;=20MB<br/>input_metadata.json", 40, 80, 145, 95, WHITE)
    m2 = d.box("<b>MOD002</b><br/>Image Validation<br/>decode, RGB, noise,<br/>single-face gate", 205, 80, 145, 95, WHITE)
    m3 = d.box(
        "<b>MOD003: 9 Independent Collectors</b><br/>metadata | image_statistics | face_detection<br/>face_quality | frequency_domain | compression<br/>color_distribution | texture | explainability_input<br/><i>(Zero inter-collector imports)</i>",
        40, 210, 310, 105, WHITE, font_size=10
    )
    m4 = d.box("<b>MOD004</b><br/>DL Specialist<br/>MODEL0001<br/>Emits P(fake) only<br/><i>(Never decides)</i>", 370, 210, 150, 105, AMBER)
    f1 = d.box("<b>MOD016 Early Stops</b><br/>unsupported_format | corrupted_image | no_face | multiple_faces<br/><i>(Halt before collectors; no decision.json; append failed CASE row)</i>", 40, 335, 480, 55, CRIMSON, font_size=10)

    # Trust Boundary 2: Image-Blind Evidence & Decision Layer
    d.group_box("TRUST BOUNDARY B: Image-Blind Evidence, Reasoning, Decision & Reporting Layer (EV IDs Only)", 570, 30, 770, 380, TEAL, dashed=True)
    m5 = d.box("<b>MOD005</b><br/>Evidence Registry<br/>Append-only EV IDs<br/>evidence_registry.csv", 590, 80, 165, 90, WHITE)
    m6 = d.box("<b>MOD006</b><br/>Evidence Validator<br/>high/med/low/unusable<br/>conflict cross-citation", 780, 80, 165, 90, WHITE)
    m7 = d.box("<b>MOD007</b><br/>Evidence Fusion<br/>FusionStrategy<br/>(rule_based, DEC0009)<br/>fused_conclusion", 970, 80, 165, 90, WHITE)
    m9 = d.box("<b>MOD009</b><br/>4D Confidence<br/>e4_calibrated_v1<br/>(DEC0010 val bins)", 1160, 80, 160, 90, AMBER)

    m8 = d.box("<b>MOD008 Decision Engine</b><br/><i>Sole Verdict Authority</i><br/>Real | Fake | Inconclusive | Unknown<br/>(Reads EV IDs only; never images)", 590, 215, 240, 95, CRIMSON)
    m10 = d.box("<b>MOD010 Explainability</b><br/>Data-only explanation.json<br/>grad_cam / saliency / no_data<br/>(Policy A.9: zero rendered imgs)", 855, 215, 215, 95, WHITE)
    m11 = d.box("<b>MOD011 Reasoning</b><br/>reasoning.json<br/>verify_sentence() checks<br/>every cited EV ID &amp; value", 1095, 215, 225, 95, WHITE)

    m12 = d.box("<b>MOD012 Forensic Report Generator</b><br/>Reproducible JSON + Markdown (Template 24) + HTML stamped with system, model, dataset, experiment &amp; Git commit SHA", 590, 335, 730, 55, WHITE)

    # Governance & Delivery Layer
    d.group_box("DELIVERY, AUDIT & GOVERNANCE LAYER (MOD013-MOD018)", 20, 440, 1320, 145, NEUTRAL, dashed=False)
    m13 = d.box("<b>MOD013 REST API</b><br/>7 Django/DRF Apps<br/>10 Endpoints (/api/v1)", 40, 485, 210, 75, SLATE)
    m14 = d.box("<b>MOD014 React Web UI</b><br/>14 Pages, 24 Components<br/>9 Stages + 4 Gauges", 275, 485, 215, 75, SLATE)
    m15 = d.box("<b>MOD015 Audit Trail</b><br/>Append-only CASExxxxxx<br/>case_registry.csv", 515, 485, 210, 75, WHITE)
    m16 = d.box("<b>MOD016 Failure Engine</b><br/>8 Canonical Failure Modes<br/>Zero Silent Failures", 750, 485, 210, 75, CRIMSON)
    m17 = d.box("<b>MOD017 Module Registry</b><br/>Spec &amp; Contract Validator<br/>module_registry.csv", 985, 485, 165, 75, WHITE)
    m18 = d.box("<b>MOD018 Extensibility</b><br/>Audio / Video / Text<br/>Collector &amp; Strategy Hooks", 1170, 485, 150, 75, TEAL)

    d.edge(m1, m2, label="accept", exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(m1, f1, label="reject", color="#922B21", dashed=True, exit_x=0.5, exit_y=1, entry_x=0.2, entry_y=0)
    d.edge(m2, f1, label="fail", color="#922B21", dashed=True, exit_x=0.8, exit_y=1, entry_x=0.6, entry_y=0)
    d.edge(m2, m3, label="pass", exit_x=0.4, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(m2, m4, label="pass", exit_x=1, exit_y=0.7, entry_x=0.5, entry_y=0)
    d.edge(m4, m5, label="EV items", exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(m5, m6, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(m6, m7, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(m7, m9, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(m9, m8, label="validated EV IDs", exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(m8, m10, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(m10, m11, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(m11, m12, exit_x=0.5, exit_y=1, entry_x=0.85, entry_y=0)
    d.edge(m8, m12, exit_x=0.5, exit_y=1, entry_x=0.2, entry_y=0)
    d.edge(m12, m13, exit_x=0.1, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(m13, m14, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(m12, m15, exit_x=0.4, exit_y=1, entry_x=0.5, entry_y=0)
    _ = (m16, m17, m18)
    d.save(OUT_DIR / "FIG0027.drawio")


def build_fig0028() -> None:
    """FIG0028 (Journal Fig. 1): Evidence Fusion, 4D E4 Confidence & 4-Way Decision."""
    d = DrawioBuilder("FIG0028_Fusion_Confidence_Decision", 1320, 580)

    d.group_box("Stage 1: Validated Evidence (MOD005-MOD006)", 20, 30, 260, 490, SLATE)
    e1 = d.box("<b>MOD004 Directional Evidence</b><br/>MODEL0001 P(fake) = p<br/>Frozen Val Threshold t = 0.3951<br/>(or model_unavailable / timeout)", 35, 80, 230, 95, WHITE)
    e2 = d.box("<b>MOD003 Contextual Evidence</b><br/>9 Non-Detector Collectors<br/>(Stats, Freq, Comp, Meta, Face,<br/>Color, Texture, XAI Input)<br/><i>Cited as context; no directional vote</i>", 35, 195, 230, 115, WHITE)
    e3 = d.box("<b>MOD006 Reliability Weights (w_i)</b><br/>high = 1.0  |  medium = 0.6<br/>low = 0.3  |  unusable = 0.0<br/>+ Conflict Cross-Citation Flag", 35, 330, 230, 100, AMBER)
    e4 = d.pill("Invariant: Source rows never mutated", 35, 455, 230, 40, NEUTRAL, 10)

    d.group_box("Stage 2: Evidence Fusion (MOD007, DEC0009)", 310, 30, 290, 490, TEAL)
    f_cfg = d.box("<b>Swappable FusionStrategy</b><br/>Active: rule_based (v0.1.0)<br/>Reserved: weighted, bayesian<br/>(Unknown ID -&gt; MOD016 error)", 325, 80, 260, 85, WHITE)
    f_rule = d.box(
        "<b>Reliability-Weighted Aggregation</b><br/>p &gt;= t -&gt; +w_i (positive_class)<br/>p &lt;  t -&gt; -w_i (negative_class)<br/>unusable items excluded (w=0)",
        325, 185, 260, 95, WHITE
    )
    f_out = d.box(
        "<b>fused_conclusion EV Item</b><br/>1. positive_class (clear lean)<br/>2. negative_class (clear lean)<br/>3. contested (both sides, |bal| &lt; 0.5)<br/>4. no_directional_evidence<br/><i>Zero verdict words emitted</i>",
        325, 305, 260, 125, WHITE
    )
    f_val = d.pill("Registered by MOD005 + Graded by MOD006", 325, 455, 260, 40, NEUTRAL, 10)

    d.group_box("Stage 3: 4D E4 Confidence (MOD009, DEC0010)", 630, 30, 330, 490, AMBER)
    c1 = d.box("<b>1. prediction_confidence (C_pred)</b><br/>r = p if p&gt;=t else 1-p<br/>Lookup EVAL0001 val bin accuracy A_val(r)<br/>C_pred = w_det * A_val(r)  (null if absent)", 645, 75, 300, 85, WHITE, font_size=10)
    c2 = d.box("<b>2. evidence_confidence (C_ev)</b><br/>Mean MOD006 weight (unusable = 0.0)<br/>x 0.5 if conflict flagged", 645, 175, 300, 70, WHITE, font_size=10)
    c3 = d.box("<b>3. system_confidence (C_sys)</b><br/>Usable Items / (Attempts + Refused + MOD016)", 645, 260, 300, 60, WHITE, font_size=10)
    c4 = d.box(
        "<b>4. decision_confidence (C_dec)</b><br/>C_base = 0.5*C_pred + 0.3*C_ev + 0.2*C_sys<br/>Cap at min(C_ev, C_sys) if either &lt;= 0.5<br/>or zero usable non-DL collectors;<br/>x 0.85 single-source | x 0.50 contested | null if C_pred null",
        645, 335, 300, 105, WHITE, font_size=10
    )
    c5 = d.pill("Example E14-10: p=0.99 -&gt; C_dec=0.3333", 645, 455, 300, 40, CRIMSON, 10)

    d.group_box("Stage 4: Image-Blind Decision (MOD008)", 990, 30, 310, 490, CRIMSON)
    d_in = d.box("<b>MOD008 Decision Engine</b><br/>Reads ONLY validated fused_conclusion<br/>and confidence EV IDs<br/><i>(Zero image or weight access)</i>", 1005, 80, 280, 85, WHITE)
    o_fake = d.pill("FAKE  (positive_class, no conflict, C_dec &gt;= 0.50)", 1005, 195, 280, 55, CRIMSON, 10)
    o_real = d.pill("REAL  (negative_class, no conflict, C_dec &gt;= 0.50)", 1005, 270, 280, 55, TEAL, 10)
    o_inc = d.pill("INCONCLUSIVE  (contested, conflict, or C_dec &lt; 0.50)", 1005, 345, 280, 55, AMBER, 10)
    o_unk = d.pill("UNKNOWN  (no_directional_evidence; C_dec = null)", 1005, 420, 280, 55, NEUTRAL, 10)

    d.edge(e1, f_rule, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.3)
    d.edge(e2, f_rule, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.6)
    d.edge(e3, f_rule, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.85)
    d.edge(f_cfg, f_rule, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(f_rule, f_out, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(f_out, c1, exit_x=1, exit_y=0.3, entry_x=0, entry_y=0.5)
    d.edge(f_out, c4, exit_x=1, exit_y=0.7, entry_x=0, entry_y=0.5)
    d.edge(c4, d_in, label="EV IDs", exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(d_in, o_fake, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(d_in, o_real, exit_x=0.15, exit_y=1, entry_x=0, entry_y=0.5)
    d.edge(d_in, o_inc, exit_x=0.85, exit_y=1, entry_x=1, entry_y=0.5)
    d.edge(d_in, o_unk, dashed=True, exit_x=0.95, exit_y=1, entry_x=1, entry_y=0.5)
    _ = (e4, f_val, c2, c3, c5)
    d.save(OUT_DIR / "FIG0028.drawio")


def build_fig0029() -> None:
    """FIG0029: Three-Tier Full-Stack Web Architecture."""
    d = DrawioBuilder("FIG0029_Three_Tier_Web_Architecture", 1320, 560)

    d.group_box("Tier 1: Frontend Presentation (12_Web / MOD014)", 20, 30, 310, 480, SLATE)
    w1 = d.box("<b>React 18.3 + Vite 6 + Tailwind 3.4</b><br/>14 Canonical Pages<br/>24 Accessible Components (WCAG/ARIA)<br/>9 Live MOD014 Stage Labels", 40, 80, 270, 95, WHITE)
    w2 = d.box("<b>State Boundaries</b><br/>SystemContext (/health, /version)<br/>ThemeContext (light/dark + toasts)<br/>useInvestigation(caseId) hook", 40, 195, 270, 85, WHITE)
    w3 = d.box("<b>Centralized API Client (src/api/)</b><br/>forensicApi.js | http.js | errors.js<br/>VITE_API_BASE_URL / Vite Proxy<br/><i>Zero fetch() outside src/api/</i>", 40, 300, 270, 90, AMBER)
    w4 = d.pill("Forbidden: Inference &amp; Threshold Logic", 40, 420, 270, 45, CRIMSON, 10)

    d.group_box("Tier 2: Django 5.2 + DRF 3.18 REST Backend (13_Backend / MOD013)", 370, 30, 430, 480, TEAL)
    b1 = d.box("<b>apps.api (10 Canonical Endpoints)</b><br/>POST /cases | GET /cases/{id} | POST /upload<br/>GET /status, /evidence, /decision, /explanation, /report<br/>GET /health | GET /version (mounted at / and /api/v1/)", 390, 80, 390, 90, WHITE, font_size=10)
    b2 = d.box("<b>apps.forensic_engine</b><br/>ThreadPoolExecutor (thread / eager)<br/>_PIPELINE_LOCK Serialization<br/>job_status.json Stage Tracking", 390, 190, 185, 95, WHITE, font_size=10)
    b3 = d.box("<b>apps.evidence &amp; apps.reports</b><br/>Read-Only Adapters<br/>Byte-identical decision.json<br/>JSON / MD / HTML Reports", 595, 190, 185, 95, WHITE, font_size=10)
    b4 = d.box("<b>apps.health &amp; apps.versioning</b><br/>Readiness Probe (no model load)<br/>Live Git + Model Provenance", 390, 305, 185, 80, WHITE, font_size=10)
    b5 = d.box("<b>apps.core Security &amp; Ops</b><br/>dev/test/prod .env | 20MB Cap<br/>DRF Throttles | MOD016 Handler<br/>7 Rotating Log Channels", 595, 305, 185, 80, WHITE, font_size=10)
    b6 = d.pill("Forbidden: Duplicated Forensic Logic &amp; User Stack Traces", 390, 420, 390, 45, CRIMSON, 10)

    d.group_box("Tier 3: Forensic Core & Registries (11_AI_Forensic_System)", 840, 30, 460, 480, AMBER)
    c1 = d.box("<b>run_investigation() Orchestrator</b><br/>11_AI_Forensic_System/pipeline.py<br/>MOD001-MOD012, MOD015-MOD018<br/>(60.02 ms mean E14 latency)", 860, 80, 420, 90, WHITE)
    c2 = d.box("<b>Immutable CSV Registries (Append-Only)</b><br/>05_Models/model_registry.csv<br/>11_AI_Forensic_System/evidence_registry.csv (EV IDs)<br/>11_AI_Forensic_System/case_registry.csv (CASE IDs)", 860, 195, 420, 95, SLATE, font_size=10)
    c3 = d.box("<b>Versioned Per-Case Media (FORENSIC_MEDIA_ROOT)</b><br/>cases/{case_id}/-input-01, -input-02 (never overwritten)<br/>decision.json | explanation.json | reasoning.json<br/>reports/{case_id}_report.{json,md,html} | failures/", 860, 315, 420, 95, NEUTRAL, font_size=10)
    c4 = d.pill("Verified: 85 Automated Tests + Live Integration + 6 UAT PASS", 860, 435, 420, 40, TEAL, 10)

    d.edge(w1, w3, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(w3, b1, label="HTTP JSON / Multipart", exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(b1, b2, exit_x=0.25, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(b1, b3, exit_x=0.75, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(b2, c1, label="run_investigation()", exit_x=1, exit_y=0.3, entry_x=0, entry_y=0.5)
    d.edge(c1, c2, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(c1, c3, exit_x=0.85, exit_y=1, entry_x=0.85, entry_y=0)
    d.edge(b3, c2, label="read-only", dashed=True, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(b3, c3, label="read-only", dashed=True, exit_x=1, exit_y=0.8, entry_x=0, entry_y=0.5)
    _ = (w2, w4, b4, b5, b6, c4)
    d.save(OUT_DIR / "FIG0029.drawio")


def build_fig0030() -> None:
    """FIG0030: Reproducible FastAI Training, SHA-256 Checkpointing & Policy A.6 Sync."""
    d = DrawioBuilder("FIG0030_Training_Checkpoint_Sync", 1320, 520)

    d.group_box("Swimlane 1: GitHub Source Tier (Single Source of Truth — Zero Large Binaries)", 20, 25, 1280, 140, SLATE)
    g1 = d.box("<b>Immutable Config</b><br/>EXPxxxx/config.yaml<br/>47 Validator Tests PASS", 45, 70, 220, 75, WHITE)
    g2 = d.box("<b>Frozen Split &amp; Env Lock</b><br/>SPLIT0001 / SPLIT0002<br/>versions.lock.md (plum 2.5.7)", 315, 70, 240, 75, WHITE)
    g3 = d.box("<b>Synced Lightweight Outputs</b><br/>predictions/*.csv | metrics/*.json<br/>logs/EXPxxxx_epochs.csv", 630, 70, 270, 75, WHITE)
    g4 = d.box("<b>Updated Registries</b><br/>experiment_registry.csv<br/>model_registry.csv | 07_Checkpoints/", 975, 70, 295, 75, WHITE)

    d.group_box("Swimlane 2: Kaggle T4 GPU Execution (17_Automation/training/ — Thin Notebook Wrapper)", 20, 195, 1280, 180, TEAL)
    k1 = d.box("<b>Pre-Flight Guards</b><br/>Config Hash + Git Ancestry<br/>Fresh vs. Resume Output Guard<br/>Dataset &amp; Leakage Check", 45, 245, 220, 105, WHITE)
    k2 = d.box("<b>LR Finder &amp; FastAI Learner</b><br/>ResNet-50 (ImageNet-1k)<br/>Adam (wd=0.01) + FP16<br/>fine_tune (1 frozen + 10 unfrozen)", 310, 245, 245, 105, WHITE)
    k3 = d.box("<b>Atomic CheckpointStore</b><br/>EXPxxxx_epoch_NNN.pth<br/>Weights + Opt + RNG + SHA-256<br/>Auto-Quarantine Corrupt Resume", 600, 245, 260, 105, AMBER)
    k4 = d.box("<b>Finalize &amp; Val-Only Threshold</b><br/>Load Best Epoch (valid_loss)<br/>Freeze Threshold on Val ONLY<br/>Write Predictions, ECE, Summary", 910, 245, 360, 105, WHITE)

    d.group_box("Swimlane 3: Kaggle Data &amp; Artifact Tiers (Policy A.6 — Git-Ignored Binaries)", 20, 405, 1280, 95, NEUTRAL)
    a1 = d.pill("Kaggle Data Tier: Processed 224x224 PNG Datasets (ds0001-pp0001 ... ds0005-pp0005)", 45, 442, 540, 42, SLATE, 10)
    a2 = d.pill("Kaggle Artifact Tier: EXPxxxx_best.pth | EXPxxxx_last.pth | MODELxxxx_export.pkl (~105 MB)", 625, 442, 645, 42, AMBER, 10)

    d.edge(g1, k1, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0)
    d.edge(g2, k1, exit_x=0.2, exit_y=1, entry_x=0.8, entry_y=0)
    d.edge(a1, k1, label="read-only mount", dashed=True, exit_x=0.25, exit_y=0, entry_x=0.5, entry_y=1)
    d.edge(k1, k2, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(k2, k3, label="every epoch", exit_x=1, exit_y=0.35, entry_x=0, entry_y=0.35)
    d.edge(k3, k2, label="resume", dashed=True, color="#B9770E", exit_x=0, exit_y=0.75, entry_x=1, entry_y=0.75)
    d.edge(k3, k4, exit_x=1, exit_y=0.5, entry_x=0, entry_y=0.5)
    d.edge(k3, a2, label="binary push", dashed=True, exit_x=0.5, exit_y=1, entry_x=0.3, entry_y=0)
    d.edge(k4, a2, label="export.pkl", dashed=True, exit_x=0.5, exit_y=1, entry_x=0.75, entry_y=0)
    d.edge(k4, g3, label="binary-guarded git sync", exit_x=0.25, exit_y=0, entry_x=0.5, entry_y=1)
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
