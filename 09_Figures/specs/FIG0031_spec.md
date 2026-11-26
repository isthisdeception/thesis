# Figure Spec: FIG0031

**Purpose:** Complete multi-dataset visual sample atlas across all five public benchmark corpora (`DS0001`–`DS0005`), covering every evaluated authentic source, synthetic generator, and demographic race subgroup directly in the main manuscript.  
**Required data:** Forty-nine newly selected `224 x 224` lossless PNG samples from `_processed_dataset/`: `(a)` `DS0001` ArtiFact (`3` authentic sources + `13` synthetic generators = `16`), `(b)` `DS0003` 140k Real and Fake Faces (`2` FFHQ authentic + `2` StyleGAN synthetic = `4`), `(c)` `DS0002` DiFF official test (`12` unseen diffusion generators across `FE`, `FS`, `I2I`, `T2I`), `(d)` `DS0005` FairFace (`7` official demographic subgroups verified from `fairface_label_val.csv` + `1` legend key), and `(e)` `DS0004` Synthbuster (`1` RAISE authentic + `9` diffusion generators = `10`).  
**Recommended chart type:** Structured five-block (`(a)`–`(e)`) `5 x 10` square-thumbnail layout with rounded dataset containers, subgroup headers, and embedded legend card.  
**Exact axes:** Axes ticks hidden; class-coded frame (`#3B6D9A` for Authentic `Real`, `#B85C38` for Synthetic `Fake`) around each `224 x 224` panel.  
**Legend:** Embedded legend card in block `(d)` indicating Authentic (`Real`) vs. Synthetic (`Fake`) frame colors and `224 x 224` lossless RGB preprocessing.  
**Caption:** Preprocessed authentic and synthetic samples (`224 x 224` px) covering every generator, source, and demographic subgroup across `(a)` ArtiFact, `(b)` 140k Faces, `(c)` DiFF, `(d)` FairFace, and `(e)` Synthbuster.  
**Color recommendations:** Real `#3B6D9A`; Fake `#B85C38`.  
**Data source path:** `_processed_dataset/*/metadata/index.csv` and `_staging/DS0005_fairface/kaggle_upload/ds0005-fairface/raw/DS0005/fairface_label_val.csv`.  
**Responsible notebook:** `09_Figures/scripts/render_figures.py` (`--only FIG0031`).  
**Expected output filename:** `09_Figures/assets/FIG0031_v1.png` and `09_Figures/assets/FIG0031_v1.pdf`
