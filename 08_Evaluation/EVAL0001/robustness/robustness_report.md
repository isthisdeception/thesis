# Robustness Evaluation: EVAL0001

**Experiment:** EXP0001  
**Model:** MODEL0001 (export SHA-256 `228495c1fe16…`)  
**Phase:** E7  
**Date:** 2026-11-10

7505 `test` images, 53 perturbed conditions plus clean. Config: `config.yaml` (SHA-256 `a619c9a0e21c…`). Probabilities: `robustness_probs.csv`. Device: cuda.

Clean check: the clean run reproduces `predictions.csv` with max |diff| 3.61e-05 (limit 0.001) and 0 decision mismatch(es).

Decisions use the frozen threshold 0.3951. No threshold is chosen on perturbed data.

## Terms

- **Degradation:** change against clean (`delta_*`). Clean balanced accuracy is 0.8483, ROC-AUC 0.9261.
- **Tolerance level:** the strongest level up to which balanced accuracy stays within 0.02 of clean at every milder level. Blank means even the mildest level falls outside.
- **Pattern:** `robust` (worst drop within 0.02); `threshold_shift` (balanced accuracy drops but ROC-AUC drops less than 0.02: ranking kept, probabilities moved, so recalibration might recover it without retraining); `ranking_loss` (ROC-AUC drops too).
- **Flip direction:** whether changed decisions at the worst level mostly move to fake or to real.

## Summary by perturbation

| Perturbation | Levels (mild → strong) | Tolerance level | Worst level | Worst BA | ΔBA | ΔROC-AUC | ΔFNR | ΔFPR | Flip rate | Direction | Pattern | Most affected group (Δ error) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| jpeg | 90, 70, 50, 30, 10 | — | 10 | 0.6014 | -0.2469 | -0.2569 | +0.0783 | +0.4155 | 0.378 | to_fake | ranking_loss | real:metfaces (+0.4667) |
| gaussian_noise | 0.01, 0.02, 0.05, 0.1 | — | 0.1 | 0.5043 | -0.3440 | -0.3714 | -0.1815 | +0.8696 | 0.523 | to_fake | ranking_loss | real:celebahq (+0.9179) |
| gaussian_blur | 0.5, 1, 2, 3 | — | 2 | 0.5039 | -0.3444 | -0.1930 | -0.1807 | +0.8696 | 0.523 | to_fake | ranking_loss | real:celebahq (+0.9238) |
| brightness_down | 0.9, 0.75, 0.5 | 0.75 | 0.5 | 0.7829 | -0.0654 | -0.0172 | -0.1045 | +0.2354 | 0.190 | to_fake | threshold_shift | real:ffhq (+0.2614) |
| brightness_up | 1.1, 1.25, 1.5 | 1.25 | 1.5 | 0.8040 | -0.0443 | -0.0359 | +0.0953 | -0.0067 | 0.127 | to_real | ranking_loss | fake:stylegan1 (+0.1987) |
| contrast_down | 0.9, 0.75, 0.5 | 0.9 | 0.5 | 0.7516 | -0.0967 | -0.0230 | -0.1244 | +0.3178 | 0.237 | to_fake | ranking_loss | real:ffhq (+0.3661) |
| contrast_up | 1.1, 1.25, 1.5 | 1.25 | 1.5 | 0.7934 | -0.0550 | -0.0329 | +0.1585 | -0.0486 | 0.136 | to_real | ranking_loss | fake:lama (+0.2897) |
| desaturate | 0.75, 0.5, 0 | 0.75 | 0 | 0.7641 | -0.0842 | -0.0533 | -0.0439 | +0.2123 | 0.214 | to_fake | ranking_loss | real:ffhq (+0.2210) |
| oversaturate | 1.25, 1.5, 2 | 1.5 | 2 | 0.8242 | -0.0241 | -0.0145 | +0.0770 | -0.0287 | 0.109 | to_real | threshold_shift | fake:stylegan1 (+0.1859) |
| resolution | 0.75, 0.5, 0.35, 0.25 | — | 0.35 | 0.5000 | -0.3483 | -0.2343 | -0.1829 | +0.8795 | 0.529 | to_fake | ranking_loss | real:celebahq (+0.9298) |
| upscaling | 1.25, 1.5, 2 | — | 2 | 0.6941 | -0.1543 | -0.0153 | -0.1614 | +0.4699 | 0.320 | to_fake | threshold_shift | real:celebahq (+0.4864) |
| center_crop | 0.95, 0.9, 0.8, 0.7 | — | 0.7 | 0.5620 | -0.2863 | -0.0775 | -0.1762 | +0.7488 | 0.463 | to_fake | ranking_loss | real:celebahq (+0.7798) |
| rotation | 5, 10, 15, 30 | — | 30 | 0.7625 | -0.0858 | -0.0707 | +0.1831 | -0.0115 | 0.199 | to_real | ranking_loss | fake:stylegan1 (+0.4006) |
| occlusion | 0.05, 0.1, 0.2, 0.3 | 0.1 | 0.3 | 0.7590 | -0.0893 | -0.0451 | -0.0828 | +0.2614 | 0.206 | to_fake | ranking_loss | real:metfaces (+0.3733) |
| low_quality_upload | 0.75_75, 0.5_50, 0.35_30 | — | 0.35_30 | 0.4999 | -0.3485 | -0.3947 | -0.1826 | +0.8795 | 0.529 | to_fake | ranking_loss | real:celebahq (+0.9298) |

- Patterns: `ranking_loss` 12, `threshold_shift` 3.
- Largest balanced-accuracy drop: `low_quality_upload` at 0.35_30 (-0.3485).
- At the worst level, changed decisions mostly move to fake for 11 perturbation(s) and to real for 4.

## All conditions

| Condition | BA | ΔBA | ROC-AUC | ΔROC-AUC | FNR | FPR | ECE | Mean P(fake) | Flip rate |
|---|---|---|---|---|---|---|---|---|---|
| clean | 0.8483 | +0.0000 | 0.9261 | +0.0000 | 0.1829 | 0.1205 | 0.0525 | 0.4511 | 0.000 |
| jpeg@90 | 0.8237 | -0.0247 | 0.9170 | -0.0090 | 0.1299 | 0.2228 | 0.0433 | 0.5171 | 0.112 |
| jpeg@70 | 0.8174 | -0.0309 | 0.9051 | -0.0209 | 0.1530 | 0.2123 | 0.0375 | 0.5008 | 0.132 |
| jpeg@50 | 0.7941 | -0.0543 | 0.8835 | -0.0426 | 0.1564 | 0.2555 | 0.0482 | 0.5096 | 0.169 |
| jpeg@30 | 0.7347 | -0.1136 | 0.8293 | -0.0967 | 0.1863 | 0.3443 | 0.0729 | 0.5201 | 0.235 |
| jpeg@10 | 0.6014 | -0.2469 | 0.6691 | -0.2569 | 0.2612 | 0.5360 | 0.1510 | 0.5357 | 0.378 |
| gaussian_noise@0.01 | 0.6942 | -0.1541 | 0.8604 | -0.0656 | 0.0572 | 0.5545 | 0.1676 | 0.6710 | 0.301 |
| gaussian_noise@0.02 | 0.6682 | -0.1801 | 0.7776 | -0.1484 | 0.1387 | 0.5250 | 0.1091 | 0.5921 | 0.316 |
| gaussian_noise@0.05 | 0.5795 | -0.2688 | 0.6840 | -0.2420 | 0.0646 | 0.7764 | 0.1717 | 0.6701 | 0.431 |
| gaussian_noise@0.1 | 0.5043 | -0.3440 | 0.5546 | -0.3714 | 0.0013 | 0.9901 | 0.3352 | 0.8388 | 0.523 |
| gaussian_blur@0.5 | 0.8189 | -0.0294 | 0.9271 | +0.0011 | 0.0841 | 0.2780 | 0.0608 | 0.5598 | 0.135 |
| gaussian_blur@1 | 0.5208 | -0.3275 | 0.8367 | -0.0893 | 0.0026 | 0.9557 | 0.4215 | 0.9250 | 0.506 |
| gaussian_blur@2 | 0.5039 | -0.3444 | 0.7331 | -0.1930 | 0.0021 | 0.9901 | 0.4495 | 0.9529 | 0.523 |
| gaussian_blur@3 | 0.5092 | -0.3391 | 0.6699 | -0.2562 | 0.0087 | 0.9729 | 0.4026 | 0.9051 | 0.516 |
| brightness_down@0.9 | 0.8487 | +0.0004 | 0.9256 | -0.0004 | 0.1572 | 0.1455 | 0.0384 | 0.4745 | 0.041 |
| brightness_down@0.75 | 0.8332 | -0.0151 | 0.9228 | -0.0033 | 0.1326 | 0.2010 | 0.0428 | 0.5079 | 0.091 |
| brightness_down@0.5 | 0.7829 | -0.0654 | 0.9089 | -0.0172 | 0.0783 | 0.3559 | 0.0989 | 0.5967 | 0.190 |
| brightness_up@1.1 | 0.8439 | -0.0045 | 0.9230 | -0.0031 | 0.1778 | 0.1345 | 0.0467 | 0.4572 | 0.043 |
| brightness_up@1.25 | 0.8360 | -0.0124 | 0.9158 | -0.0103 | 0.1987 | 0.1294 | 0.0603 | 0.4441 | 0.074 |
| brightness_up@1.5 | 0.8040 | -0.0443 | 0.8901 | -0.0359 | 0.2781 | 0.1138 | 0.1088 | 0.3947 | 0.127 |
| contrast_down@0.9 | 0.8459 | -0.0024 | 0.9256 | -0.0005 | 0.1458 | 0.1624 | 0.0358 | 0.4861 | 0.050 |
| contrast_down@0.75 | 0.8240 | -0.0243 | 0.9217 | -0.0044 | 0.1098 | 0.2421 | 0.0467 | 0.5356 | 0.109 |
| contrast_down@0.5 | 0.7516 | -0.0967 | 0.9031 | -0.0230 | 0.0585 | 0.4383 | 0.1360 | 0.6380 | 0.237 |
| contrast_up@1.1 | 0.8440 | -0.0043 | 0.9233 | -0.0027 | 0.1945 | 0.1176 | 0.0610 | 0.4434 | 0.041 |
| contrast_up@1.25 | 0.8318 | -0.0165 | 0.9140 | -0.0121 | 0.2387 | 0.0977 | 0.0937 | 0.4098 | 0.074 |
| contrast_up@1.5 | 0.7934 | -0.0550 | 0.8932 | -0.0329 | 0.3414 | 0.0719 | 0.1561 | 0.3474 | 0.136 |
| desaturate@0.75 | 0.8395 | -0.0088 | 0.9229 | -0.0032 | 0.1490 | 0.1720 | 0.0361 | 0.4889 | 0.057 |
| desaturate@0.5 | 0.8163 | -0.0320 | 0.9158 | -0.0102 | 0.1185 | 0.2488 | 0.0458 | 0.5295 | 0.116 |
| desaturate@0 | 0.7641 | -0.0842 | 0.8728 | -0.0533 | 0.1389 | 0.3328 | 0.0532 | 0.5388 | 0.214 |
| oversaturate@1.25 | 0.8494 | +0.0011 | 0.9249 | -0.0011 | 0.2032 | 0.0980 | 0.0739 | 0.4297 | 0.043 |
| oversaturate@1.5 | 0.8420 | -0.0063 | 0.9220 | -0.0040 | 0.2247 | 0.0913 | 0.0892 | 0.4144 | 0.070 |
| oversaturate@2 | 0.8242 | -0.0241 | 0.9115 | -0.0145 | 0.2599 | 0.0918 | 0.1078 | 0.3957 | 0.109 |
| resolution@0.75 | 0.6058 | -0.2425 | 0.8888 | -0.0372 | 0.0095 | 0.7789 | 0.3117 | 0.8152 | 0.417 |
| resolution@0.5 | 0.5125 | -0.3358 | 0.8029 | -0.1231 | 0.0011 | 0.9740 | 0.4463 | 0.9498 | 0.516 |
| resolution@0.35 | 0.5000 | -0.3483 | 0.6918 | -0.2343 | 0.0000 | 1.0000 | 0.4928 | 0.9963 | 0.529 |
| resolution@0.25 | 0.5000 | -0.3483 | 0.6315 | -0.2946 | 0.0000 | 1.0000 | 0.4950 | 0.9985 | 0.529 |
| upscaling@1.25 | 0.7133 | -0.1350 | 0.9163 | -0.0098 | 0.0280 | 0.5454 | 0.1967 | 0.7002 | 0.295 |
| upscaling@1.5 | 0.6945 | -0.1538 | 0.9119 | -0.0142 | 0.0236 | 0.5875 | 0.2184 | 0.7219 | 0.317 |
| upscaling@2 | 0.6941 | -0.1543 | 0.9108 | -0.0153 | 0.0214 | 0.5904 | 0.2181 | 0.7216 | 0.320 |
| center_crop@0.95 | 0.7989 | -0.0494 | 0.9262 | +0.0001 | 0.0659 | 0.3363 | 0.0919 | 0.5952 | 0.187 |
| center_crop@0.9 | 0.7556 | -0.0928 | 0.9187 | -0.0073 | 0.0474 | 0.4415 | 0.1391 | 0.6423 | 0.242 |
| center_crop@0.8 | 0.6536 | -0.1947 | 0.8996 | -0.0264 | 0.0164 | 0.6763 | 0.2648 | 0.7683 | 0.368 |
| center_crop@0.7 | 0.5620 | -0.2863 | 0.8486 | -0.0775 | 0.0066 | 0.8693 | 0.3762 | 0.8797 | 0.463 |
| rotation@5 | 0.8279 | -0.0204 | 0.9285 | +0.0025 | 0.0886 | 0.2555 | 0.0536 | 0.5500 | 0.149 |
| rotation@10 | 0.8312 | -0.0171 | 0.9284 | +0.0023 | 0.0950 | 0.2426 | 0.0463 | 0.5411 | 0.148 |
| rotation@15 | 0.8298 | -0.0185 | 0.9152 | -0.0109 | 0.1429 | 0.1975 | 0.0328 | 0.4990 | 0.137 |
| rotation@30 | 0.7625 | -0.0858 | 0.8554 | -0.0707 | 0.3660 | 0.1090 | 0.1484 | 0.3551 | 0.199 |
| occlusion@0.05 | 0.8359 | -0.0124 | 0.9186 | -0.0075 | 0.2096 | 0.1186 | 0.0699 | 0.4336 | 0.065 |
| occlusion@0.1 | 0.8328 | -0.0155 | 0.9137 | -0.0123 | 0.1852 | 0.1492 | 0.0485 | 0.4610 | 0.078 |
| occlusion@0.2 | 0.8070 | -0.0413 | 0.8993 | -0.0268 | 0.1487 | 0.2373 | 0.0450 | 0.5091 | 0.133 |
| occlusion@0.3 | 0.7590 | -0.0893 | 0.8810 | -0.0451 | 0.1000 | 0.3819 | 0.0907 | 0.5809 | 0.206 |
| low_quality_upload@0.75_75 | 0.5168 | -0.3315 | 0.8269 | -0.0992 | 0.0024 | 0.9640 | 0.4359 | 0.9394 | 0.510 |
| low_quality_upload@0.5_50 | 0.5000 | -0.3483 | 0.6360 | -0.2901 | 0.0000 | 1.0000 | 0.4957 | 0.9992 | 0.529 |
| low_quality_upload@0.35_30 | 0.4999 | -0.3485 | 0.5314 | -0.3947 | 0.0003 | 1.0000 | 0.4964 | 0.9997 | 0.529 |

Per-generator and per-source error rates for every condition: `robustness_by_group.csv`. Figure specs: FIG0016, FIG0017.

## Limits

- Perturbations are synthetic and applied after preprocessing (to the 224 px face crop), not to the original upload.
- One model, one seed, one split. No statistical test (Phase E11).
- `threshold_shift` marks where recalibration might help; it has not been tried. Any recalibration needs a new Evaluation ID.
- Patterns describe where performance changes, not why.
