"""Image discovery helpers for STEP-027 (filesystem + zip members)."""

from __future__ import annotations

import zipfile
from pathlib import Path
from typing import Iterator

from modules.image_verification import is_macos_junk

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def iter_filesystem_images(root: Path) -> Iterator[tuple[Path, str]]:
    """Yield (absolute_path, relative_path) for image files under root."""
    root = Path(root)
    if not root.is_dir():
        return
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if is_macos_junk(rel):
            continue
        if path.suffix.lower() not in IMAGE_EXTS:
            continue
        yield path, rel


def iter_zip_images(zip_path: Path) -> Iterator[tuple[Path, str, bytes]]:
    """Yield (zip_path, member_rel, bytes) for image members (read-only)."""
    zip_path = Path(zip_path)
    with zipfile.ZipFile(zip_path, "r") as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = info.filename.replace("\\", "/")
            if is_macos_junk(name):
                continue
            if Path(name).suffix.lower() not in IMAGE_EXTS:
                continue
            yield zip_path, name, zf.read(info)


def discover_image_paths(
    raw_root: Path,
    *,
    max_images: int | None = None,
    include_zips: bool = True,
) -> list[tuple[Path, str]]:
    """Discover filesystem images; zip members are listed as virtual paths.

    Zip members are returned as (zip_path, 'zipname.zip::member') and must be
    handled by the runner via ``verify_image_bytes`` (not ``verify_path``).
    For simplicity, STEP-027 default expands zips into a temp read cache only
    when ``expand_zips=True`` in the Kaggle runner — here we only return
    filesystem files unless ``include_zips`` is used by the caller separately.
    """
    out: list[tuple[Path, str]] = []
    for path, rel in iter_filesystem_images(raw_root):
        out.append((path, rel))
        if max_images is not None and len(out) >= max_images:
            return out
    if include_zips:
        # Prefer scanning top-level and nested zips without extracting
        for zpath in Path(raw_root).rglob("*.zip"):
            # Skip huge accidental double-scans of nested temp zips if any
            try:
                with zipfile.ZipFile(zpath, "r") as zf:
                    for info in zf.infolist():
                        if info.is_dir():
                            continue
                        name = info.filename.replace("\\", "/")
                        if is_macos_junk(name):
                            continue
                        if Path(name).suffix.lower() not in IMAGE_EXTS:
                            continue
                        # Marker path: zip file itself + member encoded in rel
                        rel = f"{zpath.name}::{name}"
                        out.append((zpath, rel))
                        if max_images is not None and len(out) >= max_images:
                            return out
            except zipfile.BadZipFile:
                continue
    return out
