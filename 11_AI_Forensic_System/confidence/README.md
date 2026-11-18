# confidence/ — MOD009 Confidence Estimation (STEP-057)

Computes four distinct confidence scores from MOD006-validated evidence rows, separating forensic certainty from raw detector softmax $P(\text{fake})$ using Phase E4 calibration (`08_Evaluation/EVAL0001/confidence_distribution.csv`, `split=val`).

## The Four Confidence Types

| Field | Range | Interpretation |
|---|---|---|
| `prediction_confidence` | `[0, 1]` or `null` | Empirical validation-set accuracy for the detector's predicted class at its recorded threshold (`E4 EVAL0001`, `split=val`), scaled by the detector item's MOD006 reliability weight (`high=1.0`, `medium=0.6`, `low=0.3`). Never raw $P(\text{fake})$. `null` when no usable detector item exists. |
| `evidence_confidence` | `[0, 1]` or `null` | Mean MOD006 reliability weight across the case's validated collector items (`high=1.0`, `medium=0.6`, `low=0.3`, `unusable=0.0`), multiplied by `0.5` when validation flags conflicting evidence. |
| `system_confidence` | `[0, 1]` or `null` | Fraction of usable validated collector items among all collector attempts, refused IDs, and prior MOD016 case failures. |
| `decision_confidence` | `[0, 1]` or `null` | Forensic certainty attached to the conclusion MOD008 will cite: weighted blend (`0.5 * prediction + 0.3 * evidence + 0.2 * system`), bounded by weak evidence/system health and discounted for single-source (`0.85`) or contested (`0.5`) leans. `null` when directional evidence is missing or the fused conclusion is unusable. |

## Usage

```python
from confidence import estimate_confidence

result = estimate_confidence(
    registry_path,
    [*validated_collector_ids, validated_fused_id],
    case_id="CASE000001",
    storage_root=storage_root,
)
result.confidence_item  # MOD009 row with its EV id
result.validated        # MOD006 row for the confidence item
```

Configuration lives in `confidence_config.json` (`formula_id: "e4_calibrated_v1"`, approved in `DEC0010` (Human, 2026-11-18)).

Tests: `python -m pytest tests/test_decision_confidence.py` from `11_AI_Forensic_System/`.
