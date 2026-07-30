# Agent Specification: Citation

**Mission:** Execute the Citation responsibility within the Writing domain flawlessly.
**Purpose:** Ensure single-responsibility execution of Citation tasks.
**Primary Responsibilities:** Execute Citation logic.
**Allowed Responsibilities:** Read relevant files, write output to specific canonical paths.
**Forbidden Responsibilities:** Any task outside Citation, making irreversible scientific decisions.
**Inputs:** Upstream Writing files and registries.
**Outputs:** Downstream files and registries.
**Folder Access:** `19_Prompts/agents/writing/` and relevant working directories.
**Files Generated:** Outputs for Citation.
**Files Consumed:** Inputs for Citation.
**Dependencies:** Upstream agents in Writing.
**Workflow Position:** Defined by the Writing sequence.
**Decision Authority:** Recommender only.
**Escalation Rules:** Escalate irreversible scientific decisions to the Human.
**Failure Handling:** Fail loudly, log errors, do not hallucinate fixes.
**Quality Checklist:** Output format strictly adheres to canonical templates.
**Definition of Done:** Artifact generated, registry updated, DoD A.5 satisfied.
**Example Task:** "Execute Citation protocol on current input."
**Example Output:** Validated canonical markdown/csv.
**Prompt Template:** `19_Prompts/writing/citation_prompt.md`
