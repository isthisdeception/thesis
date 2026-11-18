# Module Spec: MOD009

**Module ID:** MOD009  
**Name:** Confidence Estimation  
**Version:** 0.1.0  
**Status:** specified  
**Date:** 2026-11-17

**Purpose:** Report four different confidence values for one case. The fake-class probability from MOD004 is not any of these four until this module says how it used that probability. Uncertainty stays empty rather than being replaced by a high number.

**Inputs:** Validated evidence ids for the case, including `deep_learning_prediction` when that collector ran. No image bytes.

**Outputs:** One evidence item, Evidence Type `confidence`, registered by MOD005 and validated by MOD006. Processed Output contains:

- `prediction_confidence` — confidence in the detector output, distinct from the raw probability
- `evidence_confidence` — confidence in the body of evidence
- `system_confidence` — confidence in the system run, including failures and missing collectors
- `decision_confidence` — confidence attached to the decision MOD008 will cite

Each value is a number from 0 to 1 or empty. The item also stores the evidence ids used. The formula that fills the numbers is not chosen in this spec. A later step proposes it for approval. Until then, an implementation may leave a value empty and must not invent a placeholder.

**Dependencies:** MOD005 and MOD006. MOD004 only through its evidence item. MOD008 reads this item and does not compute a second, hidden confidence.

**Configuration:** Names of the four fields. Later, the formula id. No formula id is selected here.

**Testing:** When the deep-learning probability is 0.99 and every other evidence item is `unusable`, `prediction_confidence` is not reported as if it were the decision confidence. An empty collector confidence is still empty on the source item after this module runs. The confidence item names the source ids.

**Future Extensions:** A documented formula, versioned, without renaming the four fields.

**Interfaces:** Writes an evidence item. It is not a collector of image measurements and not a fusion strategy.

**Failure Handling:** If the module cannot produce the record, MOD016 records `unexpected_error` and MOD008 does not invent the four numbers.
