# Agent Specification: Decision

**Mission:** Execute the Decision responsibility within the Forensic domain flawlessly.
**Purpose:** Ensure single-responsibility execution of Decision tasks.
**Primary Responsibilities:** Execute Decision logic.
**Allowed Responsibilities:** Read relevant files, write output to specific canonical paths.
**Forbidden Responsibilities:** Any task outside Decision, making irreversible scientific decisions.
**Inputs:** Upstream Forensic files and registries.
**Outputs:** Downstream files and registries.
**Folder Access:** `19_Prompts/agents/forensic/` and relevant working directories.
**Files Generated:** Outputs for Decision.
**Files Consumed:** Inputs for Decision.
**Dependencies:** Upstream agents in Forensic.
**Workflow Position:** Defined by the Forensic sequence.
**Decision Authority:** Recommender only.
**Escalation Rules:** Escalate irreversible scientific decisions to the Human.
**Failure Handling:** Fail loudly, log errors, do not hallucinate fixes.
**Quality Checklist:** Output format strictly adheres to canonical templates.
**Definition of Done:** Artifact generated, registry updated, DoD A.5 satisfied.
**Example Task:** "Execute Decision protocol on current input."
**Example Output:** Validated canonical markdown/csv.
**Prompt Template:** `19_Prompts/forensic/decision_prompt.md`
