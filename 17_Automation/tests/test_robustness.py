"""STEP-046 robustness evaluation: config, perturbations, inference loop (stand-in model), analysis."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml
from PIL import Image

from robustness import CLEAN, KINDS, RobustnessConfigError, apply, image_seed, load_config

REPO = Path(__file__).resolve().parents[2]
CONFIG = REPO / "08_Evaluation/EVAL0001/robustness/config.yaml"


def _image(seed: int = 0, size: int = 224) -> Image.Image:
    rng = np.random.default_rng(seed)
    base = np.linspace(0, 255, size, dtype=np.float32)
    x = np.stack([np.add.outer(base, base) / 2, np.tile(base, (size, 1)), rng.uniform(0, 255, (size, size))], axis=2)
    return Image.fromarray(x.astype(np.uint8), "RGB")


def _write_config(tmp_path: Path, perturbations: list[dict], **overrides) -> Path:
    raw = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    raw["perturbations"] = perturbations
    for dotted, value in overrides.items():
        node = raw
        *head, last = dotted.split(".")
        for key in head:
            node = node[key]
        node[last] = value
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")
    return path


# --- config -----------------------------------------------------------------------


def test_repo_config_loads() -> None:
    config = load_config(CONFIG)
    ids = [c.id for c in config.conditions]
    assert ids[0] == CLEAN and len(ids) == len(set(ids))
    assert {p["kind"] for p in config.raw["perturbations"]} == set(KINDS)
    assert "low_quality_upload@0.75_75" in ids


def test_config_hash_ignores_line_endings(tmp_path: Path) -> None:
    text = CONFIG.read_bytes().replace(b"\r\n", b"\n")
    (tmp_path / "lf.yaml").write_bytes(text)
    (tmp_path / "crlf.yaml").write_bytes(text.replace(b"\n", b"\r\n"))
    assert load_config(tmp_path / "lf.yaml").sha256 == load_config(tmp_path / "crlf.yaml").sha256


@pytest.mark.parametrize(
    "perturbations, match",
    [
        ([{"name": "x", "kind": "sepia", "levels": [1]}], "unknown kind"),
        ([{"name": "x", "kind": "jpeg", "levels": [50]}, {"name": "x", "kind": "jpeg", "levels": [30]}], "duplicate"),
        ([{"name": "x", "kind": "jpeg", "levels": [150]}], "out of range"),
        ([{"name": "x", "kind": "resolution", "levels": [1.5]}], "out of range"),
        ([{"name": "x", "kind": "low_quality", "levels": [0.5]}], "factor, quality"),
        ([{"name": "x", "kind": "jpeg", "levels": []}], "non-empty"),
        ([{"name": "clean", "kind": "jpeg", "levels": [50]}], "invalid perturbation name"),
    ],
)
def test_bad_config_fails(tmp_path: Path, perturbations, match) -> None:
    with pytest.raises(RobustnessConfigError, match=match):
        load_config(_write_config(tmp_path, perturbations))


# --- perturbations ----------------------------------------------------------------


def test_every_kind_is_deterministic_rgb() -> None:
    config = load_config(CONFIG)
    img = _image()
    for c in config.conditions[1:]:
        seed = image_seed(42, c.id, "img")
        a, b = apply(c.kind, img, c.level, seed), apply(c.kind, img, c.level, seed)
        assert a.mode == "RGB"
        assert np.array_equal(np.asarray(a), np.asarray(b)), c.id


def test_seeds_depend_on_condition_and_image() -> None:
    assert image_seed(42, "occlusion@0.1", "a") == image_seed(42, "occlusion@0.1", "a")
    assert image_seed(42, "occlusion@0.1", "a") != image_seed(42, "occlusion@0.1", "b")
    assert image_seed(42, "occlusion@0.1", "a") != image_seed(42, "occlusion@0.2", "a")
    img = _image()
    a = apply("occlusion", img, 0.1, image_seed(42, "occlusion@0.1", "a"))
    b = apply("occlusion", img, 0.1, image_seed(42, "occlusion@0.1", "b"))
    assert not np.array_equal(np.asarray(a), np.asarray(b))


def test_perturbations_do_what_they_say() -> None:
    img = _image()
    x = np.asarray(img, dtype=float)

    def err(out):
        return np.abs(np.asarray(out, dtype=float) - x).mean()

    assert err(apply("jpeg", img, 10, 0)) > err(apply("jpeg", img, 90, 0)) > 0
    assert apply("resolution", img, 0.5, 0).size == (112, 112)
    assert apply("scaling", img, 2.0, 0).size == (448, 448)
    assert apply("crop", img, 0.8, 0).size == (179, 179)
    assert apply("low_quality", img, [0.5, 50], 0).size == (112, 112)
    assert np.asarray(apply("gaussian_blur", img, 3.0, 0), dtype=float).std() < x.std()
    assert err(apply("brightness", img, 1.0, 0)) == 0
    assert np.asarray(apply("brightness", img, 0.5, 0), dtype=float).mean() < x.mean()
    grey = np.asarray(apply("saturation", img, 0.0, 0), dtype=int)
    assert np.abs(grey[..., 0] - grey[..., 1]).max() <= 1
    noise = np.asarray(apply("gaussian_noise", _image(size=64).point(lambda v: 128), 0.05, 1), dtype=float) / 255
    assert noise.std() == pytest.approx(0.05, rel=0.1)
    occluded = np.asarray(apply("occlusion", img.point(lambda v: 0), 0.2, 5))
    assert (occluded == 128).all(axis=2).mean() == pytest.approx(0.2, abs=0.01)
    assert apply("rotation", img, 30, 0).size == img.size


# --- inference loop ---------------------------------------------------------------

torch = pytest.importorskip("torch")


class StandIn(torch.nn.Module):
    """P(fake) rises with image brightness; enough to tell conditions apart."""

    def forward(self, x):
        m = x.mean(dim=(1, 2, 3))
        return torch.stack([m, -m], dim=1)


@pytest.fixture()
def tiny(tmp_path: Path):
    from robustness.inference import PerturbedImages, predict

    root = tmp_path / "processed"
    rows = []
    for i in range(6):
        rel = f"images/{'fake' if i < 3 else 'real'}/img{i}.png"
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        _image(seed=i).point(lambda v, i=i: min(255, v + 20 * i)).save(root / rel)
        rows.append({"split": "test", "id": f"id{i}", "y_true": int(i < 3), "processed_path": rel, "generator": "g" if i < 3 else "none"})
    items = pd.DataFrame(rows)
    path = _write_config(
        tmp_path,
        [{"name": "jpeg", "kind": "jpeg", "levels": [50, 10]}, {"name": "occlusion", "kind": "occlusion", "levels": [0.2]}],
        **{"data.predictions": "preds.csv", "inference.batch_size": 4, "inference.num_workers": 0},
    )
    config = load_config(path)
    clean = predict(StandIn(), PerturbedImages(root, items, config.conditions[0], config), 0, 4, 0, "cpu")
    threshold = float(np.median(clean))
    items = items.assign(y_prob=clean, threshold=threshold, y_pred=(clean >= threshold).astype(int))
    items.to_csv(tmp_path / "preds.csv", index=False)
    return tmp_path, root, config, items


def test_run_writes_probs_and_resumes(tiny) -> None:
    from robustness.inference import MANIFEST_NAME, PROBS_NAME, run

    tmp, root, config, items = tiny
    logs: list[str] = []
    wide = run(config, tmp, root, StandIn(), ["fake", "real"], tmp / "work", tmp / "out", device="cpu", log=logs.append)
    assert list(wide.columns) == ["id"] + [c.id for c in config.conditions]
    assert np.allclose(wide[CLEAN], items["y_prob"])
    assert not np.allclose(wide["jpeg@10"], wide[CLEAN])
    manifest = json.loads((tmp / "out" / MANIFEST_NAME).read_text(encoding="utf-8"))
    assert manifest["clean_check"]["max_abs_diff"] < 1e-12 and manifest["config_sha256"] == config.sha256
    first = (tmp / "out" / PROBS_NAME).read_bytes()

    logs.clear()
    run(config, tmp, root, StandIn(), ["fake", "real"], tmp / "work", tmp / "out", device="cpu", log=logs.append)
    assert all("reused" in line for line in logs)
    assert (tmp / "out" / PROBS_NAME).read_bytes() == first


def test_clean_mismatch_stops_the_run(tiny) -> None:
    from robustness.inference import CleanCheckError, run

    tmp, root, config, items = tiny
    items.assign(y_prob=items["y_prob"] + 0.01).to_csv(tmp / "preds.csv", index=False)
    with pytest.raises(CleanCheckError, match="does not match training"):
        run(config, tmp, root, StandIn(), ["fake", "real"], tmp / "work", tmp / "out", device="cpu", log=lambda _: None)
    assert not (tmp / "work" / "jpeg@50.csv").exists()


def test_input_matches_fastai_pipeline(tiny) -> None:
    pytest.importorskip("fastai")
    from fastai.vision.all import CategoryBlock, ColReader, DataBlock, ImageBlock, Normalize, Resize

    from robustness.inference import PerturbedImages

    tmp, root, config, items = tiny
    frame = items.assign(class_label=np.where(items["y_true"] == 1, "fake", "real"))
    block = DataBlock(
        blocks=(ImageBlock, CategoryBlock(vocab=["fake", "real"])),
        get_x=ColReader("processed_path", pref=str(root).rstrip("/\\") + "/"),
        get_y=ColReader("class_label"),
        item_tfms=Resize(224, method="squish"),
        batch_tfms=[Normalize.from_stats(config.get("inference.mean"), config.get("inference.std"))],
    )
    dls = block.dataloaders(frame, bs=6, num_workers=0, device="cpu")
    x_fastai = dls.test_dl(frame, bs=6, num_workers=0).one_batch()[0]
    ours = PerturbedImages(root, items, config.conditions[0], config)
    x_ours = torch.stack([ours[i][0] for i in range(len(ours))])
    assert torch.allclose(x_fastai.float().cpu(), x_ours, atol=1e-5)


def test_find_export_checks_sha(tmp_path: Path) -> None:
    from robustness.inference import find_export

    (tmp_path / "a" / "b").mkdir(parents=True)
    (tmp_path / "a" / "b" / "M_export.pkl").write_bytes(b"model")
    sha = hashlib.sha256(b"model").hexdigest()
    assert find_export([tmp_path], "M_export.pkl", sha).name == "M_export.pkl"
    with pytest.raises(ValueError, match="none matches"):
        find_export([tmp_path], "M_export.pkl", "0" * 64)
    with pytest.raises(FileNotFoundError):
        find_export([tmp_path], "other.pkl", sha)


# --- analysis ---------------------------------------------------------------------


@pytest.fixture(scope="module")
def synthetic():
    from robustness.inference import test_items

    config = load_config(CONFIG)
    items = test_items(config, REPO)
    p = items["y_prob"].to_numpy()
    rng = np.random.default_rng(0)
    cols = {"id": items["id"]}
    for c in config.conditions:
        if c.perturbation == "gaussian_noise":
            cols[c.id] = p * (1 - 0.15 * c.rank)  # same ranking, lower probabilities
        elif c.perturbation == "gaussian_blur":
            mix = 0.2 * c.rank
            cols[c.id] = (1 - mix) * p + mix * rng.uniform(0, 1, len(p))
        else:
            cols[c.id] = p
    index = pd.read_csv(REPO / config.get("data.metadata_index"))
    return config, items, pd.DataFrame(cols), index


def test_analysis_patterns(synthetic) -> None:
    from robustness.analysis import flips_frame, group_frame, metrics_frame, summary_frame

    config, items, wide, index = synthetic
    metrics = metrics_frame(wide, items, config)
    flips = flips_frame(wide, items, config)
    groups = group_frame(wide, items, index, config)
    summary = summary_frame(metrics, flips, groups, config).set_index("perturbation")

    clean = metrics[metrics["condition"] == CLEAN].iloc[0]
    stored = pd.read_csv(REPO / "08_Evaluation/EVAL0001/classification_metrics.csv").set_index("split").loc["test"]
    assert clean["balanced_accuracy"] == pytest.approx(stored["balanced_accuracy"])
    assert (metrics.loc[metrics["condition"] == CLEAN, [c for c in metrics if c.startswith("delta_")]] == 0).all(axis=None)
    assert flips.loc[flips["condition"] == CLEAN, "flips"].iloc[0] == 0

    assert summary.loc["jpeg", "pattern"] == "robust" and summary.loc["jpeg", "tolerance_level"] == "10"
    assert summary.loc["gaussian_noise", "pattern"] == "threshold_shift"
    assert summary.loc["gaussian_noise", "flip_direction"] == "to_real"
    assert summary.loc["gaussian_blur", "pattern"] == "ranking_loss"
    assert summary.loc["gaussian_blur", "tolerance_level"] in {"", "0.5"}
    assert set(summary.index) == {p["name"] for p in config.raw["perturbations"]}


def test_report_lists_every_perturbation(synthetic) -> None:
    from robustness.analysis import flips_frame, group_frame, metrics_frame, summary_frame
    from robustness.report import render_report

    config, items, wide, index = synthetic
    metrics = metrics_frame(wide, items, config)
    flips = flips_frame(wide, items, config)
    summary = summary_frame(metrics, flips, group_frame(wide, items, index, config), config)
    manifest = {"evaluation_id": "EVAL0001", "experiment_id": "EXP0001", "model_id": "MODEL0001", "export_sha256": "a" * 64,
                "config": "config.yaml", "config_sha256": config.sha256, "split": "test", "n_images": len(items),
                "clean_check": {"max_abs_diff": 1e-6, "atol": 0.001, "decision_mismatches": 0}, "device": "cuda"}
    report = render_report(metrics, flips, summary, manifest, 0.02, 0.02, "2026-11-10")
    for p in config.raw["perturbations"]:
        assert f"| {p['name']} |" in report
    assert "threshold_shift" in report and "Clean check" in report
