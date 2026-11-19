# AI Forensic Analyst Pipeline Workflow (`MOD001`–`MOD018`)

Companion to [architecture.md](../architecture.md) and [11_AI_Forensic_System/architecture.md](../../11_AI_Forensic_System/architecture.md).

## End-to-End Forensic Pipeline & Failure Gates

```mermaid
flowchart TD
    S0["Stage 1: Uploading - MOD001 Input Management"] --> G1{"Accepted? ext, non-empty, <=20MB"}
    G1 -->|"No"| F1["MOD016 failure: unsupported_format -> MOD015 failed row"]
    G1 -->|"Yes"| S1["Stage 2-3: Validating & Detecting Face - MOD002"]
    S1 --> G2{"Image & Face valid?"}
    G2 -->|"No"| F2["MOD016 failure: corrupted_image / no_face / multiple_faces -> MOD015 failed row"]
    G2 -->|"Yes"| COL

    subgraph COL["Stage 4-5: Running Analysis & Collecting Evidence"]
        M3["MOD003: 9 Independent Collectors (meta, stats, face, freq, comp, color, texture, explainability_input)"]
        M4["MOD004: Deep Learning Specialist (MODEL0001 -> P_fake, threshold 0.395)"]
    end

    COL --> REG["MOD005 Evidence Registry: Assign immutable EVxxxxxx IDs"]
    REG --> VAL["MOD006 Evidence Validation: Mark high/medium/low/unusable & conflict citations"]
    VAL --> FUS["MOD007 Fusion Engine: FusionStrategy (rule_based, DEC0009) -> fused_conclusion"]
    FUS --> CON["Stage 6: Evaluating Confidence - MOD009 E4 Calibrated Confidence (DEC0010)"]
    CON --> DEC["MOD008 Decision Engine: Reads fused + confidence EV IDs ONLY -> Real / Fake / Inconclusive / Unknown"]
    DEC --> EXP["Stage 7: Generating Explanation - MOD010 (A.9 data-only) & MOD011 (EV-cited reasoning)"]
    EXP --> REP["Stage 8: Preparing Report - MOD012 (JSON, Markdown Template 24, HTML)"]
    REP --> AUD["MOD015 Case Audit Trail: Append immutable CASExxxxxx row"]
    AUD --> DONE["Stage 9: Complete (MOD014 UI Ready)"]
```

## Trust Boundaries (Who Reads Image Bytes vs. Who Decides)

- **Image bytes accessible:** `MOD001` (store), `MOD002` (validate), `MOD003`/`MOD004` collectors (per-collector isolation only).
- **Evidence IDs only (never image bytes):** `MOD005`–`MOD012`, `MOD015`.
- **Exclusive decision authority:** `MOD008` alone chooses `Real`, `Fake`, `Inconclusive`, or `Unknown` from validated `fused_conclusion` and `confidence` records.
- **Extensibility governance:** `MOD017` (module registry) & `MOD018` (new `EvidenceCollector` / `FusionStrategy` contract checks).
