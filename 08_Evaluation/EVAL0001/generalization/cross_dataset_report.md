# Cross-Dataset Evaluation: EVAL0001

**Model:** MODEL0001 (export SHA-256 `228495c1fe16…`), trained on DS0001 SPLIT0001  
**Phase:** E8  
**Date:** 2026-11-10

Threshold 0.3951 (chosen on DS0001 val) for every dataset. Nothing is re-tuned on target data. Config: `config.yaml` (SHA-256 `c5c05305f0e7…`). Per-image probabilities: `predictions/`.

Sanity check: 500 DS0001 test images re-predicted with max |diff| 1.33e-05 against `predictions.csv` (limit 0.001).

## Datasets

| Dataset | Content | n (fake / real) | Recall | FNR | Specificity | FPR | Balanced acc. | ROC-AUC | Mean P(fake) |
|---|---|---|---|---|---|---|---|---|---|
| DS0001 | in-distribution test (reference) | 7505 (3779 / 3726) | 0.8171 | 0.1829 | 0.8795 | 0.1205 | 0.8483 | 0.9261 | 0.4511 |
| DS0002 | DiFF official test, diffusion-generated faces (fake only) | 7364 (7364 / 0) | 0.4976 | 0.5024 | — | — | — | — | 0.4574 |
| DS0003 | 140k Real and Fake Faces, FFHQ real vs StyleGAN fake | 20000 (10000 / 10000) | 0.9083 | 0.0917 | 0.6963 | 0.3037 | 0.8023 | 0.9012 | 0.5370 |
| DS0004 | Synthbuster, general scenes (not faces), RAISE real vs 9 diffusion generators | 1500 (1350 / 150) | 0.7630 | 0.2370 | 0.2333 | 0.7667 | 0.4981 | 0.5172 | 0.6617 |
| DS0005 | FairFace, real faces only | 10000 (0 / 10000) | — | — | 0.1741 | 0.8259 | — | — | 0.7969 |

— = not defined because the dataset has one class. Fake-only datasets give recall; real-only give specificity.

Notes from the config:

- DS0003: Real images are FFHQ, a real source also present in DS0001.
- DS0004: Not faces; tests a different content distribution.

## Fake images by relation to the training generators

`seen`: same generator name as in DS0001 training. `related`: same family, version not confirmed (set in the config). `unseen`: neither.

| Relation | Datasets | Generators | n | FNR | 95% CI |
|---|---|---|---|---|---|
| related | DS0003, DS0004 | 5 | 10630 | 9.9% | 9.3%–10.5% |
| unseen | DS0002, DS0004 | 17 | 8084 | 48.1% | 47.0%–49.2% |

In-distribution FNR on DS0001 test is 18.3%.

## By generator (cross-dataset)

Error rate is FNR for fake generators and FPR for real sources. Wilson 95% intervals. Groups under 30 images are flagged in the CSV.

| Dataset | Class | Generator | Relation | n | Error rate | 95% CI | Mean P(fake) |
|---|---|---|---|---|---|---|---|
| DS0002 | fake | FreeDoM_I | unseen | 259 | 81.5% | 76.3%–85.7% | 0.208 |
| DS0002 | fake | FreeDoM_T | unseen | 368 | 72.8% | 68.1%–77.1% | 0.266 |
| DS0002 | fake | cycle_diff | unseen | 1238 | 64.5% | 61.8%–67.1% | 0.333 |
| DS0002 | fake | LoRA | unseen | 360 | 63.6% | 58.5%–68.4% | 0.340 |
| DS0002 | fake | Midjourney | unseen | 425 | 61.2% | 56.5%–65.7% | 0.355 |
| DS0002 | fake | DiffFace | unseen | 304 | 60.5% | 54.9%–65.9% | 0.386 |
| DS0002 | fake | Imagic | unseen | 819 | 58.7% | 55.3%–62.1% | 0.375 |
| DS0002 | fake | DreamBooth | unseen | 553 | 56.8% | 52.6%–60.8% | 0.395 |
| DS0002 | fake | SDXL | unseen | 1061 | 46.4% | 43.4%–49.4% | 0.466 |
| DS0002 | fake | HPS | unseen | 915 | 39.3% | 36.2%–42.5% | 0.538 |
| DS0002 | fake | CoDiff | unseen | 420 | 24.5% | 20.7%–28.9% | 0.629 |
| DS0002 | fake | DCFace | unseen | 642 | 0.0% | 0.0%–0.6% | 0.995 |
| DS0003 | fake | stylegan | related | 10000 | 9.2% | 8.6%–9.8% | 0.788 |
| DS0003 | real | none | real | 10000 | 30.4% | 29.5%–31.3% | 0.286 |
| DS0004 | fake | dalle3 | unseen | 143 | 46.9% | 38.9%–55.0% | 0.486 |
| DS0004 | fake | midjourney-v5 | unseen | 140 | 26.4% | 19.8%–34.3% | 0.621 |
| DS0004 | fake | stable-diffusion-1-4 | related | 164 | 25.0% | 19.0%–32.1% | 0.630 |
| DS0004 | fake | stable-diffusion-xl | related | 153 | 24.8% | 18.7%–32.2% | 0.657 |
| DS0004 | fake | dalle2 | unseen | 142 | 23.2% | 17.1%–30.8% | 0.632 |
| DS0004 | fake | stable-diffusion-1-3 | related | 154 | 21.4% | 15.7%–28.6% | 0.680 |
| DS0004 | fake | firefly | unseen | 146 | 17.1% | 11.9%–24.1% | 0.708 |
| DS0004 | fake | glide | unseen | 149 | 16.8% | 11.6%–23.6% | 0.774 |
| DS0004 | fake | stable-diffusion-2 | related | 159 | 13.2% | 8.8%–19.3% | 0.762 |
| DS0004 | real | raise_1k_jpeg | real | 150 | 76.7% | 69.3%–82.7% | 0.654 |
| DS0005 | real | none | real | 10000 | 82.6% | 81.8%–83.3% | 0.797 |

## Limits

- Fake-only and real-only datasets support one error type each; their numbers are not balanced accuracy.
- Each dataset was preprocessed with its own pipeline (PP0002–PP0006) to the same 224 px PNG format; source resolutions and formats differ.
- `related` labels are a judgement recorded in the config, not a verified identity of generator versions.
- One model, one seed. No statistical test (Phase E11). Differences describe where performance changes, not why.
