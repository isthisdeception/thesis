# Module Spec: MOD004

**Module ID:** MOD004  
**Name:** Deep Learning Specialist  
**Version:** 0.1.0  
**Status:** implemented  
**Date:** 2026-11-17  
**Code:** `evidence/collectors/deep_learning_specialist/`

**Purpose:** Load one registered detector and run inference. The output is a probability and the metadata of that run. This module never decides Real, Fake, Inconclusive, or Unknown.

**Inputs:** `input_id` and the stored image, as an `EvidenceCollector`. The model id from configuration. The model registry row for that id supplies the export path. The current registered baseline is MODEL0001. Configuration can name a different registered model later (DEF-002). This module does not train.

**Outputs:** One evidence item, Evidence Type `deep_learning_prediction`. Processed Output carries `model_id`, the probability of the fake class, the threshold recorded for that model if the registry has one, optional embedding, prediction metadata, and execution time. Confidence on the evidence item is empty unless the model export itself provides a separate confidence field. The fake-class probability is not copied into that confidence field. Softmax is not forensic certainty; MOD009 is the module that may say so.

**Dependencies:** The model registry. MOD003 only as the layer that schedules this collector. MOD005 to receive the item. MOD016 if the export cannot be loaded.

**Configuration:** `model_id`. Device. Batch size of one for a case. No threshold in this module is allowed to become a label.

**Testing:** A known input returns a probability inside 0–1, the configured model id, and an execution time. The item's description and processed output contain none of the four decision words as a conclusion. Swapping `model_id` to another registered export changes `model_id` on the item and does not require a change to MOD008. A missing export yields `model_unavailable` and no probability.

**Future Extensions:** Another image detector behind the same collector. Embeddings stay optional.

**Interfaces:** `EvidenceCollector`. It does not implement `FusionStrategy` and it does not write `decision.json`.

**Failure Handling:** Missing export, failed load, and inference timeout call MOD016 (`model_unavailable` or `timeout`). No substitute probability is written.
