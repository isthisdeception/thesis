# Figure Spec: FIG0031

**Purpose:** Representative visual grid of preprocessed authentic and synthetic samples across all five benchmark datasets (`DS0001`–`DS0005`).  
**Required data:** Ten verified `224 x 224` lossless PNG samples from `_processed_dataset/` (`DS0001` real CelebA-HQ & fake StyleGAN3; `DS0002` fake SDXL & fake Midjourney; `DS0003` real FFHQ & fake StyleGAN; `DS0004` real RAISE scene & fake DALL-E 3; `DS0005` two demographically diverse real portraits).  
**Recommended chart type:** Two-row by five-column (`2 x 5`) image grid with explicit `(a)`–`(j)` subfigure labels beneath each panel and dataset headers above each column.  
**Exact axes:** Axes ticks hidden; thin color-coded border (`#3B6D9A` for Real, `#B85C38` for Fake) framing each `224 x 224` panel.  
**Legend:** Border color and panel sublabels indicate ground-truth class (`Real` vs. `Fake`) and generator/source provenance.  
**Caption:** Representative preprocessed samples (`224 x 224` px) across the five public benchmark datasets, labeled `(a)` through `(j)`.  
**Color recommendations:** Real `#3B6D9A`; Fake `#B85C38`.  
**Data source path:** `_processed_dataset/*/metadata/index.csv` and corresponding processed PNG assets.  
**Responsible script:** `09_Figures/scripts/render_figures.py` (`--only FIG0031`).  
**Expected output filename:** `09_Figures/assets/FIG0031_v1.png` and `09_Figures/assets/FIG0031_v1.pdf`
