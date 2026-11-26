# Paper Summary: P0043

## Metadata
- **Paper ID:** P0043
- **Title:** Deepfake Media Generation and Detection in the Generative AI Era: A Survey and Outlook
- **Authors:** Florinel Alin Croitoru, Andrei Hiji, Vlad Hondru, Nicolae-Catalin Ristea, Paul Irofti, Marius Popescu, Cristian Rusu, Radu Ionescu, Fahad Khan, Mubarak Shah
- **Year:** 2026
- **Venue:** ACM Computing Surveys (Vol. 58, No. 15, Article 387, November 2026, 35 pages)
- **DOI:** 10.1145/3833867

## Problem
Rapid advances in generative AI (diffusion models, transformers, NeRFs, 3D Gaussian splatting, and modern GANs) have made realistic deepfakes easy to produce across images, video, audio, and multimodal audio-visual streams. Existing surveys are either outdated (omitting diffusion models, vision transformers, NeRFs, and Gaussian splatting) or narrow in scope (covering only generation or detection, or a single modality). Furthermore, existing detection benchmarks are saturated because detectors are typically trained and evaluated on samples from the same set of generators, masking severe generalization failures on unseen modern generative models.

## Motivation
To provide an up-to-date, unified taxonomy and comparative reference covering both deepfake generation and detection across all four media types (image, video, audio, multimodal), update benchmark leaderboards, and rigorously test whether state-of-the-art deepfake detectors generalize to out-of-distribution (OOD) synthetic media produced by recent talking-face, diffusion, NeRF, Gaussian splatting, and neural speech/voice-cloning generators.

## Method
The paper combines a comprehensive survey, a technical tutorial, comparative empirical analyses, and a new OOD evaluation benchmark:
1. **Deepfake categorization (Section 3, Fig. 1):** Defines domain-agnostic and domain-specific deepfake procedures: identity swapping (face swapping / voice conversion), expression/emotion swapping (face reenactment / speech emotion swapping), facial attribute manipulation, talking face synthesis, background swapping, text-to-speech (TTS) synthesis, text-to-image/video generation, and partial synthesis.
2. **Generative tutorial & multi-perspective taxonomy (Section 4, Fig. A1 in supplementary):** Provides mathematical tutorials on GANs, VAEs, Diffusion Models, and NeRFs (Section 4.1), then surveys generation methods organized by modality (image, video, audio, multimodal) and architecture (GANs, diffusion models, transformers, VAEs, NeRFs, 3DMMs, 3D Gaussian splatting, RNNs, CNNs).
3. **Detection taxonomy & multimodal fusion analysis (Section 5, Fig. A2 in supplementary):** Categorizes detection methods across image, video, audio, and multimodal domains by architecture (CNNs, GCNs, Transformers, Hybrid CNN+Transformer/RNN, traditional ML), and classifies 20 multimodal detectors by fusion level: early, middle, or late fusion (Section 5.4.4, Table 3).
4. **Generation speed vs. quality study (Section 4.6, Table 2) & artifact inspection (Fig. 2):** Benchmarks 6 GANs and 6 diffusion models on Celeb-HQ and FFHQ using FID and per-image inference time on an NVIDIA RTX 4090 (24GB VRAM, 50-step sampler for diffusion), alongside visual artifact comparisons from ExDDV [113].
5. **Dataset survey & BioDeepAV OOD benchmark (Sections 6–7, Tables 4–5):** Catalogs 24 widely used datasets across 4 modalities (Table 4) and introduces **BioDeepAV** (Section 7) to test OOD generalization of 7 state-of-the-art detectors trained on FaceForensics++ or FakeAVCeleb using DeepfakeBench [331].

## Architecture
Survey paper with a new benchmark; no new detector architecture is proposed. The paper synthesizes and evaluates the following architectural families:
- **Generation architectures surveyed:** GANs (StyleGAN/2/3/XL, Projected GAN, CycleGAN, StarGAN, SimSwap, BigVGAN), VAEs/CVAE-GAN (NaturalSpeech, YourTTS), Diffusion Models (DDPM, Stable Diffusion, SDXL, GLIDE, DreamBooth, LoRA, PhotoMaker, Arc2Face, InstantID, DiffSwap, AnimateDiff, Latte, Vidu, EchoMimic, AniTalker, Hallo, VASA-1, EMO), Transformers (FastSpeech, VALL-E, VideoGPT, MAGVIT, VideoReTalking), NeRFs (SyncTalk, GeneFace++), and 3D Gaussian Splatting (GaussianTalker).
- **Detection architectures surveyed & evaluated:** CNNs (XceptionNet, EfficientNet, ResNet, F3Net, RECCE, UCF, RawNet2), GCNs/GATs (AASIST, facial-region relation graphs), Transformers (ViT, Swin, wav2vec 2.0, AVFakeNet, MRDF, FRADE), Hybrid CNN+Transformer/RNN (TALL, StA, MARLIN, AVoiD-DF), and Traditional ML (EM convolutional trace extraction + SVM/k-NN, PRNU + SVM).

## Dataset
- **Surveyed Datasets (Section 6, Table 4):** Summarizes 24 benchmarks across Image (DFFD, FakeSpotter, ForgeryNet, DiffusionFace), Video (FaceForensics++, DeeperForensics, Celeb-DF, WildDeepfake, DeepFake-TIMIT, UADFV, GenVideo), Audio (WaveFake, ASVspoof 2019-LA, ASVspoof 2021-LA/DF, In-the-Wild, ADD 2022/2023, FoR, MLAAD), and Audio-Video (FakeAVCeleb, LAV-DF, DFDC, KoDF).
- **Proposed BioDeepAV Benchmark (Section 7):**
  - **Fake data (>1,600 deepfake talking-face videos):** Generated with 4 recent talking-face synthesis methods: EchoMimic [44] (diffusion), AniTalker [193] (diffusion), SyncTalk [232] (NeRF), and GaussianTalker [48] (3D Gaussian Splatting).
  - **Target identities & motion cues:** 300 synthetic faces generated via RealVisXLv5 plus real faces from LAION-Face [372] and HDTF [364]; head motion conditioning from HDTF [364].
  - **Conditioning audio:** English dialects corpus [66], HDTF audio, and >700 self-generated deepfake audio clips using StyleTTS [181], SSR-Speech [294], and YourTTS [30] (prompts/speakers from LibriTTS [353] and target voices from [66]). Includes audio-visual examples with audio-only manipulations.
  - **Real data:** All available videos from HDTF [364] plus 2,000 sampled videos from TalkingHead-1KH [305].
  - Publicly available at `https://github.com/CroitoruAlin/biodeep`.

## Training
Not applicable to the survey component. For the **BioDeepAV** evaluation (Section 7), the 7 evaluated state-of-the-art detectors were not re-trained on BioDeepAV; instead, DeepfakeBench [331] (plus the official MRDF implementation) was used with detectors trained on standard in-domain benchmarks: **UCF, RECCE, TALL, F3Net, StA, and XceptionNet** trained on **FaceForensics++ [289]**, and **MRDF** trained on **FakeAVCeleb [150]**, evaluating zero-shot OOD generalization.

## Evaluation
- **Survey comparison (Section 2, Table 1):** Compares the survey against 12 prior surveys across 18 criteria (tasks, domains, methods, taxonomies, datasets, tutorial, benchmark, blockchain solution).
- **Generative model comparison (Section 4.6, Table 2):** Evaluates FID on Celeb-HQ and FFHQ and average per-image inference time (over 50 images on NVIDIA RTX 4090 24GB VRAM, 50 sampling steps for diffusion) across 6 GANs and 6 diffusion models at resolutions from 256×256 to 1024×1024.
- **Multimodal fusion categorization (Section 5.4.4, Table 3):** Organizes 20 multimodal detectors into early, middle, and late fusion strategies (quantitative fusion results and popular benchmark leaderboards are deferred to Supplementary Sections C and D).
- **BioDeepAV OOD benchmark (Section 7, Table 5):** Evaluates video-level AUC of 7 detectors (3 image-based: UCF, RECCE, XceptionNet; 1 frequency-based: F3Net; 2 video-based: TALL, StA; 1 audio-visual: MRDF) on their original in-domain test sets vs. BioDeepAV (per-generator breakdown deferred to Supplementary Section E).

## Results
- **Generation speed vs. quality (Table 2):** GANs remain substantially faster and achieve lower FID on high-resolution unconditional face synthesis (e.g., StyleGAN-XL [253] at 1024×1024 achieves FFHQ FID 2.02 in 0.0871 s; StyleGAN3 [147] achieves 2.79 in 0.0239 s; StyleGAN2 [146] achieves 2.84 in 0.3474 s), whereas diffusion models are slower (1.1350 s to 11.3865 s per image; e.g., LDM/Stable Diffusion [244] at 256×256 achieves Celeb-HQ FID 5.11 and FFHQ FID 4.98 in 1.1350 s) but offer superior conditional generation capabilities.
- **Multimodal fusion trend (Table 3):** Among 20 multimodal detectors analyzed, late fusion dominates (13 papers, including Salvi et al. [250] which spans early/middle/late), followed by middle fusion (7 papers), and early fusion (2 papers), largely because late fusion preserves modality-specific predictions, interpretability, and resilience to missing modalities.
- **BioDeepAV OOD generalization collapse (Table 5):** All 7 detectors achieve >90% AUC on their original in-domain test sets (FF++ or FakeAVCeleb) but suffer >30% AUC drops on BioDeepAV (falling near random chance):
  - **StA [333]:** 0.9420 (Original) -> **0.6195** (BioDeepAV)
  - **MRDF [379]:** 0.9243 (Original) -> **0.5852** (BioDeepAV)
  - **XceptionNet [289]:** 0.9637 (Original) -> **0.5677** (BioDeepAV)
  - **F3Net [234]:** 0.9449 (Original) -> **0.5010** (BioDeepAV)
  - **RECCE [28]:** 0.9422 (Original) -> **0.5001** (BioDeepAV)
  - **TALL [325]:** 0.9987 (Original) -> **0.4935** (BioDeepAV)
  - **UCF [332]:** 0.9527 (Original) -> **0.4882** (BioDeepAV)

## Strengths
- **Unusually broad and up-to-date scope (2026):** Covers both generation and detection across all 4 modalities (image, video, audio, multimodal), including modern diffusion models, vision transformers, NeRFs, and 3D Gaussian splatting.
- **Actionable empirical contributions:** Goes beyond a pure literature review by benchmarking 12 generative models on Celeb-HQ/FFHQ (Table 2) and releasing the **BioDeepAV** OOD benchmark with DeepfakeBench evaluations (Table 5).
- **Clear taxonomies and artifact synthesis:** Distinguishes 9 deepfake procedures (Fig. 1), catalogs 24 datasets (Table 4), maps generative artifact types (Fig. 2), and systematically analyzes early/middle/late multimodal fusion trade-offs (Table 3).
- **Forward-looking research agenda (Section 8.1):** Highlights under-explored paradigms including one-class anomaly learning, uncertainty-calibrated explainable detection, person-of-interest (POI) verification, and provenance-based multimedia blockchain.
- **Publicly available benchmark and project page:** `https://github.com/CroitoruAlin/biodeep`.

## Weaknesses
- [GAP-ready: supported by P0043] **Severe OOD generalization failure across all tested detectors:** Every evaluated SOTA detector (image, frequency, video, and audio-visual) loses >30% AUC on BioDeepAV (0.4882–0.6195), confirming existing detectors fail on unseen diffusion, NeRF, and 3DGS talking-face generators.
- [GAP-ready: supported by P0043] **Lack of uncertainty calibration and explainability in current detectors (Section 8.1):** Deep neural detectors cannot reliably quantify prediction uncertainty or explain why/when they fail, limiting user trust.
- [GAP-ready: supported by P0043] **Scarcity of POI and one-class detection benchmarks/methods (Section 8.1):** Despite the robustness advantages of person-of-interest matching and one-class anomaly detection, only one POI dataset (FakePoI [280]) is available and unsupervised/one-class methods still lag behind supervised approaches.
- [GAP-ready: supported by P0043] **Key quantitative breakdowns reside in external supplementary material:** Benchmark leaderboard compilations (Section D), fusion performance comparisons (Section C), per-generator BioDeepAV results (Section E), and full taxonomy diagrams (Figs. A1–A2) are omitted from the 35-page main article.
- [GAP-ready: supported by P0043] **Limited evaluation of diffusion-image-specific detectors on BioDeepAV:** The BioDeepAV benchmark evaluates FF++-trained face-forgery detectors and MRDF, rather than recent training-free or diffusion-specific detectors (e.g., AEROBLADE [242], D4 [117]), leaving their talking-face OOD performance untested in Table 5.

## Research Gap
- [GAP-ready: supported by P0043] State-of-the-art detectors trained on legacy benchmarks (FF++, FakeAVCeleb) fail catastrophically (>30% AUC drop) on unseen diffusion, NeRF, and 3D Gaussian splatting talking-face generators.
- [GAP-ready: supported by P0043] Explainable deepfake detection and uncertainty calibration remain severely under-explored, preventing forensic systems from signaling low-confidence or out-of-distribution inputs.
- [GAP-ready: supported by P0043] One-class self-supervised anomaly detection and continual, poisoning-resistant Person-of-Interest (POI) verification need standardized benchmarks and stronger architectures.
- [GAP-ready: supported by P0043] Audio-visual detectors often exploit dataset shortcuts (e.g., Smeu et al. [263]) and require cross-domain evaluation on diverse synthetic voice + talking-face pipelines.

## Future Work
- **Generation safeguarding:** Embed invisible watermarks and usage restrictions in open-source generative models, paired with legal/regulatory frameworks and digital literacy campaigns.
- **Cross-domain and open-set benchmarks:** Continuously update OOD benchmarks like BioDeepAV as generative architectures evolve.
- **One-class learning:** Train multimodal models solely on real samples using self-supervised spatio-temporal pretext tasks (inspired by video anomaly detection) and score discrepancy at inference time.
- **Explainable and calibrated detection:** Develop explainable detectors with uncertainty calibration to flag uncertain predictions.
- **Person-of-interest (POI) detection:** Build POI benchmarks and continual learning methods robust to aging, appearance shifts, and data poisoning.
- **Multimedia blockchain provenance:** Adopt hardware-signed "born verified" media recorded via NFTs on-chain to establish verifiable chain-of-custody, while resolving hardware adoption, privacy, storage/scalability, and governance challenges.

## Interesting Ideas
- **Late fusion vs. early fusion trade-off (Section 5.4.4, Table 3):** Late fusion naturally preserves per-modality evidence, supports interpretability, and degrades gracefully when a modality is absent—directly validating modular forensic evidence pipelines.
- **One-class discrepancy scoring & uncertainty calibration (Section 8.1):** Instead of closed-world binary classification over known fake generators, modeling the distribution of authentic media and calibrating prediction uncertainty directly addresses OOD failure.
- **Explicit generative artifact taxonomy (Fig. 2):** Mouth/teeth anomalies, nose deformations, temporal flickering, eyeglass inconsistencies, and face/neck/hair artifacts provide concrete semantic cues for forensic reasoning modules.

## Possible Reuse
- **AI Forensic Analyst (`MOD007` Evidence Fusion & `MOD018` Modality Registry):** Table 3's early/middle/late fusion taxonomy justifies our late-style evidence fusion architecture (`MOD007`) and guides future audio/video/multimodal extensions under `MOD018`.
- **AI Forensic Analyst (`MOD009` Confidence Calibration, `MOD010` Explainability, `MOD011` Reasoning):** Section 8.1's call for uncertainty-calibrated, explainable detectors directly aligns with `MOD009`'s multi-faceted confidence scoring and `MOD010`/`MOD011`'s evidence-grounded explanations.
- **OOD Evaluation Protocol (`BioDeepAV`):** Useful external OOD benchmark candidate for stress-testing `MOD004` (Deep Learning Specialist) models on modern diffusion/NeRF/3DGS talking-face deepfakes alongside image-level benchmarks.
- **Related Work & Literature Taxonomy:** Provides a 2026 taxonomy (Sections 3–6) for structuring our thesis literature review chapter across generation and detection paradigms.

## Questions
- How do diffusion-specific image detectors (such as `P0003` Synthbuster or AEROBLADE [242]) perform on frames extracted from BioDeepAV's diffusion talking-face videos (EchoMimic, AniTalker) compared to FF++-trained detectors?
- In BioDeepAV, which modality (visual talking-face vs. cloned audio via StyleTTS/YourTTS/SSR-Speech) drives MRDF's 0.5852 AUC drop?
- Can combining frequency-domain, spatial, and uncertainty-calibrated evidence collectors (`MOD003`, `MOD004`, `MOD009`) mitigate the >30% OOD drop reported in Table 5?

## Connections
- Directly updates earlier comprehensive surveys in our corpus: **P0024** (2023), **P0026** (2024), **P0027** (2023), **P0028** (2022), and **P0022** (2022) by incorporating diffusion models, ViTs, NeRFs, 3DGS, audio/multimodal detection, and OOD benchmarking.
- Complements **P0025** (StyleGAN survey) with Table 2's head-to-head FID and inference-speed benchmark of GANs vs. diffusion models on Celeb-HQ and FFHQ.
- Strongly reinforces **P0007** (cross-dataset generalization) and **P0044** (ID test set benchmark): P0043's BioDeepAV confirms that in-domain >90% AUC collapses by >30% on unseen talking-face generators.
- Connects to **P0023** (DiFF diffusion face dataset) and **P0018** (hierarchical GAN+DM classification/attribution) on the need to cover modern diffusion generators.
- Connects to **P0016** (bias, robustness, explainability) and **P0003**/**P0005**/**P0010** (interpretable frequency/trace analysis) via P0043's emphasis on explainable, calibrated detection and dataset shortcut avoidance.
- Relates to **P0020** (proactive watermarking) and **P0004**/**P0012** (blockchain + face recognition) through P0043's Section 8.1 proposals on generation safeguarding and multimedia blockchain provenance.
