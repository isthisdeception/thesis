# Agent Specification: Fusion

**Mission:** Execute the Fusion responsibility within the Forensic domain flawlessly.
**Purpose:** Ensure single-responsibility execution of Fusion tasks.
**Primary Responsibilities:** Execute Fusion logic.
**Allowed Responsibilities:** Read relevant files, write output to specific canonical paths.
**Forbidden Responsibilities:** Any task outside Fusion, making irreversible scientific decisions.
**Inputs:** Upstream Forensic files and registries.
**Outputs:** Downstream files and registries.
**Folder Access:** `19_Prompts/agents/forensic/` and relevant working directories.
**Files Generated:** Outputs for Fusion.
**Files Consumed:** Inputs for Fusion.
**Dependencies:** Upstream agents in Forensic.
**Workflow Position:** Defined by the Forensic sequence.
**Decision Authority:** Recommender only.
**Escalation Rules:** Escalate irreversible scientific decisions to the Human.
**Failure Handling:** Fail loudly, log errors, do not hallucinate fixes.
**Quality Checklist:** Output format strictly adheres to canonical templates.
**Definition of Done:** Artifact generated, registry updated, DoD A.5 satisfied.
**Example Task:** "Execute Fusion protocol on current input."
**Example Output:** Validated canonical markdown/csv.
**Prompt Template:** `19_Prompts/forensic/fusion_prompt.md`
