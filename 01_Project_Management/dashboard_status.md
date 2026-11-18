# Project Dashboard

## Active Phase
- Current Phase: AI Forensic Analyst (PART 9)
- Active Step: **STEP-059** — Report generator, audit trail, failure handling + Forensic Gate (Checklist 9 + E14)
- Evaluation gate (Checklist 8): PASS, human-confirmed 2026-11-17. Evidence is in `08_Evaluation/evaluation_audit.md`.
- Registered Datasets: DS0001–DS0005 (`Ready=yes`, version v1.0)
- Registered Pipelines: PP0001–PP0003, PP0005–PP0006 (`complete`); PP0004 superseded
- Registered Splits: 10 splits across 5 outputs (`dataset_registry.csv` + `split_registry.csv`)

## Progress
- Literature Gate (Checklist 2): PASS
- Dataset Readiness (Checklist 3): PASS (human-confirmed 2026-09-01)
- Preprocessing (Checklist 4): PASS (human-confirmed 2026-09-01)
- Preprocessing design (STEP-025): COMPLETE
- Preprocessing modules (STEP-026): COMPLETE (34 unit tests)
- Preprocessing execution (STEP-027): COMPLETE
- Split generation (STEP-028): COMPLETE — leakage checks PASS
- FastAI prep + versioning + master registry (STEP-029): COMPLETE
- Environment lock (STEP-030): COMPLETE — Kaggle GPU v170 (Python 3.12, torch 2.10.0+cu128, fastai 2.8.7)
- Kaggle dataset upload + sync setup (STEP-031): COMPLETE — dry-run verified; shared artifact dataset created
- Candidate model discovery (STEP-032): COMPLETE — approved shortlist = ResNet-50, Xception, EfficientNet-B4
- Baseline strategy + fairness invariants (STEP-033): COMPLETE — EXP0001 fixed to ResNet-50 on DS0001/v1.0/PP0001/SPLIT0001
- Config system + FastAI training standard (STEP-034): COMPLETE — `config.yaml` template finalized; config validator (47 unit tests)
- Experiment readiness (STEP-035): COMPLETE — `EXP0001` scaffolded, config validator PASS, Checklist 5 PASS, registry `Status=ready`
- Training pipeline package (STEP-036): COMPLETE — `17_Automation/training/`, thin EXP0001 notebook, end-to-end smoke test PASS (CPU)
- Checkpoint system (STEP-037): COMPLETE — full-state recovery checkpoints, SHA-256 manifests, never-overwrite, resume verified by interruption tests
- Logging system (STEP-038): COMPLETE — live session-tagged epoch/batch CSVs, event log, hyperparameter records, warning capture, binary guard on metadata push
- Baseline training (STEP-039): COMPLETE — EXP0001 on Kaggle, test ROC-AUC 0.926, balanced accuracy 0.848 (below DEC0006 sanity bar, above 0.90)
- Training completion (STEP-040): COMPLETE — MODEL0001 registered, Checklist 6 PASS
- Evaluation inputs (STEP-041): COMPLETE — confusion, ROC, PR, and calibration tables derived from the saved predictions. Grad-CAM maps are not in Git. The eight-case list is `08_Evaluation/EXP0001/gradcam_sample.csv`.
- Prediction validation (STEP-042): COMPLETE — EVAL0001, E1–E2 PASS. Counts, ids, labels, and probabilities match the split.
- Classification metrics (STEP-043): COMPLETE — EVAL0001 E3 suite in `08_Evaluation/EVAL0001/classification_metrics.csv`. Test MCC 0.698, PR-AUC 0.935, FNR 0.183 vs FPR 0.120.
- Calibration & threshold analysis (STEP-044): COMPLETE — test ECE 0.052, MCE 0.154, Brier 0.113. Frozen threshold 0.395 kept for reporting; screening (0.089) and flag-for-review (0.629) points chosen on val. Figure specs FIG0011–FIG0013.
- Confusion & failure analysis (STEP-045): COMPLETE — `08_Evaluation/EVAL0001/failure_analysis.md`. Missed fakes concentrate in StyleGAN3, Projected GAN, StyleGAN2, MAT (FNR 38–44%); MetFaces real images have FPR 36.7%. Compression, quality, identity, lighting not assessable from metadata. Figure specs FIG0014–FIG0015.
- Robustness evaluation (STEP-046): COMPLETE — Kaggle T4, 54 conditions × 7505 test images; clean check PASS. Blur, downscaling, low-quality uploads, strong noise, and JPEG 10 push balanced accuracy to ~0.50 (nearly every image called fake). Brightness, contrast, colour, and small rotations cost under 0.10. `08_Evaluation/EVAL0001/robustness/robustness_report.md`; figure specs FIG0016–FIG0017.
- Cross-dataset (STEP-047, E8): DONE — MODEL0001 at its frozen threshold. Unseen-generator fakes missed 48% (DS0002 diffusion faces 50%) vs 18% in-distribution; StyleGAN-family fakes missed 9%. Real images from other sources mostly flagged as fake: FPR 30% (DS0003 FFHQ), 77% (DS0004 scenes), 83% (DS0005 FairFace). DS0004 ROC-AUC 0.52. `08_Evaluation/EVAL0001/generalization/cross_dataset_report.md`.
- Ablation study (STEP-048): DONE — four one-factor runs of EXP0001 (DEC0008). Seed change (EXP0003) moves test ROC-AUC by +0.001. No augmentation (EXP0004) −0.034. No ImageNet pretraining (EXP0005) −0.224. Image size 160 (EXP0006) −0.038. `08_Evaluation/ablations/ablation_report.md`.
- Statistical testing (STEP-049): DONE — 10,000 paired bootstrap resamples (seed 49) and exact McNemar on the 7505 SPLIT0001 test images. EXP0003 is not distinguishable from EXP0001 (ROC-AUC +0.001, 95% CI includes 0; McNemar p 0.96; decision agreement 0.933). On this split the three factor runs are lower: no augmentation −0.034, no pretraining −0.224, image size 160 −0.038; each Bonferroni-adjusted 98.3% CI excludes 0. No superiority claim. Wilcoxon across seeds not run (2 seeds; the test needs 6). `08_Evaluation/statistics/statistics_report.md`.
- Comparison and evaluation gate (STEP-050): DONE — ranked table is EXP0001 and EXP0003–EXP0006 (same dataset, pipeline, and SPLIT0001). EXP0002 is excluded (SPLIT0002). Publication specs FIG0021–FIG0025 and TAB0002–TAB0003 are data only. Checklist 8 PASS, human-confirmed 2026-11-17. `08_Evaluation/comparison_report.md`, `08_Evaluation/evaluation_audit.md`.
- Forensic architecture (STEP-051): DONE — specs for MOD001–MOD018, `EvidenceCollector` and `FusionStrategy`, and the evidence schema. The detector does not decide. The decision module reads validated evidence ids. `11_AI_Forensic_System/architecture.md`. No module code yet.
- Input and validation (STEP-052): DONE — MOD001 stores an upload as `input_metadata.json` and does not keep a rejected file. MOD002 checks format, corruption, channels, resolution, compression, noise, missing pixels, and face availability, and writes a MOD016 failure instead of continuing. `11_AI_Forensic_System/input_management/`, `image_validation/`.
- Evidence collectors (STEP-053): DONE — nine collectors run only after validation passes. None imports another. A failure or an unknown name leaves the others in place. The detector collector is not in this set. `11_AI_Forensic_System/evidence/`.
- Deep learning specialist (STEP-054): DONE — MOD004 reads the model id from configuration and the export pointer from `model_registry.csv`. It records the fake-class probability, optional embedding, and execution time. It does not apply the threshold or choose Real or Fake. A missing export yields `model_unavailable`. `evidence/collectors/deep_learning_specialist/`.
- Evidence registry and validation (STEP-055): DONE — each item receives an `EVxxxxxx` id in an append-only registry. Validation appends a reliability row (`high`, `medium`, `low`, or `unusable`) and leaves the collector row unchanged. Empty confidence stays empty. Conflicting items both remain and cite each other. `evidence/registry/`, `evidence/validation/`.
- Evidence fusion (STEP-056): DONE — MOD007 runs the strategy named in `fusion/fusion_config.json` (`rule_based`, DEF-004). Reliability weights high 1.0 / medium 0.6 / low 0.3; the detector probability is compared with its recorded threshold; other evidence types are cited as context. Output is one `fused_conclusion` item (lean `positive_class`, `negative_class`, `contested`, or `no_directional_evidence`, rationale citing `EV` ids), registered by MOD005 and validated by MOD006. No decision word. Unknown strategy id → MOD016, no fallback. Rule table approved in DEC0009 (human-confirmed 2026-11-18). 14 tests. `11_AI_Forensic_System/fusion/`.
- Decision and confidence (STEP-057): DONE — MOD009 (`confidence/`) computes `prediction_confidence` (E4 `EVAL0001` validation-split empirical accuracy at the frozen threshold, distinct from raw $P(\text{fake})$), `evidence_confidence`, `system_confidence`, and `decision_confidence`, and registers a validated `confidence` item without modifying collector rows. MOD008 (`decision/`) reads only the validated `fused_conclusion` and `confidence` `EV` ids (never the image) and writes `decision.json` (`Real`, `Fake`, `Inconclusive`, or `Unknown`, plus `reasoning_path` and `decision_metadata`). Missing detector → `Unknown`; conflicting evidence or low `decision_confidence` → `Inconclusive`. Formula and rules approved in DEC0010 (human-confirmed 2026-11-18). 7 new tests (44 total). `11_AI_Forensic_System/confidence/`, `11_AI_Forensic_System/decision/`.
- Explainability and reasoning (STEP-058): DONE — MOD010 (`explainability/`) assembles data-only `explanation.json` (`grad_cam`, `attention_maps`, `saliency`, `integrated_gradients`; future `shap`, `lime`, `counterfactuals` reserved), marking unrecorded methods `"no_data"` (`data: null`) and refusing rendered images (A.9) or decision words. MOD011 (`reasoning/`) writes `reasoning.json` from validated evidence rows and verifies every sentence against its cited `EV` ids and recorded values, rejecting untied or ungrounded sentences via MOD016. 7 new tests (51 total). `11_AI_Forensic_System/explainability/`, `11_AI_Forensic_System/reasoning/`.
- Unseen generator (STEP-047, E9): DONE — EXP0002 / MODEL0008 (EXP0001 settings, Stable Diffusion held out; DEC0007). Val ROC-AUC 0.937 on seen generators; held-out Stable Diffusion recall 15.2% vs 83.3% for seen generators. Same 299 images: MODEL0001 96.3%, MODEL0008 13.7%. `08_Evaluation/EVAL0002/unseen_generator/unseen_report.md`. STEP-047 COMPLETE.
- `Ready=yes`

## Health
- Risk Indicators: Amber on DS0002 (processed 51452 after 5608 PP exclusions; raw untouched)
- Storage Tier Compliance: Enforced (processed images → Kaggle only)
- Publication Readiness: Dataset + Preprocessing phases complete (Checklists 3 & 4 PASS)
