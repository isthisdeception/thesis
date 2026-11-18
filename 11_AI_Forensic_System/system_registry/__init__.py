"""MOD017 System Registry and MOD018 Future Modality Support verification."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

FORENSIC_ROOT = Path(__file__).resolve().parents[1]
MODULE_REGISTRY_PATH = FORENSIC_ROOT / "module_registry.csv"
SPECS_DIR = FORENSIC_ROOT / "specs"
EXPECTED_MODULE_IDS = tuple(f"MOD{i:03d}" for i in range(1, 19))
HEADER = [
    "Module ID",
    "Responsibilities",
    "Inputs",
    "Outputs",
    "Dependencies",
    "Version",
    "Status",
    "Owner",
    "Future Extensions",
    "Created",
    "Updated",
]
REQUIRED_SPEC_SECTIONS = (
    "**Module ID:**",
    "**Name:**",
    "**Version:**",
    "**Status:**",
    "**Purpose:**",
    "**Inputs:**",
    "**Outputs:**",
    "**Dependencies:**",
    "**Configuration:**",
    "**Testing:**",
    "**Future Extensions:**",
    "**Interfaces:**",
    "**Failure Handling:**",
)


@dataclass(frozen=True)
class ModalityProposal:
    kind: str  # "collector" | "fusion_strategy" | "llm_reasoner"
    name: str
    owner_module: str
    contract: str  # "EvidenceCollector" | "FusionStrategy" | "verify_sentence"
    calls_other_collectors: bool = False
    decision_reads_image: bool = False
    cites_ev_ids: bool = True


def validate_module_registry(
    registry_path: Path = MODULE_REGISTRY_PATH,
    specs_dir: Path = SPECS_DIR,
) -> list[dict[str, str]]:
    """Verify MOD001-MOD018 registry rows and their specs (MOD017)."""

    with registry_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = [col.strip() for col in next(reader, [])]
        if header != HEADER:
            raise ValueError(f"module_registry.csv header mismatch: {header}")
        rows = [{header[i]: val.strip() for i, val in enumerate(r)} for r in reader if r]

    ids = tuple(r["Module ID"] for r in rows)
    if ids != EXPECTED_MODULE_IDS:
        raise ValueError(f"expected MOD001..MOD018, found {ids}")

    for row in rows:
        mid = row["Module ID"]
        if not row["Responsibilities"]:
            raise ValueError(f"{mid} has empty Responsibilities")
        if mid == "MOD008" and "image" in row["Inputs"].lower():
            raise ValueError("MOD008 Inputs must not name the image")
        spec_path = specs_dir / f"{mid}_spec.md"
        if not spec_path.is_file():
            raise ValueError(f"missing spec file for {mid}: {spec_path}")
        text = spec_path.read_text(encoding="utf-8")
        missing = [sec for sec in REQUIRED_SPEC_SECTIONS if sec not in text]
        if missing:
            raise ValueError(f"{spec_path.name} missing required sections: {missing}")
    return rows


def validate_modality_proposal(proposal: ModalityProposal) -> tuple[bool, str]:
    """Check whether a new modality proposal honours MOD018 invariants."""

    if not proposal.name or not proposal.owner_module:
        return False, "proposal is missing name or owner_module"
    if proposal.decision_reads_image:
        return False, "rejected: Decision Engine (MOD008) may never read the image or file"
    if proposal.kind == "collector":
        if proposal.contract != "EvidenceCollector":
            return False, "collector proposal must implement EvidenceCollector"
        if proposal.calls_other_collectors:
            return False, "collector proposal must not call other collectors"
        return True, "accepted"
    if proposal.kind == "fusion_strategy":
        if proposal.contract != "FusionStrategy":
            return False, "fusion strategy proposal must implement FusionStrategy"
        return True, "accepted"
    if proposal.kind == "llm_reasoner":
        if not proposal.cites_ev_ids:
            return False, "llm_reasoner proposal must cite EV ids and pass verify_sentence"
        return True, "accepted"
    return False, f"unknown proposal kind {proposal.kind!r}"


__all__ = [
    "EXPECTED_MODULE_IDS",
    "HEADER",
    "MODULE_REGISTRY_PATH",
    "ModalityProposal",
    "REQUIRED_SPEC_SECTIONS",
    "SPECS_DIR",
    "validate_modality_proposal",
    "validate_module_registry",
]
