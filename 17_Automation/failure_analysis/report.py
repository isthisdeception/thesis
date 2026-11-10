"""failure_analysis.md. Observations come from the frames; causes are written as hypotheses only."""

from __future__ import annotations

import pandas as pd

from .analysis import MIN_GROUP


def _pct(value: float) -> str:
    return "n/a" if pd.isna(value) else f"{value:.1%}"


def _names(frame: pd.DataFrame) -> str:
    return ", ".join(f"`{g}`" for g in frame["group"]) or "none"


def render_report(
    confusion: pd.DataFrame,
    per_class: pd.DataFrame,
    groups: pd.DataFrame,
    summary: pd.DataFrame,
    cases: pd.DataFrame,
    coverage: dict,
    evaluation_id: str,
    experiment_id: str,
    predictions_sha256: str,
    date: str,
    split: str = "test",
) -> str:
    c = confusion[confusion["split"] == split].set_index(["true_label", "predicted_label"])
    pc = per_class[per_class["split"] == split]
    g = groups[(groups["split"] == split) & ~groups["small_group"]]
    gen = g[g["group_type"] == "generator"].sort_values(["error_rate", "group"], ascending=[False, True])
    real = g[g["group_type"] == "real_source"].sort_values(["error_rate", "group"], ascending=[False, True])
    s = summary[summary["split"] == split].set_index("error_type")
    fn_rate = pc.loc[pc["class"] == "fake", "error_rate"].iloc[0]
    fp_rate = pc.loc[pc["class"] == "real", "error_rate"].iloc[0]
    hard = gen[gen["ci_low"] > fn_rate]
    easy = gen[gen["ci_high"] < fn_rate]
    top3 = gen.head(3)
    hard_real = real[real["ci_low"] > fp_rate]
    top_cases = cases[(cases["split"] == split)]
    fp_cases = top_cases[top_cases["error_type"] == "false_positive"]["subgroup"].value_counts()
    fn_cases = top_cases[top_cases["error_type"] == "false_negative"]["subgroup"].value_counts()

    lines = [
        f"# Failure Analysis: {evaluation_id}",
        "",
        f"**Experiment:** {experiment_id}",
        "**Phases:** E6, E12",
        f"**Date:** {date}",
        "",
        f"Source: `08_Evaluation/{experiment_id}/predictions.csv` (SHA-256 `{predictions_sha256}`), joined to the preprocessing "
        "index by content hash. Decisions are the saved ones at the frozen threshold, as in `classification_metrics.csv`. "
        f"This report describes `{split}`; `val` rows are in the CSVs.",
        "",
        "Causes below are **hypotheses**. None has been tested. Each lists how it could be checked.",
        "",
        "## Confusion matrix (E6)",
        "",
        "| True \\ Predicted | fake | real |",
        "|------------------|------|------|",
    ]
    for t in ("fake", "real"):
        lines.append(f"| {t} | " + " | ".join(f"{int(c.loc[(t, p), 'count'])} ({_pct(c.loc[(t, p), 'share_of_true'])})" for p in ("fake", "real")) + " |")
    lines += [
        "",
        "Percentages are shares of the true class. Figure spec: FIG0014.",
        "",
        "| Class | Support | Predicted | Correct | Precision | Recall | F1 | Error rate |",
        "|-------|---------|-----------|---------|-----------|--------|----|------------|",
    ]
    for _, r in pc.iterrows():
        lines.append(f"| {r['class']} | {r['support']} | {r['predicted']} | {r['correct']} | {r['precision']:.4f} | {r['recall']:.4f} | {r['f1']:.4f} | {r['error_rate']:.4f} |")

    lines += ["", "## Errors by generator and real source (E6)", "",
              "Error rate is FNR for fake generators and FPR for real sources. Interval: Wilson 95%. "
              f"Groups under {MIN_GROUP} images are flagged `small_group` in the CSV and left out here.",
              "",
              "| Class | Group | n | Errors | Error rate | 95% CI | Share of class errors | Mean P(fake) |",
              "|-------|-------|---|--------|------------|--------|-----------------------|--------------|"]
    for _, r in pd.concat([gen, real]).iterrows():
        lines.append(f"| {r['true_label']} | {r['group']} | {r['n']} | {r['errors']} | {_pct(r['error_rate'])} | "
                     f"{_pct(r['ci_low'])}–{_pct(r['ci_high'])} | {_pct(r['share_of_class_errors'])} | {r['mean_prob']:.3f} |")

    fp, fn = s.loc["false_positive"], s.loc["false_negative"]
    lines += [
        "",
        "## FP and FN summary (E6)",
        "",
        "| Error | Count | Within 0.1 of threshold | Confidence ≥ 0.9 | Mean P(fake) |",
        "|-------|-------|-------------------------|------------------|--------------|",
        f"| false positive (real → fake) | {fp['count']} | {fp['near_threshold']} ({_pct(fp['near_threshold_share'])}) | {fp['high_confidence']} ({_pct(fp['high_confidence_share'])}) | {fp['mean_prob']:.3f} |",
        f"| false negative (fake → real) | {fn['count']} | {fn['near_threshold']} ({_pct(fn['near_threshold_share'])}) | {fn['high_confidence']} ({_pct(fn['high_confidence_share'])}) | {fn['mean_prob']:.3f} |",
        "",
        f"`error_cases.csv` lists the {len(fp_cases) and int(fp_cases.sum())} most confident false positives and "
        f"{len(fn_cases) and int(fn_cases.sum())} most confident false negatives per split for manual review. "
        f"On `{split}` the false positives come from " + ", ".join(f"`{k}` ({v})" for k, v in fp_cases.items())
        + "; the false negatives from " + ", ".join(f"`{k}` ({v})" for k, v in fn_cases.items()) + ".",
        "",
        "## Failure categories (E12)",
        "",
        "| Category | Evidence available | Observation | Possible causes (hypotheses) | How to check |",
        "|----------|--------------------|-------------|------------------------------|--------------|",
        f"| Generator confusion | yes (`generator`) | FNR ranges from {_pct(gen['error_rate'].min())} to {_pct(gen['error_rate'].max())}. "
        f"Above the overall FNR ({_pct(fn_rate)}) with the whole interval: {_names(hard)}. Below it: {_names(easy)}. "
        f"Highest: {_names(top3)}. | These generators may leave fewer of the traces the model relies on for the others; "
        "the 224-px PNG preprocessing may also remove some of their traces. | Leave-one-generator-out (STEP-047, E9); "
        "per-generator Grad-CAM on `error_cases.csv`. |",
        f"| Real-source shift | yes (identity prefix) | FPR by real source: "
        + ", ".join(f"`{r['group']}` {_pct(r['error_rate'])}" for _, r in real.iterrows())
        + f". Above the overall FPR ({_pct(fp_rate)}) with the whole interval: {_names(hard_real)}. | A source that is rare in training "
        "or differs in style (for example artwork portraits) may look unlike the real images the model learned. | "
        "Count each source in train; compare FPR after re-weighting; cross-dataset tests (STEP-047, E8). |",
        f"| Identity confusion | no | `identity` is a file-derived id. {coverage['repeated_identity_images']} `{split}` images share one, "
        f"all from {', '.join(f'`{x}`' for x in coverage['repeated_identity_groups']) or 'no group'}: filename indices, not people. | "
        "Not assessable. | A dataset with person identity labels, or face-recognition clustering. |",
        f"| Compression | no | Every `{split}` image has source format {', '.join(coverage['source_formats'])}. | "
        "Not assessable: no variation to compare. | JPEG-quality perturbations (STEP-046, E7). |",
        f"| Poor quality / resolution | no | Every `{split}` image has original size {', '.join(coverage['original_sizes'])}; no quality score is stored. | "
        "Not assessable. | Blur, noise, and resolution perturbations (STEP-046, E7). |",
        "| Background, lighting, occlusion | no | No annotations for these. | Not assessable. | Manual tagging of `error_cases.csv`; Grad-CAM. |",
        f"| Artifacts | partial | {_pct(fn['high_confidence_share'])} of false negatives have confidence ≥ 0.9 (the model is confidently wrong). | "
        "Some fakes may lack visible artifacts at 224 px, or contain features the model links to real images. | "
        "Grad-CAM on the most confident false negatives (`error_cases.csv`). |",
        f"| Unexpected behaviour | yes | {_pct(fp['near_threshold_share'])} of false positives lie within 0.1 of the threshold, "
        f"against {_pct(fn['near_threshold_share'])} of false negatives. | Many false positives may be borderline rather than confident. | "
        "Threshold trade-offs in `calibration_threshold.md`. |",
        "",
        "## Limits",
        "",
        "- One model, one seed, one split. No statistical test (Phase E11).",
        "- Metadata has no quality, lighting, background, or occlusion fields. Those categories need manual or perturbation-based checks.",
        "- Subgroup intervals are per group and not corrected for multiple comparisons.",
    ]
    return "\n".join(lines) + "\n"
