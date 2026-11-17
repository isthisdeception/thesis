# Table Spec: TAB0003

**Table ID:** TAB0003

**Title:** Paired ROC-AUC differences against EXP0001

**Source:** `08_Evaluation/statistics/paired_tests.csv`, rows with `metric == roc_auc`.

**Supporting experiment:** EXP0003, EXP0004, EXP0005, EXP0006, each paired with EXP0001 on the same 7505 test images.

**Purpose:** Show the primary-metric difference, its interval, and that no superiority claim is attached.

**Formatting:**
- One row per challenger.
- Intervals in brackets. The seed replicate uses the 95% interval. The three factor runs use the Bonferroni-adjusted interval.

**Consistency:**
- Challengers are exactly the ranked experiments other than the baseline.
- `superiority_claim` is `none`.
- The seed-level Wilcoxon test is not in this table; it was not run.

**Units:**
- Delta ROC-AUC: difference of two 0–1 scores. Negative means the challenger is lower on this split.

**Rendering notes:** Spec only. Do not add a significance star. The report already states when an interval excludes zero.
