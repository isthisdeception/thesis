# Supplementary Material: AI Forensic Analyst Journal Manuscript

**Companion Document to:** `15_Writing/journal/manuscript.md`  
**Version:** `2.2.0` | **Date:** 2026-11-27  
**Shared Evidence Base:** `10_Tables/rendered/TAB0001.md`–`TAB0003.md`, `09_Figures/assets/FIG0001_v1`–`FIG0034_v1`, `11_AI_Forensic_System/module_registry.csv`, `08_Evaluation/forensic_analyst_eval/e14_case_results.csv`, `08_Evaluation/cross_backbone_generalization.csv`, and `08_Evaluation/EVAL0008/abstention_by_track.csv`.

---

## S1. Systematic Literature Comparison Matrix (`TAB0001`)

The full 28-method comparative matrix extracted from the 44 reviewed studies (`P0001`–`P0044`), covering detection families, generator coverage, datasets, evaluation metrics, cross-generator testing, robustness, explainability, and primary limitations, is maintained in `10_Tables/data/TAB0001.csv` and rendered in `10_Tables/rendered/TAB0001.md` (supporting `CLAIM0001`–`CLAIM0009` and `GAP0001`–`GAP0009`).

---

## S2. Diagnostic Lowest- vs. Highest-Error Case Contrast and Exploratory Data Analysis (`FIG0032`, `FIG0001`–`FIG0010`)

Whereas Figure 1 (`FIG0031`) in the main manuscript presents the complete 49-sample visual atlas covering every evaluated authentic source, synthetic generator, and demographic race subgroup across `DS0001`–`DS0005`, Figure S1 (`FIG0032`) provides a focused ten-panel (`2 x 5`) diagnostic contrast pairing the lowest-error subgroup `(a)`–`(e)` against the highest-error failure subgroup `(f)`–`(j)` within each corpus (`CelebA-HQ` `7.0%` FPR vs. `StyleGAN3` `43.7%` FNR in `DS0001`; `DCFace` `0.0%` FNR vs. `FreeDoM-I` `81.5%` FNR in `DS0002`; `FFHQ` `30.4%` FPR vs. `StyleGAN` `9.2%` FNR in `DS0003`; `RAISE` `76.7%` FPR vs. `DALL-E 3` `46.9%` FNR in `DS0004`; and `FairFace` true-negative vs. false-positive authentic portraits in `DS0005`).

![FIG0032: Diagnostic lowest-error vs highest-error contrast across DS0001-DS0005](../../09_Figures/assets/FIG0032_v1.png)

*Figure S1 (`FIG0032`): Criterion-selected lowest-error `(a)`–`(e)` versus highest-error `(f)`–`(j)` diagnostic samples (`224 x 224` px) across `DS0001`–`DS0005`.*

All five public corpora (`DS0001`–`DS0005`) were audited prior to modeling under deterministic preprocessing (`PP0001`–`PP0006`, seed `42`, EXIF stripped, minimum resolution `64 px`, RGB PNG conversion, `224 x 224` resizing without denoising) (`DEC0004`; `DEC0005`). Specifically, `FIG0001`–`FIG0006` document class, generator, and demographic distributions, while `FIG0007`–`FIG0010` audit resolution, brightness, contrast, and compression footprints. Figure S2 (`FIG0002`) illustrates the balanced 13-generator plus real composition of `DS0001` ArtiFact.

![FIG0002: DS0001 Generator Mix](../../09_Figures/assets/FIG0002_v1.png)

*Figure S2 (`FIG0002`): Generator distribution across the 50,000-image `DS0001` ArtiFact face benchmark.*

To establish demographic fairness stress-testing coverage, Figure S3 (`FIG0006`) presents the seven-group demographic distribution of `DS0005` FairFace (`97,698` authentic portraits).

![FIG0006: DS0005 FairFace Demographic Distribution](../../09_Figures/assets/FIG0006_v1.png)

*Figure S3 (`FIG0006`): Seven-group demographic composition of `DS0005` FairFace (`97,698` authentic faces).*

---

## S3. Extended Architecture, Training, Calibration, ROC/PR, and Robustness Figures

The main manuscript presents eleven primary figures (`FIG0031`, `FIG0027`, `FIG0028`, `FIG0011`, `FIG0015`, `FIG0016`, `FIG0018`, `FIG0019`, `FIG0020`, `FIG0034`, and `FIG0033`). All remaining publication-grade figures (600 DPI PNG and vector PDF) reside in `09_Figures/assets/`, covering confidence-accuracy histograms (`FIG0012`), threshold trade-off curves (`FIG0013`), test confusion matrices (`FIG0014`), worst-level subgroup perturbation shifts (`FIG0017`), paired ROC and PR curves (`FIG0021`–`FIG0023`), training convergence (`FIG0024`–`FIG0025`), and full-stack architecture diagrams (`FIG0026`, `FIG0029`, `FIG0030`). Figure S4 (`FIG0026`) depicts the end-to-end research methodology pipeline.

![FIG0026: End-to-End Methodology Pipeline](../../09_Figures/assets/FIG0026_v1.png)

*Figure S4 (`FIG0026`): End-to-end benchmark curation, preprocessing, controlled training, stress evaluation, and forensic verification pipeline.*

Figure S5 (`FIG0029`) illustrates the three-tier separation connecting the React investigation interface (`MOD014`), the seven-app Django REST API (`MOD013`), and the eighteen-module forensic core (`MOD001`–`MOD018`).

![FIG0029: Three-Tier Full-Stack Web Architecture](../../09_Figures/assets/FIG0029_v1.png)

*Figure S5 (`FIG0029`): Three-tier full-stack architecture separating React UI (`MOD014`), Django/DRF API (`MOD013`), and forensic core.*

Figure S6 (`FIG0030`) details the YAML-governed training workflow, SHA-256 atomic checkpointing, and three-tier storage synchronization.

![FIG0030: Reproducible Training, SHA-256 Checkpointing and Storage Architecture](../../09_Figures/assets/FIG0030_v1.png)

*Figure S6 (`FIG0030`): Config-driven FastAI training pipeline with SHA-256 checkpointing and validation-only threshold freezing.*

Finally, Figure S7 (`FIG0021`) plots paired receiver operating characteristic curves across `EXP0001` and the four one-factor ablations `EXP0003`–`EXP0006` on `DS0001` `SPLIT0001` (`n = 7,505`).

![FIG0021: Fairness-Compatible ROC Curves](../../09_Figures/assets/FIG0021_v1.png)

*Figure S7 (`FIG0021`): Paired ROC curves across `EXP0001` and one-factor ablations `EXP0003`–`EXP0006` on the ArtiFact test split.*

---

## S4. Complete 18-Module Contract, REST API Surface, and Verification (`EVAL0007`–`EVAL0008`)

### S4.1 AI Forensic Analyst Module Registry (`MOD001`–`MOD018`)

All eighteen modules (`M1`–`M18`) are implemented and verified in `11_AI_Forensic_System/module_registry.csv`: `MOD001` Input Management, `MOD002` Image Validation, `MOD003` Nine Independent Non-Detector Collectors, `MOD004` Isolated Deep Learning Specialist, `MOD005` Append-Only Evidence Registry (`EVxxxxxx`), `MOD006` Non-Destructive Evidence Validator, `MOD007` Pluggable Evidence Fusion (`rule_based`, `DEC0009`), `MOD008` Image-Blind Four-Way Decision Engine, `MOD009` Validation-Calibrated 4D Confidence Estimator (`DEC0010`), `MOD010` Data-Only Explainability Engine, `MOD011` Programmatically `EV`-Verified Reasoning Engine, `MOD012` Provenance-Stamped Report Generator (JSON/MD/HTML), `MOD013` 7-App Django/DRF REST API (`POST /cases`, `GET /cases/{id}`, `POST /cases/{id}/upload`, `GET /cases/{id}/{status,evidence,decision,explanation,report}`, `GET /health`, `GET /version`), `MOD014` 14-Page / 24-Component React UI, `MOD015` Append-Only Case Audit Trail (`CASExxxxxx`), `MOD016` Eight-Mode Failure Handler, `MOD017` Module Contract Validator, and `MOD018` Multimodal Extensibility Registry (`audio`/`video`/`text`).

### S4.2 Phase E14 Fault Matrix (`EVAL0007`) and 2,700-Case Multi-Specialist Benchmark (`EVAL0008`)

Sixteen deterministic fault scenarios (`08_Evaluation/forensic_analyst_eval/e14_case_results.csv`) passed all nine dimensions (`135` verified reasoning sentences, `0` ungrounded leaks, mean unloaded latency `60.02 ms`), complemented by `2,700` end-to-end single-specialist (`K = 1`) and cross-paradigm multi-specialist (`K = 3`: `MODEL0001` ResNet-50, `MODEL0003` EfficientNet-B4, `MODEL0004` ViT-B/16) benchmark investigations across nine tracks in `08_Evaluation/EVAL0008/abstention_by_track.csv` and `selective_risk_coverage.csv`.

---

## S5. Reproducibility Commands and Locked Environment

All experiments and verification checks execute deterministically under `Python 3.12`, `PyTorch 2.10.0+cu128`, `FastAI 2.8.7`, `Django 5.2.19`, `DRF 3.18.3`, `React 18.3`, `Vite 6`, and `Tailwind CSS 3.4` using the following repository-root commands:

```powershell
python 17_Automation/run_all_tests.py
python 11_AI_Forensic_System/evaluate_benchmark_abstention.py
python 17_Automation/verify_writing_consistency.py
python 17_Automation/build_camera_ready.py
python 09_Figures/scripts/render_figures.py
```
