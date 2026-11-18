# decision/ — MOD008 Decision Engine (STEP-057)

Reads the MOD006-validated `fused_conclusion` (`MOD007`) and `confidence` (`MOD009`) rows by `EV` id, maps them onto `Real`, `Fake`, `Inconclusive`, or `Unknown`, and writes `decision.json`. Never reads the image, a file path, or model weights.

## Decision Rules (`decision_config.json`)

| Priority | Condition | Decision | Rule ID |
|---|---|---|---|
| 1 | Fused lean is `no_directional_evidence` (e.g., missing model) or `positive_class` is unmapped | `Unknown` | `no_directional_evidence_unknown` / `unmapped_positive_class_unknown` |
| 2 | Fused lean is `contested` or directional detectors conflict | `Inconclusive` | `contested_directional_evidence_inconclusive` |
| 3 | MOD006 flagged conflicting collector evidence (`inconclusive_on_validation_conflict=true`) | `Inconclusive` | `conflicting_evidence_inconclusive` |
| 4 | `decision_confidence` is `null` or `< min_decision_confidence` (`0.50`) | `Inconclusive` (+ MOD016 `low_confidence` warning) | `low_decision_confidence_inconclusive` |
| 5 | Fused lean is `positive_class` (`positive_class == "fake"`) | `Fake` | `validated_positive_lean_fake` |
| 6 | Fused lean is `negative_class` (`positive_class == "fake"`) | `Real` | `validated_negative_lean_real` |

## `decision.json` Schema

```json
{
  "case_id": "CASE000001",
  "decision": "Fake",
  "fused_evidence_id": "EV000008",
  "confidence_evidence_id": "EV000010",
  "reasoning_path": [
    "EV000004",
    "EV000005",
    "EV000006",
    "EV000008",
    "EV000010"
  ],
  "decision_metadata": {
    "module_id": "MOD008",
    "version": "0.1.0",
    "strategy_id": "rule_based",
    "rule_id": "validated_positive_lean_fake",
    "rule_version": "0.1.0",
    "rule_status": "approved in DEC0010 (Human, 2026-11-18)",
    "lean": "positive_class",
    "confidence": {
      "prediction_confidence": 0.971745,
      "evidence_confidence": 1.0,
      "system_confidence": 1.0,
      "decision_confidence": 0.985873
    },
    "reasoning_steps": [
      {
        "step": "supporting_evidence",
        "evidence_ids": ["EV000004", "EV000005", "EV000006"],
        "unresolved_evidence_ids": []
      },
      {
        "step": "evidence_fusion",
        "evidence_id": "EV000008",
        "collector_evidence_id": "EV000007",
        "strategy_id": "rule_based",
        "lean": "positive_class"
      },
      {
        "step": "confidence_estimation",
        "evidence_id": "EV000010",
        "collector_evidence_id": "EV000009",
        "formula_id": "e4_calibrated_v1"
      },
      {
        "step": "decision_rule",
        "evidence_ids": ["EV000008", "EV000010"],
        "rule_id": "validated_positive_lean_fake",
        "decision": "Fake"
      }
    ],
    "warning_failure_ids": [],
    "timestamp": "2026-11-18T10:12:00+06:00"
  }
}
```

Tests: `python -m pytest tests/test_decision_confidence.py` from `11_AI_Forensic_System/`.
