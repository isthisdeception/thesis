# fusion/ — MOD007 Evidence Fusion Engine (STEP-056)

The engine fuses MOD006-validated evidence rows for one case into one `fused_conclusion` evidence item. It does not decide the case.

```
validated EV ids ──► engine (fusion/engine.py)
                      ├─ refuses: unknown ids, unvalidated rows, earlier fused rows, other cases  → unresolved
                      ├─ strategy = build_strategy(strategy_id)   (fusion_config.json; no fallback)
                      ├─ strategy.fuse(ValidatedEvidence[])       (no image bytes, no file paths)
                      ├─ contract checks (traceability, no decision words)
                      └─ MOD005 register → MOD006 validate → fused_conclusion row
```

## Usage

```python
from fusion import fuse_case
result = fuse_case(registry_path, validated_ids, case_id="CASE000001", storage_root=storage)
result.fused        # MOD007 row with its EV id
result.validated    # MOD006 row for the fused item (quality reflects conflict / single source / no direction)
result.failures     # MOD016 records; non-empty means no fused item was written
```

## Adding a strategy

```python
from fusion import register_strategy, FusionOutput

class WeightedStrategy:
    strategy_id = "weighted"
    version = "0.1.0"
    def fuse(self, evidence):
        ...
        return FusionOutput(self.strategy_id, supporting_ids, summary, unresolved)

register_strategy("weighted", lambda settings: WeightedStrategy())
```

Then set `"strategy_id": "weighted"` in `fusion_config.json`. The engine, MOD006, and MOD008 do not change. Every id the strategy receives must come back in `supporting_ids` or `unresolved`.

## rule_based (DEF-004 baseline)

| Item | Treatment |
|---|---|
| `failed` / `unusable` | unresolved, reason `unusable:<validation_reason>`, weight 0 |
| Same collector validated twice | earlier validation row unresolved, `superseded_by:<EV>` |
| Type with a directional rule | probability ≥ recorded threshold → positive-class side, else negative-class side; weight from reliability |
| Directional item without a threshold or a 0–1 value | unresolved |
| Any other type (incl. future types) | context: supporting, cited, no vote |

Lean: no directional item → `no_directional_evidence`; both sides present and |balance| < `contested_balance_below` → `contested`; otherwise the side with more weight. Conflicts flagged by MOD006 are copied into `summary.conflicts.flagged_by_validation`.

The table values are in `fusion_config.json` and were approved in DEC0009 (Human, 2026-11-18).

Tests: `python -m pytest tests/test_fusion.py` from `11_AI_Forensic_System/`.
