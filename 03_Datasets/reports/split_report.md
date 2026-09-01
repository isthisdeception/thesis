# Split Report (STEP-028 / Phase D12)

> Generated: 2026-09-01

## Summary

| Split ID | Output | Scheme | Train | Val | Test | Leakage | Fingerprint |
|----------|--------|--------|------:|----:|-----:|---------|-------------|
| SPLIT0001 | DS0001_PP0001 | grouped_random | 34993 | 7502 | 7505 | PASS | `ff16279f2fe09c70…` |
| SPLIT0002 | DS0001_PP0001 | logo | 40873 | 7204 | 1923 | PASS | `8caf8ab38f094785…` |
| SPLIT0001 | DS0002_PP0002 | grouped_random | 36985 | 7103 | 7364 | PASS | `2752b608c9f46328…` |
| SPLIT0002 | DS0002_PP0002 | logo | 39718 | 6087 | 5647 | PASS | `fca325246b312d52…` |
| SPLIT0001 | DS0003_PP0003 | official_holdout | 101999 | 18001 | 20000 | PASS | `76ec5f3ad98dcd79…` |
| SPLIT0002 | DS0003_PP0003 | logo | 59499 | 10501 | 70000 | PASS | `2768a8b3070381aa…` |
| SPLIT0001 | DS0004_PP0006 | grouped_random | 7001 | 1498 | 1500 | PASS | `87c9d974f696ab0a…` |
| SPLIT0002 | DS0004_PP0006 | logo | 7648 | 1351 | 1000 | PASS | `62ae46771e01633e…` |
| SPLIT0001 | DS0005_PP0005 | official_holdout | 64372 | 11364 | 21962 | PASS | `40c4a0cc48c3454d…` |
| SPLIT0002 | DS0005_PP0005 | grouped_random | 68416 | 14641 | 14641 | PASS | `21475a42f7909307…` |

## Per-split notes

### DS0001_PP0001_SPLIT0001
- Scheme: `grouped_random` (seed=42)
- Notes: Primary train split; groups by identity+generator.

### DS0001_PP0001_SPLIT0002
- Scheme: `logo` (seed=42)
- Notes: Leave-one-generator-out (stable_diffusion held out for test).

### DS0002_PP0002_SPLIT0001
- Scheme: `grouped_random` (seed=42)
- Notes: DiFF eval pool internal grouped split (fake-only).

### DS0002_PP0002_SPLIT0002
- Scheme: `logo` (seed=42)
- Notes: LOGO: Midjourney held out for unseen-generator eval (E9).

### DS0003_PP0003_SPLIT0001
- Scheme: `official_holdout` (seed=42)
- Notes: Respect native train/valid; valid->test, train subsplit train/val by hash groups.

### DS0003_PP0003_SPLIT0002
- Scheme: `logo` (seed=42)
- Notes: LOGO: stylegan fakes held out (native valid still test when present).

### DS0004_PP0006_SPLIT0001
- Scheme: `grouped_random` (seed=42)
- Notes: Synthbuster grouped by RAISE/synth stem identity.

### DS0004_PP0006_SPLIT0002
- Scheme: `logo` (seed=42)
- Notes: LOGO: dalle3 generator held out for frequency supplementary eval.

### DS0005_PP0005_SPLIT0001
- Scheme: `official_holdout` (seed=42)
- Notes: FairFace official val->test; train subsplit for tuning.

### DS0005_PP0005_SPLIT0002
- Scheme: `grouped_random` (seed=42)
- Notes: Alternate grouped random split for bias ablations.

