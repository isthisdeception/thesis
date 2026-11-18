# reports/ — MOD012 Report Generator (STEP-059)

Generates reproducible forensic case reports in JSON (`{case_id}_report.json`), Markdown (`{case_id}_report.md`, following Template 24), and HTML (`{case_id}_report.html`) from recorded pipeline outputs (`decision.json`, `explanation.json`, `reasoning.json`, `input_metadata.json`, `validation.json`, and `evidence_registry.csv`).

- Embeds exact version provenance: `system_version`, `model_id`, `model_version`, `dataset_id`, `experiment_id`, and `git_commit`.
- Refuses to generate a report if `decision.json` is missing, any version stamp is blank, or any cited `EV` ID is not in `evidence_registry.csv`.
- Explicitly includes empty (`null`) confidence values in `Limitations`.

Tests: `python -m pytest tests/test_report_audit_pipeline.py` from `11_AI_Forensic_System/`.
