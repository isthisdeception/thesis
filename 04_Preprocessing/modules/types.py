"""Shared types for Phase D9 preprocessing modules (STEP-026)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from PIL import Image


ReasonCode = str


@dataclass
class ModuleError(Exception):
    """Explicit module failure — never swallowed silently."""

    module_id: str
    reason_code: str
    message: str
    path: str | None = None

    def __str__(self) -> str:
        loc = f" path={self.path}" if self.path else ""
        return f"[{self.module_id}] {self.reason_code}: {self.message}{loc}"


@dataclass
class FaceBox:
    """Axis-aligned face box with optional score."""

    x1: float
    y1: float
    x2: float
    y2: float
    score: float = 1.0

    def as_tuple(self) -> tuple[float, float, float, float, float]:
        return (self.x1, self.y1, self.x2, self.y2, self.score)

    def clip(self, width: int, height: int) -> FaceBox:
        return FaceBox(
            x1=max(0.0, min(float(width), self.x1)),
            y1=max(0.0, min(float(height), self.y1)),
            x2=max(0.0, min(float(width), self.x2)),
            y2=max(0.0, min(float(height), self.y2)),
            score=self.score,
        )

    @property
    def width(self) -> float:
        return max(0.0, self.x2 - self.x1)

    @property
    def height(self) -> float:
        return max(0.0, self.y2 - self.y1)


FULL_FRAME = "FULL_FRAME"


@dataclass
class ImageRecord:
    """In-pipeline image state passed between modules."""

    relative_path: str
    dataset_id: str = ""
    image: Image.Image | None = None
    source_path: Path | None = None
    content_hash: str | None = None
    class_label: str | None = None
    generator: str | None = None
    condition: str | None = None
    identity: str | None = None
    split: str | None = None
    age: str | None = None
    gender: str | None = None
    race: str | None = None
    face_boxes: list[FaceBox] = field(default_factory=list)
    primary_face_index: int | None = None
    face_sentinel: str | None = None  # FULL_FRAME when assume crop
    affine_matrix: list[list[float]] | None = None
    crop_box: tuple[int, int, int, int] | None = None
    original_size: tuple[int, int] | None = None
    current_size: tuple[int, int] | None = None
    source_mode: str | None = None
    output_format: str | None = None
    exif_stripped: bool = False
    kept: bool = True
    reason_code: ReasonCode = "OK"
    extras: dict[str, Any] = field(default_factory=dict)

    def ensure_image(self) -> Image.Image:
        if self.image is None:
            raise ModuleError(
                module_id="SHARED",
                reason_code="MISSING_IMAGE",
                message="ImageRecord.image is None",
                path=self.relative_path,
            )
        return self.image

    def sync_size_from_image(self) -> None:
        im = self.ensure_image()
        self.current_size = (im.width, im.height)
        if self.original_size is None:
            self.original_size = (im.width, im.height)
        if self.source_mode is None:
            self.source_mode = im.mode


@dataclass
class ExcludeRow:
    relative_path: str
    reason_code: str
    detail: str = ""


@dataclass
class ErrorRow:
    relative_path: str
    module_id: str
    reason_code: str
    message: str
