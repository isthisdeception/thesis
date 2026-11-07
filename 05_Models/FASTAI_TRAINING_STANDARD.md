# FastAI Training Standard (Phase M3)

**Step:** STEP-034  
**Handbook:** Phase M3, Phase M4, Phase M6, Phase M7  
**Config template:** `18_Templates/config.yaml`  
**Validator:** `17_Automation/config_validation/`  
**Implementation:** `17_Automation/training/` (STEP-036)

## Purpose

This is the reference workflow every `EXPxxxx` training notebook follows. Each stage reads its parameters from the experiment's `config.yaml`; the notebook contains the workflow, the config contains every value. A parameter that appears as a literal in notebook code is a defect.

## Reference workflow

```
config validation → DataBlock → DataLoaders → Learner → callbacks → mixed precision
→ transfer learning (frozen head) → LR Finder → fit_one_cycle / fine_tune
→ unfreeze + fine-tune → export
```

| # | Stage | FastAI call | Config keys |
|---|-------|-------------|-------------|
| 0 | Config validation | `python -m config_validation 06_Experiments/EXPxxxx/config.yaml` | whole file |
| 1 | Seed | `set_seed(seed, reproducible=True)` | `random_seed` |
| 2 | DataBlock | `DataBlock(blocks=(ImageBlock, CategoryBlock), ...)` | `fastai.datablock`, `dataset.*`, `split.*` |
| 3 | Item transforms | `Resize(size, method=...)` | `fastai.item_tfms`, `image_size` |
| 4 | Batch transforms | `aug_transforms(...)`, `Normalize.from_stats(...)` | `augmentations.aug_transforms`, `fastai.normalize` |
| 5 | DataLoaders | `dblock.dataloaders(df, bs=..., num_workers=...)` | `batch_size`, `fastai.dataloaders` |
| 6 | Learner | `vision_learner(dls, arch, pretrained=..., loss_func=..., opt_func=..., metrics=..., wd=...)` | `model.*`, `loss_function`, `optimizer`, `metrics` |
| 7 | Callbacks | `SaveModelCallback`, `EarlyStoppingCallback`, `CSVLogger` | `fastai.callbacks` |
| 8 | Mixed precision | `learn.to_fp16()` | `fastai.mixed_precision` |
| 9 | LR Finder | `learn.lr_find(suggest_funcs=(valley,))` | `fastai.lr_finder`, `learning_rate` |
| 10 | Train | `learn.fine_tune(epochs, base_lr, freeze_epochs=...)` or `learn.fit_one_cycle(epochs, lr_max)` | `fastai.schedule`, `epochs`, `learning_rate.value` |
| 11 | Export | `learn.export("MODELxxxx_export.pkl")`, `torch.save(learn.model.state_dict(), "MODELxxxx_weights.pth")` | `fastai.export`, `outputs.*` |

## Stage rules

**Data (stages 2–5).** Items come from the split's `assignments.csv`; the splitter uses the `partition` column so train/val/test are exactly the registered split (`split.leakage_required: PASS`). Images are already 224 px on disk (PPMOD05), so `Resize` is only a safety clamp and must equal `image_size`. Augmentations run on the training set only. Normalization uses ImageNet statistics to match pretrained weights; it is never baked into the PNGs (`apply_on_disk: false`).

**Learner (stage 6).** The backbone comes from `model.backbone` and `model.source` (`torchvision` for ResNet, `timm` for Xception and EfficientNet). `model.architecture` must match the Model ID's row in `05_Models/candidate_models.csv` (or `model_registry.csv` once registered). Training-time metrics are cheap monitors; the full canonical metric set in `metrics.primary` is computed by the evaluation pipeline on saved predictions.

**Transfer learning and LR (stages 9–10).** Default schedule is `fine_tune`: `freeze_epochs` epochs with the pretrained body frozen (one-cycle, `pct_start` 0.99 as in FastAI's `fine_tune`), then unfreeze, halve the LR, and train `epochs` more with discriminative learning rates `slice(lr / lr_mult, lr)` using the configured `pct_start` and `div`. Run LR Finder once, write the suggested value into `learning_rate.value` with `source: lr_find`, commit the config, then train. The LR is never chosen inside the training cell.

**Callbacks and checkpoints (stage 7).** `fastai.callbacks.save_model` (`every_epoch: true`, `with_opt: true`) drives the project's `EpochCheckpointer`, which replaces FastAI's `SaveModelCallback`/`EarlyStoppingCallback` so that best-model tracking, early stopping, optimizer state, schedule position, and RNG all survive a terminated Kaggle session (Phase M7, `07_Checkpoints/checkpoint_policy.md`). Checkpoints go to `outputs.checkpoint_dir`; nothing is overwritten, and the manifest at `outputs.checkpoint_manifest` records checksums. `CSVLogger` writes the raw per-epoch log; the pipeline's own learning-curve files are the clean record.

**Export (stage 11).** Both `MODELxxxx_export.pkl` (FastAI inference) and `MODELxxxx_weights.pth` (plain PyTorch state dict) are produced from the best epoch's weights, alongside `EXPxxxx_best.pth` and `EXPxxxx_last.pth` (A.2 names). Binaries go to the artifact tier (`outputs.artifact_dataset_slug`), never to Git.

## Runtime fields

At session start, before training, the notebook fills `git_commit` (from `git rev-parse HEAD`) and `timestamp` (ISO-8601 with timezone), re-runs the validator in ready mode, and archives the config. After training starts the config is never edited (Template 8 Definition of Done).

## Fairness

Changing any value that `05_Models/baseline_plan.md` lists as a fairness invariant (dataset, version, pipeline, split, seed policy, augmentation family, loss/optimizer/epoch-budget family, metric set, threshold policy) requires a different `study_track`, usually `ablation`. The validator enforces the registered IDs, the canonical metric set, and the validation-only threshold policy; the study-track label is the author's responsibility.
