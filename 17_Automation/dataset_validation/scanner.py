"""Read-only image/archive scanning for Phase D6."""

from __future__ import annotations

import csv
import hashlib
import io
import re
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator

from .schemas import (
    CORRUPT_IMAGE,
    DUPLICATE_HASH,
    EMPTY_FILE,
    IMAGE_EXTENSIONS,
    INVALID_FILENAME,
    MISSING_FILE_FOR_LABEL,
    MISSING_LABEL,
    UNEXPECTED_MODE,
    UNSUPPORTED_FORMAT,
    ARCHIVE_UNREADABLE,
)

try:
    from PIL import Image

    HAS_PIL = True
except ImportError:  # pragma: no cover
    HAS_PIL = False


INVALID_NAME_RE = re.compile(r'[<>:"|?*\x00-\x1f]')


@dataclass
class Finding:
    dataset_id: str
    relative_path: str
    issue_code: str
    issue_detail: str
    severity: str
    source_container: str


@dataclass
class ImageStats:
    width: int
    height: int
    mode: str
    format: str
    sha256: str
    size_bytes: int


@dataclass
class ScanAccumulator:
    findings: list[Finding] = field(default_factory=list)
    widths: list[int] = field(default_factory=list)
    heights: list[int] = field(default_factory=list)
    aspects: list[float] = field(default_factory=list)
    modes: Counter = field(default_factory=Counter)
    formats: Counter = field(default_factory=Counter)
    hash_to_paths: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))
    scanned_images: int = 0
    corrupt: int = 0
    empty: int = 0
    unsupported: int = 0
    integrity_rows: list[dict] = field(default_factory=list)

    def add_stat(self, st: ImageStats, rel: str) -> None:
        self.scanned_images += 1
        self.widths.append(st.width)
        self.heights.append(st.height)
        if st.height:
            self.aspects.append(st.width / st.height)
        self.modes[st.mode] += 1
        self.formats[st.format or "unknown"] += 1
        self.hash_to_paths[st.sha256].append(rel)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_image_name(name: str) -> bool:
    return Path(name).suffix.lower() in IMAGE_EXTENSIONS


def _validate_filename(name: str) -> str | None:
    base = Path(name).name
    if not base or base in {".", ".."}:
        return "empty or dot filename"
    if INVALID_NAME_RE.search(base):
        return "illegal characters in filename"
    if base.startswith(" "):
        return "leading whitespace in filename"
    return None


def inspect_image_bytes(data: bytes) -> ImageStats | str:
    """Return ImageStats or error string."""
    if not data:
        return "empty file"
    if not HAS_PIL:
        # fallback: hash only, treat as unscannable visual
        return ImageStats(
            width=0,
            height=0,
            mode="unknown",
            format=Path("x").suffix,
            sha256=_sha256_bytes(data),
            size_bytes=len(data),
        )
    try:
        with Image.open(io.BytesIO(data)) as im:
            im.verify()
        with Image.open(io.BytesIO(data)) as im:  # reopen after verify
            width, height = im.size
            mode = im.mode
            fmt = im.format or "unknown"
            # load once to catch truncated payloads
            im.load()
        return ImageStats(
            width=width,
            height=height,
            mode=mode,
            format=fmt,
            sha256=_sha256_bytes(data),
            size_bytes=len(data),
        )
    except Exception as exc:  # noqa: BLE001 — must surface all decode failures
        return f"decode_error: {type(exc).__name__}: {exc}"


def iter_dir_images(root: Path) -> Iterator[tuple[str, Path]]:
    for path in sorted(root.rglob("*")):
        if path.is_file() and _is_image_name(path.name):
            yield path.relative_to(root).as_posix(), path


def iter_zip_images(
    zip_path: Path, *, _depth: int = 0, _max_depth: int = 3
) -> Iterator[tuple[str, bytes]]:
    """Yield (relative_name, bytes) for images; descends into nested zip entries."""
    if _depth > _max_depth:
        return
    with zipfile.ZipFile(zip_path, "r") as zf:
        for info in sorted(zf.infolist(), key=lambda i: i.filename):
            if info.is_dir():
                continue
            name = info.filename.replace("\\", "/")
            with zf.open(info, "r") as fh:
                data = fh.read()
            if name.lower().endswith(".zip"):
                try:
                    with zipfile.ZipFile(io.BytesIO(data), "r") as inner:
                        for i2 in sorted(inner.infolist(), key=lambda x: x.filename):
                            if i2.is_dir():
                                continue
                            n2 = i2.filename.replace("\\", "/")
                            if not _is_image_name(n2):
                                continue
                            with inner.open(i2, "r") as fh2:
                                yield f"{zip_path.name}::{name}::{n2}", fh2.read()
                except zipfile.BadZipFile:
                    continue
            elif _is_image_name(name):
                prefix = f"{zip_path.name}::" if _depth else ""
                yield f"{prefix}{name}", data


def scan_directory(
    dataset_id: str,
    root: Path,
    acc: ScanAccumulator,
    *,
    max_images: int | None = None,
    integrity_sample_every: int = 0,
) -> None:
    container = str(root)
    for rel, path in iter_dir_images(root):
        if max_images is not None and acc.scanned_images >= max_images:
            return
        bad = _validate_filename(rel)
        if bad:
            acc.findings.append(
                Finding(dataset_id, rel, INVALID_FILENAME, bad, "error", container)
            )
        try:
            size = path.stat().st_size
        except OSError as exc:
            acc.findings.append(
                Finding(
                    dataset_id,
                    rel,
                    CORRUPT_IMAGE,
                    f"stat_failed: {exc}",
                    "error",
                    container,
                )
            )
            acc.corrupt += 1
            continue
        if size == 0:
            acc.empty += 1
            acc.findings.append(
                Finding(dataset_id, rel, EMPTY_FILE, "zero-byte file", "error", container)
            )
            continue
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            acc.unsupported += 1
            acc.findings.append(
                Finding(
                    dataset_id,
                    rel,
                    UNSUPPORTED_FORMAT,
                    path.suffix,
                    "error",
                    container,
                )
            )
            continue
        try:
            data = path.read_bytes()
        except OSError as exc:
            acc.corrupt += 1
            acc.findings.append(
                Finding(
                    dataset_id,
                    rel,
                    CORRUPT_IMAGE,
                    f"read_failed: {exc}",
                    "error",
                    container,
                )
            )
            continue
        result = inspect_image_bytes(data)
        if isinstance(result, str):
            acc.corrupt += 1
            acc.findings.append(
                Finding(dataset_id, rel, CORRUPT_IMAGE, result, "error", container)
            )
            continue
        acc.add_stat(result, rel)
        if result.mode not in {"RGB", "L", "RGBA"}:
            acc.findings.append(
                Finding(
                    dataset_id,
                    rel,
                    UNEXPECTED_MODE,
                    result.mode,
                    "info",
                    container,
                )
            )
        if integrity_sample_every and acc.scanned_images % integrity_sample_every == 0:
            acc.integrity_rows.append(
                {
                    "Dataset ID": dataset_id,
                    "File Path": f"{container}/{rel}",
                    "File Size Bytes": result.size_bytes,
                    "SHA256": result.sha256,
                    "Integrity Status": "sample_ok",
                    "Raw Lock Status": "read_only_scan",
                }
            )


def scan_zip(
    dataset_id: str,
    zip_path: Path,
    acc: ScanAccumulator,
    *,
    max_images: int | None = None,
    integrity_sample_every: int = 0,
) -> None:
    container = str(zip_path)
    try:
        # probe
        with zipfile.ZipFile(zip_path, "r") as zf:
            _ = zf.namelist()
    except Exception as exc:  # noqa: BLE001
        acc.findings.append(
            Finding(
                dataset_id,
                zip_path.name,
                ARCHIVE_UNREADABLE,
                str(exc),
                "error",
                container,
            )
        )
        return

    count_before = acc.scanned_images
    for rel, data in iter_zip_images(zip_path):
        if max_images is not None and (acc.scanned_images - count_before) >= max_images:
            # max_images applies per call when scanning one zip in full pipeline
            # For zip we use absolute scanned_images vs limit from caller — use local
            pass
        if max_images is not None and acc.scanned_images >= max_images:
            return
        bad = _validate_filename(rel)
        if bad:
            acc.findings.append(
                Finding(dataset_id, rel, INVALID_FILENAME, bad, "error", container)
            )
        if len(data) == 0:
            acc.empty += 1
            acc.findings.append(
                Finding(dataset_id, rel, EMPTY_FILE, "zero-byte file", "error", container)
            )
            continue
        result = inspect_image_bytes(data)
        if isinstance(result, str):
            acc.corrupt += 1
            acc.findings.append(
                Finding(dataset_id, rel, CORRUPT_IMAGE, result, "error", container)
            )
            continue
        acc.add_stat(result, f"{zip_path.name}::{rel}")
        if result.mode not in {"RGB", "L", "RGBA"}:
            acc.findings.append(
                Finding(
                    dataset_id,
                    f"{zip_path.name}::{rel}",
                    UNEXPECTED_MODE,
                    result.mode,
                    "info",
                    container,
                )
            )
        if integrity_sample_every and acc.scanned_images % integrity_sample_every == 0:
            acc.integrity_rows.append(
                {
                    "Dataset ID": dataset_id,
                    "File Path": f"{container}::{rel}",
                    "File Size Bytes": result.size_bytes,
                    "SHA256": result.sha256,
                    "Integrity Status": "sample_ok",
                    "Raw Lock Status": "read_only_scan",
                }
            )


def finalize_duplicates(dataset_id: str, acc: ScanAccumulator) -> None:
    for digest, paths in acc.hash_to_paths.items():
        if len(paths) < 2:
            continue
        # keep first as canonical; flag others
        canonical, *dupes = paths
        for d in dupes:
            acc.findings.append(
                Finding(
                    dataset_id,
                    d,
                    DUPLICATE_HASH,
                    f"duplicate_of={canonical}; sha256={digest[:16]}...",
                    "warning",
                    "hash_index",
                )
            )


def check_label_csv(
    dataset_id: str,
    csv_path: Path,
    acc: ScanAccumulator,
    *,
    path_column_candidates: Iterable[str] = ("file", "output_path", "filename", "img_path"),
    available_relpaths: set[str] | None = None,
) -> None:
    """Validate label CSV rows; optionally check file presence against available_relpaths."""
    container = str(csv_path)
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            acc.findings.append(
                Finding(
                    dataset_id,
                    csv_path.name,
                    MISSING_LABEL,
                    "empty CSV header",
                    "error",
                    container,
                )
            )
            return
        cols = {c.lower(): c for c in reader.fieldnames}
        path_col = None
        for cand in path_column_candidates:
            if cand.lower() in cols:
                path_col = cols[cand.lower()]
                break
        if path_col is None:
            acc.findings.append(
                Finding(
                    dataset_id,
                    csv_path.name,
                    MISSING_LABEL,
                    f"no path column in {reader.fieldnames}",
                    "warning",
                    container,
                )
            )
            return
        for i, row in enumerate(reader, start=2):
            rel = (row.get(path_col) or "").strip().replace("\\", "/")
            if not rel:
                acc.findings.append(
                    Finding(
                        dataset_id,
                        f"{csv_path.name}:line{i}",
                        MISSING_LABEL,
                        f"empty {path_col}",
                        "error",
                        container,
                    )
                )
                continue
            if available_relpaths is not None:
                # FairFace uses train/1.jpg; Artifact metadata uses real/... or fake/...
                candidates = {rel, Path(rel).name}
                # also try without leading folder variants
                if not any(c in available_relpaths for c in candidates) and rel not in available_relpaths:
                    # soft check: suffix match
                    matched = any(p.endswith("/" + Path(rel).name) or p.endswith(rel) for p in available_relpaths)
                    if not matched:
                        acc.findings.append(
                            Finding(
                                dataset_id,
                                rel,
                                MISSING_FILE_FOR_LABEL,
                                f"label row has no matching image (csv={csv_path.name})",
                                "error",
                                container,
                            )
                        )
