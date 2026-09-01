"""STEP-022 / Phase D6 dataset validation package.

Read-only scanners for raw dataset trees and ZIP archives.
Never modifies source files.
"""

from .runner import run_validation, DEFAULT_THRESHOLDS
from .adapters import debug_layout

__all__ = ["run_validation", "DEFAULT_THRESHOLDS", "debug_layout"]
