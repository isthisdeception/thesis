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

# Filename hints when slug folder layout differs on Kaggle.
ARCHIVE_NAME_HINTS = {
    "DS0001": ["artifact", "50k"],
    "DS0002": [],  # use path contains /test/
    "DS0003": [],
    "DS0004": ["synthbuster", "raise"],
    "DS0005": ["fairface", "margin025", "ds0005"],
}


def _find_named_dirs(base: Path, names: list[str]) -> list[Path]:
    found: list[Path] = []
    if not base.exists():
        return found
    for name in names:
        direct = base / name
        if direct.is_dir():
            found.append(direct)
    datasets_root = base / "datasets"
    if datasets_root.is_dir():
        for owner_dir in sorted(datasets_root.iterdir()):
            if not owner_dir.is_dir():
                continue
            for name in names:
                slug_dir = owner_dir / name
                if slug_dir.is_dir() and slug_dir not in found:
                    found.append(slug_dir)
    for child in sorted(base.iterdir()) if base.is_dir() else []:
        if child.is_dir() and child.name in names and child not in found:
            found.append(child)
    return found


def _dedup_paths(paths: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    out: list[Path] = []
    for p in paths:
        try:
            key = p.resolve()
        except OSError:
            key = p
        if key not in seen and p.exists():
            seen.add(key)
            out.append(p)
    return out


def _collect_candidates(dataset_id: str, search_roots: list[Path]) -> list[Path]:
    """Aggressively find every plausible mount point under search roots."""
    slugs = KAGGLE_SLUG_DIRS.get(dataset_id, [])
    candidates: list[Path] = []

    for root in search_roots:
        root = Path(root)
        if not root.exists():
            continue
        candidates.append(root)
        candidates.extend(_find_named_dirs(root, slugs))
        # Any folder named like the Kaggle slug anywhere under root
        for slug in slugs:
            try:
                for hit in root.rglob(slug):
                    if hit.is_dir():
                        candidates.append(hit)
            except OSError:
                pass
        # raw/DSxxxx folders
        try:
            for hit in root.rglob(f"raw/{dataset_id}"):
                if hit.is_dir():
                    candidates.append(hit)
            for hit in root.rglob(dataset_id):
                if hit.is_dir():
                    candidates.append(hit)
        except OSError:
            pass
        ds_direct = root / "raw" / dataset_id
        if ds_direct.is_dir():
            candidates.append(ds_direct)

    return _dedup_paths(candidates)


def _find_all_zips(base: Path) -> list[Path]:
    try:
        return sorted(p for p in base.rglob("*.zip") if p.is_file())
    except OSError:
        return []


def _filter_archives(dataset_id: str, zips: list[Path]) -> list[Path]:
    if not zips:
        return []
    hints = ARCHIVE_NAME_HINTS.get(dataset_id, [])
    if dataset_id == "DS0002":
        matched = [
            z
            for z in zips
            if "/test/" in z.as_posix() or "\\test\\" in str(z)
        ]
        return matched or zips
    if hints:
        matched = [z for z in zips if any(h in z.name.lower() for h in hints)]
        if matched:
            return matched
    return zips


def _find_label_csvs(base: Path, dataset_id: str) -> list[Path]:
    csvs: list[Path] = []
    try:
        for p in base.rglob("*.csv"):
            if not p.is_file():
                continue
            # Never treat pack manifests as label tables
            if "manifests" in p.as_posix().lower():
                continue
            n = p.name.lower()
            if dataset_id == "DS0005":
                if n.startswith("fairface_label_"):
                    csvs.append(p)
            elif dataset_id == "DS0001":
                if n == "metadata.csv":
                    csvs.append(p)
            elif "label" in n and n not in {"label_summary.csv"}:
                csvs.append(p)
    except OSError:
        pass
    return sorted(set(csvs))


def discover_layout(dataset_id: str, search_roots: list[Path]) -> DatasetLayout:
    """Discover archives, image roots, and label CSVs for a dataset ID."""
    layout = DatasetLayout(dataset_id=dataset_id)
    candidates = _collect_candidates(dataset_id, search_roots)

    for base in candidates:
        zips = _find_all_zips(base)
        layout.archives.extend(_filter_archives(dataset_id, zips))
        # Always keep every zip under a DSxxxx path for zip-packaged sets
        if dataset_id in {"DS0002", "DS0004"}:
            layout.archives.extend(zips)
        layout.label_csvs.extend(_find_label_csvs(base, dataset_id))

        if dataset_id == "DS0001":
            for p in base.rglob("DS0001"):
                if p.is_dir() and (p / "real").is_dir():
                    layout.roots.append(p)
            if (base / "real").is_dir() and (base / "fake").is_dir():
                layout.roots.append(base)
        elif dataset_id == "DS0002":
            # Prefer remaining test/*.zip archives; also accept extracted generator trees
            for cond in ("FE", "FS", "I2I", "T2I"):
                for d in base.rglob(cond):
                    if d.is_dir() and any(d.iterdir()):
                        layout.roots.append(d)
            for p in base.rglob("test"):
                if p.is_dir():
                    layout.roots.append(p)
        elif dataset_id == "DS0003":
            for p in base.rglob("real_vs_fake"):
                if p.is_dir():
                    layout.roots.append(p)
            if not any(r.name == "real_vs_fake" for r in layout.roots):
                # train/valid folders with images
                for probe in base.rglob("train"):
                    if probe.is_dir() and list(probe.glob("*.jpg"))[:1]:
                        layout.roots.append(base)
                        break
        elif dataset_id == "DS0004":
            # Kaggle extracts to:
            #   raw/DS0004/real/raise_1k_jpeg/*.jpg
            #   raw/DS0004/synthetic/synthbuster/synthbuster/<generator>/*.png
            # Avoid list(iterdir()) on huge image dirs — use glob probes only.
            named = ("real", "synthetic", "synthbuster", "raise_1k_jpeg", "DS0004")

            def _usable_image_dir(d: Path) -> bool:
                if not d.is_dir():
                    return False
                try:
                    if next(d.glob("*.jpg"), None):
                        return True
                    if next(d.glob("*.jpeg"), None):
                        return True
                    if next(d.glob("*.png"), None):
                        return True
                    # Generator / split folders (dirs only — do not list all files)
                    return any(child.is_dir() for child in d.iterdir())
                except OSError:
                    return False

            if base.name in named and _usable_image_dir(base):
                layout.roots.append(base)
            for name in named:
                for d in base.rglob(name):
                    if _usable_image_dir(d):
                        layout.roots.append(d)

            # Hard Kaggle paths (bypass brittle discovery)
            for rel in (
                "raw/DS0004/real/raise_1k_jpeg",
                "raw/DS0004/synthetic/synthbuster/synthbuster",
                "raw/DS0004/synthetic/synthbuster",
                "raw/DS0004/real",
            ):
                hard = base / rel
                if _usable_image_dir(hard):
                    layout.roots.append(hard)
                # also from dataset root one level up
                hard2 = base.parent / rel if base.name == "DS0004" else None
                if hard2 and _usable_image_dir(hard2):
                    layout.roots.append(hard2)

            layout.archives.extend(zips)
            if not layout.roots and not layout.archives:
                for d in base.rglob("*"):
                    if not d.is_dir():
                        continue
                    try:
                        if next(d.glob("*.jpg"), None) or next(d.glob("*.png"), None):
                            layout.roots.append(d)
                    except OSError:
                        continue
                    if len(layout.roots) >= 30:
                        break
        elif dataset_id == "DS0005":
            if (base / "train").is_dir() or (base / "val").is_dir():
                layout.roots.append(base)
            for split in ("train", "val"):
                for d in base.rglob(split):
                    if d.is_dir() and list(d.glob("*.jpg"))[:1]:
                        layout.roots.append(d.parent)
                        break

    layout.roots = _dedup_paths(layout.roots)
    layout.archives = _dedup_paths(layout.archives)
    layout.label_csvs = _dedup_paths(layout.label_csvs)
    layout.notes = (
        f"search_roots={[str(p) for p in search_roots]}; "
        f"candidates={[str(p) for p in candidates]}"
    )
    return layout


def debug_layout(dataset_id: str, search_roots: list[Path]) -> dict:
    """Human-readable discovery debug (for Kaggle smoke tests)."""
    roots = [Path(r) for r in search_roots]
    layout = discover_layout(dataset_id, roots)
    return {
        "dataset_id": dataset_id,
        "search_roots_exist": {str(r): r.exists() for r in roots},
        "candidates": layout.notes,
        "roots": [str(p) for p in layout.roots],
        "archives": [str(p) for p in layout.archives],
        "label_csvs": [str(p) for p in layout.label_csvs],
        "all_zips_under_input": [
            str(p)
            for p in sorted(Path("/kaggle/input").rglob("*.zip"))
            if any(
                k in p.as_posix().lower()
                for k in ("fairface", "margin", "ds0005", "synthbuster", "raise", "ds0004", "diff", "artifact")
            )
        ][:40]
        if Path("/kaggle/input").exists()
        else [],
    }
