# Failure Analysis: EVAL0001

**Experiment:** EXP0001
**Phases:** E6, E12
**Date:** 2026-11-10

Source: `08_Evaluation/EXP0001/predictions.csv` (SHA-256 `4553498081ef7da8574c6742f0f5fbec08993556b6ef0b25abcd76c313c1cc90`), joined to the preprocessing index by content hash. Decisions are the saved ones at the frozen threshold, as in `classification_metrics.csv`. This report describes `test`; `val` rows are in the CSVs.

Causes below are **hypotheses**. None has been tested. Each lists how it could be checked.

## Confusion matrix (E6)

| True \ Predicted | fake | real |
|------------------|------|------|
| fake | 3088 (81.7%) | 691 (18.3%) |
| real | 449 (12.1%) | 3277 (87.9%) |

Percentages are shares of the true class. Figure spec: FIG0014.

| Class | Support | Predicted | Correct | Precision | Recall | F1 | Error rate |
|-------|---------|-----------|---------|-----------|--------|----|------------|
| fake | 3779 | 3537 | 3088 | 0.8731 | 0.8171 | 0.8442 | 0.1829 |
| real | 3726 | 3968 | 3277 | 0.8259 | 0.8795 | 0.8518 | 0.1205 |

## Errors by generator and real source (E6)

Error rate is FNR for fake generators and FPR for real sources. Interval: Wilson 95%. Groups under 30 images are flagged `small_group` in the CSV and left out here.

| Class | Group | n | Errors | Error rate | 95% CI | Share of class errors | Mean P(fake) |
|-------|-------|---|--------|------------|--------|-----------------------|--------------|
| fake | stylegan3 | 284 | 124 | 43.7% | 38.0%–49.5% | 17.9% | 0.479 |
| fake | projected_gan | 304 | 128 | 42.1% | 36.7%–47.7% | 18.5% | 0.517 |
| fake | stylegan2 | 313 | 120 | 38.3% | 33.1%–43.8% | 17.4% | 0.569 |
| fake | mat | 272 | 104 | 38.2% | 32.7%–44.1% | 15.1% | 0.556 |
| fake | lama | 290 | 72 | 24.8% | 20.2%–30.1% | 10.4% | 0.670 |
| fake | stylegan1 | 312 | 73 | 23.4% | 19.0%–28.4% | 10.6% | 0.659 |
| fake | taming_transformer | 281 | 29 | 10.3% | 7.3%–14.4% | 4.2% | 0.796 |
| fake | gansformer | 283 | 15 | 5.3% | 3.2%–8.6% | 2.2% | 0.839 |
| fake | stable_diffusion | 299 | 11 | 3.7% | 2.1%–6.5% | 1.6% | 0.915 |
| fake | sfhq | 302 | 9 | 3.0% | 1.6%–5.6% | 1.3% | 0.906 |
| fake | face_synthetics | 279 | 6 | 2.2% | 1.0%–4.6% | 0.9% | 0.947 |
| fake | cips | 265 | 0 | 0.0% | 0.0%–1.4% | 0.0% | 0.968 |
| fake | stargan | 295 | 0 | 0.0% | 0.0%–1.3% | 0.0% | 0.990 |
| real | metfaces | 150 | 55 | 36.7% | 29.4%–44.6% | 12.2% | 0.356 |
| real | ffhq | 1882 | 275 | 14.6% | 13.1%–16.3% | 61.2% | 0.171 |
| real | celebahq | 1694 | 119 | 7.0% | 5.9%–8.3% | 26.5% | 0.099 |

## FP and FN summary (E6)

| Error | Count | Within 0.1 of threshold | Confidence ≥ 0.9 | Mean P(fake) |
|-------|-------|-------------------------|------------------|--------------|
| false positive (real → fake) | 449 | 133 (29.6%) | 51 (11.4%) | 0.635 |
| false negative (fake → real) | 691 | 143 (20.7%) | 233 (33.7%) | 0.179 |

`error_cases.csv` lists the 20 most confident false positives and 20 most confident false negatives per split for manual review. On `test` the false positives come from `ffhq` (14), `celebahq` (5), `metfaces` (1); the false negatives from `stylegan2` (6), `stylegan3` (4), `mat` (3), `projected_gan` (3), `lama` (2), `stable_diffusion` (1), `taming_transformer` (1).

## Failure categories (E12)

| Category | Evidence available | Observation | Possible causes (hypotheses) | How to check |
|----------|--------------------|-------------|------------------------------|--------------|
| Generator confusion | yes (`generator`) | FNR ranges from 0.0% to 43.7%. Above the overall FNR (18.3%) with the whole interval: `stylegan3`, `projected_gan`, `stylegan2`, `mat`, `lama`, `stylegan1`. Below it: `taming_transformer`, `gansformer`, `stable_diffusion`, `sfhq`, `face_synthetics`, `cips`, `stargan`. Highest: `stylegan3`, `projected_gan`, `stylegan2`. | These generators may leave fewer of the traces the model relies on for the others; the 224-px PNG preprocessing may also remove some of their traces. | Leave-one-generator-out (STEP-047, E9); per-generator Grad-CAM on `error_cases.csv`. |
| Real-source shift | yes (identity prefix) | FPR by real source: `metfaces` 36.7%, `ffhq` 14.6%, `celebahq` 7.0%. Above the overall FPR (12.1%) with the whole interval: `metfaces`, `ffhq`. | A source that is rare in training or differs in style (for example artwork portraits) may look unlike the real images the model learned. | Count each source in train; compare FPR after re-weighting; cross-dataset tests (STEP-047, E8). |
| Identity confusion | no | `identity` is a file-derived id. 69 `test` images share one, all from `stylegan2`, `stylegan3`: filename indices, not people. | Not assessable. | A dataset with person identity labels, or face-recognition clustering. |
| Compression | no | Every `test` image has source format jpg. | Not assessable: no variation to compare. | JPEG-quality perturbations (STEP-046, E7). |
| Poor quality / resolution | no | Every `test` image has original size 200x200; no quality score is stored. | Not assessable. | Blur, noise, and resolution perturbations (STEP-046, E7). |
| Background, lighting, occlusion | no | No annotations for these. | Not assessable. | Manual tagging of `error_cases.csv`; Grad-CAM. |
| Artifacts | partial | 33.7% of false negatives have confidence ≥ 0.9 (the model is confidently wrong). | Some fakes may lack visible artifacts at 224 px, or contain features the model links to real images. | Grad-CAM on the most confident false negatives (`error_cases.csv`). |
| Unexpected behaviour | yes | 29.6% of false positives lie within 0.1 of the threshold, against 20.7% of false negatives. | Many false positives may be borderline rather than confident. | Threshold trade-offs in `calibration_threshold.md`. |

## Limits

- One model, one seed, one split. No statistical test (Phase E11).
- Metadata has no quality, lighting, background, or occlusion fields. Those categories need manual or perturbation-based checks.
- Subgroup intervals are per group and not corrected for multiple comparisons.
