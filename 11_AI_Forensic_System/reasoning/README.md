# reasoning/ — MOD011 Forensic Reasoning Engine (STEP-058)

Composes and verifies human-readable forensic reasoning (`reasoning.json`) strictly from MOD006-validated evidence rows. Never reads the image and never invents an explanation.

## Grounding & Verification Rules (`verify_sentence`)

Every sentence in the reasoning record is verified before writing:
1. Must contain at least one `EVxxxxxx` ID in both `evidence_ids` and `text`, and every cited `EV` ID must exist in the validated input set for the case.
2. May not name any known `evidence_type` absent from the row(s) it cites.
3. Every entry in `fields_used` and every numeric measurement in `text` must match a recorded value on the cited row(s).
4. Any sentence failing verification triggers a `MOD016` `unexpected_error` failure and is discarded from `reasoning.json`.
5. When given an empty evidence list, `sentences` and `reasoning_path` are `[]` and `narrative` is `""`.

## `reasoning.json` Schema

```json
{
  "case_id": "CASE000001",
  "module_id": "MOD011",
  "version": "0.1.0",
  "language": "en",
  "max_sentences": 12,
  "sentences": [
    {
      "text": "Evidence EV000004 (face_detection, quality high) records value 1 count.",
      "evidence_ids": ["EV000004"],
      "evidence_types": ["face_detection"],
      "fields_used": {
        "EV000004": {
          "quality": "high",
          "value": 1
        }
      }
    }
  ],
  "reasoning_path": ["EV000004"],
  "narrative": "Evidence EV000004 (face_detection, quality high) records value 1 count.",
  "unresolved": [],
  "rejected_count": 0,
  "timestamp": "2026-11-18T10:35:00+06:00"
}
```

Tests: `python -m pytest tests/test_explainability_reasoning.py` from `11_AI_Forensic_System/`.
