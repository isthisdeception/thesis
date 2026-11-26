# Paper Summary: P0033

## Metadata
- **Paper ID:** P0033
- **Title:** Dual Frequency Branch Framework With Reconstructed Sliding Windows Attention for AI-Generated Image Detection
- **Authors:** Jiazhen Yan, Ziqiang Li, Fan Wang, Ziwen He, Zhangjie Fu
- **Year:** 2026
- **Venue:** IEEE Transactions on Information Forensics and Security
- **DOI:** 10.1109/tifs.2026.3664000

## Problem
Existing AI-generated image detectors that extract fine-grained local features often fail to model the relative importance and complex interdependencies among internal elements within local regions, and typically operate in only a single frequency domain. As a result, they struggle to generalize across diverse generative paradigms (both GANs and diffusion models) and complex open-world benchmarks.

## Motivation
- Standard global self-attention (e.g., ViT, CLIP) weights broad semantic regions and is insufficiently sensitive to fine-grained, localized forgery traces.
- Single-domain frequency methods (FFT or DCT alone) lose spatial positional correspondence or miss multi-scale texture artifacts.
- Through a phase-swapping experiment on 1,000 real and 1,000 fake GenImage images (Sec. I, Fig. 1), the authors observe that detectors classify fake-phase/real-amplitude hybrids as fake more strongly than real-phase/fake-amplitude hybrids, indicating that the FFT phase spectrum encodes stronger generator-induced structural artifacts while amplitude primarily reflects color and brightness.
- Combining local spatial-frequency decomposition (DWT) with global structural dependencies (FFT phase) and localized window attention aims to capture richer, generator-agnostic forgery traces.

## Method
The proposed framework (DFFreq) integrates a dual frequency branch feature enrichment module with a Reconstructed Sliding Window Attention (`RSWAttention`) block and a ResNet-50 classifier (Sec. III, Figs. 2–3):
1. **DWT-based Window Tiling Branch (Sec. III-C, Fig. 3):** Decomposes the input image into four subbands $\{I_{LL}, I_{LH}, I_{HL}, I_{HH}\} \in \mathbb{R}^{C \times \frac{H}{2} \times \frac{W}{2}}$ via Discrete Wavelet Transform (DWT). Each channel is divided into $2 \times 2$ windows and tiled row-wise across all four frequency bands into $\hat{I}_{\text{DWT}} \in \mathbb{R}^{C \times 4 \times \frac{H \times W}{4}}$, followed by LayerNorm. This feeds into `RSWAttention` with window size $b = 4$ (so each $4 \times 4$ window couples 4 spatially adjacent locations with all 4 DWT subbands), and is reconstructed back to the spatial domain via Inverse DWT ($\hat{I}_{\text{IDWT}}$).
2. **FFT-based Phase Complement Branch (Sec. III-C):** Applies Fast Fourier Transform (FFT), isolates only the phase spectrum (keeping amplitude unmodified), processes phase features through `RSWAttention` with window size $b = 8$ to capture longer-range structural dependencies, and recombines the learned phase with the original amplitude via Inverse FFT ($\hat{I}_{\text{IFFT}}$).
3. **Dual-Branch Fusion & Classification (Sec. III-C–D):** Fuses both spatial reconstructions via $\hat{I}_{\text{output}} = (1 - \lambda)\hat{I}_{\text{IDWT}} + \lambda\hat{I}_{\text{IFFT}}$ ($\lambda = 0.4$, Eq. 5) and passes $\hat{I}_{\text{output}}$ into a ResNet-50 + linear classification head trained with binary cross-entropy loss (Eq. 6).

## Architecture
- **Preprocessing inside `RSWAttention` (Sec. III-B, Fig. 2):** `1x1` convolution (cross-channel mixing) followed by `3x3` depthwise separable convolution (local spatial features), producing $I_{\text{in}} \in \mathbb{R}^{C \times H \times W}$.
- **`LoAttention` (Local Attention Block):** Partitions features into $b \times b$ sliding windows ($Q_i, K_i, V_i \in \mathbb{R}^{C \times N}$, $N = b \times b$) and computes local scaled/unscaled dot-product attention $A_i = \text{SoftMax}(Q_i K_i^\top)V_i$ (Eq. 1).
- **`GMLP` (Global Window MLP Layer):** Reuses $V_i$ and applies $\hat{V}_i = \text{GELU}(\text{Linear}(V_i))$ (Eq. 2) to mix local frequency features and retain global context.
- **Window Restoration:** Combines $A_i$ and $\hat{V}_i$ via element-wise product ($\odot$), applies inverse window restoration, and applies a convolution layer (Eq. 3).
- **Backbone Classifier:** ResNet-50 + linear head (`BCELoss`).

## Dataset
- **Training set (Sec. IV-A):** ForenSynths [73] (ProGAN synthetic images + LSUN real images; 18,000 synthetic and 18,000 real images per category across 20 categories), trained under the 4-class protocol (`car`, `cat`, `chair`, `horse`) following [14].
- **Testing sets (5 benchmarks covering 65 distinct generative models listed in Footnote 1, p. 2):**
  - **GANGen-Detection [15]:** 9 GANs (BEGAN, SNGAN, CramerGAN, MMDGAN, RelGAN, STGAN, S3GAN, AttGAN, InfoMaxGAN), 4K images per model (balanced real/fake).
  - **DiffusionForensics [72] (DIRE dataset):** 8 diffusion models (DDPM, VQ-Diffusion, SDv1, ADM, SDv2, IDDPM, PNDM, LDM) with LSUN and ImageNet real images.
  - **UniversalFakeDetect [14]:** Guided, Glide (`50_27`, `100_10`, `100_27`), LDM (`100`, `200`, `200_cfg`), DALLE with LAION and ImageNet real images.
  - **AIGCDetectBenchmark / GenImage [79]:** 17 subsets in Table IV (ProGAN, GauGAN, StyleGAN2, BigGAN, StyleGAN, CycleGAN, StarGAN, Deepfake, WFIR, ADM, Glide, Midjourney, SDv1.4, SDv1.5, VQDM, Wukong, DALLE2).
  - **AIGIBench [80]:** Noise-to-image GANs (ProGAN, R3GAN, StyleGAN3, StyleGAN-XL, StyleSwim, WFIR), GAN face-swapping deepfakes (BlendFace, E4S, FaceSwap, InSwap, SimSwap), text-to-image diffusion (FLUX1-dev, Midjourney V6, GLIDE, DALLE-3, Imagen3, SD3, SDXL), personalized diffusion (BLIP, Infinite-ID, InstantID, IP-Adapter, PhotoMaker), and 2 social-media subsets (`SocialRF`, `CommunityAI`).
- **Availability:** Code is publicly available at `https://github.com/HorizonTEL/DFFreq-main`; evaluation uses publicly cited benchmarks.

## Training
- **Optimizer & Schedule (Sec. IV-B):** PyTorch on an NVIDIA RTX A6000 GPU; Adam optimizer, initial learning rate $2 \times 10^{-4}$ decayed by 20% every 10 epochs, batch size 128, 90 epochs, binary cross-entropy loss (`BCELoss`), fusion weight $\lambda = 0.4$.
- **Comparison Protocol (Sec. IV-C):** Compares against 13 baselines (CNN-Spot, Patchfor, F3Net, FrePGAN, GANDetection, LGrad, UnivFD, FreqNet, NPR, FatFormer, LaDeDa, C2P-CLIP, AIDE) trained under the same 4-class ProGAN paradigm (with official pretrained weights used for FatFormer and C2P-CLIP, and cited NPR results for Patchfor, F3Net, FrePGAN, GANDetection).

## Evaluation
- **Metrics:** Classification Accuracy (Acc. %) and Average Precision (A.P. %).
- **Cross-generator generalization:** Evaluated across all 5 benchmarks (Tables I–V).
- **Qualitative & feature analysis:** Phase-swapping test (Fig. 1), logit distribution comparison vs. NPR on ProGAN, R3GAN, BLIP, VQDM (Fig. 4), and spatial-residual visualizations of both branches (Fig. 5).
- **Ablation studies:** Module ablation (Table VI), `WAttention` vs. `RSWAttention` (Table IX), FFT phase-only vs. phase+amplitude (Table X), FFT vs. DCT complement branch (Table XI), DWT subband combinations (Table XII), window size configurations (Table XIII), and $\lambda$ sensitivity from 0.0 to 1.0 (Table XIV).
- **Perturbation robustness:** Evaluated on GenImage (Table VII) and AIGIBench (Table VIII) under JPEG compression ($\text{QF} = 95, 85, 75$) and Gaussian blur ($\sigma = 0.5, 1.0, 1.5$).

## Results
- **GANGen-Detection (Table I):** Mean Acc. **97.3%**, Mean A.P. **98.8%** (outperforms LaDeDa 97.2%/98.3% and C2P-CLIP 96.4%/99.9%, though behind FatFormer 98.9%/100.0%).
- **DiffusionForensics (Table II):** Mean Acc. **98.8%**, Mean A.P. **100.0%** (outperforms NPR 95.8%/99.4%, LaDeDa 95.1%/99.4%, AIDE 88.6%/95.9%, C2P-CLIP 80.7%/94.6%).
- **UniversalFakeDetect (Table III):** Mean Acc. **96.4%**, Mean A.P. **99.3%** (outperforms LaDeDa 94.2%/98.1%, NPR 93.9%/96.7%, C2P-CLIP 93.8%/99.2%).
- **GenImage / AIGCDetectBenchmark (Table IV):** Mean Acc. **90.6%**, Mean A.P. **93.6%** (outperforms C2P-CLIP 88.2%/92.6% and LaDeDa 86.6%/92.8%); achieves 93.5%–99.9% Acc. on most GAN/diffusion subsets, but drops on `Deepfake` (64.2% Acc. / 71.8% A.P.) and `WFIR` (52.2% Acc. / 46.8% A.P.).
- **AIGIBench (Table V):** Mean Acc. **77.9%**, Mean A.P. **82.0%** (outperforms AIDE 74.9%/76.2% and C2P-CLIP 71.0%/77.3%), representing +2.13% overall accuracy gain across the 5 benchmarks (and +5.8% / +7.0% over C2P-CLIP and AIDE in Sec. I, p. 2). Strong on modern text-to-image diffusion (`FLUX1-dev` 93.2%, `Imagen3` 93.6%, `SD3` 95.4%, `SDXL` 95.9%) and personalized diffusion (`BLIP` 99.2%, `InstantID` 94.6%), but weak on face-swapping (`BlendFace` 44.1%, `E4S` 45.1%, `FaceSwap` 50.8%, `InSwap` 52.1%, `SimSwap` 48.4%), `DALLE-3` (46.2%), `WFIR` (52.2%), `SocialRF` (60.8%), and `CommunityAI` (54.6%).
- **Perturbation Robustness (Tables VII–VIII):** Best overall robustness among compared methods: on GenImage, 78.8% / 76.6% / 75.2% (JPEG QF=95/85/75) and 92.0% / 88.4% / 87.9% (Gaussian blur $\sigma=0.5/1.0/1.5$); on AIGIBench, 68.9% / 67.2% / 65.2% (JPEG) and 75.5% / 74.6% / 74.2% (blur).
- **Key Ablations (Tables VI, IX–XIV):** Full model reaches 92.1% mean Acc. / 94.1% mean A.P. across 5 datasets (Table XIV lists 94.7% mean A.P. at $\lambda = 0.4$). `RSWAttention` beats `WAttention` by +24.2% mean Acc. (92.1% vs. 67.9%, Table IX); phase-only FFT beats phase+amplitude by +5.2% (92.1% vs. 86.9%, Table X); FFT beats DCT complement by +1.6% (92.1% vs. 90.5%, Table XI); FFT alone without DWT collapses to 49.0% / 49.0% (Table VI).

## Strengths
- **Extensive cross-generator validation:** Trained solely on 4-class ProGAN and evaluated across 5 large-scale benchmarks covering 65 generative models (GANs, diffusion, personalized generation, and social media subsets).
- **Principled dual-frequency synergy:** Empirically validates (via phase-swapping, branch visualization, and ablations) why combining local DWT spatial-frequency window tiling with global FFT phase dependencies outperforms single-domain frequency detectors.
- **High perturbation resilience:** Maintains top accuracy under Gaussian blur and outperforms baselines under JPEG compression across both GenImage and AIGIBench.
- **Reproducible implementation:** Official code is publicly released with thorough hyperparameter and architectural ablations.

## Weaknesses
- [GAP-ready: supported by P0033] **Severe failure on face-swapping and social-media deepfakes:** Accuracy drops below ~52% on AIGIBench face-swapping subsets (`BlendFace` 44.1%, `E4S` 45.1%, `FaceSwap` 50.8%, `InSwap` 52.1%, `SimSwap` 48.4%), 64.2% on GenImage `Deepfake`, and 54.6%–60.8% on social-platform subsets (`CommunityAI`, `SocialRF`) (Tables IV–V, Sec. IV-C).
- [GAP-ready: supported by P0033] **Lack of face-specific forensic modeling:** Trained on general ForenSynths object categories (`car`, `cat`, `chair`, `horse`) rather than facial structures, leaving face-manipulation and boundary-blending traces unexploited.
- [GAP-ready: supported by P0033] **Black-box binary prediction without XAI or attribution:** Outputs only a binary real/fake logit without pixel-level artifact localization, source-generator attribution, or human-interpretable forensic rationales beyond post-hoc branch visualizations (Fig. 5).
- [GAP-ready: supported by P0033] **Compression vulnerability remains substantial:** Despite beating baselines, accuracy still drops sharply under JPEG compression (e.g., GenImage drops from 90.6% clean to 75.2% at QF=75; AIGIBench drops from 77.9% to 65.2% at QF=75, Tables VII–VIII).
- [GAP-ready: supported by P0033] **Lower accuracy on certain GAN and newer commercial models:** Trails FatFormer on GANGen-Detection (97.3% vs. 98.9%, Table I) and performs near chance on `WFIR` (52.2%) and `DALLE-3` (46.2%) in AIGIBench (Table V).

## Research Gap
- [GAP-ready: supported by P0033] Bridging general frequency-domain synthetic image detectors to face-swapping and social-media deepfakes where semantic blending and re-encoding suppress low-level generator traces.
- [GAP-ready: supported by P0033] Integrating dual-frequency (DWT + FFT phase) evidence into interpretable, calibrated forensic pipelines capable of source attribution and human-readable explanations rather than uncalibrated binary logits.
- [GAP-ready: supported by P0033] Mitigating performance drops on post-processed/compressed social-media images and unseen proprietary generators (e.g., DALLE-3).

## Future Work
- Improving detection accuracy on unknown social-media generated images (`SocialRF`, `CommunityAI`) and face-swapping deepfakes (explicitly highlighted in Sec. IV-C, p. 7).
- Investigating why CLIP-based detectors underperform on DiffusionForensics while excelling on GANGen-Detection, and closing the remaining GAN accuracy gap relative to FatFormer (Sec. IV-C, p. 6).

## Interesting Ideas
- **FFT phase-only branch + unmodified amplitude recombination:** Keeping amplitude untouched prevents color/brightness nuisance variations from confounding the detector while isolating structural phase artifacts.
- **`2x2` DWT window tiling across 4 subbands:** Structuring `4x4` attention windows so each window simultaneously spans 4 adjacent spatial positions and all 4 wavelet subbands (`LL, LH, HL, HH`) forces attention to model fine-grained spatial-frequency coupling.
- **Explicit complementarity warning:** FFT phase alone fails (<50% Acc.) with local window attention, proving global phase representations require multi-scale spatial-frequency grounding (`DWT` + `Window Tiling`) to be effective.

## Possible Reuse
- **Frequency-domain collector enhancement (`MOD003` / `MOD018`):** The DWT 4-subband + FFT phase decomposition pattern can enrich `frequency_domain.py` in `11_AI_Forensic_System` as a dual-frequency forensic signal or specialist detector (`MOD004`), complementing the classical FFT spectral peak approach of **P0003** and DCT beta statistics of **P0010**.
- **Explainability artifacts (`MOD010`):** Reconstructed DWT edge-residual and FFT phase-residual maps (Fig. 5) could serve as visual `explainability_input` artifacts alongside Grad-CAM (**P0016**) in `11_AI_Forensic_System`.
- **Benchmarking protocol:** Using `AIGIBench` and `GenImage` subsets (especially `SocialRF`, `CommunityAI`, and face-swapping subsets) provides stress tests for our forensic analyst's failure handling (`MOD016`) and confidence calibration (`MOD009`).

## Questions
- How does `DFFreq` perform when trained directly on face datasets (e.g., FaceForensics++, CelebA-HQ, or DiFF from **P0023**) rather than 4-class ForenSynths?
- Why does `DALLE-3` accuracy drop to 46.2% on AIGIBench while `Imagen3`, `SD3`, and `SDXL` exceed 93%?
- Can the reconstructed DWT/FFT-phase spatial residual maps be quantitatively calibrated into reliability scores for evidence fusion (`MOD006`, `MOD007`)?

## Connections
- Directly advances frequency-domain detection from **P0003** (FFT spectral peaks for diffusion models) and **P0010** (DCT anomalies for GANs) by unifying DWT subbands and FFT phase into an end-to-end trainable attention framework tested on both GANs and diffusion models.
- Contrasts with **P0034** (LASTED), which improves cross-generator generalization via vision-language contrastive training in the spatial/semantic embedding space rather than dual-frequency local window attention.
- Complements **P0018** (hierarchical ResNet-101 GAN+DM detection and source attribution) and **P0023** (DiFF facial diffusion benchmark) by exposing the exact failure mode of general-image frequency detectors on face-swapping (`BlendFace`, `FaceSwap`, `SimSwap`) and social-media images.
- Relates to **P0015** (GLFNet) and **P0016** (bias/robustness/Grad-CAM audit) on balancing local vs. global cues and evaluating perturbation robustness.
