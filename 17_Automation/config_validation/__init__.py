"""Phase M4 config.yaml validation (STEP-034)."""

from .registries import Registries, load_registries
from .validator import (
    ConfigValidationError,
    ValidationReport,
    find_repo_root,
    validate_config,
    validate_config_file,
)

__all__ = [
    "ConfigValidationError",
    "Registries",
    "ValidationReport",
    "find_repo_root",
    "load_registries",
    "validate_config",
    "validate_config_file",
]
