# Paper Summary: P0015

## Metadata
- **Paper ID:** P0015
- **Title:** Global–Local Facial Fusion Based GAN Generated Fake Face Detection
- **Authors:** Ziyu Xue, Xiuhua Jiang, Qingtong Liu, Zhaoshan Wei
- **Year:** 2023
- **Venue:** Sensors, MDPI
- **DOI:** 10.3390/s23020616

## Problem
GAN-generated faces contain both global-level artifacts (overall image statistics, residual patterns) and local-level artifacts (physiological inconsistencies in specific facial regions). Single-branch detectors that focus on only one scale miss complementary information.

## Motivation
Combining global and local feature analysis in a dual-branch architecture can capture both image-level statistical artifacts and region-specific physiological anomalies (e.g., iris/pupil inconsistencies), providing richer detection evidence.

## Method
**GLFNet (Global-Local Fusion Network):** A dual-branch architecture:
- **Local branch:** Analyzes iris/pupil regions for physiological inconsistencies (color, shape anomalies in eyes).
- **Global branch:** Extracts residual features using ResNeSt backbone for image-wide GAN artifact detection.
- **Fusion classifier:** Combines both branches for final detection decision.

## Architecture
- Local: Iris/pupil analysis module.
- Global: ResNeSt residual feature extraction.
- Fusion: Combined classification head.

## Dataset
- CelebA (real images), CelebA-HQ (25,000 real + 25,000 fake for training; 2,500 + 2,500 for testing).

## Training
Supervised training of dual-branch architecture on CelebA-HQ.

## Evaluation
Binary detection accuracy on CelebA-HQ test set.

## Results
- Dual-branch fusion outperforms single-branch approaches.
- Local physiological features (iris/pupil) provide meaningful detection signal.
- Global residual features capture GAN-specific artifacts.

## Strengths
- **Dual-branch design** captures multi-scale evidence — directly relevant to our forensic system's multi-evidence philosophy.
- **Physiological analysis** (iris/pupil) provides explainable, semantically meaningful detection features.
- **Complementary evidence fusion** demonstrates the value of combining different feature types.

## Weaknesses
- [GAP-ready: supported by P0015] **Limited dataset diversity** — only CelebA-HQ.
- [GAP-ready: supported by P0015] **GAN-only** — physiological features may not transfer to diffusion models.
- [GAP-ready: supported by P0015] **Iris/pupil analysis requires face alignment and eye region detection** — adds preprocessing complexity.
- [GAP-ready: supported by P0015] **Limited generalization testing**.

## Research Gap
- [GAP-ready: supported by P0015] Multi-scale evidence fusion for deepfake detection is under-explored.
- [GAP-ready: supported by P0015] Physiological anomaly detection for diffusion-generated faces is untested.

## Future Work
Cross-generator testing; diffusion model extension; more physiological features; larger datasets.

## Interesting Ideas
- **Dual-branch fusion** directly maps to our forensic analyst's multi-evidence architecture.
- **Physiological features as evidence** aligns with our evidence collector design (different evidence types fused for final decision).
- The local+global decomposition is applicable to our modular system design.

## Possible Reuse
- **Multi-branch evidence fusion concept** for the forensic analyst.
- **Physiological evidence collector** as a module in our system.
- **CelebA-HQ as benchmark dataset**.

## Questions
Do physiological anomalies (iris/pupil) exist in diffusion-generated faces?

## Connections
- Relates to **P0008** (biometric trait analysis — similar concept of using facial physiology for detection).
- Relates to **P0018** (multi-level approach; P0015's dual-branch is conceptually related).
- Relates to **P0005** (residual feature extraction — global branch uses similar principles).
