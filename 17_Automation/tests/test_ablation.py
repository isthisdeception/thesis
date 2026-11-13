"""STEP-048 ablations: plan, one-factor check, scaffolding, comparison."""

from __future__ import annotations

import copy
import csv
import json
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

from ablation import IDENTITY_KEYS, AblationPlanError, changed_keys, check_one_factor, load_plan
from config_validation import validate_config
from config_validation.registries import load_registries

REPO = Path(__file__).resolve().parents[2]
PLAN = REPO / "06_Experiments/ablations/STEP048_plan.yaml"
BASE = yaml.safe_load((REPO / "06_Experiments/EXP0001/config.yaml").read_text(encoding="utf-8"))
REGISTRIES = ["06_Experiments/experiment_registry.csv", "05_Models/model_registry.csv",
              "03_Datasets/metadata/dataset_registry.csv", "08_Evaluation/evaluation_registry.csv"]


def _plan_file(tmp_path: Path, mutate) -> Path:
    raw = yaml.safe_load(PLAN.read_text(encoding="utf-8"))
    mutate(raw)
    path = tmp_path / "plan.yaml"
    path.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")
    return path


def test_repo_plan_loads() -> None:
    plan = load_plan(PLAN)
    assert [a.experiment_id for a in plan.ablations] == ["EXP0003", "EXP0004", "EXP0005", "EXP0006"]
    assert plan.noise_reference == "EXP0003" and plan.artifact_slug("EXP0004") == "isthisdeception/thesis-exp0004-artifacts"


@pytest.mark.parametrize(
    "mutate, match",
    [
        (lambda r: r["ablations"][1].update(experiment_id="EXP0003"), "used twice"),
        (lambda r: r["ablations"][1].update(model_id="MODEL1"), "does not match"),
        (lambda r: r["ablations"][1].update(changes={"git_commit": "abc"}), "identity"),
        (lambda r: r["ablations"][1].update(changes={}), "non-empty"),
        (lambda r: r.update(noise_reference="EXP0099"), "noise_reference"),
    ],
)
def test_bad_plan_fails(tmp_path: Path, mutate, match) -> None:
    with pytest.raises(AblationPlanError, match=match):
        load_plan(_plan_file(tmp_path, mutate))


def test_every_config_changes_one_factor_and_validates() -> None:
    from ablation.scaffold import build_config

    plan = load_plan(PLAN)
    registries = load_registries(REPO)
    for a in plan.ablations:
        config = build_config(BASE, plan, a, "0" * 40, "2026-11-13T10:00:00+06:00")
        assert changed_keys(BASE, config) - IDENTITY_KEYS == set(a.changes)
        report = validate_config(config, registries=registries)
        assert report.ok, report.errors
        generated = yaml.safe_load((REPO / "06_Experiments" / a.experiment_id / "config.yaml").read_text(encoding="utf-8"))
        assert changed_keys(BASE, generated) - IDENTITY_KEYS == set(a.changes)


def test_extra_change_is_rejected() -> None:
    from ablation.scaffold import build_config

    plan = load_plan(PLAN)
    a = plan.ablations[1]
    config = build_config(BASE, plan, a, "0" * 40, "2026-11-13T10:00:00+06:00")
    config["batch_size"] = 32
    with pytest.raises(AblationPlanError, match="more than its factor"):
        check_one_factor(BASE, config, a)


def test_create_is_complete_and_never_overwrites(tmp_path: Path) -> None:
    from ablation.scaffold import create

    plan = load_plan(PLAN)
    planned = {x for a in plan.ablations for x in (a.experiment_id, a.model_id, a.evaluation_id)}
    for rel in REGISTRIES:
        rows = [r for r in csv.reader((REPO / rel).open(encoding="utf-8", newline="")) if not planned & {c.strip() for c in r}]
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        with (tmp_path / rel).open("w", encoding="utf-8", newline="") as f:
            csv.writer(f, lineterminator="\n").writerows(rows)
    (tmp_path / "06_Experiments/EXP0001").mkdir(parents=True, exist_ok=True)
    shutil.copy(REPO / "06_Experiments/EXP0001/config.yaml", tmp_path / "06_Experiments/EXP0001/config.yaml")
    (tmp_path / "17_Automation/kaggle_sync").mkdir(parents=True)
    first = create(tmp_path, plan, "0" * 40, "2026-11-13T10:00:00+06:00")
    assert all("experiment folder" in w and "evaluation" in w for w in first.values())
    for a in plan.ablations:
        exp = tmp_path / "06_Experiments" / a.experiment_id
        assert (exp / "config.yaml").is_file() and (exp / "metrics/.gitkeep").is_file()
        sync = yaml.safe_load((tmp_path / f"17_Automation/kaggle_sync/sync_plan.{a.experiment_id.lower()}.yaml").read_text(encoding="utf-8"))
        assert sync["publish_targets"][0]["dataset_slug"] == plan.artifact_slug(a.experiment_id)
    combined = yaml.safe_load((tmp_path / "17_Automation/kaggle_sync/sync_plan.ablations.yaml").read_text(encoding="utf-8"))
    assert len(combined["metadata_paths"]) == 6 * len(plan.ablations) and "publish_targets" not in combined
    for rel in REGISTRIES:
        rows = list(csv.reader((tmp_path / rel).open(encoding="utf-8")))
        assert len({len(r) for r in rows}) == 1
    before = (tmp_path / "06_Experiments/EXP0004/config.yaml").read_bytes()
    second = create(tmp_path, plan, "1" * 40, "2026-11-14T10:00:00+06:00")
    assert all(w == [] for w in second.values())
    assert (tmp_path / "06_Experiments/EXP0004/config.yaml").read_bytes() == before


def test_comparison_uses_seed_noise(tmp_path: Path) -> None:
    from ablation.compare import comparison_frame
    from ablation.report import render_report

    plan = load_plan(PLAN)
    src = pd.read_csv(REPO / "08_Evaluation/EXP0001/predictions.csv")
    rng = np.random.default_rng(0)
    shifts = {"EXP0001": 0.0, "EXP0003": 0.01, "EXP0004": 0.02, "EXP0005": 0.25, "EXP0006": 0.0}
    for exp, noise in shifts.items():
        p = np.clip(src["y_prob"] + rng.normal(0, noise, len(src)) if noise else src["y_prob"], 0, 1)
        frame = src.assign(y_prob=p, y_pred=(p >= src["threshold"]).astype(int))
        (tmp_path / "08_Evaluation" / exp).mkdir(parents=True)
        frame.to_csv(tmp_path / "08_Evaluation" / exp / "predictions.csv", index=False)
        (tmp_path / "06_Experiments" / exp / "metrics").mkdir(parents=True)
        (tmp_path / "06_Experiments" / exp / "metrics/run_summary.json").write_text(
            json.dumps({"best_epoch": 7, "training_seconds": 2200.0, "early_stopped": False}), encoding="utf-8")
    frame = comparison_frame(tmp_path, plan).set_index("experiment_id")
    assert frame.loc["EXP0001", "delta_roc_auc"] == 0
    assert frame.loc["EXP0006", "delta_roc_auc"] == 0 and frame.loc["EXP0006", "beyond_seed_roc_auc"] is False
    assert frame.loc["EXP0005", "delta_roc_auc"] < frame.loc["EXP0003", "delta_roc_auc"] and frame.loc["EXP0005", "beyond_seed_roc_auc"]
    assert frame.loc["EXP0003", "beyond_seed_roc_auc"] is None
    report = render_report(frame.reset_index(), plan, "2026-11-13")
    for a in plan.ablations:
        assert f"| {a.experiment_id} |" in report
    assert "(noise)" in report and "seed replicate" in report
