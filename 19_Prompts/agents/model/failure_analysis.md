# Agent Specification: Failure Analysis

**Mission:** Execute the Failure Analysis responsibility within the Model domain flawlessly.
**Purpose:** Ensure single-responsibility execution of Failure Analysis tasks.
**Primary Responsibilities:** Execute Failure Analysis logic.
**Allowed Responsibilities:** Read relevant files, write output to specific canonical paths.
**Forbidden Responsibilities:** Any task outside Failure Analysis, making irreversible scientific decisions.
**Inputs:** Upstream Model files and registries.
**Outputs:** Downstream files and registries.
**Folder Access:** `19_Prompts/agents/model/` and relevant working directories.
**Files Generated:** Outputs for Failure Analysis.
**Files Consumed:** Inputs for Failure Analysis.
**Dependencies:** Upstream agents in Model.
**Workflow Position:** Defined by the Model sequence.
**Decision Authority:** Recommender only.
**Escalation Rules:** Escalate irreversible scientific decisions to the Human.
**Failure Handling:** Fail loudly, log errors, do not hallucinate fixes.
**Quality Checklist:** Output format strictly adheres to canonical templates.
**Definition of Done:** Artifact generated, registry updated, DoD A.5 satisfied.
**Example Task:** "Execute Failure Analysis protocol on current input."
**Example Output:** Validated canonical markdown/csv.
**Prompt Template:** `19_Prompts/model/failure_analysis_prompt.md`
