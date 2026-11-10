# Unseen-Generator Evaluation: EVAL0002

**Experiment:** EXP0002 (MODEL0008), trained on DS0001_PP0001_SPLIT0002 without stable_diffusion  
**Phase:** E9  
**Date:** 2026-11-10

Threshold 0.4420, chosen on the experiment's val split (no held-out images). Source: `08_Evaluation/EXP0002/predictions.csv`.

Leakage check PASS: held-out generator(s) absent from train and val. Training generators: cips, face_synthetics, gansformer, lama, mat, projected_gan, sfhq, stargan, stylegan1, stylegan2, stylegan3, taming_transformer.

## Detection

| Group | Images | Role | n | Detected | 95% CI | Mean P(fake) |
|---|---|---|---|---|---|---|
| stable_diffusion | fake | unseen (test) | 1923 | 15.2% (recall) | 13.7%–16.9% | 0.182 |
| cips | fake | seen (val) | 290 | 100.0% (recall) | 98.7%–100.0% | 0.986 |
| face_synthetics | fake | seen (val) | 290 | 98.3% (recall) | 96.0%–99.3% | 0.963 |
| gansformer | fake | seen (val) | 265 | 92.8% (recall) | 89.1%–95.4% | 0.883 |
| lama | fake | seen (val) | 285 | 75.4% (recall) | 70.1%–80.1% | 0.689 |
| mat | fake | seen (val) | 292 | 65.1% (recall) | 59.4%–70.3% | 0.590 |
| projected_gan | fake | seen (val) | 295 | 64.1% (recall) | 58.4%–69.3% | 0.610 |
| sfhq | fake | seen (val) | 287 | 98.3% (recall) | 96.0%–99.3% | 0.946 |
| stargan | fake | seen (val) | 316 | 100.0% (recall) | 98.8%–100.0% | 0.993 |
| stylegan1 | fake | seen (val) | 287 | 84.3% (recall) | 79.7%–88.1% | 0.758 |
| stylegan2 | fake | seen (val) | 296 | 66.9% (recall) | 61.3%–72.0% | 0.650 |
| stylegan3 | fake | seen (val) | 271 | 60.1% (recall) | 54.2%–65.8% | 0.554 |
| taming_transformer | fake | seen (val) | 274 | 93.1% (recall) | 89.4%–95.5% | 0.874 |
| all seen generators | fake | seen (val) | 3448 | 83.3% (recall) | 82.0%–84.5% | 0.793 |
| real | real | real (val) | 3756 | 88.6% (specificity) | 87.5%–89.5% | 0.146 |

- `stable_diffusion` (unseen): 15.2% detected, against 83.3% for seen generators on val.
- ROC-AUC of unseen test fakes against val real images: 0.5542. Indicative only: those real images also set the threshold.

## Same images, generator seen vs unseen

`MODEL0001 (EXP0001)` saw the generator in training; MODEL0008 did not. Same test images, each model at its own threshold.

| Generator | n | Recall (seen in training) | Recall (unseen) | Both | Only seen-model | Only unseen-model | Neither |
|---|---|---|---|---|---|---|---|
| stable_diffusion | 299 | 96.3% | 13.7% | 41 | 247 | 0 | 11 |

## Limits

- One held-out generator (stable_diffusion); other generators were not held out (decision recorded in DEC0007).
- The held-out test split has fake images only, so only recall is measured on it.
- The two models differ in training data (the held-out model has no images of that generator) and are single runs. No statistical test (Phase E11).
