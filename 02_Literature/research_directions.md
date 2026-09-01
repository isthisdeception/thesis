# Research Direction Candidates

> **Phase L10 — Research Direction Selection**
> The AI proposes; the human decides. This document is produced by the Research Planning Agent. The human must select the final direction and record the choice in `DEC0003.md`.
>
> **Handbook References:** [Phase L10](../MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l10--research-direction-selection); [§1.9 Human-in-the-Loop](../MASTER_RESEARCH_OPERATING_SYSTEM.md#19-human-in-the-loop-rule); [§1.2 Project Identity](../MASTER_RESEARCH_OPERATING_SYSTEM.md#12-project-identity).

---

## Grounding Summary

| Source | Count | Key Insight |
|---|---|---|
| Reviewed Papers | 28 (P0001–P0028) | 4 critical, 8 high, 9 medium, 7 low relevance |
| Research Gaps | 8 (GAP0001–GAP0008) | 2 Critical, 4 High, 2 Medium importance |
| Verified Claims | 8 (CLAIM0001–CLAIM0008) | Cross-validated evidence base |
| Future Work Items | 233 extracted items | Clustered into the 8 gap categories |

### Primary Contribution Constraint (§1.2)

The project's primary scientific contribution is **the AI Forensic Analyst** — an intelligent, evidence-driven forensic *system*, not merely a better classifier. Every candidate direction must demonstrate how it advances the *system-level* contribution (evidence collection, validation, fusion, reasoning, confidence calibration, explainability, forensic reporting) rather than reducing the project to training a single detector.

---

## Candidate Direction 1: Evidence-Driven Forensic Analysis System for Cross-Generator Synthetic Face Detection

**One-line summary:** Build the AI Forensic Analyst as a multi-evidence forensic system that fuses spatial, spectral, and semantic evidence streams to detect synthetic faces regardless of generator architecture (GAN or diffusion).

### Grounding

| Supporting Gaps | GAP0001 (Critical, freq=11), GAP0003 (Critical, freq=9), GAP0007 (High, freq=5) |
|---|---|
| Supporting Claims | CLAIM0001, CLAIM0002, CLAIM0006, CLAIM0007 |
| Key Papers | P0003, P0005, P0007, P0010, P0016, P0018, P0021, P0022, P0023 |

### Evaluation

| Criterion | Assessment |
|---|---|
| **Advantages** | (1) Directly implements the AI Forensic Analyst as the primary contribution. (2) Multi-evidence fusion addresses the critical cross-generator gap (GAP0001). (3) Explainable by design — each evidence stream produces interpretable forensic artifacts (GAP0003). (4) Modular architecture enables future extension to audio/video/text modalities (§1.2). (5) Novel contribution: no existing work combines multiple independent evidence collectors with validation, fusion, confidence calibration, and forensic reporting in a single system for synthetic face detection. |
| **Disadvantages** | (1) High system complexity — requires multiple evidence collectors, a fusion engine, and a report generator. (2) Requires careful interface design to avoid monolithic coupling. (3) Each evidence stream must independently achieve reasonable accuracy before fusion is meaningful. |
| **Complexity** | High — but modular design makes each component independently testable. |
| **Novelty** | **High** — no existing work implements a full forensic analysis pipeline combining multiple independent evidence types with calibrated confidence and automated forensic reporting for synthetic face detection. Individual components exist (frequency analysis, spatial CNN, biometric analysis) but the *system-level integration* is novel. |
| **Publication Potential** | **Very High** — novel system contribution; clear gap in literature; addresses the most-cited limitations across reviewed papers; suitable for top multimedia/forensics venues. |
| **Implementation Difficulty** | High, but mitigated by the modular architecture (each module is a bounded implementation task). FastAI/PyTorch stack (§1.4) supports all components. |
| **Dataset Needs** | Multiple public datasets covering both GAN and diffusion generators: FaceForensics++, CelebDF, DiFF (P0023), Synthbuster (P0003), CelebA-HQ. Addresses DEF-003. |
| **Evaluation Needs** | Cross-generator generalization, per-evidence-stream ablation, fusion strategy comparison, calibration analysis, explainability quality, robustness to compression. Aligns with §7 protocol. |
| **Future Scalability** | **Excellent** — new modalities (audio, video, text) become new evidence collectors plugged into the same fusion and reporting system (§1.2 extensibility). |
| **Alignment with Primary Contribution** | **Perfect** — *this is* the AI Forensic Analyst. |

### Objective Decision Criteria
Choose this direction if: (a) the goal is to maximize the system-level contribution; (b) the human values novelty of the *system design* over novelty of a single detector; (c) the scope of an undergraduate thesis can accommodate multiple interacting modules (each individually small, but integrated).

---

## Candidate Direction 2: Hybrid Spatial-Frequency Feature Fusion for Cross-Generator Deepfake Detection

**One-line summary:** Design a dual-branch neural architecture that fuses CNN/ViT spatial features with multi-band frequency domain representations (FFT/DCT/wavelet) for robust cross-generator synthetic face detection.

### Grounding

| Supporting Gaps | GAP0001 (Critical, freq=11), GAP0007 (High, freq=5), GAP0004 (High, freq=6) |
|---|---|
| Supporting Claims | CLAIM0001, CLAIM0002, CLAIM0006, CLAIM0007 |
| Key Papers | P0003, P0005, P0010, P0015, P0018, P0022 |

### Evaluation

| Criterion | Assessment |
|---|---|
| **Advantages** | (1) Directly addresses the critical cross-generator generalization gap. (2) Frequency-domain features provide inherent interpretability (CLAIM0002). (3) Hybrid approach compensates for each domain's weaknesses (spatial robust to compression per CLAIM0006, frequency captures generation fingerprints per CLAIM0002). (4) Well-grounded in literature (P0003, P0005, P0010, P0022). |
| **Disadvantages** | (1) Reduces the project to a *better detector* — does not build the forensic *system*. (2) Hybrid architectures for deepfake detection already exist (P0015 GLFNet); novelty is incremental. (3) Does not address evidence fusion, confidence calibration, or forensic reporting. |
| **Complexity** | Medium — standard deep learning pipeline. |
| **Novelty** | **Medium** — dual-branch fusion exists (P0015); the novelty would be in specific frequency bands and cross-attention mechanism, but this is incremental. |
| **Publication Potential** | Medium — strong technical paper but lower novelty ceiling than a system contribution. |
| **Implementation Difficulty** | Medium — well-understood components in FastAI/PyTorch. |
| **Dataset Needs** | Same as Direction 1. |
| **Evaluation Needs** | Cross-generator accuracy, robustness, ablation of branches, frequency band analysis. |
| **Future Scalability** | Limited — a single detector architecture does not extend to other modalities without redesign. |
| **Alignment with Primary Contribution** | **Partial** — this would be *one evidence collector* (the Deep Learning Specialist, Module 4 in §6), not the full forensic system. |

### Objective Decision Criteria
Choose this direction if: (a) time constraints prevent building the full forensic system; (b) the thesis can focus narrowly on detection accuracy; (c) the system-level contribution is deferred to future work. **Warning:** choosing this direction contradicts §1.2 which identifies the AI Forensic Analyst — not the detector — as the primary contribution.

---

## Candidate Direction 3: Bias-Aware Cross-Generator Detection with Dataset Integrity Auditing

**One-line summary:** Develop a detection framework that explicitly audits and mitigates dataset bias (compression, color, resolution shortcuts) to achieve genuine cross-generator generalization rather than inflated benchmark accuracy.

### Grounding

| Supporting Gaps | GAP0002 (High, freq=6), GAP0001 (Critical, freq=11) |
|---|---|
| Supporting Claims | CLAIM0003, CLAIM0001, CLAIM0006 |
| Key Papers | P0002, P0007, P0011, P0016, P0021, P0023 |

### Evaluation

| Criterion | Assessment |
|---|---|
| **Advantages** | (1) Addresses a pervasive but under-acknowledged problem: dataset bias inflating results (CLAIM0003, P0016 zero-learning audit achieved 85%). (2) Contributes a methodology for honest evaluation — valuable to the entire field. (3) Builds on recent critical finding (P0016, 2026). |
| **Disadvantages** | (1) Primarily a methodology/evaluation contribution rather than a system contribution. (2) Does not build the forensic system. (3) Bias mitigation alone may not sufficiently differentiate the thesis. |
| **Complexity** | Medium. |
| **Novelty** | **Medium-High** — bias auditing for deepfake detection is nascent (P0016 is the first major work), but this is an evaluation contribution, not a system one. |
| **Publication Potential** | Medium-High — evaluation/methodology papers are valued but harder to publish at top venues without a system or method contribution. |
| **Implementation Difficulty** | Medium — statistical auditing + training with debiased data. |
| **Dataset Needs** | Multiple datasets required to demonstrate bias; same as Direction 1. |
| **Evaluation Needs** | Zero-learning statistical audits, cross-dataset evaluation with and without bias mitigation, demographic fairness analysis. |
| **Future Scalability** | Limited — bias auditing is a practice, not an extensible system. |
| **Alignment with Primary Contribution** | **Weak** — this is a methodology contribution, not the AI Forensic Analyst. |

### Objective Decision Criteria
Choose this direction if: (a) the human prioritizes evaluation methodology over system building; (b) there is strong concern about publishing inflated results; (c) time is very limited. **Note:** bias-aware evaluation can (and should) be *integrated into* Direction 1 as a component, rather than being the sole contribution.

---

## Candidate Direction 4: Hierarchical Source Attribution with Forensic Reporting

**One-line summary:** Build a hierarchical multi-level classifier (real/fake → GAN/diffusion → specific generator) wrapped in a forensic reporting pipeline that explains each classification level's decision.

### Grounding

| Supporting Gaps | GAP0005 (High, freq=3), GAP0001 (Critical, freq=11), GAP0003 (Critical, freq=9) |
|---|---|
| Supporting Claims | CLAIM0001, CLAIM0004, CLAIM0007 |
| Key Papers | P0018, P0021, P0023 |

### Evaluation

| Criterion | Assessment |
|---|---|
| **Advantages** | (1) Source attribution is practically valuable (forensic use case). (2) Hierarchical structure maps well to the Forensic Analyst's evidence chain. (3) Builds on the strongest existing approach (P0018, 97%+ accuracy). (4) Each level is explainable independently. |
| **Disadvantages** | (1) P0018 already does this — novelty requires significant differentiation. (2) Error propagation across levels is a known problem (P0018 weakness). (3) Requires a large, multi-generator dataset which may overlap with P0018's proprietary one. (4) Without the full evidence-fusion system, this is P0018 + reporting. |
| **Complexity** | Medium-High. |
| **Novelty** | **Low-Medium** — P0018 established the paradigm; incremental improvement is hard to publish. |
| **Publication Potential** | Medium — unless significantly differentiated from P0018. |
| **Implementation Difficulty** | Medium — cascading classifiers are standard. |
| **Dataset Needs** | Requires datasets covering many specific generators (at least 5+ GAN + 5+ diffusion architectures). |
| **Evaluation Needs** | Per-level accuracy, error propagation analysis, source attribution confusion matrices, explainability quality. |
| **Future Scalability** | Moderate — new generators require retraining the appropriate level. |
| **Alignment with Primary Contribution** | **Moderate** — the forensic reporting layer aligns with the system, but the core is still a classifier. |

### Objective Decision Criteria
Choose this direction if: (a) source attribution is the primary forensic requirement; (b) access to a diverse multi-generator dataset is assured; (c) clear differentiation from P0018 can be articulated (e.g., by integrating with evidence fusion from Direction 1).

---

## Candidate Direction 5: Compression-Robust Synthetic Face Detection for Social Media Forensics

**One-line summary:** Develop a detection pipeline specifically optimized for social-media-degraded synthetic faces, combining noise-invariant frequency features with compression-aware spatial features and augmentation strategies.

### Grounding

| Supporting Gaps | GAP0004 (High, freq=6), GAP0001 (Critical, freq=11) |
|---|---|
| Supporting Claims | CLAIM0002, CLAIM0006 |
| Key Papers | P0003, P0005, P0010, P0013, P0016, P0018 |

### Evaluation

| Criterion | Assessment |
|---|---|
| **Advantages** | (1) High practical impact — most synthetic faces are shared via social media. (2) Directly addresses a known weakness of all current methods (CLAIM0006). (3) Clear, measurable evaluation (before/after compression accuracy). |
| **Disadvantages** | (1) Narrow scope — robustness is one dimension of the problem. (2) Does not build the forensic system. (3) May be seen as an engineering improvement rather than a research contribution. |
| **Complexity** | Medium. |
| **Novelty** | **Medium** — compression robustness is acknowledged but few works focus on it exclusively; however, it's an engineering contribution. |
| **Publication Potential** | Medium — practical but may lack the novelty depth for top venues. |
| **Implementation Difficulty** | Medium — augmentation strategies + architecture design for robustness. |
| **Dataset Needs** | Existing datasets + social media simulation pipeline (JPEG re-compression, resizing, platform-specific filters). |
| **Evaluation Needs** | Accuracy across compression levels, platform-specific simulation, comparison with uncompressed baselines. |
| **Future Scalability** | Limited — specific to the compression robustness problem. |
| **Alignment with Primary Contribution** | **Weak** — this is a robustness enhancement for a single detector, not a system contribution. |

### Objective Decision Criteria
Choose this direction if: (a) the primary application target is social media forensics; (b) the thesis scope is deliberately narrow; (c) practical deployment concerns outweigh system novelty. **Note:** like Direction 3, this can be integrated into Direction 1 as a component.

---

## Comparative Summary

| Criterion | Dir. 1: Forensic System | Dir. 2: Hybrid Features | Dir. 3: Bias-Aware | Dir. 4: Hierarchical | Dir. 5: Robust |
|---|---|---|---|---|---|
| **Novelty** | ★★★★★ | ★★★☆☆ | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ |
| **Publication Potential** | ★★★★★ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ |
| **Alignment w/ Primary Contribution** | ★★★★★ | ★★☆☆☆ | ★☆☆☆☆ | ★★★☆☆ | ★☆☆☆☆ |
| **Complexity** | High | Medium | Medium | Med-High | Medium |
| **Future Scalability** | ★★★★★ | ★★☆☆☆ | ★☆☆☆☆ | ★★★☆☆ | ★★☆☆☆ |
| **Implementation Difficulty** | High | Medium | Medium | Medium | Medium |
| **Gap Coverage** | GAP0001,3,7 | GAP0001,4,7 | GAP0001,2 | GAP0001,3,5 | GAP0001,4 |
| **Deferred Decisions Resolved** | DEF-002 (partial), DEF-004 | DEF-002 | — | DEF-002 | — |

---

## Recommendation (Non-Binding)

**Direction 1** is the strongest candidate by every criterion except implementation complexity. It is the *only* direction that directly builds the AI Forensic Analyst — the project's declared primary contribution (§1.2). Directions 2–5 are each subcomponents or aspects that can be *integrated into* Direction 1:

- Direction 2 (hybrid features) becomes one **evidence collector** in the forensic system.
- Direction 3 (bias-aware evaluation) becomes a component of the **evaluation protocol**.
- Direction 4 (hierarchical attribution) informs the **decision engine** hierarchy.
- Direction 5 (robustness) becomes a **training strategy** for the evidence collectors.

Direction 1 subsumes the others. The implementation complexity is managed by the project's modular architecture — each module is independently built, tested, and integrated via the [Module Registry](../MASTER_RESEARCH_OPERATING_SYSTEM.md#11_ai_forensic_system).

---

## ⚠️ HUMAN DECISION REQUIRED (A.8 Protocol)

**What:** Select the research direction for this project.

**Why:** This is an irreversible scientific decision reserved for the human (§1.9). It anchors the project's scope, dataset selection (DEF-003), backbone architecture (DEF-002), and evidence fusion strategy (DEF-004).

**Exactly what to do:**
1. Review all 5 candidate directions above.
2. Select one direction (or specify a combination/modification).
3. Complete the decision record in `01_Project_Management/decision_log/DEC0003.md` with your choice.

**Expected output:** A completed `DEC0003.md` recording the selected direction, rejected alternatives, and rationale.

**Where files go:** `01_Project_Management/decision_log/DEC0003.md` (stub provided).

> **The AI does not choose. The human decides.**
