"""File and image metadata that is present. Absent fields stay absent."""

from __future__ import annotations

from evidence.item import CollectorContext, CollectorOutcome, make_item

EVIDENCE_TYPE = "metadata"


def _present(info: dict) -> dict:
    kept = {}
    for key, value in info.items():
        if isinstance(value, (str, int, float, bool)) or value is None:
            kept[str(key)] = value
    return kept


class MetadataCollector:
    evidence_type = EVIDENCE_TYPE

    def collect(self, context: CollectorContext) -> CollectorOutcome:
        path = context.stored_path
        if not path.is_file():
            return CollectorOutcome.failed("unexpected_error", f"stored file is missing: {path.name}")
        present = _present(dict(context.image.info))
        raw = {
            "input_id": context.input_id,
            "case_id": context.case_id,
            "filename": path.name,
            "byte_size": path.stat().st_size,
            "pil_format": context.image.format,
            "mode": context.image.mode,
            "info": present,
        }
        item = make_item(
            evidence_type=self.evidence_type,
            description=f"file {path.name} is {raw['byte_size']} bytes, format {raw['pil_format']}",
            raw_output=raw,
            value={"byte_size": raw["byte_size"], "pil_format": raw["pil_format"]},
            unit="byte",
        )
        return CollectorOutcome.one(item)
