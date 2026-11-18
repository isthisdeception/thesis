"""Single-responsibility reports app: read-only adapter over `{case_id}_report.{json,md,html}`."""

from .reader import ALLOWED_REPORT_FORMATS, read_case_report

__all__ = ["ALLOWED_REPORT_FORMATS", "read_case_report"]
