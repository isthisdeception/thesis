# 20_Archive

**Purpose:** Read-only storage of completed/superseded artifacts (Phase W19 Archiving Policy).

## Contents
Submitted final thesis PDFs, journal submission snapshots, retired designs, and cryptographic checksum manifests.

## Workflow
Human writes on archival events, anyone reads. **No modifications after placement.** If a submitted deliverable is later revised (e.g., post-defense or journal R1 revision), supersede it with a new versioned directory (e.g., `thesis_v1.1/`) rather than overwriting an archived folder.

## Expected Archival Layout (Read-Only Upon Placement)
- `20_Archive/thesis_v1.0/` — Final human-compiled thesis PDF (`thesis_v1.0.pdf`) and `SHA256SUMS.txt` placed per `15_Writing/THESIS_SUBMISSION_RUNBOOK.md` (Checklist 17 / STEP-074).
- `20_Archive/journal_v1.1/` — Reserved for final submitted journal manuscript package (Checklist 16 / STEP-075).

## Owner
Human

## Related Folders
`15_Writing`, `09_Figures`, `10_Tables`

## Expected Outputs
Archived read-only deliverables (`thesis_v1.0.pdf`, `SHA256SUMS.txt`)

> *This folder follows the canonical repository hygiene and naming rules defined in `MASTER_RESEARCH_OPERATING_SYSTEM.md`. Please refer to the handbook for full policy details.*
