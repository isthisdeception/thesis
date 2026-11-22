# Figure Spec: FIG0026

**Purpose:** Illustrate the end-to-end research and evaluation methodology pipeline from five public datasets through versioned preprocessing, leakage-free splitting, reproducible training, 18-phase evaluation, and whole-platform forensic verification.  
**Required data:** Registered pipeline lineage from `03_Datasets/metadata/datasets.csv` (`DS0001`–`DS0005`), `04_Preprocessing/preprocessing_registry.csv` (`PP0001`–`PP0006`), `03_Datasets/metadata/split_registry.csv` (`SPLIT0001`–`SPLIT0002`), `06_Experiments/experiment_registry.csv` (`EXP0001`–`EXP0006`), and `08_Evaluation/evaluation_registry.csv` (`EVAL0001`–`EVAL0007`).  
**Recommended chart type:** Horizontal multi-stage architectural block diagram (IEEE/ACM double-column width, `7.16 in` / `182 mm`).  
**Exact axes:** Not applicable (architectural pipeline diagram); left-to-right data and governance flow with top-level quality gate checkpoints (Checklists 3, 4, 5, 6, 8, 9).  
**Legend:** Color-coded stage groups: Data/Preprocessing (slate `#1F618D`), Training/Experiments (teal `#117A65`), Evaluation Tracks (amber `#B9770E`), Forensic Platform & Audit Gates (crimson `#922B21` dashed outline).  
**Caption:** End-to-end reproducible research and evaluation pipeline spanning public dataset curation (`DS0001`–`DS0005`), seven-stage preprocessing (`PP0001`–`PP0006`), leakage-checked grouped (`SPLIT0001`) and leave-one-generator-out (`SPLIT0002`) splitting, six GPU experiments (`EXP0001`–`EXP0006`), Phases E1–E18 evaluation (`EVAL0001`–`EVAL0006`), and whole-platform AI Forensic Analyst verification (`EVAL0007`).  
**Color recommendations:** Slate `#1F618D`, teal `#117A65`, amber `#B9770E`, crimson `#922B21`, light neutral fill `#F4F6F9`, crisp white canvas `#FFFFFF`.  
**Data source path:** `03_Datasets/metadata/dataset_registry.csv`; `06_Experiments/experiment_registry.csv`; `08_Evaluation/evaluation_registry.csv`.  
**Responsible notebook:** Editable Draw.io source `09_Figures/diagrams/FIG0026.drawio`.  
**Manual creation instructions:** Open `09_Figures/diagrams/FIG0026.drawio` in diagrams.net (app.diagrams.net or VS Code Draw.io extension), inspect alignment and text readability at 100% print width, and export cropped vector PDF (`FIG0026_v1.pdf`) plus 600 DPI PNG (`FIG0026_v1.png`).  
**Expected output filename:** `09_Figures/assets/FIG0026_v1.png` (and vector `09_Figures/assets/FIG0026_v1.pdf`, human-exported).
