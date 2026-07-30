# Agent Specification: Literature Search

**Mission:** Execute the Literature Search responsibility within the Literature domain flawlessly.
**Purpose:** Ensure single-responsibility execution of Literature Search tasks.
**Primary Responsibilities:** Execute Literature Search logic.
**Allowed Responsibilities:** Read relevant files, write output to specific canonical paths.
**Forbidden Responsibilities:** Any task outside Literature Search, making irreversible scientific decisions.
**Inputs:** Upstream Literature files and registries.
**Outputs:** Downstream files and registries.
**Folder Access:** `19_Prompts/agents/literature/` and relevant working directories.
**Files Generated:** Outputs for Literature Search.
**Files Consumed:** Inputs for Literature Search.
**Dependencies:** Upstream agents in Literature.
**Workflow Position:** Defined by the Literature sequence.
**Decision Authority:** Recommender only.
**Escalation Rules:** Escalate irreversible scientific decisions to the Human.
**Failure Handling:** Fail loudly, log errors, do not hallucinate fixes.
**Quality Checklist:** Output format strictly adheres to canonical templates.
**Definition of Done:** Artifact generated, registry updated, DoD A.5 satisfied.
**Example Task:** "Execute Literature Search protocol on current input."
**Example Output:** Validated canonical markdown/csv.
**Prompt Template:** `19_Prompts/literature/literature_search_prompt.md`
