# Module Spec: MOD010

**Module ID:** MOD010  
**Name:** Explainability Engine  
**Version:** 0.1.0  
**Status:** specified  
**Date:** 2026-11-17

**Purpose:** Assemble `explanation.json` from explainability evidence that a collector actually recorded. The file carries data. It does not include a rendered image. This module does not draw a map the collector did not produce, and it does not decide the case.

**Inputs:** Validated evidence items of type `explainability_input` for the case. The method name on each item. No new read of the image in this module. Computing a map is the collector's work, done during MOD003, because that work needs the image and the model.

**Outputs:** `explanation.json`. For each method that has an evidence id: the id, the method name, and the map data from that item. For a configured method with no evidence id: an entry that says the method produced no data. Methods named in the handbook for this interface: Grad-CAM, attention maps, saliency, integrated gradients. SHAP, LIME, and counterfactuals are future method names, not current outputs.

**Dependencies:** The explainability collector under MOD003. MOD005 for ids. MOD006 so only validated items are quoted. MOD016 when the JSON cannot be written. The figure policy: no rendered publication figure.

**Configuration:** The list of method names the report may include. A name with no collector stays in the file as "no data".

**Testing:** When the collector recorded one Grad-CAM payload, the JSON contains that evidence id and no second map. When the collector recorded nothing, the JSON says no data and does not contain an array of highlighted pixels. The file contains no decision word as a conclusion of this module.

**Future Extensions:** SHAP, LIME, and counterfactual collectors, each a new `EvidenceCollector`, then a new method name in this list.

**Interfaces:** Reads evidence items. The collector that produces maps implements `EvidenceCollector`. This module does not implement `FusionStrategy`.

**Failure Handling:** A missing map is an explicit "no data" entry. A failure to write the file is MOD016 `unexpected_error`. Neither case is filled with a fabricated map.
