"""Config-driven FastAI training pipeline (Phase M6 / STEP-036).

FastAI is imported lazily, so settings, dataset validation, and metrics work
without a deep-learning stack installed.
"""

from .settings import TrainingConfigError, TrainingSettings, load_settings


def run_experiment(*args, **kwargs):
    from .pipeline import run_experiment as _run

    return _run(*args, **kwargs)


def find_lr(*args, **kwargs):
    from .pipeline import find_lr as _find

    return _find(*args, **kwargs)


run_experiment.__doc__ = "Run one experiment end to end from its config.yaml; see training.pipeline.run_experiment."
find_lr.__doc__ = "Run the LR Finder for a config.yaml; see training.pipeline.find_lr."

__all__ = ["TrainingConfigError", "TrainingSettings", "find_lr", "load_settings", "run_experiment"]
