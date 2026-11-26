# Paper Summary: P0029

## Metadata
- **Paper ID:** P0029
- **Title:** Enhancing abnormality identification: Robust out-of-distribution strategies for deepfake detection
- **Authors:** Luca Maiano, Fabrizio Casadei, Irene Amerini
- **Year:** 2026
- **Venue:** Forensic Science International: Digital Investigation (Vol. 56, 302062; DFRWS EU 2026)
- **DOI:** 10.1016/j.fsidi.2026.302062

## Problem
Deepfake detectors trained under the closed-world assumption assume test inputs come from the same In-Distribution (ID) manifold as training data. When deployed in open-world scenarios where generative AI models continuously evolve and produce diverse manipulations (face swapping, reenactment, retouching, full-face or non-face synthesis), detectors encounter Out-Of-Distribution (OOD) inputs that cause sharp performance degradation and overconfident misclassifications (Section 1, pp. 1–2). Framed under the generalized OOD taxonomy of Yang et al. (2021), the problem maps to Anomaly Detection with binary labels (Real/Fake, ID/OOD) and pure covariate shift (Section 1, p. 2).

## Motivation
Training a detector on every possible generative model is infeasible. Integrating an OOD detector into the deepfake detection pipeline enables open-world reliability by flagging unfamiliar inputs and signaling when model retraining is required (Section 1, p. 1). Output-only OOD baselines such as MSP, ODIN, and Confidence Branch rely solely on logits or confidence scores, which remain prone to overconfidence on unseen data. Combining Softmax probabilities with latent image encodings and reconstruction residuals (either raw image reconstruction or Vision Transformer attention-map reconstruction) provides richer signals to separate ID and OOD samples (Sections 2.2, 3, 4, pp. 2–4).

## Method
A two-stage cascade pipeline (Fig. 1, p. 3) coupling an **In-Distribution (ID) module** (deepfake classifier) with an **Abnormality module** (OOD detector):
1. **ID Module — CNN-based (`U-Net Scorer`, Section 3.1, p. 3):**
   - Uses a U-Net autoencoder (`U-Net4` for 112×112, `U-Net5` for 224×224) with $2^{4+l}$ bottleneck features and a 5-layer linear classification head (with 1D BatchNorm, 30% dropout, ReLU) attached after the bottleneck.
   - Simultaneously learns real/fake classification and input reconstruction via a weighted linear interpolation loss $\mathcal{L} = \alpha\,\text{BCE}(y, p) + \beta\,\text{MSE}(x, \hat{x})$ with $\alpha = 0.9$ and $\beta = 0.1$ (Eqs. 1–3, p. 3).
   - Computes the squared image reconstruction residual $(x - \hat{x})^2$ as auxiliary OOD evidence (Section 4.1, p. 4).
2. **ID Module — Transformer-based (`Tiny DeiT + AE/VAE`, Section 3.2, pp. 3–4):**
   - Trains a Tiny DeiT classifier for deepfake detection and extracts visual attention heatmaps (Fig. 2, p. 4) plus `[CLS]` token embeddings (192-D) before the classification MLP block (Section 4.2, p. 4).
   - Trains a separate convolutional AutoEncoder (MAE loss) or Variational AutoEncoder (MAE + KL divergence loss, Eq. 4, p. 4; VAE with reconstruction MSE $2e-4$ used in Section 5.3, p. 7) on ID attention maps; OOD inputs yield elevated attention-map reconstruction residuals.
3. **Abnormality Module (`V1`, `V2`, `V3`, Section 4.3, pp. 4–6):**
   - Consumes three auxiliary inputs from the ID module: (i) 2-D Softmax probability vector, (ii) latent encoding, and (iii) flattened squared reconstruction residual, outputting an OOD risk score via Sigmoid.
   - **V1** (Table 1, p. 5): Compresses residual with 3 Conv+BN+GELU Encoder blocks (stride-2 downsampling) to match bottleneck encoding size (12,544-D each), concatenates with Softmax (25,090-D), and feeds a 5-layer MLP + Sigmoid. Incompatible with Tiny DeiT's 192-D embedding (Section 4.3, p. 5).
   - **V2** (Table 2, p. 5): Uses a smaller encoding from the first conv layer of `U-Net Scorer`'s classification branch (1,568-D) or Tiny DeiT `[CLS]` (192-D) and 4 residual Encoder blocks (1,568-D) to reduce concatenation imbalance (3,138-D for CNN). Compatible with both CNN and Transformer (112p/224p).
   - **V3** (Fig. 4, Table 3, pp. 5–6): Passes both residual (after 3 Encoder blocks) and encoding through symmetric 6-layer FC+BN+GELU MLPs down to 10-D each, concatenating them with 2-D Softmax (22-D total) before a single Dense + Sigmoid layer.
4. **Abnormality Training Regimes (Section 4.4, p. 6):**
   - **S (Synthesized / unsupervised):** Alters ID images with 5 synthetic corruptions (Gaussian blur, 10% JPEG quality, normal noise, normal noise with random std distortion, normal noise + $\pi/2$ rotation; Fig. 5, p. 6).
   - **R (Real / supervised):** Uses real OOD outlier images.
   - **M (Mixed):** Combines synthesized and real OOD samples.

## Architecture
- **CNN pipeline:** `U-Net4 Scorer` (4 encoders/decoders, 112×112) or `U-Net5 Scorer` (5 encoders/decoders, 224×224) + 5-layer MLP classification head -> `Abnormality Module` (`V1`, `V2`, or `V3` with Conv2D+BN+GELU Encoder blocks and FC+BN+GELU Risk MLP).
- **Transformer pipeline:** `Tiny DeiT` (224×224, 192-D `[CLS]` embedding) + separate convolutional `VAE` (or `AE`) for attention-map reconstruction -> `Abnormality Module` (`V2` or `V3`).

## Dataset
- **CDDB (Continual Deepfake Detection Benchmark, Li et al., 2023; Section 5.1, p. 6):** 82,000 images from 11 deepfake models across 3 groups (GAN models, non-GAN models, unknown models), re-partitioned into `binary` and `binary-partial` OOD settings under three scenarios:
  - **Content scenario:** Face images as ID; non-face images as OOD (mixed-content subsets removed to prevent semantic overlap).
  - **Group scenario:** GAN models as ID; non-GAN and unknown models as OOD.
  - **Mix scenario:** Random balanced split across techniques; ID includes BigGAN, GauGAN, StarGAN, Deepfake dataset, Glow, CRN, and WildDeepFake, with remaining sets in OOD.
- **CIFAR-10 OpenOOD Benchmark (Zhang et al., 2023b; Section 5.4, pp. 7–8):** ID = CIFAR-10; Far-OOD = MNIST, SVHN, Textures; Near-OOD = CIFAR-100, TinyImageNet (TIN).
- **Availability:** CDDB and OpenOOD/CIFAR-10 are existing public benchmarks; custom code/implementation availability is **Not reported** in the paper.

## Training
- **CNN ID module:** Trained with weighted BCE + MSE loss ($\alpha=0.9, \beta=0.1$); data augmentations include vertical/horizontal flip, RandAugment, and CutMix (Section 3.1, p. 3).
- **Transformer ID module:** Tiny DeiT classifier and VAE attention-map reconstructor trained separately; VAE uses MAE + KL divergence loss (Eq. 4, p. 4) achieving $2e-4$ reconstruction MSE (Section 5.3, p. 7).
- **Abnormality module:** Trained with standard BCE loss using `S`, `R`, or `M` OOD data (Sections 4.3–4.4, pp. 5–6).
- **Compute / Hyperparameters:** Video memory reported as ~2760 MB (`U-Net4` 112p and `U-Net5` 224p), 3602 MB (`U-Net4` 224p), and 1118 MB (`Tiny DeiT` 224p, ~57% reduction vs. `U-Net5`; Sections 5.2, pp. 6–7). Exact optimizer, learning rate, batch size, epochs, and GPU model are **Not reported**.

## Evaluation
- **ID Deepfake Detection (Section 5.2, Tables 4–5, pp. 6–7):** Accuracy, Precision, Recall, F1-Score, AUROC, AUPR, Jaccard Score, and VRAM usage.
- **CDDB OOD Detection (Section 5.3, Tables 6–11, p. 7):** AUROC, AUPR, and FPR95 across Content, Group, and Mix scenarios, compared against MSP (Hendrycks & Gimpel, 2016), ODIN (Liang et al., 2017), and Confidence Branch (DeVries & Taylor, 2018).
- **CIFAR-10 OOD Benchmark (Section 5.4, Tables 12–13, p. 8):** ID Accuracy and AUROC on Far-OOD and Near-OOD against 21 post-hoc, 12 trained-without-outliers, and 4 trained-with-outliers baselines.

## Results
- **ID Deepfake Detection (Section 5.2):**
  - *Content (Table 4, p. 6):* `U-Net5 Scorer` (224p) achieves Acc 0.946, Prec 0.957, Rec 0.934, F1 0.945, AUROC 0.991, AUPR 0.991, Jaccard 0.897, outperforming `U-Net4 Scorer` (112p: Acc 0.906, F1 0.907, AUROC 0.968) at the same ~2760 MB VRAM.
  - *Group & Mix with `U-Net5 Scorer` (Table 5, p. 7):* Group reaches Acc 0.906, F1 0.908, AUROC 0.973; Mix reaches Acc 0.926, F1 0.924, AUROC 0.988.
  - *Content with `Tiny DeiT` (text, p. 7):* Acc 0.96, Prec 0.96, Rec 0.956, F1 0.96, Jaccard 0.92, AUROC 0.993, AUPR 0.993, using only 1118 MB VRAM.
- **CDDB OOD Detection (Section 5.3, Tables 6–11, p. 7):**
  - *Baselines (Tables 6–8):* Content best baseline ODIN gets AUROC 82.67, AUPR 80.03, FPR95 0.56 (MSP 77.85; Conf. branch 78.38); Group MSP/ODIN drop to AUROC 62.06 / 60.3 (FPR95 0.84 / 0.83); Mix MSP/ODIN get AUROC 69.74 / 62.58 (FPR95 0.74 / 0.823).
  - *CNN Abnormality Modules on Content with U-Net4 (Table 9):* Unsupervised `V2S` achieves AUROC 91.6, AUPR 93.55, FPR95 0.49 (vs. `V1S` 77.79 and `V3S` 64.13). Supervised `V2R` reaches AUROC 100, AUPR 100, FPR95 0; Mixed `V2M` gets AUROC 99.95, AUPR 99.88, FPR95 8e-4.
  - *CNN V2 on Group & Mix with U-Net5 (Table 10):* `V2S` drops to AUROC 63.35 (Group) and 60.14 (Mix), whereas `V2M` recovers to AUROC 92.72, AUPR 95.1, FPR95 0.59 (Group) and AUROC 80.0, AUPR 86.19, FPR95 0.87 (Mix).
  - *Transformer Abnormality Modules on Content (Table 11):* `V3S` achieves AUROC 93.77, AUPR 94.55, FPR95 0.41 (beating CNN `V2S`); `V2R` gets AUROC 100, AUPR 100, FPR95 1e-4; `V2M` gets AUROC 99.97, AUPR 99.98, FPR95 3e-4. However, the Transformer approach fails on Group and Mix scenarios because attention maps collapse toward uniform distributions on semantically varied images (p. 7).
- **CIFAR-10 OpenOOD Benchmark (Tables 12–13, p. 8):**
  - `Tiny DeiT` reaches 97.5% ID Accuracy.
  - *Far-OOD (Table 12):* `ABN Module V2M` achieves AUROC 99.24 (MNIST), 98.06 (SVHN), 99.43 (Textures); unsupervised `ABN Module V2S` achieves 93.15 (MNIST), 95.42 (SVHN), 94.88 (Textures).
  - *Near-OOD (Table 13):* `ABN Module V2M` achieves AUROC 93.36 (CIFAR-100) and 99.66 (TIN, highest overall), whereas `ABN Module V2S` drops to 69.07 (CIFAR-100) and 84.02 (TIN).

## Strengths
- **Dual-paradigm OOD framework** comparing CNN image-reconstruction residuals (`U-Net Scorer`) against Vision Transformer attention-map residuals (`Tiny DeiT + VAE`).
- **Auxiliary feature balancing (`V1`–`V3`)** systematically addresses dimensional imbalance between 2-D Softmax probabilities, high-dimensional latent encodings, and spatial reconstruction residuals.
- **Unsupervised synthetic OOD option (`S`)** removes dependence on real outlier exposure while achieving strong Far-OOD and Content-scenario OOD detection (91.6–93.77 AUROC).
- **Hard OOD benchmark construction** repurposing CDDB into Content, Group (GAN vs. non-GAN/unknown), and Mix splits alongside standard CIFAR-10 OpenOOD evaluation.
- **Lightweight Transformer ID module** (`Tiny DeiT`) cuts VRAM by ~57% (1118 MB vs. 2760 MB) while improving ID AUROC to 0.993.

## Weaknesses
- [GAP-ready: supported by P0029] **Transformer attention-map OOD failure on generator shifts** — `Tiny DeiT` attention maps become uniform and fail on Group and Mix scenarios because the transformer prioritizes semantic content over subtle forgery traces (Section 5.3, p. 7).
- [GAP-ready: supported by P0029] **Unsupervised OOD (`V2S`) struggles on Near-OOD and generator shifts** — AUROC drops to 63.35 on CDDB Group, 60.14 on CDDB Mix, and 69.07 on CIFAR-100 Near-OOD, showing that simple image corruptions do not mimic unseen generative architectures (Tables 10, 13, pp. 7–8).
- [GAP-ready: supported by P0029] **JPEG/blur corruption conflict** — using 10% JPEG compression and Gaussian blur as synthesized OOD triggers risks falsely flagging heavily compressed real-world or social-media ID images as OOD (Section 4.4, p. 6).
- [GAP-ready: supported by P0029] **No probability calibration or uncertainty decomposition** — does not evaluate ECE, Brier Score, or epistemic/aleatoric uncertainty calibration on ID or OOD samples.
- [GAP-ready: supported by P0029] **Missing reproducibility and protocol concerns** — training hyperparameters/code URL are not reported, validation sets are noted as sampled from test data (Section 5.1, p. 6), and experiments are restricted to 112×112 / 224×224 CDDB and CIFAR-10 rather than modern high-resolution diffusion face datasets (e.g., DiFF).

## Research Gap
- [GAP-ready: supported by P0029] Synthetic OOD generation tailored to generative-artifact shifts (e.g., frequency/noise fingerprints or GAN/diffusion-synthesized outliers) rather than generic blur/JPEG corruptions is needed for robust generator-level OOD detection.
- [GAP-ready: supported by P0029] Attention-map OOD detection needs artifact-aware or frequency-guided representations so Vision Transformers do not collapse on semantically heterogeneous deepfake benchmarks.
- [GAP-ready: supported by P0029] Joint evaluation of OOD detection (AUROC/FPR95) and probability calibration (ECE/BS) for deepfake forensics remains under-explored.

## Future Work
- Designing new OOD synthesis techniques (GAN-generated OOD images, salt-and-pepper/speckle noise, multi-frequency filtered images) and new auxiliary signals such as noise fingerprints (Section 6, p. 9).
- Extending the ID module from binary classification to multi-class source/technique attribution, higher-resolution inputs, and multimodal deepfakes (Section 6, p. 9).

## Interesting Ideas
- Feeding `(Softmax probs, latent encoding, squared reconstruction residual)` into a compact risk-scoring Abnormality MLP cleanly decouples real/fake classification from OOD/novelty detection.
- Downsampling the reconstruction residual and projecting encoding + residual to equal low-dimensional vectors (10-D in `V3`) prevents high-dimensional spatial tensors from drowning out the 2-D Softmax signal.
- Attention-map reconstruction via VAE provides a natural bridge between spatial explainability (`MOD010`) and OOD anomaly scoring (`MOD008`/`MOD009`).

## Possible Reuse
- **AI Forensic Analyst `MOD008` (Decision Engine) & `MOD009` (Confidence Estimation):** An Abnormality-style OOD risk score can trigger the `Unknown` or `Inconclusive` decision path in `MOD008` and discount `prediction_confidence` / `decision_confidence` in `MOD009` when an image lies outside the detector's training distribution.
- **AI Forensic Analyst `MOD010` (Explainability) & `MOD004` (Deep Learning Specialist):** Attention-map or input reconstruction residuals can serve as an auxiliary `explainability_input` / anomaly signal alongside `grad_cam` and `attention_maps`.
- **Evaluation Benchmark Design:** The CDDB Content / Group (GAN vs. non-GAN) / Mix OOD partitioning strategy can inspire open-set evaluation splits on our thesis datasets (GAN vs. Diffusion generalization).

## Questions
- How does `V2S` / `V3S` behave when legitimate ID deepfakes undergo standard social-media JPEG compression (e.g., c40 or QF 50–70), given that JPEG-10% is used to synthesize OOD training samples?
- Can replacing raw spatial/attention residuals with spectral residuals (like P0003) or SRM high-frequency residuals (like P0030) resolve the Transformer failure on the Group and Mix OOD scenarios?
- Does the Abnormality Module's OOD risk score correlate with calibration error (ECE/BS) or epistemic uncertainty?

## Connections
- Directly complements **P0030** (uncertainty calibration via Packed-Ensembles): P0029 focuses on explicit OOD flagging (`ID vs. OOD`), whereas P0030 calibrates predictive probabilities (`ECE`, `BS`) under distribution shift and unseen datasets.
- Relates to **P0006** (diffusion reconstruction error): both leverage reconstruction residuals to detect unfamiliar/synthetic faces, though P0029 applies AE/VAE reconstruction to images and ViT attention maps for OOD detection.
- Relates to **P0018** (hierarchical GAN vs. DM detection and attribution) and **P0021** (patch-wise ViT multiclass detection): P0029 explicitly evaluates GAN vs. non-GAN/unknown OOD splits (Group scenario) and notes multi-class attribution as future work.
- Relates to **P0007** and **P0016** (cross-dataset/cross-generator generalization and bias): P0029's CDDB Group/Mix failure for ViT highlights the same semantic/dataset-bias vulnerability identified in P0016 and P0007.
- Relates to **P0003** and **P0010** (frequency-domain residuals): P0029 explicitly suggests noise fingerprints and frequency-filtered auxiliary inputs as future work to overcome spatial/semantic limitations.
