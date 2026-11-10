"""E1–E2 checks. Every failure is reported. No metrics are computed."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import yaml

POSITIVE_CLASS = "fake"
NEGATIVE_CLASS = "real"
PROBABILITY_EDGE = 1e-5


@dataclass(frozen=True)
class Check:
    phase: str
    name: str
    passed: bool
    detail: str


class PredictionValidationError(ValueError):
    """One or more E1/E2 checks failed."""

    def __init__(self, checks: list[Check]) -> None:
        self.checks = checks
        failed = [c for c in checks if not c.passed]
        lines = "\n".join(f"  - {c.phase} {c.name}: {c.detail}" for c in failed)
        super().__init__(f"prediction validation failed ({len(failed)} check(s)):\n{lines}")


def _sha256(path: Path, *, normalize_newlines: bool) -> str:
    """Hash file bytes.

    ``normalize_newlines`` compares a Windows CRLF checkout with a hash that
    was recorded from an LF file, which is the case for ``config.yaml``.
    Prediction CSVs are hashed exactly as stored, because their manifest hash
    was computed from those bytes.
    """

    data = path.read_bytes()
    if normalize_newlines:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [{(k or "").strip(): (v or "").strip() for k, v in row.items()} for row in csv.DictReader(handle)]


def _add(checks: list[Check], phase: str, name: str, passed: bool, detail: str) -> None:
    checks.append(Check(phase, name, passed, detail))


def _experiment_config(repo: Path, experiment_id: str) -> dict:
    path = repo / "06_Experiments" / experiment_id / "config.yaml"
    return (yaml.safe_load(path.read_text(encoding="utf-8")) or {}) if path.is_file() else {}


def check_registration(repo: Path, experiment_id: str, evaluation_id: str) -> list[Check]:
    """Phase E1. An incomplete experiment is rejected."""

    checks: list[Check] = []
    experiments = _read_csv(repo / "06_Experiments" / "experiment_registry.csv")
    exp = next((r for r in experiments if r.get("Experiment ID") == experiment_id), None)
    _add(checks, "E1", "experiment registered", exp is not None and exp.get("Status") == "completed",
         "missing" if exp is None else f"status={exp.get('Status')}")

    models = _read_csv(repo / "05_Models" / "model_registry.csv")
    model = next((r for r in models if r.get("Experiment") == experiment_id), None)
    exported = bool(model and model.get("Export Path") and model.get("Git Commit") and model.get("Status") == "trained")
    _add(checks, "E1", "model exported and registered", exported,
         "missing" if model is None else f"status={model.get('Status')}, export={model.get('Export Path') or 'empty'}")

    datasets = _read_csv(repo / "03_Datasets" / "metadata" / "dataset_registry.csv")
    linked = [
        r for r in datasets
        if r.get("Experiment ID") == experiment_id and r.get("Model ID") == (model or {}).get("Model ID")
    ]
    _add(checks, "E1", "dataset and split linked", len(linked) == 1 and linked[0].get("Status") == "ready",
         "no linked row" if not linked else f"{linked[0].get('Split ID')} status={linked[0].get('Status')}")

    config = repo / "06_Experiments" / experiment_id / "config.yaml"
    summary_path = repo / "06_Experiments" / experiment_id / "metrics" / "run_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.is_file() else {}
    config_ok = config.is_file() and summary.get("status") == "complete" and summary.get("config_sha256") == _sha256(config, normalize_newlines=True)
    _add(
        checks, "E1", "config archived", config_ok,
        "SHA-256 matches run_summary.json" if config_ok else "config missing or its SHA-256 differs from run_summary.json",
    )

    manifest = repo / "07_Checkpoints" / f"{experiment_id}_checkpoints.md"
    text = manifest.read_text(encoding="utf-8") if manifest.is_file() else ""
    model_id = (_experiment_config(repo, experiment_id).get("model") or {}).get("model_id", "")
    _add(checks, "E1", "checkpoint and export archived",
         bool(model_id) and f"{model_id}_export.pkl" in text and f"{experiment_id}_best.pth" in text,
         manifest.name if manifest.is_file() else "manifest missing")

    git_ok = bool(summary.get("git", {}).get("recorded")) and bool(model and model.get("Git Commit"))
    _add(checks, "E1", "git commit recorded", git_ok, str(summary.get("git", {}).get("recorded") or "missing"))

    evaluations = _read_csv(repo / "08_Evaluation" / "evaluation_registry.csv") if (repo / "08_Evaluation" / "evaluation_registry.csv").is_file() else []
    reserved = any(r.get("Evaluation ID") == evaluation_id and r.get("Experiment") == experiment_id for r in evaluations)
    _add(checks, "E1", "evaluation id reserved", reserved and re.fullmatch(r"EVAL\d{4}", evaluation_id) is not None,
         evaluation_id if reserved else f"{evaluation_id} not in evaluation_registry.csv for {experiment_id}")
    return checks


def check_predictions(repo: Path, experiment_id: str, positive_class: str = POSITIVE_CLASS) -> list[Check]:
    """Phase E2. Counts, ids, labels, probabilities, and file hashes."""

    checks: list[Check] = []
    manifest_path = repo / "08_Evaluation" / experiment_id / "manifest.json"
    predictions_path = repo / "08_Evaluation" / experiment_id / "predictions.csv"
    if not manifest_path.is_file() or not predictions_path.is_file():
        _add(checks, "E2", "prediction files present", False, "manifest.json or predictions.csv missing")
        return checks
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    predictions = pd.read_csv(predictions_path)
    _add(checks, "E2", "prediction files present", True, f"{len(predictions)} rows")

    hash_ok = True
    for split, source in manifest.get("sources", {}).items():
        path = repo / source["path"]
        actual = _sha256(path, normalize_newlines=False) if path.is_file() else ""
        if actual != source.get("sha256"):
            hash_ok = False
    _add(checks, "E2", "source file integrity", hash_ok, "SHA-256 matches the manifest" if hash_ok else "a source prediction file was modified")

    required = {"split", "id", "y_true", "y_prob", "y_pred", "processed_path"}
    _add(checks, "E2", "prediction columns", required <= set(predictions.columns), ", ".join(sorted(required - set(predictions.columns))) or "present")
    if not required <= set(predictions.columns):
        return checks

    duplicates = int(predictions.duplicated(["split", "id"]).sum())
    _add(checks, "E2", "no duplicate ids", duplicates == 0, f"{duplicates} duplicate id(s)")

    probs = predictions["y_prob"]
    prob_ok = probs.notna().all() and probs.between(0.0, 1.0).all()
    _add(checks, "E2", "probabilities in [0, 1]", bool(prob_ok), "all in range" if prob_ok else "a probability is missing or outside [0, 1]")

    labels_ok = set(predictions["y_true"].unique()).issubset({0, 1})
    _add(checks, "E2", "class labels binary", bool(labels_ok), "y_true is 0/1" if labels_ok else "unexpected y_true")

    relative = (_experiment_config(repo, experiment_id).get("split") or {}).get("assignments_csv")
    assignments_path = repo / relative if relative else None
    if assignments_path is None or not assignments_path.is_file():
        _add(checks, "E2", "ground truth present", False, f"missing {relative or 'split.assignments_csv in the experiment config'}")
        return checks
    assignments = pd.read_csv(assignments_path, dtype=str)
    for split in ("val", "test"):
        predicted = predictions[predictions["split"] == split]
        truth = assignments[assignments["partition"] == split]
        predicted_ids = set(predicted["id"].astype(str))
        truth_ids = set(truth["content_hash"].astype(str))
        missing = truth_ids - predicted_ids
        extra = predicted_ids - truth_ids
        _add(checks, "E2", f"{split} count", len(predicted) == len(truth) and not missing and not extra,
             f"predictions={len(predicted)} ground_truth={len(truth)} missing={len(missing)} extra={len(extra)}")
        merged = predicted.merge(truth, left_on="id", right_on="content_hash", how="inner")
        if merged.empty:
            _add(checks, "E2", f"{split} labels", False, "no ids aligned")
            continue
        expected_true = (merged["class_label"] == positive_class).astype(int)
        label_mismatch = int((merged["y_true"].astype(int) != expected_true).sum())
        path_mismatch = int((merged["processed_path_x"] != merged["processed_path_y"]).sum())
        _add(checks, "E2", f"{split} labels and paths", label_mismatch == 0 and path_mismatch == 0,
             f"label mismatches={label_mismatch}, path mismatches={path_mismatch}")
    return checks


def validate(repo: Path, experiment_id: str = "EXP0001", evaluation_id: str = "EVAL0001") -> list[Check]:
    checks = check_registration(repo, experiment_id, evaluation_id) + check_predictions(repo, experiment_id)
    return checks


def render_report(checks: list[Check], evaluation_id: str, experiment_id: str) -> str:
    failed = [c for c in checks if not c.passed]
    status = "PASS" if not failed else "FAIL"
    rows = "\n".join(f"| {c.phase} | {c.name} | {'PASS' if c.passed else 'FAIL'} | {c.detail} |" for c in checks)
    closing = "No metrics were computed. STEP-043 may use these predictions." if not failed else "Do not compute metrics. Return to STEP-041 and regenerate the inputs."
    return "\n".join([
        f"# Prediction Validation: {evaluation_id}",
        "",
        f"**Experiment:** {experiment_id}",
        f"**Status:** {status}",
        "**Date:** 2026-11-09",
        "",
        "Phases E1 and E2 only. This report does not recompute ROC-AUC or any other metric.",
        "",
        "| Phase | Check | Result | Detail |",
        "|-------|-------|--------|--------|",
        rows,
        "",
        closing,
        "",
    ])


def write_report(repo: Path, evaluation_id: str = "EVAL0001", experiment_id: str = "EXP0001") -> list[Check]:
    checks = validate(repo, experiment_id, evaluation_id)
    out = repo / "08_Evaluation" / evaluation_id
    out.mkdir(parents=True, exist_ok=True)
    (out / "prediction_validation_report.md").write_text(render_report(checks, evaluation_id, experiment_id), encoding="utf-8")
    failed = [c for c in checks if not c.passed]
    if failed:
        raise PredictionValidationError(checks)
    return checks
