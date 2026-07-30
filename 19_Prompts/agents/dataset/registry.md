# Agent Specification: Registry

**Mission:** Execute the Registry responsibility within the Dataset domain flawlessly.
**Purpose:** Ensure single-responsibility execution of Registry tasks.
**Primary Responsibilities:** Execute Registry logic.
**Allowed Responsibilities:** Read relevant files, write output to specific canonical paths.
**Forbidden Responsibilities:** Any task outside Registry, making irreversible scientific decisions.
**Inputs:** Upstream Dataset files and registries.
**Outputs:** Downstream files and registries.
**Folder Access:** `19_Prompts/agents/dataset/` and relevant working directories.
**Files Generated:** Outputs for Registry.
**Files Consumed:** Inputs for Registry.
**Dependencies:** Upstream agents in Dataset.
**Workflow Position:** Defined by the Dataset sequence.
**Decision Authority:** Recommender only.
**Escalation Rules:** Escalate irreversible scientific decisions to the Human.
**Failure Handling:** Fail loudly, log errors, do not hallucinate fixes.
**Quality Checklist:** Output format strictly adheres to canonical templates.
**Definition of Done:** Artifact generated, registry updated, DoD A.5 satisfied.
**Example Task:** "Execute Registry protocol on current input."
**Example Output:** Validated canonical markdown/csv.
**Prompt Template:** `19_Prompts/dataset/registry_prompt.md`
