"""Orchestrate Phase D7 EDA and write report CSVs (read-only on raw)."""

from __future__ import annotations

import csv
import json
import random
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

from dataset_validation.adapters import DatasetLayout, discover_layout

from .labels import (
    ImageRecord,
    load_ds0001_metadata,
    load_fairface_labels,
    record_from_path,
)
from .metrics import mean_std, percentile, stats_from_path, stats_from_zip_member
from .schemas import (
    BALANCE_COLUMNS,
    BRIGHTNESS_COLUMNS,
    CHANNEL_COLUMNS,
    CLASS_COLUMNS,
    COMPRESSION_COLUMNS,
    CONTRAST_COLUMNS,
    DEFAULT_PIXEL_SAMPLE,
    DEFAULT_RNG_SEED,
    DEMOGRAPHIC_COLUMNS,
    ERROR_COLUMNS,
    GENERATOR_COLUMNS,
    IDENTITY_COLUMNS,
    RESOLUTION_COLUMNS,
)


@dataclass
class EdaAccumulator:
    records: list[ImageRecord] = field(default_factory=list)
    errors: list[dict] = field(default_factory=list)
    # pixel sample results keyed parallel to sampled records
    widths: list[int] = field(default_factory=list)
    heights: list[int] = field(default_factory=list)
    modes: list[str] = field(default_factory=list)
    formats: list[str] = field(default_factory=list)
    brightness: list[float] = field(default_factory=list)
    contrast: list[float] = field(default_factory=list)
    mean_r: list[float] = field(default_factory=list)
    mean_g: list[float] = field(default_factory=list)
    mean_b: list[float] = field(default_factory=list)
    sizes: list[int] = field(default_factory=list)
    strata: list[str] = field(default_factory=list)
    pixel_policy: str = ""
    roots_used: list[str] = field(default_factory=list)
    archives_used: list[str] = field(default_factory=list)


def _write_csv(path: Path, columns: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({c: row.get(c, "") for c in columns})


def _enumerate_directory(
    dataset_id: str,
    root: Path,
    ds0001_meta: dict,
) -> tuple[list[ImageRecord], list[dict]]:
    records: list[ImageRecord] = []
    errors: list[dict] = []
    try:
        paths = sorted(p for p in root.rglob("*") if p.is_file())
    except OSError as e:
        errors.append(
            {
                "Dataset ID": dataset_id,
                "Relative Path": str(root),
                "Error Code": "ROOT_UNREADABLE",
                "Error Detail": str(e),
                "Source Container": str(root),
            }
        )
        return records, errors
    for p in paths:
        try:
            rel = p.relative_to(root).as_posix()
        except ValueError:
            rel = p.as_posix()
        try:
            size = p.stat().st_size
        except OSError as e:
            errors.append(
                {
                    "Dataset ID": dataset_id,
                    "Relative Path": rel,
                    "Error Code": "STAT_FAILED",
                    "Error Detail": str(e),
                    "Source Container": str(root),
                }
            )
            continue
        rec = record_from_path(dataset_id, rel, str(root), size_bytes=size, ds0001_meta=ds0001_meta)
        if rec:
            records.append(rec)
    return records, errors


def _enumerate_zip(
    dataset_id: str,
    archive: Path,
    ds0001_meta: dict,
) -> tuple[list[ImageRecord], list[dict]]:
    records: list[ImageRecord] = []
    errors: list[dict] = []
    try:
        zf = zipfile.ZipFile(archive, "r")
    except zipfile.BadZipFile as e:
        errors.append(
            {
                "Dataset ID": dataset_id,
                "Relative Path": archive.name,
                "Error Code": "ARCHIVE_UNREADABLE",
                "Error Detail": str(e),
                "Source Container": str(archive),
            }
        )
        return records, errors
    with zf:
        for info in sorted(zf.infolist(), key=lambda x: x.filename):
            if info.is_dir():
                continue
            rec = record_from_path(
                dataset_id,
                info.filename,
                str(archive),
                size_bytes=info.file_size,
                ds0001_meta=ds0001_meta,
            )
            if rec:
                records.append(rec)
    return records, errors


def _stratum(rec: ImageRecord) -> str:
    return f"{rec.class_label}|{rec.generator}|{rec.condition}"


def _select_pixel_sample(
    records: list[ImageRecord],
    pixel_sample: int | None,
    full_pixels: bool,
    seed: int,
) -> list[ImageRecord]:
    if full_pixels or pixel_sample is None:
        return list(records)
    if pixel_sample <= 0:
        return []
    if len(records) <= pixel_sample:
        return list(records)
    by_s: dict[str, list[ImageRecord]] = defaultdict(list)
    for r in records:
        by_s[_stratum(r)].append(r)
    rng = random.Random(seed)
    # proportional allocation with at least 1 per non-empty stratum when possible
    keys = sorted(by_s.keys())
    alloc: dict[str, int] = {}
    remaining = pixel_sample
    for k in keys:
        alloc[k] = 1
        remaining -= 1
    if remaining < 0:
        # too many strata; take first pixel_sample strata with 1 each
        chosen_keys = keys[:pixel_sample]
        return [by_s[k][0] for k in chosen_keys]
    total = len(records)
    extras = []
    for k in keys:
        share = int(round(remaining * (len(by_s[k]) / total)))
        extras.append((k, share))
    # fix rounding
    s = sum(x for _, x in extras)
    i = 0
    while s < remaining and extras:
        k, v = extras[i % len(extras)]
        extras[i % len(extras)] = (k, v + 1)
        s += 1
        i += 1
    while s > remaining and extras:
        k, v = extras[i % len(extras)]
        if v > 0:
            extras[i % len(extras)] = (k, v - 1)
            s -= 1
        i += 1
    for k, v in extras:
        alloc[k] = alloc.get(k, 0) + v
    sample: list[ImageRecord] = []
    for k in keys:
        pool = list(by_s[k])
        rng.shuffle(pool)
        sample.extend(pool[: min(alloc[k], len(pool))])
    # top up if short
    if len(sample) < pixel_sample:
        leftover = [r for r in records if r not in sample]
        rng.shuffle(leftover)
        sample.extend(leftover[: pixel_sample - len(sample)])
    return sample[:pixel_sample]


def _measure_pixels(dataset_id: str, sample: list[ImageRecord], acc: EdaAccumulator) -> None:
    # Group zip members
    zip_groups: dict[str, list[ImageRecord]] = defaultdict(list)
    files: list[ImageRecord] = []
    for r in sample:
        cont = Path(r.source_container)
        if cont.suffix.lower() == ".zip":
            zip_groups[str(cont)].append(r)
        else:
            files.append(r)

    for r in files:
        path = Path(r.source_container) / r.relative_path
        # if container is already the file's parent tree root
        if not path.is_file():
            path = Path(r.source_container)
            # relative may already include parents under root
            cand = Path(r.source_container) / Path(r.relative_path).name
            path = path if path.is_file() else cand
        try:
            # Prefer join of container root + relative
            full = Path(r.source_container) / r.relative_path
            if not full.is_file():
                # sometimes container is a leaf folder and relative is basename-ish
                full = Path(r.source_container) / Path(r.relative_path).name
            st = stats_from_path(full)
            acc.widths.append(st.width)
            acc.heights.append(st.height)
            acc.modes.append(st.mode)
            acc.formats.append(st.format)
            acc.brightness.append(st.brightness)
            acc.contrast.append(st.contrast)
            acc.mean_r.append(st.mean_r)
            acc.mean_g.append(st.mean_g)
            acc.mean_b.append(st.mean_b)
            acc.sizes.append(st.size_bytes or r.size_bytes)
            acc.strata.append(_stratum(r))
        except Exception as e:  # noqa: BLE001 — record and continue
            acc.errors.append(
                {
                    "Dataset ID": dataset_id,
                    "Relative Path": r.relative_path,
                    "Error Code": "PIXEL_READ_FAILED",
                    "Error Detail": str(e),
                    "Source Container": r.source_container,
                }
            )

    for zpath, recs in sorted(zip_groups.items()):
        try:
            zf = zipfile.ZipFile(zpath, "r")
        except zipfile.BadZipFile as e:
            acc.errors.append(
                {
                    "Dataset ID": dataset_id,
                    "Relative Path": Path(zpath).name,
                    "Error Code": "ARCHIVE_UNREADABLE",
                    "Error Detail": str(e),
                    "Source Container": zpath,
                }
            )
            continue
        with zf:
            for r in recs:
                try:
                    st = stats_from_zip_member(zf, r.relative_path)
                    acc.widths.append(st.width)
                    acc.heights.append(st.height)
                    acc.modes.append(st.mode)
                    acc.formats.append(st.format)
                    acc.brightness.append(st.brightness)
                    acc.contrast.append(st.contrast)
                    acc.mean_r.append(st.mean_r)
                    acc.mean_g.append(st.mean_g)
                    acc.mean_b.append(st.mean_b)
                    acc.sizes.append(st.size_bytes or r.size_bytes)
                    acc.strata.append(_stratum(r))
                except Exception as e:  # noqa: BLE001
                    acc.errors.append(
                        {
                            "Dataset ID": dataset_id,
                            "Relative Path": r.relative_path,
                            "Error Code": "PIXEL_READ_FAILED",
                            "Error Detail": str(e),
                            "Source Container": zpath,
                        }
                    )


def analyze_dataset(
    dataset_id: str,
    search_roots: Sequence[Path],
    pixel_sample: int | None = DEFAULT_PIXEL_SAMPLE,
    full_pixels: bool = False,
    seed: int = DEFAULT_RNG_SEED,
) -> EdaAccumulator:
    layout: DatasetLayout = discover_layout(dataset_id, list(search_roots))
    ds0001_meta = load_ds0001_metadata(layout.label_csvs) if dataset_id == "DS0001" else {}
    # Also search metadata.csv next to archives
    if dataset_id == "DS0001" and not ds0001_meta:
        for a in layout.archives:
            side = a.parent / "metadata.csv"
            if side.is_file():
                ds0001_meta = load_ds0001_metadata([side])
                break

    acc = EdaAccumulator()
    acc.roots_used = [str(p) for p in layout.roots]
    acc.archives_used = [str(p) for p in layout.archives]

    # Prefer archives when present (local Kaggle packs); also scan extracted roots.
    # Avoid double-counting: if an archive exists under a root, skip enumerating that root's loose files
    # that are the same images — for staging packs, images live only in zips.
    seen_containers: set[str] = set()

    for archive in layout.archives:
        key = str(archive.resolve()) if archive.exists() else str(archive)
        if key in seen_containers:
            continue
        seen_containers.add(key)
        recs, errs = _enumerate_zip(dataset_id, archive, ds0001_meta)
        acc.records.extend(recs)
        acc.errors.extend(errs)

    for root in layout.roots:
        key = str(root.resolve()) if root.exists() else str(root)
        if key in seen_containers:
            continue
        # Skip roots that only contain zips we already enumerated
        try:
            only_zips = all(p.suffix.lower() == ".zip" for p in root.rglob("*") if p.is_file()) and any(
                p.suffix.lower() == ".zip" for p in root.rglob("*.zip")
            )
        except OSError:
            only_zips = False
        if only_zips:
            continue
        seen_containers.add(key)
        recs, errs = _enumerate_directory(dataset_id, root, ds0001_meta)
        acc.records.extend(recs)
        acc.errors.extend(errs)

    # Dedup by (container, relative_path)
    uniq: dict[tuple[str, str], ImageRecord] = {}
    for r in acc.records:
        uniq[(r.source_container, r.relative_path)] = r
    acc.records = [uniq[k] for k in sorted(uniq.keys())]

    if full_pixels:
        acc.pixel_policy = "full_population"
        sample = acc.records
    else:
        n = DEFAULT_PIXEL_SAMPLE if pixel_sample is None else pixel_sample
        acc.pixel_policy = f"stratified_sample_n={n}_seed={seed}"
        sample = _select_pixel_sample(acc.records, n, full_pixels=False, seed=seed)

    _measure_pixels(dataset_id, sample, acc)
    return acc


def _prop(count: int, total: int) -> str:
    return f"{(count / total):.6f}" if total else "0.000000"


def _brightness_rows(dataset_id: str, acc: EdaAccumulator) -> list[dict]:
    rows: list[dict] = []
    # overall
    m, s = mean_std(acc.brightness)
    rows.append(
        {
            "Dataset ID": dataset_id,
            "Stratum": "ALL",
            "N": len(acc.brightness),
            "Mean": f"{m:.6f}" if acc.brightness else "",
            "Std": f"{s:.6f}" if acc.brightness else "",
            "P05": f"{percentile(acc.brightness, 5):.6f}" if acc.brightness else "",
            "P50": f"{percentile(acc.brightness, 50):.6f}" if acc.brightness else "",
            "P95": f"{percentile(acc.brightness, 95):.6f}" if acc.brightness else "",
            "Sample Policy": acc.pixel_policy,
            "Notes": "luma mean in [0,1]; thumbnail<=256px",
        }
    )
    by: dict[str, list[float]] = defaultdict(list)
    for st, b in zip(acc.strata, acc.brightness):
        by[st].append(b)
    for st in sorted(by.keys()):
        xs = by[st]
        m, s = mean_std(xs)
        rows.append(
            {
                "Dataset ID": dataset_id,
                "Stratum": st,
                "N": len(xs),
                "Mean": f"{m:.6f}",
                "Std": f"{s:.6f}",
                "P05": f"{percentile(xs, 5):.6f}",
                "P50": f"{percentile(xs, 50):.6f}",
                "P95": f"{percentile(xs, 95):.6f}",
                "Sample Policy": acc.pixel_policy,
                "Notes": "",
            }
        )
    return rows


def _contrast_rows(dataset_id: str, acc: EdaAccumulator) -> list[dict]:
    rows: list[dict] = []
    m, s = mean_std(acc.contrast)
    rows.append(
        {
            "Dataset ID": dataset_id,
            "Stratum": "ALL",
            "N": len(acc.contrast),
            "Mean": f"{m:.6f}" if acc.contrast else "",
            "Std": f"{s:.6f}" if acc.contrast else "",
            "P05": f"{percentile(acc.contrast, 5):.6f}" if acc.contrast else "",
            "P50": f"{percentile(acc.contrast, 50):.6f}" if acc.contrast else "",
            "P95": f"{percentile(acc.contrast, 95):.6f}" if acc.contrast else "",
            "Sample Policy": acc.pixel_policy,
            "Notes": "luma std in [0,1]; thumbnail<=256px",
        }
    )
    by: dict[str, list[float]] = defaultdict(list)
    for st, c in zip(acc.strata, acc.contrast):
        by[st].append(c)
    for st in sorted(by.keys()):
        xs = by[st]
        m, s = mean_std(xs)
        rows.append(
            {
                "Dataset ID": dataset_id,
                "Stratum": st,
                "N": len(xs),
                "Mean": f"{m:.6f}",
                "Std": f"{s:.6f}",
                "P05": f"{percentile(xs, 5):.6f}",
                "P50": f"{percentile(xs, 50):.6f}",
                "P95": f"{percentile(xs, 95):.6f}",
                "Sample Policy": acc.pixel_policy,
                "Notes": "",
            }
        )
    return rows


def build_report_rows(
    dataset_id: str,
    acc: EdaAccumulator,
    fairface: dict[str, dict[str, str]] | None = None,
) -> dict[str, list[dict]]:
    total = len(acc.records)
    class_c = Counter(r.class_label for r in acc.records)
    gen_c = Counter((r.generator, r.class_label, r.condition) for r in acc.records)

    class_rows = [
        {
            "Dataset ID": dataset_id,
            "Class": k,
            "Count": v,
            "Proportion": _prop(v, total),
            "Notes": "",
        }
        for k, v in sorted(class_c.items())
    ]

    gen_rows = [
        {
            "Dataset ID": dataset_id,
            "Generator": g,
            "Class": cls,
            "Condition": cond,
            "Count": n,
            "Proportion": _prop(n, total),
            "Notes": "",
        }
        for (g, cls, cond), n in sorted(gen_c.items(), key=lambda x: (-x[1], x[0]))
    ]

    ids = [r.identity for r in acc.records if r.identity]
    id_counts = Counter(ids)
    if id_counts:
        vals = list(id_counts.values())
        identity_rows = [
            {"Dataset ID": dataset_id, "Metric": "n_images_with_identity", "Value": len(ids), "Notes": ""},
            {
                "Dataset ID": dataset_id,
                "Metric": "n_unique_identities",
                "Value": len(id_counts),
                "Notes": "DS0001/DS0002 person-like; DS0004 image stem",
            },
            {
                "Dataset ID": dataset_id,
                "Metric": "mean_images_per_identity",
                "Value": f"{(sum(vals) / len(vals)):.4f}",
                "Notes": "",
            },
            {"Dataset ID": dataset_id, "Metric": "max_images_per_identity", "Value": max(vals), "Notes": ""},
            {
                "Dataset ID": dataset_id,
                "Metric": "singleton_identities",
                "Value": sum(1 for v in vals if v == 1),
                "Notes": "",
            },
            {
                "Dataset ID": dataset_id,
                "Metric": "coverage",
                "Value": _prop(len(ids), total),
                "Notes": "fraction of images with identity attribute",
            },
        ]
    else:
        identity_rows = [
            {
                "Dataset ID": dataset_id,
                "Metric": "identity_available",
                "Value": "no",
                "Notes": "unavailable for this dataset layout",
            }
        ]

    # resolution from pixel sample
    res_c = Counter(zip(acc.widths, acc.heights))
    res_n = sum(res_c.values())
    resolution_rows = [
        {
            "Dataset ID": dataset_id,
            "Width": w,
            "Height": h,
            "Count": n,
            "Proportion": _prop(n, res_n),
            "Notes": acc.pixel_policy,
        }
        for (w, h), n in sorted(res_c.items(), key=lambda x: -x[1])
    ]

    mode_c = Counter(acc.modes)
    mode_n = sum(mode_c.values()) or 1
    # mean RGB overall
    mr, _ = mean_std(acc.mean_r)
    mg, _ = mean_std(acc.mean_g)
    mb, _ = mean_std(acc.mean_b)
    channel_rows = []
    for mode, n in sorted(mode_c.items()):
        channel_rows.append(
            {
                "Dataset ID": dataset_id,
                "Mode": mode,
                "Count": n,
                "Proportion": _prop(n, mode_n),
                "Mean_R": f"{mr:.6f}" if acc.mean_r else "",
                "Mean_G": f"{mg:.6f}" if acc.mean_g else "",
                "Mean_B": f"{mb:.6f}" if acc.mean_b else "",
                "Sample Policy": acc.pixel_policy,
                "Notes": "RGB means are global sample means (not per-mode)",
            }
        )

    fmt_groups: dict[str, list[int]] = defaultdict(list)
    for fmt, sz in zip(acc.formats, acc.sizes):
        fmt_groups[fmt].append(sz)
    compression_rows = []
    for fmt, sizes in sorted(fmt_groups.items()):
        compression_rows.append(
            {
                "Dataset ID": dataset_id,
                "Format": fmt,
                "Count": len(sizes),
                "Mean Bytes": f"{(sum(sizes) / len(sizes)):.1f}",
                "Median Bytes": f"{percentile([float(x) for x in sizes], 50):.1f}",
                "P05 Bytes": f"{percentile([float(x) for x in sizes], 5):.1f}",
                "P95 Bytes": f"{percentile([float(x) for x in sizes], 95):.1f}",
                "Sample Policy": acc.pixel_policy,
                "Notes": "",
            }
        )

    real_n = class_c.get("real", 0)
    fake_n = class_c.get("fake", 0)
    balance_rows = [
        {"Dataset ID": dataset_id, "Metric": "n_images", "Value": total, "Notes": "full enumeration"},
        {
            "Dataset ID": dataset_id,
            "Metric": "n_generators",
            "Value": len({r.generator for r in acc.records}),
            "Notes": "",
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "real_fake_ratio",
            "Value": f"{(real_n / fake_n):.6f}" if fake_n else ("inf" if real_n else "n/a"),
            "Notes": "real/fake; inf if fake=0",
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "balance_abs_diff",
            "Value": abs(real_n - fake_n),
            "Notes": "|real-fake|",
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "pixel_sample_n",
            "Value": len(acc.brightness),
            "Notes": acc.pixel_policy,
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "pixel_errors",
            "Value": sum(1 for e in acc.errors if e.get("Error Code") == "PIXEL_READ_FAILED"),
            "Notes": "",
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "roots_used",
            "Value": len(acc.roots_used),
            "Notes": ";".join(acc.roots_used[:5]),
        },
        {
            "Dataset ID": dataset_id,
            "Metric": "archives_used",
            "Value": len(acc.archives_used),
            "Notes": ";".join(Path(p).name for p in acc.archives_used[:8]),
        },
    ]

    demo_rows: list[dict] = []
    if fairface:
        # Count from label table (authoritative for DS0005)
        split_attr: Counter[tuple[str, str, str]] = Counter()
        for meta in fairface.values():
            # fairface dict also has basename keys — skip duplicates by requiring split
            split = meta.get("split") or ""
            if not split:
                continue
            for attr in ("age", "gender", "race"):
                level = meta.get(attr) or ""
                if level:
                    split_attr[(split, attr, level)] += 1
        # If double-counted due to basename keys, rebuild from unique file keys only
        split_attr = Counter()
        seen_files: set[str] = set()
        for key, meta in fairface.items():
            if "/" not in key:
                continue
            if key in seen_files:
                continue
            seen_files.add(key)
            split = meta.get("split") or key.split("/", 1)[0]
            for attr in ("age", "gender", "race"):
                level = meta.get(attr) or ""
                if level:
                    split_attr[(split, attr, level)] += 1
        by_split_attr_total: dict[tuple[str, str], int] = defaultdict(int)
        for (split, attr, _level), n in split_attr.items():
            by_split_attr_total[(split, attr)] += n
        for (split, attr, level), n in sorted(split_attr.items()):
            demo_rows.append(
                {
                    "Dataset ID": dataset_id,
                    "Split": split,
                    "Attribute": attr,
                    "Level": level,
                    "Count": n,
                    "Proportion": _prop(n, by_split_attr_total[(split, attr)]),
                    "Notes": "from FairFace label CSVs",
                }
            )

    return {
        "class": class_rows,
        "generator": gen_rows,
        "identity": identity_rows,
        "resolution": resolution_rows,
        "brightness": _brightness_rows(dataset_id, acc),
        "contrast": _contrast_rows(dataset_id, acc),
        "channel": channel_rows,
        "compression": compression_rows,
        "balance": balance_rows,
        "demographic": demo_rows,
        "errors": acc.errors,
    }


def run_eda(
    dataset_ids: Sequence[str],
    search_roots: Sequence[Path],
    output_dir: Path,
    pixel_sample: int | None = DEFAULT_PIXEL_SAMPLE,
    full_pixels: bool = False,
    seed: int = DEFAULT_RNG_SEED,
) -> dict:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    step_dir = output_dir / "step023"
    step_dir.mkdir(parents=True, exist_ok=True)

    combined: dict[str, list[dict]] = {
        "class": [],
        "generator": [],
        "identity": [],
        "resolution": [],
        "brightness": [],
        "contrast": [],
        "channel": [],
        "compression": [],
        "balance": [],
        "demographic": [],
        "errors": [],
    }
    summary: dict = {
        "built_utc": datetime.now(timezone.utc).isoformat(),
        "pixel_sample": pixel_sample,
        "full_pixels": full_pixels,
        "seed": seed,
        "search_roots": [str(p) for p in search_roots],
        "datasets": {},
    }

    for ds in dataset_ids:
        print(f"[EDA] {ds}: discovering + enumerating…", flush=True)
        acc = analyze_dataset(
            ds,
            search_roots,
            pixel_sample=pixel_sample,
            full_pixels=full_pixels,
            seed=seed,
        )
        fairface = None
        if ds == "DS0005":
            layout = discover_layout(ds, list(search_roots))
            fairface = load_fairface_labels(layout.label_csvs)
            if not fairface:
                # staging pack: labels beside zip
                for a in layout.archives:
                    for name in ("fairface_label_train.csv", "fairface_label_val.csv"):
                        p = a.parent / name
                        if p.is_file():
                            fairface = {**(fairface or {}), **load_fairface_labels([p])}

        rows = build_report_rows(ds, acc, fairface=fairface)
        for k, v in rows.items():
            combined[k].extend(v)

        # per-dataset copies
        mapping = {
            "class": ("eda_class_distribution.csv", CLASS_COLUMNS),
            "generator": ("eda_generator_distribution.csv", GENERATOR_COLUMNS),
            "identity": ("eda_identity_distribution.csv", IDENTITY_COLUMNS),
            "resolution": ("eda_resolution_distribution.csv", RESOLUTION_COLUMNS),
            "brightness": ("eda_brightness_stats.csv", BRIGHTNESS_COLUMNS),
            "contrast": ("eda_contrast_stats.csv", CONTRAST_COLUMNS),
            "channel": ("eda_channel_stats.csv", CHANNEL_COLUMNS),
            "compression": ("eda_compression_stats.csv", COMPRESSION_COLUMNS),
            "balance": ("eda_balance_summary.csv", BALANCE_COLUMNS),
            "demographic": ("eda_demographic_distribution.csv", DEMOGRAPHIC_COLUMNS),
            "errors": ("eda_errors.csv", ERROR_COLUMNS),
        }
        ds_dir = step_dir / ds
        ds_dir.mkdir(parents=True, exist_ok=True)
        for key, (fname, cols) in mapping.items():
            if rows[key] or key == "errors":
                _write_csv(ds_dir / fname, cols, rows[key])

        summary["datasets"][ds] = {
            "n_images": len(acc.records),
            "n_pixel_measured": len(acc.brightness),
            "n_errors": len(acc.errors),
            "pixel_policy": acc.pixel_policy,
            "roots_used": acc.roots_used,
            "archives_used": [Path(p).name for p in acc.archives_used],
        }
        print(
            f"[EDA] {ds}: images={len(acc.records)} pixels={len(acc.brightness)} errors={len(acc.errors)}",
            flush=True,
        )

    # combined outputs at reports/
    _write_csv(output_dir / "eda_class_distribution.csv", CLASS_COLUMNS, combined["class"])
    _write_csv(output_dir / "eda_generator_distribution.csv", GENERATOR_COLUMNS, combined["generator"])
    _write_csv(output_dir / "eda_identity_distribution.csv", IDENTITY_COLUMNS, combined["identity"])
    _write_csv(output_dir / "eda_resolution_distribution.csv", RESOLUTION_COLUMNS, combined["resolution"])
    _write_csv(output_dir / "eda_brightness_stats.csv", BRIGHTNESS_COLUMNS, combined["brightness"])
    _write_csv(output_dir / "eda_contrast_stats.csv", CONTRAST_COLUMNS, combined["contrast"])
    _write_csv(output_dir / "eda_channel_stats.csv", CHANNEL_COLUMNS, combined["channel"])
    _write_csv(output_dir / "eda_compression_stats.csv", COMPRESSION_COLUMNS, combined["compression"])
    _write_csv(output_dir / "eda_balance_summary.csv", BALANCE_COLUMNS, combined["balance"])
    _write_csv(
        output_dir / "eda_demographic_distribution.csv", DEMOGRAPHIC_COLUMNS, combined["demographic"]
    )
    _write_csv(output_dir / "eda_errors.csv", ERROR_COLUMNS, combined["errors"])
    (output_dir / "eda_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (step_dir / "eda_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
