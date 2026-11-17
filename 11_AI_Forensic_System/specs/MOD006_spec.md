# Module Spec: MOD006

**Module ID:** MOD006  
**Name:** Evidence Validation  
**Version:** 0.1.0  
**Status:** specified  
**Date:** 2026-11-17

**Purpose:** Judge the reliability of each recorded evidence item. Items are not treated as equally reliable. This module does not drop an item to make the case look cleaner, and it does not decide the case.

**Inputs:** Evidence rows for one case, by `EV` id, after MOD005. It does not open the image.

**Outputs:** The same rows updated in place only for Quality and Status. Quality becomes `high`, `medium`, `low`, or `unusable`. Status becomes `validated` or `failed`. A short reason is stored in Description's existing text only by appending the validation reason, or in Processed Output under a `validation_reason` field. Low confidence, poor image quality, face-detection failure, incomplete metadata, model uncertainty, and conflict with another item are reasons. Conflict is recorded on both items. Neither item is deleted.

**Dependencies:** MOD005. MOD016 when the validation step itself cannot finish. No model.

**Configuration:** The quality labels. The conditions that map to `unusable`, as named checks rather than a hidden score. The numeric cutoffs, when a later step chooses them, are configuration and are not chosen in this spec.

**Testing:** An item with an empty collector confidence remains in the registry and is not given a filled-in confidence. Two items that the configured checks call conflicting both remain, each with the other's id in Dependencies. An `unusable` item is still visible to MOD007, marked `unusable`.

**Future Extensions:** Further reliability checks, each named in configuration.

**Interfaces:** Reads and annotates the evidence schema. It does not implement `EvidenceCollector` or `FusionStrategy`.

**Failure Handling:** If validation cannot complete, MOD016 records `unexpected_error` and no item is silently marked `high`.
