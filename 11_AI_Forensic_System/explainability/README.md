# explainability/ — MOD010 Explainability Engine (STEP-058)

Assembles `explanation.json` from MOD006-validated `explainability_input` evidence items. Complies with Canonical Figure Policy (A.9): **data only, no rendered images**, no image reads, no fabricated maps, and no decision words.

## Configured Methods (`explainability_config.json`)

- `grad_cam`
- `attention_maps`
- `saliency`
- `integrated_gradients`
- Reserved future methods: `shap`, `lime`, `counterfactuals`

When a collector recorded numeric map data for a method, its entry has `status: "recorded"`, `evidence_id`, `collector_evidence_id`, `quality`, `model_id`, and `data`. When a collector recorded `"no_data"` or did not run for a configured method, its entry has `status: "no_data"` and `data: null`.

## `explanation.json` Schema

```json
{
  "case_id": "CASE000001",
  "module_id": "MOD010",
  "version": "0.1.0",
  "figure_policy": "A.9_data_only_no_rendered_images",
  "methods": [
    {
      "method": "grad_cam",
      "status": "recorded",
      "evidence_id": "EV000002",
      "collector_evidence_id": "EV000001",
      "quality": "high",
      "model_id": "MODEL0001",
      "data": {
        "grid": [[0.1, 0.8], [0.3, 0.9]],
        "layer": "0.7.2",
        "shape": [2, 2]
      }
    },
    {
      "method": "attention_maps",
      "status": "no_data",
      "evidence_id": null,
      "collector_evidence_id": null,
      "quality": null,
      "model_id": null,
      "data": null
    }
  ],
  "supporting_ids": ["EV000002"],
  "unresolved": [],
  "timestamp": "2026-11-18T10:35:00+06:00"
}
```

Tests: `python -m pytest tests/test_explainability_reasoning.py` from `11_AI_Forensic_System/`.
