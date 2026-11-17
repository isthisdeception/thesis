# Module Spec: MOD011

**Module ID:** MOD011  
**Name:** Forensic Reasoning Engine  
**Version:** 0.1.0  
**Status:** specified  
**Date:** 2026-11-17

**Purpose:** Write the human-readable reasoning for one case from the evidence rows. Every sentence maps to one or more `EV` ids. The module does not add an observation that no row records.

**Inputs:** The validated evidence ids for the case, including the fused item and the confidence item when they exist. No image bytes.

**Outputs:** A reasoning record whose sentences each carry the evidence ids they use. The record is what MOD008 stores as the reasoning path and what MOD012 quotes. Example of an allowed sentence, only when those ids exist: the face_detection item records a face, the frequency_domain item records a measurement, and the deep_learning_prediction item records a probability. The sentence stops at what those rows contain.

**Dependencies:** MOD005 and MOD006. MOD007 and MOD009 when their items exist. MOD016 if the writer cannot tie a sentence to an id. No model.

**Configuration:** Language of the text. A maximum number of sentences. No template sentence may ship without an evidence-id slot.

**Testing:** A sentence whose cited id is removed from the input is rejected, and the record is not written with that sentence still in it. Wording that names a measurement absent from the cited row is rejected. The writer produces no sentence when it is given an empty evidence list; MOD008 then has an empty reasoning path and does not invent one.

**Future Extensions:** Another language. An LLM reasoner, under MOD018, only if its sentences still cite `EV` ids and it still cannot see the image.

**Interfaces:** Reads the evidence schema. It is not a collector and not a fusion strategy.

**Failure Handling:** An untied sentence is a MOD016 `unexpected_error` for the writer, and that sentence is discarded. The failure is not replaced with a fluent guess.
