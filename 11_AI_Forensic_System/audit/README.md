# audit/ — MOD015 Case Audit Trail (STEP-059)

Appends one immutable row per investigation to `case_registry.csv` (`CASE000001`, ...). Never rewrites or deletes earlier case rows.

- Completed investigations record `Status: completed`, the exact `EV` IDs written for the case, the `Decision` word matching `decision.json`, `Model`, `Version`, `Configuration`, `Execution Time`, `Errors`, and `Warnings`.
- Failed investigations (stopped at `MOD001` or `MOD002`) still append a row with `Status: failed`, `Decision: ""`, and `Errors` set.

Tests: `python -m pytest tests/test_report_audit_pipeline.py` from `11_AI_Forensic_System/`.
