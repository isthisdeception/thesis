# Paper Summary: P0038

## Metadata
- **Paper ID:** P0038
- **Title:** Analyzing Fairness in Deepfake Detection With Massively Annotated Databases
- **Authors:** Ying Xu, Philipp Terhörst, Marius Pedersen, Kiran Raja
- **Year:** 2024
- **Venue:** IEEE Transactions on Technology and Society (Vol. 5, No. 1, pp. 93–106)
- **Publisher:** Institute of Electrical and Electronics Engineers (IEEE)
- **DOI:** 10.1109/tts.2024.3365421
- **Citations:** 92

## Problem
Deepfake detection models trained on widely used public face-forgery benchmarks exhibit low cross-dataset generalizability and concerning demographic/attribute biases, risking false accusations against authentic individuals or missed detections of manipulated media. Prior fairness audits examined at most 2–4 demographic attributes on a single dataset, while existing Deepfake databases lack fine-grained demographic and non-demographic facial attribute annotations needed to systematically diagnose bias and spurious model shortcuts.

## Motivation
Real-world Deepfake misclassifications carry severe societal, political, and security consequences (illustrated by the 2018 Gabon President Ali Bongo New Year's address controversy, Fig. 1). Because neural networks encode attribute-related patterns in internal representations even when not trained for them, auditing whether detectors behave fairly across both demographic (age, gender, ethnicity) and non-demographic attributes (facial geometry, hair, accessories, expressions)—and whether errors differ between pristine (real) and manipulated (fake) faces—is critical before operational deployment.

## Method
The paper introduces a two-part annotation and bias-auditing methodology without proposing a new detector:
1. **Confidence-Guided Attribute Annotation Transfer (Section III-A):** Uses the **MAAD-Face** attribute classifier [49] (trained on LFW and CelebA) with reliability estimation [50] to transfer **47 facial attributes** (demographics, skin, hair, beard, face geometry, mouth, nose, accessories, other) onto five Deepfake datasets. Predictions are labeled positive (`1`), negative (`-1`), or undefined (`0` when prediction confidence is **< 90%**), generating **over 65.3M labels**.
2. **Imbalance-Corrected Fairness Metrics (Section III-B, Eq. 1–3; Section IV-C):**
   - Computes error rate as `1 - balanced accuracy` (arithmetic mean of sensitivity and specificity) to handle class imbalance.
   - Defines **Relative Performance** `RP_type(a) = 1 - err^(+)_type(a) / err^(-)_type(a)` comparing error rates with vs. without attribute `a` (`RP = -100%` indicates twice the error rate when `a` is present).
   - Proposes **Corrected Relative Performance (`CRP(a) = RP_data(a) - RP_control(a)`)** using randomly sampled control groups of matched size `N` from the same distribution, isolating genuine attribute bias from test-set imbalance.
   - Splits `CRP` into **Pristine Data Relative Performance (`PDRP`)** (real faces only; negative = higher false-fake rate) and **Deepfake Data Relative Performance (`DDRP`)** (fake faces only; negative = higher missed-fake rate) using 4-quadrant diagnostic plots (Fig. 5).

## Architecture
Evaluates **three established Deepfake detection backbone architectures** independently across the annotated datasets (Section IV-B):
- **EfficientNetB0** [46]: Compound-scaled CNN with mobile inverted bottleneck blocks (MBConv), squeeze-and-excitation optimization, and stochastic depth regularization.
- **Xception** [8]: CNN using depthwise separable convolutions for decoupled spatial/channel feature extraction.
- **Capsule-Forensics-v2** [36]: Capsule network extracting facial features and spatial relationships with a disentanglement-encouraging loss.

## Dataset
Five widely used Deepfake video datasets annotated with **47 attributes** (30 frames extracted from the first 300 frames per video at 10-frame intervals; faces detected and aligned via **MTCNN** [59]; Section III-A, IV-A, Table II):
- **A-DFD:** 28 identities; 363 pristine / 3,068 forged videos; 10.8k pristine / 89.6k forged frames; **4.7M labels**.
- **A-FF++:** 1,000 identities; 1,000 pristine / 5,000 forged videos; 29.8k pristine / 149.1k forged frames; **8.5M labels**.
- **A-DFDC:** 960 identities; 23,654 pristine / 104,500 forged videos; 54.5k pristine / 52.6k forged frames; **4.6M labels**.
- **A-Celeb-DF:** 59 identities; 590 pristine / 5,639 forged videos; 26.3k pristine / 166.5k forged frames; **9.2M labels**.
- **A-DF-1.0 (DeeperForensics-1.0):** 100 identities; 50,000 pristine / 10,000 forged videos; 870.3k pristine / 321.5k forged frames; **38.3M labels**.
- **Curation for bias experiments (Section IV-A, I-B fn 2):** Attributes with fewer than 100 positive or negative samples are excluded, leaving **31 attributes** for bias analysis; **A-DF-1.0** is excluded from bias analysis because the three detectors produced too few errors to analyze biased behavior.
- Annotations and code are publicly released (`https://github.com/xuyingzhongguo/DeepFakeAnnotations`).

## Training
- Each of the three backbone models (EfficientNetB0, Xception, Capsule-Forensics-v2) is trained and evaluated per dataset using a **subject-exclusive 60% / 20% / 20% train / validation / test split** across all attributes (Section IV-B).
- Exact training hyperparameters (optimizer, learning rate, batch size, epochs, data augmentations) and raw per-attribute numerical tables (referenced as Appendix Tables IV, XIV, XV, XVI) are **Not reported** in this 14-page manuscript PDF.

## Evaluation
- **Database Attribute Distribution & Correlations (Section V-A1–2, Fig. 2–3):** Quantifies positive/negative/undefined attribute percentages and top 20 positive/negative Pearson pairwise correlations across all five annotated databases.
- **Annotation Correctness Audit (Section V-A3, Table III):** Validates MAAD-Face label quality against 3 human evaluators (majority vote on 100 positive + 100 negative samples per attribute), reporting **92% average accuracy, 90% precision, 94% recall** across 32 tabulated attributes (compared to 72%/61%/84% for LFW and 85%/83%/89% for CelebA).
- **General Attribute Bias (`RP` vs. `CRP`, Section V-B1, Fig. 4):** 12 scatter plots (3 backbones × 4 datasets: A-Celeb-DF, A-DFD, A-FF++, A-DFDC) across 31 attributes.
- **Pristine vs. Deepfake Asymmetry (`PDRP` vs. `DDRP`, Section V-B2, Fig. 5):** 12 four-quadrant scatter plots separating bias on real faces from bias on fake faces and identifying Quadrant II / IV shortcut assumptions.

## Results
- **Severe dataset attribute imbalance (Section V-A1, Fig. 2):**
  - In **A-Celeb-DF**, same-gender face swapping amplifies male over-representation from 56.8%/43.2% (original) to **70.15% male / 29.85% female**, and **88.1% Caucasian** (5.1% Asian, 6.8% African).
  - **DFDC** under-represents Asian descent; **DFD** and **FF++** heavily over-represent White subjects.
- **Strong spurious attribute correlations (Section V-A2, Fig. 3):** Pairwise correlations (e.g., `Heavy Makeup`–`Wearing Lipstick` in celebrity-dominated Celeb-DF; `Mustache`–`Goatee`) show how non-forensic cues co-occur with gender or dataset domains.
- **Strong demographic and non-demographic bias across backbones (Section V-B1, Fig. 4):**
  - On **A-Celeb-DF**, **EfficientNetB0** suffers **>2× error (`RP <= -100%`)** on faces with `Big Nose`, `Big Lips`, `Black`, or `Chubby` (with `Double Chin`, `Obstructed Forehead`, and `Male` also in the high-error region of Fig. 4a).
  - On **A-FF++**, `No Beard` and `Smiling` (EfficientNetB0, Fig. 4g) and `Young`/`Black` (Xception, Fig. 4h) exhibit `RP < -200%`. On **A-DFD**, `Xception` exhibits `RP` near `-1200%` for `Shiny Skin` (Fig. 4e). `Obstructed Forehead` causes severe misclassification in both Celeb-DF and DFDC.
- **Pristine vs. Fake asymmetry & spurious shortcut learning (Section V-B2, Fig. 5, Section VI):**
  - Attributes frequently fall far from the bisectrix and into Quadrants II and IV, showing opposite effects on real vs. fake data.
  - **Spurious shortcut example (p. 11):** On A-Celeb-DF, **EfficientNetB0** yields **`DDRP ≈ +100%`** and **`PDRP ≈ -75%`** for `Wearing Hat`—meaning fake faces with hats are detected 2× more accurately, while real faces with hats incur nearly 2× more false-fake errors (the network learned "hat = Deepfake"). Similar questionable shortcuts occur for `Smiling` and `Wearing Hat`.
  - **Adversarial/security risk (p. 11):** On A-Celeb-DF, fake faces with `Goatee`, `Big Nose`, `Chubby`, `Male`, or `Black` double EfficientNetB0's error rate compared to faces without those attributes, creating exploitable blind spots.

## Strengths
- **Massively annotated open resource:** Releases **65.3M+ high-confidence labels** across 47 attributes on five standard benchmarks with validated **92% annotation accuracy** (Table III).
- **Goes beyond demographics:** Demonstrates that non-demographic attributes (`Big Nose`, `Big Lips`, `Smiling`, `Wearing Hat`, `Obstructed Forehead`, `Shiny Skin`) drive dramatic detector errors and spurious shortcuts.
- **Principled imbalance-corrected metric (`CRP` / `PDRP` / `DDRP`):** Disentangles true model bias from test-set attribute imbalance and cleanly separates false-accusation risk on pristine images (`PDRP`) from missed-detection risk on fakes (`DDRP`).
- **Subject-exclusive evaluation:** Uses strict 60/20/20 subject-exclusive splits across four distinct datasets and three standard backbones.

## Weaknesses
- [GAP-ready: supported by P0038] **Correlation rather than causation (acknowledged in Section VI-A):** `CRP`, `PDRP`, and `DDRP` establish statistical associations between single attributes and detector errors, without causal intervention or disentangling correlated attribute clusters (e.g., `Male` + `Goatee` + `No Makeup`).
- [GAP-ready: supported by P0038] **Single-attribute analysis only (Section V-B2, p. 11):** Multi-attribute / intersectional interactions (e.g., older + darker skin + glasses) are not evaluated, though authors note combined attributes could compound bias exponentially.
- [GAP-ready: supported by P0038] **Pre-diffusion video benchmarks and older CNN backbones only:** Evaluates only FF++, Celeb-DF, DFD, and DFDC (face-swap/GAN/video manipulation era) with EfficientNetB0, Xception, and Capsule-Forensics-v2; excludes diffusion-generated faces, ViTs, and self-supervised foundation detectors.
- [GAP-ready: supported by P0038] **Intra-dataset training/evaluation only:** Models are trained and tested within each dataset's 60/20/20 split rather than cross-dataset, leaving cross-domain attribute bias transfer untested.
- [GAP-ready: supported by P0038] **Relies on automated pseudo-labels and omits exact raw tables in PDF:** 47-attribute labels inherit MAAD-Face classifier accuracy limits (e.g., 0.70 accuracy / 0.50 precision on `Big Lips`, 0.77 on `Shiny Skin`/`Receding Hairline`; Table III), and exact raw error tables (Tables IV, XIV–XVI) and training hyperparameters are absent from the 14-page manuscript.

## Research Gap
- [GAP-ready: supported by P0038] Attribute-level bias and spurious shortcut auditing (`PDRP`/`DDRP`) has not been systematically extended to **diffusion-generated synthetic faces** or modern ViT / self-supervised / reconstruction-based detectors (`P0037`, `P0023`).
- [GAP-ready: supported by P0038] Intersectional and multi-attribute causal bias analysis—disentangling correlated facial attributes from genuine generative artifacts—remains under-explored.
- [GAP-ready: supported by P0038] Concrete bias-mitigation strategies (adversarial debiasing, counterfactual augmentation, attribute-invariant representation learning) that preserve cross-generator generalization are needed.

## Future Work
- Build more balanced, diverse, and richly annotated Deepfake datasets (Section VI).
- Conduct causal (beyond correlational) studies of bias origins and multi-attribute/intersectional compounding effects (Section V-B2, VI-A).
- Evaluate newer detection architectures (ViTs, frequency/diffusion detectors) for architecture-dependent fairness factors (Section VI-A).
- Develop bias-mitigation techniques to improve both demographic fairness and cross-dataset generalization, and harden detectors against attribute-exploiting evasion attacks (Section VI).

## Interesting Ideas
- **Quadrant II / IV (`PDRP` vs. `DDRP`) shortcut detector:** Checking whether an attribute helps on fakes (`DDRP > 0`) while hurting on real faces (`PDRP < 0`) is a brilliant automated test for spurious shortcut learning (e.g., `Wearing Hat` -> "Deepfake").
- **Confidence-thresholded pseudo-labeling (`<90%` -> undefined):** Using reliability-scored attribute transfer allows scaling demographic/non-demographic audits to unlabeled datasets (like `DS0001` or `DS0002`) without manual annotation.

## Possible Reuse
- **Explaining our `DS0005` FairFace failure mode (`EVAL0001`):** In our cross-dataset evaluation (`EVAL0001`), `MODEL0001` trained on `DS0001` exhibited an **82.59% FPR** (`17.41%` specificity, mean `P(fake) = 0.7969`) on 10,000 pristine FairFace (`DS0005`) images. `P0038`'s `PDRP` framing directly formalizes this failure: training-set attribute/domain imbalance causes detectors to misclassify pristine demographic groups at alarming rates, motivating attribute-stratified evaluation on `DS0005` (which has race/gender/age labels) and `MOD006` (Evidence Validation) / `MOD009` (Confidence Estimation) calibration checks.
- **Forensic Audit & Explainability integration:** `P0038`'s attribute-correlation and shortcut findings directly inform `MOD010` (Explainability Engine), `MOD011` (Forensic Reasoning Engine), and `MOD015` (Audit Trail)—flagging when a detector's attention (Grad-CAM) aligns with non-forensic attributes (`Wearing Hat`, `Smiling`, `Big Nose`, `Obstructed Forehead`) rather than generative artifacts.
- **`CRP` / `PDRP` / `DDRP` metrics:** Can be reused directly in our `08_Evaluation` fairness protocol for both `DS0005` (pristine FairFace `PDRP`) and `DS0002` (`DiFF` fake `DDRP`).

## Questions
- Do our own `DS0001`-trained detectors (`MODEL0001`) exhibit the same `PDRP` disparities across FairFace (`DS0005`) race/gender/age subgroups behind the 82.59% aggregate FPR?
- Can Grad-CAM (`P0016` / `MOD010`) confirm visually whether `Wearing Hat` or `Obstructed Forehead` shortcuts drive misclassifications on `DS0001` and `DS0003`?
- How would `P0038`'s `CRP`/`PDRP`/`DDRP` diagnostic behave on `P0037`'s DiffSynFace + FairFace benchmark if applied to `DIRE`, `LaDeDa`, and `NPR`?

## Connections
- Directly complements and challenges **P0037** (Panda et al., 2026): `P0037` reports minimal demographic bias in aggregate ACC/AP for diffusion detectors, whereas `P0038` reveals stark attribute-level biases and opposing pristine-vs-fake (`PDRP`/`DDRP`) errors on CNN backbones—highlighting the need to evaluate `P0037`'s datasets with `P0038`'s `CRP`/`PDRP`/`DDRP` decomposition.
- Closely aligns with **P0016** (Altamimi et al., 2026): both expose dataset-driven shortcuts in deepfake detectors—`P0016` via a zero-learning photometric audit (85% accuracy) and Grad-CAM, and `P0038` via `CRP` and `PDRP`/`DDRP` attribute correlations.
- Relates to **P0007** (Khan & Dang-Nguyen, 2024): `P0038` explicitly attributes the poor cross-dataset generalization documented in `P0007` (across FF++, CelebDF-V2, DFDC) to imbalanced demographic and non-demographic attributes in those exact benchmarks.
- Connects to **P0023** (Cheng et al., 2024) and **P0018** (Guarnera et al., 2024): provides the fairness/attribute-bias dimension missing from `DiFF` (`P0023`) and hierarchical GAN+DM (`P0018`) evaluations.
