# Module Spec: MOD008

**Module ID:** MOD008  
**Name:** Decision Engine  
**Version:** 0.1.0  
**Status:** specified  
**Date:** 2026-11-17

**Purpose:** Read the validated fused evidence and the validated confidence record, and write the case decision. The decision is one of Real, Fake, Inconclusive, or Unknown.

**Inputs:** The `EV` id of the validated `fused_conclusion`. The `EV` id of the validated confidence record from MOD009. Decision metadata allowed in the input is the case id and those evidence ids. This module does not receive image bytes, a path used to open the image, model weights, or a collector's private objects.

**Outputs:** `decision.json`. Fields: case id, decision, the fused evidence id, the confidence evidence id, a reasoning-path list of evidence ids, and decision metadata (strategy id copied from the fused item, timestamp). The file cites ids. It does not restate measurements that are not on those evidence rows.

**Dependencies:** MOD007 for the fused item. MOD009 for the confidence record. MOD006 must have validated both before this module reads them. MOD016 if either id is missing or not `validated`. No dependency on MOD001's file store.

**Configuration:** The four allowed decision words. Any numeric rule that maps the fused item onto one of those words is configuration owned by a later step, reviewed as a scientific choice. This spec fixes the vocabulary and the inputs, not that rule.

**Testing:** A test that supplies only the two evidence records can produce a `decision.json`. A test that supplies an image path and no evidence ids does not run the decision. If the fused item is `unusable` or absent, the decision is not guessed; MOD016 runs. Unknown is the outcome when the evidence needed to choose is not there, and that outcome is written explicitly rather than omitted.

**Future Extensions:** More decision metadata fields. The four words stay the vocabulary unless the handbook changes.

**Interfaces:** Consumes evidence records. It does not implement `EvidenceCollector` or `FusionStrategy`.

**Failure Handling:** Missing fused evidence, unvalidated evidence, or a confidence record that is absent calls MOD016 (`low_confidence` only when that is the configured condition, otherwise `unexpected_error`). The module does not open the image to resolve the gap.
