"""CSV schemas and default acceptance thresholds for Phase D6."""

from __future__ import annotations

VALIDATION_COLUMNS = [
    "Dataset ID",
    "Relative Path",
    "Issue Code",
    "Issue Detail",
    "Severity",  # error | warning | info
    "Source Container",  # directory path or zip path
]

QUALITY_COLUMNS = [
    "Dataset ID",
    "Metric",
    "Value",
    "Notes",
]

INTEGRITY_COLUMNS = [
    "Dataset ID",
    "File Path",
    "File Size Bytes",
    "SHA256",
    "Integrity Status",
    "Raw Lock Status",
]

# Issue codes
CORRUPT_IMAGE = "CORRUPT_IMAGE"
UNSUPPORTED_FORMAT = "UNSUPPORTED_FORMAT"
INVALID_FILENAME = "INVALID_FILENAME"
MISSING_LABEL = "MISSING_LABEL"
MISSING_FILE_FOR_LABEL = "MISSING_FILE_FOR_LABEL"
DUPLICATE_HASH = "DUPLICATE_HASH"
EMPTY_FILE = "EMPTY_FILE"
UNEXPECTED_MODE = "UNEXPECTED_MODE"
ARCHIVE_UNREADABLE = "ARCHIVE_UNREADABLE"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}

DEFAULT_THRESHOLDS = {
    "max_corrupt_rate": 0.001,  # 0.1%
    "max_empty_files": 0,
    "max_missing_labels": 0,
    "max_missing_files_for_labels": 0,
}
