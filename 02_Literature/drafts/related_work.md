# Related Work: AI-Generated Face Detection

> **Document Type:** Living Related Work Section (Phase L12)
> **Version:** 1.0
> **Status:** Draft
> **Last Updated:** 2026-07-31
> **Incremental Update Rule:** When a new paper is registered, update only the affected subsection. Record changes in the version history.

## Version History

| Version | Date | Sections Updated | Trigger |
|---|---|---|---|
| 1.0 | 2026-07-31 | All (initial draft) | STEP-017 initial generation from P0001–P0028 |

---

## 1. GAN-Based Face Generation and Detection

The detection of GAN-generated faces has been studied extensively since the widespread adoption of architectures such as StyleGAN, StyleGAN2, and ProGAN. Melnik et al. [P0025] surveyed the StyleGAN family, documenting the progressive improvement in generation quality that has made detection increasingly challenging. Early comparative studies, such as Taeb and Chi [P0002], evaluated CNN architectures (VGG19, DenseNet-121) on small-scale datasets, achieving approximately 95% accuracy but without cross-dataset evaluation or generalization analysis [P0002].

Guarnera et al. [P0005] introduced a foundational approach to GAN detection through convolutional trace extraction using an Expectation-Maximization (EM) algorithm. Their work demonstrated that transposed convolution operations in GANs leave architecture-specific fingerprints that enable both detection and source attribution across five GAN architectures [P0005]. Building on this, Giudice et al. [P0010] proposed DCT-based frequency anomaly detection using beta statistics, providing a lightweight, interpretable method that operates without deep learning [P0010]. Both methods, from the same research group (Guarnera, Giudice, Battiato), established the principle that GAN artifacts are generator-specific and detectable through either spatial or frequency domain analysis [P0005, P0010].

Hybrid approaches have also been explored. Safwat et al. [P0011] proposed a GAN-ResNet hybrid model, but evaluation on only 2,041 images severely limits the generalizability of their conclusions [P0011]. Xue et al. [P0015] developed GLFNet, a dual-branch architecture fusing local iris/pupil analysis with global residual features, demonstrating that physiological evidence provides an alternative detection modality [P0015] (CLAIM0005). The Face Deepfake Detection Challenge [P0014] provided a multi-method benchmark, but its fixed GAN architecture set does not extend to diffusion-generated content [P0014].

## 2. Diffusion Model Detection

The emergence of diffusion models (Stable Diffusion, DALL-E, Midjourney) has fundamentally shifted the detection landscape. Bammey [P0003] proposed Synthbuster, a spectral analysis method detecting periodic high-frequency patterns introduced by the iterative denoising process, evaluated across nine diffusion models. The training-free nature of this approach eliminates the dataset bias concerns identified in supervised methods (CLAIM0003) [P0003, P0016].

Cheng et al. [P0023] introduced the DiFF benchmark, containing over 500,000 images from 13 diffusion generation methods across four conditions (text-to-image, image-to-image, inpainting, face swap). Their key finding was that existing GAN-era detectors achieve below 30% binary accuracy on DiFF, quantifying the severity of the cross-paradigm generalization challenge (CLAIM0001) [P0023]. Their proposed edge graph regularization approach improved detection over baselines but absolute accuracy on the most challenging conditions remained relatively low [P0023].

Zeng et al. [P0006] proposed using diffusion reconstruction error as a diagnostic feature, exploiting the observation that diffusion models more accurately reconstruct images they generated [P0006] (CLAIM0008). While novel, the approach introduces high inference latency and has limited validation.

## 3. Cross-Generator Generalization

Cross-generator generalization represents the most critical challenge in the field (GAP0001). Khan and Dang-Nguyen [P0007] conducted a systematic comparison of 10 architectures across four benchmarks, demonstrating that even state-of-the-art models suffer significant performance degradation in cross-dataset settings: intra-dataset accuracy exceeding 95% drops to 60–70% cross-dataset [P0007]. Their analysis revealed that training dataset selection affects generalization more than architecture choice, and self-supervised pre-training (DINO, CLIP) provides more robust representations than purely supervised training [P0007] (CLAIM0007).

Guarnera et al. [P0018] addressed cross-paradigm generalization through a hierarchical multi-level pipeline achieving over 97% accuracy across nine GAN and four diffusion architectures [P0018] (CLAIM0004). However, the proprietary dataset limits reproducibility, and no cross-dataset evaluation was reported [P0018].

Altamimi et al. [P0016] exposed a fundamental confound in generalization studies: a zero-learning statistical audit, using simple photometric features with no model training, achieved 85% detection accuracy, demonstrating that benchmark datasets contain pervasive biases (CLAIM0003) [P0016]. Their Grad-CAM analysis revealed that without bias-aware training, models attend to dataset artifacts rather than forensic features [P0016].

## 4. Explainability and Evidence-Based Forensics

Explainability in deepfake detection has received limited systematic attention (GAP0003). Three categories of explainability exist in the reviewed literature:

**Inherently interpretable methods** include spectral analysis (Synthbuster [P0003], DCT anomalies [P0010]) and convolutional trace extraction [P0005], where detection features are physically meaningful and visually inspectable.

**Post-hoc explainability** has been applied through Grad-CAM attention analysis [P0016], revealing model focus regions. While informative, post-hoc methods do not guarantee faithful representation of the model's decision process.

**Physiological evidence** from biometric analysis (iris symmetry, pupil shape [P0008, P0015]) provides domain-agnostic forensic indicators, though advanced generators increasingly produce flawless biometric features (CLAIM0005) [P0025].

No existing work integrates multiple independent evidence types into a unified forensic system with calibrated confidence estimation and automated forensic reporting (GAP0003). The AI Forensic Analyst proposed in this research addresses this gap by treating each detection approach as an evidence collector whose outputs are independently validated, fused, and presented in reproducible forensic reports.

## 5. Robustness to Real-World Perturbations

Lossy JPEG compression and social media re-encoding significantly degrade detection accuracy across all methods (CLAIM0006, supported by P0003, P0005, P0010, P0013, P0018). Spatial-domain gradient architectures demonstrate slightly greater compression robustness than pure spectral detectors [P0018]. Sharma et al. [P0013] proposed ensemble methods targeting social media robustness, but evaluation was limited to GAN-generated content [P0013].

Adversarial anti-forensic attacks pose an additional threat. Alkishri et al. [P0019] demonstrated that GAN fingerprints can be deliberately removed to fool detectors (GAP0006), while Nadimpalli and Rattani [P0020] explored proactive watermarking as a complementary defense. The combination of compression sensitivity and adversarial vulnerability motivates multi-evidence forensic systems where no single point of failure can compromise the overall analysis.

## 6. Comprehensive Surveys

The field has been documented through several systematic reviews. Heidari et al. [P0024] (285 citations) and Malik et al. [P0028] (254 citations) provided comprehensive surveys of deep learning detection methods, though both predate the diffusion era. Gragnaniello et al. [P0022] offered a focused taxonomy of synthetic face detection methods. Edwards et al. [P0026] and Dang and Nguyen [P0027] contributed more recent reviews, but a comprehensive survey bridging legacy GAN detection with diffusion model detection paradigms remains needed (GAP0008).

## 7. Comparison of Detection Methods

A detailed comparison of detection methods, datasets, architectures, and evaluation metrics is provided in the companion comparison table (TAB0001). The comparison covers all 28 reviewed papers and highlights the evaluation dimensions most relevant to cross-generator forensic analysis.

---

## References

All citations use the canonical Paper ID scheme (P0001–P0028). Full bibliographic details are in `02_Literature/metadata/papers.csv` and `02_Literature/metadata/papers.bib`.
