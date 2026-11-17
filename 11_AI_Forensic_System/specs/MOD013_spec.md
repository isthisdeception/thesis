# Module Spec: MOD013

**Module ID:** MOD013  
**Name:** API Layer  
**Version:** 0.1.0  
**Status:** specified  
**Date:** 2026-11-17

**Purpose:** Define the HTTP boundary that starts an investigation and returns its records. This step specifies the endpoints. It does not implement them. The API does not run a model and does not choose a decision. It calls the pipeline and returns the records the pipeline wrote.

**Inputs:** HTTP requests as in the handbook contract. File bytes arrive only at the upload endpoint and are passed to MOD001.

**Outputs:** HTTP responses that carry ids and the JSON files the other modules wrote. Status responses use the Module 14 progress labels.

**Dependencies:** MOD001 for upload, the pipeline through MOD012 for a finished case, MOD015 for the case row, MOD016 for error bodies. The backend that will host these routes is `13_Backend`, in a later step.

**Configuration:** The route table below is the contract. Authentication is future and is not required by this spec.

**Testing:** A later API test checks that `GET /cases/{id}/decision` returns `decision.json` unchanged and does not add a label. `GET /health` and `GET /version` do not load a case. Upload of an unsupported file returns the MOD016 record and no decision.

**Future Extensions:** Authentication, history, and batch upload, as the handbook lists them. Each new route is added to this table before it is implemented.

**Interfaces:** The routes are:

| Method | Endpoint | Returns |
|---|---|---|
| POST | `/cases` | A new case id |
| GET | `/cases/{id}` | The case row |
| POST | `/cases/{id}/upload` | The MOD001 input record |
| GET | `/cases/{id}/status` | The progress label |
| GET | `/cases/{id}/evidence` | The evidence ids and rows |
| GET | `/cases/{id}/decision` | `decision.json` |
| GET | `/cases/{id}/explanation` | `explanation.json` |
| GET | `/cases/{id}/report` | The report |
| GET | `/health` | Health |
| GET | `/version` | System, model, dataset, and Git versions |

This module does not implement `EvidenceCollector` or `FusionStrategy`.

**Failure Handling:** Pipeline failures are returned as the MOD016 record. Stack traces are not part of the response. They stay in the server log.
