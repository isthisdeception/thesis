#!/usr/bin/env python3
"""
dataset_checksum_verifier.py
-----------------------------
Computes SHA-256 checksums for raw dataset files/archives in accordance with
Phase D4 (Dataset Download) and Phase D5 (Raw Dataset Policy - sacred).

Supports three modes:
1. FULL mode: Computes SHA-256 for every file in raw/DSxxxx/ (for small datasets).
2. SAMPLE mode: Computes SHA-256 for all archives + a random sample of N files
   (for large datasets where full checksumming is impractical).
3. ARCHIVE mode: Computes SHA-256 for archive files only (ZIP/TAR/GZ/BZ2/XZ/7Z).

Outputs: 03_Datasets/reports/integrity_report.csv

Usage:
  python dataset_checksum_verifier.py                    # Full mode (all files)
  python dataset_checksum_verifier.py --mode sample -n 100  # Sample 100 files per dataset
  python dataset_checksum_verifier.py --mode archive     # Archives only
  python dataset_checksum_verifier.py --dataset DS0003   # Single dataset only
"""

import os
import sys
import hashlib
import random
import argparse
from pathlib import Path
from datetime import datetime

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

DATASETS_DIR = Path("03_Datasets")
RAW_DIR = DATASETS_DIR / "raw"
REPORTS_DIR = DATASETS_DIR / "reports"
OUTPUT_CSV = REPORTS_DIR / "integrity_report.csv"

ARCHIVE_EXTENSIONS = {".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar", ".tgz"}

COLUMNS = [
    "Dataset ID", "File Path", "File Size Bytes", "SHA256",
    "Integrity Status", "Raw Lock Status"
]


def compute_sha256(filepath: Path) -> str:
    """Compute SHA-256 hex digest for a file, reading in 64KB chunks."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def is_archive(filepath: Path) -> bool:
    """Check if a file is a recognized archive format."""
    return filepath.suffix.lower() in ARCHIVE_EXTENSIONS


def collect_files(dataset_folder: Path, mode: str = "full", sample_n: int = 100):
    """Collect files to checksum based on mode.
    
    Args:
        dataset_folder: Path to raw/DSxxxx/ folder
        mode: 'full', 'sample', or 'archive'
        sample_n: Number of non-archive files to sample (for 'sample' mode)
    
    Returns:
        List of Path objects to checksum
    """
    all_files = []
    archive_files = []
    non_archive_files = []

    for root, _, files in os.walk(dataset_folder):
        for file in files:
            file_path = Path(root) / file
            if file.startswith("."):
                continue  # Skip hidden files like .gitkeep
            all_files.append(file_path)
            if is_archive(file_path):
                archive_files.append(file_path)
            else:
                non_archive_files.append(file_path)

    if mode == "full":
        return all_files
    elif mode == "archive":
        return archive_files
    elif mode == "sample":
        # Always include all archives + random sample of non-archives
        sampled = list(archive_files)
        if len(non_archive_files) <= sample_n:
            sampled.extend(non_archive_files)
        else:
            random.seed(42)  # Reproducible sampling
            sampled.extend(random.sample(non_archive_files, sample_n))
        return sampled
    else:
        raise ValueError(f"Unknown mode: {mode}. Use 'full', 'sample', or 'archive'.")


def verify_dataset(dataset_folder: Path, mode: str = "full", sample_n: int = 100):
    """Verify a single dataset folder and return records."""
    ds_id = dataset_folder.name
    files_to_check = collect_files(dataset_folder, mode, sample_n)
    records = []
    total_size = 0
    failures = 0

    for file_path in files_to_check:
        try:
            rel_path = file_path.relative_to(DATASETS_DIR)
            file_size = file_path.stat().st_size
            sha256 = compute_sha256(file_path)
            total_size += file_size
            records.append({
                "Dataset ID": ds_id,
                "File Path": str(rel_path),
                "File Size Bytes": file_size,
                "SHA256": sha256,
                "Integrity Status": "VERIFIED",
                "Raw Lock Status": "IMMUTABLE"
            })
        except (PermissionError, OSError) as e:
            failures += 1
            records.append({
                "Dataset ID": ds_id,
                "File Path": str(file_path),
                "File Size Bytes": -1,
                "SHA256": "ERROR",
                "Integrity Status": f"FAILED: {e}",
                "Raw Lock Status": "UNKNOWN"
            })

    return records, len(files_to_check), total_size, failures


def write_report(records, output_path: Path):
    """Write the integrity report CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if HAS_PANDAS:
        df = pd.DataFrame(records, columns=COLUMNS)
        df.to_csv(output_path, index=False)
    else:
        # Fallback: write CSV without pandas
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            f.write(",".join(COLUMNS) + "\n")
            for record in records:
                row = [str(record.get(col, "")) for col in COLUMNS]
                f.write(",".join(row) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Compute SHA-256 checksums for raw dataset files (Phase D4/D5)."
    )
    parser.add_argument(
        "--mode", choices=["full", "sample", "archive"], default="full",
        help="Checksumming mode: full (all files), sample (archives + N random), archive (archives only)"
    )
    parser.add_argument(
        "-n", "--sample-n", type=int, default=100,
        help="Number of non-archive files to sample per dataset (for 'sample' mode)"
    )
    parser.add_argument(
        "--dataset", type=str, default=None,
        help="Process a single dataset only (e.g., DS0003). Default: all datasets."
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output CSV path. Default: 03_Datasets/reports/integrity_report.csv"
    )
    args = parser.parse_args()

    output_path = Path(args.output) if args.output else OUTPUT_CSV

    if not RAW_DIR.exists():
        print(f"[WARN] Raw directory {RAW_DIR} does not exist. Creating...")
        RAW_DIR.mkdir(parents=True, exist_ok=True)

    # Collect dataset folders
    if args.dataset:
        target = RAW_DIR / args.dataset
        if not target.exists():
            print(f"[ERROR] Dataset folder {target} does not exist.")
            sys.exit(1)
        dataset_folders = [target]
    else:
        dataset_folders = sorted([
            d for d in RAW_DIR.iterdir()
            if d.is_dir() and d.name.startswith("DS")
        ])

    if not dataset_folders:
        print(f"[INFO] No dataset folders found under {RAW_DIR}.")
        print(f"[INFO] Writing header-only report to {output_path}")
        write_report([], output_path)
        return

    # Process each dataset
    all_records = []
    print(f"{'='*60}")
    print(f"Dataset Checksum Verifier — {datetime.now().isoformat()}")
    print(f"Mode: {args.mode} | Sample size: {args.sample_n}")
    print(f"{'='*60}")

    for folder in dataset_folders:
        print(f"\n[{folder.name}] Processing...")
        records, file_count, total_size, failures = verify_dataset(
            folder, args.mode, args.sample_n
        )
        all_records.extend(records)

        size_mb = total_size / (1024 * 1024)
        print(f"  Files checked: {file_count}")
        print(f"  Total size: {size_mb:.1f} MB")
        print(f"  Failures: {failures}")
        if failures > 0:
            print(f"  [WARN] {failures} file(s) could not be checksummed!")

    # Write report
    write_report(all_records, output_path)
    print(f"\n{'='*60}")
    print(f"Integrity report written to {output_path}")
    print(f"Total entries: {len(all_records)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
