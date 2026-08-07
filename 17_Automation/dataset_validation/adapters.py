"""Locate raw roots / archives for each DSxxxx under a Kaggle (or local) root."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DatasetLayout:
    dataset_id: str
    roots: list[Path] = field(default_factory=list)
    archives: list[Path] = field(default_factory=list)
    label_csvs: list[Path] = field(default_factory=list)
    notes: str = ""


KAGGLE_SLUG_DIRS = {
    "DS0001": ["ds0001-artifact-face-subset"],
    "DS0002": ["ds0002-diff-official-test"],
    "DS0003": ["140k-real-and-fake-faces"],
    "DS0004": ["ds0004-synthbuster"],
    "DS0005": ["ds0005-fairface"],
}


def _find_named_dirs(base: Path, names: list[str]) -> list[Path]:
    found: list[Path] = []
    if not base.exists():
        return found
    for name in names:
        direct = base / name
        if direct.is_dir():
            found.append(direct)
    # also search one level deeper (Kaggle sometimes nests)
    for child in sorted(base.iterdir()) if base.is_dir() else []:
        if child.is_dir() and child.name in names and child not in found:
            found.append(child)
    return found


def _rglob_limited(root: Path, pattern: str, limit: int = 50) -> list[Path]:
    out: list[Path] = []
    for p in root.rglob(pattern):
        out.append(p)
        if len(out) >= limit:
            break
    return sorted(out)


def discover_layout(dataset_id: str, search_roots: list[Path]) -> DatasetLayout:
    """Discover archives, image roots, and label CSVs for a dataset ID."""
    layout = DatasetLayout(dataset_id=dataset_id)
    candidates: list[Path] = []

    for root in search_roots:
        root = Path(root)
        if not root.exists():
            continue
        # Prefer slug-named folders under /kaggle/input
        for slug_dir in _find_named_dirs(root, KAGGLE_SLUG_DIRS.get(dataset_id, [])):
            candidates.append(slug_dir)
        # Explicit DS folder
        ds_dir = root / "raw" / dataset_id
        if ds_dir.is_dir():
            candidates.append(ds_dir)
        # Local staging shorthand
        if root.name.upper().startswith(dataset_id) or dataset_id.lower() in root.name.lower():
            candidates.append(root)
        candidates.append(root)

    # Deduplicate while preserving order
    seen: set[Path] = set()
    uniq: list[Path] = []
    for c in candidates:
        rp = c.resolve() if c.exists() else c
        if rp not in seen and c.exists():
            seen.add(rp)
            uniq.append(c)

    for base in uniq:
        zips = _rglob_limited(base, "*.zip", limit=80)
        csvs = [
            p
            for p in _rglob_limited(base, "*.csv", limit=40)
            if "label" in p.name.lower()
            or p.name.lower() == "metadata.csv"
            or "fairface_label" in p.name.lower()
        ]
        # Image directories (contain many jpg/png)
        img_dirs: list[Path] = []
        for dname in ("real", "fake", "train", "val", "valid", "test", "synthetic"):
            for d in base.rglob(dname):
                if d.is_dir():
                    # quick probe
                    probe = list(d.glob("*.jpg"))[:1] + list(d.glob("*.png"))[:1]
                    if probe or any(d.iterdir()):
                        img_dirs.append(d)

        if dataset_id == "DS0001":
            layout.archives.extend(
                [z for z in zips if "artifact" in z.name.lower() or "50k" in z.name.lower()]
                or zips
            )
            layout.label_csvs.extend([c for c in csvs if "metadata" in c.name.lower()] or csvs)
            # Prefer extracted raw/DS0001 if present
            for p in base.rglob("DS0001"):
                if p.is_dir() and (p / "real").exists():
                    layout.roots.append(p)
            # Local staging: incoming/Artifact with real/ + fake/
            if (base / "real").is_dir() and (base / "fake").is_dir():
                layout.roots.append(base)
            meta = base / "metadata.csv"
            if meta.is_file():
                layout.label_csvs.append(meta)
        elif dataset_id == "DS0002":
            layout.archives.extend(
                [z for z in zips if "/test/" in z.as_posix() or "\\test\\" in str(z)] or zips
            )
        elif dataset_id == "DS0003":
            # Usually already extracted on Kaggle
            for p in base.rglob("real_vs_fake"):
                if p.is_dir():
                    layout.roots.append(p)
            if not layout.roots:
                layout.roots.append(base)
            layout.archives.extend(zips)
        elif dataset_id == "DS0004":
            layout.archives.extend(zips)
        elif dataset_id == "DS0005":
            layout.archives.extend(
                [z for z in zips if "fairface" in z.name.lower() or "margin025" in z.name.lower()]
                or zips
            )
            layout.label_csvs.extend(
                [c for c in csvs if "fairface_label" in c.name.lower()] or csvs
            )
            for split in ("train", "val"):
                d = base / split
                if d.is_dir():
                    layout.roots.append(base)

    # Dedup lists
    def dedup(paths: list[Path]) -> list[Path]:
        s: set[Path] = set()
        out: list[Path] = []
        for p in paths:
            try:
                r = p.resolve()
            except OSError:
                r = p
            if r not in s:
                s.add(r)
                out.append(p)
        return out

    layout.roots = dedup(layout.roots)
    layout.archives = dedup(layout.archives)
    layout.label_csvs = dedup(layout.label_csvs)
    layout.notes = f"search_roots={[str(p) for p in search_roots]}"
    return layout
