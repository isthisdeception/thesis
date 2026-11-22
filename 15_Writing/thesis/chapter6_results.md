# Chapter 6: Results

> **Version:** `0.2.0` | **Status:** Revised (W13 Reviewed; Pending Supervisor Sign-off) | **Last Updated:** 2026-11-22
> **Writing Units:** `WR0029`, `WR0030`, `WR0031`, `WR0032`, `WR0033`, `WR0034`
> **Traceability:** Every numerical value in this chapter is transcribed directly from verified outputs in `06_Experiments/EXP0001/metrics/run_summary.json`, `08_Evaluation/` (`EVAL0001`–`EVAL0007`, `ablations/`, `statistics/`, `comparison_report.md`, `forensic_analyst_eval/`), `16_Documentation/test_plan.md`, and `15_Writing/shared/knowledge_index.csv` (`KI0027`–`KI0037`).

---

## 6.1 In-Distribution Baseline Performance, Training Dynamics, Calibration, and Operating Points

The primary baseline experiment `EXP0001` (`MODEL0001`, ImageNet-1k pretrained ResNet-50 on `DS0001/v1.0/PP0001/SPLIT0001`) completed 11 scheduled epochs in 36.7 minutes (2,204.8 seconds) on a Kaggle Tesla T4 GPU (14,912 MB VRAM) with zero logged warnings or errors (`WR0029`; `KI0027`; `06_Experiments/EXP0001/metrics/run_summary.json`). Validation loss reached its minimum (`0.3424`) at epoch 7, triggering early stopping at the end of epoch 11; the full validation ROC-AUC and train/validation loss trajectories are specified in `FIG0024` and `FIG0025`. Prediction validation (`EVAL0001`, Phases E1–E2) passed across both validation (`n=7,502`) and test (`n=7,505`) partitions (`P0007`; `P0016`).

Applying the validation-chosen `frozen` threshold (`0.3951`, maximizing validation balanced accuracy) unchanged to `SPLIT0001` test yields the following canonical metrics (`WR0029`; `08_Evaluation/EVAL0001/classification_metrics.csv`; `FIG0021`; `FIG0022`; `TAB0002`):

| Split | n | ROC-AUC | PR-AUC | Balanced Acc. | MCC | F1 | Precision | Recall (1-FNR) | Specificity (1-FPR) | FNR | FPR | Accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Validation | 7,502 | 0.9341 | 0.9399 | 0.8565 | 0.7142 | 0.8516 | 0.8751 | 0.8293 | 0.8837 | 0.1707 | 0.1163 | 0.8567 |
| Test | 7,505 | 0.9261 | 0.9348 | 0.8483 | 0.6978 | 0.8442 | 0.8731 | 0.8171 | 0.8795 | 0.1829 | 0.1205 | 0.8481 |

Observed test performance (`ROC-AUC 0.9261`, balanced accuracy `0.8483`) falls below the `DEC0006` pre-training sanity expectation (`0.95` / `0.90`) while remaining well above the `0.90` ROC-AUC pipeline-failure trigger (`KI0027`; `EXP0001`). Consistent with `DEC0006`, these metrics are reported verbatim without post-hoc retuning, and validation-to-test generalization within `SPLIT0001` is tight (ROC-AUC gap `0.0080`).

Phase E4 calibration analysis on `SPLIT0001` test records Expected Calibration Error (`ECE`) of `0.0525` (validation `0.0510`), Maximum Calibration Error (`MCE`) of `0.1544` (validation `0.1535`), Brier score of `0.1128` (validation `0.1069`, against a `0.2500` constant-prevalence reference), and log loss of `0.3672` (validation `0.3427`) (`WR0029`; `KI0028`; `08_Evaluation/EVAL0001/calibration_threshold.md`; `FIG0011`; `FIG0012`). Mean predicted fake probability on test is `0.4511` compared to the actual fake share of `0.5035`, with the largest bin discrepancy (`+0.154`) occurring in `[0.200, 0.267]` (298 images, indicating more fake faces than implied by raw probability). Across confidence bins, predicted confidence exceeds empirical accuracy by more than `0.02` in six of ten bins (mean confidence `0.8785` versus accuracy `0.8481`), while 49.4% of test decisions carry confidence `>= 0.95` with empirical accuracy `0.962` (`EVAL0001`). These miscalibration patterns empirically justify replacing raw softmax probabilities with `MOD009` validation-calibrated accuracy lookups (`DEC0010`).

Phase E5 threshold analysis confirms clear operational trade-offs across the validation-chosen operating points when applied unchanged to `SPLIT0001` test (`WR0029`; `08_Evaluation/EVAL0001/calibration_threshold.md`; `FIG0013`):

| Operating Point | Validation Criterion | Threshold | Test Recall | Test Specificity | Test FPR | Test FNR | Test Balanced Acc. | Test F1 | Test MCC |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `frozen` (reporting) | Max balanced accuracy on val | 0.3951 | 0.8171 | 0.8795 | 0.1205 | 0.1829 | 0.8483 | 0.8442 | 0.6978 |
| `high_sensitivity` (screening) | Highest threshold with val FNR <= 0.05 | 0.0894 | 0.9447 | 0.6151 | 0.3849 | 0.0553 | 0.7799 | 0.8129 | 0.5938 |
| `high_specificity` (flag review) | Lowest threshold with val FPR <= 0.05 | 0.6288 | 0.7211 | 0.9444 | 0.0556 | 0.2789 | 0.8328 | 0.8121 | 0.6820 |
| `max_f1` (reference) | Max F1 on val | 0.3099 | 0.8513 | 0.8333 | 0.1667 | 0.1487 | 0.8423 | 0.8447 | 0.6848 |
| `fixed_0.5` (reference) | Default 0.50 cutoff | 0.5000 | 0.7788 | 0.9155 | 0.0845 | 0.2212 | 0.8471 | 0.8364 | 0.7003 |

## 6.2 Confusion Matrix, Per-Generator FNR, and Real-Source FPR Failure Analysis

On the 7,505 `SPLIT0001` test images at threshold `0.3951`, `MODEL0001` produces 3,088 true positives (81.7% of 3,779 fakes), 691 false negatives (18.3%), 3,277 true negatives (87.9% of 3,726 reals), and 449 false positives (12.1%) (`WR0030`; `KI0029`; `08_Evaluation/EVAL0001/failure_analysis.md`; `FIG0014`). Disaggregating errors by generator and real source reveals strong subgroup concentration despite balanced training representation (`FIG0015`):

| Class | Subgroup | n | Errors | Error Rate | Wilson 95% CI | Share of Class Errors | Mean P(fake) |
|---|---|---:|---:|---:|---|---:|---:|
| fake | `stylegan3` | 284 | 124 | 43.7% | 38.0%–49.5% | 17.9% | 0.479 |
| fake | `projected_gan` | 304 | 128 | 42.1% | 36.7%–47.7% | 18.5% | 0.517 |
| fake | `stylegan2` | 313 | 120 | 38.3% | 33.1%–43.8% | 17.4% | 0.569 |
| fake | `mat` | 272 | 104 | 38.2% | 32.7%–44.1% | 15.1% | 0.556 |
| fake | `lama` | 290 | 72 | 24.8% | 20.2%–30.1% | 10.4% | 0.670 |
| fake | `stylegan1` | 312 | 73 | 23.4% | 19.0%–28.4% | 10.6% | 0.659 |
| fake | `taming_transformer` | 281 | 29 | 10.3% | 7.3%–14.4% | 4.2% | 0.796 |
| fake | `gansformer` | 283 | 15 | 5.3% | 3.2%–8.6% | 2.2% | 0.839 |
| fake | `stable_diffusion` | 299 | 11 | 3.7% | 2.1%–6.5% | 1.6% | 0.915 |
| fake | `sfhq` | 302 | 9 | 3.0% | 1.6%–5.6% | 1.3% | 0.906 |
| fake | `face_synthetics` | 279 | 6 | 2.2% | 1.0%–4.6% | 0.9% | 0.947 |
| fake | `cips` | 265 | 0 | 0.0% | 0.0%–1.4% | 0.0% | 0.968 |
| fake | `stargan` | 295 | 0 | 0.0% | 0.0%–1.3% | 0.0% | 0.990 |
| real | `metfaces` | 150 | 55 | 36.7% | 29.4%–44.6% | 12.2% | 0.356 |
| real | `ffhq` | 1,882 | 275 | 14.6% | 13.1%–16.3% | 61.2% | 0.171 |
| real | `celebahq` | 1,694 | 119 | 7.0% | 5.9%–8.3% | 26.5% | 0.099 |

Four high-fidelity generators (`stylegan3` 43.7%, `projected_gan` 42.1%, `stylegan2` 38.3%, and `mat` 38.2%) account for 68.9% of all missed fakes, whereas `cips` and `stargan` exhibit 0.0% FNR (`WR0030`; `EVAL0001`; `P0023`; `P0025`; `CLAIM0005`). Among authentic images, artistic portrait faces from `metfaces` suffer a 36.7% FPR compared to 14.6% for `ffhq` and 7.0% for `celebahq`, indicating sensitivity to stylistic real-source distribution shifts (`P0016`; `CLAIM0003`). Error confidence profiles further diverge by direction: 33.7% (233/691) of false negatives occur at high confidence (`>= 0.9`, mean $P(\text{fake})=0.179$), demonstrating confident misses, whereas 29.6% (133/449) of false positives sit within `0.1` of the threshold (mean $P(\text{fake})=0.635$). Because `DS0001` metadata lacks person-identity, compression-variation, lighting, background, and occlusion tags, causal attributions for these subgroup patterns remain documented as untested hypotheses (`08_Evaluation/EVAL0001/failure_analysis.md`).

## 6.3 Robustness Under 53 Image Perturbations

Phase E7 executed all 54 conditions on the 7,505 `SPLIT0001` test images on a Kaggle Tesla T4 GPU; the clean baseline check reproduced `predictions.csv` with `max |diff| = 3.61e-5` (threshold `0.001`) and zero decision mismatches (`WR0031`; `KI0030`; `08_Evaluation/EVAL0001/robustness/robustness_report.md`; `FIG0016`; `FIG0017`). Across the 15 perturbation families, 12 exhibit `ranking_loss`, 3 exhibit `threshold_shift` (`brightness_down`, `oversaturate`, `upscaling`), and zero families remain `robust` through their strongest tested severity (`CLAIM0006`; `P0003`; `P0010`; `P0013`; `P0018`):

| Perturbation Family | Tolerance Level | Worst Level | Worst BA | ΔBA | ΔROC-AUC | ΔFNR | ΔFPR | Flip Rate | Direction | Pattern |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| `low_quality_upload` | none | `0.35_30` | 0.4999 | -0.3485 | -0.3947 | -0.1826 | +0.8795 | 0.529 | `to_fake` | `ranking_loss` |
| `resolution` | none | `0.35` | 0.5000 | -0.3483 | -0.2343 | -0.1829 | +0.8795 | 0.529 | `to_fake` | `ranking_loss` |
| `gaussian_blur` | none | `2` | 0.5039 | -0.3444 | -0.1930 | -0.1807 | +0.8696 | 0.523 | `to_fake` | `ranking_loss` |
| `gaussian_noise` | none | `0.1` | 0.5043 | -0.3440 | -0.3714 | -0.1815 | +0.8696 | 0.523 | `to_fake` | `ranking_loss` |
| `center_crop` | none | `0.7` | 0.5620 | -0.2863 | -0.0775 | -0.1762 | +0.7488 | 0.463 | `to_fake` | `ranking_loss` |
| `jpeg` | none | `10` | 0.6014 | -0.2469 | -0.2569 | +0.0783 | +0.4155 | 0.378 | `to_fake` | `ranking_loss` |
| `upscaling` | none | `2` | 0.6941 | -0.1543 | -0.0153 | -0.1614 | +0.4699 | 0.320 | `to_fake` | `threshold_shift` |
| `contrast_down` | `0.9` | `0.5` | 0.7516 | -0.0967 | -0.0230 | -0.1244 | +0.3178 | 0.237 | `to_fake` | `ranking_loss` |
| `occlusion` | `0.1` | `0.3` | 0.7590 | -0.0893 | -0.0451 | -0.0828 | +0.2614 | 0.206 | `to_fake` | `ranking_loss` |
| `rotation` | none | `30` | 0.7625 | -0.0858 | -0.0707 | +0.1831 | -0.0115 | 0.199 | `to_real` | `ranking_loss` |
| `desaturate` | `0.75` | `0` | 0.7641 | -0.0842 | -0.0533 | -0.0439 | +0.2123 | 0.214 | `to_fake` | `ranking_loss` |
| `brightness_down` | `0.75` | `0.5` | 0.7829 | -0.0654 | -0.0172 | -0.1045 | +0.2354 | 0.190 | `to_fake` | `threshold_shift` |
| `contrast_up` | `1.25` | `1.5` | 0.7934 | -0.0550 | -0.0329 | +0.1585 | -0.0486 | 0.136 | `to_real` | `ranking_loss` |
| `brightness_up` | `1.25` | `1.5` | 0.8040 | -0.0443 | -0.0359 | +0.0953 | -0.0067 | 0.127 | `to_real` | `ranking_loss` |
| `oversaturate` | `1.5` | `2` | 0.8242 | -0.0241 | -0.0145 | +0.0770 | -0.0287 | 0.109 | `to_real` | `threshold_shift` |

Perturbations that destroy high-frequency spatial detail (`low_quality_upload`, `resolution`, `gaussian_blur`, `gaussian_noise`, and `jpeg@10`) drive balanced accuracy to chance (`~0.50`) by pushing `FPR` toward `1.0000` (classifying virtually every degraded real image as fake; e.g., `real:celebahq` error jumps by `+0.9298` under `low_quality_upload@0.35_30` and `resolution@0.35`) (`WR0031`; `EVAL0001`). At mild distortion levels such as `gaussian_blur@0.5` (ROC-AUC `0.9271`, BA `0.8189`), `resolution@0.75` (ROC-AUC `0.8888`, BA `0.6058`), and `upscaling@2` (ROC-AUC `0.9108`, BA `0.6941`), ROC-AUC stays comparatively intact while balanced accuracy plunges, revealing an initial score shift toward fake before ranking collapses. By contrast, photometric adjustments (`brightness`, `contrast`, `saturation`), small rotations (5–15 degrees), and mild occlusions (`<= 0.1`) degrade balanced accuracy by less than `0.10`, with brightening, contrast increases, oversaturation, and rotation shifting flipped decisions `to_real` (`EXP0001`; `CLAIM0006`).

## 6.4 Cross-Dataset Generalization and Controlled Unseen-Generator LOGO Results

Phase E8 cross-dataset inference passed its 500-image `DS0001` sanity check (`max |diff| = 1.33e-5`) and exposed severe domain and generator generalization gaps at the frozen `0.3951` threshold (`WR0032`; `KI0031`; `08_Evaluation/EVAL0001/generalization/cross_dataset_report.md`; `FIG0018`; `CLAIM0001`; `CLAIM0003`):

| Dataset | Content & Class Structure | n (fake / real) | Recall | FNR | Specificity | FPR | Balanced Acc. | ROC-AUC | Mean P(fake) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| `DS0001` | In-distribution reference (`SPLIT0001` test) | 7,505 (3,779 / 3,726) | 0.8171 | 0.1829 | 0.8795 | 0.1205 | 0.8483 | 0.9261 | 0.4511 |
| `DS0002` | DiFF diffusion faces (fake only) | 7,364 (7,364 / 0) | 0.4976 | 0.5024 | N/A | N/A | N/A | N/A | 0.4574 |
| `DS0003` | 140k FFHQ real vs StyleGAN fake | 20,000 (10,000 / 10,000) | 0.9083 | 0.0917 | 0.6963 | 0.3037 | 0.8023 | 0.9012 | 0.5370 |
| `DS0004` | Synthbuster general scenes (RAISE vs 9 DMs) | 1,500 (1,350 / 150) | 0.7630 | 0.2370 | 0.2333 | 0.7667 | 0.4981 | 0.5172 | 0.6617 |
| `DS0005` | FairFace real faces (real only, `DEC0007`) | 10,000 (0 / 10,000) | N/A | N/A | 0.1741 | 0.8259 | N/A | N/A | 0.7969 |

Grouping external synthetic images by training relation confirms sharp cross-generator degradation (`WR0032`; `P0003`; `P0007`; `P0016`; `P0018`; `P0023`): across five `related` generators (`n=10,630`, `DS0003` StyleGAN and `DS0004` Stable Diffusion variants), FNR is `9.9%` (95% CI `9.3%`–`10.5%`), whereas across 17 `unseen` generators (`n=8,084`, `DS0002` and `DS0004`), FNR surges to `48.1%` (95% CI `47.0%`–`49.2%`), reaching `81.5%` on `FreeDoM_I`, `72.8%` on `FreeDoM_T`, `64.5%` on `cycle_diff`, `63.6%` on `LoRA`, `61.2%` on `Midjourney`, `60.5%` on `DiffFace`, and `46.4%` on `SDXL` (with `DCFace` at `0.0%` FNR). Simultaneously, authentic images from external corpora trigger extreme false positives: `30.4%` FPR on `DS0003` (FFHQ), `76.7%` on `DS0004` (RAISE scenes, collapsing ROC-AUC to `0.5172`), and `82.6%` on `DS0005` (FairFace real faces, mean $P(\text{fake})=0.7969$), confirming that `MODEL0001` heavily relies on `DS0001`-specific real-image statistics (`CLAIM0003`; `EXP0001`).

Phase E9 (`EXP0002` / `MODEL0008` on `DS0001_PP0001_SPLIT0002`, `stable_diffusion` held out) eliminates cross-dataset format confounds and isolates pure unseen-generator behavior (`WR0032`; `KI0032`; `08_Evaluation/EVAL0002/unseen_generator/unseen_report.md`; `FIG0019`). Trained in 66.0 minutes (best epoch 9) with verified zero leakage, `MODEL0008` attains validation ROC-AUC `0.937`, balanced accuracy `0.859`, seen-generator recall `83.3%` (`n=3,448`, 95% CI `82.0%`–`84.5%`), and real specificity `88.6%` (`n=3,756`) at its validation threshold (`0.4420`). On the 1,923 held-out unseen `stable_diffusion` faces, however, recall drops to `15.2%` (293/1,923, 95% CI `13.7%`–`16.9%`, mean $P(\text{fake})=0.182$; indicative ROC-AUC against validation real images `0.5542`). On the exact same 299 `stable_diffusion` images evaluated by both models, `MODEL0001` (which saw `stable_diffusion` in training) detects `96.3%` while `MODEL0008` (unseen) detects `13.7%`: 247 images are detected exclusively by `MODEL0001`, 41 by both, 11 by neither, and 0 exclusively by `MODEL0008` (`EXP0002`; `EVAL0002`; `CLAIM0001`).

## 6.5 Controlled One-Factor Ablations, Ranked Comparison, and Paired Statistical Testing

All four one-factor ablations (`EXP0003`–`EXP0006`, `MODEL0009`–`MODEL0012`) satisfied `E1–E2` prediction validation and `SPLIT0001` fairness invariants, yielding the canonical ranked comparison table (`EXP0002` excluded due to `SPLIT0002`) (`WR0033`; `KI0033`; `KI0034`; `08_Evaluation/comparison_report.md`; `08_Evaluation/ablations/ablation_report.md`; `08_Evaluation/statistics/statistics_report.md`; `FIG0020`–`FIG0023`; `TAB0002`; `TAB0003`):

| Experiment | Factor | ROC-AUC | PR-AUC | Balanced Acc. | MCC | FNR | FPR | ECE | ΔROC-AUC (Adjusted CI) | Exact McNemar Adj. p | Run Difference |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| `EXP0001` | baseline | 0.9261 | 0.9348 | 0.8483 | 0.6978 | 0.1829 | 0.1205 | 0.0525 | +0.0000 | N/A | baseline |
| `EXP0003` | `random_seed` (43) | 0.9272 | 0.9363 | 0.8481 | 0.6978 | 0.1881 | 0.1157 | 0.0545 | +0.0011 `[-0.0012, +0.0035]` | `0.964` | `not_supported` |
| `EXP0004` | no augmentation | 0.8925 | 0.9042 | 0.8059 | 0.6120 | 0.2056 | 0.1825 | 0.0378 | -0.0336 `[-0.0396, -0.0279]` | `8.34e-23` | `challenger_lower` |
| `EXP0005` | no pretraining | 0.7017 | 0.7092 | 0.6452 | 0.2912 | 0.3162 | 0.3935 | 0.0230 | -0.2243 `[-0.2383, -0.2101]` | `7.1e-217` | `challenger_lower` |
| `EXP0006` | `image_size` 160 | 0.8885 | 0.9053 | 0.8039 | 0.6082 | 0.2170 | 0.1753 | 0.0944 | -0.0376 `[-0.0447, -0.0307]` | `1.36e-21` | `challenger_lower` |

Seed repeatability between `EXP0001` and `EXP0003` establishes a narrow run-to-run noise floor (`ΔROC-AUC +0.0011`, `ΔBA -0.0002`, `ΔMCC 0.0000`, two-seed SD `0.0008` on ROC-AUC; decision agreement `0.9334`, Cohen's kappa `0.8662`, probability Pearson `r = 0.9662`, mean absolute probability difference `0.0601`; McNemar `b=251` vs `c=249`, `p = 0.964`) (`WR0033`; `EVAL0003`). Every one of the three factor ablations degrades discrimination far beyond this seed noise floor with Bonferroni-adjusted 98.3% bootstrap intervals strictly excluding zero and highly significant McNemar decision disagreement (`EVAL0004`; `EVAL0005`; `EVAL0006`): removing ImageNet pretraining (`EXP0005`; `EVAL0005`) produces the largest collapse (`-0.2243` ROC-AUC, `-0.2032` BA, `-0.4065` MCC, `b=2,012` vs `c=491`), reducing spatial resolution to 160 pixels (`EXP0006`) loses `-0.0376` ROC-AUC while worsening ECE by `+0.0420` (`0.0944`), and disabling train-only augmentation (`EXP0004`) loses `-0.0336` ROC-AUC and triggers early stopping at epoch 3 (20.1 minutes) due to faster overfitting (`P0007`; `P0016`). Because each factor has one seed and Wilcoxon signed-rank across seeds was not run (`n=2 < 6` pairs), `superiority_claim` remains `none` across all rows of `TAB0003`.

## 6.6 AI Forensic Analyst Whole-Platform Phase E14 Evaluation and Full-Stack UAT Results

Whole-platform evaluation (`EVAL0007`, Phase E14) verified all 16 end-to-end scenarios across all nine quality dimensions (`WR0034`; `KI0035`; `08_Evaluation/forensic_analyst_eval/e14_report.md`; `08_Evaluation/forensic_analyst_eval/e14_case_results.csv`; `MOD001`–`MOD018`):

| E14 Dimension | Observed Performance (`EVAL0007`) | Status |
|---|---|---|
| Evidence completeness | `10/10` collectors registered (`MOD005`) and validated (`MOD006`); `24` `EV` rows per canonical case | PASS |
| Fusion quality | `rule_based` (`DEC0009`) leans match approved rules across `12/12` completed cases | PASS |
| Decision consistency | Image-blind `MOD008` 4-way verdicts match rules across `16/16` scenarios | PASS |
| Confidence consistency | `MOD009` E4 val-calibrated (`DEC0010`), distinct from raw softmax, `null` when absent (`12/12`) | PASS |
| Report quality | `MOD012` Template 24 JSON/MD/HTML with byte-identical version/Git stamps (`12/12`; `4/4` stops omit reports) | PASS |
| Reasoning quality | `135` `MOD011` `EV`-grounded sentences verified by `verify_sentence`, `0` ungrounded leaks | PASS |
| Execution time | Mean `60.02 ms`, max `149.08 ms` per case (excluding external GPU model load) | PASS |
| Module failures | `8/8` canonical `MOD016` failure modes verified; `0` silent failures | PASS |
| Recovery behavior | `7/7` fault scenarios degrade gracefully (`Inconclusive`/`Unknown`) or stop cleanly with `MOD015` audit row | PASS |

The E14 case results empirically demonstrate how the AI Forensic Analyst prevents unsafe binary verdicts (`WR0034`; `KI0036`; `P0016`; `P0018`; `EXP0001`; `EXP0002`): on clean `EXP0001` cases (`E14-01`–`E14-08`), high detector probabilities map to calibrated `prediction_confidence = 0.971745` (never raw `0.99`), `evidence_confidence = 0.900000`, `system_confidence = 0.900000`, and single-source-discounted `decision_confidence = 0.795492` with 12 verified reasoning sentences per case. Under multi-specialist conflict (`E14-09`, `MODEL0001` vs `MODEL0008`), `MOD007` marks the lean `contested` (`26` `EV` rows), dropping `decision_confidence` to `0.256239` and producing `Inconclusive`. Under `E14-10`, even though `MOD004` outputs $P(\text{fake})=0.99$ (`prediction_confidence = 0.971745`), unusable supporting evidence drops `evidence_confidence` and `system_confidence` to `0.333333`, capping `decision_confidence` at `0.333333` (`< 0.50`) so `MOD008` issues `Inconclusive` with a `low_confidence` warning rather than repeating `0.99` as `Fake`. Under `E14-11` (`model_unavailable`) and `E14-12` (`timeout`), all nine non-detector collectors still register (`22` `EV` rows, `evidence_confidence = 0.888889`, `system_confidence = 0.800000`), `prediction_confidence` and `decision_confidence` stay `null`, and `MOD008` emits `Unknown`. Finally, `E14-13`–`E14-16` (`unsupported_format`, `corrupted_image`, `no_face`, `multiple_faces`) halt cleanly with `0` `EV` rows, no `decision.json` or report, and a `failed` audit record in `case_registry.csv` (`08_Evaluation/forensic_audit.md`).

Across the complete web platform (`17_Automation/run_all_tests.py`; `16_Documentation/test_plan.md`), all automated verification suites pass: `55` forensic unit/integration tests, `18` backend API/smoke/regression/CORS tests, `12` frontend Vitest suites plus production `vite build`, `1` live cross-tier React-to-Django integration test (`17_Automation/verify_integration.py`), and all `6/6` live HTTP UAT scenarios (`UAT-01` through `UAT-06`), confirming end-to-end operational readiness across Checklists 9, 10, 11, and 12 (`WR0034`; `KI0037`).
