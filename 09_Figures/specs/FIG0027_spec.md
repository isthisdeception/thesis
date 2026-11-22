# Figure Spec: FIG0027

**Purpose:** Visualize the 18-module AI Forensic Analyst architecture (`MOD001`–`MOD018`), explicitly highlighting the strict security and scientific trust boundary separating image-reading modules from image-blind evidence, fusion, decision, explanation, and reporting modules, plus `MOD016` early-stop failure gates.  
**Required data:** Module contracts and trust boundaries from `11_AI_Forensic_System/architecture.md`, `11_AI_Forensic_System/module_registry.csv`, and `16_Documentation/workflow_diagrams/forensic_pipeline.md`.  
**Recommended chart type:** Layered pipeline architecture diagram with dashed trust-boundary container (IEEE/ACM double-column width, `7.16 in` / `182 mm`).  
**Exact axes:** Not applicable (system architecture diagram); left-to-right stage progression with bottom governance bar (`MOD015`–`MOD018`) and top/bottom rejection paths (`MOD016`).  
**Legend:** Dashed blue container = Image-Reading Layer (`MOD001`–`MOD004`, per-collector isolation); Dashed teal container = Image-Blind Evidence & Decision Layer (`MOD005`–`MOD012`); Red boxes = `MOD016` structured stop gates; Slate bar = Transport & Governance (`MOD013`–`MOD018`).  
**Caption:** Architecture and trust boundaries of the 18-module AI Forensic Analyst (`MOD001`–`MOD018`). Raw image bytes are accessible only to intake (`MOD001`), validation (`MOD002`), and isolated evidence collectors (`MOD003`, `MOD004`); the Decision Engine (`MOD008`) reads validated `EV` identifiers only, while `MOD016` records all eight canonical failure modes without silent fallback.  
**Color recommendations:** Slate `#1F618D`, teal `#117A65`, amber `#B9770E`, crimson `#922B21`, light neutral fill `#F4F6F9`, crisp white canvas `#FFFFFF`.  
**Data source path:** `11_AI_Forensic_System/module_registry.csv`; `11_AI_Forensic_System/architecture.md`.  
**Responsible notebook:** Editable Draw.io source `09_Figures/diagrams/FIG0027.drawio`.  
**Manual creation instructions:** Open `09_Figures/diagrams/FIG0027.drawio` in diagrams.net, verify trust-boundary dashed frame and arrow routing, and export cropped vector PDF (`FIG0027_v1.pdf`) plus 600 DPI PNG (`FIG0027_v1.png`).  
**Expected output filename:** `09_Figures/assets/FIG0027_v1.png` (and vector `09_Figures/assets/FIG0027_v1.pdf`, human-exported).
