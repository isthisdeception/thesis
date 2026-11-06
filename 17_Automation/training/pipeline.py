"""Phase M6 training workflow: config → data → train → checkpoints → metrics → curves → export → summary."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from . import evaluation
from .data import SplitFrames, build_dataloaders, load_assignments, validate_dataset
from .logs import close_run_logging, environment_info, get_logger, setup_run_logging, step
from .settings import TrainingConfigError, TrainingSettings, load_settings

# FastAI `Learner.fine_tune` semantics for the frozen phase and the unfreeze LR step.
FROZEN_PCT_START = 0.99
UNFREEZE_LR_DIVISOR = 2

LR_SUGGESTERS = ("valley", "minimum", "steep", "slide")


class OutputsExistError(FileExistsError):
    """The experiment already has training outputs; nothing is ever overwritten."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def _existing_outputs(settings: TrainingSettings) -> list[Path]:
    found: list[Path] = []
    for folder in (settings.checkpoint_dir, settings.metrics_dir, settings.predictions_dir, settings.curves_dir):
        if folder.is_dir():
            found.extend(p for p in folder.iterdir() if p.name != ".gitkeep")
    history = settings.logs_dir / "history.csv"
    if history.exists():
        found.append(history)
    return found


def guard_outputs(settings: TrainingSettings) -> None:
    existing = _existing_outputs(settings)
    if existing:
        listed = ", ".join(str(p.relative_to(settings.repo_root)) for p in existing[:5])
        raise OutputsExistError(
            f"{settings.experiment_id} already has training outputs ({listed}{', ...' if len(existing) > 5 else ''}). "
            "Outputs are never overwritten: resume belongs to the checkpoint system, and a changed rerun needs a new EXP ID."
        )


def check_git_provenance(settings: TrainingSettings) -> dict:
    """The config's git_commit must be HEAD or an ancestor of it (the config commit itself comes later)."""

    logger = get_logger()
    recorded = str(settings.get("git_commit"))
    try:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=settings.repo_root, check=True, capture_output=True, text=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        logger.warning("git unavailable; cannot verify git_commit %s (%s)", recorded, exc)
        return {"recorded": recorded, "head": None, "verified": False}
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", recorded, "HEAD"], cwd=settings.repo_root, capture_output=True
    )
    if ancestor.returncode != 0:
        raise TrainingConfigError(
            f"config git_commit {recorded} is not HEAD or an ancestor of HEAD ({head}); refresh it before training"
        )
    logger.info("git provenance: config commit %s is an ancestor of HEAD %s", recorded, head)
    return {"recorded": recorded, "head": head, "verified": True}


def check_export_picklable() -> None:
    """Fail before training if FastAI transforms cannot be pickled (export.pkl would fail at the end)."""

    import pickle
    from importlib.metadata import PackageNotFoundError, version

    from fastai.vision.all import PILImage, Transform

    try:
        pickle.dumps(Transform(PILImage.create))
    except Exception as exc:
        try:
            plum = version("plum-dispatch")
        except PackageNotFoundError:
            plum = "unknown"
        raise RuntimeError(
            f"FastAI transforms are not picklable here (plum-dispatch {plum}), so export.pkl would fail after "
            "training. Install plum-dispatch==2.5.7 (environment/requirements.txt) and restart the kernel."
        ) from exc


def prepare(settings: TrainingSettings):
    """Seed, validate data, and build DataLoaders + Learner (shared by training and LR Finder)."""

    import torch
    from fastai.torch_core import set_seed

    from .learner import build_learner

    logger = get_logger()
    with step("environment"):
        env = environment_info()
        logger.info("environment %s", env)
        if settings.get("fastai.mixed_precision") and not torch.cuda.is_available():
            raise RuntimeError("fastai.mixed_precision is true but CUDA is not available")
        if settings.get("fastai.export").get("export_pkl"):
            check_export_picklable()
        set_seed(settings.get("random_seed"), reproducible=True)
    with step("dataset validation"):
        frames = validate_dataset(settings, load_assignments(settings))
    with step("dataloaders"):
        dls = build_dataloaders(settings, frames)
        logger.info("vocab %s; train batches %d; valid batches %d", list(dls.vocab), len(dls.train), len(dls.valid))
    with step("learner"):
        learn = build_learner(settings, dls)
        logger.info("learner %s (%s), pretrained=%s", settings.get("model.backbone"), settings.get("model.source"),
                    settings.get("model.pretrained"))
    return env, frames, dls, learn


def train(learn, settings: TrainingSettings, checkpointer, tracker) -> None:
    """Transfer-learning schedule (FastAI standard stages 9–10)."""

    from fastai.callback.progress import CSVLogger
    from fastai.callback.tracker import EarlyStoppingCallback

    logger = get_logger()
    lr = float(settings.get("learning_rate.value"))
    schedule = settings.get("fastai.schedule")
    method = schedule["method"]
    freeze_epochs = int(schedule["freeze_epochs"])
    epochs = int(settings.get("epochs"))
    callbacks_cfg = settings.get("fastai.callbacks")
    csv_logger = CSVLogger(fname="logs/history.csv", append=True) if callbacks_cfg.get("csv_logger") else None
    base_cbs = [cb for cb in (checkpointer, tracker, csv_logger) if cb is not None]
    unfrozen_cbs = list(base_cbs)
    early = callbacks_cfg.get("early_stopping") or {}
    if early.get("enabled"):
        unfrozen_cbs.append(EarlyStoppingCallback(monitor=early["monitor"], patience=int(early["patience"])))

    logger.info("schedule %s: lr=%g (source=%s), freeze_epochs=%d, epochs=%d", method, lr,
                settings.get("learning_rate.source"), freeze_epochs, epochs)
    if freeze_epochs > 0:
        tracker.phase = "frozen"
        learn.freeze()
        learn.fit_one_cycle(freeze_epochs, slice(lr), pct_start=FROZEN_PCT_START, cbs=base_cbs)
    tracker.phase = "unfrozen"
    learn.unfreeze()
    if method == "fine_tune":
        base = lr / UNFREEZE_LR_DIVISOR if freeze_epochs > 0 else lr
        learn.fit_one_cycle(
            epochs,
            slice(base / float(schedule["lr_mult"]), base),
            pct_start=float(schedule["pct_start"]),
            div=float(schedule["div"]),
            cbs=unfrozen_cbs,
        )
    elif method == "fit_one_cycle":
        learn.fit_one_cycle(epochs, lr, pct_start=float(schedule["pct_start"]), div=float(schedule["div"]),
                            cbs=unfrozen_cbs)
    else:
        raise TrainingConfigError(f"unsupported fastai.schedule.method {method!r}")


def _prediction_frame(items: pd.DataFrame, probs: np.ndarray, vocab: list[str], positive: str,
                      threshold: float) -> pd.DataFrame:
    frame = items.drop(columns=["is_valid"], errors="ignore").reset_index(drop=True).copy()
    for i, name in enumerate(vocab):
        frame[f"prob_{name}"] = probs[:, i]
    pos = vocab.index(positive)
    frame["prob_positive"] = probs[:, pos]
    frame["pred_positive"] = (probs[:, pos] >= threshold).astype(int)
    frame["threshold"] = threshold
    return frame


def predict_and_score(learn, settings: TrainingSettings, frames: SplitFrames) -> dict:
    """Validation + test predictions, validation-only threshold, canonical metrics (M16 inputs)."""

    logger = get_logger()
    vocab = list(learn.dls.vocab)
    positive = settings.positive_class
    label_col = settings.get("dataset.label_column")
    metrics_cfg = settings.get("metrics")
    bins = int(metrics_cfg["calibration_bins"])

    val_probs, _ = learn.get_preds(ds_idx=1)
    val_items = learn.dls.valid.items
    test_dl = learn.dls.test_dl(frames.test, with_labels=True)
    test_probs, _ = learn.get_preds(dl=test_dl)
    val_probs, test_probs = val_probs.float().numpy(), test_probs.float().numpy()

    pos = vocab.index(positive)
    y_val = (val_items[label_col].to_numpy() == positive).astype(int)
    y_test = (frames.test[label_col].to_numpy() == positive).astype(int)

    threshold = evaluation.select_threshold(y_val, val_probs[:, pos], metrics_cfg["threshold_criterion"])
    logger.info("threshold %.6f chosen on validation (%s)", threshold, metrics_cfg["threshold_criterion"])
    results = {
        "threshold": {"value": threshold, "criterion": metrics_cfg["threshold_criterion"],
                      "policy": metrics_cfg["threshold_policy"], "positive_class": positive},
        "val": evaluation.compute_metrics(y_val, val_probs[:, pos], threshold, bins),
        "test": evaluation.compute_metrics(y_test, test_probs[:, pos], threshold, bins),
    }

    settings.predictions_dir.mkdir(parents=True, exist_ok=True)
    settings.metrics_dir.mkdir(parents=True, exist_ok=True)
    _prediction_frame(val_items, val_probs, vocab, positive, threshold).to_csv(
        settings.predictions_dir / "val_predictions.csv", index=False)
    _prediction_frame(frames.test, test_probs, vocab, positive, threshold).to_csv(
        settings.predictions_dir / "test_predictions.csv", index=False)
    _write_json(settings.metrics_dir / "threshold.json", results["threshold"])
    for split, y, p in (("val", y_val, val_probs[:, pos]), ("test", y_test, test_probs[:, pos])):
        _write_json(settings.metrics_dir / f"{split}_metrics.json", results[split])
        pd.DataFrame(evaluation.calibration_table(y, p, bins)).to_csv(
            settings.metrics_dir / f"{split}_calibration.csv", index=False)
        logger.info("%s metrics %s", split, {k: round(v, 4) if isinstance(v, float) else v
                                             for k, v in results[split].items()})
    return results


def export_artifacts(learn, settings: TrainingSettings, checkpointer) -> dict[str, dict]:
    """best_model.pth, last_checkpoint.pth, export.pkl, weights.pth (Phase M15)."""

    import torch

    export_cfg = settings.get("fastai.export")
    ckpt = settings.checkpoint_dir
    artifacts: dict[str, Path] = {"best_model": ckpt / "best_model.pth"}
    if checkpointer.saved:
        last_src = ckpt / f"{checkpointer.saved[-1]}.pth"
        last = ckpt / "last_checkpoint.pth"
        shutil.copy2(last_src, last)
        artifacts["last_checkpoint"] = last
    learn.load("best_model", with_opt=False)
    if settings.get("fastai.mixed_precision"):
        learn.to_fp32()
    if export_cfg.get("export_pkl"):
        artifacts["export_pkl"] = ckpt / "export.pkl"
        learn.export(artifacts["export_pkl"])
    if export_cfg.get("weights_pth"):
        artifacts["weights_pth"] = ckpt / "weights.pth"
        torch.save(learn.model.state_dict(), artifacts["weights_pth"])
    missing = [name for name, path in artifacts.items() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"expected export artifact(s) were not written: {missing}")
    return {
        name: {"path": str(path.relative_to(settings.repo_root)), "bytes": path.stat().st_size,
               "sha256": _sha256(path)}
        for name, path in artifacts.items()
    }


def run_experiment(
    config_path: str | Path,
    *,
    repo_root: str | Path | None = None,
    check_registries: bool = True,
) -> dict:
    """Run one experiment end to end from its config.yaml and return the run summary."""

    from .callbacks import EpochCheckpointer, HistoryTracker

    settings = load_settings(config_path, repo_root=repo_root, check_registries=check_registries)
    started = datetime.now().astimezone()
    log_path = setup_run_logging(settings.logs_dir, "train")
    logger = get_logger()
    try:
        logger.info("experiment %s; config %s; config validation PASS", settings.experiment_id, settings.config_path)
        with step("output guard"):
            guard_outputs(settings)
            settings.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        with step("git provenance"):
            provenance = check_git_provenance(settings)
        env, frames, dls, learn = prepare(settings)

        save_cfg = settings.get("fastai.callbacks.save_model")
        checkpointer = EpochCheckpointer(
            monitor=save_cfg["monitor"], comp=save_cfg["comp"], with_opt=bool(save_cfg["with_opt"]),
            every_epoch=bool(save_cfg["every_epoch"]),
        )
        tracker = HistoryTracker()
        with step("training"):
            train(learn, settings, checkpointer, tracker)
        with step("learning curves"):
            settings.curves_dir.mkdir(parents=True, exist_ok=True)
            pd.DataFrame(tracker.epochs).to_csv(settings.curves_dir / "epochs.csv", index=False)
            pd.DataFrame(tracker.batches).to_csv(settings.curves_dir / "batches.csv", index=False)
        with step("checkpoint save + export"):
            artifacts = export_artifacts(learn, settings, checkpointer)
        with step("validation + test predictions"):
            results = predict_and_score(learn, settings, frames)
        finished = datetime.now().astimezone()
        summary = {
            "experiment_id": settings.experiment_id,
            "status": "complete",
            "config": str(settings.config_path.relative_to(settings.repo_root)),
            "config_sha256": _sha256(settings.config_path),
            "git": provenance,
            "started": started.isoformat(),
            "finished": finished.isoformat(),
            "training_seconds": round(sum(row["seconds"] for row in tracker.epochs), 1),
            "epochs_run": tracker.global_epoch,
            "best_epoch": checkpointer.best_epoch,
            "best_monitor": {"name": checkpointer.monitor, "value": checkpointer.best_value},
            "metrics": results,
            "artifacts": artifacts,
            "environment": env,
            "log": str(log_path.relative_to(settings.repo_root)),
        }
        with step("summary"):
            _write_json(settings.metrics_dir / "run_summary.json", summary)
        logger.info("run complete: best epoch %s, test ROC-AUC %.4f", checkpointer.best_epoch,
                    results["test"]["roc_auc"])
        return summary
    finally:
        close_run_logging()


def find_lr(
    config_path: str | Path,
    *,
    repo_root: str | Path | None = None,
    check_registries: bool = True,
) -> dict:
    """Run the LR Finder and record the suggestion; never edits config.yaml."""

    settings = load_settings(config_path, repo_root=repo_root, check_registries=check_registries)
    lr_cfg = settings.get("fastai.lr_finder")
    if not lr_cfg.get("enabled"):
        raise TrainingConfigError("fastai.lr_finder.enabled is false")
    suggest = lr_cfg["suggest_func"]
    if suggest not in LR_SUGGESTERS:
        raise TrainingConfigError(f"fastai.lr_finder.suggest_func must be one of {LR_SUGGESTERS}, got {suggest!r}")
    log_path = setup_run_logging(settings.logs_dir, "lr_find")
    logger = get_logger()
    try:
        import fastai.callback.schedule as sched

        _, _, _, learn = prepare(settings)
        with step("lr finder"):
            learn.freeze()
            result = learn.lr_find(num_it=int(lr_cfg["num_it"]), suggest_funcs=(getattr(sched, suggest),),
                                   show_plot=False)
            suggestion = float(getattr(result, suggest))
        stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        curve = pd.DataFrame({"lr": [float(x) for x in learn.recorder.lrs],
                              "loss": [float(x) for x in learn.recorder.losses]})
        curve_path = settings.logs_dir / f"lr_find_{stamp}.csv"
        curve.to_csv(curve_path, index=False)
        payload = {
            "experiment_id": settings.experiment_id,
            "suggest_func": suggest,
            "suggested_lr": suggestion,
            "config_lr": float(settings.get("learning_rate.value")),
            "curve": str(curve_path.relative_to(settings.repo_root)),
            "log": str(log_path.relative_to(settings.repo_root)),
        }
        _write_json(settings.logs_dir / f"lr_find_{stamp}.json", payload)
        logger.info("LR Finder suggests %.3g (%s); record it in learning_rate.value before training", suggestion,
                    suggest)
        return payload
    finally:
        close_run_logging()
