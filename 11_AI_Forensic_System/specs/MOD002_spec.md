# Module Spec: MOD002

**Module ID:** MOD002  
**Name:** Image Validation Engine  
**Version:** 0.1.0  
**Status:** specified  
**Date:** 2026-11-17

**Purpose:** Check one accepted input before any collector runs. A failed check stops the investigation with a structured failure. The module does not repair the image and does not decide the case.

**Inputs:** `input_id` and the stored file from MOD001. It reads the image bytes only to measure them.

**Outputs:** A validation record on the input: status `passed` or `failed`, and the measured format, corruption flag, channel count, width, height, compression marker, missing-data flag, quality note, and face availability. On failure, a MOD016 report. Face availability is this module's gate: `no_face` or `multiple_faces` stops the pipeline. The face_detection collector still writes its own evidence item when validation has passed, and it does not read this module's measurement.

**Dependencies:** MOD001 for the stored file. MOD016 for failures. No model.

**Configuration:** Supported formats, minimum resolution, allowed channel counts, and the corruption checks that constitute failure. Values are configuration, not constants buried in a later module.

**Testing:** A truncated file, a file whose contents disagree with its extension, an image with no decodable pixels, and an image below the minimum resolution each yield `failed` and a MOD016 record. A decodable image inside the limits yields `passed`. No test expects a Real or Fake label.

**Future Extensions:** Stricter quality scores. Those scores are extra fields on the validation record, not a second decision.

**Interfaces:** The `passed` or `failed` status is the gate `EvidenceCollector` checks. This module is not a collector.

**Failure Handling:** Integrity failure, unsupported content, corruption, missing pixels, and resolution outside the configured limits call MOD016 (`corrupted_image`, `unsupported_format`, or `unexpected_error`) and do not start MOD003. The failure names the measurement. It does not say the image is fake.
