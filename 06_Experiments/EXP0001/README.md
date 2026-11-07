# Experiment: EXP0001

**Status:** ready (Checklist 5 PASS, 2026-11-06; expected outcome approved in DEC0006, 2026-11-07) — not yet trained

**Research Question:** How can we improve the cross-generator generalization of image-based AI face detection models to maintain high accuracy on unseen generative architectures?

**Hypothesis:** An ImageNet-pretrained ResNet-50, fine-tuned with the FastAI training standard, separates real from AI-generated faces well when the test generators were also seen in training (SPLIT0001 test: ROC-AUC ≥ 0.95, balanced accuracy ≥ 0.90). This run is the fair reference point; it does not test cross-generator generalization itself, which is measured on the SPLIT0002 hold-out track.

**Dataset:** `DS0001` v1.0, preprocessed by `PP0001` (224 px PNG, ImageNet statistics applied at load time), split `SPLIT0001` (`grouped_random`, seed 42, grouped by identity + generator, leakage PASS). Partitions: train 34,993 (17,502 fake / 17,491 real), val 7,502 (3,719 / 3,783), test 7,505 (3,779 / 3,726). Processed images: Kaggle dataset `isthisdeception/ds0001-pp0001`.

**Model:** `MODEL0001` — ResNet-50 (torchvision, ImageNet-1k pretrained), from the approved STEP-032 shortlist.

**Configuration:** [`config.yaml`](config.yaml), validated by `17_Automation/config_validation`. Summary:

| Setting | Value |
|---------|-------|
| Image size / batch size | 224 / 64 |
| Schedule | `fine_tune`: 1 frozen epoch, then 10 unfrozen epochs |
| Optimizer | FastAI Adam, weight decay 0.01 |
| Learning rate | LR Finder (`valley`); 1.0e-3 placeholder until the suggestion is recorded |
| Loss | `CrossEntropyLossFlat` |
| Augmentation | `aug_transforms`: horizontal flip, rotate ≤ 10°, zoom ≤ 1.05, lighting ≤ 0.1, no warp |
| Precision | mixed (`to_fp16`) |
| Callbacks | per-epoch `SaveModelCallback` (with optimizer state), early stopping (patience 3 on `valid_loss`), `CSVLogger` |
| Hardware | Kaggle GPU T4, image v170 (`environment/versions.lock.md`) |
| Seed | 42 |

**Planned results:** the full canonical metric set from `05_Models/baseline_plan.md` on the SPLIT0001 test partition (ROC-AUC, PR-AUC, F1, balanced accuracy, MCC, precision, recall, specificity, FPR, FNR; plus accuracy, ECE, Brier), with the operating threshold chosen on the validation partition only.

**Results:** pending (training starts in STEP-039).

**Failures:** none yet.

**Observations:** see [`observations.md`](observations.md).

**Conclusion:** pending.

**Next Experiment:** `MODEL0002` Xception on the same frozen track (`DS0001 / v1.0 / PP0001 / SPLIT0001`), then `MODEL0003` EfficientNet-B4.

## Folder layout

| Path | Contents |
|------|----------|
| `config.yaml` | Experiment configuration (immutable once training starts) |
| `logs/` | Training logs, `CSVLogger` output, environment smoke output |
| `metrics/` | Per-epoch and final metric tables |
| `predictions/` | Validation/test prediction CSVs for the evaluation pipeline |
| `learning_curves/` | Learning-curve data (not rendered figures) |
| `checkpoints_info.md` | Checkpoint locations, policy, and resume instructions |
| `observations.md` | Running observations during setup and training |
| `notebook/` | Kaggle training notebook; `notebook/checkpoints/` holds local checkpoint binaries (Git-ignored) |
