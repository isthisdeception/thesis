# Figure Spec: FIG0034

**Purpose:** Compare fairness-matched in-distribution discrimination (`DS0001` `SPLIT0001` test, `n = 7,505`) and zero-shot cross-dataset error polarization (`DS0002`–`DS0005`, `n = 38,864`) across three distinct detector architectures: `MODEL0001` (ResNet-50), `MODEL0003` (EfficientNet-B4), and `MODEL0004` (ViT-B/16).  
**Required data:** `06_Experiments/EXP0001/predictions/test_predictions.csv`, `06_Experiments/EXP0007/predictions/test_predictions.csv`, `06_Experiments/EXP0008/predictions/test_predictions.csv`, and `08_Evaluation/cross_backbone_generalization.csv`.  
**Recommended chart type:** Two-panel horizontal composite: `(a)` paired ROC curves with validation-frozen operating points on `DS0001` test (`n = 7,505`), and `(b)` grouped bar chart of zero-shot cross-dataset FNR and FPR across `DS0001`–`DS0005` (`46,369` evaluated images per model).  
**Exact axes:** Panel `(a)` X = False Positive Rate, Y = True Positive Rate; Panel `(b)` X = Dataset error strata (`ArtiFact`, `DiFF FNR`, `140k FNR`, `140k FPR`, `Synth. FNR`, `Synth. FPR`, `FairFace FPR`), Y = Error rate (`%`).  
**Caption:** Multi-backbone comparison across ResNet-50, EfficientNet-B4, and ViT-B/16 showing `(a)` paired in-distribution ROC curves (`n = 7,505`) and `(b)` zero-shot cross-dataset FNR and FPR polarization (`n = 46,369` per model).  
**Data source path:** `08_Evaluation/cross_backbone_generalization.csv` and `06_Experiments/EXP000{1,7,8}/predictions/test_predictions.csv`.  
**Responsible notebook:** `09_Figures/scripts/render_figures.py` (`--only FIG0034`).  
**Expected output filename:** `09_Figures/assets/FIG0034_v1.png` and `09_Figures/assets/FIG0034_v1.pdf`
