"""Root URL configuration for `forensic_backend`."""

from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path("", include("apps.api.urls")),
    path("api/v1/", include("apps.api.urls")),
]
