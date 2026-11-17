# Module Spec: MOD015

**Module ID:** MOD015  
**Name:** Audit Trail  
**Version:** 0.1.0  
**Status:** specified  
**Date:** 2026-11-17

**Purpose:** Append one case row for every investigation so the decision can be traced to its input, its evidence ids, its model, and its errors.

**Inputs:** Case id, timestamps, `input_id`, the list of `EV` ids, the decision word, model id, system version, the configuration id used for the run, execution time, and the MOD016 ids for errors and warnings.

**Outputs:** One append-only row in `case_registry.csv`. The Evidence column holds the `EV` ids. The Decision column holds the decision word or empty while the case is still running. A finished case is not rewritten to hide an error. A follow-up is a new row or a status change that preserves the original decision text.

**Dependencies:** MOD001 for the input id, MOD005 for evidence ids, MOD008 for the decision, MOD016 for error ids. The canonical columns are already the header of `case_registry.csv`.

**Configuration:** The path of `case_registry.csv`.

**Testing:** A finished case row contains the same evidence ids as the registry rows for that case and the same decision word as `decision.json`. An investigation that fails before a decision still has a row, with Decision empty and Errors set. Rows are not deleted by a later successful run.

**Future Extensions:** Case history queries, served by a future API route, reading this file.

**Interfaces:** Writes the case registry. It does not implement `EvidenceCollector` or `FusionStrategy` and does not open the image.

**Failure Handling:** If the row cannot be appended, MOD016 records `unexpected_error`. The investigation does not report Complete while the case row is missing.
