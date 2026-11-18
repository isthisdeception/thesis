from __future__ import annotations

from django.apps import AppConfig


class ForensicEngineConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.forensic_engine"
    verbose_name = "AI Forensic Analyst Engine Wrapper"
