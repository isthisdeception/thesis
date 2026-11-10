"""Phase E3 classification metrics (STEP-043)."""

from .compute import (
    COLUMNS,
    METRIC_COLUMNS,
    METRIC_NOTES,
    classification_row,
    metrics_frame,
    note_key,
    render_report,
    require_validated,
    write_metrics,
)

__all__ = [
    "COLUMNS",
    "METRIC_COLUMNS",
    "METRIC_NOTES",
    "classification_row",
    "metrics_frame",
    "note_key",
    "render_report",
    "require_validated",
    "write_metrics",
]
