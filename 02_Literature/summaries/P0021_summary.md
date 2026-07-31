# Paper Summary: P0021

## Metadata
- **Paper ID:** P0021
- **Title:** Multiclass AI-Generated Deepfake Face Detection Using Patch-Wise Deep Learning Model
- **Authors:** Muhammad Asad Arshed, Shahzad Mumtaz, Muhammad Ibrahim, Christine Dewi, Muhammad Tanveer, Saeed Ahmed
- **Year:** 2024
- **Venue:** Computers, MDPI
- **DOI:** 10.3390/computers13010031

## Problem
Most deepfake detectors treat detection as a binary problem (real vs. fake), which fails to capture the nuances of different generative frameworks. A multiclass approach that distinguishes between real images and images from different generator types (GAN, diffusion model) provides more forensically useful information.

## Motivation
Different generative frameworks (GANs vs. diffusion models) produce images with distinct artifact profiles. A multiclass classifier that can differentiate between these categories provides richer forensic output and better supports source attribution, which is critical for forensic investigations.

## Method
**Multiclass classification** using a Vision Transformer (ViT) with **patch-wise processing**. The image is divided into patches, and the ViT processes these patches to extract global features for classification into 4 classes: Real, GAN_Fake, Stable&GAN_Fake, Diffusion_Fake.

## Architecture
- **Vision Transformer (ViT)** as the primary architecture.
- **Patch-wise processing:** Images divided into fixed-size patches fed as token sequences to the transformer.
- Compared against CNN baselines: **VGG-16** and **ResNet-50**.
- ViT demonstrates superior performance over CNN baselines.

## Dataset
- Custom multiclass dataset: **28,802 training + 7,198 validation images**.
- Sources: Kaggle (existing face datasets), Stable Diffusion (generated), StyleGAN2 (generated).
- 4 classes: Real, GAN_Fake, Stable&GAN_Fake, Diffusion_Fake.
- Dataset is publicly available.

## Training
- Standard supervised training with cross-entropy loss for 4-class classification.
- ViT fine-tuned on the custom multiclass dataset.
- Comparison training with VGG-16 and ResNet-50 under same conditions.

## Evaluation
- Multiclass classification metrics: accuracy, precision, recall, F1 score.
- Comparison across ViT, VGG-16, and ResNet-50 architectures.
- Per-class performance analysis.

## Results
- **ViT achieves 99.90% F1 score** on the multiclass task.
- ViT outperforms both VGG-16 and ResNet-50.
- Successfully distinguishes between GAN and diffusion-generated fakes.
- Patch-wise processing effectively captures generator-specific artifacts.

## Strengths
- **Multiclass formulation** directly addresses GAN vs. diffusion distinction.
- **ViT architecture** demonstrates Transformer superiority for this task.
- **Patch-wise processing** aligns with ViT's natural tokenization.
- **Very high F1 score** (99.90%) demonstrates effectiveness.
- **Dataset publicly available**.

## Weaknesses
- [GAP-ready: supported by P0021] **Custom dataset may have bias** — relatively small (36K images) and may contain shortcuts similar to those identified in P0016.
- [GAP-ready: supported by P0021] **Limited generator diversity** — only StyleGAN2 and Stable Diffusion represented; more generators needed.
- [GAP-ready: supported by P0021] **No cross-dataset evaluation** — all training and testing on the same custom dataset.
- [GAP-ready: supported by P0021] **Single ViT architecture** — no comparison with other transformer variants or recent architectures.
- [GAP-ready: supported by P0021] **No explainability analysis** — attention maps not analyzed to understand what the ViT learns.
- [GAP-ready: supported by P0021] **Mixed class label ("Stable&GAN_Fake")** is semantically unclear.

## Research Gap
- [GAP-ready: supported by P0021] Multiclass deepfake detection with diverse generators across both GAN and DM families is under-explored.
- [GAP-ready: supported by P0021] Cross-dataset generalization of multiclass detectors is not studied.
- [GAP-ready: supported by P0021] ViT attention analysis for understanding forensic features in deepfake detection is missing.

## Future Work
- More generators for broader multiclass taxonomy.
- Cross-dataset evaluation.
- Ensemble approaches combining ViT with other architectures.
- Explainability via attention visualization.

## Interesting Ideas
- Multiclass formulation mirrors our forensic analyst's need for nuanced classification beyond binary.
- ViT's patch-wise processing may naturally capture different artifacts at different spatial scales.
- The 99.90% F1 score may indicate dataset bias (cf. P0016's 85% zero-learning finding).

## Possible Reuse
- **ViT as candidate architecture** for our detection model.
- **Multiclass formulation** aligns with our forensic system's classification needs.
- **Benchmark comparison** — our system should outperform or match this baseline on comparable data.

## Questions
- Would the 99.90% hold under cross-dataset evaluation?
- Does the ViT exploit dataset-specific bias or learn genuine forensic features?
- What do the ViT attention maps reveal about which image regions drive classification?

## Connections
- Relates to **P0018** (both address GAN+DM classification, but different architectures: ViT vs. ResNet).
- Relates to **P0007** (ViT is among architectures evaluated; generalization concern applies).
- Relates to **P0016** (bias concerns about high accuracy on custom datasets).
- Relates to **P0025** (StyleGAN survey provides context for the GAN generator used).
