"""Named reliability checks. Cutoffs live in ValidationConfig, not in the check names."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationConfig:
    low_confidence_below: float = 0.3
    medium_confidence_below: float = 0.6
    min_sharpness: float = 1.0
    uncertainty_band: float = 0.05
    conflict_tolerance: float = 0.0
    threshold_center: float = 0.5
    unusable_sharpness_below: float | None = None
    max_sharpness: float | None = None
    max_blockiness: float | None = None
    min_freq_change: float | None = None
    max_freq_change: float | None = None
    min_texture: float | None = None
    max_texture: float | None = None
    physical_integrity_conflict: bool = False
    detector_polarity_conflict: bool = False

    @classmethod
    def calibrated_artifact_val(cls) -> "ValidationConfig":
        """Strictly validation-derived bounds from DS0001 SPLIT0001 val quantiles (zero test/OOD tuning)."""
        return cls(
            low_confidence_below=0.3,
            medium_confidence_below=0.6,
            min_sharpness=3.00,
            unusable_sharpness_below=2.65,
            max_sharpness=11.50,
            max_blockiness=1.20,
            min_freq_change=2.55,
            max_freq_change=10.80,
            min_texture=2.35,
            max_texture=10.40,
            threshold_center=0.395057,
            uncertainty_band=0.10,
            conflict_tolerance=0.0,
            physical_integrity_conflict=True,
            detector_polarity_conflict=True,
        )


@dataclass(frozen=True)
class Finding:
    quality: str
    reason: str


def _number(value) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def findings_for(item: dict, config: ValidationConfig) -> list[Finding]:
    """Reliability reasons for one item. An empty confidence is not treated as low."""

    found: list[Finding] = []
    confidence = _number(item.get("confidence"))
    if confidence is not None and confidence < config.low_confidence_below:
        found.append(Finding("low", "low_confidence"))
    elif confidence is not None and confidence < config.medium_confidence_below:
        found.append(Finding("medium", "moderate_confidence"))
    evidence_type = item["evidence_type"]
    raw = item["raw_output"]
    value = item["processed_output"].get("value")
    if evidence_type == "face_detection" and value == 0:
        found.append(Finding("unusable", "face_detection_failure"))
    if evidence_type == "metadata" and (raw.get("byte_size") in (None, "") or not raw.get("pil_format")):
        found.append(Finding("unusable", "incomplete_metadata"))
    if evidence_type == "deep_learning_prediction":
        probability = _number(value)
        center = (
            _number(item["processed_output"].get("threshold"))
            if config.detector_polarity_conflict and _number(item["processed_output"].get("threshold")) is not None
            else config.threshold_center
        )
        if probability is not None and abs(probability - center) <= config.uncertainty_band:
            found.append(Finding("low", "model_uncertainty"))
    if evidence_type == "face_quality":
        sharpness = _number(value)
        if sharpness is not None:
            if config.unusable_sharpness_below is not None and sharpness < config.unusable_sharpness_below:
                found.append(Finding("unusable", "poor_image_quality"))
            elif config.max_sharpness is not None and sharpness > config.max_sharpness:
                found.append(Finding("unusable", "excessive_noise"))
            elif sharpness < config.min_sharpness:
                found.append(Finding("low", "poor_image_quality"))
    if evidence_type == "compression_artifacts" and config.max_blockiness is not None:
        blockiness = _number(value)
        if blockiness is not None and blockiness > config.max_blockiness:
            found.append(Finding("unusable", "compression_degradation"))
    if evidence_type == "frequency_domain":
        freq = _number(value)
        if freq is not None:
            if config.min_freq_change is not None and freq < config.min_freq_change:
                found.append(Finding("unusable", "spectral_detail_loss"))
            elif config.max_freq_change is not None and freq > config.max_freq_change:
                found.append(Finding("unusable", "spectral_noise_spike"))
    if evidence_type == "texture_analysis":
        tex = _number(value)
        if tex is not None:
            if config.min_texture is not None and tex < config.min_texture:
                found.append(Finding("unusable", "texture_degradation"))
            elif config.max_texture is not None and tex > config.max_texture:
                found.append(Finding("unusable", "texture_noise_spike"))
    if evidence_type == "image_statistics":
        variance = _number(raw.get("luminance_variance"))
        if variance == 0:
            found.append(Finding("unusable", "poor_image_quality"))
    if evidence_type == "fused_conclusion":
        found.extend(_fused_findings(item["processed_output"]))
    if evidence_type == "confidence":
        found.extend(_confidence_findings(item["processed_output"]))
    return found


def _confidence_findings(processed: dict) -> list[Finding]:
    """A MOD009 confidence record must carry the four confidence fields."""

    required = ("prediction_confidence", "evidence_confidence", "system_confidence", "decision_confidence")
    if not all(key in processed for key in required) or not processed.get("formula_id"):
        return [Finding("unusable", "confidence_output_incomplete")]
    found: list[Finding] = []
    if processed.get("decision_confidence") is None:
        found.append(Finding("low", "decision_confidence_unavailable"))
    return found


def _fused_findings(processed: dict) -> list[Finding]:
    """A MOD007 item is not more reliable than the evidence under it."""

    summary = processed.get("summary") if isinstance(processed.get("summary"), dict) else None
    if not processed.get("strategy_id") or summary is None:
        return [Finding("unusable", "fused_output_incomplete")]
    found: list[Finding] = []
    lean = summary.get("lean")
    conflicts = summary.get("conflicts") or {}
    if lean == "contested" or conflicts.get("directional"):
        found.append(Finding("low", "fused_conflict"))
    if lean == "no_directional_evidence":
        found.append(Finding("low", "no_directional_evidence"))
    if summary.get("single_source"):
        found.append(Finding("medium", "single_source"))
    return found


def conflicts(items: list[dict], config: ValidationConfig) -> dict[str, list[str]]:
    """Same-type numeric disagreements inside one case. Both ids are returned."""

    groups: dict[str, list[dict]] = {}
    for item in items:
        groups.setdefault(item["evidence_type"], []).append(item)
    partners: dict[str, list[str]] = {item["evidence_id"]: [] for item in items}
    for group in groups.values():
        for left in group:
            left_value = _number(left["processed_output"].get("value"))
            if left_value is None:
                continue
            for right in group:
                if left["evidence_id"] == right["evidence_id"]:
                    continue
                right_value = _number(right["processed_output"].get("value"))
                if right_value is None:
                    continue
                if config.detector_polarity_conflict and left["evidence_type"] == "deep_learning_prediction":
                    t_left = _number(left["processed_output"].get("threshold"))
                    t_right = _number(right["processed_output"].get("threshold"))
                    c_left = config.threshold_center if t_left is None else t_left
                    c_right = config.threshold_center if t_right is None else t_right
                    if (left_value >= c_left) != (right_value >= c_right):
                        partners[left["evidence_id"]].append(right["evidence_id"])
                elif abs(left_value - right_value) > config.conflict_tolerance:
                    partners[left["evidence_id"]].append(right["evidence_id"])
    if config.physical_integrity_conflict:
        physical_types = {"compression_artifacts", "face_quality", "frequency_domain", "texture_analysis"}
        corrupted_ids = [
            item["evidence_id"]
            for item in items
            if item["evidence_type"] in physical_types
            and any(f.quality == "unusable" for f in findings_for(item, config))
        ]
        dl_ids = [item["evidence_id"] for item in items if item["evidence_type"] == "deep_learning_prediction"]
        if corrupted_ids and dl_ids:
            for cid in corrupted_ids:
                for did in dl_ids:
                    if did not in partners[cid]:
                        partners[cid].append(did)
                    if cid not in partners[did]:
                        partners[did].append(cid)
    return partners
