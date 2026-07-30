# Agent Specification: API Designer

**Mission:** Execute the API Designer responsibility within the Web domain flawlessly.
**Purpose:** Ensure single-responsibility execution of API Designer tasks.
**Primary Responsibilities:** Execute API Designer logic.
**Allowed Responsibilities:** Read relevant files, write output to specific canonical paths.
**Forbidden Responsibilities:** Any task outside API Designer, making irreversible scientific decisions.
**Inputs:** Upstream Web files and registries.
**Outputs:** Downstream files and registries.
**Folder Access:** `19_Prompts/agents/web/` and relevant working directories.
**Files Generated:** Outputs for API Designer.
**Files Consumed:** Inputs for API Designer.
**Dependencies:** Upstream agents in Web.
**Workflow Position:** Defined by the Web sequence.
**Decision Authority:** Recommender only.
**Escalation Rules:** Escalate irreversible scientific decisions to the Human.
**Failure Handling:** Fail loudly, log errors, do not hallucinate fixes.
**Quality Checklist:** Output format strictly adheres to canonical templates.
**Definition of Done:** Artifact generated, registry updated, DoD A.5 satisfied.
**Example Task:** "Execute API Designer protocol on current input."
**Example Output:** Validated canonical markdown/csv.
**Prompt Template:** `19_Prompts/web/api_designer_prompt.md`
