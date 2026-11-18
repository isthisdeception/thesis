"""Single-responsibility health app: verifies storage and registry accessibility without loading a case."""

from .checks import check_system_health

__all__ = ["check_system_health"]
