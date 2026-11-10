"""Markdown reports for Phase E8 (cross-dataset) and Phase E9 (unseen generator). Numbers come from the frames."""

from __future__ import annotations

import pandas as pd


def _f(v, d: int = 4) -> str:
    return "—" if pd.isna(v) else f"{float(v):.{d}f}"


def _p(v) -> str:
    return "—" if pd.isna(v) else f"{float(v):.1%}"


def render_cross_dataset(datasets: pd.DataFrame, groups: pd.DataFrame, relations: pd.DataFrame, manifest: dict,
                         config_raw: dict, date: str) -> str:
    descriptions = {d["name"]: d for d in config_raw["datasets"]}
    ref = datasets[datasets["role"] == "in_distribution"].iloc[0]
    check = manifest.get("sanity_check") or {}
    lines = [
        f"# Cross-Dataset Evaluation: {manifest['evaluation_id']}",
        "",
        f"**Model:** {manifest['model_id']} (export SHA-256 `{manifest['export_sha256'][:12]}…`), trained on DS0001 SPLIT0001  ",
        "**Phase:** E8  ",
        f"**Date:** {date}",
        "",
        f"Threshold {ref['threshold']:.4f} (chosen on DS0001 val) for every dataset. Nothing is re-tuned on target data. "
        f"Config: `{manifest['config']}` (SHA-256 `{manifest['config_sha256'][:12]}…`). Per-image probabilities: `predictions/`.",
        "",
        f"Sanity check: {check.get('images', 'n/a')} DS0001 test images re-predicted with max |diff| "
        f"{check.get('max_abs_diff', float('nan')):.2e} against `predictions.csv` (limit {check.get('atol', 'n/a')}).",
        "",
        "## Datasets",
        "",
        "| Dataset | Content | n (fake / real) | Recall | FNR | Specificity | FPR | Balanced acc. | ROC-AUC | Mean P(fake) |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for _, r in datasets.iterrows():
        what = descriptions.get(r["dataset"], {}).get("description", "in-distribution test (reference)")
        lines.append(f"| {r['dataset']} | {what} | {r['n']} ({r['n_fake']} / {r['n_real']}) | {_f(r['recall'])} | {_f(r['fnr'])} | "
                     f"{_f(r['specificity'])} | {_f(r['fpr'])} | {_f(r['balanced_accuracy'])} | {_f(r['roc_auc'])} | {_f(r['mean_prob'])} |")
    lines += ["", "— = not defined because the dataset has one class. Fake-only datasets give recall; real-only give specificity.", ""]
    notes = [f"- {d['name']}: {d['notes']}" for d in config_raw["datasets"] if d.get("notes")]
    if notes:
        lines += ["Notes from the config:", "", *notes, ""]
    lines += [
        "## Fake images by relation to the training generators",
        "",
        "`seen`: same generator name as in DS0001 training. `related`: same family, version not confirmed (set in the config). `unseen`: neither.",
        "",
        "| Relation | Datasets | Generators | n | FNR | 95% CI |",
        "|---|---|---|---|---|---|",
    ]
    for _, r in relations.iterrows():
        lines.append(f"| {r['relation']} | {r['datasets']} | {r['generators']} | {r['n']} | {_p(r['fnr'])} | {_p(r['ci_low'])}–{_p(r['ci_high'])} |")
    ref_fnr = ref["fnr"]
    lines += ["", f"In-distribution FNR on DS0001 test is {_p(ref_fnr)}.", "",
              "## By generator (cross-dataset)", "",
              "Error rate is FNR for fake generators and FPR for real sources. Wilson 95% intervals. Groups under 30 images are flagged in the CSV.",
              "",
              "| Dataset | Class | Generator | Relation | n | Error rate | 95% CI | Mean P(fake) |",
              "|---|---|---|---|---|---|---|---|"]
    cross = groups[(groups["dataset"] != "DS0001") & ~groups["small_group"]].sort_values(["dataset", "true_label", "error_rate"], ascending=[True, True, False])
    for _, r in cross.iterrows():
        lines.append(f"| {r['dataset']} | {r['true_label']} | {r['generator']} | {r['relation']} | {r['n']} | {_p(r['error_rate'])} | "
                     f"{_p(r['ci_low'])}–{_p(r['ci_high'])} | {_f(r['mean_prob'], 3)} |")
    lines += [
        "",
        "## Limits",
        "",
        "- Fake-only and real-only datasets support one error type each; their numbers are not balanced accuracy.",
        "- Each dataset was preprocessed with its own pipeline (PP0002–PP0006) to the same 224 px PNG format; source resolutions and formats differ.",
        "- `related` labels are a judgement recorded in the config, not a verified identity of generator versions.",
        "- One model, one seed. No statistical test (Phase E11). Differences describe where performance changes, not why.",
    ]
    return "\n".join(lines) + "\n"


def render_unseen(detection: pd.DataFrame, paired: pd.DataFrame, leakage: dict, auc: float, info: dict, date: str) -> str:
    unseen = detection[detection["role"] == "unseen (test)"]
    seen_all = detection[detection["group"] == "all seen generators"].iloc[0]
    lines = [
        f"# Unseen-Generator Evaluation: {info['evaluation_id']}",
        "",
        f"**Experiment:** {info['experiment_id']} ({info['model_id']}), trained on {info['split']} without {', '.join(leakage['held_out'])}  ",
        "**Phase:** E9  ",
        f"**Date:** {date}",
        "",
        f"Threshold {info['threshold']:.4f}, chosen on the experiment's val split (no held-out images). Source: `{info['source']}`.",
        "",
        f"Leakage check PASS: held-out generator(s) absent from train and val. Training generators: {', '.join(leakage['train_generators'])}.",
        "",
        "## Detection",
        "",
        "| Group | Images | Role | n | Detected | 95% CI | Mean P(fake) |",
        "|---|---|---|---|---|---|---|",
    ]
    for _, r in detection.iterrows():
        what = "specificity" if r["true_label"] == "real" else "recall"
        lines.append(f"| {r['group']} | {r['true_label']} | {r['role']} | {r['n']} | {_p(r['rate'])} ({what}) | {_p(r['ci_low'])}–{_p(r['ci_high'])} | {_f(r['mean_prob'], 3)} |")
    lines += [""]
    for _, r in unseen.iterrows():
        lines.append(f"- `{r['group']}` (unseen): {_p(r['rate'])} detected, against {_p(seen_all['rate'])} for seen generators on val.")
    lines += [
        f"- ROC-AUC of unseen test fakes against val real images: {_f(auc)}. Indicative only: those real images also set the threshold.",
        "",
        "## Same images, generator seen vs unseen",
        "",
        f"`{info['reference_name']}` saw the generator in training; {info['model_id']} did not. Same test images, each model at its own threshold.",
        "",
        "| Generator | n | Recall (seen in training) | Recall (unseen) | Both | Only seen-model | Only unseen-model | Neither |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for _, r in paired.iterrows():
        lines.append(f"| {r['generator']} | {r['n']} | {_p(r['recall_reference'])} | {_p(r['recall_held_out'])} | {r['both_detected']} | "
                     f"{r['only_reference']} | {r['only_held_out']} | {r['neither']} |")
    lines += [
        "",
        "## Limits",
        "",
        f"- One held-out generator ({', '.join(leakage['held_out'])}); other generators were not held out (decision recorded in DEC0007).",
        "- The held-out test split has fake images only, so only recall is measured on it.",
        "- The two models differ in training data (the held-out model has no images of that generator) and are single runs. No statistical test (Phase E11).",
    ]
    return "\n".join(lines) + "\n"
