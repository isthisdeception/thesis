# Paper Summary: P0031

## Metadata
- **Paper ID:** P0031
- **Title:** Empirical Assessment of Deepfake Detection: Advancing Judicial Evidence Verification Through Artificial Intelligence
- **Authors:** Ebrima Hydara, Masato Kikuchi, Tadachika Ozono
- **Year:** 2024
- **Venue:** IEEE Access (Vol. 12, pp. 151188–151203)
- **DOI:** 10.1109/access.2024.3480320

## Problem
Deepfake technology compromises the authenticity and courtroom admissibility of facial evidence (mugshots, surveillance footage, witness videos) in criminal justice, creating risks of wrongful convictions or exoneration of guilty individuals (Section I-A, I-C). Traditional facial recognition technology (FRT) and face-matching pipelines compare facial traits against police databases without first verifying whether the footage itself was synthetically manipulated (Section II-A, Fig. 1–2). Meanwhile, existing deepfake detectors often lack generalization, frame-level granularity, timestamping, confidence-threshold filtering, and transparent explainability required for legal proceedings and human forensic review (Section II-C).

## Motivation
Judicial workflows demand not only accurate manipulation detection, but also verifiable chain-of-custody documentation, minimization of false positives (to prevent wrongful accusations), elimination of redundant low-certainty evidence, and intuitive visual explanations comprehensible to non-experts such as judges and jurors (Section I-D, I-E). Combining automated Vision Transformer (ViT) frame verification with user-configurable confidence thresholds, chronological timestamps, and spatial heatmaps aims to foster calibrated trust and human-AI collaboration in criminal justice (Section I-C, VI-A).

## Method
A full-stack, user-centric forensic video verification pipeline that inserts a preliminary deepfake authentication stage before suspect face matching (Section II-C, III-D, Fig. 6):
1. **Input Acquisition & Frame Extraction (`ExtractFrames`):** Video evidence is ingested via a web interface and sampled into still frames using OpenCV at consistent intervals (typically 1 frame per second in Section III-D1). A face-recognition module detects human faces so authentication focuses on facial regions (Section IV-A1, Fig. 6–7).
2. **Frame Analysis (`PredictWithViT`):** Each extracted frame is normalized, resized, split into fixed-size patches with positional embeddings, and classified frame-by-frame as real or fake using a pre-trained Vision Transformer (ViT) via global self-attention (Section III-B, III-C2, III-D2). *(Note: Section III-C3 conceptually mentions LSTM and 3D-CNN temporal modeling, though the implemented prototype flow in Sections III-D and IV-A operates per extracted frame with OpenCV + face recognition + ViT).*
3. **Confidence-Threshold Filtering:** Predictions are filtered against an analyst-configurable confidence threshold (validated from 50% to 90%, prototype default set to 80%) so only high-certainty frames trigger downstream flagging, reducing false positives and courtroom redundancy (Section III-D3, IV-B1).
4. **Timestamping & Heatmap Visualization (`GetTimestamp`, `GenerateHeatmap`):** Frames meeting threshold criteria receive time-coded overlays logging exact appearance times and OpenCV-generated color-coded heatmaps highlighting manipulation-salient regions (Section III-D4, IV-B2–B3).
5. **Output Report Compilation:** Produces a labeled output video and structured report combining per-frame predictions, confidence scores, timestamps, and heatmaps (Section III-D5, IV-B4).

## Architecture
- **Core Classifier:** Pre-trained **Vision Transformer (ViT)** with multi-head self-attention, MLP blocks, layer normalization, and residual connections (selected over ResNet and EfficientNet; Section III-A, III-B, Fig. 3). Specific ViT variant (e.g., ViT-B/16) and input patch/pixel dimensions are **Not reported**.
- **Five-Layer Web Application Architecture (Section IV-A, Fig. 7):**
  - *Presentation Layer:* HTML5, CSS3, JavaScript ES6 web UI for video upload and result inspection.
  - *Server Layer:* Python-Django framework handling authentication, session management, request orchestration, and database/model integration.
  - *ViT Model Layer:* GPU + CUDA compute layer running OpenCV frame extraction, face detection, and ViT inference.
  - *Database Layer:* MySQL storing user records, video metadata, and detection logs.
  - *File System Layer:* Dedicated filesystem storage for large uploaded video files.

## Dataset
- **Training & Testing Dataset (Section III-C1, III-C4, Fig. 4):** A curated 1,000-video dataset (500 real, 500 fake) sampled from **Celeb-DF**, **FaceForensics++**, and **Deepfake Detection Challenge (DFDC)**, extracted via OpenCV into **15,000 frames** (7,500 real, 7,500 fake), split 80% training (12,000 frames: 6,000 real, 6,000 fake) and 20% testing (3,000 frames: 1,500 real, 1,500 fake).
- **Confidence-Threshold Assessment Subset (Section V-B):** 102 video frames (42 real, 60 fake).
- **Human-AI Empirical Evaluation Pool (Section V-A1–A2):** 200 videos (authentic and manipulated), from which each of 10 participants evaluated 20 randomly drawn videos.
- **Availability:** Source benchmarks (Celeb-DF, FaceForensics++, DFDC) are public; the curated 1,000-video/15,000-frame subset and code repository links are **Not reported** in the paper.

## Training
- Pre-trained ViT fine-tuned using PyTorch (`ImageFolder` class organization) with frame normalization and uniform resizing on the 80/20 split (12,000 train / 3,000 test frames; Section III-B, III-C3, III-C4).
- Exact optimization hyperparameters (optimizer, learning rate, batch size, epochs, loss function, hardware GPU model) are **Not reported**.

## Evaluation
- **Confidence-Threshold Sweep (Section V-B, Fig. 9):** Accuracy, Precision, Recall, and F1-score measured on 102 frames (42 real, 60 fake) across thresholds from 50% to 90% in 5% increments.
- **Human-AI Collaborative Evaluation (Section V-A, V-C, Table 1, Fig. 10):** 10 novice participants (1 professor aged 45–50, 9 students aged 20–30; origins: Japan, Zimbabwe, Togo, China, Côte d'Ivoire) each evaluated 20 videos out of 200; human perceptions were compared against system predictions using Accuracy, Precision, Recall, and F1-score.
- **User Confidence, Trust & Acceptance Surveys (Section V-D–F, Figs. 11–13):** Likert-scale assessments ("Extremely Confident" to "Not At All Confident") across Accuracy, Precision, Recall, and F1-score, plus a 10-item system acceptance survey (Confidence Threshold, Frame Extraction, Frame Timestamp, Frame Heatmap, Practicality, Relevance, Trust, Approach, Performance, User Friendliness).

## Results
- **Threshold Sensitivity (Section V-B, Fig. 9):**
  - At **50% confidence threshold**, performance was close to random chance and unsuitable for forensic use.
  - System efficacy became pronounced at **>=70%**, achieving peak Accuracy and Precision between **80% and 85%** confidence thresholds (visually ~88–90% accuracy and ~83–88% precision in Fig. 9; exact tabular numbers are **Not reported**).
  - Within the **80%–85%** range, **Recall dropped to 18%** (explicitly reported in Section V-B), illustrating a steep precision–recall trade-off as high thresholds filter out uncertain detections.
  - Prototype demonstration mockup at 80% threshold (Fig. 8) reports frame-level probabilities (89.31%, 80.45%, 88.62%, 88.32%, 96.87% across 1–5 s) and an overall video score of 96.87% Fake.
- **Human-AI Collaboration (Section V-C, Fig. 10):** Automated system accuracy closely aligned with human perception (~87–88% visually in Fig. 10; exact numeric table **Not reported**). Users exhibited higher recall than the system (flagging more videos as deepfakes cautiously) and slightly lower precision, yielding a balanced F1-score compromise.
- **User Trust & Feature Acceptance (Section V-D–F, Figs. 11–13):** High user confidence in system Accuracy and Precision, slightly lower confidence in Recall. **Confidence Threshold**, **Frame Timestamp**, **Practicality**, **Relevance**, **Trust**, **Performance**, and **User Friendliness** received strong positive ratings, whereas **Frame Extraction**, **Frame Heat Map**, and **Approach** received mixed/neutral-to-negative responses, indicating a need to improve heatmap clarity and frame sampling.

## Strengths
- **End-to-end judicial workflow focus:** Explicitly addresses courtroom admissibility, chain-of-custody framing, and pre-FRT authenticity screening rather than isolated benchmark accuracy (Section I-D, II-C).
- **Configurable confidence thresholding & frame-level auditability:** Combines per-frame scoring, 1 fps timestamping, and heatmap overlays in an operational Python-Django prototype (Section III-D, IV-A).
- **Empirical human-AI evaluation:** Measures alignment, trust, confidence, and feature usability with human evaluators rather than relying solely on offline ML metrics (Section V-A–F).

## Weaknesses
- [GAP-ready: supported by P0031] **Severe recall collapse at forensic confidence thresholds:** At the recommended 80%–85% operating threshold used to suppress false positives, recall drops to 18% (Section V-B), risking missed deepfakes in judicial evidence unless mitigated by human review or better calibration.
- [GAP-ready: supported by P0031] **Lack of crime-specific forensic datasets and domain experts:** Trained on general benchmarks (Celeb-DF, FaceForensics++, DFDC) and evaluated with 10 novice academic participants (9 students, 1 professor) rather than trained forensic analysts or real criminal surveillance footage (Section VI-C, Table 1).
- [GAP-ready: supported by P0031] **GAN/video-swap focus without diffusion-model evaluation:** Evaluated on legacy video-deepfake datasets (Celeb-DF, FF++, DFDC) with no testing on modern diffusion-generated faces or counter-forensic post-processing attacks (Section III-C1).
- [GAP-ready: supported by P0031] **Insufficient reproducibility and missing baseline comparisons:** Exact ViT architecture variant, training hyperparameters, OpenCV heatmap generation algorithm, and quantitative comparisons against competing detectors (or tabular per-threshold values) are omitted, and no code/checkpoint repository is released (Section III-C4, V-B).
- [GAP-ready: supported by P0031] **Mixed user reception of heatmaps and frame extraction:** User acceptance results show notable neutral/negative ratings for the frame heatmap and frame extraction features (Section V-F, Fig. 13), indicating that naive frame-level heatmaps may lack forensic clarity.

## Research Gap
- [GAP-ready: supported by P0031] Judicial deepfake verification systems suffer from an uncalibrated precision–recall trade-off (18% recall at 80%–85% confidence thresholds) and need calibrated uncertainty/abstention mechanisms rather than hard threshold filtering alone.
- [GAP-ready: supported by P0031] Explainable heatmap visualizations and frame-sampling policies must be empirically validated for clarity and forensic utility with domain experts, not just novice users.
- [GAP-ready: supported by P0031] Forensic video verification pipelines tested only on Celeb-DF/FF++/DFDC need evaluation against modern diffusion-based manipulations and adversarial/counter-forensic degradations.

## Future Work
- Involve certified forensic examiners and legal professionals in system validation rather than novice participants (Section VI-C).
- Refine frame extraction and heatmap visualizations for higher interpretability and user satisfaction (Section V-F, VII-A).
- Enhance UI intuitiveness, user education programs on AI capabilities/limitations, continuous user-feedback loops, and interdisciplinary collaboration among technologists, legal experts, and policymakers (Section VII-B).

## Interesting Ideas
- **Pre-FRT Deepfake Gate:** Inserting authenticity verification *before* suspect face-matching prevents manipulated footage from poisoning downstream biometric identification (Section II-C).
- **Evidence Redundancy Filtering:** Using configurable confidence thresholds + timestamps to surface only high-confidence manipulated segments aligns directly with courtroom evidentiary standards (Section I-E).
- **Human-AI Calibration Gap:** Human evaluators naturally err toward higher recall (cautious flagging) while tuned ML thresholds favor higher precision, making explicit confidence communication essential (Section V-C, VI-B).

## Possible Reuse
- **MOD001 / MOD013 / MOD014 (Upload, REST API, Investigation UI):** The 5-layer Django + MySQL + filesystem separation and timestamped frame-level inspection UI pattern inform how our AI Forensic Analyst exposes video/image timelines and case records.
- **MOD008 / MOD009 (Decision & Confidence Reporting):** Highlights why raw confidence thresholding (e.g., 80% cutoff causing 18% recall) is risky without calibrated confidence bands and explicit abstention/review states.
- **MOD010 / MOD012 (Explainability & Case Reports):** Motivates clear, analyst-validated spatial heatmaps and timestamped forensic evidence logs in reproducible case reports, while avoiding P0031's vague heatmap usability issues.

## Questions
- Which specific ViT backbone, input resolution, and heatmap computation method (e.g., attention rollout vs. Grad-CAM) were used in the `GenerateHeatmap` and `PredictWithViT` modules?
- How does the ViT detector perform across individual source datasets (Celeb-DF vs. FF++ vs. DFDC) and against unseen diffusion generators or heavy CCTV compression?
- How can calibrated confidence intervals or selective abstention prevent the 18% recall collapse observed at 80%–85% confidence thresholds?

## Connections
- Relates to **P0021** (also uses patch-wise ViT for synthetic face detection, though P0021 performs multiclass GAN/DM attribution while P0031 builds a judicial web prototype on FF++/Celeb-DF/DFDC).
- Complements **P0016** (Grad-CAM explainability analysis for GAN/DM detectors) and **P0032** (provides the calibrated probabilities, abstention/AURC metrics, and attack-aware weak localization missing from P0031's ad-hoc 80% threshold and OpenCV heatmaps).
- Contrasts with **P0007** (evaluates cross-dataset generalization across FF++, CelebDF-v2, DFDC, FakeAVCeleb, whereas P0031 pools Celeb-DF/FF++/DFDC into one 80/20 split without cross-dataset testing).
- Aligns with **P0028** and **P0024** on forensic deployment challenges and explainable AI needs in legal/social settings.
