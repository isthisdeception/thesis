"""Phase M6 training workflow: config → data → train (resumable) → checkpoints → curves → export → metrics → summary."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from . import evaluation
from .checkpoints import MANIFEST_NAME, QUARANTINE_DIR, STATE_FORMAT_VERSION, CheckpointStore, capture_rng, restore_rng
from .data import SplitFrames, build_dataloaders, load_assignments, validate_dataset
from .logs import close_run_logging, environment_info, get_logger, setup_run_logging, step
from .settings import TrainingConfigError, TrainingSettings, load_settings

# FastAI `Learner.fine_tune` semantics for the frozen phase and the unfreeze LR step.
FROZEN_PCT_START = 0.99
UNFREEZE_LR_DIVISOR = 2

LR_SUGGESTERS = ("valley", "minimum", "steep", "slide")
SUMMARY_NAME = "run_summary.json"


class OutputsExistError(FileExistsError):
    """The experiment already has outputs that this run would overwrite."""


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def _files_in(folder: Path, ignore: set[str]) -> list[Path]:
    return [p for p in folder.iterdir() if p.name not in ignore] if folder.is_dir() else []


def _raise_existing(settings: TrainingSettings, found: list[Path], why: str) -> None:
    listed = ", ".join(str(p.relative_to(settings.repo_root)) for p in found[:5])
    raise OutputsExistError(f"{settings.experiment_id}: {why} ({listed}{', ...' if len(found) > 5 else ''})")


def plan_run(settings: TrainingSettings, store: CheckpointStore, *, resume: bool) -> str:
    """Decide between a fresh run and a resume; refuse anything that would overwrite outputs.

    Returns ``"fresh"`` or ``"resume"``.
    """

    summary = settings.metrics_dir / SUMMARY_NAME
    if summary.exists():
        _raise_existing(settings, [summary], "experiment is already complete; a changed rerun needs a new EXP ID")
    finished = [f for d in (settings.metrics_dir, settings.predictions_dir, settings.curves_dir)
                for f in _files_in(d, {".gitkeep"})]
    if finished:
        _raise_existing(settings, finished,
                        "post-training outputs from an incomplete run exist; move them aside before running")

    has_recovery = bool(store.valid_entries("recovery"))
    if has_recovery:
        if not resume:
            _raise_existing(settings, [store.manifest_path], "recovery checkpoints exist and resume=False")
        manifest = store.load_manifest()
        if manifest["config_sha256"] != store.config_sha256:
            raise TrainingConfigError(
                f"config.yaml changed since {settings.experiment_id}'s checkpoints were written "
                f"(manifest {manifest['config_sha256'][:12]}…, now {store.config_sha256[:12]}…); "
                "the config is immutable after launch — a changed run needs a new EXP ID"
            )
        return "resume"

    unknown = _files_in(settings.checkpoint_dir, {".gitkeep", MANIFEST_NAME, QUARANTINE_DIR})
    if unknown:
        _raise_existing(settings, unknown, "checkpoint folder holds files that are not in a checkpoint manifest")
    history = settings.logs_dir / "history.csv"
    if history.exists():
        _raise_existing(settings, [history], "a training log from an earlier run exists")
    return "fresh"


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


def check_checkpoint_policy(settings: TrainingSettings) -> None:
    save_cfg = settings.get("fastai.callbacks.save_model")
    if not (save_cfg.get("every_epoch") and save_cfg.get("with_opt")):
        raise TrainingConfigError(
            "fastai.callbacks.save_model.every_epoch and with_opt must both be true: "
            "recovery checkpoints need full state every epoch (Phase M7)"
        )


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


# --- schedule -------------------------------------------------------------------


def phase_plan(settings: TrainingSettings) -> list[tuple[str, int]]:
    freeze_epochs = int(settings.get("fastai.schedule.freeze_epochs"))
    plan = [("frozen", freeze_epochs)] if freeze_epochs > 0 else []
    return plan + [("unfrozen", int(settings.get("epochs")))]


@dataclass(frozen=True)
class StartPoint:
    phase_index: int
    start_epoch: int
    done: bool = False


def start_point(settings: TrainingSettings, state: dict | None) -> StartPoint:
    """Where training continues, given the last recovery state (``None`` for a fresh run)."""

    if state is None:
        return StartPoint(0, 0)
    if state["experiment"]["checkpointer"]["training_complete"]:
        return StartPoint(0, 0, done=True)
    plan = phase_plan(settings)
    names = [name for name, _ in plan]
    if state["phase"] not in names:
        raise TrainingConfigError(f"checkpoint phase {state['phase']!r} does not exist in the configured schedule")
    index = names.index(state["phase"])
    nxt = state["phase_epoch"] + 1
    if nxt < plan[index][1]:
        return StartPoint(index, nxt)
    if index + 1 < len(plan):
        return StartPoint(index + 1, 0)
    return StartPoint(0, 0, done=True)


def schedule_record(settings: TrainingSettings) -> dict:
    schedule = settings.get("fastai.schedule")
    return {
        "method": schedule["method"],
        "lr": float(settings.get("learning_rate.value")),
        "freeze_epochs": int(schedule["freeze_epochs"]),
        "epochs": int(settings.get("epochs")),
        "lr_mult": float(schedule["lr_mult"]),
        "pct_start": float(schedule["pct_start"]),
        "div": float(schedule["div"]),
        "frozen_pct_start": FROZEN_PCT_START,
        "unfreeze_lr_divisor": UNFREEZE_LR_DIVISOR,
    }


def make_state_builder(learn, settings: TrainingSettings, store: CheckpointStore, tracker):
    """Full training state for a recovery checkpoint (Phase M7)."""

    schedule = schedule_record(settings)

    def build(checkpointer) -> dict:
        return {
            "format_version": STATE_FORMAT_VERSION,
            "experiment_id": settings.experiment_id,
            "config_sha256": store.config_sha256,
            "epoch": checkpointer.global_epoch,
            "phase": checkpointer.phase,
            "phase_epoch": int(checkpointer.epoch),
            "phase_n_epoch": checkpointer.phase_n_epoch,
            # The one-cycle LR/momentum schedule is a pure function of these values plus the phase position.
            "schedule": schedule,
            "model": learn.model.state_dict(),
            "opt": learn.opt.state_dict(),
            "rng": capture_rng(),
            "experiment": {
                "checkpointer": checkpointer.state_dict(),
                "tracker": tracker.state_dict(),
                "values": checkpointer.last_values,
            },
        }

    return build


def restore_state(learn, state: dict, checkpointer, tracker) -> None:
    """Load weights, optimizer, callback state; RNG is restored last, right before training resumes."""

    if state["phase"] == "unfrozen":
        learn.unfreeze()
    else:
        learn.freeze()
    learn.model.load_state_dict(state["model"])
    learn.opt.load_state_dict(state["opt"])
    checkpointer.load_state_dict(state["experiment"]["checkpointer"])
    tracker.load_state_dict(state["experiment"]["tracker"])


def train(learn, settings: TrainingSettings, checkpointer, tracker, start: StartPoint, rng_state: dict | None) -> None:
    """Transfer-learning schedule (FastAI standard stages 9–10), resumable at any epoch boundary."""

    from fastai.callback.progress import CSVLogger

    logger = get_logger()
    if start.done:
        logger.info("training already complete in the recovery checkpoint; skipping to post-training steps")
        return
    sched = schedule_record(settings)
    lr = sched["lr"]
    csv_logger = CSVLogger(fname="logs/history.csv", append=True) if settings.get("fastai.callbacks.csv_logger") else None
    cbs = [cb for cb in (checkpointer, tracker, csv_logger) if cb is not None]
    logger.info("schedule %s: lr=%g (source=%s), freeze_epochs=%d, epochs=%d; starting at phase %d epoch %d",
                sched["method"], lr, settings.get("learning_rate.source"), sched["freeze_epochs"], sched["epochs"],
                start.phase_index, start.start_epoch)

    for index, (phase, n_epoch) in enumerate(phase_plan(settings)):
        if index < start.phase_index:
            continue
        first = start.start_epoch if index == start.phase_index else 0
        resuming_here = rng_state is not None and index == start.phase_index
        # freeze()/unfreeze() clear optimizer state, so they are skipped when resuming inside a phase.
        if not (resuming_here and first > 0):
            learn.freeze() if phase == "frozen" else learn.unfreeze()
        tracker.begin_phase(phase, n_epoch, first)
        checkpointer.begin_phase(phase, n_epoch, first, early_active=phase == "unfrozen")
        if resuming_here:
            restore_rng(rng_state)
        if phase == "frozen":
            learn.fit_one_cycle(n_epoch, slice(lr), pct_start=FROZEN_PCT_START, cbs=cbs, start_epoch=first)
        elif sched["method"] == "fine_tune":
            base = lr / UNFREEZE_LR_DIVISOR if sched["freeze_epochs"] > 0 else lr
            learn.fit_one_cycle(n_epoch, slice(base / sched["lr_mult"], base), pct_start=sched["pct_start"],
                                div=sched["div"], cbs=cbs, start_epoch=first)
        elif sched["method"] == "fit_one_cycle":
            learn.fit_one_cycle(n_epoch, lr, pct_start=sched["pct_start"], div=sched["div"], cbs=cbs,
                                start_epoch=first)
        else:
            raise TrainingConfigError(f"unsupported fastai.schedule.method {sched['method']!r}")
        if checkpointer.early_stopped:
            break


# --- post-training --------------------------------------------------------------


def finalize_checkpoints(learn, settings: TrainingSettings, store: CheckpointStore, checkpointer) -> dict[str, dict]:
    """EXPxxxx_best/last copies, best weights loaded, MODELxxxx export.pkl + weights.pth (Phase M15)."""

    import torch

    recovery = store.valid_entries("recovery")
    if not recovery:
        raise FileNotFoundError("no recovery checkpoints to finalize")
    best_src = store.find(store.recovery_name(checkpointer.best.epoch))
    last_src = max(recovery, key=lambda e: e["epoch"])
    if best_src is None:
        raise FileNotFoundError(f"best epoch {checkpointer.best.epoch} has no valid recovery checkpoint")
    entries = {
        "best": store.copy_as(best_src, store.best_name, "best"),
        "last": store.copy_as(last_src, store.last_name, "last"),
    }
    state = torch.load(store.path_of(entries["best"]), map_location=learn.dls.device, weights_only=False)
    learn.model.load_state_dict(state["model"])
    if settings.get("fastai.mixed_precision"):
        learn.to_fp32()

    export_cfg = settings.get("fastai.export")
    meta = {"epoch": entries["best"]["epoch"], "copied_from": None, "source_checkpoint": store.best_name}
    if export_cfg.get("export_pkl"):
        entries["export_pkl"] = store.find(store.export_name) or _write_artifact(
            store, store.export_name, "export_pkl", meta, lambda tmp: learn.export(tmp))
    if export_cfg.get("weights_pth"):
        entries["weights_pth"] = store.find(store.weights_name) or _write_artifact(
            store, store.weights_name, "weights_pth", meta, lambda tmp: torch.save(learn.model.state_dict(), tmp))

    broken = store.verify_all()
    if broken:
        raise FileNotFoundError(f"checkpoint checksum verification failed for: {broken}")
    return {
        kind: {"name": e["name"], "path": (store.dir / e["name"]).relative_to(settings.repo_root).as_posix(),
               "sha256": e["sha256"], "bytes": e["bytes"]}
        for kind, e in entries.items()
    }


def _write_artifact(store: CheckpointStore, name: str, kind: str, meta: dict, write) -> dict:
    tmp = store.reserve(name)
    write(tmp)
    return store.commit(tmp, name, kind, meta)


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


# --- entry points ---------------------------------------------------------------


def run_experiment(
    config_path: str | Path,
    *,
    repo_root: str | Path | None = None,
    check_registries: bool = True,
    resume: bool = True,
) -> dict:
    """Run one experiment from its config.yaml, resuming from the latest valid recovery checkpoint if present."""

    from .callbacks import EpochCheckpointer, HistoryTracker, default_comp

    settings = load_settings(config_path, repo_root=repo_root, check_registries=check_registries)
    check_checkpoint_policy(settings)
    store = CheckpointStore(settings)
    started = datetime.now().astimezone()
    log_path = setup_run_logging(settings.logs_dir, f"{settings.experiment_id}_train")
    logger = get_logger()
    try:
        logger.info("experiment %s; config %s; config validation PASS", settings.experiment_id, settings.config_path)
        with step("output guard"):
            mode = plan_run(settings, store, resume=resume)
            logger.info("run mode: %s", mode)
        with step("git provenance"):
            provenance = check_git_provenance(settings)
        env, frames, dls, learn = prepare(settings)

        save_cfg = settings.get("fastai.callbacks.save_model")
        tracker = HistoryTracker()
        checkpointer = EpochCheckpointer(
            store,
            make_state_builder(learn, settings, store, tracker),
            monitor=save_cfg["monitor"],
            comp=save_cfg.get("comp") or default_comp(save_cfg["monitor"]),
            early_stopping=settings.get("fastai.callbacks").get("early_stopping"),
        )
        resumed_from = None
        rng_state = None
        state = None
        if mode == "resume":
            with step("resume"):
                found = store.latest_valid_recovery(map_location=dls.device)
                if found is None:
                    raise FileNotFoundError(
                        f"no recovery checkpoint passed verification in {store.dir}; see quarantine/ and the manifest"
                    )
                entry, state = found
                restore_state(learn, state, checkpointer, tracker)
                rng_state = state["rng"]
                resumed_from = entry["epoch"]
                logger.info("resumed from %s (epoch %d, phase %s)", entry["name"], entry["epoch"], state["phase"])
        start = start_point(settings, state)
        with step("training"):
            train(learn, settings, checkpointer, tracker, start, rng_state)
        with step("learning curves"):
            settings.curves_dir.mkdir(parents=True, exist_ok=True)
            pd.DataFrame(tracker.epochs).to_csv(settings.curves_dir / "epochs.csv", index=False)
            pd.DataFrame(tracker.batches).to_csv(settings.curves_dir / "batches.csv", index=False)
        with step("checkpoint finalize + export"):
            artifacts = finalize_checkpoints(learn, settings, store, checkpointer)
        with step("validation + test predictions"):
            results = predict_and_score(learn, settings, frames)
        finished = datetime.now().astimezone()
        summary = {
            "experiment_id": settings.experiment_id,
            "status": "complete",
            "config": settings.config_path.relative_to(settings.repo_root).as_posix(),
            "config_sha256": store.config_sha256,
            "git": provenance,
            "started": started.isoformat(),
            "finished": finished.isoformat(),
            "resumed_from_epoch": resumed_from,
            "training_seconds": round(sum(row["seconds"] for row in tracker.epochs), 1),
            "epochs_run": tracker.global_epoch,
            "early_stopped": checkpointer.early_stopped,
            "best_epoch": checkpointer.best.epoch,
            "best_monitor": {"name": checkpointer.best.monitor, "value": checkpointer.best.value},
            "metrics": results,
            "artifacts": artifacts,
            "checkpoint_manifest": {
                "json": store.manifest_path.relative_to(settings.repo_root).as_posix(),
                "markdown": store.markdown_path.relative_to(settings.repo_root).as_posix(),
            },
            "environment": env,
            "log": log_path.relative_to(settings.repo_root).as_posix(),
        }
        with step("summary"):
            _write_json(settings.metrics_dir / SUMMARY_NAME, summary)
        logger.info("run complete: best epoch %s, test ROC-AUC %.4f", checkpointer.best.epoch,
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
    log_path = setup_run_logging(settings.logs_dir, f"{settings.experiment_id}_lr_find")
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
        curve_path = settings.logs_dir / f"{settings.experiment_id}_lr_find_{stamp}.csv"
        curve.to_csv(curve_path, index=False)
        payload = {
            "experiment_id": settings.experiment_id,
            "suggest_func": suggest,
            "suggested_lr": suggestion,
            "config_lr": float(settings.get("learning_rate.value")),
            "curve": curve_path.relative_to(settings.repo_root).as_posix(),
            "log": log_path.relative_to(settings.repo_root).as_posix(),
        }
        _write_json(settings.logs_dir / f"{settings.experiment_id}_lr_find_{stamp}.json", payload)
        logger.info("LR Finder suggests %.3g (%s); record it in learning_rate.value before training", suggestion,
                    suggest)
        return payload
    finally:
        close_run_logging()
