#!/usr/bin/env python3
"""Sanitize DS0002 processed image paths for Kaggle upload."""

from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from pathlib import Path

# Characters rejected by Kaggle dataset upload (observed + conservative set).
FORBIDDEN = set("'\"?*:<>|#%\\")
_REPLACEMENTS = {
    "'": "_",
    '"': "_",
    "?": "_",
    "*": "_",
    ":": "_",
    "<": "_",
    ">": "_",
    "|": "_",
    "#": "_",
    "%": "_",
    "\\": "_",
}


def sanitize_segment(segment: str) -> str:
    # Fold accents/combining marks (e.g. Camélia, Butkevičius) to ASCII-safe names.
    folded = unicodedata.normalize("NFKD", segment)
    folded = folded.encode("ascii", "ignore").decode("ascii")
    out = "".join(_REPLACEMENTS.get(ch, ch) for ch in folded)
    out = re.sub(r"_+", "_", out)
    return out.strip("_") or "unnamed"


def sanitize_relpath(rel: str) -> str:
    parts = rel.replace("\\", "/").split("/")
    return "/".join(sanitize_segment(p) for p in parts)


def needs_sanitize(rel: str) -> bool:
    folded = sanitize_relpath(rel)
    return folded != rel.replace("\\", "/")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("_processed_dataset/processed_DS0002_PP0002"),
        help="Processed DS0002_PP0002 root",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    images = root / "images"
    index_path = root / "metadata" / "index.csv"
    if not images.is_dir():
        raise SystemExit(f"images dir not found: {images}")
    if not index_path.is_file():
        raise SystemExit(f"index.csv not found: {index_path}")

    renames: list[tuple[Path, Path]] = []
    for src in sorted(images.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(images).as_posix()
        if not needs_sanitize(rel):
            continue
        new_rel = sanitize_relpath(rel)
        dst = images / Path(new_rel)
        if dst == src:
            continue
        if dst.exists() and dst.resolve() != src.resolve():
            raise SystemExit(f"collision after sanitize: {rel} -> {new_rel}")
        renames.append((src, dst))

    print(f"files needing rename: {len(renames)}")
    if args.dry_run:
        for src, dst in renames[:20]:
            print(f"  {src.relative_to(images).as_posix()} -> {dst.relative_to(images).as_posix()}")
        if len(renames) > 20:
            print(f"  ... and {len(renames) - 20} more")
        return 0

    # Rename deepest paths first so parent dirs can be cleaned up.
    for src, dst in sorted(renames, key=lambda t: len(t[0].parts), reverse=True):
        dst.parent.mkdir(parents=True, exist_ok=True)
        src.rename(dst)

    # Update index.csv processed_path + relative_path columns.
    rows: list[dict[str, str]] = []
    with index_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for row in reader:
            for col in ("relative_path", "processed_path"):
                val = row.get(col, "")
                if val.startswith("images/"):
                    suffix = val[len("images/") :]
                    new_suffix = sanitize_relpath(suffix)
                    row[col] = f"images/{new_suffix}"
                elif val:
                    row[col] = sanitize_relpath(val.replace("\\", "/"))
            rows.append(row)

    with index_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Remove empty directories left behind after renames.
    for d in sorted(images.rglob("*"), reverse=True):
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()

    print("sanitization complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
