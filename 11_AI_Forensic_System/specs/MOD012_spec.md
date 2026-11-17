# Module Spec: MOD012

**Module ID:** MOD012  
**Name:** Report Generator  
**Version:** 0.1.0  
**Status:** specified  
**Date:** 2026-11-17

**Purpose:** Write the case report from the decision, the evidence ids, the explanation data, and the version stamps. The report is reproducible from those records. It does not recompute a prediction.

**Inputs:** Case id. `decision.json` from MOD008. The evidence ids it cites. `explanation.json` from MOD010. The reasoning record from MOD011. Version fields: system version, model id, dataset id, experiment id, and Git commit, taken from the case configuration and the model registry row. Execution statistics from the case record.

**Outputs:** The case report in JSON and Markdown, using the Case Report sections: Case ID, input summary, evidence summary, model results, confidence, explanation, decision, limitations, recommendations, execution stats, and the version stamps above. HTML is a third rendering of the same fields. PDF is future. Input summary cites `input_id` and MOD002's validation status. It does not embed a new measurement.

**Dependencies:** MOD008, MOD010, MOD011, MOD015 for the case id, and the model registry for the version stamps. MOD016 if a required section has no source record.

**Configuration:** Which of JSON, Markdown, and HTML to write. The path is under the case directory, outside Git.

**Testing:** The model id, dataset id, experiment id, and Git commit in the report match the case configuration byte for byte. Removing `decision.json` from the input prevents the report. The evidence summary lists ids that exist in the registry and no other ids. Limitations includes empty confidence values rather than omitting them.

**Future Extensions:** PDF, generated from the same JSON.

**Interfaces:** Reads evidence records and the decision file. It does not implement `EvidenceCollector` or `FusionStrategy`.

**Failure Handling:** A missing decision, a missing version stamp, or an evidence id that is not in the registry calls MOD016 `unexpected_error`. The report is not written with a blank version presented as known.
