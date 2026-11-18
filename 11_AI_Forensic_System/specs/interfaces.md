# Shared interfaces (STEP-051)

**Date:** 2026-11-17  
**Status:** specified  
These are contracts. The evidence item and `EvidenceCollector` types are `evidence/item.py`. Collectors still do not assign `EV` ids. `FusionStrategy` is `fusion/interface.py` (STEP-056); the engine is `fusion/engine.py`.

## Evidence item

Module 5 assigns the id. The fields are the Evidence Registry columns. A collector may not invent an extra registry column.

| Field | Rule |
|---|---|
| Evidence ID | `EV` plus six digits, immutable, assigned only by MOD005 |
| Evidence Type | The collector name from the MOD003 list, or a name registered later under MOD018 |
| Source Module | `MODxxx` of the collector |
| Timestamp | ISO-8601, when the collector finished |
| Confidence | A number from 0 to 1, or empty. Empty means the collector did not estimate one. It is not filled with 0 or 1 |
| Description | One statement of what was observed |
| Raw Output | The collector payload, unchanged |
| Processed Output | The same observation in the normalized fields below, or empty when the collector has no normalized form |
| Quality | `unevaluated` until MOD006 sets `high`, `medium`, `low`, or `unusable` |
| Dependencies | Other `EV` ids this item needs, or empty. Collectors start with an empty dependency list |
| Owner | The module that wrote the row |
| Version | Schema version of this document: `0.1.0` |
| Status | `recorded`, then `validated` or `failed` |
| Created, Updated | ISO-8601 dates |

Normalized fields inside Processed Output, when the collector has them:

- `value` — the observation
- `unit` — empty when the value has no unit
- `model_id` — set only by the deep-learning collector and the explainability collector

The case does not add a column. MOD015 stores the evidence ids on the case row.

An input is not an evidence item. MOD001 stores `input_id` in `input_metadata.json` as `{case_id}-input-{seq}`. Collectors name that id inside Raw Output.

## EvidenceCollector

Every collector in Module 3 implements this contract. Collectors do not call each other.

**Input:** `input_id`, the validation status from MOD002, and a read of the stored file. The collector also receives the case id so the resulting evidence can be attached to the case.

**Output:** one or more evidence items with Evidence ID still empty. MOD005 assigns the ids. The collector sets Evidence Type, Source Module, Timestamp, Confidence, Description, Raw Output, and Processed Output. Quality is `unevaluated`. Status is `recorded`.

**Refusal:** if the collector cannot run, it returns a structured failure to MOD016 and no evidence item. It does not return a guessed observation.

**Independence:** the collector's result does not change because another collector succeeded or failed.

Initial collectors, each a separate implementation of this contract:

| Evidence Type | What it observes | Source |
|---|---|---|
| image_statistics | Width, height, channels, simple image statistics | MOD003 |
| metadata | File and image metadata that is present | MOD003 |
| face_detection | Whether a face is found, and how many | MOD003 |
| face_quality | Quality of the face region when the collector can measure it without calling face_detection | MOD003 |
| frequency_domain | A recorded frequency-domain measurement | MOD003 |
| compression_artifacts | A recorded compression measurement | MOD003 |
| color_distribution | A recorded color summary | MOD003 |
| texture_analysis | A recorded texture summary | MOD003 |
| deep_learning_prediction | Probability, optional embedding, timing, model id | MOD004 |
| explainability_input | Map data for one method, or a statement that the method produced none | MOD003 |

`deep_learning_prediction` includes the probability. It does not include Real, Fake, Inconclusive, or Unknown.

## FusionStrategy

Module 7 calls the strategy named by configuration. The strategy is replaceable. No strategy is hardcoded as the only implementation.

**Input:** the validated evidence items for one case. Each item has an `EV` id, a quality, and a status of `validated` or `failed`. `unusable` items are present and marked. The strategy does not receive image bytes.

**Output:** one fused evidence item, Evidence Type `fused_conclusion`, Source Module MOD007. Processed Output contains:

- `strategy_id` — `rule_based`, `weighted`, or `bayesian`
- `supporting_ids` — the `EV` ids the strategy used
- `summary` — a structured conclusion, not a case decision
- `unresolved` — ids the strategy could not use, with the reason

The fused item is not a decision. MOD008 reads it after MOD006 has validated it.

Each id the strategy receives must appear in `supporting_ids` or `unresolved`, never both. The engine adds ids it refused before the strategy ran (not in registry, not validated by MOD006, an earlier fused item, another case) to `unresolved`. A strategy output that breaks this rule, names a different `strategy_id`, or contains a decision word is refused and no fused item is written.

**Configured now:** `rule_based` (DEF-004), `fusion/fusion_config.json`. The rule table is not part of this contract; its approved values are in DEC0009.

**Reserved, not selected:** `weighted`, `bayesian`.

A new modality registers another `EvidenceCollector`. It becomes available to every strategy because strategies read the evidence list, not a fixed set of module classes.
