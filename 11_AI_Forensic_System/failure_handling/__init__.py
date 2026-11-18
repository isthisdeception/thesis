"""MOD016 failure records used by the forensic pipeline."""

from .report import FAILURE_NAMES, FailureRecord, write_failure

__all__ = ["FAILURE_NAMES", "FailureRecord", "write_failure"]
