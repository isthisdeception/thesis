# EXP0001 — Conclusions

**Status:** completed (2026-11-08). Not a failed experiment.

## Result

`MODEL0001` (ImageNet-pretrained ResNet-50) separates real from AI-generated faces on the in-distribution test partition of `DS0001 / v1.0 / PP0001 / SPLIT0001`.

Test ROC-AUC is **0.926** and balanced accuracy is **0.848** at the validation-chosen threshold 0.395. PR-AUC is 0.935, F1 is 0.844, and MCC is 0.698. Exact values are in `metrics/test_metrics.json`. They are not restated anywhere else as a second source.

Best checkpoint is epoch 7 (validation loss 0.342). Training ran all 11 scheduled epochs (1 frozen + 10 unfrozen, 36.7 min, Tesla T4) and early stopping fired on the last epoch.

## Against the pre-registered bar

DEC0006 asked for test ROC-AUC ≥ 0.95 and balanced accuracy ≥ 0.90, and said a ROC-AUC below 0.90 would mean a pipeline problem. This run is below the sanity bar and above 0.90. DEC0006 says a miss does not invalidate the run. Nothing in the config, split, or metrics was edited after the run.

## What this experiment does not show

`SPLIT0001` puts every generator in train, validation, and test. The score is not evidence of cross-generator generalization. That question belongs to `SPLIT0002`. The run also does not measure demographic bias, compression robustness, or a comparison against Xception or EfficientNet-B4.

None of `CLAIM0001`–`CLAIM0008` is updated. Those claims are about diffusion shift, spectral cues, shortcuts, source attribution, physiology, compression, ViTs, or reconstruction error. This baseline tests none of them.

## Next

Register the evaluation (STEP-041 onward) from the saved test predictions. `MODEL0002` (Xception), when it is run, must use this same frozen track and metric set.
