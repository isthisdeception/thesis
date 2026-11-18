"""Publication figure and table specs. Data only; no image is written."""

from __future__ import annotations

from pathlib import Path

FIGURES = {
    "FIG0021": """# Figure Spec: FIG0021

**Purpose:** ROC curves on the SPLIT0001 test split for the fairness-compatible runs.  
**Required data:** `fpr`, `tpr` where `split == test`, one curve per experiment.  
**Recommended chart type:** Line chart, one curve per experiment, plus the diagonal.  
**Exact axes:** X = false positive rate (0–1). Y = true positive rate (0–1). Equal aspect.  
**Legend:** EXP0001 baseline, EXP0003 seed, EXP0004 augmentation off, EXP0005 no pretraining, EXP0006 image size 160, chance.  
**Caption:** Test ROC curves for EXP0001 and the one-factor runs on the same split. Intervals and the decision to make no superiority claim are in the STEP-049 statistics report.  
**Color recommendations:** EXP0001 `#1F618D`; other runs `#117A65`, `#B9770E`, `#922B21`, `#5D6D7E`; diagonal `#566573` dashed.  
**Data source path:** `08_Evaluation/EXP0001/roc_curve.csv` and the same filename under `EXP0003` … `EXP0006`.  
**Responsible notebook:** `python -m evaluation_trigger` wrote the curves; this spec does not recompute them.  
**Manual creation instructions:** Filter `split == test`. Do not draw a marker for a winning model.  
**Expected output filename:** `09_Figures/assets/FIG0021_v1.png`
""",
    "FIG0022": """# Figure Spec: FIG0022

**Purpose:** Precision-recall curves on the SPLIT0001 test split for the same runs as FIG0021.  
**Required data:** `precision`, `recall` where `split == test`. The chance level is the fake share in that split.  
**Recommended chart type:** Line chart, one curve per experiment, plus a horizontal chance line.  
**Exact axes:** X = recall (0–1). Y = precision (0–1).  
**Legend:** Same experiments as FIG0021, plus the test fake share.  
**Caption:** Test precision-recall curves for EXP0001 and the one-factor runs. Chance is the fake share of the SPLIT0001 test split, not 0.5.  
**Color recommendations:** Same series colors as FIG0021. Chance line `#566573` dashed.  
**Data source path:** `08_Evaluation/EXP0001/pr_curve.csv` and the same filename under `EXP0003` … `EXP0006`.  
**Responsible notebook:** `python -m evaluation_trigger`.  
**Manual creation instructions:** Filter `split == test`. State the fake share in the caption.  
**Expected output filename:** `09_Figures/assets/FIG0022_v1.png`
""",
    "FIG0023": """# Figure Spec: FIG0023

**Purpose:** Metric comparison of the fairness-compatible runs, with the seed replicate visible as the run-to-run pair.  
**Required data:** `roc_auc`, `balanced_accuracy`, `mcc` from the ranked comparison table.  
**Recommended chart type:** Grouped dots, one panel per metric.  
**Exact axes:** Y = experiment (baseline, then seed replicate, then ablations). X = metric value. ROC-AUC and balanced accuracy on 0.5–1; MCC on 0–1.  
**Legend:** Baseline, seed replicate, ablation.  
**Caption:** SPLIT0001 test metrics for experiments that share DS0001 / v1.0 / PP0001 / SPLIT0001. No bar is marked as a winner. Statistical intervals are in `08_Evaluation/statistics/paired_tests.csv`.  
**Color recommendations:** Baseline `#1F618D`; seed `#117A65`; ablations `#922B21`.  
**Data source path:** `08_Evaluation/comparison_tables.csv`.  
**Responsible notebook:** `python -m comparison`.  
**Manual creation instructions:** Omit EXP0002. Do not plot accuracy alone.  
**Expected output filename:** `09_Figures/assets/FIG0023_v1.png`
""",
    "FIG0024": """# Figure Spec: FIG0024

**Purpose:** Validation ROC-AUC across the completed EXP0001 training session.  
**Required data:** `epoch` and `roc_auc_score` for the session listed in `metrics/run_summary.json`.  
**Recommended chart type:** Line chart. Mark the best epoch from `run_summary.json`.  
**Exact axes:** X = epoch (integer). Y = validation ROC-AUC (0.5–1).  
**Legend:** Validation ROC-AUC, best epoch.  
**Caption:** Validation ROC-AUC during the completed EXP0001 session. Earlier sessions in the same log file are abandoned runs and are not plotted.  
**Color recommendations:** Line `#1F618D`; best-epoch marker `#922B21`.  
**Data source path:** `06_Experiments/EXP0001/logs/EXP0001_epochs.csv`; session id from `06_Experiments/EXP0001/metrics/run_summary.json`.  
**Responsible notebook:** The EXP0001 training log. This spec does not refit the model.  
**Manual creation instructions:** Keep only `sessions[0]` from `run_summary.json`.  
**Expected output filename:** `09_Figures/assets/FIG0024_v1.png`
""",
    "FIG0025": """# Figure Spec: FIG0025

**Purpose:** Training and validation loss across the same completed EXP0001 session as FIG0024.  
**Required data:** `epoch`, `train_loss`, `valid_loss` for that session.  
**Recommended chart type:** Two lines on one set of axes.  
**Exact axes:** X = epoch (integer). Y = loss (the logged values, unscaled).  
**Legend:** Train loss, validation loss.  
**Caption:** Train and validation loss for the completed EXP0001 session. The best epoch is chosen by validation ROC-AUC, not by the lowest validation loss.  
**Color recommendations:** Train `#5D6D7E`; validation `#1F618D`.  
**Data source path:** `06_Experiments/EXP0001/logs/EXP0001_epochs.csv`; session id from `06_Experiments/EXP0001/metrics/run_summary.json`.  
**Responsible notebook:** The EXP0001 training log.  
**Manual creation instructions:** Same session filter as FIG0024. Do not add the abandoned sessions.  
**Expected output filename:** `09_Figures/assets/FIG0025_v1.png`
""",
}

TABLES = {
    "TAB0002": """# Table Spec: TAB0002

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
""",
    "TAB0003": """# Table Spec: TAB0003

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
""",
}

REQUIRED_EXISTING_FIGURES = {
    "calibration": "FIG0011",
    "confusion": "FIG0014",
    "threshold": "FIG0013",
    "robustness": "FIG0016",
    "ablation": "FIG0020",
}


def write_specs(repo: Path) -> list[Path]:
    written = []
    for figure_id, text in FIGURES.items():
        path = repo / "09_Figures/specs" / f"{figure_id}_spec.md"
        path.write_text(text, encoding="utf-8")
        written.append(path)
    for table_id, text in TABLES.items():
        path = repo / "10_Tables/specs" / f"{table_id}_spec.md"
        path.write_text(text, encoding="utf-8")
        written.append(path)
    return written
