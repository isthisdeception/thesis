# Figure Spec: FIG0028

**Purpose:** Present the mathematical and logical flow of reliability-weighted evidence fusion (`MOD007`, `DEC0009`), four-dimensional E4-calibrated confidence estimation (`MOD009`, `DEC0010`), and image-blind four-way forensic decision mapping (`MOD008`) — serving as the signature methodology diagram (Figure 1 candidate for the journal manuscript).  
**Required data:** Approved rule tables and equations from `01_Project_Management/decision_log/DEC0009.md`, `01_Project_Management/decision_log/DEC0010.md`, and `08_Evaluation/EVAL0001/confidence_distribution.csv` (`split=val`).  
**Recommended chart type:** Four-column structured decision-flow diagram with explicit formula callout boxes and four-way verdict outcomes (IEEE/ACM double-column width, `7.16 in` / `182 mm`).  
**Exact axes:** Not applicable (methodological decision flowchart).  
**Legend:** Slate `#1F618D` = `MOD005`/`MOD006` validated evidence & reliability weights; Teal `#117A65` = `MOD007` swappable `FusionStrategy`; Amber `#B9770E` = `MOD009` 4D E4-calibrated confidence (`e4_calibrated_v1`); Crimson/Teal/Amber/Gray outcome pills = `MOD008` `Fake`, `Real`, `Inconclusive`, `Unknown`.  
**Caption:** Reliability-weighted evidence fusion (`MOD007`, `DEC0009`), four-dimensional validation-calibrated confidence estimation (`MOD009`, `DEC0010`), and image-blind four-way decision rules (`MOD008`). Unusable supporting evidence or specialist conflict caps `decision_confidence` below `0.50`, routing high raw detector scores to `Inconclusive` rather than forcing an unverified binary verdict; missing directional evidence yields `Unknown` with `null` prediction and decision confidence.  
**Color recommendations:** Slate `#1F618D`, teal `#117A65`, amber `#B9770E`, crimson `#922B21`, light neutral fill `#F4F6F9`, crisp white canvas `#FFFFFF`.  
**Data source path:** `01_Project_Management/decision_log/DEC0009.md`; `01_Project_Management/decision_log/DEC0010.md`; `11_AI_Forensic_System/fusion/fusion_config.json`; `11_AI_Forensic_System/confidence/confidence_config.json`; `11_AI_Forensic_System/decision/decision_config.json`.  
**Responsible notebook:** Editable Draw.io source `09_Figures/diagrams/FIG0028.drawio`.  
**Manual creation instructions:** Open `09_Figures/diagrams/FIG0028.drawio` in diagrams.net, verify formula legibility and four-way decision branches, and export cropped vector PDF (`FIG0028_v1.pdf`) plus 600 DPI PNG (`FIG0028_v1.png`).  
**Expected output filename:** `09_Figures/assets/FIG0028_v1.png` (and vector `09_Figures/assets/FIG0028_v1.pdf`, human-exported).
