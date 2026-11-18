"""Phase E11 statistical testing (STEP-049)."""

from .core import (
    ALPHA,
    BOOT_SEED,
    METRICS,
    MIN_WILCOXON_N,
    N_BOOT_DEFAULT,
    PRIMARY_METRIC,
    mcnemar,
    roc_auc,
    wilcoxon_signed_rank,
)

__all__ = [
    "ALPHA",
    "BOOT_SEED",
    "METRICS",
    "MIN_WILCOXON_N",
    "N_BOOT_DEFAULT",
    "PRIMARY_METRIC",
    "mcnemar",
    "roc_auc",
    "wilcoxon_signed_rank",
]
