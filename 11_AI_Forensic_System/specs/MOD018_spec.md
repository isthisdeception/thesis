# Module Spec: MOD018

**Module ID:** MOD018  
**Name:** Future Modality Support  
**Version:** 0.1.0  
**Status:** implemented  
**Date:** 2026-11-18  
**Code:** `system_registry/` (`system_registry/__init__.py`)

**Purpose:** State how a modality that does not exist yet is added. Audio, video, text, multimodal fusion, knowledge graphs, and an LLM reasoner are anticipated. None of them is built in this step.

**Inputs:** A proposal that names the new Evidence Type or the new `strategy_id`, the module that will own it, and which existing contract it implements.

**Outputs:** A registration note on the MOD003 collector list or the MOD007 strategy list, plus a spec change for that module. The pipeline in `architecture.md` stays the same. The decision module still reads evidence ids only.

**Dependencies:** `EvidenceCollector` for a new specialist. `FusionStrategy` when the combination rule changes. MOD011's rule that an LLM sentence must cite `EV` ids, if the extension is a reasoner. MOD017 to record the owning module.

**Configuration:** No audio, video, or text switch is turned on by this spec.

**Testing:** A paper registration of a new collector name is complete only when the name is on the MOD003 list, a spec says it does not call other collectors, and MOD008's inputs are unchanged. A new strategy id is complete only when it is listed beside `rule_based` and is not selected until DEF-004 is decided.

**Future Extensions:** Those modalities themselves, each in its own later step.

**Interfaces:** Uses `EvidenceCollector` and `FusionStrategy` as the only extension points for specialists and combination rules. Knowledge-graph links, when they exist, are evidence items with dependencies on other `EV` ids, not a side channel into the image.

**Failure Handling:** An extension that needs the Decision Engine to read the image or the file is rejected in review. MOD016 is not involved until an implementation exists.
