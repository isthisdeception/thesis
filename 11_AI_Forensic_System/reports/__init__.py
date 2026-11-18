"""MOD012 report generator package."""

from .generator import (
    DEFAULT_FORMATS,
    MODULE_ID,
    CaseReport,
    ReportResult,
    VersionStamps,
    generate_report,
    resolve_git_commit,
    resolve_version_stamps,
)

__all__ = [
    "CaseReport",
    "DEFAULT_FORMATS",
    "MODULE_ID",
    "ReportResult",
    "VersionStamps",
    "generate_report",
    "resolve_git_commit",
    "resolve_version_stamps",
]
