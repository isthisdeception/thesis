"""Run the configured collectors. One failure does not stop the others, and a failed validation runs none."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from failure_handling import FailureRecord, write_failure

from evidence.collectors import STEP053_TYPES, builtin_collectors
from evidence.item import CollectorContext, EvidenceCollector, EvidenceItem

MODULE_ID = "MOD003"


@dataclass
class CollectionResult:
    items: list[EvidenceItem] = field(default_factory=list)
    failures: list[FailureRecord] = field(default_factory=list)
    ran: bool = False


def run_collectors(
    input_dir: Path,
    storage_root: Path,
    collectors: list[EvidenceCollector],
) -> CollectionResult:
    metadata_path = input_dir / "input_metadata.json"
    validation_path = input_dir / "validation.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    case_id = metadata["case_id"]
    input_id = metadata["input_id"]
    if not validation_path.is_file():
        failure = write_failure(storage_root, name="unexpected_error", module_id=MODULE_ID, case_id=case_id, input_id=input_id, detail="validation record is missing")
        return CollectionResult(failures=[failure], ran=False)
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    if validation.get("status") != "passed":
        failure = write_failure(storage_root, name="unexpected_error", module_id=MODULE_ID, case_id=case_id, input_id=input_id, detail="validation did not pass; collectors did not run")
        return CollectionResult(failures=[failure], ran=False)
    stored = Path(metadata["stored_path"])
    try:
        image = Image.open(stored)
        image.load()
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        failure = write_failure(storage_root, name="corrupted_image", module_id=MODULE_ID, case_id=case_id, input_id=input_id, detail=f"stored image did not open: {exc.__class__.__name__}")
        return CollectionResult(failures=[failure], ran=False)
    context = CollectorContext(
        case_id=case_id,
        input_id=input_id,
        image=image.copy(),
        stored_path=stored,
        validation_status=validation["status"],
    )
    image.close()
    result = CollectionResult(ran=True)
    for collector in collectors:
        try:
            outcome = collector.collect(CollectorContext(
                case_id=context.case_id,
                input_id=context.input_id,
                image=context.image.copy(),
                stored_path=context.stored_path,
                validation_status=context.validation_status,
            ))
        except Exception as exc:
            outcome_name, outcome_detail = "unexpected_error", f"{collector.evidence_type} raised {exc.__class__.__name__}"
            outcome_items = ()
        else:
            outcome_name = outcome.failure_name
            outcome_detail = outcome.failure_detail or collector.evidence_type
            outcome_items = outcome.items
        if outcome_name:
            result.failures.append(write_failure(
                storage_root,
                name=outcome_name,
                module_id=MODULE_ID,
                case_id=case_id,
                input_id=input_id,
                detail=f"{collector.evidence_type}: {outcome_detail}",
            ))
            continue
        result.items.extend(outcome_items)
    payload = [item.to_json() for item in result.items]
    (input_dir / "evidence_items.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return result


def run_registered(
    input_dir: Path,
    storage_root: Path,
    face_counter,
    names: tuple[str, ...] = STEP053_TYPES,
    extras: dict[str, EvidenceCollector] | None = None,
) -> CollectionResult:
    """Resolve collector names. An unknown name fails on its own and does not remove the others."""

    available = builtin_collectors(face_counter)
    if extras:
        available.update(extras)
    metadata = json.loads((input_dir / "input_metadata.json").read_text(encoding="utf-8"))
    chosen: list[EvidenceCollector] = []
    early: list[FailureRecord] = []
    for name in names:
        collector = available.get(name)
        if collector is None:
            early.append(write_failure(
                storage_root,
                name="unexpected_error",
                module_id=MODULE_ID,
                case_id=metadata["case_id"],
                input_id=metadata["input_id"],
                detail=f"{name} is not registered",
            ))
            continue
        chosen.append(collector)
    result = run_collectors(input_dir, storage_root, chosen)
    result.failures = early + result.failures
    return result
