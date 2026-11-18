# Module Spec: MOD001

**Module ID:** MOD001  
**Name:** Input Management  
**Version:** 0.1.0  
**Status:** specified  
**Date:** 2026-11-17

**Purpose:** Receive one uploaded file for an existing case, check that the file is a supported image of an allowed size, give it an input id, and store its metadata. This module does not decide whether the image is real or fake.

**Inputs:** Case id. The uploaded bytes and the declared filename. The allowed formats and the maximum size come from configuration.

**Outputs:** `input_metadata.json` for that input. Fields: `input_id` (`{case_id}-input-{seq}`), case id, declared filename, stored path, byte size, declared format, received timestamp, and either `accepted` or a failure id from MOD016. The stored file is the source later collectors read. The file is not committed to Git.

**Dependencies:** MOD016 for the failure record. No collector and no model.

**Configuration:** Allowed formats. Maximum byte size. Minimum and maximum edge length recorded here only as limits that reject a file before MOD002. The storage directory, which is outside the Git tree.

**Testing:** An accepted file produces one `input_metadata.json` and a new input id. A second upload for the same case does not overwrite the first file. An empty file, an oversized file, and a disallowed extension each produce a MOD016 failure and no stored image.

**Future Extensions:** Batch upload. That extension still writes one input id per file.

**Interfaces:** Writes the input record that `EvidenceCollector` later receives as `input_id`. Does not implement `EvidenceCollector` or `FusionStrategy`.

**Failure Handling:** Unsupported format, empty file, and size outside the configured limits go to MOD016 as `unsupported_format` or `unexpected_error` with the measured size. The module does not continue to validation after a rejection.
