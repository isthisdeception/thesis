# EXP0001 evaluation inputs (STEP-041)

Derived from the training prediction CSVs. The model was not run again. No figures are rendered.

| File | Contents |
|------|----------|
| `predictions.csv` | `split, id, y_true, y_prob, y_pred, threshold, processed_path, generator`. `id` is `content_hash`. `y_true` is 1 when the label is `fake`. |
| `confusion.csv` | One row per true/predicted label pair, for `val` and `test`, at the recorded threshold. |
| `roc_curve.csv` | `split, fpr, tpr, threshold` |
| `pr_curve.csv` | `split, precision, recall, threshold` |
| `calibration.csv` | 15 equal-width bins: `split, bin, lower, upper, count, mean_confidence, fraction_positive` |
| `gradcam_sample.csv` | Eight test cases (two each of true positive, true negative, false positive, false negative) and the layer name `layer4`. This is the case list, not the maps. |
| `manifest.json` | SHA-256 of the source prediction files. |

Source files: `06_Experiments/EXP0001/predictions/{val,test}_predictions.csv`. One validation row sits within `1e-5` of the threshold because the CSV rounded the probability. The saved decision is kept.

Grad-CAM maps are numbers, produced by `17_Automation/evaluation_trigger/gradcam.py` when `MODEL0001_export.pkl` and the images are mounted. They are not in this folder. ResNet-50 has no separate feature-importance table.

Regenerate from `17_Automation/`:

```text
python -m evaluation_trigger --experiment EXP0001 --positive-class fake --negative-class real
```
