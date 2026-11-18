# Phase E14 — AI Forensic Analyst Evaluation Report (`EVAL0007`)

**Evaluation ID:** EVAL0007  
**Experiment / Model Reference:** EXP0001 / MODEL0001 (+ MODEL0008 for multi-specialist conflict evaluation)  
**Date:** 2026-11-18  
**Runner:** `11_AI_Forensic_System/evaluate_e14.py`  
**Outputs:** `e14_case_results.csv`, `e14_dimension_summary.csv`, `e14_failure_recovery.csv`

---

## 1. Scope & Purpose

Phase E14 evaluates the **whole AI Forensic Analyst platform** (`11_AI_Forensic_System/`, Modules 1–12, 15–18) across 16 end-to-end investigation scenarios:
- **E14-01 – E14-08:** The eight canonical `EXP0001` test cases from `08_Evaluation/EXP0001/gradcam_sample.csv` (2 true positives, 2 true negatives, 2 false positives, 2 false negatives at frozen threshold `0.3951`).
- **E14-09 – E14-12:** Multi-specialist conflict (`MODEL0001` vs `MODEL0008`), unusable supporting evidence with high detector score ($P(\text{fake}) = 0.99$), missing model export (`MODEL9999`), and detector inference timeout.
- **E14-13 – E14-16:** Intake and image-validation stops (`unsupported_format`, `corrupted_image`, `no_face`, `multiple_faces`).

---

## 2. E14 Dimension Summary (`e14_dimension_summary.csv`)

| Dimension | Metric | Observed Value | Status |
|---|---|---|---|
| **Evidence completeness** | Collectors registered (`MOD005`) and validated (`MOD006`) on clean cases | 10/10 collectors (24 `EV` rows/case incl. `MOD006` + `MOD007` + `MOD009`) | PASS |
| **Fusion quality** | Swappable `FusionStrategy` (`rule_based`, DEC0009); leans match expected rules | 12/12 completed cases | PASS |
| **Decision consistency** | `MOD008` decisions match 4-way rules (`Fake`/`Real`/`Inconclusive`/`Unknown`) with zero image access | 16/16 scenarios | PASS |
| **Confidence consistency** | `MOD009` E4 `val`-calibrated (`DEC0010`), distinct from raw softmax, `null` when directional evidence absent | 12/12 completed cases | PASS |
| **Report quality** | `MOD012` Template 24 JSON/Markdown/HTML with byte-identical version and Git commit stamps | 12/12 completed cases (4/4 failed stops produce no report) | PASS |
| **Reasoning quality** | `MOD011` `EV`-grounded sentences verified by `verify_sentence`; zero ungrounded sentences | 135 verified sentences, 0 ungrounded leaks | PASS |
| **Execution time** | End-to-end pipeline latency per case (excluding external GPU model load) | mean `60.02 ms`, max `149.08 ms` | PASS |
| **Module failures** | Structured `MOD016` records across all 8 canonical failure modes | 8/8 canonical modes verified; 0 silent failures | PASS |
| **Recovery behavior** | Graceful degradation (`Inconclusive`/`Unknown`) or clean stop with `MOD015` audit row | 7/7 fault scenarios verified | PASS |

---

## 3. Key Findings

1. **Separation of detector score and forensic decision:** In `E14-10`, the detector emits $P(\text{fake}) = 0.99$ (`prediction_confidence = 0.971745`), but because the supporting collectors are marked `unusable` by `MOD006`, `evidence_confidence` and `system_confidence` drop to `0.333333`, pulling `decision_confidence` to `0.333333` (`< 0.50`). `MOD008` outputs `Inconclusive` and records a `low_confidence` warning rather than repeating `0.99` as a `Fake` verdict.
2. **Explicit uncertainty on missing or timed-out specialists:** In `E14-11` (`model_unavailable`) and `E14-12` (`timeout`), the 9 non-detector collectors still execute and validate (`evidence_confidence = 0.888889`, `system_confidence = 0.800000`), `prediction_confidence` and `decision_confidence` remain `null` (never filled with a placeholder), and `MOD008` outputs `Unknown`.
3. **Intake and validation gates:** In `E14-13`–`E14-16`, rejected or invalid uploads stop before collectors run, write no `decision.json` or report, and append a `failed` row in `case_registry.csv` with `Decision=""` and `Errors` populated.
