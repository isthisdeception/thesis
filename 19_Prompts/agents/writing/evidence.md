# Agent Specification: Evidence

**Mission:** Execute the Evidence responsibility within the Writing domain flawlessly.
**Purpose:** Ensure single-responsibility execution of Evidence tasks.
**Primary Responsibilities:** Execute Evidence logic.
**Allowed Responsibilities:** Read relevant files, write output to specific canonical paths.
**Forbidden Responsibilities:** Any task outside Evidence, making irreversible scientific decisions.
**Inputs:** Upstream Writing files and registries.
**Outputs:** Downstream files and registries.
**Folder Access:** `19_Prompts/agents/writing/` and relevant working directories.
**Files Generated:** Outputs for Evidence.
**Files Consumed:** Inputs for Evidence.
**Dependencies:** Upstream agents in Writing.
**Workflow Position:** Defined by the Writing sequence.
**Decision Authority:** Recommender only.
**Escalation Rules:** Escalate irreversible scientific decisions to the Human.
**Failure Handling:** Fail loudly, log errors, do not hallucinate fixes.
**Quality Checklist:** Output format strictly adheres to canonical templates.
**Definition of Done:** Artifact generated, registry updated, DoD A.5 satisfied.
**Example Task:** "Execute Evidence protocol on current input."
**Example Output:** Validated canonical markdown/csv.
**Prompt Template:** `19_Prompts/writing/evidence_prompt.md`
