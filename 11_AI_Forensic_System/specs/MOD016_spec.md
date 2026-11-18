# Module Spec: MOD016

**Module ID:** MOD016  
**Name:** Failure Handling  
**Version:** 0.1.0  
**Status:** specified  
**Date:** 2026-11-17

**Purpose:** Record every pipeline failure as a structured report. Callers stop or continue only as their own specs say. No caller catches an error and continues without a record.

**Inputs:** A failure name, the module id that raised it, the case id, the input id when one exists, a short measured detail, and a timestamp.

**Outputs:** A failure record with a failure id, stored with the case and cited from the case registry Errors or Warnings column. The names this module accepts are: `no_face`, `multiple_faces`, `corrupted_image`, `unsupported_format`, `model_unavailable`, `low_confidence`, `timeout`, `unexpected_error`. Any other name is stored as `unexpected_error` and the original name is kept in the detail, so a typo cannot create a silent category.

**Dependencies:** None on the image or the model. MOD015 cites the failure ids. Every other module may call this one.

**Configuration:** Which of the names are warnings rather than stops. `low_confidence` is a warning unless MOD008's later rule says it stops the decision. `no_face` and `multiple_faces` are records from the face_detection collector; they do not by themselves become a Fake decision.

**Testing:** Each accepted name can be written and read back with the calling module id. A failure written for a case appears on that case row. A caller that simulates a corrupt image does not produce a decision file.

**Future Extensions:** Further names, added here before modules start using them.

**Interfaces:** A single report function used by every module. It is not a collector and not a fusion strategy.

**Failure Handling:** This module is the handler. If it cannot store the record, the pipeline stops and the server log holds the detail. The user-facing API still receives no stack trace.
