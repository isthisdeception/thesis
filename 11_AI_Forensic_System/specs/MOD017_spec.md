# Module Spec: MOD017

**Module ID:** MOD017  
**Name:** System Registry  
**Version:** 0.1.0  
**Status:** specified  
**Date:** 2026-11-17

**Purpose:** Hold the module registry that lists every forensic module, its responsibility, and its status. This file is the registry. Modules are not added by editing code alone.

**Inputs:** A module specification that already has Module ID, responsibilities, inputs, outputs, dependencies, version, status, owner, and future extensions.

**Outputs:** `module_registry.csv`, one row per module. The header is the canonical header already in that file. MOD001–MOD018 are the rows written for STEP-051, status `specified`, version `0.1.0`. A later implementation step changes Status. It does not reuse a module id.

**Dependencies:** The specs in this folder. No image and no model.

**Configuration:** The path `11_AI_Forensic_System/module_registry.csv`.

**Testing:** The registry has exactly one row for each of MOD001–MOD018. Every Module ID matches a `MODxxx_spec.md`. Status for this step is `specified`. The Decision Engine row's inputs do not name the image.

**Future Extensions:** A status change to `implemented` when that module's implementation step is done. New modules receive the next id and a new spec.

**Interfaces:** The registry lists modules. It does not implement `EvidenceCollector` or `FusionStrategy`. Those contracts are `interfaces.md`, and MOD003 and MOD007 are the modules that use them.

**Failure Handling:** A spec without a required section is not given a row. The missing section is the detail. There is no silent row with an empty responsibility.
