# Paper Summary: P0041

## Metadata
- **Paper ID:** P0041
- **Title:** Constructing New Backbone Networks via Space-Frequency Interactive Convolution for Deepfake Detection
- **Authors:** Zhiqing Guo, Zhenhong Jia, Liejun Wang, Dewang Wang, Gaobo Yang, Nikola Kasabov
- **Year:** 2024
- **Venue:** IEEE Transactions on Information Forensics and Security (accepted 2023; published 2024, DOI: 10.1109/tifs.2023.3324739)
- **DOI:** 10.1109/tifs.2023.3324739

## Problem
Existing deep learning Deepfake detectors rely on standard CNN backbones (e.g., ResNet, VGGNet, MobileNet) originally designed to learn salient semantic image content (identity, hair color, eyes) rather than subtle tampering traces. Prior works compensate using three auxiliary paradigms—pre-processing mechanisms, attention mechanisms, or stacked/embedded modules—which can destroy subtle traces during domain transformation or over-focus on local artifacts while ignoring global cues. There is a need to redesign the internal convolution operation itself so backbone networks natively capture both spatial-domain and high-frequency manipulation traces.

## Motivation
Manipulation traces in Deepfake images typically appear as isolated dots or linear textures involving sharp gray-scale transitions (high-frequency information), whereas spatial-domain features retain complete forgery context. Because spatial and frequency representations are complementary, embedding both inside the convolution layer via interactive fusion avoids the trace loss of standalone pre-processing and the narrow local focus of spatial attention, while enabling a drop-in replacement for vanilla convolutions without altering network topology or increasing parameter count.

## Method
The authors propose **Space-Frequency Interactive Convolution (SFIConv)** as a new detection paradigm (Paradigm 4 in Fig. 1) to replace vanilla convolutions in the "Body" of standard backbones (leaving the first "Head" layer and final FC "Tail" layer intact; Section III-A, Fig. 2):
1. **Multichannel Constrained Separable Convolution (MCSConv)** (Section III-B, Fig. 3, Eq. 1): Generalizes Bayar and Stamm's ConstrainedConv [33] from fixed single-channel input pre-processing to $c_{in}$ feature maps. Applies $c_{in}$ depthwise constrained kernels $W_c$ satisfying $W_c(0,0) = -1$ and $\sum_{(x,y)\neq(0,0)} W_c(x,y) = 1$ to extract $c_{in}$ depthwise high-frequency trace maps, followed by a vanilla convolution $f(\cdot)$ whose kernel size matches the replaced layer (e.g., $1\times 1, 3\times 3, 5\times 5$) for cross-channel aggregation.
2. **SFIConv-Stage1 (Space-Frequency Generation)** (Section III-C, Fig. 4): Replaces the second layer of the backbone (requiring an even multi-channel input $T_{in} \in \mathbb{R}^{c_{in}\times h\times w}$ produced by the Head). Splits channels using ratio $\alpha \in [0, 1]$ into spatial features $T_{spa} \in \mathbb{R}^{(1-\alpha)c_{out}\times h\times w}$ (via vanilla convolution) and high-frequency features $T_{fre} \in \mathbb{R}^{\alpha c_{out}\times h\times w}$ (via MCSConv).
3. **SFIConv-Stage2 (Space-Frequency Interaction)** (Section III-C, Eq. 2–5, Table I): Dual-input, dual-output convolution replacing intermediate Body layers. Computes intra-branch updates ($T_{S\to S} = f_{S\to S}(T_{spa})$, $T_{F\to F} = f_{F\to F}(T_{fre})$) and cross-branch interactions ($T_{S\to F} = f_{S\to F}(T_{spa})$, $T_{F\to S} = f_{F\to S}(T_{fre})$), fused via element-wise summation: $T'_{spa} = T_{S\to S} + T_{F\to S}$ and $T'_{fre} = T_{F\to F} + T_{S\to F}$.
4. **SFIConv-Stage3 (Space-Frequency Fusion)** (Section III-C, Eq. 6–7): Replaces the last convolution of the Body, mapping both branches to $c_{out}$ channels and summing them into $T_{fusion} = f'_{S\to S}(T'_{spa}) + f'_{F\to S}(T'_{fre}) \in \mathbb{R}^{c_{out}\times h\times w}$ for the FC Tail.
5. **Flexible Spatial Compression ($\beta \in [0, 1]$)** (Section III-C, Eq. 8): Optional nearest-neighbor interpolation $I(T, \beta)$ downsamples $T_{fre}$ at Stage 1, scales interaction maps $D_{S\to F} = I(T_{S\to F}, \beta)$ and $D_{F\to S} = I(T_{F\to S}, 1/\beta)$ in Stage 2, and upsamples back at Stage 3 to reduce FLOPs.

## Architecture
- **Drop-in Backbone Replacement:** Validated across seven CNN backbones—**MobileNet, ResNet26, ResNet50, ResNet101, VGGNet13, VGGNet16, and VGGNet19**—producing `SFIC-*` variants (Table III).
- **Parameter & FLOP Footprint:** Retains exact parameter counts of the base backbones (e.g., SFIC-ResNet26 = 13.95M params, 3.09 GMac at $\beta=1.00$ vs 3.08 GMac baseline; SFIC-VGGNet13 = 9.41M params, 14.66 GMac vs 14.68 GMac baseline), while $\beta < 1$ reduces FLOPs down to 1.24 GMac ($\alpha=0.75, \beta=0.25$ on ResNet26; Table II).
- **Code:** Publicly released at `https://github.com/EricGzq/SFIConv` (Abstract).

## Dataset
Four open Deepfake face datasets (Section IV-A1), with face crops extracted without background via `face_recognition` and resized to $256 \times 256$:
- **HFF [31]:** 155,000 face images covering 4 generative models (PGGAN, StyleGAN, Glow, StarGAN) + 1 graphics method (Face2Face) and 3 real-face resolutions (train:test = 4:1).
- **FaceForensics++ (FF++) [35]:** 1,363 real and 4,000 fake videos (FaceSwap, DeepFake, Face2Face, NeuralTextures) at H.264 HQ and LQ levels; 120,000 frames sampled (60k real, 60k fake; $N_{iter}=2$, $N_{frames}=50$ real / $16$ fake; train:test = 5:1).
- **DFDC [36]:** 2,891 real and 20,210 fake videos sampled; 120,000 frames selected (60k real, 60k fake; train:test = 5:1).
- **CelebDF [37]:** 890 real and 5,639 fake videos; 120,000 frames sampled (60k real, 60k fake) for cross-dataset evaluation.

## Training
- **Framework & Optimizer:** PyTorch; Adam ($\gamma_1 = 0.9, \gamma_2 = 0.999$), initial learning rate $L_r = 10^{-4}$ decayed by $0.5\times$ per epoch, trained for 20 epochs with batch size 64 and fixed random seed 7 (Section IV-A3).
- **Augmentation & Protocol:** Horizontal flip, rotation, and normalization; models are trained from scratch in intra-dataset comparisons (Section IV-E).

## Evaluation
- **Metrics:** AUC and Balanced Accuracy (BACC, threshold 0.5), alongside parameter count and FLOPs (GMac/M) (Section IV-A2).
- **Experimental Suites:**
  1. Hyper-parameter ablation on $\alpha \in \{0.25, 0.50, 0.75\}$ and $\beta \in \{0.25, 0.50, 0.75, 1.00\}$ using SFIC-ResNet26 on FF++ HQ/LQ (Section IV-B, Table II).
  2. Multi-backbone comparison across 7 CNN architectures on FF++ HQ/LQ (Section IV-C, Table III).
  3. Unseen manipulation leave-one-out generalization on 100k FF++ HQ training faces (`TEST-DF`, `TEST-FF`, `TEST-FS`, `TEST-NT`) vs 6 baselines (Section IV-D, Table IV).
  4. Intra-dataset comparison on DFDC, HFF, FF++ HQ, and FF++ LQ vs 6 open-source baselines: Meso-Incep, Multi-task, XceptionNet, $F^3$-Net, AMTENnet, M2TR (Section IV-E, Table V).
  5. Cross-dataset evaluation across DFDC / FF++ HQ / FF++ LQ (Section IV-F1, Table VI) and FF++ HQ $\to$ CelebDF vs 13 SOTA baselines (Section IV-F2, Tables VII–IX).
  6. Visual interpretability via Average Forgery Attention Maps (AFAMs) across 4, 8, and 16 FF++ fake faces (Section IV-G, Fig. 5).

## Results
- **Ablation (Table II):** On FF++ HQ/LQ, SFIC-ResNet26 ($\alpha=0.25, \beta=1.00$) improves ResNet26 from **87.66% / 88.81% AUC** (81.33% / 81.79% BACC) to **96.38% / 96.47% AUC** (89.57% / 89.96% BACC). With $\alpha=0.25, \beta=0.75$, FLOPs drop from 3.08 to 2.80 GMac while still reaching 90.88% / 90.92% AUC. At $\alpha=0.75, \beta=0.50$, FLOPs drop to 1.61 GMac (reported as 91.30% GMac relative reduction in text) while matching LQ AUC (88.99% vs 88.81%).
- **Backbone Upgrades (Table III, $\alpha=0.5, \beta=1.0$):** All 7 backbones improve substantially on FF++ HQ/LQ—e.g., MobileNet (71.80% $\to$ 78.28% HQ AUC), ResNet50 (84.05% $\to$ 92.11%), ResNet101 (79.80% $\to$ 85.33%), VGGNet13 (94.59% $\to$ 98.46%), VGGNet16 (94.08% $\to$ 97.36%), VGGNet19 (94.25% $\to$ 97.41%).
- **Intra-Dataset SOTA (Table V):** SFIC-ResNet26 ($\alpha=0.25, \beta=1.00$, 13.95M params, 3.09 GMac) achieves best results on **DFDC (97.44% AUC / 91.24% BACC)** and **FF++ LQ (96.47% AUC / 89.96% BACC)**, outperforming XceptionNet (92.02% LQ AUC) and M2TR (92.10% LQ AUC) with roughly half the parameters and FLOPs. SFIC-VGGNet13 ($\alpha=0.50, \beta=1.00$) leads **HFF (99.99% AUC / 99.47% BACC)** and **FF++ HQ (98.46% AUC / 93.61% BACC)**.
- **Unseen Manipulations (Table IV):** SFIC-VGGNet13 leads `TEST-DF` (**86.97% AUC / 77.09% BACC** at $\alpha=0.25, \beta=0.75$), `TEST-FF` (**78.30% AUC** at $\alpha=0.50, \beta=1.00$, **66.54% BACC** at $\alpha=0.75, \beta=0.75$), and `TEST-NT` AUC (**68.93%**, though Meso-Incep leads BACC at 61.44%). SFIC-ResNet26 leads `TEST-FS` (**60.49% AUC / 56.19% BACC**).
- **Cross-Dataset (Tables VI–IX):** Strong cross-compression transfer on FF++ (HQ $\to$ LQ **87.74% AUC**, LQ $\to$ HQ **90.71% AUC** vs XceptionNet 79.15% / 85.02%). On FF++ HQ $\to$ CelebDF, SFIConv boosts all 6 ResNet/VGG models (e.g., ResNet26: 67.29% $\to$ 70.68%; VGGNet16: 63.59% $\to$ 70.95%), though still trailing specialized domain-generalization methods like DCL (81.0%) and Luo et al. (79.4%) in Table IX.
- **AFAM Visualization (Fig. 5):** SFIC-ResNet26/50/101 attend broadly across global facial forgery clues rather than collapsing onto narrow local patches like vanilla ResNets.

## Strengths
- **Architecture-agnostic drop-in design:** Replaces vanilla convolutions cleanly without changing topology, pooling, or parameter count, and includes an explicit FLOP-accuracy trade-off knob ($\beta$).
- **Balanced space-frequency modeling:** Jointly learns and interacts spatial-domain features and adaptive multi-channel high-frequency residuals (MCSConv), avoiding information loss from standalone pre-processing.
- **Strong low-quality compression resilience:** SFIC-ResNet26 maintains virtually identical AUC on FF++ HQ (96.38%) and FF++ LQ (96.47%) and excels at HQ $\leftrightarrow$ LQ cross-compression transfer.
- **Reproducible and thorough:** Public GitHub code, 4 public benchmarks, 7 backbone families, and 13+ baseline comparisons.

## Weaknesses
- [GAP-ready: supported by P0041] **No diffusion-model evaluation:** Tested strictly on GANs (HFF) and face-swapping/reenactment videos (FF++, DFDC, CelebDF); generalization to diffusion-generated faces (Stable Diffusion, DALL-E, Midjourney) is completely untested.
- [GAP-ready: supported by P0041] **Modest true cross-dataset generalization:** DFDC $\leftrightarrow$ FF++ cross-dataset AUCs remain low (57.58%–65.63%, Table VI), and FF++ $\to$ CelebDF AUC (70.7%–71.0%, Table IX) lags domain-generalization baselines such as DCL (81.0%) and Luo et al. (79.4%).
- [GAP-ready: supported by P0041] **Weak unseen transfer on FaceSwap and NeuralTextures:** In leave-one-out evaluation (Table IV), `TEST-FS` AUC reaches at most 60.49% and `TEST-NT` BACC reaches at most 53.85%.
- [GAP-ready: supported by P0041] **CNN-only scope without modern ViT/hybrid backbones:** Only evaluates MobileNet, ResNet, and VGG; does not investigate how MCSConv/SFIConv interacts with Vision Transformers or ConvNeXt-style depthwise architectures.
- [GAP-ready: supported by P0041] **Limited degradation and localization scope:** Evaluates only H.264 HQ/LQ compression rather than controlled JPEG quality sweeps, Gaussian noise/blur, social-media re-encoding, or pixel-level forgery localization.

## Research Gap
- [GAP-ready: supported by P0041] Space-frequency interactive convolution backbones have not been evaluated or adapted for unified **GAN + Diffusion Model** synthetic face detection.
- [GAP-ready: supported by P0041] Combining SFIConv's intrinsic space-frequency convolutional inductive bias with self-supervised pre-training (e.g., CLIP/DINO, cf. P0007) or contrastive domain generalization (e.g., DCL) to close the CelebDF/DFDC cross-dataset gap remains unexplored.
- [GAP-ready: supported by P0041] Extending space-frequency interactive blocks to pixel-level forgery localization (cf. P0042) and testing robustness against social-media post-processing pipelines remain open.

## Future Work
- Combining SFIConv with dedicated cross-domain generalization mechanisms (acknowledged in Section IV-F2) to close the gap with methods like DCL on CelebDF and DFDC.
- Extending space-frequency interactive convolutions beyond CNNs to transformer/hybrid architectures and diffusion-era benchmarks.
- Evaluating robustness under controlled post-processing perturbations (JPEG compression, resizing, noise, blur).

## Interesting Ideas
- Replacing Bayar & Stamm's single-channel constrained pre-processing filter with **MCSConv** inside the network body (starting at Layer 2 where channels are rich and even-numbered) solves the classic trade-off where early high-pass filtering discards spatial semantics.
- Using **AFAMs** (averaged attention maps over 4/8/16 images) instead of single-image Grad-CAM reduces per-image noise when diagnosing whether a detector relies on local shortcuts vs global forensic cues.

## Possible Reuse
- **MOD004 (Deep Learning Specialist):** `SFIC-ResNet26` or `SFIC-VGGNet13` can serve as a lightweight, compression-resilient registered detector model (`model_id`) behind the `EvidenceCollector` interface, especially for low-quality video frames.
- **MOD003 (Evidence Acquisition Layer) / MOD010 (Explainability Engine):** MCSConv's learned constrained depthwise trace maps and SFIConv's spatial vs frequency branch activations/AFAMs can supply structured `explainability_input` payloads (`attention_maps` / `saliency`).
- **MOD007 (Evidence Fusion Engine):** Demonstrates empirically that interactive mid-network fusion between spatial and high-frequency features outperforms input-level frequency pre-processing alone.

## Questions
- How does SFIConv perform when trained from ImageNet or self-supervised weights rather than from scratch, given that Stage 1–3 alter vanilla channel routing?
- Do MCSConv's constrained kernels ($W_c(0,0)=-1$) capture diffusion-model periodic denoising residuals (as analyzed in P0003) as effectively as GAN/face-swap artifacts?
- Why does SFIC-ResNet26 degrade much less from FF++ HQ to LQ than SFIC-VGGNet13 (Table V)?

## Connections
- Directly contrasts with input-level frequency/trace pre-processing in **P0003** (non-DL spectral peaks), **P0005** (EM convolutional traces), and **P0010** (DCT beta statistics) by embedding constrained high-frequency extraction inside every Body convolution layer.
- Complements **P0007** (generalization across architectures and self-supervised DINO/CLIP) and **P0016** (GAN vs DM bias, robustness, explainability) by showing that architectural inductive bias helps compression resilience but still struggles on cross-dataset DFDC/CelebDF transfer.
- Complements **P0042** (FakeLocator): P0041 focuses on global space-frequency classification backbones, whereas P0042 targets full-resolution pixel-level manipulation localization.
- Relates to **P0015** (GLFNet dual-branch fusion) and **P0018** (hierarchical GAN+DM classification) as candidate architectures/features for **MOD004** and **MOD007**.
