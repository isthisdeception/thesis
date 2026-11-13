"""Phase E11 tests on paired predictions. Deterministic given the bootstrap seed.

Image-level intervals and McNemar describe these trained runs on one shared test split.
A seed-level Wilcoxon is a different test: it needs one metric per seed, and it is not run below MIN_WILCOXON_N.
"""

from __future__ import annotations

from math import exp, lgamma, log

import numpy as np

ALPHA = 0.05
N_BOOT_DEFAULT = 10_000
BOOT_SEED = 49
MIN_WILCOXON_N = 6
METRICS = ("roc_auc", "balanced_accuracy", "mcc")
PRIMARY_METRIC = "roc_auc"
HIGHER_IS_BETTER = {"roc_auc": True, "balanced_accuracy": True, "mcc": True}


def roc_auc(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """Mann-Whitney AUC with average ranks for ties. Matches sklearn on binary labels."""

    y = np.asarray(y_true).astype(bool)
    scores = np.asarray(y_score, dtype=float)
    n_pos = int(y.sum())
    n_neg = int(scores.size - n_pos)
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    order = np.argsort(scores, kind="mergesort")
    sorted_scores = scores[order]
    starts = np.flatnonzero(np.concatenate(([True], sorted_scores[1:] != sorted_scores[:-1])))
    counts = np.diff(np.append(starts, scores.size))
    ranks = np.empty(scores.size, dtype=float)
    ranks[order] = np.repeat(starts + (counts + 1) / 2.0, counts)
    return float((ranks[y].sum() - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg))


def confusion_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float]:
    """Balanced accuracy and MCC from saved decisions. Undefined when a class is absent."""

    y = np.asarray(y_true).astype(bool)
    pred = np.asarray(y_pred).astype(bool)
    tp = int(np.sum(pred & y))
    tn = int(np.sum(~pred & ~y))
    fp = int(np.sum(pred & ~y))
    fn = int(np.sum(~pred & y))
    if tp + fn == 0 or tn + fp == 0:
        return float("nan"), float("nan")
    balanced = 0.5 * (tp / (tp + fn) + tn / (tn + fp))
    denom = (tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)
    mcc = 0.0 if denom == 0 else (tp * tn - fp * fn) / np.sqrt(denom)
    return float(balanced), float(mcc)


def metric_value(name: str, y_true: np.ndarray, y_prob: np.ndarray, y_pred: np.ndarray) -> float:
    if name == "roc_auc":
        return roc_auc(y_true, y_prob)
    balanced, mcc = confusion_metrics(y_true, y_pred)
    if name == "balanced_accuracy":
        return balanced
    if name == "mcc":
        return mcc
    raise KeyError(name)


def _log_half_pmf(k: int, n: int) -> float:
    return lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1) - n * log(2)


def binom_test_two_sided(k: int, n: int) -> float:
    """Exact two-sided binomial test at p = 0.5. Sums outcomes whose probability is at most P(K=k)."""

    if n < 0 or not 0 <= k <= n:
        raise ValueError("k must lie inside 0..n")
    if n == 0:
        return 1.0
    logs = np.array([_log_half_pmf(i, n) for i in range(n + 1)])
    keep = logs <= logs[k] + 1e-12
    kept = logs[keep]
    peak = float(kept.max())
    return float(min(1.0, exp(peak) * np.exp(kept - peak).sum()))


def mcnemar(y_true: np.ndarray, pred_a: np.ndarray, pred_b: np.ndarray) -> dict:
    """Exact McNemar on paired decisions. b: A correct and B wrong. c: B correct and A wrong."""

    y = np.asarray(y_true).astype(bool)
    a = np.asarray(pred_a).astype(bool)
    b_hat = np.asarray(pred_b).astype(bool)
    if not (y.size == a.size == b_hat.size) or y.size == 0:
        raise ValueError("McNemar inputs must be non-empty and the same length")
    correct_a = a == y
    correct_b = b_hat == y
    b = int(np.sum(correct_a & ~correct_b))
    c = int(np.sum(~correct_a & correct_b))
    discordant = b + c
    return {
        "n": int(y.size),
        "n_agree": int(y.size - discordant),
        "b_a_only_correct": b,
        "c_b_only_correct": c,
        "accuracy_delta": (c - b) / y.size,
        "discordant_odds_ratio": float("nan") if b == 0 and c == 0 else (float("inf") if b == 0 else c / b),
        "p_exact": 1.0 if discordant == 0 else binom_test_two_sided(min(b, c), discordant),
    }


def wilcoxon_signed_rank(differences: np.ndarray) -> dict:
    """Two-sided exact signed-rank test. Not run below MIN_WILCOXON_N or when absolute ranks tie."""

    diffs = np.asarray(differences, dtype=float)
    diffs = diffs[np.isfinite(diffs) & (diffs != 0)]
    n = int(diffs.size)
    base = {"n": n, "statistic": float("nan"), "p_value": float("nan"), "minimum_n": MIN_WILCOXON_N}
    if n < MIN_WILCOXON_N:
        return {**base, "status": "not_run", "reason": f"need at least {MIN_WILCOXON_N} non-zero pairs; have {n}"}
    order = np.argsort(np.abs(diffs), kind="mergesort")
    ordered = np.abs(diffs)[order]
    if np.any(ordered[1:] == ordered[:-1]):
        return {**base, "status": "not_run", "reason": "exact signed-rank here requires no tied absolute differences"}
    ranks = np.empty(n, dtype=float)
    ranks[order] = np.arange(1, n + 1)
    observed = float(ranks[diffs > 0].sum())
    # Every sign pattern is equally likely. W+ is the sum of the positive ranks.
    total = 1 << n
    as_extreme = 0
    centre = n * (n + 1) / 4.0
    distance = abs(observed - centre)
    for mask in range(total):
        stat = float(ranks[np.array([(mask >> i) & 1 == 1 for i in range(n)])].sum())
        if abs(stat - centre) >= distance - 1e-9:
            as_extreme += 1
    return {
        **base,
        "statistic": observed,
        "p_value": as_extreme / total,
        "status": "computed",
        "reason": "exact two-sided signed-rank; zeros dropped; no ties",
    }


def _quantile_ci(samples: np.ndarray, level: float) -> tuple[float, float]:
    finite = samples[np.isfinite(samples)]
    if finite.size == 0:
        return float("nan"), float("nan")
    tail = (1.0 - level) / 2.0
    low, high = np.quantile(finite, [tail, 1.0 - tail], method="linear")
    return float(low), float(high)


def roc_auc_rows(y_true: np.ndarray, y_score: np.ndarray) -> np.ndarray:
    """Tie-aware AUC for many resamples at once. Each row is one resample."""

    y = np.asarray(y_true).astype(bool)
    scores = np.asarray(y_score, dtype=float)
    batch, n = scores.shape
    order = np.argsort(scores, axis=1, kind="mergesort")
    sorted_scores = np.take_along_axis(scores, order, axis=1)
    change = np.empty((batch, n), dtype=bool)
    change[:, 0] = True
    change[:, 1:] = sorted_scores[:, 1:] != sorted_scores[:, :-1]
    positions = np.arange(n)
    next_start = np.minimum.accumulate(np.where(change, positions, n)[:, ::-1], axis=1)[:, ::-1]
    following = np.concatenate([next_start[:, 1:], np.full((batch, 1), n)], axis=1)
    average = positions + (following - positions + 1) / 2.0
    group_start = np.maximum.accumulate(np.where(change, positions, 0), axis=1)
    ranks = np.take_along_axis(np.where(change, average, 0.0), group_start, axis=1)
    y_sorted = np.take_along_axis(y, order, axis=1)
    n_pos = y.sum(axis=1).astype(float)
    denom = n_pos * (n - n_pos)
    auc = np.full(batch, np.nan)
    ok = denom > 0
    auc[ok] = ((ranks * y_sorted).sum(axis=1)[ok] - n_pos[ok] * (n_pos[ok] + 1) / 2.0) / denom[ok]
    return auc


def confusion_rows(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    y = np.asarray(y_true).astype(bool)
    pred = np.asarray(y_pred).astype(bool)
    tp = np.sum(pred & y, axis=1).astype(float)
    tn = np.sum(~pred & ~y, axis=1).astype(float)
    fp = np.sum(pred & ~y, axis=1).astype(float)
    fn = np.sum(~pred & y, axis=1).astype(float)
    ok = (tp + fn > 0) & (tn + fp > 0)
    balanced = np.full(y.shape[0], np.nan)
    mcc = np.full(y.shape[0], np.nan)
    balanced[ok] = 0.5 * (tp[ok] / (tp[ok] + fn[ok]) + tn[ok] / (tn[ok] + fp[ok]))
    denom = (tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)
    good = ok & (denom > 0)
    mcc[good] = (tp[good] * tn[good] - fp[good] * fn[good]) / np.sqrt(denom[good])
    mcc[ok & (denom == 0)] = 0.0
    return balanced, mcc


def _resample_metrics(y, prob, pred, idx: np.ndarray) -> dict[str, np.ndarray]:
    balanced, mcc = confusion_rows(y[idx], pred[idx])
    return {"roc_auc": roc_auc_rows(y[idx], prob[idx]), "balanced_accuracy": balanced, "mcc": mcc}


def _fill(draws: dict[str, np.ndarray], start: int, batch: dict[str, np.ndarray]) -> None:
    stop = start + batch["roc_auc"].size
    for name in METRICS:
        draws[name][start:stop] = batch[name]


def bootstrap_intervals(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    y_pred: np.ndarray,
    *,
    n_boot: int,
    rng: np.random.Generator,
    levels: tuple[float, ...],
) -> dict[str, dict]:
    """Percentile intervals for each key metric. One resample serves every metric and every level."""

    y = np.asarray(y_true)
    prob = np.asarray(y_prob, dtype=float)
    pred = np.asarray(y_pred)
    n = y.size
    point = {name: metric_value(name, y, prob, pred) for name in METRICS}
    draws = {name: np.empty(n_boot) for name in METRICS}
    start = 0
    while start < n_boot:
        size = min(250, n_boot - start)
        idx = rng.integers(0, n, size=(size, n))
        _fill(draws, start, _resample_metrics(y, prob, pred, idx))
        start += size
    out = {}
    for name in METRICS:
        out[name] = {"estimate": point[name]}
        for level in levels:
            out[name][level] = _quantile_ci(draws[name], level)
    return out


def paired_bootstrap(
    y_true: np.ndarray,
    prob_a: np.ndarray,
    pred_a: np.ndarray,
    prob_b: np.ndarray,
    pred_b: np.ndarray,
    *,
    n_boot: int,
    rng: np.random.Generator,
    levels: tuple[float, ...],
) -> dict[str, dict]:
    """Percentile intervals for metric(B) - metric(A) on shared image resamples."""

    y = np.asarray(y_true)
    n = y.size
    point = {
        name: metric_value(name, y, prob_b, pred_b) - metric_value(name, y, prob_a, pred_a)
        for name in METRICS
    }
    draws = {name: np.empty(n_boot) for name in METRICS}
    start = 0
    while start < n_boot:
        size = min(250, n_boot - start)
        idx = rng.integers(0, n, size=(size, n))
        a = _resample_metrics(y, prob_a, pred_a, idx)
        b = _resample_metrics(y, prob_b, pred_b, idx)
        _fill(draws, start, {name: b[name] - a[name] for name in METRICS})
        start += size
    out = {}
    for name in METRICS:
        out[name] = {"delta": point[name]}
        for level in levels:
            out[name][level] = _quantile_ci(draws[name], level)
    return out


def run_difference(low: float, high: float) -> str:
    """Direction of B - A when the interval excludes 0. This is a difference of two runs, not a superiority claim."""

    if low > 0:
        return "challenger_higher"
    if high < 0:
        return "challenger_lower"
    return "not_supported"


def adjust_p(p: float, family: int) -> float:
    if family < 1:
        raise ValueError("family must be positive")
    return float(min(1.0, p * family))
