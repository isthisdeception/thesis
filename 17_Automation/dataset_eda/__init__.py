"""STEP-023 / Phase D7 exploratory dataset analysis package.

Read-only EDA over raw dataset trees and ZIP archives.
Never modifies source files. Never renders publication figures (A.9).
"""

from .runner import run_eda

__all__ = ["run_eda"]
