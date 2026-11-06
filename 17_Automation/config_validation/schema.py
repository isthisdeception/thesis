"""Phase M4 config.yaml schema constants."""

from __future__ import annotations

SCHEMA_VERSION = 1

# Top-level key -> Phase M4 section name (used in failure messages).
REQUIRED_SECTIONS: dict[str, str] = {
    "experiment_id": "Experiment ID",
    "dataset": "Dataset Version",
    "split": "Split Version",
    "model": "Model Version",
    "fastai": "FastAI Settings",
    "image_size": "Image Size",
    "batch_size": "Batch Size",
    "epochs": "Epochs",
    "optimizer": "Optimizer",
    "learning_rate": "Learning Rate",
    "loss_function": "Loss Function",
    "metrics": "Metrics",
    "random_seed": "Random Seed",
    "augmentations": "Augmentations",
    "hardware": "Hardware",
    "git_commit": "Git Commit",
    "timestamp": "Timestamp",
    "research_question": "Research Question",
    "purpose": "Purpose",
    "expected_outcome": "Expected Outcome",
    "outputs": "Output Folders / Checkpoint Location",
    "study_track": "Study Track",
}

REQUIRED_SUBKEYS: dict[str, tuple[str, ...]] = {
    "dataset": (
        "dataset_id",
        "version",
        "pipeline_id",
        "output_id",
        "processed_kaggle_slug",
        "processed_root",
        "path_column",
        "label_column",
        "partition_column",
        "vocab",
    ),
    "split": ("split_id", "scheme", "assignments_csv", "train_name", "valid_name", "test_name", "leakage_required"),
    "model": ("model_id", "architecture", "backbone", "source", "pretrained"),
    "fastai": (
        "datablock",
        "item_tfms",
        "normalize",
        "dataloaders",
        "mixed_precision",
        "lr_finder",
        "schedule",
        "callbacks",
        "export",
    ),
    "optimizer": ("name",),
    "learning_rate": ("value", "source"),
    "loss_function": ("name",),
    "metrics": (
        "primary",
        "monitor",
        "positive_class",
        "threshold_policy",
        "threshold_criterion",
        "calibration_bins",
    ),
    "augmentations": ("aug_transforms",),
    "hardware": ("platform", "accelerator", "gpu", "environment_lock"),
    "outputs": ("experiment_dir", "checkpoint_dir", "checkpoint_manifest"),
}

NON_EMPTY_TEXT = ("research_question", "purpose", "expected_outcome")

STUDY_TRACKS = frozenset(
    {"primary_architecture", "generator_holdout", "quick_convenience", "external_eval", "ablation"}
)
MODEL_SOURCES = frozenset({"torchvision", "timm"})
SCHEDULE_METHODS = frozenset({"fine_tune", "fit_one_cycle"})
LR_SOURCES = frozenset({"manual", "lr_find"})
THRESHOLD_POLICIES = frozenset({"validation_only"})
THRESHOLD_CRITERIA = frozenset({"max_balanced_accuracy", "max_f1", "fixed_0.5"})
SCHEDULE_NUMBERS = ("lr_mult", "pct_start", "div")

# 05_Models/baseline_plan.md canonical metric set.
CANONICAL_PRIMARY_METRICS = (
    "roc_auc",
    "pr_auc",
    "f1",
    "balanced_accuracy",
    "mcc",
    "precision",
    "recall",
    "specificity",
    "fpr",
    "fnr",
)

ID_PATTERNS = {
    "experiment": r"EXP\d{4}",
    "dataset": r"DS\d{4}",
    "pipeline": r"PP\d{4}",
    "split": r"SPLIT\d{4}",
    "model": r"MODEL\d{4}",
}
EXPERIMENT_PLACEHOLDER = "EXPxxxx"
GIT_COMMIT_PATTERN = r"[0-9a-f]{7,40}"

# Registry paths relative to the repo root.
REGISTRY_PATHS = {
    "dataset": "03_Datasets/metadata/dataset_registry.csv",
    "split": "03_Datasets/metadata/split_registry.csv",
    "preprocessing": "04_Preprocessing/preprocessing_registry.csv",
    "candidate_models": "05_Models/candidate_models.csv",
    "model": "05_Models/model_registry.csv",
}
