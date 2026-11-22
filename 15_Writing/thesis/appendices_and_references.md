# Appendices and References

> **Version:** `0.2.0` | **Status:** Revised (W13 Reviewed; Pending Supervisor Sign-off) | **Last Updated:** 2026-11-22
> **Writing Units:** `WR0039`, `WR0040`
> **Traceability:** Compiled directly from canonical registries and specifications: `03_Datasets/metadata/datasets.csv`, `03_Datasets/reports/split_report.md`, `04_Preprocessing/preprocessing_registry.csv`, `01_Project_Management/decision_log/` (`DEC0001`–`DEC0010`), `11_AI_Forensic_System/module_registry.csv`, `16_Documentation/api_guide.md`, `02_Literature/metadata/papers.csv`, `02_Literature/metadata/papers.bib`, `15_Writing/references/references.bib`, and `15_Writing/shared/knowledge_index.csv` (`KI0004`, `KI0005`, `KI0014`, `KI0015`, `KI0019`, `KI0024`–`KI0026`).

---

## Appendix A: Dataset Cards, Preprocessing Parameters, Split Fingerprints, Decision Log Index, and Gate Audit Trail

### A.1 Registered Dataset and Preprocessing Summary (`WR0039`; `KI0014`; `KI0015`)

All five public datasets (`DS0001`–`DS0005`, version `v1.0`) and six preprocessing pipelines (`PP0001`–`PP0006`, with `PP0004` superseded by `PP0006`) share deterministic seed `42`, bilinear 224x224 RGB PNG standardization, EXIF stripping, forbidden generative denoising, deferred ImageNet normalization (`apply_on_disk=false`), and zero-leakage split verification (`SPLIT0001`, `SPLIT0002`) (`03_Datasets/metadata/datasets.csv`; `04_Preprocessing/preprocessing_registry.csv`; `03_Datasets/reports/split_report.md`; `FIG0001`–`FIG0010`; `P0003`; `P0016`; `P0023`):

| Output ID | Dataset / License | Pipeline & Key Override | `SPLIT0001` (Train / Val / Test) | `SPLIT0002` LOGO (Train / Val / Test) | Leakage |
|---|---|---|---|---|---|
| `DS0001_PP0001` | `DS0001` ArtiFact face subset (MIT) | `PP0001` (`min_side=64`, default) | `34,993 / 7,502 / 7,505` (`grouped_random`) | `40,873 / 7,204 / 1,923` (`stable_diffusion` out) | PASS |
| `DS0002_PP0002` | `DS0002` DiFF official test (CC BY-NC 4.0) | `PP0002` (`exclude_list_DS0002.csv`, 1,593 corrupt excluded) | `36,985 / 7,103 / 7,364` (`grouped_random`) | `39,718 / 6,087 / 5,647` (`Midjourney` out) | PASS |
| `DS0003_PP0003` | `DS0003` 140k Real & Fake (CC BY-NC-SA 4.0) | `PP0003` (default) | `101,999 / 18,001 / 20,000` (`official_holdout`) | `59,499 / 10,501 / 70,000` (`stylegan` out) | PASS |
| `DS0004_PP0006` | `DS0004` Synthbuster (CC BY 4.0) | `PP0006` (`max_side=8192`, supersedes `PP0004`) | `7,001 / 1,498 / 1,500` (`grouped_random`) | `7,648 / 1,351 / 1,000` (`dalle3` out) | PASS |
| `DS0005_PP0005` | `DS0005` FairFace (CC BY 4.0) | `PP0005` (default) | `64,372 / 11,364 / 21,962` (`official_holdout`) | `68,416 / 14,641 / 14,641` (`grouped_random`) | PASS |

### A.2 Human-Ratified Decision Log Index (`DEC0001`–`DEC0010`)

Every irreversible scientific and architectural choice in this research is recorded in `01_Project_Management/decision_log/` and ratified by the human research authority (`WR0039`; `KI0004`; `EXP0001`–`EXP0006`):

| Decision ID | Date | Ratified Choice | Key Evidence / Impact |
|---|---|---|---|
| `DEC0001` | 2026-07-30 | MIT License | Permissive open-source dissemination (`LICENSE`) |
| `DEC0002` | 2026-07-30 | Option 1: Generalization Focus | Anchors primary RQ and Phase L2 search strategy |
| `DEC0003` | 2026-07-31 | Direction 1: Evidence-Driven Forensic Analysis System | Declares the AI Forensic Analyst as primary contribution (`GAP0001`, `GAP0003`) |
| `DEC0004` | 2026-08-01 | Public-Only Multi-Dataset Strategy (`DEF-003` resolved) | Selects `DS0001`–`DS0005`; excludes gated/broken academic hosts |
| `DEC0005` | 2026-08-01 | Replace EULA-gated AI-Face-FairnessBench with FairFace | Enforces CC BY 4.0 open preprocessing for `DS0005` |
| `DEC0006` | 2026-11-07 | `EXP0001` Pre-Training Sanity Thresholds | Locks diagnostic bar (`ROC-AUC >= 0.95`, `BA >= 0.90`, `< 0.90` trigger) |
| `DEC0007` | 2026-11-10 | Phase E9 `stable_diffusion` LOGO (`EXP0002`) + 10k FairFace E8 sample | Scopes unseen-generator evaluation (`SPLIT0002`, seed 42) |
| `DEC0008` | 2026-11-13 | Four One-Factor Ablations (`EXP0003`–`EXP0006`) | Isolates seed, augmentation, pretraining, and 160 px size (`TAB0002`, `TAB0003`) |
| `DEC0009` | 2026-11-18 | `rule_based` Reliability-Weighted Fusion (`DEF-004` resolved) | Locks `MOD007` weights (`1.0`/`0.6`/`0.3`), E4 threshold, contested band `< 0.5` |
| `DEC0010` | 2026-11-18 | `e4_calibrated_v1` Confidence & 4-Way Decision Rules | Locks `MOD009` val-calibrated formulas and `MOD008` `Real`/`Fake`/`Inconclusive`/`Unknown` rules |

### A.3 Passed Quality Gate Audit Trail (`WR0039`; `KI0026`)

Ten consecutive quality gates passed prior to thesis drafting (`01_Project_Management/dashboard_status.md`): Literature Gate (Checklist 2, `02_Literature/literature_audit.md`), Dataset Readiness Gate (Checklist 3, `03_Datasets/reports/dataset_audit.md`), Preprocessing Gate (Checklist 4, `04_Preprocessing/reports/preprocessing_audit.md`), Experiment Readiness and Training Completion Gates (Checklists 5 and 6, `EXP0001`), Evaluation Gate (Checklist 8, `08_Evaluation/evaluation_audit.md`), Forensic Analyst Gate + Phase E14 (Checklist 9, `08_Evaluation/forensic_audit.md`), Frontend Gate (Checklist 10, `12_Web/frontend_audit.md`), Backend Gate (Checklist 11, `13_Backend/backend_audit.md`), and Documentation Gate (Checklist 12, `16_Documentation/documentation_audit.md`).

---

## Appendix B: Forensic Module Registry, REST API Contract, and Verified Bibliography

### B.1 Implemented AI Forensic Analyst Module Registry (`MOD001`–`MOD018`)

All 18 modules are tracked at version `0.1.0` with status `implemented` in `11_AI_Forensic_System/module_registry.csv` (`WR0040`; `KI0019`; `EXP0001`):

| Module ID | Responsibility | Primary Inputs | Primary Outputs | Dependencies |
|---|---|---|---|---|
| `MOD001` | Receive upload and persist metadata | Case ID and upload bytes | `input_metadata.json`, `input_id` | `MOD016` |
| `MOD002` | Validate accepted image before collectors run | `input_id` and stored file | Validation status & measurements | `MOD001`, `MOD016` |
| `MOD003` | Execute 9 independent non-DL collectors | Validated input & collector list | Collector evidence items | `MOD001`, `MOD002`, `MOD005`, `MOD016` |
| `MOD004` | Run registered detector and emit probability | `input_id` and `model_id` | `deep_learning_prediction` item | Model Registry, `MOD005`, `MOD016` |
| `MOD005` | Assign immutable `EVxxxxxx` IDs | Collector evidence items | Append-only `evidence_registry.csv` | `MOD003` |
| `MOD006` | Grade item reliability & flag conflicts | Evidence rows by `EV` ID | Non-destructive reliability rows | `MOD005`, `MOD016` |
| `MOD007` | Fuse validated evidence via `FusionStrategy` | Validated `EV` rows & strategy ID | `fused_conclusion` item | `MOD005`, `MOD006`, `MOD016` |
| `MOD008` | Emit 4-way verdict from validated evidence | Fused & confidence `EV` IDs | `decision.json` | `MOD007`, `MOD009`, `MOD016` |
| `MOD009` | Compute 4 E4-calibrated confidence metrics | Validated `EV` IDs | `confidence` item | `MOD004`–`MOD006`, `MOD016` |
| `MOD010` | Assemble Policy A.9 data-only explanations | `explainability_input` `EV` items | `explanation.json` | `MOD003`, `MOD005`, `MOD006`, `MOD016` |
| `MOD011` | Generate & verify `EV`-grounded reasoning | Validated `EV` rows | `reasoning.json` | `MOD005`–`MOD007`, `MOD009`, `MOD016` |
| `MOD012` | Export provenance-stamped Template 24 reports | Decision, explanation, reasoning, stamps | JSON, Markdown, HTML reports | `MOD008`, `MOD010`, `MOD011`, `MOD015`, `MOD016` |
| `MOD013` | Expose investigation via 10 REST endpoints | HTTP requests | Unchanged pipeline records (`13_Backend/`) | `MOD001`, `MOD012`, `MOD015`, `MOD016` |
| `MOD014` | Render 14-page interactive forensic UI | API JSON responses | 9-stage progress & 4-way workspace (`12_Web/`) | `MOD013` |
| `MOD015` | Append immutable case audit trail | Input, evidence, decision, version, errors | `case_registry.csv` row | `MOD001`, `MOD005`, `MOD008`, `MOD016` |
| `MOD016` | Record 8 canonical structured failure modes | Failure name, module ID, case ID | `FailureRecord` JSON | none |
| `MOD017` | Maintain module specs and registry | `specs/MODxxx_spec.md` | Validated `module_registry.csv` | specs |
| `MOD018` | Govern new modality extensions | Collector or strategy proposal | Updated collector/strategy registry | `MOD003`, `MOD007`, `MOD011`, `MOD017` |

### B.2 Canonical REST API Surface (`MOD013`; `WR0040`; `KI0024`; `KI0025`)

The 10 REST endpoints mounted identically at `/api/v1/` and `/` in `13_Backend/apps/api/urls.py` and consumed by `12_Web/src/api/forensicApi.js` are: `POST /cases`, `GET /cases/{id}`, `POST /cases/{id}/upload`, `GET /cases/{id}/status`, `GET /cases/{id}/evidence`, `GET /cases/{id}/decision`, `GET /cases/{id}/explanation`, `GET /cases/{id}/report`, `GET /health`, and `GET /version` (`16_Documentation/api_guide.md`). All error responses return structured `MOD016` envelopes without stack traces.

### B.3 Verified Bibliography (`P0001`–`P0028`)

All 28 cited references trace one-to-one to `02_Literature/metadata/papers.csv`, `02_Literature/metadata/papers.bib`, and `15_Writing/references/references.bib`, supporting `CLAIM0001`–`CLAIM0008` and `TAB0001` (`WR0040`; `KI0005`):

1. **`P0001`** (`Cho_2026`): J. Cho, D. Kong, J. Nam, and H. Cho, "A Synthetic Defect Image Generation Method for Enhanced Industrial Defect Detection Based on Inpainting Diffusion and Context-aware Mask Generation," *Journal of Intelligent Manufacturing*, 2026. DOI: `10.1007/s10845-026-02915-2`.
2. **`P0002`** (`Taeb_2022`): M. Taeb and H. Chi, "Comparison of Deepfake Detection Techniques through Deep Learning," *Journal of Cybersecurity and Privacy*, 2022. DOI: `10.3390/jcp2010007`.
3. **`P0003`** (`Bammey_2024`): Q. Bammey, "Synthbuster: Towards Detection of Diffusion Model Generated Images," *IEEE Open Journal of Signal Processing*, 2024. DOI: `10.1109/OJSP.2023.3337714`.
4. **`P0004`** (`Ghani_2024`): M. A. N. Ul Ghani, K. She, M. A. Rauf, S. Khan, J. A. Khan, E. A. Aldakheel, and D. S. Khafaga, "Enhancing Security and Privacy in Distributed Face Recognition Systems Through Blockchain and GAN Technologies," *Computers, Materials & Continua*, 2024. DOI: `10.32604/cmc.2024.049611`.
5. **`P0005`** (`Guarnera_2020`): L. Guarnera, O. Giudice, and S. Battiato, "Fighting Deepfake by Exposing the Convolutional Traces on Images," *IEEE Access*, 2020. DOI: `10.1109/ACCESS.2020.3023037`.
6. **`P0006`** (`Zeng_2025`): W. Zeng, T. Xie, Y. Liu, and Y. Peng, "Diffusion-generated face image identification technique based on diffusion reconstruction error feature," *International Journal of Information and Communication Technology*, 2025. DOI: `10.1504/IJICT.2025.10071014`.
7. **`P0007`** (`Khan_2024`): S. A. Khan and D.-T. Dang-Nguyen, "Deepfake Detection: Analyzing Model Generalization Across Architectures, Datasets, and Pre-Training Paradigms," *IEEE Access*, 2024. DOI: `10.1109/ACCESS.2023.3348450`.
8. **`P0008`** (`Pasquini_2023`): C. Pasquini, F. Laiti, D. Lobba, G. Ambrosi, G. Boato, and F. De Natale, "Identifying Synthetic Faces through GAN Inversion and Biometric Traits Analysis," *Applied Sciences*, 2023. DOI: `10.3390/app13020816`.
9. **`P0009`** (`Abbas_2026`): F. Abbas and A. Taeihagh, "Improved latent diffusion-based IC-DGAN framework for high-resolution multi-feature and expression manipulation," *Neural Networks*, 2026. DOI: `10.1016/j.neunet.2025.108199`.
10. **`P0010`** (`Giudice_2021`): O. Giudice, L. Guarnera, and S. Battiato, "Fighting Deepfakes by Detecting GAN DCT Anomalies," *Journal of Imaging*, 2021. DOI: `10.3390/jimaging7080128`.
11. **`P0011`** (`Safwat_2024`): S. Safwat, A. Mahmoud, I. E. Fattoh, and F. Ali, "Hybrid Deep Learning Model Based on GAN and RESNET for Detecting Fake Faces," *IEEE Access*, 2024. DOI: `10.1109/ACCESS.2024.3416910`.
12. **`P0012`** (`Ul_Ghani_2024`): M. A. N. Ul Ghani, K. She, M. A. Rauf, M. Alajmi, Y. Y. Ghadi, and A. Algarni, "Securing Synthetic Faces: A GAN-blockchain Approach to Privacy-Enhanced Facial Recognition," *Journal of King Saud University - Computer and Information Sciences*, 2024. DOI: `10.1016/j.jksuci.2024.102036`.
13. **`P0013`** (`Sharma_2025`): P. Sharma, M. Kumar, and H. K. Sharma, "A robust ensemble model for Deepfake detection of GAN-generated images on social media," *Discover Computing*, 2025. DOI: `10.1007/s10791-025-09538-w`.
14. **`P0014`** (`Guarnera_2022`): L. Guarnera et al., "The Face Deepfake Detection Challenge," *Journal of Imaging*, 2022. DOI: `10.3390/jimaging8100263`.
15. **`P0015`** (`Xue_2023`): Z. Xue, X. Jiang, Q. Liu, and Z. Wei, "Global-Local Facial Fusion Based GAN Generated Fake Face Detection," *Sensors*, 2023. DOI: `10.3390/s23020616`.
16. **`P0016`** (`Altamimi_2026`): O. Altamimi, M. Al-Nashash, and M. Abdullah, "Comparative Detection of GAN and Diffusion Model Generated Faces: Bias, Robustness, and Explainability," *Proc. 17th International Conference on Information and Communication Systems (ICICS)*, ACM, 2026. DOI: `10.1145/3812734.3813716`.
17. **`P0017`** (`Preeti_2023`): Preeti, M. Kumar, and H. K. Sharma, "A GAN-Based Model of Deepfake Detection in Social Media," *Procedia Computer Science*, 2023. DOI: `10.1016/j.procs.2023.01.191`.
18. **`P0018`** (`Guarnera_2024`): L. Guarnera, O. Giudice, and S. Battiato, "Mastering Deepfake Detection: A Cutting-Edge Approach to Distinguish GAN and Diffusion-Model Images," *ACM Transactions on Multimedia Computing, Communications, and Applications*, 2024. DOI: `10.1145/3652027`.
19. **`P0019`** (`Alkishri_2024`): W. Alkishri, S. Widyarto, and J. H. Yousif, "Evaluating the Effectiveness of a Gan Fingerprint Removal Approach in Fooling Deepfake Face Detection," *Journal of Internet Services and Information Security*, 2024. DOI: `10.58346/JISIS.2024.I1.006`.
20. **`P0020`** (`Nadimpalli_2024`): A. V. Nadimpalli and A. Rattani, "ProActive DeepFake Detection Using GAN-based Visible Watermarking," *ACM Transactions on Multimedia Computing, Communications, and Applications*, 2024. DOI: `10.1145/3625547`.
21. **`P0021`** (`Arshed_2024`): M. A. Arshed, S. Mumtaz, M. Ibrahim, C. Dewi, M. Tanveer, and S. Ahmed, "Multiclass AI-Generated Deepfake Face Detection Using Patch-Wise Deep Learning Model," *Computers*, 2024. DOI: `10.3390/computers13010031`.
22. **`P0022`** (`Gragnaniello_2022`): D. Gragnaniello, F. Marra, and L. Verdoliva, "Detection of AI-Generated Synthetic Faces," *Advances in Computer Vision and Pattern Recognition*, Springer, 2022. DOI: `10.1007/978-3-030-87664-7_9`.
23. **`P0023`** (`Cheng_2024`): H. Cheng, Y. Guo, T. Wang, L. Nie, and M. Kankanhalli, "Diffusion Facial Forgery Detection," *Proc. 32nd ACM International Conference on Multimedia (ACM MM)*, 2024. DOI: `10.1145/3664647.3680797`.
24. **`P0024`** (`Heidari_2023`): A. Heidari, N. Jafari Navimipour, H. Dag, and M. Unal, "Deepfake detection using deep learning methods: A systematic and comprehensive review," *WIREs Data Mining and Knowledge Discovery*, 2023. DOI: `10.1002/widm.1520`.
25. **`P0025`** (`Melnik_2024`): A. Melnik et al., "Face Generation and Editing With StyleGAN: A Survey," *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 2024. DOI: `10.1109/TPAMI.2024.3350004`.
26. **`P0026`** (`Edwards_2024`): P. Edwards, J.-C. Nebel, D. Greenhill, and X. Liang, "A Review of Deepfake Techniques: Architecture, Detection, and Datasets," *IEEE Access*, 2024. DOI: `10.1109/ACCESS.2024.3477257`.
27. **`P0027`** (`Dang_2023`): M. Dang and T. N. Nguyen, "Digital Face Manipulation Creation and Detection: A Systematic Review," *Electronics*, 2023. DOI: `10.3390/electronics12163407`.
28. **`P0028`** (`Malik_2022`): A. Malik, M. Kuribayashi, S. M. Abdullahi, and A. N. Khan, "DeepFake Detection for Human Face Images and Videos: A Survey," *IEEE Access*, 2022. DOI: `10.1109/ACCESS.2022.3151186`.
