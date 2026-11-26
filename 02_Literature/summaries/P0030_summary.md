# Paper Summary: P0030

## Metadata
- **Paper ID:** P0030
- **Title:** Towards reliable deepfake detection from uncertainty calibration perspective
- **Authors:** Xiaoxu Jin, Weinan Guan, Wei Wang, Jing Dong
- **Year:** 2025
- **Venue:** Visual Intelligence (Vol. 3, Article 28)
- **DOI:** 10.1007/s44267-025-00100-2

## Problem
Existing deepfake detectors are evaluated primarily on binary classification accuracy or AUC, while ignoring **model calibration** and **uncertainty estimation**. When confronted with unseen manipulation methods, compression degradation, or out-of-domain (OOD) datasets, single detectors become severely **overconfident**—assigning extreme probabilities near 0 or 1 to incorrect predictions—which compromises trustworthiness in high-stakes forensic, financial, and intelligence applications (Section 1, pp. 1–2; Fig. 1(a), p. 2).

## Motivation
Well-calibrated detectors align predicted probabilities with true empirical correctness frequencies and expose borderline/ambiguous cases (e.g., $0.4 < p < 0.6$) instead of making misplaced high-confidence claims (Sections 1 & 4.3, pp. 1–2, 5). While Deep Ensembles (DE) capture epistemic uncertainty via diverse member predictions, they multiply parameter count, FLOPs, and inference latency linearly with ensemble size. Adopting **Packed-Ensembles (PE)** (Laurent et al., 2023) embeds multiple diverse subnetworks within a single network via sparse grouped convolutions at negligible computational overhead, and injecting **Steganalysis-Rich Model (SRM)** high-frequency filters forces subnetworks to attend to subtle tampering artifacts rather than brittle semantic cues (Sections 2.2 & 3, pp. 3–4).

## Method
**PE-DD (Packed-Ensembles-based Framework for Deepfake Detection, Section 3, pp. 3–4, Figs. 2–4):**
1. **High-Frequency Detail Injection (SRM Filters):** Applies specially designed SRM convolutional kernels (Fridrich & Kodovský, 2012; Eq. 1, p. 3) capturing edge information, depth structure, and high-frequency texture details, concatenating the extracted residual maps as additional input channels alongside RGB channels (Figs. 2–3, pp. 3–4).
2. **Packed-Ensembles via Sparse Grouped Convolution:** Parameterized as `packed-ensembles-(M, α, γ)`, where $M$ is the number of subnetworks/estimators (default $M=4$), $\alpha$ is the width expansion multiplier, and $\gamma$ is the number of subgroups per subnetwork. Starting from an initial full convolution (Fig. 4, p. 4), subsequent layers use grouped convolutions with $\gamma$ groups—mathematically equivalent to multiplying layer weights by binary channel masks $mask_m^j$. Parameter count per layer is $M \times \left[\frac{\alpha C_j}{M}\frac{\alpha C_{j+1}}{M}s_j^2 \gamma^{-1}\right]$ (Section 3, p. 4).
3. **Ensemble Aggregation & Uncertainty:** Each subnetwork focuses on distinct tampering cues across channels; final predictive probability averages all $M$ estimators equally: $P(y|x,\mathcal{D}) = \frac{1}{M}\sum_{m=0}^{M-1} P(y|x,\theta_{\alpha,m})$ (Eq. 2, p. 4). An ablation comparing mean fusion vs. a learned MLP self-adaptive weighting module (Section 4.5, Table 7, p. 9) confirms that simple mean averaging generalizes better on unseen OOD data.
4. **Uncertainty Visualization:** Uses **Eigen-CAM** across individual estimators to inspect predictive disagreement and verify that PE concentrates attention more comprehensively on tampered facial regions than a single model (Section 4.6, Fig. 7, p. 9).

## Architecture
- **Backbones:** `ResNet-18` (R18) and `Wide ResNet28-10` (WR), adapted with ResNeXt-style sparse grouped convolutions for `PE-(M, α, γ)` preceded by SRM high-frequency filter concatenation (Sections 3 & 4.2, pp. 3–6).
- **Configurations reported (Table 1, p. 6):**
  - `FF++`: `PE-(4, 2, 1)` — R18 (11.21M params, 22.65G Multi-adds, 1271.4 Imgs/s) and WR (24.15M params, 223.68G Multi-adds, 937.4 Imgs/s).
  - `CDFv2`: `PE-(4, 2, 3)` for R18 (8.20M params, 20.20G Multi-adds, 1255.9 Imgs/s) and `PE-(4, 2, 2)` for WR (19.35M params, 131.05G Multi-adds, 1125.7 Imgs/s).

## Dataset
Evaluated across **7 public benchmarks** plus self-blended and self-collected sets (Section 4.1, pp. 4–5):
- **FaceForensics++ (FF++):** 1,000 raw videos (from 977 YouTube videos) across 4 manipulations (Deepfakes, Face2Face, FaceSwap, NeuralTextures); `c23` (mild) and `c40` (severe) compression levels used in Table 3.
- **Celeb-DeepFakeForensics v2 (CDFv2):** 590 real YouTube videos + 5,639 fake videos.
- **DFDC:** 124,000 videos, 8 facial modification algorithms.
- **DFDCP:** 5,000 preview videos, 2 facial modification algorithms.
- **WildDeepfake (WDF):** 7,314 face sequences from 707 internet videos.
- **GenImage:** >1 million real/AI-generated image pairs (Stable Diffusion, GLIDE, BigGAN, etc.).
- **PolyGlotFake (PGF):** Multimodal/multilingual deepfake videos across 7 languages and 10 manipulation methods.
- **Additional splits:** FF++ augmented with **Self-Blended Images (SBI)** (Shiohara & Yamasaki, 2022) for cross-method/cross-dataset evaluation (Tables 4–5, p. 7); and a **self-collected dataset** (26,000 Stable Diffusion entire-image fakes added to FF++ for training; 10,000 internet deepfakes for OOD testing) used in the fusion ablation (Section 4.5, Table 7, p. 9).
- **Availability:** Links to all 7 public datasets are provided (Data availability, p. 10); code and the 26k+10k self-collected sets are **Not reported** (no public repository URL).

## Training
- **Preprocessing:** Faces extracted per frame using `Dlib`, bounding boxes enlarged by 1.2× and cropped square; 8 frames sampled per video; resized to **128×128** for ensemble/shift studies (Tables 1–5) and **256×256** for SOTA comparisons (Table 6; 224×224 for Ojha et al. and DFD-FCG) (Section 4.1, pp. 5, 8).
- **Augmentations:** Random horizontal/vertical flip, RGB shift, and JPEG compression (Section 4.1, p. 5).
- **Optimization & Hardware:** Trained from scratch with **Adam** optimizer, **Cross-Entropy** loss, batch size **32**, on **NVIDIA A40 GPUs** (Section 4.1, p. 5). Learning rate and epoch count are **Not reported**.

## Evaluation
- **Metrics (Section 4.1, p. 5):** AUC (%), Expected Calibration Error (**ECE**, Eq. 3), Brier Score (**BS**, Eq. 4), False Positive Rate at 75% TPR (**FPR75**), Mutual Information (**MI**, measuring inter-member dependency/diversity), trainable parameters (M), Multi-adds (Giga MACs via Torchinfo), and inference throughput (Imgs/Sec).
- **Protocols:**
  1. In-domain detection, calibration, and compute efficiency on FF++ and CDFv2 vs. Single model and DeepEnsembles ($M=4$) (Section 4.2, Table 1, p. 6).
  2. Synthetic distribution shift (Gaussian noise, blur, affine rotation/shift across Severities 1–3; Section 4.3, Table 2 & Fig. 5, pp. 6–7) and video-level compression shift (`c23` -> `c40` on FF++ with 1,000× bootstrap 95% CIs; Table 3, p. 7).
  3. Cross-method (`FF++ SBI` -> DF, F2F, FS, NT; Table 4, p. 7) and cross-dataset (`FF++ SBI` -> CDFv2, DFDC, DFDCP; Table 5, p. 7).
  4. Unseen-dataset SOTA comparison (`FF++` -> CDFv2, WDF, GenImage, PGF against Xception, SRM, Ojha et al., Shuai et al., LAA-Net, D³, DFD-FCG; Table 6, p. 8).
  5. Hyperparameter ablations ($\alpha, \gamma$ in Fig. 6, p. 8; Mean vs. Self-adaptive MLP fusion in Table 7, p. 9) and Eigen-CAM uncertainty visualization (Fig. 7, p. 9).

## Results
- **In-Domain Performance & Efficiency (Table 1, p. 6):**
  - *FF++ (R18):* PE achieves **97.7% AUC**, **0.020 ECE**, **0.033 BS**, **0.082 MI** (11.21M params, 22.65G Multi-adds, 1271.4 Imgs/s), outperforming Single (94.7% AUC, 0.085 ECE, 0.086 BS, 11.19M params, 1304.8 Imgs/s) and DeepEnsembles (96.1% AUC, 0.022 ECE, 0.074 BS, 44.74M params, 80.74G Multi-adds, 957.8 Imgs/s).
  - *CDFv2 (R18):* PE achieves **98.8% AUC**, **0.005 ECE**, **0.018 BS**, **0.017 MI** using only **8.20M** params and **1255.9 Imgs/s** (fewer params than Single R18's 11.19M and ~1/5 of DE's 44.75M).
  - *WR Backbone:* On FF++, PE achieves **95.3% AUC**, **0.021 ECE**, **0.035 BS** (24.15M params vs. DE 145.91M); on CDFv2, **98.9% AUC**, **0.010 ECE**, **0.016 BS** (19.35M params vs. DE 145.91M).
- **Distribution Shift & Compression (Tables 2–3, pp. 6–7):**
  - *FF++ (shift) R18 (Table 2):* PE reaches **82.6% AUC**, **0.21 FPR75**, **0.18 ECE**, **0.16 BS** vs. Single (72.8%, 0.35, 0.31, 0.34) and DE (79.3%, 0.26, 0.25, 0.25).
  - *CDFv2 (shift) R18 (Table 2):* PE reaches **85.2% AUC**, **0.18 FPR75**, **0.15 ECE**, **0.21 BS** vs. Single (80.6%, 0.27, 0.20, 0.25). (With WR on CDFv2 shift, Single has 77.1% vs. PE 76.8% AUC, but PE achieves better FPR75 0.25, ECE 0.15, and BS 0.17.)
  - *Video-level compression c23 -> c40 on FF++ (Table 3, 1,000× bootstrap):* PE-R18 achieves 72.3±0.71% AUC, **0.22±0.003 BS**, **0.15±0.005 ECE** (vs. Single 0.28±0.005 ECE, DE 0.21±0.005 ECE); PE-WR achieves **73.6±0.69% AUC**, **0.23±0.003 BS**, **0.13±0.004 ECE** (vs. Single 0.31±0.005 ECE, DE 0.18±0.005 ECE).
- **Cross-Method & Cross-Dataset (Tables 4–5, p. 7):**
  - *Cross-method FF++ SBI (Table 4):* PE achieves the lowest BS on all 4 methods—DeepFakes **0.06** (94.8% AUC), Face2Face **0.16** (72.1% AUC), FaceSwap **0.11** (86.9% AUC), NeuralTextures **0.20** (64.7% AUC).
  - *Cross-dataset FF++ SBI -> OOD (Table 5):* PE achieves lowest BS across all 3 targets: CDFv2 **0.09** (75.6% AUC, 0.30 FPR75), DFDC **0.19** (69.5% AUC, 0.35 FPR75), DFDCP **0.11** (80.7% AUC, 0.32 FPR75).
- **Unseen-Dataset SOTA Comparison (Table 6, p. 8, trained on FF++):**
  - `PE-DD` achieves the **lowest Brier Score across all 4 unseen datasets**: CDFv2 **0.13** (70.4% AUC), WDF **0.21** (69.3% AUC), GenImage **0.24** (70.4% AUC), and PGF **0.20** (79.3% AUC). Even where specialized SOTA models obtain higher AUC (e.g., LAA-Net 73.7% on CDFv2 with BS 0.25; D³ 74.2% on WDF with BS 0.23; Ojha et al. 72.3% on GenImage with BS 0.42; DFD-FCG 80.9% on PGF with BS 0.23), `PE-DD` yields substantially better calibrated probabilities.
- **Ablations (Section 4.5, pp. 8–9):**
  - Increasing width $\alpha$ (1 -> 8) consistently improves both AUC and ECE, whereas increasing sparsity $\gamma$ (1 -> 8) leaves AUC and ECE nearly flat (Fig. 6, p. 8), indicating parameter redundancy.
  - Mean fusion vs. MLP self-adaptive weighting on OOD (Table 7, p. 9): comparable results (R18 Mean 71.4% AUC / 0.24 BS vs. Self-adapt 70.2% / 0.25; WR Mean 74.5% / 0.23 vs. Self-adapt 75.1% / 0.24), showing learned fusion weights fail to transfer to OOD samples.

## Strengths
- **Introduces uncertainty calibration to deepfake forensics** with rigorous calibration metrics (`ECE`, `BS`, `FPR75`, `MI`, 1,000× bootstrap 95% CIs) rather than relying solely on accuracy/AUC.
- **Zero/negligible computational overhead** via `PE-(M, α, γ)`, achieving superior calibration to DeepEnsembles with ~1/4–1/5 the parameters and much higher inference throughput (1,125–1,271 Imgs/s).
- **Comprehensive 7-dataset evaluation** spanning face-swapping, reenactment, in-the-wild videos (WDF), diffusion/GAN full-image synthesis (GenImage), and multilingual multimodal deepfakes (PGF).
- **Interpretable subnetwork disagreement** via Eigen-CAM maps (Fig. 7, p. 9), showing complementary regional focus across the 4 estimators.
- **Actionable ablation insights** demonstrating that equal mean fusion outperforms learned MLP fusion on OOD data and that high-frequency SRM injection boosts artifact sensitivity.

## Weaknesses
- [GAP-ready: supported by P0030] **Limited to CNN backbones** — `PE-DD` is only implemented on `ResNet-18` and `Wide ResNet28-10`; calibrating modern Vision Transformers or foundation-model detectors (e.g., CLIP-ViT, LAA-Net, DFD-FCG) remains unaddressed (Section 5, p. 9).
- [GAP-ready: supported by P0030] **AUC trade-off vs. top SOTA detectors** — on unseen-dataset benchmarks (Table 6, p. 8), `PE-DD` trails top specialized detectors in raw AUC (e.g., 70.4% vs. 73.7% LAA-Net on CDFv2; 69.3% vs. 74.2% D³ on WDF), and Table 6 omits ECE/FPR75 for SOTA baselines.
- [GAP-ready: supported by P0030] **Substantial calibration drop under severe shifts** — despite outperforming baselines, ECE still degrades roughly 6–10× under Gaussian/blur perturbations (0.020 -> 0.18 on FF++, Table 2) and severe compression (`c23` -> `c40` ECE 0.13–0.15, Table 3).
- [GAP-ready: supported by P0030] **No explicit OOD rejection or abstention mechanism** — calibrates binary real/fake probabilities but does not detect OOD samples or abstain when epistemic uncertainty exceeds a safety threshold.
- [GAP-ready: supported by P0030] **Missing code release and low-resolution default** — most experiments downsample crops to 128×128 (256×256 only in Table 6), and neither source code nor the 26k+10k self-collected datasets are publicly released.

## Research Gap
- [GAP-ready: supported by P0030] Extending Packed-Ensembles uncertainty calibration to Vision Transformer and CLIP-based SOTA detectors to achieve both peak cross-generator AUC and low ECE/BS.
- [GAP-ready: supported by P0030] Bridging probability calibration (P0030) with explicit OOD abstention/rejection (P0029) under severe compression and social-media degradation.
- [GAP-ready: supported by P0030] Generator-specific and manipulation-specific uncertainty calibration (e.g., GAN vs. Diffusion attribution confidence) rather than binary-only calibration (Section 5, pp. 9–10).

## Future Work
- Calibrating existing SOTA deepfake detectors via the Packed-Ensembles scheme to improve reliability without sacrificing peak detection AUC (Section 5, p. 9).
- Incorporating forgery-method and generation-mechanism characteristics into uncertainty estimation for more trustworthy detectors (Section 5, pp. 9–10).

## Interesting Ideas
- Measuring epistemic uncertainty through **inter-subnetwork Mutual Information (MI)** and **Eigen-CAM disagreement** inside a single packed backbone gives both scalar uncertainty and spatial localization at single-model inference speed.
- Flagging borderline probability predictions ($0.4 < p < 0.6$) as truly ambiguous (`Inconclusive`) directly addresses the high-confidence false-alarm problem in forensic deployment (Section 4.3, p. 5).
- Mean aggregation across diverse channels outperforms learned MLP fusion on OOD data because adaptive fusion weights overfit to ID feature correlations (Section 4.5, Table 7, p. 9).

## Possible Reuse
- **AI Forensic Analyst `MOD009` (Confidence Estimation):** Directly informs `MOD009`'s separation of raw detector probability from calibrated `prediction_confidence` and `decision_confidence`, providing `ECE`, `Brier Score`, `FPR75`, and inter-estimator disagreement (`MI` / variance) as candidate calibration/uncertainty signals.
- **AI Forensic Analyst `MOD008` (Decision Engine):** Supports `MOD008`'s `Inconclusive` decision tier for borderline calibrated probabilities ($0.4 < p < 0.6$) and `low_confidence` warnings when distribution shift elevates uncertainty.
- **AI Forensic Analyst `MOD003` & `MOD004` (Collectors & Deep Learning Specialist):** SRM high-frequency filter injection (`MOD003` texture/frequency features) and `PE-(M, α, γ)` sparse grouped backbones (`MOD004`) can provide multi-estimator outputs at single-model compute cost.
- **AI Forensic Analyst `MOD010` (Explainability):** Multi-estimator `Eigen-CAM` maps offer spatial uncertainty visualization alongside `grad_cam` / `saliency`.

## Questions
- Can Packed-Ensembles be applied to Vision Transformer / CLIP-ViT architectures (e.g., grouped linear projections/attention heads) without losing the cross-generator AUC advantage shown by Ojha et al. or `D³`?
- How does `PE-DD` perform on diffusion-specific face benchmarks such as DiFF (**P0023**) or Synthbuster (**P0003**) in terms of both AUC and ECE?
- Can combining `PE-DD`'s epistemic disagreement (`MI`) with post-hoc temperature scaling or `MOD009`'s empirical validation-set calibration further reduce `c23 -> c40` ECE below 0.15?

## Connections
- Directly complements **P0029** (OOD Abnormality detection): P0030 solves **confidence calibration** (`ECE`, `BS`, `FPR75`) under distribution shift, whereas P0029 solves **OOD sample flagging**; combining both maps cleanly to `MOD009` + `MOD008`.
- Extends **P0007** (cross-dataset generalization across CNNs, ViTs, DINO/CLIP) by showing that high AUC on unseen datasets (e.g., Ojha et al. CLIP-ViT on GenImage: 72.3% AUC) can still mask severe miscalibration (0.42 BS vs. `PE-DD`'s 0.24 BS).
- Relates to **P0016** (GAN vs. DM bias/robustness/Grad-CAM) and **P0023** (DiFF diffusion benchmark): `PE-DD` evaluates on GenImage and self-collected Stable Diffusion images, reinforcing cross-generator evaluation with calibration metrics.
- Relates to **P0013** (ensemble model for social media robustness) and **P0018** (hierarchical GAN+DM detection): `PE-DD` provides a parameter-efficient alternative to multi-model ensembles and highlights the need for calibration in multi-generator pipelines.
- Relates to **P0005** and **P0010** (high-frequency/DCT/convolutional traces): `PE-DD` injects SRM high-frequency kernels to force subnetworks to capture subtle manipulation residuals rather than semantic shortcuts.
