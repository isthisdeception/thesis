# EXP0002 — Conclusions

**Status:** completed (2026-11-10). Not a failed experiment.

## Result

`MODEL0008` (ResNet-50, EXP0001's training standard) was trained on `DS0001 / v1.0 / PP0001 / SPLIT0002`, where `stable_diffusion` is absent from train and val.

On the 12 seen generators it performs like EXP0001: validation ROC-AUC **0.937** and balanced accuracy **0.859** at the validation-chosen threshold 0.442 (EXP0001: 0.934 and 0.856 on its own validation split). The expected-outcome bar (validation ROC-AUC ≥ 0.90) is met.

On the held-out generator it detects **15.2%** of Stable Diffusion fakes (293 of 1,923; 95% CI 13.7%–16.9%). Mean P(fake) on them is 0.182, close to the 0.146 of real validation images. On the 299 Stable Diffusion images of the EXP0001 test split, MODEL0001 (which saw the generator) detects 96.3% and MODEL0008 detects 13.7%; 247 images are caught only by MODEL0001 and none only by MODEL0008.

Exact values: `metrics/run_summary.json`, `08_Evaluation/EVAL0002/unseen_generator/`.

Best checkpoint is epoch 9 (validation loss 0.331). Training ran all 11 scheduled epochs (66.0 min, Tesla T4) without early stopping.

## What this experiment shows and does not show

- It shows that, for this baseline, detection of one generator depends almost entirely on having seen that generator in training: the same architecture, data pipeline, and schedule go from 96% to 15% recall on the same images when that generator is removed.
- It covers one held-out generator (DEC0007). Whether other generators behave the same is not tested.
- The held-out test split has no real images, so ROC-AUC and specificity on test are undefined. The ROC-AUC of 0.554 against validation real images is indicative only, because those images also set the threshold.
- Possible reasons (not tested): the features MODEL0008 uses for the 12 GAN/inpainting/transformer generators may not appear in diffusion outputs; or Stable Diffusion images may share low-level properties with the real sources. Phase E10/E11 and later model comparisons can test these.

## Next

STEP-048 comparison study. Any held-out claim for other generators needs its own experiment (DEC0007 future review).
