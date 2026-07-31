# Literature Review: AI-Generated Face Detection and Digital Forensics

> **Document Type:** Living Literature Review (Phase L11–L12)
> **Version:** 1.0
> **Status:** Draft
> **Last Updated:** 2026-07-31
> **Incremental Update Rule:** When a new paper is registered, update only the affected sections. Record the change in the version history below. Every paragraph must trace to P IDs, CLAIM IDs, or GAP IDs.

## Version History

| Version | Date | Sections Updated | Trigger |
|---|---|---|---|
| 1.0 | 2026-07-31 | All (initial draft) | STEP-017 initial generation from P0001–P0028 |

---

## 1. Introduction

The proliferation of generative artificial intelligence models capable of synthesizing photorealistic human faces has created an urgent need for reliable forensic detection systems. Two dominant generative paradigms have emerged: Generative Adversarial Networks (GANs), which learn to generate images through adversarial training between a generator and discriminator [P0005, P0010, P0025], and Diffusion Models, which generate images through iterative denoising of Gaussian noise [P0003, P0006, P0023]. Both paradigms now produce faces that deceive human observers with high frequency, with existing automated detectors achieving binary accuracy below 30% on diffusion-generated faces in controlled benchmarks [P0023].

The research landscape reveals a field in rapid transition. Early detection methods focused exclusively on GAN-generated content [P0005, P0010, P0014], exploiting architecture-specific artifacts such as transposed convolution traces [P0005] and discrete cosine transform (DCT) anomalies [P0010]. The emergence of diffusion models has invalidated many assumptions underlying these methods, as diffusion models employ fundamentally different generation processes that leave distinct artifact signatures [P0003, P0018, P0023]. This paradigm shift has exposed critical gaps: cross-generator generalization remains unsolved (GAP0001, supported by 11 papers), explainable forensic analysis is largely absent (GAP0003, supported by 9 papers), and benchmark datasets contain pervasive biases that inflate reported performance (GAP0002, supported by 6 papers) [CLAIM0003, P0016].

This review synthesizes findings from 28 papers spanning 2020 to 2026, organized around four thematic axes: detection methods, generalization challenges, explainability and forensic analysis, and robustness. It identifies eight research gaps and establishes the evidence base for the chosen research direction: an evidence-driven forensic analysis system for cross-generator synthetic face detection.

---

## 2. Detection Methods for AI-Generated Faces

### 2.1 Frequency-Domain Methods

Frequency-domain analysis exploits spectral artifacts introduced during image generation. Bammey [P0003] demonstrated that diffusion models introduce periodic high-frequency patterns detectable through Fourier analysis of high-pass filtered residuals. The Synthbuster method operates without deep learning, relying entirely on signal processing (high-pass filtering followed by FFT peak detection), achieving detection across nine diffusion models while providing fully interpretable spectral evidence [P0003]. This training-free approach eliminates the dataset bias concerns identified by Altamimi et al. [P0016] (CLAIM0003).

Giudice et al. [P0010] established that GAN-generated images exhibit anomalous DCT coefficient distributions distinguishable through beta statistics, providing a lightweight, interpretable detection method. Their approach successfully detected multiple GAN architectures but has not been validated on diffusion-generated content [P0010]. The complementarity between FFT-based diffusion detection [P0003] and DCT-based GAN detection [P0010] suggests that multi-band frequency analysis could serve as a generator-agnostic evidence source, but this integration remains unexplored (GAP0007) [CLAIM0002].

Both frequency-domain methods share a critical limitation: robustness degrades under lossy JPEG compression and aggressive resizing [P0003, P0010, P0013] (CLAIM0006). Social media platforms routinely apply such transformations, limiting the practical deployment of purely frequency-based approaches [P0010, P0018].

### 2.2 Spatial-Domain and Deep Learning Methods

Convolutional neural network (CNN) architectures dominate the detection literature. Khan and Dang-Nguyen [P0007] conducted the most comprehensive generalization study to date, evaluating eight supervised CNN architectures and two transformer-based models (DINO, CLIP) across four major benchmarks (FaceForensics++, CelebDF-V2, DFDC, FakeAVCeleb). Their findings established that intra-dataset accuracy routinely exceeds 95%, but cross-dataset accuracy can drop to 60–70% [P0007] (CLAIM0001). Transformer-based architectures generally outperform CNNs in cross-dataset settings, and self-supervised pre-training (DINO, CLIP) provides more robust feature representations [P0007] (CLAIM0007).

Guarnera et al. [P0005] introduced an Expectation-Maximization approach to extract GAN-specific convolutional traces from transposed convolution operations. This white-box method provides interpretable forensic evidence of the generation process and supports source attribution to specific GAN architectures [P0005]. However, diffusion models do not use transposed convolution, making this approach inapplicable to the diffusion paradigm [P0005].

Arshed et al. [P0021] applied Vision Transformers (ViTs) with patch-wise processing for multiclass deepfake detection, distinguishing between real, GAN-generated, and diffusion-generated faces with 99.9% F1 score on their custom dataset [P0021]. However, the limited generator diversity (only StyleGAN2 and Stable Diffusion) and absence of cross-dataset evaluation raise concerns about generalizability (CLAIM0007) [P0021].

Comparative studies demonstrate that architecture choice alone does not solve the generalization problem. Altamimi et al. [P0016] found that EfficientNet-B4 accuracy dropped to 86.75% on diffusion-generated faces without bias-aware training, suggesting that diffusion-model detection is inherently harder than GAN detection (CLAIM0001). Simpler architectures like VGG19 and DenseNet-121 achieve approximately 95% accuracy but only on small, non-diverse datasets [P0002], while hybrid GAN-ResNet approaches show similar limitations with very small datasets of 2,041 images [P0011].

### 2.3 Hierarchical and Multi-Level Approaches

Guarnera et al. [P0018] proposed the most sophisticated detection paradigm: a hierarchical multi-level pipeline using ResNet-101, progressing from binary detection (real vs. fake) to paradigm classification (GAN vs. diffusion) to specific architecture attribution. This approach achieved over 97% accuracy across all levels on a custom dataset of 83,000 images covering nine GAN and four diffusion architectures [P0018] (CLAIM0004). The hierarchical decomposition yielded approximately 2% improvement over flat multiclass approaches [P0018].

The hierarchical paradigm mirrors real forensic investigation workflows and is directly applicable to the AI Forensic Analyst design. However, several limitations constrain its current form: the training dataset is proprietary [P0018], no cross-dataset evaluation was reported [P0018], and cascading errors propagate across levels [P0018]. Additionally, the method provides limited explainability, classifying the paradigm (GAN vs. DM) but not explaining the specific forensic evidence supporting the classification [P0018].

### 2.4 Alternative Detection Paradigms

Several less-explored approaches offer complementary capabilities. Zeng et al. [P0006] proposed using diffusion reconstruction error as a diagnostic feature for diffusion-generated images, exploiting the observation that diffusion models can more accurately reconstruct images they generated (CLAIM0008). This approach introduces high inference latency that limits real-time application [P0006].

Xue et al. [P0015] developed GLFNet, a dual-branch architecture fusing local iris and pupil analysis with global residual feature extraction. The physiological evidence from biometric analysis (iris symmetry, pupil shape) provides domain-agnostic forensic evidence (CLAIM0005), though advanced generators increasingly produce flawless biometric features [P0025, P0015].

Pasquini et al. [P0008] combined GAN inversion with biometric trait analysis for synthetic face detection, using physiological inconsistencies as forensic indicators [P0008]. Both biometric approaches [P0008, P0015] are limited to GAN-generated faces and have not been validated on diffusion-generated content.

Proactive approaches such as GAN-based visible watermarking [P0020] represent a fundamentally different paradigm requiring cooperation from content creators. While relevant to future content authentication ecosystems, watermarking is not applicable to the reactive forensic detection problem addressed in this research [P0020].

---

## 3. The Cross-Generator Generalization Challenge

Cross-generator generalization is the most critical unsolved problem in AI-generated face detection (GAP0001), supported by 11 of the 28 reviewed papers [P0003, P0005, P0006, P0007, P0010, P0016, P0018, P0021, P0023, P0024, P0028]. Deep learning classifiers trained on GAN-generated faces experience severe performance degradation when evaluated on diffusion-generated images (CLAIM0001, supported by P0003, P0007, P0016, P0018, P0023).

The challenge has two dimensions. First, **intra-paradigm generalization** requires detectors to handle unseen architectures within the same generation paradigm (e.g., detecting StyleGAN3 images when trained on StyleGAN2). Khan and Dang-Nguyen [P0007] demonstrated significant performance drops even within this setting across four GAN-era benchmarks. Second, **cross-paradigm generalization** requires detectors to handle the fundamentally different artifact signatures of GANs and diffusion models. Cheng et al. [P0023] quantified this gap, showing that existing GAN-era detectors achieve below 30% binary accuracy on diffusion-generated faces from their DiFF benchmark.

Three factors exacerbate the generalization problem:

1. **Dataset bias.** Altamimi et al. [P0016] demonstrated that a zero-learning statistical audit, using only simple photometric features with no model training, achieved 85% detection accuracy on a standard benchmark (CLAIM0003). This finding indicates that published detection accuracies are systematically inflated by dataset-specific shortcuts (background noise patterns, color distributions, compression differences) rather than genuine forensic feature learning [P0016, P0007, P0021, P0023].

2. **Architecture-specific artifacts.** GAN artifacts (transposed convolution traces [P0005], DCT anomalies [P0010]) are structurally different from diffusion artifacts (iterative denoising residuals [P0003], reconstruction error signatures [P0006]). No single feature type captures both [P0003, P0005, P0010, P0022] (GAP0007).

3. **Post-processing degradation.** Lossy JPEG compression and social media re-encoding significantly degrade all detected forensic artifacts (CLAIM0006), with spatial-domain gradient architectures demonstrating slightly greater compression robustness than pure spectral detectors [P0018, P0003, P0010, P0013] (GAP0004).

---

## 4. Explainability and Forensic Analysis

Explainability in AI-generated face detection remains predominantly limited to post-hoc visualization (GAP0003, supported by 9 papers). Altamimi et al. [P0016] applied Grad-CAM to reveal that without bias-aware training, detection models attend to dataset-specific artifacts (backgrounds, borders) rather than semantically meaningful facial features. This finding underscores the need for detection systems that not only classify but also explain the forensic evidence supporting each conclusion.

Three levels of explainability exist in the current literature:

1. **Inherently interpretable methods.** Frequency-domain approaches [P0003, P0010] provide fully interpretable evidence: spectral peaks (Synthbuster [P0003]) and DCT coefficient anomalies [P0010] can be visually inspected and traced to physical generation artifacts. The convolutional trace method of Guarnera et al. [P0005] similarly produces white-box evidence of GAN generation processes.

2. **Partially interpretable methods.** Hierarchical classification [P0018] provides structural interpretability by distinguishing the generation paradigm (GAN vs. DM) and specific architecture. Biometric analysis approaches [P0008, P0015] produce physiological explanations (e.g., iris asymmetry, pupil shape irregularities). Reconstruction error features [P0006] provide partial interpretability through the error magnitude.

3. **Black-box methods.** The majority of CNN and ViT-based detection methods [P0002, P0007, P0011, P0021] provide no inherent explainability. Post-hoc methods such as Grad-CAM [P0016] can be applied but do not guarantee that the model's actual decision process is faithfully represented.

No existing work combines multiple independent evidence types into a unified forensic analysis system with calibrated confidence and automated forensic reporting (GAP0003). Individual evidence types exist (spatial CNN features, spectral anomalies, biometric inconsistencies, model attribution signals), but their systematic fusion, cross-validation, and presentation in reproducible forensic reports remains unexplored.

---

## 5. Robustness and Adversarial Considerations

Robustness to real-world perturbations is critical for practical deployment. Lossy JPEG compression and social media re-encoding significantly degrade detector accuracy by suppressing high-frequency forensic artifacts (CLAIM0006, supported by P0003, P0005, P0010, P0013, P0018). Spatial-domain gradient architectures demonstrate slightly greater compression robustness than pure spectral detectors [P0018], but no method achieves reliable detection under aggressive compression.

Sharma et al. [P0013] proposed ensemble methods specifically targeting robustness on social media platforms, combining multiple classifiers for more resilient detection [P0013]. The approach shows promise but remains limited to GAN-generated images [P0013].

Adversarial robustness presents an additional challenge. Alkishri et al. [P0019] evaluated whether GAN fingerprints can be deliberately removed to fool detectors, demonstrating that anti-forensic attacks pose a real threat (GAP0006). Defense mechanisms against such attacks remain under-developed [P0019, P0008].

The combination of compression sensitivity and anti-forensic vulnerability suggests that no single detection feature type is sufficient. Robust forensic analysis requires fusing multiple independent evidence streams, each with different failure modes, so that the system degrades gracefully rather than failing catastrophically when any individual evidence type is compromised (GAP0004, GAP0007).

---

## 6. Datasets and Benchmarks

The dataset landscape reveals both progress and persistent problems. Major benchmarks include:

- **FaceForensics++** [used by P0007, P0014]: Multiple face manipulation methods; widely used but limited to face swap and reenactment (GAN-era manipulations only).
- **CelebDF-V2** [used by P0007]: High-quality celebrity face swaps; moderate difficulty.
- **DFDC** [used by P0007]: Large-scale diverse manipulations; challenging but GAN-era only.
- **DiFF** [P0023]: Over 500,000 images from 13 diffusion generation methods across 4 conditions (text-to-image, image-to-image, inpainting, face swap); publicly available.
- **Synthbuster** [P0003]: 9,000 synthetic images from 9 diffusion models with RAISE-1k real images; publicly available.
- **AI-Face-FairnessBench** [P0016]: Million-scale, demographically annotated; covers both GAN and diffusion.

A critical gap exists in publicly available, large-scale datasets covering both GAN and diffusion generators within a single unified benchmark [P0018, P0023]. The most comprehensive cross-paradigm study [P0018] used a proprietary 83,000-image dataset, limiting reproducibility. The DiFF dataset [P0023] fills the diffusion gap but excludes GAN-generated faces. No single public benchmark enables fair, unified evaluation across both paradigms.

---

## 7. Surveys and Taxonomies

Four survey papers in the collection provide field-wide context. Heidari et al. [P0024] produced the highest-cited systematic review (285 citations), covering CNN, RNN, GAN, Transformer, and Hybrid detection approaches across image and video modalities. Malik et al. [P0028] (254 citations) provided comprehensive coverage of image and video detection methods, though both surveys predate the diffusion era. Gragnaniello et al. [P0022] offered a focused survey of synthetic face detection methods with a taxonomy of CNN-based, frequency-domain, and spatial-domain approaches. Edwards et al. [P0026] and Dang and Nguyen [P0027] contributed more recent but overlapping reviews.

A comprehensive, up-to-date survey bridging legacy GAN detection literature and emerging diffusion model detection paradigms is still needed (GAP0008, supported by 5 papers) [P0022, P0024, P0026, P0027, P0028]. Melnik et al. [P0025] provided a focused StyleGAN generation survey useful for understanding the adversary's capabilities.

---

## 8. Research Gaps and Open Challenges

The literature analysis identifies eight research gaps, ranked by importance and frequency:

| Gap ID | Category | Importance | Supporting Papers | Frequency |
|---|---|---|---|---|
| GAP0001 | Cross-Generator Generalization | Critical | P0003, P0005, P0006, P0007, P0010, P0016, P0018, P0021, P0023, P0024, P0028 | 11 |
| GAP0003 | Explainability and Forensic Analysis | Critical | P0003, P0005, P0008, P0010, P0015, P0016, P0019, P0020, P0022 | 9 |
| GAP0002 | Benchmark and Dataset Integrity | High | P0002, P0007, P0011, P0016, P0021, P0023 | 6 |
| GAP0004 | Robustness and Anti-Forensics | High | P0003, P0005, P0010, P0013, P0016, P0018 | 6 |
| GAP0007 | Architecture and Feature Fusion | High | P0003, P0005, P0010, P0015, P0022 | 5 |
| GAP0008 | Literature Synthesis | Medium | P0022, P0024, P0026, P0027, P0028 | 5 |
| GAP0005 | Source Attribution and Fine-Grained Forensics | High | P0018, P0021, P0023 | 3 |
| GAP0006 | Adversarial Robustness and Anti-Forensics | Medium | P0008, P0019 | 2 |

The two critical gaps (GAP0001 and GAP0003) jointly motivate the research direction: an evidence-driven forensic analysis system that fuses multiple independent evidence streams (addressing GAP0001 through complementary generalization) and produces explainable, calibrated forensic reports (addressing GAP0003 through systematic evidence presentation).

---

## 9. Conclusion and Research Direction Alignment

The literature establishes that: (1) no single detection method generalizes reliably across both GAN and diffusion paradigms (CLAIM0001); (2) frequency-domain and spatial-domain methods capture complementary artifacts with different robustness profiles (CLAIM0002, CLAIM0006); (3) dataset biases systematically inflate reported performance (CLAIM0003); and (4) explainable forensic analysis is absent from current systems (GAP0003).

The chosen research direction, the Evidence-Driven Forensic Analysis System, addresses these challenges by treating each detection approach as an independent evidence collector within a modular forensic system. Frequency-domain analysis [P0003, P0010], deep learning classification [P0007, P0018], and biometric analysis [P0008, P0015] become evidence streams that are independently validated, fused with calibrated confidence, and presented in reproducible forensic reports. This system-level contribution is novel: no existing work combines multiple independent evidence collectors with validation, fusion, confidence calibration, and forensic reporting for synthetic face detection.

---

## References

All citations use the canonical Paper ID scheme (P0001–P0028). Full bibliographic details are in `02_Literature/metadata/papers.csv` and `02_Literature/metadata/papers.bib`.
