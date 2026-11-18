"""Read-only adapter over `evidence_registry.csv`, `decision.json`, `explanation.json`, and `reasoning.json`."""

from __future__ import annotations

import json
from typing import Any

from apps.core.config import BackendConfig, ensure_forensic_sys_path

ensure_forensic_sys_path()
from evidence.registry.writer import read_rows  # noqa: E402
from evidence.validation.validate import _load_item  # noqa: E402
from fusion.interface import safe_raw  # noqa: E402


def read_case_evidence(
    config: BackendConfig,
    case_id: str,
    *,
    validated_only: bool = False,
) -> dict[str, Any]:
    """Return `MOD005`/`MOD006` evidence items for `case_id` with server filesystem paths stripped."""

    items: list[dict[str, Any]] = []
    if config.evidence_registry_path.is_file():
        for row in read_rows(config.evidence_registry_path):
            loaded = _load_item(row)
            if loaded["raw_output"].get("case_id") != case_id:
                continue
            if validated_only and loaded["source_module"] != "MOD006":
                continue
            loaded["raw_output"] = safe_raw(loaded["raw_output"])
            items.append(loaded)
    return {
        "case_id": case_id,
        "evidence_ids": [item["evidence_id"] for item in items],
        "count": len(items),
        "items": items,
    }


def read_case_decision(config: BackendConfig, case_id: str) -> dict[str, Any] | None:
    """Return `decision.json` written by `MOD008` unchanged (`MOD013_spec.md`)."""

    path = config.media_root / case_id / "decision.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def read_case_explanation(
    config: BackendConfig,
    case_id: str,
    *,
    include_reasoning: bool = False,
) -> dict[str, Any] | None:
    """Return `explanation.json` written by `MOD010` (plus `reasoning.json` from `MOD011` when requested)."""

    expl_path = config.media_root / case_id / "explanation.json"
    if not expl_path.is_file():
        return None
    payload = json.loads(expl_path.read_text(encoding="utf-8"))
    if include_reasoning:
        reas_path = config.media_root / case_id / "reasoning.json"
        payload["reasoning"] = json.loads(reas_path.read_text(encoding="utf-8")) if reas_path.is_file() else None
    return payload
