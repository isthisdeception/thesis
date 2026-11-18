# Module Spec: MOD007

**Module ID:** MOD007  
**Name:** Evidence Fusion Engine  
**Version:** 0.1.0  
**Status:** implemented  
**Date:** 2026-11-18  
**Code:** `fusion/` (engine `fusion/engine.py`, contract `fusion/interface.py`, strategies `fusion/strategies/`)

**Purpose:** Turn the validated evidence of one case into one fused evidence item. The combination rule is a replaceable strategy. This module is not the Decision Engine.

**Inputs:** Evidence rows for the case whose status is `validated` or `failed`, including rows MOD006 marked `unusable`. Strategy id from configuration (`fusion/fusion_config.json`). No image bytes and no model weights. Raw Output keys that name a file location (`path`, `pointer`, `bytes`) are removed before the strategy sees an item.

**Outputs:** One new evidence item, Evidence Type `fused_conclusion`, Source Module MOD007, Confidence empty, passed through MOD005 for an `EV` id and through MOD006 for validation. Processed Output follows the `FusionStrategy` output in `interfaces.md`. The item does not contain Real, Fake, Inconclusive, or Unknown; the engine refuses any strategy output that does. Dependencies are the supporting ids plus every unresolved id that exists in the registry.

**Dependencies:** MOD006 for validated rows. MOD005 to register the fused item. The strategy named by configuration. MOD016 if that strategy is not registered, raises, or breaks the output contract.

**Configuration:** `strategy_id` in `fusion/fusion_config.json`; the value is `rule_based` (DEF-004). `weighted` and `bayesian` are reserved ids and are not registered. The `rule_based` table sits in the same file under `rule_based` and was approved in DEC0009 (Human, 2026-11-18): reliability weights (high 1.0, medium 0.6, low 0.3; `unusable` is never weighted), directional rules (`deep_learning_prediction`: probability ≥ recorded threshold → positive-class side), and the contested band (|balance| < 0.5 with both sides present).

**Engine checks (every strategy):**
- Ids not in the registry, collector rows not validated by MOD006, earlier `fused_conclusion` rows, and rows of another case are listed as unresolved with a reason, not passed to the strategy.
- Every id given to the strategy is either supporting or unresolved, never both, never dropped.
- Returned `strategy_id` equals the selected strategy.
- No decision word in the output.

**Rule-based summary fields:** `lean` (`positive_class`, `negative_class`, `contested`, `no_directional_evidence`), `positive_class`, `weights`, `balance`, `single_source`, `directional`, `context`, `conflicts` (`directional`, `flagged_by_validation`), `rule_table` (version, status), `rationale` (sentences citing `EV` ids). A lean is not a decision; MOD008 owns the mapping onto the four decision words.

**Testing:** `tests/test_fusion.py`. The same evidence list through two strategy ids yields two fused items whose `strategy_id` values differ, without a change to the engine or MOD008. An evidence list that gains a new Evidence Type still runs, and the new id appears in `supporting_ids` (as context). A request for `bayesian` writes a MOD016 failure and does not fall back to `rule_based`. Conflicting, missing, single-source, unusable, superseded, and threshold-less evidence each have a test. A strategy that raises, states a decision, or drops an id writes no fused item.

**Future Extensions:** Weighted fusion, Bayesian fusion, and ensemble fusion, each a new `FusionStrategy` added with `fusion.strategies.register_strategy`. Multimodal evidence is accepted because the input is a list of evidence items. A new directional evidence type is a new row in the rule table.

**Interfaces:** `FusionStrategy`. The module selects the strategy. It does not embed one strategy's rules in the decision module.

**Failure Handling:** Unknown `strategy_id`, a strategy that throws, or an output that breaks the engine checks calls MOD016 `unexpected_error`. No fused item is written in that case, and MOD008 does not run.
