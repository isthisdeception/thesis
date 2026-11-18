# Module Spec: MOD010

**Module ID:** MOD010  
**Name:** Explainability Engine  
**Version:** 0.1.0  
**Status:** implemented  
**Date:** 2026-11-18  
**Code:** `explainability/` (`explainability/engine.py`, `explainability/explainability_config.json`)

**Purpose:** Assemble `explanation.json` from explainability evidence that a collector actually recorded. The file carries data. It does not include a rendered image. This module does not draw a map the collector did not produce, and it does not decide the case.

**Inputs:** Validated evidence items of type `explainability_input` for the case. The method name on each item. No new read of the image in this module; any forbidden image or model argument (`image`, `image_path`, `image_bytes`, `stored_path`, `model`, `weights`) is refused via MOD016. Computing a map is the collector's work, done during MOD003, because that work needs the image and the model.

**Outputs:** `explanation.json` (`explainability/README.md`). For each method that has a validated evidence id with map data: `status: "recorded"`, `evidence_id`, `collector_evidence_id`, `quality`, `model_id`, and `data`. For a configured method with `"no_data"` or no evidence id: `status: "no_data"` and `data: null`. Configured methods: `grad_cam`, `attention_maps`, `saliency`, `integrated_gradients`. Reserved future methods: `shap`, `lime`, `counterfactuals`.

**Dependencies:** The explainability collector under MOD003. MOD005 for ids. MOD006 so only validated items are quoted. MOD016 when the JSON cannot be written or a payload violates A.9. The figure policy: no rendered publication figure.

**Configuration:** `explainability/explainability_config.json` (`configured_methods`, `reserved_future_methods`, `figure_policy`).

**Testing:** `tests/test_explainability_reasoning.py`. When the collector recorded one Grad-CAM payload, `explanation.json` contains that evidence id and no second map. When the collector recorded nothing, the JSON says `"no_data"` (`data: null`) and does not contain an array of highlighted pixels. Any rendered image data URI, base64 PNG/JPEG, or image file path is rejected via MOD016. The file contains no decision word.

**Future Extensions:** SHAP, LIME, and counterfactual collectors, each a new `EvidenceCollector`, then added to `configured_methods`.

**Interfaces:** Reads evidence items. The collector that produces maps implements `EvidenceCollector`. This module does not implement `FusionStrategy`.

**Failure Handling:** A missing map is an explicit `"no_data"` entry. A rendered-image payload or failure to write the file is MOD016 `unexpected_error`. Neither case is filled with a fabricated map.
