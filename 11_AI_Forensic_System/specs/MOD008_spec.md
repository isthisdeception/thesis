# Module Spec: MOD008

**Module ID:** MOD008  
**Name:** Decision Engine  
**Version:** 0.1.0  
**Status:** implemented  
**Date:** 2026-11-18  
**Code:** `decision/` (`decision/engine.py`, `decision/decision_config.json`)

**Purpose:** Read the validated fused evidence and the validated confidence record, and write the case decision. The decision is one of Real, Fake, Inconclusive, or Unknown.

**Inputs:** The `EV` id of the validated `fused_conclusion`. The `EV` id of the validated confidence record from MOD009. Decision metadata allowed in the input is the case id and those evidence ids. This module does not receive image bytes, a path used to open the image, model weights, or a collector's private objects; any forbidden argument (`image`, `image_path`, `image_bytes`, `stored_path`, `model`, `weights`) or non-`EV` id is refused via MOD016.

**Outputs:** `decision.json` (`decision/README.md`). Fields: `case_id`, `decision`, `fused_evidence_id`, `confidence_evidence_id`, `reasoning_path` (ordered list of cited `EV` ids), and `decision_metadata` (`module_id`, `version`, `strategy_id` copied from the fused item, `rule_id`, `rule_version`, `rule_status`, `lean`, `confidence`, `reasoning_steps`, `warning_failure_ids`, `timestamp`). The file cites ids. It does not restate measurements that are not on those evidence rows.

**Dependencies:** MOD007 for the fused item. MOD009 for the confidence record. MOD006 must have validated both before this module reads them. MOD016 if either id is missing or not `validated`. No dependency on MOD001's file store.

**Configuration:** `decision/decision_config.json` (approved in DEC0010, Human, 2026-11-18): the four allowed decision words (`Real`, `Fake`, `Inconclusive`, `Unknown`), `positive_class_decisions` (`fake` → `Fake` / `Real`), `min_decision_confidence` (`0.50`), `low_confidence_warning_below` (`0.50`), `stop_on_low_confidence` (`false`), and `inconclusive_on_validation_conflict` (`true`).
- `Unknown`: when the fused item has `lean == "no_directional_evidence"` (e.g., missing detector) or an unmapped positive class.
- `Inconclusive`: when the fused lean is `contested`, validation flagged conflicting evidence, or `decision_confidence` is empty or below `min_decision_confidence` (recording a MOD016 `low_confidence` warning).
- `Fake` / `Real`: when `decision_confidence >= min_decision_confidence`, no conflict is present, and the fused lean is `positive_class` / `negative_class`.

**Testing:** `tests/test_decision_confidence.py`. Supplying only the two validated evidence records produces `decision.json` (`Fake`, `Real`, `Inconclusive`, `Unknown`). Supplying an image path or missing evidence ids writes a MOD016 failure and no `decision.json`. Unvalidated, `unusable`, or absent ids call MOD016 and write no `decision.json`.

**Future Extensions:** More decision metadata fields. The four words stay the vocabulary unless the handbook changes.

**Interfaces:** Consumes evidence records. It does not implement `EvidenceCollector` or `FusionStrategy`.

**Failure Handling:** Missing fused evidence, unvalidated evidence, or a confidence record that is absent calls MOD016 (`low_confidence` when `decision_confidence` is below threshold, otherwise `unexpected_error`). The module does not open the image to resolve the gap.
