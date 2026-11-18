# Module Spec: MOD011

**Module ID:** MOD011  
**Name:** Forensic Reasoning Engine  
**Version:** 0.1.0  
**Status:** implemented  
**Date:** 2026-11-18  
**Code:** `reasoning/` (`reasoning/engine.py`, `reasoning/reasoning_config.json`)

**Purpose:** Write the human-readable reasoning for one case from the evidence rows. Every sentence maps to one or more `EV` ids. The module does not add an observation that no row records.

**Inputs:** The validated evidence ids for the case, including the fused item and the confidence item when they exist. No image bytes; forbidden image or model arguments are refused via MOD016.

**Outputs:** `reasoning.json` (`reasoning/README.md`) and `ReasoningRecord`, whose sentences each carry `text`, `evidence_ids`, `evidence_types`, and `fields_used`, plus `reasoning_path` (ordered list of cited `EV` ids) and `narrative`. Each sentence stops at what the cited rows contain.

**Dependencies:** MOD005 and MOD006. MOD007 and MOD009 when their items exist. MOD016 if the writer cannot tie a sentence to an id or a sentence names an absent measurement. No model.

**Configuration:** `reasoning/reasoning_config.json` (`language: "en"`, `max_sentences: 12`, and `templates`). Every template is verified to contain an `{evidence_id}` slot before running.

**Testing:** `tests/test_explainability_reasoning.py`. A sentence whose cited id is removed from the input is rejected via MOD016, and `reasoning.json` is written without that sentence. Wording that names an evidence type or numeric measurement absent from the cited row is rejected via MOD016 and discarded. An empty evidence list produces no sentence (`sentences: []`, `reasoning_path: []`, `narrative: ""`).

**Future Extensions:** Another language. An LLM reasoner, under MOD018, only if its sentences pass `verify_sentence` (citing `EV` ids and matching row values) and it still cannot see the image.

**Interfaces:** Reads the evidence schema. It is not a collector and not a fusion strategy.

**Failure Handling:** An untied or ungrounded sentence is a MOD016 `unexpected_error` for the writer, and that sentence is discarded. The failure is not replaced with a fluent guess.
