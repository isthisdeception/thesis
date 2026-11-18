"""MOD016 failure records used by the forensic pipeline."""

from .report import (
    DEFAULT_WARNING_NAMES,
    FAILURE_NAMES,
    MODULE_ID,
    FailureRecord,
    classify_failures,
    read_case_failures,
    write_failure,
)

__all__ = [
    "DEFAULT_WARNING_NAMES",
    "FAILURE_NAMES",
    "FailureRecord",
    "MODULE_ID",
    "classify_failures",
    "read_case_failures",
    "write_failure",
]
