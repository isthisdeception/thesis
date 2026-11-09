"""Grad-CAM as numeric maps. Nothing is drawn."""

from __future__ import annotations

import torch


def grad_cam_map(activations: torch.Tensor, gradients: torch.Tensor) -> torch.Tensor:
    """Return one map per image, normalized to [0, 1].

    ``activations`` and ``gradients`` are ``(batch, channels, height, width)`` from the same layer.
    """

    if activations.shape != gradients.shape or activations.ndim != 4:
        raise ValueError(f"activations and gradients must share shape (N, C, H, W), got {tuple(activations.shape)} and {tuple(gradients.shape)}")
    weights = gradients.detach().mean(dim=(2, 3), keepdim=True)
    cam = torch.relu((weights * activations.detach()).sum(dim=1))
    flat = cam.flatten(1)
    minimum = flat.min(dim=1).values.view(-1, 1, 1)
    maximum = flat.max(dim=1).values.view(-1, 1, 1)
    scale = (maximum - minimum).clamp_min(1e-12)
    return (cam - minimum) / scale


def maps_to_rows(image_ids: list[str], maps: torch.Tensor) -> list[dict]:
    """Long-form rows: one per spatial cell. This is the file form of a map, not an image."""

    if maps.ndim != 3 or maps.shape[0] != len(image_ids):
        raise ValueError("maps must be (N, H, W) and match image_ids")
    rows = []
    for index, image_id in enumerate(image_ids):
        grid = maps[index].detach().cpu()
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                rows.append({"id": image_id, "row": row, "col": col, "value": float(grid[row, col])})
    return rows
