"""STEP-047 generalization: config, cross-dataset inference loop (stand-in model), E8 analysis, E9 analysis."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml
from PIL import Image

from generalization import GeneralizationConfigError, load_config

REPO = Path(__file__).resolve().parents[2]
CONFIG = REPO / "08_Evaluation/EVAL0001/generalization/config.yaml"


def _write_config(tmp_path: Path, mutate) -> Path:
    raw = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    mutate(raw)
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")
    return path


# --- config -----------------------------------------------------------------------


def test_repo_config_loads() -> None:
    config = load_config(CONFIG)
    assert [d["name"] for d in config.datasets] == ["DS0002", "DS0003", "DS0004", "DS0005"]
    ds3 = config.datasets[1]
    assert config.relation(ds3, "stylegan", "fake") == "related"
    assert config.relation(ds3, "none", "real") == "real"
    assert config.relation(config.datasets[0], "stable_diffusion", "fake") == "seen"
    assert config.relation(config.datasets[0], "Midjourney", "fake") == "unseen"


@pytest.mark.parametrize(
    "mutate, match",
    [
        (lambda r: r["datasets"].append(dict(r["datasets"][0])), "duplicate"),
        (lambda r: r["datasets"][0].update(max_images=0), "max_images"),
        (lambda r: r["datasets"][0].update(relation={"x": "cousin"}), "relation"),
        (lambda r: r["datasets"][0].pop("assignments"), "missing"),
        (lambda r: r.pop("training_generators"), "training_generators"),
    ],
)
def test_bad_config_fails(tmp_path: Path, mutate, match) -> None:
    with pytest.raises(GeneralizationConfigError, match=match):
        load_config(_write_config(tmp_path, mutate))


def test_config_hash_ignores_line_endings(tmp_path: Path) -> None:
    text = CONFIG.read_bytes().replace(b"\r\n", b"\n")
    (tmp_path / "a.yaml").write_bytes(text)
    (tmp_path / "b.yaml").write_bytes(text.replace(b"\n", b"\r\n"))
    assert load_config(tmp_path / "a.yaml").sha256 == load_config(tmp_path / "b.yaml").sha256


def test_target_items_sample_is_fixed() -> None:
    from generalization.inference import target_items

    config = load_config(CONFIG)
    ds5 = config.datasets[3]
    a, b = target_items(config, ds5, REPO), target_items(config, ds5, REPO)
    assert len(a) == 10000 and a["id"].tolist() == b["id"].tolist()
    assert a["id"].is_unique and set(a["y_true"]) == {0}
    ds2 = target_items(config, config.datasets[0], REPO)
    assert len(ds2) == 7364 and set(ds2["y_true"]) == {1}


# --- inference loop ---------------------------------------------------------------

torch = pytest.importorskip("torch")


class StandIn(torch.nn.Module):
    def forward(self, x):
        m = x.mean(dim=(1, 2, 3))
        return torch.stack([m, -m], dim=1)


def _png(path: Path, value: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(value)
    Image.fromarray(np.clip(rng.normal(value, 20, (224, 224, 3)), 0, 255).astype(np.uint8), "RGB").save(path)


@pytest.fixture()
def tiny(tmp_path: Path):
    from robustness.config import CLEAN, Condition
    from robustness.inference import PerturbedImages, predict

    ref_root = tmp_path / "ref" / "DS0001_PP0001"
    ref_rows = []
    for i in range(4):
        rel = f"images/{'fake' if i < 2 else 'real'}/r{i}.png"
        _png(ref_root / rel, 40 + 50 * i)
        ref_rows.append({"split": "test", "id": f"h{i}", "y_true": int(i < 2), "processed_path": rel, "generator": "g1" if i < 2 else "none"})
    targets = {}
    for name, labels in (("TA", ["fake", "fake", "fake"]), ("TB", ["fake", "real", "real", "fake"])):
        mount = tmp_path / name.lower()
        rows = []
        for i, label in enumerate(labels):
            rel = f"images/{label}/{name}_{i}.png"
            _png(mount / "nested" / rel, 30 + 40 * i)  # layout differs from the configured root
            rows.append({"processed_path": rel, "partition": "test", "class_label": label,
                         "generator": "genX" if label == "fake" else "none", "content_hash": f"{name}{i}"})
        (tmp_path / f"{name}.csv").write_text(pd.DataFrame(rows).to_csv(index=False), encoding="utf-8")
        targets[name] = mount

    def mutate(raw):
        raw["reference"]["predictions"] = "ref.csv"
        raw["inference"].update(batch_size=2, num_workers=0, sanity_images=4)
        raw["datasets"] = [
            {"name": n, "description": n, "assignments": f"{n}.csv", "partition": "test",
             "processed_root": str(m / "WRONG"), "max_images": None} for n, m in targets.items()
        ]

    config = load_config(_write_config(tmp_path, mutate))
    ref = pd.DataFrame(ref_rows)
    clean = Condition(CLEAN, CLEAN, CLEAN, None, 0)
    probs = predict(StandIn(), PerturbedImages(ref_root, ref, clean, config), 0, 2, 0, "cpu")
    threshold = float(np.median(probs))
    ref.assign(y_prob=probs, threshold=threshold, y_pred=(probs >= threshold).astype(int)).to_csv(tmp_path / "ref.csv", index=False)
    return tmp_path, config, ref_root


def test_run_finds_roots_and_resumes(tiny) -> None:
    from generalization.inference import MANIFEST_NAME, run

    tmp, config, ref_root = tiny
    logs: list[str] = []
    results = run(config, tmp, StandIn(), ["fake", "real"], tmp / "out", ref_root, device="cpu", log=logs.append)
    assert set(results) == {"TA", "TB"} and len(results["TB"]) == 4
    manifest = json.loads((tmp / "out" / MANIFEST_NAME).read_text(encoding="utf-8"))
    assert manifest["sanity_check"]["max_abs_diff"] < 1e-5
    assert manifest["processed_roots"]["TA"].endswith("nested")
    logs.clear()
    run(config, tmp, StandIn(), ["fake", "real"], tmp / "out", ref_root, device="cpu", log=logs.append)
    assert sum("reused" in line for line in logs) == 2


def test_sanity_mismatch_stops(tiny) -> None:
    from generalization.inference import run
    from robustness.inference import CleanCheckError

    tmp, config, ref_root = tiny
    ref = pd.read_csv(tmp / "ref.csv")
    ref.assign(y_prob=ref["y_prob"] * 0.5).to_csv(tmp / "ref.csv", index=False)
    with pytest.raises(CleanCheckError):
        run(config, tmp, StandIn(), ["fake", "real"], tmp / "out", ref_root, device="cpu", log=lambda _: None)
    assert not (tmp / "out" / "predictions" / "TA.csv").exists()


# --- E8 analysis --------------------------------------------------------------------


def test_cross_dataset_analysis() -> None:
    from generalization.cross_dataset import dataset_frame, frozen_threshold, group_frame, reference_frame, relation_frame
    from generalization.inference import target_items
    from generalization.report import render_cross_dataset

    config = load_config(CONFIG)
    rng = np.random.default_rng(0)
    frames = {}
    for d in config.datasets:
        items = target_items(config, d, REPO).drop(columns="processed_path")
        frames[d["name"]] = items.assign(y_prob=np.clip(0.3 * items["y_true"] + rng.uniform(0, 0.7, len(items)), 0, 1))
    threshold = frozen_threshold(config, REPO)
    reference = reference_frame(config, REPO)
    datasets = dataset_frame(frames, threshold, reference).set_index("dataset")
    stored = pd.read_csv(REPO / "08_Evaluation/EVAL0001/classification_metrics.csv").set_index("split").loc["test"]
    assert datasets.loc["DS0001", "balanced_accuracy"] == pytest.approx(stored["balanced_accuracy"])
    assert np.isnan(datasets.loc["DS0002", "roc_auc"]) and not np.isnan(datasets.loc["DS0002", "recall"])
    assert np.isnan(datasets.loc["DS0005", "recall"]) and not np.isnan(datasets.loc["DS0005", "fpr"])
    assert not np.isnan(datasets.loc["DS0003", "roc_auc"])
    groups = group_frame(frames, threshold, reference, config)
    assert set(groups["relation"]) <= {"seen", "related", "unseen", "real"}
    assert groups.groupby("dataset")["n"].sum().to_dict()["DS0005"] == 10000
    relations = relation_frame(groups)
    assert relations["n"].sum() == sum(int(f["y_true"].sum()) for f in frames.values())
    manifest = {"evaluation_id": "EVAL0001", "model_id": "MODEL0001", "export_sha256": "a" * 64, "config": "config.yaml",
                "config_sha256": config.sha256, "sanity_check": {"images": 500, "max_abs_diff": 1e-6, "atol": 0.001}}
    report = render_cross_dataset(datasets.reset_index(), groups, relations, manifest, config.raw, "2026-11-10")
    for name in ("DS0001", "DS0002", "DS0003", "DS0004", "DS0005"):
        assert f"| {name} |" in report


# --- E9 analysis --------------------------------------------------------------------


def test_leakage_check() -> None:
    from generalization.unseen import GeneratorLeakageError, check_no_leakage, held_out_generators

    split_dir = REPO / "03_Datasets/splits/DS0001_PP0001_SPLIT0002"
    held = held_out_generators(split_dir)
    assert held == ["stable_diffusion"]
    assignments = pd.read_csv(split_dir / "assignments.csv", dtype=str, keep_default_na=False)
    result = check_no_leakage(assignments, held)
    assert result["test_only_held_out_fakes"] and "stable_diffusion" not in result["train_generators"]
    leaky = assignments.copy()
    leaky.loc[leaky.index[0], "generator"] = "stable_diffusion"
    leaky.loc[leaky.index[0], "partition"] = "train"
    with pytest.raises(GeneratorLeakageError):
        check_no_leakage(leaky, held)


def test_unseen_analysis_on_synthetic_predictions(tmp_path: Path) -> None:
    from generalization.report import render_unseen
    from generalization.unseen import check_no_leakage, detection_frame, load_predictions, paired_frame, ranking_auc

    split_dir = REPO / "03_Datasets/splits/DS0001_PP0001_SPLIT0002"
    a = pd.read_csv(split_dir / "assignments.csv", dtype=str, keep_default_na=False)
    rng = np.random.default_rng(1)
    rows = []
    for part in ("val", "test"):
        s = a[a["partition"] == part]
        y = (s["class_label"] == "fake").astype(int).to_numpy()
        held = (s["generator"] == "stable_diffusion").to_numpy()
        p = np.clip(np.where(y == 1, np.where(held, 0.45, 0.8), 0.2) + rng.normal(0, 0.15, len(s)), 0, 1)
        rows.append(pd.DataFrame({"split": part, "id": s["content_hash"], "y_true": y, "y_prob": p, "y_pred": (p >= 0.5).astype(int),
                                  "threshold": 0.5, "processed_path": s["processed_path"], "generator": s["generator"]}))
    pd.concat(rows).to_csv(tmp_path / "predictions.csv", index=False)
    val, test = load_predictions(tmp_path / "predictions.csv")
    detection = detection_frame(val, test, ["stable_diffusion"]).set_index("group")
    assert detection.loc["stable_diffusion", "role"] == "unseen (test)" and detection.loc["stable_diffusion", "n"] == 1923
    assert detection.loc["stable_diffusion", "rate"] < detection.loc["all seen generators", "rate"]
    reference = pd.read_csv(REPO / "08_Evaluation/EXP0001/predictions.csv")
    paired = paired_frame(test, reference[reference["split"] == "test"], ["stable_diffusion"])
    assert paired["n"].iloc[0] == 299
    row = paired.iloc[0]
    assert row["both_detected"] + row["only_reference"] + row["only_held_out"] + row["neither"] == 299
    auc = ranking_auc(val, test, ["stable_diffusion"])
    assert 0.5 < auc < 1
    leakage = check_no_leakage(a, ["stable_diffusion"])
    info = {"evaluation_id": "EVAL0002", "experiment_id": "EXP0002", "model_id": "MODEL0008", "split": "DS0001_PP0001_SPLIT0002",
            "threshold": 0.5, "source": "08_Evaluation/EXP0002/predictions.csv", "reference_name": "MODEL0001 (EXP0001)"}
    report = render_unseen(detection.reset_index(), paired, leakage, auc, info, "2026-11-10")
    assert "Leakage check PASS" in report and "| stable_diffusion |" in report and "DEC0007" in report
