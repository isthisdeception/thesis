# Module Spec: MOD014

**Module ID:** MOD014  
**Name:** Frontend Interaction  
**Version:** 0.1.0  
**Status:** specified  
**Date:** 2026-11-17

**Purpose:** Describe what the user sees during an investigation. The screen shows progress and the records the API returned. It does not infer, score, or decide. The implementation of the pages belongs to the web application, not to this step.

**Inputs:** The JSON from MOD013. In particular the status label, the evidence rows, `decision.json`, `explanation.json`, and the report.

**Outputs:** A progress sequence and a result layout. Progress labels, in order: Uploading, Validating, Detecting Face, Running Analysis, Collecting Evidence, Evaluating Confidence, Generating Explanation, Preparing Report, Complete. The result shows the decision word, the four confidence fields, the evidence ids, and the limitations. It does not show a bare "Fake" plus a single percentage as the whole result.

**Dependencies:** MOD013 for every fact on screen. No model, no image analysis, and no direct read of the evidence registry except through the API.

**Configuration:** The API base URL comes from the frontend environment. It is not hardcoded in a page. Labels above are the specified copy.

**Testing:** A later UI test feeds a decision of Inconclusive with an empty decision confidence and checks that both are visible. A test that disconnects the API shows the MOD016 message and does not display a decision. No test places a model call in the frontend.

**Future Extensions:** History and accounts, after those API routes exist. The progress labels stay unless the pipeline changes.

**Interfaces:** HTTP client of MOD013 only. It does not implement `EvidenceCollector` or `FusionStrategy`.

**Failure Handling:** Network failure, timeout, and a backend error show the message from the API. The screen does not substitute a verdict.
