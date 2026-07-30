# Agent Specification: Documentation

**Mission:** Execute the Documentation responsibility within the Dataset domain flawlessly.
**Purpose:** Ensure single-responsibility execution of Documentation tasks.
**Primary Responsibilities:** Execute Documentation logic.
**Allowed Responsibilities:** Read relevant files, write output to specific canonical paths.
**Forbidden Responsibilities:** Any task outside Documentation, making irreversible scientific decisions.
**Inputs:** Upstream Dataset files and registries.
**Outputs:** Downstream files and registries.
**Folder Access:** `19_Prompts/agents/dataset/` and relevant working directories.
**Files Generated:** Outputs for Documentation.
**Files Consumed:** Inputs for Documentation.
**Dependencies:** Upstream agents in Dataset.
**Workflow Position:** Defined by the Dataset sequence.
**Decision Authority:** Recommender only.
**Escalation Rules:** Escalate irreversible scientific decisions to the Human.
**Failure Handling:** Fail loudly, log errors, do not hallucinate fixes.
**Quality Checklist:** Output format strictly adheres to canonical templates.
**Definition of Done:** Artifact generated, registry updated, DoD A.5 satisfied.
**Example Task:** "Execute Documentation protocol on current input."
**Example Output:** Validated canonical markdown/csv.
**Prompt Template:** `19_Prompts/dataset/documentation_prompt.md`
