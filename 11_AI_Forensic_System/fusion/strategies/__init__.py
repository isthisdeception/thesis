"""Fusion strategies by id. Only registered ids run; a reserved id is not a fallback."""

from __future__ import annotations

from typing import Callable

from fusion.interface import RESERVED_STRATEGY_IDS, FusionStrategy

from .rule_based import RuleBasedStrategy, RuleTable

_FACTORIES: dict[str, Callable[[dict], FusionStrategy]] = {
    "rule_based": lambda settings: RuleBasedStrategy(RuleTable.from_json(settings) if settings else None),
}


def register_strategy(strategy_id: str, factory: Callable[[dict], FusionStrategy]) -> None:
    """Add a strategy (MOD018). An existing id is not replaced."""

    if not strategy_id or strategy_id in _FACTORIES:
        raise ValueError(f"strategy id {strategy_id!r} is empty or already registered")
    _FACTORIES[strategy_id] = factory


def registered_ids() -> tuple[str, ...]:
    return tuple(_FACTORIES)


def build_strategy(strategy_id: str, settings: dict | None = None) -> FusionStrategy:
    factory = _FACTORIES.get(strategy_id)
    if factory is None:
        reserved = " (reserved, not implemented)" if strategy_id in RESERVED_STRATEGY_IDS else ""
        raise KeyError(f"fusion strategy {strategy_id!r} is not registered{reserved}")
    strategy = factory(settings or {})
    if strategy.strategy_id != strategy_id:
        raise ValueError(f"factory for {strategy_id!r} built {strategy.strategy_id!r}")
    return strategy


__all__ = ["RuleBasedStrategy", "RuleTable", "build_strategy", "register_strategy", "registered_ids"]
