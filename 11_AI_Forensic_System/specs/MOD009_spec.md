# Module Spec: MOD009

**Module ID:** MOD009  
**Name:** Confidence Estimation  
**Version:** 0.1.0  
**Status:** implemented  
**Date:** 2026-11-18  
**Code:** `confidence/` (`confidence/estimator.py`, `confidence/calibration.py`, `confidence/confidence_config.json`)

**Purpose:** Report four different confidence values for one case. The fake-class probability from MOD004 is not any of these four until this module says how it used that probability. Uncertainty stays empty rather than being replaced by a high number.

**Inputs:** Validated evidence ids for the case, including `deep_learning_prediction` when that collector ran and `fused_conclusion` when MOD007 ran. No image bytes and no file paths.

**Outputs:** One evidence item, Evidence Type `confidence`, Source Module MOD009, registered by MOD005 and validated by MOD006. Processed Output contains:

- `prediction_confidence` — empirical validation-set accuracy for the detector's predicted class at its frozen threshold (`08_Evaluation/EVAL0001/confidence_distribution.csv`, `split=val`), scaled by the detector item's MOD006 reliability weight. Distinct from the raw probability $P(\text{fake})$
- `evidence_confidence` — mean MOD006 reliability weight across the case's validated collector items (`high=1.0`, `medium=0.6`, `low=0.3`, `unusable=0.0`), penalized when validation flags conflicting evidence
- `system_confidence` — fraction of usable validated collector items among all collector attempts, refused ids, and prior MOD016 case failures
- `decision_confidence` — confidence attached to the decision MOD008 will cite: weighted blend (`0.5 * prediction + 0.3 * evidence + 0.2 * system`), bounded by weak evidence/system health and discounted for single-source (`0.85`) or contested (`0.5`) leans

Each value is a number from 0 to 1 or empty (`null`). The item also stores `supporting_ids`, `unresolved`, `calibration_details`, `formula_id`, `formula_version`, `formula_status`, and `interpretations`.

**Dependencies:** MOD005 and MOD006. MOD004 only through its evidence item. Phase E4 calibration tables (`08_Evaluation/EVAL0001/`). MOD008 reads this item and does not compute a second, hidden confidence.

**Configuration:** `confidence/confidence_config.json` (`formula_id: "e4_calibrated_v1"`, approved in DEC0010 (Human, 2026-11-18)).

**Testing:** `tests/test_decision_confidence.py`. When the deep-learning probability is 0.99 and every other evidence item is `unusable`, `prediction_confidence` (~0.9717) is not reported as `decision_confidence` (≤ 0.25). An empty collector confidence stays empty on the source item in `evidence_registry.csv` after this module runs. Missing detector leaves `prediction_confidence` and `decision_confidence` empty (`null`). The confidence item names the source ids.

**Future Extensions:** Additional versioned formulas under `formula_id` without renaming the four fields.

**Interfaces:** Writes an evidence item. It is not a collector of image measurements and not a fusion strategy.

**Failure Handling:** If the module cannot produce the record, MOD016 records `unexpected_error` and MOD008 does not invent the four numbers.
