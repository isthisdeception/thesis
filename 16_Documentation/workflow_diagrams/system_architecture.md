# Three-Tier System Architecture Diagram

Companion to [architecture.md](../architecture.md) and [integration_guide.md](../integration_guide.md).

## Component & Data-Flow Overview

```mermaid
flowchart LR
    U["Human User / Browser"] -->|"HTTP/UI Routes"| WEB["12_Web: React + Vite (MOD014)"]
    WEB -->|"src/api/forensicApi.js (VITE_API_BASE_URL)"| API["13_Backend: Django + DRF (MOD013)"]

    subgraph BackendApps["13_Backend Apps"]
        API_APP["apps.api (10 REST endpoints)"]
        FE_APP["apps.forensic_engine (Job Manager + _PIPELINE_LOCK)"]
        EV_APP["apps.evidence (Read-only adapter)"]
        REP_APP["apps.reports (JSON/MD/HTML)"]
        HLT_APP["apps.health & apps.versioning"]
        API_APP --> FE_APP
        API_APP --> EV_APP
        API_APP --> REP_APP
        API_APP --> HLT_APP
    end

    API --> API_APP
    FE_APP -->|"run_investigation()"| CORE["11_AI_Forensic_System (MOD001-MOD018)"]

    subgraph Registries["Persistent Registries & Storage"]
        MREG["05_Models/model_registry.csv"]
        EREG["11_AI_Forensic_System/evidence_registry.csv (EV ids)"]
        CREG["11_AI_Forensic_System/case_registry.csv (CASE ids)"]
        MEDIA["FORENSIC_MEDIA_ROOT/cases/{case_id}/"]
    end

    CORE -->|"MOD004 model lookup"| MREG
    CORE -->|"MOD005 append EV rows"| EREG
    CORE -->|"MOD015 append CASE row"| CREG
    CORE -->|"MOD001-MOD016 artifacts"| MEDIA
    EV_APP -.->|"Read only"| EREG
    EV_APP -.->|"Read only"| MEDIA
    REP_APP -.->|"Read only"| MEDIA
```

## Asynchronous Investigation Sequence (`thread` mode)

```mermaid
sequenceDiagram
    actor User
    participant Web as 12_Web (src/api)
    participant API as 13_Backend (MOD013)
    participant Eng as forensic_engine
    participant Sys as 11_AI_Forensic_System

    User->>Web: Open /investigate/upload & select image
    Web->>API: POST /api/v1/cases
    API-->>Web: 201 Created (case_id, stage="Created")
    Web->>API: POST /api/v1/cases/{id}/upload (multipart/form-data)
    API->>Sys: MOD001 receive_upload()
    alt Rejected by MOD001 (empty, >20MB, bad ext)
        Sys-->>API: MOD016 failure record + failed MOD015 row
        API-->>Web: 400 Bad Request (MOD016 JSON envelope)
    else Accepted by MOD001
        API->>Eng: Submit background worker job
        API-->>Web: 202 Accepted (input_id, stage="Uploading")
        loop Every VITE_POLL_INTERVAL_MS
            Web->>API: GET /api/v1/cases/{id}/status
            API-->>Web: 200 OK (stage, stage_history, progress_percent)
        end
        Eng->>Sys: run_investigation() under _PIPELINE_LOCK
        Sys-->>Eng: InvestigationResult (artifacts + registries)
        Web->>API: GET /decision, /evidence, /explanation, /report
        API-->>Web: 200 OK (unchanged pipeline records)
    end
```
