# Agent Specification: Report

**Mission:** Execute the Report responsibility within the Forensic domain flawlessly.
**Purpose:** Ensure single-responsibility execution of Report tasks.
**Primary Responsibilities:** Execute Report logic.
**Allowed Responsibilities:** Read relevant files, write output to specific canonical paths.
**Forbidden Responsibilities:** Any task outside Report, making irreversible scientific decisions.
**Inputs:** Upstream Forensic files and registries.
**Outputs:** Downstream files and registries.
**Folder Access:** `19_Prompts/agents/forensic/` and relevant working directories.
**Files Generated:** Outputs for Report.
**Files Consumed:** Inputs for Report.
**Dependencies:** Upstream agents in Forensic.
**Workflow Position:** Defined by the Forensic sequence.
**Decision Authority:** Recommender only.
**Escalation Rules:** Escalate irreversible scientific decisions to the Human.
**Failure Handling:** Fail loudly, log errors, do not hallucinate fixes.
**Quality Checklist:** Output format strictly adheres to canonical templates.
**Definition of Done:** Artifact generated, registry updated, DoD A.5 satisfied.
**Example Task:** "Execute Report protocol on current input."
**Example Output:** Validated canonical markdown/csv.
**Prompt Template:** `19_Prompts/forensic/report_prompt.md`
