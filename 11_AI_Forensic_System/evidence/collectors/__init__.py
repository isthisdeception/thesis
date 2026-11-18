"""STEP-053 collectors. Each module is imported here and does not import its siblings."""

from __future__ import annotations

from evidence.collectors.color_distribution import ColorDistributionCollector
from evidence.collectors.compression_artifacts import CompressionArtifactCollector
from evidence.collectors.explainability_input import ExplainabilityInputCollector
from evidence.collectors.face_detection import FaceCounter, FaceDetectionCollector
from evidence.collectors.face_quality import FaceQualityCollector
from evidence.collectors.frequency_domain import FrequencyDomainCollector
from evidence.collectors.image_statistics import ImageStatisticsCollector
from evidence.collectors.metadata import MetadataCollector
from evidence.collectors.texture_analysis import TextureAnalysisCollector
from evidence.item import EvidenceCollector

# deep_learning_prediction is STEP-054 and is not in this list.
STEP053_TYPES = (
    "image_statistics",
    "metadata",
    "face_detection",
    "face_quality",
    "frequency_domain",
    "compression_artifacts",
    "color_distribution",
    "texture_analysis",
    "explainability_input",
)


def builtin_collectors(face_counter: FaceCounter) -> dict[str, EvidenceCollector]:
    return {
        "image_statistics": ImageStatisticsCollector(),
        "metadata": MetadataCollector(),
        "face_detection": FaceDetectionCollector(face_counter),
        "face_quality": FaceQualityCollector(),
        "frequency_domain": FrequencyDomainCollector(),
        "compression_artifacts": CompressionArtifactCollector(),
        "color_distribution": ColorDistributionCollector(),
        "texture_analysis": TextureAnalysisCollector(),
        "explainability_input": ExplainabilityInputCollector(),
    }
