# Module Spec: MOD007

**Module ID:** MOD007  
**Name:** Evidence Fusion Engine  
**Version:** 0.1.0  
**Status:** specified  
**Date:** 2026-11-17

**Purpose:** Turn the validated evidence of one case into one fused evidence item. The combination rule is a replaceable strategy. This module is not the Decision Engine.

**Inputs:** Evidence rows for the case whose status is `validated` or `failed`, including rows MOD006 marked `unusable`. Strategy id from configuration. No image bytes and no model weights.

**Outputs:** One new evidence item, Evidence Type `fused_conclusion`, passed through MOD005 for an `EV` id and through MOD006 for validation. Processed Output follows the `FusionStrategy` output in `interfaces.md`. The item does not contain Real, Fake, Inconclusive, or Unknown as a case decision.

**Dependencies:** MOD006 for validated rows. MOD005 to register the fused item. The strategy named by configuration. MOD016 if that strategy is not registered.

**Configuration:** `strategy_id`. The value specified for the first system is `rule_based`. `weighted` and `bayesian` are legal ids and are not selected (DEF-004). The rule table for `rule_based` is not written in this spec.

**Testing:** The same evidence list through two strategy ids yields two fused items whose `strategy_id` values differ, without a change to MOD008. An evidence list that gains one new Evidence Type still runs, and the new id appears in `supporting_ids` or `unresolved`. A request for an unregistered strategy id does not fall back to `rule_based`.

**Future Extensions:** Weighted fusion, Bayesian fusion, and ensemble fusion, each a new `FusionStrategy`. Multimodal evidence is accepted because the input is a list of evidence items.

**Interfaces:** `FusionStrategy`. The module selects the strategy. It does not embed one strategy's rules in the decision module.

**Failure Handling:** Unknown `strategy_id`, or a strategy that throws, calls MOD016 `unexpected_error`. No fused item is written in that case, and MOD008 does not run.
