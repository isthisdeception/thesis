"""DRF rate throttles (§8.8 right-sized security)."""

from __future__ import annotations

from rest_framework.throttling import AnonRateThrottle


class UploadRateThrottle(AnonRateThrottle):
    scope = "upload"


class ApiReadRateThrottle(AnonRateThrottle):
    scope = "anon"
