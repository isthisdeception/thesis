"""Learner construction from config (FastAI standard stage 6)."""

from __future__ import annotations

from functools import partial

from .settings import TrainingConfigError, TrainingSettings


def resolve_arch(settings: TrainingSettings):
    """torchvision callable or timm model name, per ``model.source``."""

    source = settings.get("model.source")
    backbone = settings.get("model.backbone")
    if source == "torchvision":
        import torchvision.models as tvm

        arch = getattr(tvm, backbone, None)
        if not callable(arch):
            raise TrainingConfigError(f"torchvision has no model named {backbone!r}")
        return arch
    if source == "timm":
        try:
            import timm
        except ImportError as exc:
            raise TrainingConfigError("model.source is 'timm' but timm is not installed") from exc
        if backbone not in timm.list_models(pretrained=bool(settings.get("model.pretrained"))):
            raise TrainingConfigError(f"timm has no {'pretrained ' if settings.get('model.pretrained') else ''}model {backbone!r}")
        return backbone
    raise TrainingConfigError(f"unsupported model.source {source!r}")


def build_loss(settings: TrainingSettings):
    from fastai.losses import CrossEntropyLossFlat, LabelSmoothingCrossEntropyFlat

    loss = settings.get("loss_function")
    name = loss["name"]
    smoothing = float(settings.get("loss_function.label_smoothing"))
    if name == "CrossEntropyLossFlat":
        return CrossEntropyLossFlat(label_smoothing=smoothing)
    if name == "LabelSmoothingCrossEntropyFlat":
        return LabelSmoothingCrossEntropyFlat(eps=smoothing)
    raise TrainingConfigError(f"unsupported loss_function.name {name!r}")


def build_optimizer(settings: TrainingSettings):
    from fastai.optimizer import SGD, Adam, RAdam, ranger

    opt = settings.get("optimizer")
    name = opt["name"]
    if name in {"Adam", "RAdam"}:
        betas = opt.get("betas")
        if not (isinstance(betas, list) and len(betas) == 2):
            raise TrainingConfigError(f"optimizer.betas must be [beta1, beta2] for {name}")
        return partial(Adam if name == "Adam" else RAdam, mom=betas[0], sqr_mom=betas[1])
    if name == "SGD":
        return partial(SGD, mom=settings.get("optimizer.momentum"))
    if name == "ranger":
        return ranger
    raise TrainingConfigError(f"unsupported optimizer.name {name!r}")


def build_train_metrics(settings: TrainingSettings, vocab: list[str]) -> list:
    """FastAI monitors for every configured metric that has a FastAI equivalent.

    The remaining canonical metrics are computed from saved predictions after training.
    """

    from fastai.metrics import (
        BalancedAccuracy,
        F1Score,
        MatthewsCorrCoef,
        Precision,
        Recall,
        RocAucBinary,
        accuracy,
    )

    pos = vocab.index(settings.positive_class)
    available = {
        "accuracy": lambda: accuracy,
        "roc_auc": lambda: RocAucBinary(),
        "balanced_accuracy": lambda: BalancedAccuracy(),
        "f1": lambda: F1Score(pos_label=pos),
        "mcc": lambda: MatthewsCorrCoef(),
        "precision": lambda: Precision(pos_label=pos),
        "recall": lambda: Recall(pos_label=pos),
    }
    metrics_cfg = settings.get("metrics")
    names = [*metrics_cfg["primary"], *metrics_cfg.get("secondary", [])]
    return [available[name]() for name in names if name in available]


def build_learner(settings: TrainingSettings, dls):
    from fastai.vision.all import vision_learner

    vocab = list(dls.vocab)
    if settings.positive_class not in vocab:
        raise TrainingConfigError(f"positive class {settings.positive_class!r} not in DataLoaders vocab {vocab}")
    learn = vision_learner(
        dls,
        resolve_arch(settings),
        pretrained=bool(settings.get("model.pretrained")),
        normalize=False,
        loss_func=build_loss(settings),
        opt_func=build_optimizer(settings),
        metrics=build_train_metrics(settings, vocab),
        wd=float(settings.get("optimizer.weight_decay")),
        path=settings.experiment_dir,
        model_dir=settings.checkpoint_dir,
    )
    if settings.get("fastai.mixed_precision"):
        learn.to_fp16()
    return learn
