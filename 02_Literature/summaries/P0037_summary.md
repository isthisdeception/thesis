# Paper Summary: P0037

## Metadata
- **Paper ID:** P0037
- **Title:** Bias-Free? An Empirical Study on Ethnicity, Gender, and Age Fairness in Deepfake Detection
- **Authors:** Aditi Panda, Tanusree Ghosh, Tushar Choudhary, Ruchira Naskar
- **Year:** 2026
- **Venue:** ACM Computing Surveys (Vol. 58, No. 10, Article 246, March 2026, pp. 1–29)
- **Publisher:** Association for Computing Machinery (ACM)
- **DOI:** 10.1145/3796544
- **Citations:** 2

## Problem
While synthetic face generation via GANs, VAEs, autoregressive models, and especially latent diffusion models has advanced rapidly, most deepfake image detection benchmarks optimize and report aggregate accuracy without systematically auditing demographic fairness. It remains unclear whether state-of-the-art passive deepfake image detectors exhibit technical detection bias across ethnicity, gender, and age when evaluated out-of-distribution using publicly released pretrained checkpoints without retraining.

## Motivation
Prior studies documented demographic and representational disparities in text, audio, and earlier video deepfake detection, where sensitive attributes can correlate with linguistic or prosodic patterns. In contrast, image-based deepfake detection relies primarily on visual generation artifacts (textures, lighting, upsampling/denoising traces). Auditing pretrained detectors across both open-source (Stable Diffusion variants) and closed-source/proprietary (DALL-E 3, MidJourney) generators on a demographically balanced face dataset tests whether technical bias persists in modern image detectors and links generative model evolution to detection fairness.

## Method
The paper combines a generative model survey/taxonomy with an empirical out-of-distribution demographic fairness audit:
1. **Taxonomy of Generative Models (Section 3, Fig. 2, Table 2):** Classifies text-to-image generators into Autoregressive Models (DALL-E 1), Basic Latent Diffusion Models (Stable Diffusion 1.x, DALL-E 2), Advanced Latent Diffusion Models (Stable Diffusion 2.x, SDXL, SDXL-Turbo, DALL-E 3), and Proprietary Models (MidJourney, Adobe Firefly), contrasting core mechanism, resolution, text-image alignment, face fidelity, speed, and openness.
2. **Passive Detector Selection (Section 4, Table 5):** Selects six representative passive deepfake detection architectures spanning visual-artifact methods (NPR, DNF), knowledge-distillation methods (LaDeDa), and diffusion-model detectors (Ricker et al., DIRE, DistilDIRE), evaluating **all 22 publicly available pretrained checkpoints** without retraining or modification.
3. **Subgroup Fairness Evaluation (Section 5):** Evaluates real-vs-fake classification **Accuracy (ACC)** and **Average Precision (AP)** (Table 4; Fig. 1 and Section 5 prose also mention AUC and FPR, though only ACC and AP are tabulated) separately across six ethnic groups, two genders, and four age brackets.

## Architecture
No new detection model is proposed; instead, the study evaluates **6 existing detector families across 22 pretrained checkpoints** (Section 4, Table 5):
- **Ricker et al. [54] (5 checkpoints):** `Wang2020_0.1`, `Wang2020_0.5`, `Grag2021/ProGAN`, `Grag2021/StyleGAN2`, `Mandelli2022` (CNN/GAN-era and retrained DM detectors).
- **DIRE [55] (6 checkpoints):** `celebahq_sdv2`, `imagenet_adm`, `lsun_adm`, `lsun_iddpm`, `lsun_pndm`, `lsun_stylegan` (measures $|x_0 - R(I(x_0))|$ reconstruction error via DDIM inversion/generation).
- **DNF [52] (4 checkpoints):** `res256np_ddim20_celeba`, `res256np_ddim20_lsun`, `res256np_ddim20_imagenet`, `res256np_ddim20_cnnspot` (Diffusion Noise Feature fusing inverse-diffusion noise estimates across time steps).
- **LaDeDa [53] (2 checkpoints):** `WildRF_LaDeDa`, `ForenSynth_LaDeDa` (modified ResNet-50 scoring 9x9 image patches via average pooling; paper also discusses distilled Tiny-LaDeDa).
- **DistilDIRE [56] (2 checkpoints):** `imagenet-distil-dire-11e`, `celebahq-distil-dire-34e` (lightweight distilled DIRE using ImageNet-pretrained ResNet-50 teacher).
- **NPR [51] (3 checkpoints):** `NPR_GenImage_sdv4`, `NPR_model_epoch_last_3090`, `NPR.pth` (Neighboring Pixel Relationships capturing local upsampling artifacts).

## Dataset
- **Synthetic faces — DiffSynFace [1] (Section 5.1, Table 3):** 40k+ synthetic face images generated via prompt `"Front face of <a/an> <Ethnicity> <Gender> in <his/her> <early/mid/late> <age> in color at 4K resolution"`.
  - Table 3 reports 41,327 total images across 7 generators: Stable Diffusion 1.0 (5,760; prose on p. 20 says SD 1.5), Stable Diffusion 2.0 (5,778), Stable Diffusion XL (6,211), Stable Diffusion XL-Turbo (5,800), DALL-E 3 (5,766), Adobe Firefly (5,954), and MidJourney (5,858).
  - *Note:* Section 5.4.1 and Tables 6–8 captions state the bias experiments classify synthetic images from **six generative models** (DALL-E 3, MidJourney, SD 1, SD 2, SDXL, SDXL-Turbo; Adobe Firefly is listed in Table 3 but omitted in Section 5.4.1).
  - Demographics: 6 ethnicities (African, American, East Asian, European, Indian, South Asian), 2 genders (Male, Female), 4 age groups (20–29, 30–39, 40–49, 50–60; >=120 images per age/gender/ethnicity/generator).
- **Real faces (axis-specific external datasets):**
  - Ethnicity study (Section 5.4.1): **FairFace** [60].
  - Gender study (Section 5.4.2): **CelebA-HQ** [61] (note: ref [61] in bibliography cites Huang et al. IntroVAE rather than Karras et al.).
  - Age study (Section 5.4.3): **Adience** [62].
  - Exact real-image sample counts per experiment are **Not reported**.

## Training
**No training or fine-tuning is performed** in this study (Section 5.1, 5.3, 5.4.1). All 22 checkpoints are evaluated zero-shot using official GitHub weights pretrained on external datasets (LSUN-Bedroom, ImageNet, CelebA-HQ, FFHQ, WildRF, ForenSynth, GenImage, CNNSpot; Table 5) to measure out-of-distribution generalization and fairness.

## Evaluation
- **Ethnicity bias (Section 5.4.1, Table 6):** Subgroup ACC and AP across 6 ethnicities (synthetic faces from 6 generators + FairFace real faces).
- **Gender bias (Section 5.4.2, Table 7):** Subgroup ACC and AP across Male and Female (synthetic faces + CelebA-HQ real faces).
- **Age bias (Section 5.4.3, Table 8):** Subgroup ACC and AP across 20s, 30s, 40s, and 50s (synthetic faces + Adience real faces).
- **Unreported evaluation details:** Despite Fig. 1 and Section 5 mentioning AUC and FPR, only ACC and AP appear in Tables 6–8; separate real-FPR vs. fake-FNR, per-generator demographic breakdowns, intersectional subgroup intersections, and statistical significance tests (p-values/confidence intervals) are **Not reported**.

## Results
Across all three demographic axes, the authors report no systematic demographic bias, observing subgroup differences generally within **1–5 percentage points** with inconsistent directions across detectors (Section 5.4–5.5):
- **Ethnicity (Table 6, Section 5.4.1):**
  - Newer diffusion-aware and patch-based detectors achieve the strongest and most uniform performance across ethnicities (typically 1–2% variation): `WildRF_LaDeDa` reaches **80.556/85.923** (African), **75.897/80.076** (American), **74.983/78.43** (East Asian), **76.345/80.331** (European), **76.259/80.917** (South Asian), and **78.88/83.931** (Indian) ACC/AP. `DIRE lsun_pndm` and `lsun_stylegan` achieve **76.719–80.733%** ACC and **77.156–81.745%** AP. `DNF res256np_ddim20_imagenet` attains **74.948–75.608%** ACC and **94.656–96.526%** AP. `NPR model_epoch_last_3090` achieves **71.059–74.705%** ACC and **87.031–92.016%** AP.
  - Largest gaps occur in older/GAN-oriented checkpoints: Ricker et al. (`Wang2020_0.5`: 57.908% African vs. 50.894% Indian; text notes 5–6% African vs. East Asian) and NPR (text notes 6.5% African vs. European); `DIRE imagenet_adm` drops to 69.485% ACC on East Asian vs. 77.83% on European. `DistilDIRE` remains near chance (48.342–55.139% ACC).
- **Gender (Table 7, Section 5.4.2):**
  - Most checkpoints vary by **<3 percentage points** between Male and Female; largest ACC gap reported in text is **3.5%** for `Mandelli2022` (55.978% Male vs. 52.442% Female).
  - Top models: `WildRF_LaDeDa` (**81.14 / 91.333** Male vs. **84.453 / 93.021** Female ACC/AP), `DIRE lsun_pndm` (**80.406 / 76.874** Male vs. **80.287 / 76.954** Female), `DIRE lsun_stylegan` (**79.69 / 76.857** Male vs. **78.801 / 76.778** Female), `DIRE celebahq_sdv2` (75.974 Male vs. 78.304 Female ACC).
  - `DNF` shows lower ACC and larger gender variance (e.g., `res256np_ddim20_celeba`: 58.333% Male vs. 75.003% Female ACC; `res256np_ddim20_imagenet`: 58.333/89.648 Male vs. 66.667/93.388 Female ACC/AP).
- **Age (Table 8, Section 5.4.3):**
  - Most detectors vary by **<=4 percentage points** across 20s–50s. `DIRE lsun_stylegan` leads at **75.639–77.39%** ACC (**74.015–80.215%** AP), followed by `DIRE lsun_pndm` (**75.575–76.164%** ACC) and `DIRE lsun_adm` (**75.463–75.876%** ACC).
  - Exception: `DIRE celebahq_sdv2` drops monotonically from **76.311 / 80.452** (20s), **75.022 / 79.782** (30s), **72.372 / 79.258** (40s) to **66.096 / 74.471** (50s) — a ~10-point ACC drop attributed to fewer older faces in CelebA-HQ.
  - All 4 `DNF` checkpoints collapse to **50.0% ACC** across all age groups (despite `cnnspot` reaching 77.135–81.533% AP), and `DistilDIRE` remains near 50.0–56.0% ACC.
- **Generator Observations (Sections 5.5, 6):** Stable Diffusion outputs cluster at easier detection levels, whereas **DALL-E 3** and **MidJourney** are harder to detect (DNF notably struggles on DALL-E 3).

## Strengths
- **Comprehensive out-of-distribution audit:** Evaluates 6 detector families and all 22 official pretrained checkpoints without retraining, preventing benchmark overfitting from masking bias.
- **Covers modern closed-source and open-source T2I models:** Includes DALL-E 3, MidJourney, SD 1/2/XL/XL-Turbo alongside a structured generative taxonomy (Table 2, Fig. 2).
- **Multi-axis demographic coverage:** Tests 6 ethnicities, 2 genders, and 4 age decades using a balanced synthetic prompt template (DiffSynFace).
- **Demonstrates parameter-efficiency tradeoffs:** Shows lightweight `DistilDIRE` fails to match `DIRE` generalization (Section 6).

## Weaknesses
- [GAP-ready: supported by P0037] **Real-vs-fake source confounding across axes:** Synthetic 4K DiffSynFace faces are paired with three *different* external real-face datasets (FairFace for ethnicity, CelebA-HQ for gender, Adience for age), creating domain/resolution mismatches that can confound real-vs-fake separability and inflate or distort apparent fairness.
- [GAP-ready: supported by P0037] **Severe threshold miscalibration hidden by ACC-only reporting:** Several checkpoints achieve high AP alongside chance-level ACC (e.g., `DNF cnnspot` 50.0% ACC vs. 81.5% AP on Adience age; `ForenSynth_LaDeDa` 53.3% ACC vs. 88.1% AP on ethnicity), yet the paper omits FPR, FNR, ROC-AUC, and threshold-calibration analysis (despite mentioning AUC/FPR in Fig. 1 and Section 5).
- [GAP-ready: supported by P0037] **No pristine-vs-fake bias decomposition or intersectional analysis:** Unlike `P0038`'s PDRP/DDRP framework, Tables 6–8 pool real and fake errors into aggregate ACC/AP and evaluate ethnicity, gender, and age strictly independently—hiding opposing-direction shortcut biases (e.g., high real-face FPR offset by high fake recall) and intersectional disparities.
- [GAP-ready: supported by P0037] **Diffusion-only synthetic evaluation and generator averaging:** DiffSynFace excludes GAN-generated faces, and Tables 6–8 average over the 6 generators without per-generator demographic breakdowns or post-processing/social-media compression tests.
- [GAP-ready: supported by P0037] **Moderate ceiling accuracy and missing statistical testing:** Even top checkpoints only achieve ~76–84% ACC out-of-distribution, and no confidence intervals, sample counts for real subsets, or significance tests are reported.

## Research Gap
- [GAP-ready: supported by P0037] Contradiction between "bias-free" aggregate ACC/AP claims (`P0037`) and strong real-face false-positive / attribute biases under domain shift (`P0038`, `P0016`, and our `DS0005` FairFace finding) shows that aggregate ACC/AP without FPR/FNR decomposition and calibration auditing cannot establish fairness.
- [GAP-ready: supported by P0037] Controlled demographic fairness evaluation matching real and synthetic face domains (eliminating DiffSynFace-vs-FairFace/Adience resolution and compression confounding) is missing.
- [GAP-ready: supported by P0037] Evaluating proprietary generators (DALL-E 3, MidJourney) and GANs jointly across intersectional demographics and post-processing perturbations remains open.

## Future Work
- Retrain SOTA detectors on demographically balanced synthetic data (DiffSynFace) and supply generation prompts/captions as auxiliary inputs (Section 6.1).
- Investigate **contextual bias** across deployment contexts (social media, news, advertisements).
- Apply CLIP-based latent captioning (e.g., DALL-E 3 style recaptioning) and explainable AI (XAI) analyses on misclassified images to uncover latent forensic signals.
- Evaluate detector robustness against adversarial attacks in varied real-world contexts (Section 6.2).

## Interesting Ideas
- Evaluating *all* publicly released checkpoints per detector family exposes how training dataset choice (CelebA-HQ vs. LSUN vs. ImageNet vs. WildRF) causes huge swings in calibration (e.g., `DIRE celebahq_sdv2` dropping 10% ACC on 50s faces while `lsun_stylegan` stays flat) even within the same architecture.
- The observation that `WildRF_LaDeDa` (trained on in-the-wild social media images) outperforms benchmark-trained `ForenSynth_LaDeDa` by ~25–30% ACC out-of-distribution underscores the value of realistic real-world negative baselines.

## Possible Reuse
- **Benchmark caution for our `DS0005` FairFace evaluation:** In our `EVAL0001` cross-dataset test, `MODEL0001` trained on `DS0001` suffered **82.59% FPR** (`17.41%` specificity, mean `P(fake) = 0.7969`) on 10,000 real FairFace (`DS0005`) images at threshold 0.3951. Together with `P0037` (which uses FairFace as its ethnicity baseline) and `P0037`'s DNF 50% ACC collapse on Adience, this reinforces why `MOD009` (Confidence Estimation) and `MOD008` (Decision Engine) must audit domain calibration and report real-FPR separately rather than trusting aggregate ACC/AP.
- **Multi-detector / multi-evidence ensemble perspective:** Section 6 advises taking a collective perspective across detectors because individual models lean slightly in opposite directions (e.g., `Mandelli2022` vs. `DIRE` on gender) — directly supporting `MOD007` (Evidence Fusion Engine) and `MOD004` (Deep Learning Specialist) in our AI Forensic Analyst.
- **XAI on misclassifications:** Section 6.1(3) aligns with `MOD010` (Explainability Engine) and `MOD011` (Forensic Reasoning Engine) for auditing whether failures stem from domain shortcuts or demographic cues.

## Questions
- What are the separate real-image FPR (on FairFace, CelebA-HQ, Adience) and fake-image FNR (on DiffSynFace) behind the ~75–81% ACC scores in Tables 6–8? Does FairFace trigger elevated FPR on uncalibrated CNN detectors as observed in our `DS0005` `EVAL0001` run?
- How much of the ~75–80% ACC is driven by DiffSynFace (4K text-to-image) vs. external real-dataset (FairFace 224px / Adience) domain signatures rather than genuine generative artifacts?
- Do intersectional subgroups (e.g., 50s African or East Asian faces) exhibit disparities masked by one-attribute-at-a-time averaging?

## Connections
- Directly contrasts with **P0038** (Xu et al., 2024): whereas `P0037` finds near-uniform aggregate ACC/AP across ethnicity/gender/age on DiffSynFace diffusion models, `P0038` demonstrates severe demographic and non-demographic attribute bias and pristine-vs-fake asymmetry (`PDRP` vs. `DDRP`) on CNN/capsule detectors across FF++, Celeb-DF, DFD, and DFDC.
- Connects strongly to **P0016** (Altamimi et al., 2026): `P0016`'s zero-learning 85% photometric bias finding explains why pairing external real datasets (FairFace/CelebA-HQ/Adience) with synthetic DiffSynFace without a zero-learning audit risks domain-shortcut confounding.
- Relates to **P0007** (Khan & Dang-Nguyen, 2024) and **P0023** (Cheng et al., 2024): extends out-of-distribution generalization evaluation to diffusion/proprietary generators (DALL-E 3, MidJourney, SDXL) and confirms diffusion detectors struggle out-of-distribution when checkpoints come from narrower domains.
- Relates to **P0003** (Bammey, 2024) and **P0018** (Guarnera et al., 2024): `P0003` (training-free spectral peaks) and `P0018` (hierarchical attribution across GAN+DM) represent complementary paradigms to `P0037`'s evaluated pixel/noise/reconstruction detectors (`NPR`, `DNF`, `DIRE`, `LaDeDa`).
