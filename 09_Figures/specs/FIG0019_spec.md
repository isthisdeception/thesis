# Figure Spec: FIG0019

**Purpose:** Unseen-generator result (Phase E9): detection of Stable Diffusion when it was never seen in training, against seen generators and against the model that did see it.  
**Required data:** `unseen_detection.csv` (recall per generator with `role`, `ci_low`, `ci_high`); `unseen_paired.csv` (recall of MODEL0001 and MODEL0008 on the same Stable Diffusion images).  
**Recommended chart type:** Panel A: dot plot with 95% intervals. Panel B: two bars (paired recall) with the 2 × 2 agreement counts as a table beneath.  
**Exact axes:** Panel A: Y = generator (unseen first, then seen generators sorted by recall, then "all seen generators"); X = recall (0–1). Panel B: X = model (MODEL0001: seen in training; MODEL0008: unseen); Y = recall on the same images (0–1).  
**Legend:** unseen (test), seen (val); Panel B bars by model.  
**Caption:** MODEL0008 (EXP0002) was trained without Stable Diffusion; recall on Stable Diffusion test images at its val-chosen threshold, against seen generators on val. Panel B compares MODEL0001 and MODEL0008 on the 299 Stable Diffusion images in the EXP0001 test split.  
**Color recommendations:** unseen `#C0392B`; seen `#1F618D`; MODEL0001 `#1E8449`; MODEL0008 `#C0392B`.  
**Data source path:** `08_Evaluation/EVAL0002/unseen_generator/unseen_detection.csv`; `08_Evaluation/EVAL0002/unseen_generator/unseen_paired.csv`.  
**Responsible notebook:** `06_Experiments/EXP0002/notebook/EXP0002_train.ipynb` (training) → `python -m generalization unseen`.  
**Manual creation instructions:** Note in the caption that val images also set the threshold. State that one generator was held out (DEC0007).  
**Expected output filename:** `09_Figures/assets/FIG0019_v1.png`
