"""Validate an experiment config.yaml against the Phase M4 schema and registries."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

from . import schema
from .registries import Registries, load_registries


class ConfigValidationError(ValueError):
    """Raised when a config fails validation; carries every failure found."""

    def __init__(self, path: str, errors: list[str]) -> None:
        self.path = path
        self.errors = list(errors)
        lines = "\n".join(f"  - {error}" for error in self.errors)
        super().__init__(f"config validation failed for {path} ({len(self.errors)} error(s)):\n{lines}")


@dataclass
class ValidationReport:
    path: str
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def raise_if_failed(self) -> None:
        if self.errors:
            raise ConfigValidationError(self.path, self.errors)


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _non_empty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _matches(pattern: str, value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(pattern, value) is not None


class _Checker:
    def __init__(self, config: dict, registries: Registries | None, repo_root: Path | None, template: bool):
        self.config = config
        self.registries = registries
        self.repo_root = repo_root
        self.template = template
        self.errors: list[str] = []

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def section(self, key: str) -> dict | None:
        value = self.config.get(key)
        return value if isinstance(value, dict) else None

    def run(self) -> list[str]:
        self.check_structure()
        self.check_identity()
        self.check_text()
        self.check_dataset_and_split()
        self.check_model()
        self.check_fastai_and_sizes()
        self.check_training_policy()
        self.check_metrics()
        self.check_seed()
        self.check_hardware_and_outputs()
        self.check_runtime_fields()
        if self.registries is not None:
            self.check_registries()
        return self.errors

    # --- structure ------------------------------------------------------------

    def check_structure(self) -> None:
        version = self.config.get("schema_version")
        if version != schema.SCHEMA_VERSION:
            self.fail(f"schema_version must be {schema.SCHEMA_VERSION}, got {version!r}")
        for key, label in schema.REQUIRED_SECTIONS.items():
            if key not in self.config:
                self.fail(f"missing required section '{key}' (M4: {label})")
        for key, subkeys in schema.REQUIRED_SUBKEYS.items():
            if key not in self.config:
                continue
            value = self.config[key]
            if not isinstance(value, dict):
                self.fail(f"section '{key}' must be a mapping, got {type(value).__name__}")
                continue
            for sub in subkeys:
                if sub not in value or value[sub] is None:
                    self.fail(f"missing required field '{key}.{sub}'")

    # --- identity / text ------------------------------------------------------

    def check_identity(self) -> None:
        exp_id = self.config.get("experiment_id")
        if exp_id is None:
            return
        if self.template and exp_id == schema.EXPERIMENT_PLACEHOLDER:
            return
        if not _matches(schema.ID_PATTERNS["experiment"], exp_id):
            self.fail(f"experiment_id must match EXP#### (e.g. EXP0001), got {exp_id!r}")

    def check_text(self) -> None:
        for key in schema.NON_EMPTY_TEXT:
            if key in self.config and not _non_empty_str(self.config[key]):
                self.fail(f"'{key}' must be a non-empty string")
        track = self.config.get("study_track")
        if track is not None and track not in schema.STUDY_TRACKS:
            self.fail(f"study_track must be one of {sorted(schema.STUDY_TRACKS)}, got {track!r}")

    # --- dataset / split ------------------------------------------------------

    def check_dataset_and_split(self) -> None:
        dataset = self.section("dataset")
        split = self.section("split")
        if dataset:
            ds_id, pp_id = dataset.get("dataset_id"), dataset.get("pipeline_id")
            if ds_id is not None and not _matches(schema.ID_PATTERNS["dataset"], ds_id):
                self.fail(f"dataset.dataset_id must match DS####, got {ds_id!r}")
            if pp_id is not None and not _matches(schema.ID_PATTERNS["pipeline"], pp_id):
                self.fail(f"dataset.pipeline_id must match PP####, got {pp_id!r}")
            output_id = dataset.get("output_id")
            if ds_id and pp_id and output_id is not None and output_id != f"{ds_id}_{pp_id}":
                self.fail(f"dataset.output_id must be '{ds_id}_{pp_id}', got {output_id!r}")
            vocab = dataset.get("vocab")
            if vocab is not None and (not isinstance(vocab, list) or len(vocab) < 2):
                self.fail("dataset.vocab must be a list with at least two class labels")
        if split:
            split_id = split.get("split_id")
            if split_id is not None and not _matches(schema.ID_PATTERNS["split"], split_id):
                self.fail(f"split.split_id must match SPLIT####, got {split_id!r}")
            leakage = split.get("leakage_required")
            if leakage is not None and str(leakage).upper() != "PASS":
                self.fail(f"split.leakage_required must be PASS, got {leakage!r}")
            if dataset and dataset.get("output_id") and split_id:
                expected = f"03_Datasets/splits/{dataset['output_id']}_{split_id}/assignments.csv"
                if split.get("assignments_csv") is not None and split["assignments_csv"] != expected:
                    self.fail(f"split.assignments_csv must be '{expected}', got {split['assignments_csv']!r}")

    # --- model ----------------------------------------------------------------

    def check_model(self) -> None:
        model = self.section("model")
        if not model:
            return
        model_id = model.get("model_id")
        if model_id is not None and not _matches(schema.ID_PATTERNS["model"], model_id):
            self.fail(f"model.model_id must match MODEL####, got {model_id!r}")
        source = model.get("source")
        if source is not None and source not in schema.MODEL_SOURCES:
            self.fail(f"model.source must be one of {sorted(schema.MODEL_SOURCES)}, got {source!r}")
        pretrained = model.get("pretrained")
        if pretrained is not None and not isinstance(pretrained, bool):
            self.fail(f"model.pretrained must be true or false, got {pretrained!r}")

    # --- FastAI / sizes -------------------------------------------------------

    def check_fastai_and_sizes(self) -> None:
        for key in ("image_size", "batch_size", "epochs"):
            if key in self.config:
                value = self.config[key]
                if not _is_int(value) or value <= 0:
                    self.fail(f"'{key}' must be a positive integer, got {value!r}")
        fastai = self.section("fastai")
        if not fastai:
            return
        item_tfms = fastai.get("item_tfms")
        image_size = self.config.get("image_size")
        if isinstance(item_tfms, dict) and _is_int(image_size):
            if item_tfms.get("resize") != image_size:
                self.fail(
                    f"fastai.item_tfms.resize ({item_tfms.get('resize')!r}) must equal image_size ({image_size})"
                )
        if "mixed_precision" in fastai and not isinstance(fastai["mixed_precision"], bool):
            self.fail("fastai.mixed_precision must be true or false")
        schedule = fastai.get("schedule")
        if isinstance(schedule, dict):
            method = schedule.get("method")
            if method not in schema.SCHEDULE_METHODS:
                self.fail(f"fastai.schedule.method must be one of {sorted(schema.SCHEDULE_METHODS)}, got {method!r}")
            freeze = schedule.get("freeze_epochs")
            if not _is_int(freeze) or freeze < 0:
                self.fail(f"fastai.schedule.freeze_epochs must be an integer >= 0, got {freeze!r}")
        elif "schedule" in fastai:
            self.fail("fastai.schedule must be a mapping")
        export = fastai.get("export")
        if isinstance(export, dict) and not (export.get("export_pkl") or export.get("weights_pth")):
            self.fail("fastai.export must enable export_pkl and/or weights_pth")

    # --- optimizer / LR / loss ------------------------------------------------

    def check_training_policy(self) -> None:
        optimizer = self.section("optimizer")
        if optimizer and "name" in optimizer and not _non_empty_str(optimizer["name"]):
            self.fail("optimizer.name must be a non-empty string")
        lr = self.section("learning_rate")
        if lr:
            value = lr.get("value")
            if value is not None:
                if isinstance(value, str):
                    self.fail(
                        f"learning_rate.value must be a number, got string {value!r} "
                        "(write 1.0e-3, not 1e-3, so YAML parses it as a float)"
                    )
                elif not _is_number(value) or value <= 0:
                    self.fail(f"learning_rate.value must be a positive number, got {value!r}")
            source = lr.get("source")
            if source is not None and source not in schema.LR_SOURCES:
                self.fail(f"learning_rate.source must be one of {sorted(schema.LR_SOURCES)}, got {source!r}")
        loss = self.section("loss_function")
        if loss and "name" in loss and not _non_empty_str(loss["name"]):
            self.fail("loss_function.name must be a non-empty string")

    # --- metrics --------------------------------------------------------------

    def check_metrics(self) -> None:
        metrics = self.section("metrics")
        if not metrics:
            return
        primary = metrics.get("primary")
        if primary is not None:
            if not isinstance(primary, list):
                self.fail("metrics.primary must be a list")
            else:
                missing = [m for m in schema.CANONICAL_PRIMARY_METRICS if m not in primary]
                if missing:
                    self.fail(f"metrics.primary is missing canonical metric(s): {', '.join(missing)}")
        policy = metrics.get("threshold_policy")
        if policy is not None and policy not in schema.THRESHOLD_POLICIES:
            self.fail(f"metrics.threshold_policy must be one of {sorted(schema.THRESHOLD_POLICIES)}, got {policy!r}")

    # --- seed -----------------------------------------------------------------

    def check_seed(self) -> None:
        if "random_seed" not in self.config:
            return
        seed = self.config["random_seed"]
        if seed is None:
            self.fail("random_seed is unset")
        elif not _is_int(seed) or seed < 0:
            self.fail(f"random_seed must be a non-negative integer, got {seed!r}")

    # --- hardware / outputs ---------------------------------------------------

    def check_hardware_and_outputs(self) -> None:
        hardware = self.section("hardware")
        if hardware:
            for key in ("platform", "accelerator", "gpu"):
                if key in hardware and not _non_empty_str(hardware[key]):
                    self.fail(f"hardware.{key} must be a non-empty string")
        outputs = self.section("outputs")
        exp_id = self.config.get("experiment_id")
        if outputs and isinstance(exp_id, str):
            exp_dir = outputs.get("experiment_dir")
            if exp_dir is not None and exp_dir != f"06_Experiments/{exp_id}":
                self.fail(f"outputs.experiment_dir must be '06_Experiments/{exp_id}', got {exp_dir!r}")
            ckpt_dir = outputs.get("checkpoint_dir")
            if isinstance(ckpt_dir, str) and exp_id not in ckpt_dir:
                self.fail(f"outputs.checkpoint_dir must be scoped to {exp_id}, got {ckpt_dir!r}")

    # --- runtime fields -------------------------------------------------------

    def check_runtime_fields(self) -> None:
        commit = self.config.get("git_commit")
        if "git_commit" in self.config:
            if commit is None:
                if not self.template:
                    self.fail("git_commit is unset; record the repo SHA before training")
            elif not _matches(schema.GIT_COMMIT_PATTERN, str(commit).lower()):
                self.fail(f"git_commit must be a 7-40 character hex SHA, got {commit!r}")
        if "timestamp" in self.config:
            stamp = self.config.get("timestamp")
            if stamp is None:
                if not self.template:
                    self.fail("timestamp is unset; record the ISO-8601 session time before training")
            else:
                self._check_timestamp(stamp)

    def _check_timestamp(self, stamp: Any) -> None:
        if isinstance(stamp, datetime):
            parsed = stamp
        elif isinstance(stamp, date):
            self.fail(f"timestamp must include a time and timezone, got date {stamp.isoformat()}")
            return
        else:
            try:
                parsed = datetime.fromisoformat(str(stamp))
            except ValueError:
                self.fail(f"timestamp must be ISO-8601, got {stamp!r}")
                return
        if parsed.tzinfo is None:
            self.fail(f"timestamp must include a timezone offset, got {stamp!r}")

    # --- registries -----------------------------------------------------------

    def check_registries(self) -> None:
        assert self.registries is not None
        dataset = self.section("dataset") or {}
        split = self.section("split") or {}
        model = self.section("model") or {}
        ds_id, version, pp_id = dataset.get("dataset_id"), dataset.get("version"), dataset.get("pipeline_id")
        output_id, split_id = dataset.get("output_id"), split.get("split_id")

        if ds_id:
            ds_rows = [r for r in self.registries.dataset if r.get("Dataset ID") == ds_id]
            if not ds_rows:
                self.fail(f"dataset.dataset_id {ds_id} not found in {schema.REGISTRY_PATHS['dataset']}")
            elif version and not any(r.get("Version") == str(version) for r in ds_rows):
                self.fail(f"dataset version {ds_id}/{version} not found in {schema.REGISTRY_PATHS['dataset']}")
            elif pp_id and output_id and split_id:
                full_split = f"{output_id}_{split_id}"
                combo = [
                    r
                    for r in ds_rows
                    if r.get("Version") == str(version)
                    and r.get("Preprocessing ID") == pp_id
                    and r.get("Split ID") == full_split
                ]
                if not combo:
                    self.fail(
                        f"dataset combination {ds_id}/{version}/{pp_id}/{full_split} is not registered in "
                        f"{schema.REGISTRY_PATHS['dataset']}"
                    )
                elif combo[0].get("Status", "").lower() != "ready":
                    self.fail(f"dataset combination {ds_id}/{version}/{pp_id}/{full_split} is not ready")

        if pp_id:
            pp_rows = [r for r in self.registries.preprocessing if r.get("Pipeline ID") == pp_id]
            if not pp_rows:
                self.fail(f"dataset.pipeline_id {pp_id} not found in {schema.REGISTRY_PATHS['preprocessing']}")
            else:
                row = pp_rows[0]
                if row.get("Status", "").lower() != "complete":
                    self.fail(f"pipeline {pp_id} has status {row.get('Status')!r}; only 'complete' pipelines may train")
                if ds_id and row.get("Dataset") != ds_id:
                    self.fail(f"pipeline {pp_id} belongs to {row.get('Dataset')}, not {ds_id}")

        if split_id and output_id:
            split_rows = [
                r
                for r in self.registries.split
                if r.get("Split ID") == split_id and r.get("Output ID") == output_id
            ]
            if not split_rows:
                self.fail(
                    f"split {split_id} for output {output_id} not found in {schema.REGISTRY_PATHS['split']}"
                )
            else:
                row = split_rows[0]
                if row.get("Leakage", "").upper() != "PASS":
                    self.fail(f"split {output_id}_{split_id} leakage check is {row.get('Leakage')!r}, not PASS")
                scheme = split.get("scheme")
                if scheme and row.get("Scheme") != scheme:
                    self.fail(f"split.scheme {scheme!r} does not match registry scheme {row.get('Scheme')!r}")

        assignments = split.get("assignments_csv")
        if self.repo_root is not None and isinstance(assignments, str):
            if not (self.repo_root / assignments).is_file():
                self.fail(f"split.assignments_csv not found: {assignments}")

        model_id = model.get("model_id")
        if model_id:
            rows = [r for r in self.registries.models() if r.get("Model ID") == model_id]
            if not rows:
                self.fail(
                    f"model.model_id {model_id} not found in {schema.REGISTRY_PATHS['model']} or "
                    f"{schema.REGISTRY_PATHS['candidate_models']}"
                )
            else:
                arch = model.get("architecture")
                registered = rows[0].get("Architecture")
                if arch and registered and arch != registered:
                    self.fail(f"model.architecture {arch!r} does not match registry architecture {registered!r}")


def find_repo_root(start: str | Path) -> Path:
    """Walk upward until the folder holding MASTER_RESEARCH_OPERATING_SYSTEM.md."""

    current = Path(start).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "MASTER_RESEARCH_OPERATING_SYSTEM.md").is_file():
            return candidate
    raise FileNotFoundError(f"could not locate repo root above {start}")


def validate_config(
    config: dict,
    *,
    repo_root: str | Path | None = None,
    registries: Registries | None = None,
    template: bool = False,
    path: str = "<config>",
) -> ValidationReport:
    """Return every validation failure for an already-parsed config mapping.

    Registry checks run when ``registries`` or ``repo_root`` is supplied.
    ``template=True`` allows the EXPxxxx placeholder and unset git_commit/timestamp.
    """

    if not isinstance(config, dict):
        return ValidationReport(path, [f"config must be a YAML mapping, got {type(config).__name__}"])
    root = Path(repo_root) if repo_root is not None else None
    if registries is None and root is not None:
        registries = load_registries(root)
    errors = _Checker(config, registries, root, template).run()
    return ValidationReport(path, errors)


def validate_config_file(
    path: str | Path,
    *,
    repo_root: str | Path | None = None,
    template: bool = False,
) -> ValidationReport:
    """Parse a config.yaml and validate it; the repo root is auto-detected if omitted."""

    source = Path(path)
    try:
        config = yaml.safe_load(source.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return ValidationReport(str(source), [f"YAML does not parse: {exc}"])
    root = Path(repo_root) if repo_root is not None else find_repo_root(source.parent)
    return validate_config(config, repo_root=root, template=template, path=str(source))
