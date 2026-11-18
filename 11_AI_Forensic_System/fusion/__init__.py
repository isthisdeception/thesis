"""MOD007 evidence fusion. The strategy is replaceable; this package does not decide the case."""

from fusion.engine import FusionResult, fuse_case, load_config
from fusion.interface import FusionOutput, FusionStrategy, Unresolved, ValidatedEvidence
from fusion.strategies import RuleBasedStrategy, RuleTable, build_strategy, register_strategy, registered_ids

__all__ = [
    "FusionOutput",
    "FusionResult",
    "FusionStrategy",
    "RuleBasedStrategy",
    "RuleTable",
    "Unresolved",
    "ValidatedEvidence",
    "build_strategy",
    "fuse_case",
    "load_config",
    "register_strategy",
    "registered_ids",
]
