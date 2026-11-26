# Paper Summary: P0035

## Metadata
- **Paper ID:** P0035
- **Title:** Artifact feature purification for cross-domain detection of AI-generated images
- **Authors:** Zheling Meng, Bo Peng, Jing Dong, Tieniu Tan, Haonan Cheng
- **Year:** 2024
- **Venue:** Computer Vision and Image Understanding
- **DOI:** 10.1016/j.cviu.2024.104078

## Problem
Existing AI-generated image detectors achieve near-perfect in-domain accuracy (e.g., 90.3%–99.9% on Stable Diffusion v1 under ImageNet in Fig. 1(a)), but experience severe accuracy drops under **cross-domain** shifts: both **cross-generator detection** (unseen generative models; baseline drops of 26.5%–59.5% when moving from SD v1 to GLIDE under ImageNet) and **cross-scene detection** (unseen image content distributions; baseline drops of 3.7%–23.5% when moving from ImageNet to LSUN-Bedroom for SD v1). The root cause is that learned feature spaces remain coupled with generator-specific artifacts and object/content-biased scene features.

## Motivation
In real-world forensic deployments, training data cannot cover all possible generative models or all possible visual scenes. Detectors therefore need domain-agnostic artifact representations decoupled from irrelevant image content and generator-specific shortcuts. Crucially, the authors argue (Sec. 3.3, Sec. 4.5) that explicit feature separation alone does not prevent artifact cues from remaining diluted inside "artifact-irrelated" features or prevent "artifact-related" features from retaining domain bias—motivating an additional training-time **implicit purification** mechanism grounded in mutual information minimization, together with adaptive frequency-band localization and spatial orthogonal decomposition.

## Method
The paper proposes the **Artifact Purification Network (APN)** (Sec. 3, Fig. 2), consisting of three components:
1. **Explicit Purification in Frequency (Sec. 3.2.1):**
   - Applies 2D Discrete Fourier Transform (DFT) per RGB channel $c \in \{R, G, B\}$, leveraging Hermitian symmetry ($0 \le u \le \lfloor M/2 \rfloor$, $0 \le v \le N-1$) so inverse DFT reconstructs real-valued images. Computes amplitude $A_c$ and phase $P_c$.
   - Predicts $K$ suspicious frequency-band proposals ($PPS^i_{A_c,u}, PPS^i_{A_c,v}, PPS^i_{P_c,u}, PPS^i_{P_c,v}$ for $i=0,\dots,K-1$) via BatchNorm, residual convolutions, One-sided Feature Pooling ($OFP(\cdot)$ with kernels $(3 \times N)$ along $u$ and $(\lfloor M/2 \rfloor \times 3)$ along $v$), a fully connected layer, and Sigmoid activation, anchored by equal-division prior frequency positions in $[0,1]$.
   - Uses cross-shaped binary masks $\mathbb{I}^i_{A_c}, \mathbb{I}^i_{P_c}$ (Eqs. 2–3) to partition $A_c$ and $P_c$ into artifact-related ($A^{i,r}_c, P^{i,r}_c$) and artifact-irrelated ($A^{i,ir}_c, P^{i,ir}_c$) spectra (Eq. 1), and applies inverse DFT (Eq. 4) to obtain 3-channel spatial reconstructions $I^{i,r}$ (containing suspicious bands) and $I^{i,ir}$ (excluding them).
   - Two backbones extract feature vectors from $I^{i,r}$ and $I^{i,ir}$. An 8-head self-attention layer followed by three FC layers and Sigmoid scores the $K$ suspicious proposals to form a confidence-weighted artifact-related feature $f^r_f$, while $f^{ir}_f$ averages the $I^{i,ir}$ features.
2. **Explicit Purification in Space (Sec. 3.2.2):**
   - Extracts a spatial feature vector $f_s \in \mathbb{R}^{C \times 1}$ ($C=256$) from the RGB input $I$.
   - Performs **learnable feature orthogonal decomposition** (Eq. 5) using two mutually orthogonal learnable basis sets $\Omega^r = \{\omega^r_1,\dots,\omega^r_{m_r}\}$ and $\Omega^{ir} = \{\omega^{ir}_1,\dots,\omega^{ir}_{m_{ir}}\}$ ($m_r = m_{ir} = 128$, $m_r + m_{ir} = C$) to obtain $f^r_s$ and $f^{ir}_s$.
3. **Implicit Purification (Sec. 3.3, training-only; discarded at inference):**
   - **Cross-branch Alignment ($\mathcal{L}_{align}$, Eq. 6):** MSE loss aligning $(f^r_f, f^r_s)$ and $(f^{ir}_f, f^{ir}_s)$ across modalities.
   - **Mutual Information Minimization ($\mathcal{L}_{mi}$, Eq. 7):** Minimizes the CLUB variational upper bound of mutual information between averaged $f^r = 0.5(f^r_f + f^r_s)$ and $f^{ir} = 0.5(f^{ir}_f + f^{ir}_s)$ using an auxiliary neural estimator $q_\theta(f^r \mid f^{ir})$ trained with $\mathcal{L}_q$ (Eq. 8).
4. **Classification (Sec. 3.1, Fig. 2):** Averages $f^r_f$ and $f^r_s$ and passes the fused 256-D vector to an MLP classifier to predict fake probability.

## Architecture
- **Spatial Branch (`Backbone-s`):** Swin-Transformer-tiny (`Swin-T`) producing $C = 256$-D features, followed by learnable orthogonal decomposition bases $\Omega^r, \Omega^{ir}$ ($128$ basis vectors each).
- **Frequency Branch (`Backbone-f1`, `Backbone-f2`):** Two ResNet-18 backbones encoding $I^{i,r}$ and $I^{i,ir}$; $K=15$ frequency-band proposals on GenImage and $K=5$ on DiffusionForensics; 8-head self-attention + 3-layer FC scoring network.
- **Implicit Purification Estimator $q_\theta$ (training-only):** Two fully connected neural networks predicting variational mean and variance of $f^r \mid f^{ir}$.
- **Classifier:** MLP head operating on $0.5(f^r_f + f^r_s)$.
- **Parameter count / FLOPs / latency:** Not reported in the PDF.

## Dataset
- **GenImage** (Zhu et al., 2023a; Sec. 4.1.1): 1,331,167 real images from ImageNet and 1,350,000 fake images from 8 generators (SD v1.4, SD v1.5, Wukong, ADM, BigGAN, GLIDE, Midjourney, VQDM) across ImageNet classes, partitioned into 8 non-overlapping subsets.
- **DiffusionForensics (DF)** (Wang et al., 2023a; Sec. 4.1.1): Training set has 40,000 real LSUN-Bedroom images and 40,000 ADM-generated images. Evaluation set has 1,000 real LSUN-Bedroom images and fake images from 8 generators under LSUN-Bedroom (1,000 images each for ADM, DALLE2, Diff-ProjectedGAN, iDDPM, IF, ProjectedGAN, SD v1; 100 images for Midjourney).
- **Note:** Both benchmarks are general-object/scene datasets (ImageNet, LSUN-Bedroom), not face-specific.
- **Availability:** Both datasets are publicly available external benchmarks; the abstract states code "will be available on GitHub" (no URL provided in the preprint PDF).

## Training
- **Loss Functions (Sec. 3.4):** Total APN loss $\mathcal{L}_{APN} = \mathcal{L}_{ce} + \mathcal{L}_{band} + \mathcal{L}_{basis} + \mathcal{L}_{align} + \mathcal{L}_{mi}$ (Eq. 9), where $\mathcal{L}_{band}$ (Eq. 10, $\epsilon = 0.01$) enforces valid proposal intervals and $\mathcal{L}_{basis}$ (Eq. 11) enforces orthogonality between $\Omega^r$ and $\Omega^{ir}$. Estimator $q_\theta$ is trained with $\mathcal{L}_q$ (Eq. 8).
- **Alternating Optimization (Sec. 4.2.2):** For every 1 APN update step, $q_\theta$ is updated 3 times (alternately freezing the other network).
- **Hyperparameters:** Adam optimizer, batch size 32 for both APN and $q_\theta$; LR $1 \times 10^{-4}$ (except $1 \times 10^{-7}$ for $\Omega^r, \Omega^{ir}$), decaying by $0.1\times$ every 20,000 iterations for APN and every 60,000 iterations for $q_\theta$. Orthogonal bases initialized as $\Omega^r = [I, Z]$ and $\Omega^{ir} = [Z, I]$. Trained for 10 epochs on GenImage and 40 epochs on DF.
- **Preprocessing:** Random $224 \times 224$ crop during training; center $224 \times 224$ crop at inference. No other data augmentations used.

## Evaluation
- **Baselines (10 methods, Sec. 4.1.2):** Spec, CNNSpot, F3Net, GramNet, PatchFron (PatchForensics), Swin-T, Patch5M, SIA, LNP, and LGrad, trained and evaluated with official code/configurations.
- **Protocols (Sec. 4.1.3):**
  1. *Cross-generator (GenImage):* Train on SD v1.4 subset; evaluate on all 8 ImageNet subsets (Table 1).
  2. *Cross-generator (DF):* Train on real + ADM LSUN-Bedroom images; evaluate on real + 8 LSUN-Bedroom generators (Table 2).
  3. *Cross-scene:* Train separately on SD v1.4, ADM, and Midjourney subsets of GenImage (ImageNet); evaluate on corresponding ImageNet and LSUN-Bedroom (DF) subsets (Table 3).
- **Metric:** Classification Accuracy (%) only (AUC, AP, F1, and EER are not reported).
- **Explainability & Diagnostics (Sec. 4.5):** t-SNE visualizations of $f^r, f^{ir}$ with/without implicit purification (Fig. 3), confidence-weighted proposal frequency distributions and cross-domain correlation matrices (Fig. 4), Layer-CAM heatmaps on the final spatial backbone layer (Fig. 5), and spatial reconstructions of top-5 frequency proposals (Fig. 6).
- **Ablations (Sec. 4.6, Table 4):** Module ablation across 7 configurations on GenImage (Table 4(a)) and proposal-count sensitivity $K \in \{1, 5, 10, 15, 20, 25\}$ on GenImage and DF (Table 4(b)).

## Results
- **Cross-Generator on GenImage (Table 1):** APN achieves **80.4%** mean accuracy across 8 generators, outperforming all 10 baselines by **5.6%–16.4%** (second-best Swin-T 74.8%, LNP 73.1%, Patch5M/SIA 71.9%). APN ranks 1st on 4/8 generators (SD v1.4: 99.9%, ADM: 53.9%, GLIDE: **89.3%** [+21.0% over second-best LNP 68.3%], VQDM: 67.2%) and 2nd on 3/8 (SD v1.5: 99.8%, Wukong: 98.9%, Midjourney: 72.3%; BigGAN: 61.7% vs. LGrad 69.9%).
- **Cross-Generator on DF (Table 2):** APN achieves **98.7%** mean accuracy (Real: 99.8%, ADM: 99.6%, DALLE2: 100.0%, D-Pro.GAN: 94.3%, iDDPM: 100.0%, IF: 100.0%, Midjourney: 99.0%, Pro.GAN: 96.0%, SD v1: 99.3%), outperforming baselines by **1.7%–50.1%** (Patch5M 97.0%, F3Net 96.8%).
- **Cross-Scene ImageNet $\rightarrow$ LSUN-Bedroom (Table 3):** APN achieves **99.6%** average on ImageNet and **99.5%** on LSUN-Bedroom (SD v1: 100.0%, ADM: 99.2%, Midjourney: 99.2%), suffering only a **0.1%** cross-scene drop vs. 3.1% for CNNSpot and 4.5% for F3Net.
- **Ablations (Table 4):**
  - *Module ablation (Table 4(a)):* Full APN (Line 7) = **80.4%**; without implicit purification $\mathcal{L}_{mi}$ (Line 1) = 75.3% (-5.1%); without explicit purification (Line 2) = 71.0% (-9.4%); frequency explicit + implicit only (Line 3) = 79.1%; spatial explicit + implicit only (Line 4) = 77.1%; removing proposal module `PPS` (Line 5) = 74.8% (-5.6%); removing spatial orthogonal decomposition `D` (Line 6) = 77.8% (-2.6%).
  - *Proposal count $K$ (Table 4(b)):* Optimal $K$ differs by dataset—$K=15$ peaks on GenImage (**80.4%**, vs. 72.9% at $K=1$ and 76.5% at $K=25$), whereas $K=5$ and $K=10$ peak on DF (**98.7%**, vs. 98.2% at $K=15$).
- **Visualizations (Sec. 4.5, Figs. 3–6):** Implicit purification collapses real/fake density discrepancies in $f^{ir}$ and tightens $f^r$ into more isotropic clusters (Fig. 3). Layer-CAM maps show broad, diverse activations (bright, dark, textured, and plain regions) on fake images vs. minimal activation on real images (Fig. 5).

## Strengths
- **Dual-domain problem framing:** Explicitly addresses both cross-generator and cross-scene generalization rather than treating cross-domain evaluation as generator-shift alone.
- **Principled explicit + implicit purification:** Combines adaptive DFT amplitude/phase band proposals (via Hermitian-symmetric iDFT) and orthogonal spatial subspace decomposition with CLUB-based mutual information minimization during training, yielding clear ablation gains (+5.1% from implicit purification, +9.4% from explicit purification).
- **Zero-overhead implicit purification at inference:** The variational estimator $q_\theta$ and mutual-information losses are discarded after training.
- **Strong empirical cross-generator and cross-scene gains:** +5.6%–16.4% on GenImage, +1.7%–50.1% on DF, and near-zero (0.1%) drop across ImageNet $\rightarrow$ LSUN-Bedroom.
- **Interpretability diagnostics:** t-SNE feature disentanglement, Layer-CAM spatial heatmaps, and confidence-weighted proposal correlation analyses substantiate why purification improves generalization.

## Weaknesses
- [GAP-ready: supported by P0035] **Accuracy-only evaluation without ranking or calibration metrics:** Reports only classification Accuracy (%) across Tables 1–4, omitting threshold-independent AUC, AP, and calibration/F1 metrics that are critical when positive/negative score distributions shift across domains.
- [GAP-ready: supported by P0035] **No post-processing or compression robustness evaluation:** Trains solely with random $224 \times 224$ cropping and no augmentations, and never tests resilience to JPEG compression, resizing, Gaussian blur, or social media re-encoding—transformations known to severely degrade frequency/DFT artifacts.
- [GAP-ready: supported by P0035] **Not evaluated on face-specific deepfake or diffusion-face benchmarks:** Experiments cover general ImageNet objects (GenImage) and bedrooms (LSUN-Bedroom/DF); transfer to synthetic human faces (e.g., FF++, StyleGAN faces, DiFF) is untested.
- [GAP-ready: supported by P0035] **Substantial performance gaps remain on several unseen GenImage generators:** When trained on SD v1.4, GenImage accuracy remains modest on ADM (53.9%), BigGAN (61.7%), VQDM (67.2%), and Midjourney (72.3%).
- [GAP-ready: supported by P0035] **Dataset-sensitive proposal count $K$ and omitted compute profiling:** Optimal $K$ shifts between GenImage ($K=15$) and DF ($K=5/10$), and no parameter count, FLOPs, or inference latency is reported despite running Swin-T plus two ResNet-18 backbones across $K$ reconstructed images per branch.
- [GAP-ready: supported by P0035] **No code URL or statistical variance reported:** Preprint states code will be on GitHub without a link, and single-run results are reported without multi-seed variance.

## Research Gap
- [GAP-ready: supported by P0035] Extending explicit + implicit artifact purification (orthogonal spatial decomposition and MI-based disentanglement) to **synthetic face forensics** across both GAN and diffusion face generators, paired with AUC/AP and post-processing robustness evaluation.
- [GAP-ready: supported by P0035] Developing **post-processing-resilient frequency-band proposals** or training-time augmentation/purification schedules so DFT amplitude/phase proposals survive JPEG compression and resizing.
- [GAP-ready: supported by P0035] Replacing dataset-tuned fixed $K$ proposals and heavy dual-backbone iDFT passes with **lightweight, dynamically calibrated** artifact extraction.

## Future Work
- Not explicitly enumerated in a dedicated section in the PDF (Sec. 5 summarizes findings without a future work list).
- Implicitly motivated extensions include evaluating robustness under compression/resizing perturbations, testing on facial forgery benchmarks, and automating selection of proposal count $K$.

## Interesting Ideas
- **Orthogonal basis decomposition + CLUB MI minimization:** Constraining artifact-related and artifact-irrelated subspaces to be orthogonal ($\mathcal{L}_{basis}$) while minimizing their mutual information upper bound ($\mathcal{L}_{mi}$) directly operationalizes content/domain disentanglement without adversarial discriminators.
- **Learning with "irrelevant" features to purify "relevant" features:** Instead of discarding non-artifact features immediately, explicitly modeling $f^{ir}$ via complementary masked iDFT images ($I^{i,ir}$) and orthogonal complement bases ($\Omega^{ir}$) provides a contrastive anchor that prevents artifact leakage.
- **Training-only variational MI estimator:** Keeping $q_\theta$ strictly in the training loop adds zero inference overhead.

## Possible Reuse
- **MOD004 (`Deep Learning Specialist`) / Feature Disentanglement:** Orthogonal subspace decomposition ($\Omega^r, \Omega^{ir}$) and real/fake MI minimization can inspire an improved training objective for our deep learning forensic detector to suppress scene/semantic shortcuts.
- **MOD003 (`Evidence Acquisition Layer`) & MOD010 (`Explainability Engine`):** Confidence-weighted suspicious frequency-band proposals paired with Layer-CAM maps illustrate how frequency-band importance scores can be aligned with spatial attribution maps in `explanation.json` (while noting MOD010 only packages maps actually emitted by collectors).
- **Methodology for Cross-Scene Evaluation:** Separating *cross-generator* shift from *cross-scene* shift (Table 3 protocol) is directly reusable in our thesis evaluation design to verify that a face/image detector does not rely on background/scene biases.

## Questions
- How does APN perform when evaluated under JPEG compression (e.g., QF 50–85), downsampling, or social media re-encoding where high-frequency DFT bands are attenuated?
- Why did GenImage ADM accuracy remain near random guessing (53.9%) despite strong performance on GLIDE (89.3%) and DF-ADM (99.6%)?
- What is the exact computational overhead (GFLOPs and latency) of running $K=15$ inverse DFTs and dual ResNet-18 passes per image compared with single-pass detectors?

## Connections
- Relates to **P0003** (*Synthbuster*, Bammey 2024) and **P0010** (*GAN DCT Anomalies*, Giudice et al. 2021): all exploit frequency-domain synthesis traces, but P0035 learns adaptive DFT amplitude+phase proposals end-to-end with spatial orthogonal purification rather than fixed hand-crafted filters/DCT statistics.
- Complements **P0007** (*Deepfake Detection Generalization*, Khan & Dang-Nguyen 2024) and **P0016** (*Comparative GAN vs DM Faces*, Altamimi et al. 2026): directly targets the dataset/scene bias and cross-generator drop documented in P0007 and P0016.
- Contrasts with **P0018** (*Mastering Deepfake Detection*, Guarnera et al. 2024) and **P0021** (*Multiclass ViT*, Arshed et al. 2024): P0035 trains on a single generator (SD v1.4 or ADM) for zero-shot cross-generator generalization on general scenes rather than multi-generator closed-set classification/attribution on faces.
- Connects to **P0036** (*PORI-Gate*, Shen & Tian 2026): both fuse multiple complementary forensic representations for cross-generator generalization, with P0035 purifying spatial+frequency features via MI minimization while P0036 adaptively weights three lightweight deterministic low-level operators via reliability gating.
