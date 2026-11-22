# Figure Spec: FIG0029

**Purpose:** Show the three-tier full-stack web architecture (`12_Web` React/Vite `MOD014`, `13_Backend` 7-app Django/DRF `MOD013`, and `11_AI_Forensic_System` core) including strict tier separation, `_PIPELINE_LOCK` async execution, 10 canonical REST endpoints, and persistent CSV/media storage.  
**Required data:** Tier contracts from `16_Documentation/architecture.md`, `16_Documentation/integration_guide.md`, `13_Backend/architecture.md`, and `12_Web/architecture.md`.  
**Recommended chart type:** Three-tier architectural component diagram with storage tier panel (IEEE/ACM double-column width, `7.16 in` / `182 mm`).  
**Exact axes:** Not applicable (software system architecture diagram).  
**Legend:** Slate `#1F618D` = Frontend UI (`12_Web`, zero inference, centralized `src/api/`); Teal `#117A65` = REST Backend (`13_Backend`, 7 single-responsibility apps, zero duplicated forensic logic); Amber `#B9770E` = Forensic Core (`11_AI_Forensic_System`); Neutral Gray = Immutable Registries & Per-Case Versioned Media.  
**Caption:** Three-tier system architecture connecting the React 18 frontend (`12_Web`, `MOD014`, 14 pages, 24 accessible components), the seven-app Django/DRF REST API (`13_Backend`, `MOD013`, 10 endpoints, `_PIPELINE_LOCK` thread safety), and the 18-module AI Forensic Analyst core (`11_AI_Forensic_System`) with append-only CSV registries and versioned per-case media storage.  
**Color recommendations:** Slate `#1F618D`, teal `#117A65`, amber `#B9770E`, neutral `#566573`, light fill `#F4F6F9`, crisp white canvas `#FFFFFF`.  
**Data source path:** `16_Documentation/architecture.md`; `16_Documentation/workflow_diagrams/system_architecture.md`.  
**Responsible notebook:** Editable Draw.io source `09_Figures/diagrams/FIG0029.drawio`.  
**Manual creation instructions:** Open `09_Figures/diagrams/FIG0029.drawio` in diagrams.net, verify clean arrow spacing between the 3 tiers and persistent registries, and export cropped vector PDF (`FIG0029_v1.pdf`) plus 600 DPI PNG (`FIG0029_v1.png`).  
**Expected output filename:** `09_Figures/assets/FIG0029_v1.png` (and vector `09_Figures/assets/FIG0029_v1.pdf`, human-exported).
