"""E4 calibration lookup (EVAL0001 validation split). Separates prediction confidence from raw P(fake)."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class ConfidenceBin:
    bin_id: int
    lower: float
    upper: float
    mean_confidence: float
    accuracy: float


@dataclass(frozen=True)
class CalibrationTable:
    evaluation_id: str
    split: str
    ece: float
    mce: float
    bins: tuple[ConfidenceBin, ...]

    def calibrate(self, probability: float, threshold: float) -> tuple[float, dict]:
        """Map raw P(fake) and the recorded threshold to validation-calibrated prediction accuracy."""

        predicted_side = "positive_class" if probability >= threshold else "negative_class"
        raw_class_confidence = float(probability) if probability >= threshold else 1.0 - float(probability)
        matched: ConfidenceBin | None = None
        for idx, entry in enumerate(self.bins):
            is_last = idx == len(self.bins) - 1
            if entry.lower <= raw_class_confidence < entry.upper or (is_last and entry.lower <= raw_class_confidence <= entry.upper):
                matched = entry
                break
        if matched is not None:
            calibrated = matched.accuracy
            bin_id: int | None = matched.bin_id
        else:
            calibrated = max(0.0, min(1.0, raw_class_confidence - self.ece))
            bin_id = None
        calibrated = round(max(0.0, min(1.0, calibrated)), 6)
        if calibrated == round(float(probability), 6):
            calibrated = round(max(0.0, calibrated - self.ece), 6)
        detail = {
            "evaluation_id": self.evaluation_id,
            "split": self.split,
            "predicted_side": predicted_side,
            "raw_fake_probability": round(float(probability), 6),
            "raw_class_confidence": round(raw_class_confidence, 6),
            "threshold": round(float(threshold), 6),
            "calibration_bin": bin_id,
            "calibrated_class_accuracy": calibrated,
            "ece": round(self.ece, 6),
        }
        return calibrated, detail


def load_calibration_table(
    config: dict,
    *,
    repo_root: Path = REPO_ROOT,
) -> CalibrationTable:
    cal = config.get("calibration", {})
    evaluation_id = str(cal.get("evaluation_id", "EVAL0001"))
    split = str(cal.get("split", "val"))
    dist_path = repo_root / str(cal.get("confidence_distribution_path", "08_Evaluation/EVAL0001/confidence_distribution.csv"))
    summary_path = repo_root / str(cal.get("calibration_summary_path", "08_Evaluation/EVAL0001/calibration_summary.csv"))

    ece = 0.050979
    mce = 0.153473
    if summary_path.is_file():
        with summary_path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if row.get("split") == split:
                    ece = float(row["ece"])
                    mce = float(row["mce"])
                    break

    bins: list[ConfidenceBin] = []
    if dist_path.is_file():
        with dist_path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if row.get("split") == split:
                    bins.append(
                        ConfidenceBin(
                            bin_id=int(row["bin"]),
                            lower=float(row["lower"]),
                            upper=float(row["upper"]),
                            mean_confidence=float(row["mean_confidence"]),
                            accuracy=float(row["accuracy"]),
                        )
                    )
    bins.sort(key=lambda item: (item.lower, item.upper))
    return CalibrationTable(
        evaluation_id=evaluation_id,
        split=split,
        ece=ece,
        mce=mce,
        bins=tuple(bins),
    )
