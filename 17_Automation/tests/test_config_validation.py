"""Tests for STEP-034 config.yaml validation."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from config_validation import (
    ConfigValidationError,
    load_registries,
    validate_config,
    validate_config_file,
)
from config_validation.__main__ import main

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "18_Templates" / "config.yaml"


@pytest.fixture(scope="module")
def registries():
    return load_registries(REPO_ROOT)


@pytest.fixture()
def ready_config() -> dict:
    """The template filled in as a training-ready EXP0001 config."""

    config = yaml.safe_load(TEMPLATE.read_text(encoding="utf-8"))
    config["experiment_id"] = "EXP0001"
    config["outputs"]["experiment_dir"] = "06_Experiments/EXP0001"
    config["outputs"]["checkpoint_dir"] = "06_Experiments/EXP0001/notebook/checkpoints"
    config["outputs"]["checkpoint_manifest"] = "07_Checkpoints/EXP0001_checkpoints.md"
    config["git_commit"] = "70850ff"
    config["timestamp"] = "2026-11-07T10:00:00+06:00"
    return config


def _errors(config: dict, registries, **kwargs) -> list[str]:
    return validate_config(config, repo_root=REPO_ROOT, registries=registries, **kwargs).errors


def _assert_error(errors: list[str], fragment: str) -> None:
    assert any(fragment in error for error in errors), f"expected {fragment!r} in {errors}"


def test_template_passes_in_template_mode() -> None:
    report = validate_config_file(TEMPLATE, template=True)
    assert report.ok, report.errors


def test_template_fails_in_ready_mode() -> None:
    errors = validate_config_file(TEMPLATE).errors
    _assert_error(errors, "experiment_id must match EXP####")
    _assert_error(errors, "git_commit is unset")
    _assert_error(errors, "timestamp is unset")


def test_ready_config_passes(ready_config, registries) -> None:
    assert _errors(ready_config, registries) == []


@pytest.mark.parametrize(
    "section",
    ["experiment_id", "dataset", "split", "model", "fastai", "optimizer", "learning_rate",
     "loss_function", "metrics", "random_seed", "augmentations", "hardware", "git_commit",
     "timestamp", "research_question", "purpose", "expected_outcome", "image_size",
     "batch_size", "epochs"],
)
def test_missing_m4_section_fails(ready_config, registries, section) -> None:
    del ready_config[section]
    _assert_error(_errors(ready_config, registries), f"missing required section '{section}'")


def test_missing_nested_field_fails(ready_config, registries) -> None:
    del ready_config["dataset"]["version"]
    _assert_error(_errors(ready_config, registries), "missing required field 'dataset.version'")


@pytest.mark.parametrize("seed", [None, "42", -1, True])
def test_unset_or_invalid_seed_fails(ready_config, registries, seed) -> None:
    ready_config["random_seed"] = seed
    _assert_error(_errors(ready_config, registries), "random_seed")


def test_unknown_dataset_id_fails(ready_config, registries) -> None:
    ready_config["dataset"]["dataset_id"] = "DS0099"
    ready_config["dataset"]["output_id"] = "DS0099_PP0001"
    ready_config["split"]["assignments_csv"] = "03_Datasets/splits/DS0099_PP0001_SPLIT0001/assignments.csv"
    _assert_error(_errors(ready_config, registries), "DS0099 not found")


def test_unknown_dataset_version_fails(ready_config, registries) -> None:
    ready_config["dataset"]["version"] = "v9.9"
    _assert_error(_errors(ready_config, registries), "dataset version DS0001/v9.9 not found")


def test_unknown_pipeline_id_fails(ready_config, registries) -> None:
    ready_config["dataset"]["pipeline_id"] = "PP0099"
    ready_config["dataset"]["output_id"] = "DS0001_PP0099"
    ready_config["split"]["assignments_csv"] = "03_Datasets/splits/DS0001_PP0099_SPLIT0001/assignments.csv"
    _assert_error(_errors(ready_config, registries), "PP0099 not found")


def test_superseded_pipeline_fails(ready_config, registries) -> None:
    ready_config["dataset"].update(dataset_id="DS0004", pipeline_id="PP0004", output_id="DS0004_PP0004")
    ready_config["split"]["assignments_csv"] = "03_Datasets/splits/DS0004_PP0004_SPLIT0001/assignments.csv"
    _assert_error(_errors(ready_config, registries), "only 'complete' pipelines may train")


def test_pipeline_from_other_dataset_fails(ready_config, registries) -> None:
    ready_config["dataset"].update(pipeline_id="PP0003", output_id="DS0001_PP0003")
    ready_config["split"]["assignments_csv"] = "03_Datasets/splits/DS0001_PP0003_SPLIT0001/assignments.csv"
    _assert_error(_errors(ready_config, registries), "pipeline PP0003 belongs to DS0003")


def test_unknown_split_id_fails(ready_config, registries) -> None:
    ready_config["split"]["split_id"] = "SPLIT0099"
    ready_config["split"]["assignments_csv"] = "03_Datasets/splits/DS0001_PP0001_SPLIT0099/assignments.csv"
    _assert_error(_errors(ready_config, registries), "split SPLIT0099 for output DS0001_PP0001 not found")


def test_split_scheme_mismatch_fails(ready_config, registries) -> None:
    ready_config["split"]["scheme"] = "logo"
    _assert_error(_errors(ready_config, registries), "does not match registry scheme")


def test_unknown_model_id_fails(ready_config, registries) -> None:
    ready_config["model"]["model_id"] = "MODEL0099"
    _assert_error(_errors(ready_config, registries), "MODEL0099 not found")


def test_model_architecture_mismatch_fails(ready_config, registries) -> None:
    ready_config["model"]["architecture"] = "Xception"
    _assert_error(_errors(ready_config, registries), "does not match registry architecture 'ResNet-50'")


def test_image_size_must_match_resize(ready_config, registries) -> None:
    ready_config["image_size"] = 299
    _assert_error(_errors(ready_config, registries), "must equal image_size")


def test_string_learning_rate_fails_with_hint(ready_config, registries) -> None:
    ready_config["learning_rate"]["value"] = "1e-3"
    _assert_error(_errors(ready_config, registries), "write 1.0e-3")


def test_missing_canonical_metric_fails(ready_config, registries) -> None:
    ready_config["metrics"]["primary"].remove("mcc")
    _assert_error(_errors(ready_config, registries), "missing canonical metric(s): mcc")


def test_bad_git_commit_fails(ready_config, registries) -> None:
    ready_config["git_commit"] = "not-a-sha"
    _assert_error(_errors(ready_config, registries), "git_commit must be a 7-40 character hex SHA")


def test_naive_timestamp_fails(ready_config, registries) -> None:
    ready_config["timestamp"] = "2026-11-07T10:00:00"
    _assert_error(_errors(ready_config, registries), "timestamp must include a timezone offset")


def test_experiment_dir_must_match_id(ready_config, registries) -> None:
    ready_config["outputs"]["experiment_dir"] = "06_Experiments/EXP0002"
    _assert_error(_errors(ready_config, registries), "outputs.experiment_dir must be '06_Experiments/EXP0001'")


def test_structure_checks_run_without_registries(ready_config) -> None:
    config = copy.deepcopy(ready_config)
    config["model"]["model_id"] = "MODEL0099"
    assert validate_config(config).ok


def test_non_mapping_config_fails() -> None:
    report = validate_config(["not", "a", "mapping"])
    assert not report.ok
    with pytest.raises(ConfigValidationError, match="must be a YAML mapping"):
        report.raise_if_failed()


def test_invalid_yaml_fails(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    path.write_text("experiment_id: [unclosed\n", encoding="utf-8")
    report = validate_config_file(path, repo_root=REPO_ROOT)
    _assert_error(report.errors, "YAML does not parse")


def test_cli_exit_codes(tmp_path: Path, ready_config, capsys) -> None:
    good = tmp_path / "good.yaml"
    good.write_text(yaml.safe_dump(ready_config), encoding="utf-8")
    bad_config = copy.deepcopy(ready_config)
    bad_config["random_seed"] = None
    bad = tmp_path / "bad.yaml"
    bad.write_text(yaml.safe_dump(bad_config), encoding="utf-8")

    assert main([str(good), "--repo-root", str(REPO_ROOT)]) == 0
    assert main([str(bad), "--repo-root", str(REPO_ROOT)]) == 1
    assert "random_seed is unset" in capsys.readouterr().out
