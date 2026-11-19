"""Django settings for `forensic_backend`, loaded from environment variables via `apps.core.config`."""

from __future__ import annotations

from pathlib import Path

from apps.core.config import load_backend_config
from apps.core.logging_config import build_logging_dict, get_channel_logger

BASE_DIR = Path(__file__).resolve().parent.parent
FORENSIC_CONFIG = load_backend_config()

SECRET_KEY = FORENSIC_CONFIG.secret_key
DEBUG = FORENSIC_CONFIG.debug
ALLOWED_HOSTS = list(FORENSIC_CONFIG.allowed_hosts)

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "apps.core",
    "apps.forensic_engine",
    "apps.evidence",
    "apps.reports",
    "apps.health",
    "apps.versioning",
    "apps.api",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "forensic_backend.urls"
WSGI_APPLICATION = "forensic_backend.wsgi.application"
ASGI_APPLICATION = "forensic_backend.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / "media" / "db.sqlite3"),
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = str(FORENSIC_CONFIG.media_root)

DATA_UPLOAD_MAX_MEMORY_SIZE = FORENSIC_CONFIG.max_upload_bytes
FILE_UPLOAD_MAX_MEMORY_SIZE = FORENSIC_CONFIG.max_upload_bytes

CORS_ALLOWED_ORIGINS = list(FORENSIC_CONFIG.cors_allowed_origins)
CSRF_TRUSTED_ORIGINS = list(FORENSIC_CONFIG.csrf_trusted_origins)
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FormParser",
    ],
    "EXCEPTION_HANDLER": "apps.core.exceptions.forensic_exception_handler",
    "URL_FORMAT_OVERRIDE": None,
    "DEFAULT_THROTTLE_RATES": {
        "upload": FORENSIC_CONFIG.throttle_upload,
        "anon": FORENSIC_CONFIG.throttle_anon,
    },
    "UNAUTHENTICATED_USER": None,
}

LOGGING = build_logging_dict(FORENSIC_CONFIG.log_dir)
get_channel_logger("application", FORENSIC_CONFIG.log_dir).info(
    "Forensic backend configured | env=%s | async_mode=%s | model_id=%s",
    FORENSIC_CONFIG.env,
    FORENSIC_CONFIG.async_mode,
    FORENSIC_CONFIG.model_id,
)
