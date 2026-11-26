# Paper Summary: P0039

## Metadata
- **Paper ID:** P0039
- **Title:** Attention and residual mechanism-based CNN architecture (ARC-Net) with enhanced fairness generalization for deepfake facial image detection
- **Authors:** Md Shihab Reza, Farhana Elias, Monirul Islam Mahmud, Nova Ahmed
- **Year:** 2026
- **Venue:** PLoS ONE (21(4): e0340099)
- **DOI:** 10.1371/journal.pone.0340099

## Problem
Deepfake (DF) facial images pose growing threats in misinformation, online harassment, and targeted attacks against women and marginalized groups, particularly in underrepresented regions such as Bangladesh and South Asia. Existing deep learning detectors often apply residual or attention blocks in isolation, attend to irrelevant background regions, suffer from geographic/demographic dataset bias (leading to high false positive rates on underrepresented populations), and rarely combine out-of-distribution (OOD) testing, ablation analysis, statistical significance testing, and quantitative explainability in a single study.

## Motivation
Combining residual convolutional blocks with spatial/channel attention atop a compact EfficientNetB0 backbone enables the detector to preserve subtle, localized manipulation cues (facial boundaries, unnatural textures, lighting inconsistencies) without losing gradient stability or attending to background noise. Furthermore, incorporating a small fraction (<1%) of real Bangladeshi facial images into training/validation directly tests whether minimal targeted regional representation can mitigate subgroup bias and improve probability calibration on South Asian faces.

## Method
A supervised binary classification pipeline (`Real` vs. `Fake`) with standardized preprocessing, residual–attention refinement, subgroup fairness auditing, and dual XAI verification (Section 3, Fig. 1):
1. **Preprocessing and augmentation (Section 3.2, Table 2):** Lanczos interpolation resize to `224 × 224 × 3`, pixel rescaling to `[0, 1]`, and training-only augmentations: horizontal flip (`p = 0.5`), random rotation (`±12°`), random zoom (`up to 1.1×`), and Gaussian noise (`σ = 0.03`, clipped to `[0, 1]`). Validation and test sets undergo resizing and normalization only.
2. **Residual and attention feature refinement (Section 3.4, Algorithm 1, Fig. 3):** Feature maps from an ImageNet-pretrained EfficientNetB0 backbone pass through stacked residual convolutional blocks (`y_j = F_j(x_j, {W_j}) + x_j`) followed by an attention module before `GlobalAveragePooling2D`, dropout (`0.5`), dense aggregation, and a 2-unit softmax classification head.
3. **Explainable AI & quantitative localization (Sections 3.5, 4.5, 4.6):** Qualitative **Grad-CAM** heatmaps and **LIME** superpixel explanations are supplemented by quantitative heatmap-to-human-mask overlap evaluation (IoU, Dice, Peak-in-Mask) on VGG Image Annotator (VIA) masks.
4. **Fairness & statistical validation (Section 4.3.1, Tables 9–10):** Compares ARC-Net trained without South Asian faces (Model A) vs. with 400 real Bangladeshi faces (Model B) on 100 held-out real South Asian faces using False Positive Rate (FPR), probability calibration (Brier score), and McNemar's paired test.

## Architecture
**ARC-Net** (Fig. 3, Algorithm 1, Table 3, Table 13):
- **Backbone:** `EfficientNetB0` (ImageNet-pretrained, `include_top = False`; frozen in Table 13 ablation description, while Algorithm 1 step 14 also notes fine-tuning top-k layers with `η = 10^-5`).
- **Residual stack:** Convolutional Block 1 (`Conv2D 1280` ×2 + residual), Convolutional Block 2 (`Conv2D 256` + ReLU + `Conv2D 256` ×2 + residual), Convolutional Block 3 (`Conv2D 512` + ReLU + `Conv2D 512` ×2 + residual) in Fig. 3.
- **Attention module:** Softmax spatial attention layer (`A_ij = exp(W_att · x + b_att) / Σ exp(...)`, Glorot uniform weights, zero bias in Eq. 2 / Section 3.4), while Algorithm 1 lines 7–8 depict sequential channel attention (`M_c` via GAP + FC1/ReLU/FC2/Sigmoid) and spatial attention (`M_s` via `7×7` conv over `[AvgPool; MaxPool]`).
- **Classification head:** `GlobalAveragePooling2D` → Dense layer with ReLU + `BatchNormalization` + `Dropout(0.5)` (note: Table 3 lists `256` dense units, whereas Fig. 1 and Fig. 3 show `512` units) → `Dense(2)` with `Softmax` output (note: Table 3 lists `sparse_categorical_crossentropy`, Section 3.4 text mentions categorical cross-entropy, and Algorithm 1 line 12 writes `L_BCE`).
- **Compared baselines (Tables 3, 5, 6):** `DenseNet121`, `ResNet-50`, `InceptionV3`, `MobileNetV2` (all ImageNet-pretrained), plus standalone `EfficientNetB0` in Table 14 (VGG16 and ResNet50V2 are also listed in Table 3 parameter summary).

## Dataset
- **Hybrid 140k Real/Fake Faces + 500 Bangladeshi real images (Section 3.1, Table 1):**
  - `140k Real and Fake Faces` (Kaggle, XHLULU [1]): 70,000 real faces from FFHQ + 70,000 fake faces (`100,000` train, `20,000` val, `20,000` test).
  - Extended with `500` IRB-approved real facial images collected in Bangladesh (North South University IRB `2024/OR-NSU/IRB/1109`; Jan 6 – Apr 4, 2025): `200` added to train, `200` to val, `100` held out for test (`140,500` total: `100,200` train, `20,200` val, `20,100` test).
  - The 500 Bangladeshi images are **not publicly available** due to privacy/ethics (available via data agreement request); the Kaggle datasets are publicly available.
- **Deepfake Dataset (Kaggle, Singh [2], Table 1):** `142,100` total images (`102,100` train, `20,000` val, `20,000` test).
- **Deepfake Database (Kaggle, Khan [3], Table 1):** `19,457` total images (`12,023` train, `7,104` val, `330` test).
- **XAI Annotation Subset (Section 4.6):** `200` manually annotated images (100 fake, 100 real) with VIA binary masks (`224×224`), split 70/30 (`140` train, `60` held-out test).

## Training
- **Hardware (Section 3.6):** Intel Core i5-13500HX CPU, 16 GB DDR5 RAM, NVIDIA GeForce RTX 4050 GPU (6 GB DDR6), 1 TB NVMe SSD.
- **Software:** Windows OS, Python, TensorFlow / Keras API, Jupyter Notebook.
- **Hyperparameters (Section 3.3, 3.6, Table 3):** Adam optimizer (`lr = 5e-4`), batch size `64`, `30` epochs (~2.5–3 hours total wall-clock time; ~5–6 min/epoch; `< 5 GB` peak GPU memory), `Dropout(0.5)`, `BatchNormalization`, `ReduceLROnPlateau` and early stopping callbacks.

## Evaluation
- **In-domain benchmark & baseline comparison (Section 4.1, Tables 5–6):** Evaluated on the hybrid `140k + 500 BD` test set (`20,100` images) against DenseNet121, ResNet-50, InceptionV3, and MobileNetV2 using accuracy, loss, per-class precision/recall/F1, ROC-AUC, and confusion matrices.
- **Multi-dataset evaluation (Section 4.2, Table 7):** Trained and tested on Deepfake Dataset [2] and Deepfake Database [3].
- **Subgroup fairness & calibration (Section 4.3.1, Tables 9–10):** Model A (no South Asian data) vs. Model B (+400 real BD images) on 100 held-out real South Asian images using FPR (95% CI), Mean/Median `prob_real`, Brier Score, and McNemar's paired test.
- **Out-of-Distribution (OOD) generalization (Sections 4.3.2–4.3.3, Tables 11–12):**
  - `OOD-1`: Trained on 140k Real/Fake Faces (Dataset A), tested unseen on Deepfake Database (B) and Deepfake Dataset (C).
  - `OOD-2`: Trained on Deepfake Dataset (A), tested unseen on Deepfake Database (B) and 140k Real/Fake Faces (C).
- **Ablation study (Section 4.4, Tables 13–14):** Variants A (frozen EfficientNetB0 baseline), B (A + Attention), C (A + Residual blocks), D (DenseNet121 + Residual + Attention), and full ARC-Net.
- **XAI localization evaluation (Sections 4.5–4.6, Table 15):** Qualitative Grad-CAM & LIME inspection (plus DenseNet121/ResNet-50 Grad-CAM comparison) and quantitative IoU, Dice, and Peak-in-Mask on `60` held-out annotated test images.

## Results
- **Hybrid 140k + 500 BD test set (Tables 5–6, Fig. 5b, Fig. 7a):**
  - **ARC-Net:** `99.53%` train accuracy, **`99%`** test accuracy, **`0.05`** test loss, **`0.99`** ROC-AUC. Real class: Precision `0.97`, Recall `1.00`, F1 `0.99`; Fake class: Precision `1.00`, Recall `0.97`, F1 `0.98` (0 false positives on real images, 300 false negatives on fake images in Fig. 7a).
  - **Baselines (Tables 5–6):** DenseNet121 (`98%` test acc, `0.06` loss, `0.98` AUC in Fig. 6b), ResNet-50 (`92%` test acc, `0.12` loss), InceptionV3 (`78%` test acc, `0.45` loss), MobileNetV2 (`68%` test acc, `0.58` loss).
- **Multi-dataset generalizability (Table 7, Figs. 8–10):**
  - **Deepfake Dataset [2]:** `99.52%` train acc, **`97.60%`** test acc (`1.92%` gap), `0.0703` test loss, `0.98` P/R/F1 for both classes, `1.00` ROC-AUC.
  - **Deepfake Database [3]:** `99.87%` train acc, **`99.33%`** test acc, `0.0231` test loss, `0.99` P/R/F1 for both classes, `1.00` ROC-AUC.
- **South Asian subgroup fairness (Table 10, `n = 100` held-out real BD images):**
  - **Model A (no BD data):** FPR = **`22.0%`** (95% CI: `14.3–31.4`), Mean `prob_real` = `0.7200`, Median = `0.7300`, Brier Score = `0.1800`.
  - **Model B (+400 BD real images):** FPR = **`10.0%`** (95% CI: `4.9–18.0`) — a **12 percentage point** absolute / **54.5%** relative FPR reduction; Mean `prob_real` = `0.8600`, Median = `0.7300`, Brier Score = **`0.1100`**.
  - **McNemar's test:** `p = 0.028` (Model B fixed 15 errors made by A, while A got 3 right where B erred; 75 both right, 7 both wrong; statistically significant at `α = 0.05`).
- **OOD generalization (Tables 11–12):**
  - **OOD-1 (trained on 140k):** `98.5%` in-domain val acc; **`94.2%`** acc (`0.94` F1) on unseen Deepfake Database; **`93.7%`** acc (`0.94` F1) on unseen Deepfake Dataset.
  - **OOD-2 (trained on Deepfake Dataset):** `0.98` in-domain acc (`0.98` F1); **`0.94`** acc (`0.94` F1) on unseen Deepfake Database; **`0.92`** acc (`0.92` F1) on unseen 140k Real/Fake Faces.
- **Ablation study (Table 14):** Exp A (`94.00%`, loss `0.1607`) → Exp B (`92.00%`, loss `0.2265`, fake recall drops to `0.87`) → Exp C (`95.00%`, loss `0.1294`) → Exp D (`97.50%`, loss `0.0850`) → Full ARC-Net (**`99.00%`**, `+5.0%` over A, `+4.0%` over C, `+1.5%` over D, loss `0.0500`).
- **Quantitative XAI localization (Section 4.6, Table 15, `60` test images):** Mean IoU = **`0.8396`** (95% CI: `0.8071–0.8684`), Mean Dice = **`0.9121`** (95% CI: `0.8931–0.9284`), Peak-in-Mask = **`88.9%`**.

## Strengths
- **Synergistic residual + attention design** verified via controlled ablation (`+5.0%` over EfficientNetB0 baseline, `+4.0%` over residual-only, and `+1.5%` over DenseNet121+residual+attention).
- **Concrete subgroup fairness & calibration analysis** showing that `<1%` targeted regional real data (`400` images) cuts South Asian real-face FPR by `54.5%` (`22.0% → 10.0%`), improves Brier score (`0.180 → 0.110`), and achieves statistical significance (`p = 0.028`).
- **Bi-directional OOD cross-dataset testing** across three datasets, maintaining `92%–94.2%` accuracy under domain shift.
- **Quantitative + qualitative XAI validation** combining Grad-CAM, LIME, and expert VIA mask overlap (`0.8396` IoU, `0.9121` Dice, `88.9%` peak-in-mask).
- **Lightweight resource footprint** (`< 5 GB` VRAM on an RTX 4050) enabling practical reproducibility for training and inference.

## Weaknesses
- [GAP-ready: supported by P0039] **No diffusion-model face evaluation** — experiments rely on Kaggle deepfake/GAN benchmarks (`140k Real and Fake Faces`, `Deepfake Dataset`, `Deepfake Database`), leaving generalization to modern diffusion generators (e.g., Stable Diffusion, Midjourney, DALL-E 3) untested.
- [GAP-ready: supported by P0039] **Incomplete demographic fairness scope** — subgroup testing covers only `100` held-out **real** Bangladeshi faces (FPR only), without synthetic South Asian faces (FNR), intersectional breakdowns (age, gender, skin tone), or multi-region fairness evaluation.
- [GAP-ready: supported by P0039] **No post-processing or social media robustness evaluation** — robustness to JPEG compression levels, aggressive resizing, social media re-encoding, or adversarial attacks is not benchmarked beyond training-time Gaussian noise (`σ = 0.03`).
- [GAP-ready: supported by P0039] **No zero-learning dataset bias audit** — does not test whether non-semantic photometric shortcuts separate real vs. fake samples across the three Kaggle benchmarks (as demonstrated in P0016).
- [GAP-ready: supported by P0039] **Reproducibility & reporting gaps** — source code repository URL is not provided, the 500 Bangladeshi images are access-restricted, and minor specification discrepancies exist between text/tables/figures (e.g., `256` vs. `512` dense units; softmax spatial attention Eq. 2 vs. CBAM-like Eq. in Algorithm 1; `sparse_categorical_crossentropy` vs. `L_BCE`).
- [GAP-ready: supported by P0039] **Image-only binary classification** — does not address video temporal inconsistencies or multi-class generator attribution.

## Research Gap
- [GAP-ready: supported by P0039] Fairness-aware deepfake detection evaluated jointly across **both GAN and diffusion-model faces** and across **both FPR (real) and FNR (fake)** demographic subgroups remains unaddressed.
- [GAP-ready: supported by P0039] Standardizing **quantitative XAI localization metrics** (IoU/Dice/Peak-in-Mask) alongside calibration metrics (Brier score, ECE) across cross-generator benchmarks is still rare.
- [GAP-ready: supported by P0039] Evaluating whether minimal subgroup data inclusion (`<1%`) preserves fairness gains under heavy social-media compression and diffusion-era generators needs investigation.

## Future Work
- Extending ARC-Net to diffusion-generated faces and video-level temporal modeling (only image-level GAN/Kaggle benchmarks are tested here).
- Expanding demographic fairness evaluations to include synthetic South Asian faces and multi-group intersectional testing (age, gender, skin tone).
- Evaluating robustness under controlled compression, resizing, and social media transmission perturbations.
- Releasing reproducible training/inference code and standardized model checkpoints.

## Interesting Ideas
- Adding `<1%` underrepresented real facial images (`400` images in a `120k` train+val pool) can halve false positive rates (`22.0% → 10.0%`) and substantially improve probability calibration (`Brier 0.180 → 0.110`) for that demographic.
- Standalone attention hurt EfficientNetB0 (`94% → 92%`, fake recall `0.87`), whereas placing **residual blocks before the attention layer** created synergy (`99%`) — showing attention needs residual feature stabilization first.
- Quantifying Grad-CAM faithfulness via VIA human-annotated facial masks (`IoU`, `Dice`, `Peak-in-Mask`) provides an objective benchmark for XAI quality rather than relying on cherry-picked heatmaps.

## Possible Reuse
- **ARC-Net backbone for `MOD004` (Deep Learning Specialist):** EfficientNetB0 + residual stack + attention is lightweight (`< 5 GB` VRAM) and a strong candidate architecture for registration in `MOD004`.
- **Probability calibration & subgroup error auditing for `MOD009` (Confidence Estimator) and `MOD006` (Reliability Marker):** Brier score calibration and McNemar significance testing can be reused to benchmark confidence quality across demographic subgroups.
- **Quantitative Grad-CAM + LIME evaluation protocol for `MOD010` (Explainability Engine):** Directly informs `MOD010`'s heatmap assembly and planned `LIME` extension, while IoU/Dice/Peak-in-Mask scoring provides a testable faithfulness metric.
- **Controlled training-only Gaussian noise & geometric augmentation (`Table 2`):** Reusable in `04_Preprocessing` / training pipelines while keeping validation/test unaugmented.

## Questions
- How does ARC-Net perform when evaluated on modern diffusion face benchmarks such as **DiFF (P0023)**, **Synthbuster (P0003)**, or **AI-Face-FairnessBench (P0016)**?
- Does the `54.5%` FPR reduction on Bangladeshi real faces hold if the test set includes South Asian deepfakes generated by unseen GANs and diffusion models, or does it shift FNR?
- Which exact attention formulation (`Eq. 2` softmax spatial attention vs. `Algorithm 1` channel+spatial attention) and dense head width (`256` vs. `512`) produced the reported `99%` result?
- How sensitive is ARC-Net's `93.7%–94.2%` OOD accuracy to JPEG compression (`QF 50–90`) and social media resizing?

## Connections
- Directly complements **P0016** (Bias, Robustness, and Explainability on GAN vs. DM faces) — P0039 adds regional South Asian fairness, Brier calibration, McNemar testing, and quantitative Grad-CAM IoU/Dice, while lacking P0016's zero-learning bias audit and diffusion-model evaluation.
- Relates to **P0007** (Generalization across architectures and datasets; cited in P0039 as [38]) — P0039 provides bi-directional OOD evaluation on Kaggle face datasets, whereas P0007 evaluates FF++, CelebDF-V2, DFDC, and FakeAVCeleb with self-supervised ViTs (DINO/CLIP).
- Relates to **P0018** (Hierarchical GAN+DM detection; cited in P0039 as [32]) and **P0021** (Multiclass ViT detection; cited as [12]) — P0039 remains binary and pre-diffusion in its test datasets.
- Relates to **P0002** (CNN/DenseNet-121 comparison) — P0039 similarly benchmarks DenseNet-121 (`98%`), ResNet-50 (`92%`), InceptionV3 (`78%`), and MobileNetV2 (`68%`), showing ARC-Net (`99%`) outperforms them.
- Complements **P0040** (Explainable hierarchical ensemble) — both use EfficientNet + attention + Grad-CAM; P0039 adds residual–attention synergy, quantitative XAI localization, and demographic fairness, whereas P0040 adds weakly supervised attention crop/drop augmentation and DFT/DCT frequency forensics.
