# Figure Spec: FIG0030

**Purpose:** Diagram the reproducible config-driven FastAI training pipeline (`17_Automation/training/`), SHA-256 atomic resumable checkpointing (`CheckpointStore`), validation-only threshold freezing, and three-tier Local-GitHub-Kaggle storage synchronization (Policy A.6).  
**Required data:** Training lifecycle from `17_Automation/training/README.md`, `07_Checkpoints/checkpoint_policy.md`, and `06_Experiments/EXP0001/config.yaml`.  
**Recommended chart type:** Two-swimlane workflow diagram separating Kaggle GPU execution from GitHub Source Tier and Kaggle Artifact/Data Tiers (IEEE/ACM double-column width, `7.16 in` / `182 mm`).  
**Exact axes:** Not applicable (engineering workflow diagram).  
**Legend:** Slate `#1F618D` = Pre-flight guards & immutable config validation; Teal `#117A65` = Kaggle T4 training & SHA-256 atomic resume loop; Amber `#B9770E` = Validation-only thresholding & metric export; Neutral Gray = Source Tier (GitHub) vs. Artifact/Data Tier (Kaggle).  
**Caption:** Config-driven FastAI training and fault-tolerant checkpoint architecture (`17_Automation/training/`). Every run validates immutable YAML configs and dataset splits prior to GPU execution, writes never-overwritten SHA-256 recovery checkpoints (`EXPxxxx_epoch_NNN.pth`) with full RNG/optimizer restoration and automatic corrupt-file quarantine, freezes operating thresholds strictly on validation, and enforces Policy A.6 binary separation between GitHub and Kaggle.  
**Color recommendations:** Slate `#1F618D`, teal `#117A65`, amber `#B9770E`, crimson `#922B21`, light neutral fill `#F4F6F9`, crisp white canvas `#FFFFFF`.  
**Data source path:** `17_Automation/training/README.md`; `06_Experiments/EXP0001/config.yaml`.  
**Responsible notebook:** Editable Draw.io source `09_Figures/diagrams/FIG0030.drawio`.  
**Manual creation instructions:** Open `09_Figures/diagrams/FIG0030.drawio` in diagrams.net, verify swimlane labels and resume-loop arrow clarity, and export cropped vector PDF (`FIG0030_v1.pdf`) plus 600 DPI PNG (`FIG0030_v1.png`).  
**Expected output filename:** `09_Figures/assets/FIG0030_v1.png` (and vector `09_Figures/assets/FIG0030_v1.pdf`, human-exported).
