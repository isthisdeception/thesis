"""Environment-based configuration loader (`dev`, `test`, `prod`). Never hardcodes URLs or secrets."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = BACKEND_ROOT.parent
FORENSIC_SYSTEM_ROOT = REPO_ROOT / "11_AI_Forensic_System"
ALLOWED_ENVS = ("dev", "test", "prod")
ALLOWED_ASYNC_MODES = ("thread", "eager")
DEV_PLACEHOLDER_SECRET = "dev-insecure-placeholder-do-not-use-in-prod"


def ensure_forensic_sys_path() -> None:
    """Ensure `13_Backend` and `11_AI_Forensic_System` are importable without duplicating package files."""

    for entry in (str(BACKEND_ROOT), str(FORENSIC_SYSTEM_ROOT)):
        if entry not in sys.path:
            sys.path.insert(0, entry)


def _resolve_path(raw: str, default_rel: str) -> Path:
    val = (raw or "").strip() or default_rel
    candidate = Path(val)
    if candidate.is_absolute():
        return candidate
    return (REPO_ROOT / candidate).resolve()


def _csv_list(raw: str, default: tuple[str, ...]) -> tuple[str, ...]:
    parts = tuple(item.strip() for item in (raw or "").split(",") if item.strip())
    return parts if parts else default


@dataclass(frozen=True)
class BackendConfig:
    env: str
    secret_key: str
    debug: bool
    allowed_hosts: tuple[str, ...]
    cors_allowed_origins: tuple[str, ...]
    csrf_trusted_origins: tuple[str, ...]
    media_root: Path
    log_dir: Path
    evidence_registry_path: Path
    case_registry_path: Path
    model_id: str
    artifact_root: Path | None
    async_mode: str
    media_retention_days: int
    max_upload_bytes: int
    throttle_upload: str
    throttle_anon: str
    repo_root: Path = REPO_ROOT


def _load_dotenv_file(dotenv_path: Path) -> None:
    """Populate os.environ from a local `.env` file without overwriting explicit environment variables."""

    if not dotenv_path.is_file():
        return
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, val)


def load_backend_config(environ: dict[str, str] | None = None) -> BackendConfig:
    """Load and validate backend configuration from environment variables."""

    ensure_forensic_sys_path()
    if environ is None:
        _load_dotenv_file(BACKEND_ROOT / ".env")
    env_map = os.environ if environ is None else environ
    env = env_map.get("DJANGO_ENV", "dev").strip().lower()
    if env not in ALLOWED_ENVS:
        raise ValueError(f"DJANGO_ENV must be one of {ALLOWED_ENVS}, got {env!r}")

    raw_secret = env_map.get("DJANGO_SECRET_KEY", "").strip()
    if env == "prod" and (not raw_secret or "replace-with" in raw_secret or raw_secret == DEV_PLACEHOLDER_SECRET):
        raise ValueError("DJANGO_SECRET_KEY must be set to a real secret in prod environment")
    secret_key = raw_secret or DEV_PLACEHOLDER_SECRET

    raw_debug = env_map.get("DJANGO_DEBUG", "").strip().lower()
    if env == "prod":
        debug = False
    elif raw_debug in ("true", "1", "yes"):
        debug = True
    elif raw_debug in ("false", "0", "no"):
        debug = False
    else:
        debug = env == "dev"

    allowed_hosts = _csv_list(env_map.get("DJANGO_ALLOWED_HOSTS", ""), ("127.0.0.1", "localhost", "testserver"))
    cors_origins = _csv_list(
        env_map.get("CORS_ALLOWED_ORIGINS", ""),
        ("http://localhost:5173", "http://127.0.0.1:5173"),
    )
    csrf_origins = _csv_list(
        env_map.get("CSRF_TRUSTED_ORIGINS", ""),
        ("http://localhost:5173", "http://127.0.0.1:5173"),
    )

    media_root = _resolve_path(env_map.get("FORENSIC_MEDIA_ROOT", ""), "13_Backend/media/cases")
    log_dir = _resolve_path(env_map.get("FORENSIC_LOG_DIR", ""), "13_Backend/media/logs")
    ev_reg = _resolve_path(
        env_map.get("FORENSIC_EVIDENCE_REGISTRY", ""),
        "11_AI_Forensic_System/evidence_registry.csv",
    )
    case_reg = _resolve_path(
        env_map.get("FORENSIC_CASE_REGISTRY", ""),
        "11_AI_Forensic_System/case_registry.csv",
    )
    model_id = env_map.get("FORENSIC_MODEL_ID", "MODEL0001").strip() or "MODEL0001"
    raw_artifact = env_map.get("FORENSIC_ARTIFACT_ROOT", "").strip()
    artifact_root = _resolve_path(raw_artifact, raw_artifact) if raw_artifact else None

    async_mode = env_map.get("FORENSIC_ASYNC_MODE", "thread").strip().lower()
    if async_mode not in ALLOWED_ASYNC_MODES:
        raise ValueError(f"FORENSIC_ASYNC_MODE must be one of {ALLOWED_ASYNC_MODES}, got {async_mode!r}")

    retention_days = int(env_map.get("FORENSIC_MEDIA_RETENTION_DAYS", "30"))
    max_upload_bytes = int(env_map.get("FORENSIC_MAX_UPLOAD_BYTES", str(20 * 1024 * 1024)))
    throttle_upload = env_map.get("FORENSIC_THROTTLE_UPLOAD", "30/min").strip() or "30/min"
    throttle_anon = env_map.get("FORENSIC_THROTTLE_ANON", "240/min").strip() or "240/min"

    media_root.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    return BackendConfig(
        env=env,
        secret_key=secret_key,
        debug=debug,
        allowed_hosts=allowed_hosts,
        cors_allowed_origins=cors_origins,
        csrf_trusted_origins=csrf_origins,
        media_root=media_root,
        log_dir=log_dir,
        evidence_registry_path=ev_reg,
        case_registry_path=case_reg,
        model_id=model_id,
        artifact_root=artifact_root,
        async_mode=async_mode,
        media_retention_days=retention_days,
        max_upload_bytes=max_upload_bytes,
        throttle_upload=throttle_upload,
        throttle_anon=throttle_anon,
    )
