"""Single-responsibility evidence app: read-only adapter over case evidence, decision, explanation, and reasoning."""

from .reader import read_case_decision, read_case_evidence, read_case_explanation

__all__ = ["read_case_decision", "read_case_evidence", "read_case_explanation"]
