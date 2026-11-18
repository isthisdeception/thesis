# Table Spec: TAB0002

**Table ID:** TAB0002

**Title:** Fairness-compatible comparison on DS0001 / v1.0 / PP0001 / SPLIT0001

**Source:** `08_Evaluation/comparison_tables.csv`, built from `08_Evaluation/ablations/ablation_results.csv` and `08_Evaluation/statistics/paired_tests.csv`.

**Supporting experiment:** EXP0001, EXP0003, EXP0004, EXP0005, EXP0006. EXP0002 is excluded because it uses SPLIT0002.

**Purpose:** One table for the ranked comparison. Accuracy appears only beside ROC-AUC, PR-AUC, balanced accuracy, and MCC.

**Formatting:**
- One row per ranked experiment, baseline first.
- Numeric metrics to four decimal places.
- The ROC-AUC run-difference column uses the STEP-049 label, or a dash for the baseline.

**Consistency:**
- Every experiment id is in `experiment_registry.csv`.
- Dataset, version, pipeline, and split are identical on every ranked row.
- `superiority_claim` is `none` on every row.

**Units:**
- ROC-AUC, PR-AUC, balanced accuracy, F1, recall, specificity, FNR, FPR, accuracy, ECE, Brier: 0–1.
- MCC: −1–1.
- Threshold: probability of the fake class.

**Rendering notes:** Spec only. The data file is the comparison table itself. No rendered markdown table is required beyond `comparison_report.md`.
