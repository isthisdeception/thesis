# Module Spec: MOD003

**Module ID:** MOD003  
**Name:** Evidence Acquisition Layer  
**Version:** 0.1.0  
**Status:** specified  
**Date:** 2026-11-17

**Purpose:** Run the registered collectors on one validated input. Each collector observes one kind of evidence. No collector depends on another collector's result.

**Inputs:** An input whose MOD002 status is `passed`. The collector list from configuration. Each collector also receives the stored file, and nothing that another collector returned.

**Outputs:** Evidence items with empty Evidence IDs, handed to MOD005. A collector that cannot run hands a failure to MOD016 and contributes no item. The other collectors still run.

**Dependencies:** MOD001 and MOD002 for the input. MOD005 to register items. MOD016 for a collector that cannot run. MOD004 is one collector behind the same interface, not a module this layer calls internally.

**Configuration:** The ordered list of Evidence Type names to run. Removing a name removes that collector. Adding a name requires an implementation of `EvidenceCollector` registered under MOD018. The initial list is `image_statistics`, `metadata`, `face_detection`, `face_quality`, `frequency_domain`, `compression_artifacts`, `color_distribution`, `texture_analysis`, `deep_learning_prediction`, `explainability_input`.

**Testing:** With two collectors configured, each output item stands alone: deleting one collector's result leaves the other item unchanged. A collector that fails does not prevent the other from recording an item. No item contains a case decision.

**Future Extensions:** Audio, video, text, and multimodal collectors, each added as a new `EvidenceCollector` without a change to this layer's control flow.

**Interfaces:** `EvidenceCollector`, defined in `interfaces.md`. This module does not implement `FusionStrategy`.

**Failure Handling:** A collector failure is that collector's MOD016 record. It is not a case decision and not a reason to invent the missing observation. If MOD002 did not pass, this module does not run.
