"""CSV schemas for STEP-023 / Phase D7 EDA reports."""

from __future__ import annotations

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}

CLASS_COLUMNS = ["Dataset ID", "Class", "Count", "Proportion", "Notes"]
GENERATOR_COLUMNS = [
    "Dataset ID",
    "Generator",
    "Class",
    "Condition",
    "Count",
    "Proportion",
    "Notes",
]
IDENTITY_COLUMNS = [
    "Dataset ID",
    "Metric",
    "Value",
    "Notes",
]
RESOLUTION_COLUMNS = [
    "Dataset ID",
    "Width",
    "Height",
    "Count",
    "Proportion",
    "Notes",
]
BRIGHTNESS_COLUMNS = [
    "Dataset ID",
    "Stratum",
    "N",
    "Mean",
    "Std",
    "P05",
    "P50",
    "P95",
    "Sample Policy",
    "Notes",
]
CONTRAST_COLUMNS = BRIGHTNESS_COLUMNS  # same shape; metric is pixel std
CHANNEL_COLUMNS = [
    "Dataset ID",
    "Mode",
    "Count",
    "Proportion",
    "Mean_R",
    "Mean_G",
    "Mean_B",
    "Sample Policy",
    "Notes",
]
COMPRESSION_COLUMNS = [
    "Dataset ID",
    "Format",
    "Count",
    "Mean Bytes",
    "Median Bytes",
    "P05 Bytes",
    "P95 Bytes",
    "Sample Policy",
    "Notes",
]
BALANCE_COLUMNS = ["Dataset ID", "Metric", "Value", "Notes"]
DEMOGRAPHIC_COLUMNS = [
    "Dataset ID",
    "Split",
    "Attribute",
    "Level",
    "Count",
    "Proportion",
    "Notes",
]
ERROR_COLUMNS = [
    "Dataset ID",
    "Relative Path",
    "Error Code",
    "Error Detail",
    "Source Container",
]

DEFAULT_PIXEL_SAMPLE = 3000
DEFAULT_RNG_SEED = 42
