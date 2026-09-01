"""Infer class / generator / identity / demographics from paths and label CSVs."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
ID_FOLDER_RE = re.compile(r"(id[_-]?\d+)", re.IGNORECASE)
CELEB_RE = re.compile(r"celebahq_img(\d+)", re.IGNORECASE)
FFHQ_RE = re.compile(r"ffhq_img(\d+)", re.IGNORECASE)
DS0002_CONDS = ("FE", "FS", "I2I", "T2I")


@dataclass(frozen=True)
class ImageRecord:
    dataset_id: str
    relative_path: str
    source_container: str
    class_label: str
    generator: str
    condition: str
    identity: str  # "" if unavailable
    size_bytes: int = 0


def is_image_path(path: str) -> bool:
    p = _norm(path)
    name = Path(p).name
    # Skip macOS resource forks / AppleDouble and __MACOSX junk often present in zips
    if name.startswith("._") or name in {".DS_Store", "Thumbs.db"}:
        return False
    if "/__macosx/" in f"/{p.lower()}/" or p.lower().startswith("__macosx/"):
        return False
    return Path(p).suffix.lower() in IMAGE_EXTS


def _norm(p: str) -> str:
    return p.replace("\\", "/")


def load_ds0001_metadata(csv_paths: Iterable[Path]) -> dict[str, dict[str, str]]:
    """Map basename / output_path -> metadata fields."""
    out: dict[str, dict[str, str]] = {}
    for csv_path in csv_paths:
        if not csv_path.is_file():
            continue
        with csv_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                filename = (row.get("filename") or "").strip()
                output_path = _norm(row.get("output_path") or "")
                meta = {
                    "label": (row.get("label") or "").strip().lower() or "unknown",
                    "generator": (row.get("generator") or "none").strip() or "none",
                    "original_source": (row.get("original_source") or "").strip(),
                    "original_path": _norm(row.get("original_path") or ""),
                }
                if filename:
                    out[filename] = meta
                    out[_norm(f"real/{filename}")] = meta
                    out[_norm(f"fake/{filename}")] = meta
                if output_path:
                    out[output_path] = meta
                    out[output_path.split("/")[-1]] = meta
    return out


def load_fairface_labels(csv_paths: Iterable[Path]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for csv_path in csv_paths:
        if not csv_path.is_file():
            continue
        with csv_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = _norm((row.get("file") or "").strip())
                if not key:
                    continue
                out[key] = {
                    "age": (row.get("age") or "").strip(),
                    "gender": (row.get("gender") or "").strip(),
                    "race": (row.get("race") or "").strip(),
                    "split": key.split("/", 1)[0] if "/" in key else "",
                }
                out[Path(key).name] = out[key]
    return out


def infer_identity(dataset_id: str, rel: str, meta: dict[str, str] | None = None) -> str:
    rel_n = _norm(rel)
    name = Path(rel_n).name
    if dataset_id == "DS0002":
        m = ID_FOLDER_RE.search(rel_n)
        return m.group(1).lower() if m else ""
    if dataset_id == "DS0001":
        m = CELEB_RE.search(name) or FFHQ_RE.search(name)
        if m:
            src = (meta or {}).get("original_source") or "src"
            return f"{src}_{m.group(1)}"
        op = (meta or {}).get("original_path") or ""
        if op:
            stem = Path(op).stem
            if stem:
                return f"{(meta or {}).get('original_source', 'src')}_{stem}"
        return ""
    if dataset_id == "DS0004":
        # RAISE / synth stems are unique image ids (not person ids); still useful for leakage checks
        return Path(name).stem
    return ""


def infer_ds0002_attrs(rel: str, container: str) -> tuple[str, str, str]:
    """Return (class, generator, condition)."""
    rel_n = _norm(rel)
    cont = _norm(container)
    joined = f"{cont}/{rel_n}"
    condition = ""
    for cond in DS0002_CONDS:
        if f"/{cond}/" in f"/{joined}/" or f"/{cond}/" in f"/{rel_n}/":
            condition = cond
            break
    generator = ""
    # Prefer zip stem (CoDiff.zip -> CoDiff)
    cpath = Path(container)
    if cpath.suffix.lower() == ".zip":
        generator = cpath.stem
    if not generator:
        parts = [p for p in rel_n.split("/") if p and p not in DS0002_CONDS]
        if parts:
            # DCFace/id_xxx/img -> DCFace
            generator = parts[0]
    return "fake", generator or "unknown", condition


def infer_ds0003_attrs(rel: str) -> tuple[str, str, str]:
    rel_n = _norm(rel).lower()
    parts = rel_n.split("/")
    label = "unknown"
    if "real" in parts:
        label = "real"
    elif "fake" in parts:
        label = "fake"
    generator = "none" if label == "real" else "stylegan"
    split = ""
    for s in ("train", "valid", "validation", "test"):
        if s in parts:
            split = s
            break
    return label, generator, split


def infer_ds0004_attrs(rel: str, container: str) -> tuple[str, str]:
    rel_n = _norm(rel)
    cont = _norm(container)
    joined = f"{cont}/{rel_n}".lower()
    if "raise" in joined or "/real/" in joined or Path(container).name.lower().startswith("raise"):
        return "real", "raise_1k_jpeg"
    # synthbuster/<generator>/file
    parts = [p for p in rel_n.split("/") if p and p.lower() != "synthbuster"]
    if parts:
        return "fake", parts[0]
    # zip under synthetic/
    if "synth" in joined:
        return "fake", Path(container).stem if Path(container).suffix.lower() == ".zip" else "synthetic"
    return "unknown", "unknown"


def record_from_path(
    dataset_id: str,
    rel: str,
    container: str,
    size_bytes: int = 0,
    ds0001_meta: dict[str, dict[str, str]] | None = None,
) -> ImageRecord | None:
    if not is_image_path(rel):
        return None
    rel_n = _norm(rel)
    class_label = "unknown"
    generator = "unknown"
    condition = ""
    meta: dict[str, str] | None = None

    if dataset_id == "DS0001":
        meta = None
        if ds0001_meta:
            base = Path(rel_n).name
            # try several keys
            for key in (
                base,
                rel_n,
                rel_n.split("raw/DS0001/", 1)[-1],
                "/".join(rel_n.split("/")[-2:]),
            ):
                if key in ds0001_meta:
                    meta = ds0001_meta[key]
                    break
        if meta:
            class_label = meta.get("label") or "unknown"
            generator = meta.get("generator") or ("none" if class_label == "real" else "unknown")
        else:
            low = rel_n.lower()
            if "/real/" in f"/{low}/":
                class_label, generator = "real", "none"
            elif "/fake/" in f"/{low}/":
                class_label, generator = "fake", "unknown"
        identity = infer_identity(dataset_id, rel_n, meta)
    elif dataset_id == "DS0002":
        class_label, generator, condition = infer_ds0002_attrs(rel_n, container)
        identity = infer_identity(dataset_id, rel_n)
    elif dataset_id == "DS0003":
        class_label, generator, condition = infer_ds0003_attrs(rel_n)
        identity = ""
    elif dataset_id == "DS0004":
        class_label, generator = infer_ds0004_attrs(rel_n, container)
        identity = infer_identity(dataset_id, rel_n)
    elif dataset_id == "DS0005":
        class_label, generator, condition = "real", "none", ""
        # condition holds split if present
        low = rel_n.lower()
        if low.startswith("train/") or "/train/" in f"/{low}/":
            condition = "train"
        elif low.startswith("val/") or "/val/" in f"/{low}/":
            condition = "val"
        identity = ""
    else:
        identity = ""

    return ImageRecord(
        dataset_id=dataset_id,
        relative_path=rel_n,
        source_container=container,
        class_label=class_label,
        generator=generator,
        condition=condition,
        identity=identity,
        size_bytes=size_bytes,
    )
