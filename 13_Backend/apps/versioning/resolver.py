"""Version provenance resolver (`GET /version`). Does not load a case or model weights (`MOD013_spec.md`)."""

from __future__ import annotations

from typing import Any

from apps.core.config import BackendConfig, ensure_forensic_sys_path

ensure_forensic_sys_path()
from confidence import load_confidence_config  # noqa: E402
from evidence.item import SCHEMA_VERSION, clock  # noqa: E402
from fusion import load_config as load_fusion_config  # noqa: E402
from reports import resolve_version_stamps  # noqa: E402

API_VERSION = "0.1.0"


def get_version_info(config: BackendConfig) -> dict[str, Any]:
    """Return full version provenance from `11_AI_Forensic_System` and `05_Models/model_registry.csv`."""

    stamps = resolve_version_stamps(
        config.model_id,
        system_version=SCHEMA_VERSION,
        repo_root=config.repo_root,
    )
    fusion_strategy_id, _ = load_fusion_config()
    conf_settings = load_confidence_config()
    return {
        "system_version": stamps.system_version,
        "api_version": API_VERSION,
        "model_id": stamps.model_id,
        "model_version": stamps.model_version,
        "dataset_id": stamps.dataset_id,
        "experiment_id": stamps.experiment_id,
        "git_commit": stamps.git_commit,
        "fusion_strategy_id": fusion_strategy_id,
        "confidence_formula_id": str(conf_settings.get("formula_id", "e4_calibrated_v1")),
        "timestamp": clock(),
    }
