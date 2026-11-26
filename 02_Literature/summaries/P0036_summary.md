# Paper Summary: P0036

## Metadata
- **Paper ID:** P0036
- **Title:** PORI-Gate: Reliability-Guided Operator-Response Fusion for Generalizable AI-Generated Image Detection
- **Authors:** Hongxu Shen, Jin Tian
- **Year:** 2026
- **Venue:** IEEE Access
- **DOI:** 10.1109/access.2026.3747330

## Problem
Detectors trained on one generative model family or dataset often fail to generalize to unseen GANs, diffusion models, or shifted real-image sources due to generator-specific artifacts, dataset shortcuts, source bias, and semantic bias. While low-level forensic cues reduce reliance on high-level RGB semantics, no individual low-level cue remains uniformly reliable across generators, image content, or post-processing conditions (Sec. I, Fig. 1(a)-(b)). Naive concatenation or globally fixed fusion cannot dynamically reallocate importance across complementary cues on a per-image basis.

## Motivation
Development-set diagnostics (Fig. 1(a)-(b)) reveal that three matched single-operator detectors—ColorQuant, LowBit, and JPEGProbe—respond very differently to resizing ($\times 0.5$), Gaussian blur ($\sigma=1$), and gamma adjustment ($0.8$). Although 85.7% of pooled single-operator errors are false positives on real image-condition pairs, their error sets only partially overlap: JPEGProbe rescues **94.2%** of ColorQuant's real-image errors, while LowBit rescues **83.8%** of JPEGProbe's real-image errors. This complementarity motivates a lightweight, RGB-semantic-decoupled detector that extracts deterministic low-level operator responses and fuses them via an **input-dependent Reliability-Guided Fusion Gate** combining sample-specific allocation logits with a learnable global operator bias—avoiding both large pretrained backbones (CLIP) and costly generative reconstruction models (DIRE/LaRE2).

## Method
**PORI-Gate** (Sec. III, Fig. 2, Algorithm 1) operates in five stages:
1. **Deterministic Operator Response Extraction (Sec. III-C, Algorithm 1):** Given a preprocessed $256 \times 256$ uint8 RGB image $\mathbf{x}^u$, three float32 responses are stacked as $\mathbf{R} = [\mathbf{r}_{cq}, \mathbf{r}_{lb}, \mathbf{r}_{jpg}] \in \mathbb{R}^{3 \times 3 \times 256 \times 256}$:
   - **O1 ColorQuant ($\mathbf{r}_{cq}$):** Projects float32 RGB pixels into a fixed 3-channel luminance–chrominance space via matrix $M$ (Eqs. 3–4, no chroma offset), performs unit-step integer rounding (ties-to-even), reconstructs to RGB via $M^{-T}$ clipped to $[0,255]$, and computes the signed clipped normalized residual $\mathbf{r}_{cq} = \text{clip}((\mathbf{x}^f - \hat{\mathbf{x}}_{cq})/s_c, -1, 1)$ with default $s_c = 8.0$ (Eqs. 5–7).
   - **O2 LowBit ($\mathbf{r}_{lb}$):** Extracts the lowest $n=3$ least significant bits per 8-bit RGB channel via bitwise AND with $m = 2^3 - 1 = 7$ and normalizes to $[0,1]$: $\mathbf{r}_{lb} = \text{float32}(\text{bitand}(\mathbf{x}^u, 7))/7$ (Eq. 8).
   - **O3 JPEGProbe ($\mathbf{r}_{jpg}$):** Recompresses the image in memory with Pillow JPEG at quality $q=75$ (stripping Exif/file metadata), decodes back to RGB, and computes the signed clipped residual $\mathbf{r}_{jpg} = \text{clip}((\mathbf{x}^f - \hat{\mathbf{x}}^f_{jpg})/s_j, -1, 1)$ with default $s_j = 25.0$ (Eqs. 9–10).
2. **Shared Encoding & Identity Embeddings (Sec. III-D):** A shared ResNet18 encoder $E(\cdot)$ (no ImageNet pretraining) maps each response independently to a 256-D feature token $\mathbf{f}_{i,k} = E(\mathbf{r}_{i,k})$, to which a learnable operator identity embedding $\mathbf{e}_k$ is added: $\mathbf{t}_{i,k} = \mathbf{f}_{i,k} + \mathbf{e}_k$ (Eqs. 12–13).
3. **Reliability-Guided Fusion Gate (Sec. III-D):**
   - Computes the cross-operator mean token $\bar{\mathbf{t}}_i = \frac{1}{3}\sum_{k=1}^3 \mathbf{t}_{i,k}$ (Eq. 14).
   - A shared gate MLP $G([\mathbf{t}_{i,k}, \bar{\mathbf{t}}_i])$ predicts scalar allocation logit $s_{i,k}$ (Eq. 15).
   - Combines $\mathbf{s}_i$ with a learnable global operator bias $\mathbf{b}$ (initialized as $\mathbf{b}_0 = [0.7, -0.1, -0.1]$) via temperature-scaled softmax ($\tau = 1.3$, Eq. 16) and gate-floor normalization $\mathcal{N}_\epsilon$ ($\epsilon = 0.003$, Eqs. 17–18) to produce $\boldsymbol{\alpha}_i = [\alpha_{i,1}, \alpha_{i,2}, \alpha_{i,3}]$, yielding $\mathbf{f}^{\text{gate}}_i = \sum_{k=1}^3 \alpha_{i,k} \mathbf{t}_{i,k}$ (Eq. 19).
4. **Context Descriptor & Binary Classification (Sec. III-E):** Concatenates $[\text{mean}_k(\mathbf{t}_{i,k}), \max_k(\mathbf{t}_{i,k}), \text{std}_k(\mathbf{t}_{i,k})]$ (768-D) into a context head $H$ producing 256-D $\mathbf{c}_i$ (Eq. 20), then concatenates $[\mathbf{f}^{\text{gate}}_i, \mathbf{c}_i]$ into classifier $C$ for logit $z_i$ and probability $\hat{p}_i = \sigma(z_i)$ (Eqs. 21–22).
5. **Real-Only Response-Consistency Regularization (Sec. III-F):** Trains with $\mathcal{L} = \mathcal{L}_{cls} + \lambda_{resp}\mathcal{L}_{resp}$ ($\lambda_{resp} = 0.001$, Eqs. 23–24), where $\mathcal{L}_{resp}$ penalizes squared L2 deviation of L2-normalized pre-embedding encoder features $\tilde{\mathbf{f}}_{i,k}$ from their within-image center $\boldsymbol{\mu}^f_i$ for **real images only** ($\mathcal{B}_r$, Eqs. 25–28), preserving heterogeneous artifact patterns on fake images.

## Architecture
- **Encoder:** Shared **ResNet18** (trained from scratch, 256-D output) applied independently to the 3 operator response maps.
- **Gate MLP ($G$):** `Linear(512, 256) -> ReLU -> Dropout(0.1) -> Linear(256, 1)` + learnable 3-D global bias $\mathbf{b}$.
- **Context Head ($H$):** `Linear(768, 256) -> ReLU -> Dropout(0.25)`.
- **Classifier ($C$):** Linear/binary classification head over concatenated $[\mathbf{f}^{\text{gate}}_i, \mathbf{c}_i]$ (512-D).
- **Computational Profile (Sec. V-G, Table 12; NVIDIA 4090D, batch size 32, $256 \times 256$):** **11.77M** learnable parameters, **14.21 GFLOPs** (3-response forward pass), **893.07 MB** peak GPU memory, **0.465 ms/image** (2,151.74 FPS) network-only, and **1.994 ms/image** (501.39 FPS) end-to-end (including image loading, operator construction, CPU-to-GPU transfer, and inference).

## Dataset
- **Training & Validation (Sec. IV-A, Table A-II):** ForenSynths `train.csv` (4 classes: `car`, `cat`, `chair`, `horse`; **72,012 real / 72,012 fake** = 144,024 images) and `val.csv` (same 4 classes; **800 real / 800 fake** = 1,600 images).
- **Evaluation Suites (all strictly held out, Appendix B Tables A-I & A-II):**
  1. **CrossGen-38:** 38 evaluation subsets assembled from 5 public dataset families—Diffusion1kStep (D1K, 5 subsets), DiffusionForensics (DF, 8 subsets), ForenSynths test (FS, 8 subsets including Deepfakes), GANGen-Detection (GG, 9 subsets), and UniversalFakeDetect (UFD, 8 subsets). Total 190,598 images analyzed in gate entropy diagnostics (Sec. V-F4).
  2. **UniversalFakeDetect-aligned (UFD-aligned):** 15 subsets (Pro-GAN, Cycle-GAN, Big-GAN, Style-GAN, Gau-GAN, Star-GAN, Deepfakes, Guided, LDM 200/200 w/CFG/100, GLIDE 100-27/50-27/100-10, DALLE).
  3. **GANGen-Detection / Self-Synthesis:** 9 GAN subsets (AttGAN, BEGAN, CramerGAN, InfoMaxGAN, MMDGAN, RelGAN, S3GAN, SNGAN, STGAN).
- **Availability:** Source datasets are public; CrossGen-38 is a manifest-defined suite over those public datasets. Code repository link is not reported in the PDF.

## Training
- **Preprocessing (Sec. IV-B):** Convert to RGB; training resizes to $288 \times 288$, random crops to $256 \times 256$, and horizontal flips ($p=0.5$); validation/testing deterministically resize to $256 \times 256$.
- **Optimization:** AdamW optimizer, LR $5 \times 10^{-5}$, weight decay $2 \times 10^{-4}$, batch size 16, 10 epochs, mixed-precision enabled, $\lambda_{resp} = 0.001$, $\tau = 1.3$, $\epsilon = 0.003$, $\mathbf{b}_0 = [0.7, -0.1, -0.1]$.
- **Model Selection & Seeds:** Main run uses seed 42; multi-seed fusion validation uses seeds 42, 123, and 2026. Checkpoints selected solely via balanced accuracy on `val.csv`; test evaluation uses fixed threshold 0.5.

## Evaluation
- **Metrics (Sec. IV-C):** Accuracy (Acc, fixed threshold 0.5), Average Precision (AP), and ROC-AUC (positive class = AI-generated), macro-averaged equally across subsets (mAcc, mAP, mAUC).
- **Protocols (Sec. IV-A/D, V-A–D):** CrossGen-38 (38 subsets), GANGen-Detection/Self-Synthesis (9 GANs vs. 11 baselines), and UFD-aligned (15 GAN+DM+Deepfakes subsets vs. 11–13 baselines). Note: External baselines are protocol-aligned reported numbers rather than re-trained under identical conditions (Sec. IV-D).
- **Controlled Ablations & Diagnostics (Sec. V-E–H):**
  - Single-operator, naive concatenation, 4-branch Gamma-Sharpen, last-epoch checkpoint, all-sample consistency, gate-only allocation (without $\bar{\mathbf{t}}_i$), uniform fusion, static learned fusion, and dynamic gate without bias (Table 5).
  - Leave-one-operator-out deletion and Gamma-Sharpen replacement (Table 6).
  - 3-seed paired comparison vs. uniform fusion (Table 7).
  - Inference-time operator parameter sensitivity and matched vs. mismatched ColorQuant divisor experiments (Tables 8–9).
  - Frozen linear branch probes (Tables 10, 14), subset-level gate–probe agreement, fixed-checkpoint weight interventions (Tables 11, 15), gate entropy statistics (Fig. 4), and source-level threshold/score diagnostics on Diffusion1kStep (Table 13, Fig. 5, Fig. 6).

## Results
- **CrossGen-38 Overall & Group-Wise (Table 1):** Achieves **92.86% mAcc**, **96.94% mAP**, and **97.23% mAUC** across all 38 subsets. Group mAcc: GANGen-Detection **96.98%**, ForenSynths test **94.82%**, UniversalFakeDetect **94.82%**, DiffusionForensics **93.82%**, and Diffusion1kStep **77.60%**.
- **GANGen-Detection / Self-Synthesis (Table 2):** Achieves **96.98% mAcc / 99.26% mAP**, surpassing PiD (round) (94.70% / 99.40%) by +2.28 pp mAcc (-0.14 pp mAP), NPR (93.20% / 96.60%), and PatchForensics (90.10% / 95.40%). Hardest source: S3GAN (85.10% Acc / 93.84% AP).
- **UFD-Aligned 15-Subset Comparison (Tables 3–4):** Achieves **95.62% mAcc** (2nd to PiD 96.22%, ahead of DySy-Det 94.41%, NPR 93.21%, UnivFD 86.29%) and **98.01% mAP** (2nd to PiD 98.24%, ahead of NPR 97.61%, AIDE 97.35%, UnivFD 95.89%, B-Free 94.46%).
- **Controlled Ablations (Tables 5–7):**
  - Single operators: ColorQuant 82.34% mAcc / 93.19% mAUC; JPEGProbe 79.32% / 88.26%; LowBit 71.56% / 83.15%. Naive concatenation drops sharply to **64.62% mAcc / 75.94% mAUC**.
  - Controlled fusion (seed 42): Full PORI-Gate (**92.86% mAcc / 96.94% mAP / 97.23% mAUC**) beats uniform fusion (91.66% / 95.61% / 96.35%), static learned fusion (91.47% / 95.46% / 96.24%), and bias-free dynamic gate (89.73% / 94.38% / 95.15%). Removing mean-token allocation context drops to 90.25% mAcc; all-sample consistency drops to 90.47% mAcc.
  - Leave-one-out (Table 6): Removing ColorQuant drops mAcc by 11.37 pp (to 81.49%), JPEGProbe by 4.92 pp (87.94%), LowBit by 2.11 pp (90.75%); replacing LowBit with Gamma-Sharpen drops 2.82 pp (90.04%).
  - Multi-seed (Table 7, seeds 42/123/2026): PORI-Gate **92.39±0.41% mAcc / 96.46±0.42% mAP / 96.84±0.35% mAUC** vs. uniform **90.97±0.63% / 95.09±0.49% / 95.89±0.42%** (+1.43 pp mAcc, +1.37 pp mAP, +0.94 pp mAUC).
- **Operator Sensitivity & Gate Diagnostics (Tables 8–11, 13–15):**
  - Inference-time normalization mismatch causes catastrophic drops (CQ divisor $8 \to 4/16$: 52.48%/46.94% mAcc; JPEGProbe divisor $25 \to 12.5/50$: 80.56%/79.63% mAcc), whereas retraining with CQ divisor 16 recovers 91.92% mAcc (Table 9).
  - Gate's top mean weight matches the highest linear-probe branch AUC on **37/38 subsets (97.37%)**, vs. 32/38 (84.21%) for always-CQ; mean gate entropy across 190,598 images is $0.3238 \pm 0.3094$ (normalized ~0.295).
  - Diffusion1kStep failure analysis (Table 13–15, Fig. 5): `Improved-Diffusion` suffers poor representation transfer (60.38% Acc, 67.64% AUC; frozen probes below chance: CQ 26.62%, LB 31.06%, JPG 40.98%), while `DDPM` retains strong ranking (90.16% AUC, CQ probe 91.70% AUC) but fails fixed-0.5 thresholding (76.37% Acc vs. 87.62% balanced accuracy at post-hoc threshold $1.0 \times 10^{-6}$).

## Strengths
- **Lightweight, fast, and semantic-decoupled:** Only 11.77M parameters and 501.39 FPS end-to-end (batch 32) without CLIP/ViT backbones or generative reconstruction overhead, trained solely on 4-class ProGAN ForenSynths.
- **Rigorous controlled ablations & multi-seed validation:** Clearly isolates the contributions of deterministic probes, real-only consistency regularization, mean-token context, image-adaptive logits, and global operator bias.
- **Transparent failure-mode & calibration diagnostics:** Explicitly audits Diffusion1kStep failures (`Improved-Diffusion` vs. `DDPM`), separating representation-transfer failure from operating-point threshold mismatch, and quantifies normalization-mismatch fragility.
- **Interpretable per-image gate allocations:** Operator weights $\alpha_{cq}, \alpha_{lb}, \alpha_{jpg}$ align 97.37% of the time with the strongest subset-level forensic branch.

## Weaknesses
- [GAP-ready: supported by P0036] **Severe failure on specific diffusion sampling regimes (`Improved-Diffusion` and `DDPM`):** In Diffusion1kStep, `Improved-Diffusion` yields 60.38% Acc / 67.64% AUC with reversed frozen-probe orderings (26.62%–40.98% AUC), and `DDPM` drops to 76.37% Acc due to score-distribution shift (optimal threshold $1.0 \times 10^{-6}$ vs. fixed 0.5).
- [GAP-ready: supported by P0036] **No full-model post-processing robustness benchmark on CrossGen-38:** Resize/blur/gamma perturbations were only tested on the validation split for single-operator diagnostics (Fig. 1), not evaluated end-to-end on the final PORI-Gate detector across CrossGen-38 (e.g., social media JPEG compression, resizing, noise).
- [GAP-ready: supported by P0036] **Not evaluated on modern face-specific or newest text-to-image diffusion benchmarks:** ForenSynths training uses 4 non-face classes (`car, cat, chair, horse`), and only FS Deepfakes and older GAN/DM suites are tested—omitting modern diffusion face benchmarks (e.g., DiFF, SDXL/FLUX/Midjourney v5+).
- [GAP-ready: supported by P0036] **Extreme sensitivity to operator-normalization mismatch and deterministic $256 \times 256$ resizing:** Changing ColorQuant or JPEGProbe divisors at inference without retraining collapses mAcc (92.86% $\to$ 46.94%–52.48%), and deterministic resizing to $256 \times 256$ may distort high-resolution spatial/bit-plane artifacts.
- [GAP-ready: supported by P0036] **No code link and external baselines are protocol-aligned rather than identically re-trained:** Tables 2–4 compare against published numbers from other papers with differing training data, backbones, and preprocessing.

## Research Gap
- [GAP-ready: supported by P0036] **Operating-point calibration and out-of-distribution score-shift handling:** As `Diffusion1kStep-DDPM` demonstrates (90.16% AUC but 76.37% Acc at threshold 0.5), threshold-fixed binary classification fails under cross-generator score-distribution shifts unless paired with calibration or abstention (`Inconclusive`) mechanisms.
- [GAP-ready: supported by P0036] **End-to-end robustness of adaptive low-level operator fusion under post-processing and on face-specific diffusion generators:** Extending reliability-guided operator fusion to facial deepfake/diffusion forensics and JPEG/resize/social-media attack suites.
- [GAP-ready: supported by P0036] **Incorporating explicit reliability/conflict checks rather than purely learned soft weights:** On `Improved-Diffusion`, the learned gate still assigns 0.6912 weight to ColorQuant despite ColorQuant's 26.62% probe AUC, showing that learned gates without external reliability validation can misallocate trust on unseen generators.

## Future Work
- Expanding forensic cue coverage beyond the three low-level RGB operators to address challenging diffusion sources like `Improved-Diffusion` (Sec. V-H, Sec. VI).
- Developing more adaptive allocation and operating-point calibration/transfer strategies across generator families (Sec. V-H, Sec. VI).
- Joint evaluation of representation transfer and adaptive allocation under broader distribution shifts.

## Interesting Ideas
- **Hybrid global bias + sample-specific reliability gate ($\mathbf{s}_i + \mathbf{b}$):** Combining a learnable population prior with input-conditioned logits prevents the gate collapse seen in bias-free dynamic gating (89.73% vs. 92.86% mAcc) while outperforming static weights (91.47%).
- **Real-only response-consistency regularization:** Enforcing representation consistency across operators *only on real images* aligns natural-image statistics while allowing different operators to preserve distinct forgery signatures on synthetic images (+2.39 pp mAcc over all-sample consistency).
- **Context descriptor alongside gated fusion:** Passing $[\text{mean}_k, \max_k, \text{std}_k]$ of operator tokens separately from the weighted sum prevents weighted averaging from washing out cross-operator disagreement signals.

## Possible Reuse
- **MOD006 (`Evidence Validation`):** P0036's empirical proof that no single forensic probe is uniformly reliable across conditions (Fig. 1: JPEGProbe rescues 94.2% of ColorQuant's real-image false positives; LowBit rescues 83.8% of JPEGProbe's) directly reinforces MOD006's design principle of explicit reliability annotation (`high`/`medium`/`low`/`unusable`) without discarding conflicting evidence. Moreover, P0036's failure on `Improved-Diffusion`—where the learned gate still trusted ColorQuant (0.6912 weight) despite reversed probe discrimination—demonstrates why MOD006's independent validation checks and conflict flagging are essential safeguards before fusion.
- **MOD007 (`Evidence Fusion Engine`):** P0036's Reliability-Guided Fusion Gate ($\mathbf{s}_i + \mathbf{b}$ with temperature scaling and floor $\epsilon$) plus cross-operator context statistics ($\text{mean}, \max, \text{std}$) provides a concrete architectural blueprint for future `weighted` / learned `FusionStrategy` extensions registered in MOD007 (`fusion/strategies/`), showing empirically (+1.43 pp mAcc across 3 seeds) why reliability-weighted fusion + disagreement summary outperforms uniform averaging.
- **MOD003 (`Evidence Acquisition Layer`) & MOD004 (`Deep Learning Specialist`):** ColorQuant, LowBit, and JPEGProbe (Algorithm 1) are fast, deterministic, Exif-free low-level operators that can be wrapped as lightweight forensic collectors or preprocessing branches in MOD003/MOD004.
- **MOD008 (`Decision Engine`) & MOD009 (`Confidence Estimation`):** The `Diffusion1kStep-DDPM` finding (90.16% AUC vs. 76.37% Acc at fixed threshold 0.5) directly informs MOD008's separation of fused evidence lean from hard thresholding and supports MOD009's separation of probability from decision uncertainty/calibration; normalized gate entropy $\tilde{H}_i$ is also a useful auxiliary uncertainty signal.
- **MOD010 (`Explainability Engine`) & MOD011 (`Forensic Reasoning Engine`):** Per-sample operator weights ($\alpha_{cq}, \alpha_{lb}, \alpha_{jpg}$) and response maps can populate structured attribution evidence in `explanation.json` (MOD010) and support evidence-cited reasoning sentences in MOD011 (e.g., citing which low-level probe dominated and whether cross-operator dispersion was high).

## Questions
- How would PORI-Gate perform under end-to-end JPEG compression (QF 50–90), Gaussian blur, and social media re-encoding across the full CrossGen-38 suite (especially since JPEGProbe itself uses internal QF 75)?
- Can explicitly calibrating the classifier threshold or incorporating out-of-distribution/entropy gating (MOD006/MOD008 style) resolve the `Diffusion1kStep-DDPM` operating-point shift without access to test labels?
- How well does a ForenSynths-trained (car/cat/chair/horse) PORI-Gate transfer to high-resolution diffusion face benchmarks such as DiFF (`P0023`) or AI-Face-FairnessBench (`P0016`)?

## Connections
- Directly relates to **P0035** (*APN*, Meng et al. 2024): both target cross-generator generalization using multi-cue fusion, but P0035 uses heavy Swin-T + dual ResNet-18 DFT-proposal networks trained with MI minimization, whereas P0036 uses a single shared ResNet-18 (11.77M params) over three deterministic RGB operators fused via a reliability gate.
- Relates to **P0003** (*Synthbuster*, Bammey 2024) and **P0010** (*GAN DCT Anomalies*, Giudice et al. 2021): shares the low-level non-semantic forensic philosophy, replacing Fourier/DCT spectral transforms with ColorQuant, LowBit, and JPEGProbe spatial responses.
- Complements **P0007** (*Deepfake Detection Generalization*, Khan & Dang-Nguyen 2024) and **P0016** (*Comparative GAN vs DM Faces*, Altamimi et al. 2026): addresses dataset/semantic shortcuts via low-level probes and directly surfaces threshold/score-shift issues under domain shift.
- Contrasts with **P0018** (*Mastering Deepfake Detection*, Guarnera et al. 2024) and **P0023** (*DiFF*, Cheng et al. 2024): P0036 demonstrates strong zero-shot transfer from 4 non-face ProGAN classes to 38 GAN+diffusion subsets, whereas P0018/P0023 focus on face-specific multi-generator detection and attribution.
- Relates to **P0013** (*Robust Ensemble for Social Media*, Sharma et al. 2025) and **P0015** (*GLFNet*, Xue et al. 2023): advances multi-cue fusion from static/naive combination to input-conditioned reliability weighting with explicit global bias and dispersion context.
