"""Single-responsibility versioning app: resolves system, model, dataset, experiment, and Git versions."""

from .resolver import get_version_info

__all__ = ["get_version_info"]
