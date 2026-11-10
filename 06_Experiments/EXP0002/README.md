# Experiment: EXP0002

**Status:** ready (Checklist 5 PASS, 2026-11-10). Waiting for the Kaggle training session.

**Research Question:** How can we improve the cross-generator generalization of image-based AI face detection models to maintain high accuracy on unseen generative architectures?

**Hypothesis:** A ResNet-50 trained exactly like EXP0001 but without any Stable Diffusion images detects Stable Diffusion fakes less often than EXP0001, which saw that generator in training. The size of the drop is the unseen-generator result (Phase E9). No numeric target is set for it.

**Dataset:** `DS0001` v1.0, preprocessed by `PP0001`, split `SPLIT0002` (`logo`, seed 42, grouped by identity + generator, leakage PASS). `stable_diffusion` is held out: train 40,873 (19,629 fake / 21,244 real) and val 7,204 (3,448 / 3,756) contain the other 12 generators; test 1,923 is `stable_diffusion` fakes only.

**Model:** `MODEL0008` — ResNet-50 (torchvision, ImageNet-1k pretrained). Same architecture as `MODEL0001`; a separate ID because it is a separately trained model.

**Configuration:** [`config.yaml`](config.yaml), validated by `17_Automation/config_validation`. Identical to EXP0001 except experiment ID, model ID, split, purpose, expected outcome, and output locations (DEC0007). The learning rate 3.31e-4 is EXP0001's LR Finder value, reused so that the held-out generator is the only change.

**Expected outcome:** pipeline sanity only — validation ROC-AUC ≥ 0.90 on the seen generators.

**Planned results:** the canonical metric set on val (both classes) and recall on the held-out generator (test). Metrics that need real images (ROC-AUC, specificity) are undefined on this test split. The E9 analysis (`python -m generalization unseen`) compares recall on unseen Stable Diffusion with recall on the seen generators, and with EXP0001 on the same 299 Stable Diffusion images.

**Results:** pending.

**Kaggle:** [`KAGGLE_RUNBOOK.md`](KAGGLE_RUNBOOK.md). Artifacts go to the separate Kaggle dataset `isthisdeception/thesis-exp0002-artifacts`.

## Folder layout

| Path | Contents |
|------|----------|
| `config.yaml` | Experiment configuration (immutable once training starts) |
| `logs/`, `metrics/`, `predictions/`, `learning_curves/` | Written by the training pipeline, pushed from Kaggle |
| `checkpoints_info.md` | Checkpoint locations and resume instructions |
| `observations.md` | Running observations |
| `notebook/EXP0002_train.ipynb` | Kaggle session notebook; `notebook/checkpoints/` holds local binaries (Git-ignored) |
