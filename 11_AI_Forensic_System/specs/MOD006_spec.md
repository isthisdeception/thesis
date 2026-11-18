# Module Spec: MOD006

**Module ID:** MOD006  
**Name:** Evidence Validation  
**Version:** 0.1.0  
**Status:** implemented  
**Date:** 2026-11-17  
**Code:** `evidence/validation/`

**Purpose:** Judge the reliability of each recorded evidence item. Items are not treated as equally reliable. This module does not drop an item to make the case look cleaner, and it does not decide the case.

**Inputs:** Evidence rows for one case, by `EV` id, after MOD005. It does not open the image.

**Outputs:** A new registry row per item, appended after the collector row. The collector row is not rewritten. The new row's Quality is `high`, `medium`, `low`, or `unusable`, and its Status is `validated` or `failed`. Its Dependencies name the collector row and, when two items conflict, the other collector row. Processed Output carries `validation_reason`. Low confidence, poor image quality, face-detection failure, incomplete metadata, model uncertainty, and conflict are reasons. Neither item is deleted.

**Dependencies:** MOD005. MOD016 when the validation step itself cannot finish. No model.

**Configuration:** The quality labels. The conditions that map to `unusable`, as named checks rather than a hidden score. The numeric cutoffs, when a later step chooses them, are configuration and are not chosen in this spec.

**Testing:** An item with an empty collector confidence remains in the registry and is not given a filled-in confidence. Two items that the configured checks call conflicting both remain, each with the other's id in Dependencies. An `unusable` item is still visible to MOD007, marked `unusable`.

**Fused items (STEP-056):** a MOD007 `fused_conclusion` row is validated like any other item. Named checks: `fused_output_incomplete` (no strategy id or summary → `unusable`), `fused_conflict` (contested lean or directional conflict → `low`), `no_directional_evidence` (→ `low`), `single_source` (→ `medium`).

**Confidence items (STEP-057):** a MOD009 `confidence` row is validated like any other item. Named checks: `confidence_output_incomplete` (missing formula id or any of the four confidence keys → `unusable`), `decision_confidence_unavailable` (`decision_confidence` is empty → `low`).

**Future Extensions:** Further reliability checks, each named in configuration.

**Interfaces:** Reads and annotates the evidence schema. It does not implement `EvidenceCollector` or `FusionStrategy`.

**Failure Handling:** If validation cannot complete, MOD016 records `unexpected_error` and no item is silently marked `high`.
