"""Phase E6 confusion analysis and Phase E12 failure analysis (STEP-045)."""

from .analysis import (
    confusion_frame,
    error_cases_frame,
    error_summary_frame,
    group_frame,
    join_metadata,
    metadata_coverage,
    per_class_frame,
    wilson_interval,
)
from .report import render_report

__all__ = [
    "confusion_frame",
    "error_cases_frame",
    "error_summary_frame",
    "group_frame",
    "join_metadata",
    "metadata_coverage",
    "per_class_frame",
    "render_report",
    "wilson_interval",
]
