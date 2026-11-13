"""statistics_report.md. Numbers come from the result frames. No superiority claim is written."""

from __future__ import annotations

import pandas as pd

from .core import ALPHA, PRIMARY_METRIC


def _f(value, digits: int = 4) -> str:
    if value is None or pd.isna(value):
        return "—"
    return f"{float(value):.{digits}f}"


def _s(value, digits: int = 4) -> str:
    if value is None or pd.isna(value):
        return "—"
    return f"{float(value):+.{digits}f}"


def _p(value) -> str:
    if value is None or pd.isna(value):
        return "—"
    number = float(value)
    if number == 0:
        return "<1e-16"
    return f"{number:.3g}"


def render_report(frames: dict[str, pd.DataFrame], date: str) -> str:
    paired = frames["paired_tests"]
    mcnemar = frames["mcnemar_tests"]
    seeds = frames["seed_variance"]
    repeat = frames["repeatability"].iloc[0]
    primary = paired[paired["metric"] == PRIMARY_METRIC]
    base = primary["baseline_id"].iloc[0]
    family = int(mcnemar.loc[mcnemar["role"] == "ablation", "family_size"].iloc[0])
    claim_level = float(primary.loc[primary["role"] == "ablation", "claim_ci_level"].iloc[0])
    lines = [
        "# Statistical Testing: STEP-049",
        "",
        f"**Baseline:** {base}  ",
        "**Phase:** E11  ",
        f"**Date:** {date}",
        "",
        f"Tests use the saved {primary['n'].iloc[0]} SPLIT0001 test predictions of {base} and the STEP-048 runs. "
        "Images are paired by id. Thresholded metrics use each run's own saved decisions. "
        f"Bootstrap intervals are percentiles of {int(primary['n_bootstrap'].iloc[0])} resamples "
        f"(seed {int(primary['bootstrap_seed'].iloc[0])}).",
        "",
        f"**What a result can support.** A {claim_level:.1%} interval for the primary metric ({PRIMARY_METRIC}) that excludes zero "
        f"supports a difference between those two trained runs, after a Bonferroni adjustment for the {family} factor comparisons "
        f"(family-wise alpha {ALPHA}). The seed replicate is reported at {(1 - ALPHA):.0%} and is not part of that family. "
        "None of these results is a superiority claim. Each configuration was trained once, so the tests do not separate a factor "
        "from run-to-run variation.",
        "",
        "## Primary metric, challenger minus baseline",
        "",
        "| Challenger | Factor | Delta ROC-AUC | 95% CI | Adjusted CI | Runs differ | Larger than the seed pair |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in primary.itertuples(index=False):
        lines.append(
            f"| {row.challenger_id} | {row.factor} | {_s(row.delta)} | "
            f"[{_s(row.ci_low)}, {_s(row.ci_high)}] | [{_s(row.claim_ci_low)}, {_s(row.claim_ci_high)}] | "
            f"{row.run_difference} | {row.larger_than_seed_pair} |"
        )
    lines += [
        "",
        "`Runs differ` uses the adjusted interval for a factor and the 95% interval for the seed replicate. "
        "`Larger than the seed pair` compares the absolute delta with |EXP0003 − EXP0001| on that metric. "
        "That comparison is one pair of runs, not a test.",
        "",
        "## Decisions (exact McNemar)",
        "",
        "b counts images the baseline got right and the challenger got wrong. c counts the reverse. "
        "A small adjusted p-value means the saved decisions disagree. It does not say which run is better.",
        "",
        "| Challenger | Factor | Agree | b | c | Accuracy delta | Odds c/b | p | Adjusted p | Decisions differ |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for row in mcnemar.itertuples(index=False):
        lines.append(
            f"| {row.challenger_id} | {row.factor} | {row.n_agree} | {row.b_baseline_only_correct} | "
            f"{row.c_challenger_only_correct} | {_s(row.accuracy_delta)} | {_f(row.discordant_odds_ratio, 3)} | "
            f"{_p(row.p_exact)} | {_p(row.p_adjusted)} | {row.decisions_differ} |"
        )
    lines += [
        "",
        "## Seed variance and repeatability",
        "",
        f"Decision agreement {repeat.decision_agreement:.4f}, Cohen's kappa {_f(repeat.cohen_kappa)}, "
        f"probability Pearson {_f(repeat.prob_pearson)}, mean absolute probability difference {_f(repeat.prob_mae)} "
        f"({repeat.experiment_a} vs {repeat.experiment_b}, n={int(repeat.n)}).",
        "",
        "| Metric | EXP0001 | EXP0003 | Mean | Absolute difference | Sample SD (n=2) | Wilcoxon |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in seeds.itertuples(index=False):
        lines.append(
            f"| {row.metric} | {_f(row.value_a)} | {_f(row.value_b)} | {_f(row.mean)} | "
            f"{_f(row.abs_diff)} | {_f(row.sample_sd)} | {row.wilcoxon_status} |"
        )
    lines += [
        "",
        f"Sample SD with two observations is the absolute difference divided by sqrt(2). "
        f"Wilcoxon signed-rank across seeds was not run: {seeds['wilcoxon_reason'].iloc[0]}",
        "",
        "## Other metrics",
        "",
        "Balanced accuracy and MCC are in `paired_tests.csv` and `bootstrap_cis.csv` with the same intervals. "
        "They are descriptive. The pre-specified primary metric is ROC-AUC, so they are not a second family of claims.",
        "",
        "## Limits",
        "",
        "- No superiority claim is made. `superiority_claim` is `none` on every row.",
        "- One seed per configuration. A factor-versus-seed test needs new experiment IDs, at least six seeds.",
        "- McNemar uses each run's own validation-chosen threshold, so decision differences mix ranking and operating point.",
        "- EXP0004 stopped at epoch 3. That early stop is part of the saved run being compared.",
        "- EXP0002 is a different split and is outside this comparison.",
        "- Intervals are percentile bootstrap intervals of these test images, not of a new population of images.",
        "",
    ]
    return "\n".join(lines)
