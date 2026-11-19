"""Canonical URL routing table (`13_Backend/api_spec/api_spec.md` & `MOD013_spec.md`)."""

from __future__ import annotations

from django.urls import path

from .views import (
    CaseCreateView,
    CaseDecisionView,
    CaseDetailView,
    CaseEvidenceView,
    CaseExplanationView,
    CaseReportView,
    CaseStatusView,
    CaseUploadView,
    HealthView,
    VersionView,
)

urlpatterns = [
    path("cases", CaseCreateView.as_view(), name="case-create"),
    path("cases/<str:case_id>", CaseDetailView.as_view(), name="case-detail"),
    path("cases/<str:case_id>/upload", CaseUploadView.as_view(), name="case-upload"),
    path("cases/<str:case_id>/status", CaseStatusView.as_view(), name="case-status"),
    path("cases/<str:case_id>/evidence", CaseEvidenceView.as_view(), name="case-evidence"),
    path("cases/<str:case_id>/decision", CaseDecisionView.as_view(), name="case-decision"),
    path("cases/<str:case_id>/explanation", CaseExplanationView.as_view(), name="case-explanation"),
    path("cases/<str:case_id>/report", CaseReportView.as_view(), name="case-report"),
    path("health", HealthView.as_view(), name="health"),
    path("version", VersionView.as_view(), name="version"),
]
