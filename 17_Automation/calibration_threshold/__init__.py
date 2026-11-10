"""Phase E4 calibration and Phase E5 threshold analysis (STEP-044)."""

from .calibration import calibration_frames, calibration_summary, confidence_rows, maximum_calibration_error, reliability_rows
from .report import render_report
from .threshold import OPERATING_POINTS, SWEEP, operating_frame, rate_threshold, select_operating_points, sweep_frame

__all__ = [
    "OPERATING_POINTS",
    "SWEEP",
    "calibration_frames",
    "calibration_summary",
    "confidence_rows",
    "maximum_calibration_error",
    "operating_frame",
    "rate_threshold",
    "reliability_rows",
    "render_report",
    "select_operating_points",
    "sweep_frame",
]
