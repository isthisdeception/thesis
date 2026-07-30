<!--
============================================================================
 PROJECT EXECUTION BLUEPRINT
 The executable implementation roadmap for the AI Digital Forensics project.
============================================================================
 This document is SUBORDINATE to MASTER_RESEARCH_OPERATING_SYSTEM.md.
 It does not redesign, invent, or contradict the handbook. It converts the
 approved architecture into 78 sequential, session-sized implementation steps
 that run from Day 1 (Literature Review) to Thesis Submission, Journal
 Submission, and Project Archival. Where this document is ever silent or
 ambiguous, the handbook governs.
============================================================================
-->

# PROJECT EXECUTION BLUEPRINT

### The Execution Manual of the AI Digital Forensics Research Laboratory

| Field | Value |
|---|---|
| **Document Title** | `PROJECT_EXECUTION_BLUEPRINT.md` |
| **Document Type** | Execution Playbook (derived, operational) |
| **Architectural Authority** | `MASTER_RESEARCH_OPERATING_SYSTEM.md` v1.0.0 (the *only* source of truth) |
| **Purpose** | Tell the researcher exactly *what to do next* at every stage |
| **Scope** | Literature → Data → Models → Forensic System → Evaluation → Web → Writing → Thesis → Journal → Archival |
| **Total Steps** | 78 sequential steps (STEP-001 … STEP-078) |
| **Execution Environment** | Cursor → Google Antigravity → GitHub → Kaggle → GitHub → Cursor (no local development) |
| **Executable by** | One undergraduate researcher using AI assistance |

---

## How To Use This Blueprint

1. **The handbook rules; this document sequences.** Every step cites the exact handbook sections it implements. If a step ever appears to conflict with the handbook, **stop and follow the handbook** ([§1 Constitution](MASTER_RESEARCH_OPERATING_SYSTEM.md#1-project-constitution)).
2. **Steps are strictly sequential unless marked Parallelizable.** Never begin a step before its Prerequisites exist. Never assume prior work is done — verify it with the step's Verification Checklist.
3. **Every step is one focused work session** ([§O4](MASTER_RESEARCH_OPERATING_SYSTEM.md#12-daily-research-operating-workflow)): one objective, one deliverable, one verification, one Definition of Done.
4. **Two AI roles, never mixed** ([§10.1](MASTER_RESEARCH_OPERATING_SYSTEM.md#101-core-philosophy--platform-responsibilities)):
   - **Cursor** = plan, architect, review, verify, document. **Cursor never writes production code.**
   - **Google Antigravity** = implement only, against the plan Cursor produced.
   Each step therefore contains a **Cursor Prompt** (planning/verification) and, where implementation is required, a **Google Antigravity Prompt** (implementation only).
5. **GitHub is the single source of truth.** Every step ends synchronized to GitHub. **Kaggle is the only execution/training environment.** No step requires local execution.
6. **The human owns all irreversible scientific decisions** ([§1.9](MASTER_RESEARCH_OPERATING_SYSTEM.md#19-human-in-the-loop-rule)). Steps that require a human decision say so explicitly and follow the [Human Task Protocol (A.8)](MASTER_RESEARCH_OPERATING_SYSTEM.md#a8-human-task-protocol).
7. **A step is Done only when the universal [Definition of Done (A.5)](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) passes** — objective met, reproducible, documented, registry updated, committed+pushed, quality gate PASS, reproducible by another researcher, survives peer review.

---

## Ordering Note (Handbook-Driven Reconciliation)

The handbook mandates that **every artifact has exactly one home in the repository** ([§2](MASTER_RESEARCH_OPERATING_SYSTEM.md#2-repository-architecture)) and that **repository initialization is Phase 1 of the infrastructure workflow** ([§10 Phase 1](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-1--repository-initialization)). Because literature registries (`papers.csv`, etc.) cannot exist without the repository and its registries, the **repository skeleton, template library, and registries are bootstrapped first** (Part 1, STEP-002…007), *before* Literature Review. This is not a redesign — it is the handbook's own dependency order.

The heavier **engineering environment hardening** (dependency pinning, `versions.lock.md`, Kaggle sync, Git LFS) is completed later, in Part 6 (STEP-030…031), immediately before training, per [§10 Phase 16](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-16--environment-management). Thus "Repository Initialization" and "Environment Setup" from the requested stage list are split across Part 1 (skeleton) and Part 6 (hardening), exactly where each is first needed.

---

## Legend

- **[H]** Human-only action (irreversible scientific decision or manual download/upload) — [A.8](MASTER_RESEARCH_OPERATING_SYSTEM.md#a8-human-task-protocol).
- **[C]** Cursor session (planning/architecture/review/verification — no code).
- **[A]** Google Antigravity session (implementation only).
- **[K]** Kaggle session (execution/training only).
- **GATE** This step contains a mandatory [Quality Gate](MASTER_RESEARCH_OPERATING_SYSTEM.md#132-quality-gates); the next phase cannot begin until it PASSes.

---

## Stage → Step Map

| Stage | Steps | Handbook |
|---|---|---|
| Research Foundation & Repository Bootstrap | 001–007 | §1, §2, §10, §11, §14 |
| Literature Review | 008–013 | §3 (L1–L7) |
| Research Gap & Direction | 014–017 | §3 (L8–L12), Checklist 2 |
| Dataset Discovery → Documentation | 018–024 | §4 (D1–D8), Checklist 3 |
| Preprocessing → Splits → Registry | 025–029 | §4 (D9–D15), Checklist 4 |
| Environment & Model Foundation | 030–034 | §10 P16, §4 D19, §5 (M1–M4) |
| Experiment / Training / Checkpoint | 035–041 | §5 (M5–M16), §10 P7–P8, Checklists 5–7 |
| Evaluation Pipeline | 042–050 | §7 (E1–E18), Checklist 8 |
| AI Forensic Analyst | 051–059 | §6 (Modules 1–19), E14, Checklist 9 |
| Backend Development | 060–062 | §8.4–§8.5, Checklist 11 |
| Frontend Development | 063–065 | §8.3, Checklist 10 |
| System Integration & Testing | 066–067 | §8.9, Checklists 10–11 |
| Documentation | 068 | §16, Checklist 12 |
| Writing | 069–072 | §9 (W1–W17), Checklist 13 |
| Thesis Submission | 073–074 | §9 W18, Checklists 17 & 19 |
| Journal Submission | 075–076 | §9 W6/W14, Checklist 16 |
| Project Archival | 077–078 | §10 P12, §9 W19, Checklist 18 |

---

## Master Dependency Chain (Quality-Gated)

```
Foundation(001-007)
   → Literature(008-013) → [GATE Checklist 2](017)
   → Dataset(018-024) → [GATE Checklist 3](024)
   → Preprocessing(025-029) → [GATE Checklist 4](029)
   → Environment+Models(030-034)
   → Experiment/Training(035-041) → [GATE Checklists 5,6,7]
   → Evaluation(042-050) → [GATE Checklist 8](050)
   → Forensic Analyst(051-059) → [GATE Checklist 9](059)
   → Backend(060-062) → [GATE Checklist 11](062)
   → Frontend(063-065) → [GATE Checklist 10](065)
   → Integration+Testing(066-067)
   → Documentation(068) → [GATE Checklist 12]
   → Writing(069-072) → [GATE Checklist 13](072)
   → Thesis(073-074) → [GATE Checklists 19,17]
   → Journal(075-076) → [GATE Checklist 16]
   → Archival(077-078) → [GATE Checklist 18]
```

The model→evaluation loop (035–050) and the module loop (051–059) are **iterated** for each additional experiment, ablation, generator hold-out, and evidence collector, as the handbook requires ([§5 M12–M14](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system), [§7 E9–E10](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol)). Each iteration reuses the same steps with a new immutable `EXP`/`EVAL` ID.

---
# PART 1 — RESEARCH FOUNDATION & REPOSITORY BOOTSTRAP

> Implements [§1 Constitution](MASTER_RESEARCH_OPERATING_SYSTEM.md#1-project-constitution), [§2 Repository Architecture](MASTER_RESEARCH_OPERATING_SYSTEM.md#2-repository-architecture), [§10 Infrastructure](MASTER_RESEARCH_OPERATING_SYSTEM.md#10-github--kaggle--antigravity-workflow), [§11 Agents](MASTER_RESEARCH_OPERATING_SYSTEM.md#11-agent-framework), [§14 Templates](MASTER_RESEARCH_OPERATING_SYSTEM.md#14-template-library), and [Appendix A/B](MASTER_RESEARCH_OPERATING_SYSTEM.md#appendix-a--canonical-definitions). Nothing in Literature/Dataset/Model can start until the repository has a home for its registries.

---

## STEP-001 — Ratify the Handbook & Resolve Deferred Decisions  **[H][C]**

**Title:** Human ratification of the operating system and recording of DEF-001…DEF-004.

**Objective:** Convert the handbook from *Authoritative Draft* to *Ratified*, and record the human's position on the four deferred decisions and the fixed stack/license/repo name, so all later steps have a settled foundation.

**Why this step exists:** The handbook's [Appendix F](MASTER_RESEARCH_OPERATING_SYSTEM.md#appendix-f--self-review--validation-record) states it is a *draft pending human ratification* of the [deferred decisions (§1.11)](MASTER_RESEARCH_OPERATING_SYSTEM.md#111-deferred-decisions), technology stack, license, and repository name. No implementation may begin against an unratified source of truth ([§1.10 Planning-Before-Implementation](MASTER_RESEARCH_OPERATING_SYSTEM.md#110-planning-before-implementation)).

**Handbook References:** [Cover Page](MASTER_RESEARCH_OPERATING_SYSTEM.md#cover-page); [§1.4 Fixed Technology Stack](MASTER_RESEARCH_OPERATING_SYSTEM.md#14-fixed-technology-stack); [§1.11 Deferred Decisions](MASTER_RESEARCH_OPERATING_SYSTEM.md#111-deferred-decisions); [Appendix F](MASTER_RESEARCH_OPERATING_SYSTEM.md#appendix-f--self-review--validation-record); [Template 3 — Decision Log](MASTER_RESEARCH_OPERATING_SYSTEM.md#14-template-library).

**Prerequisites:** `MASTER_RESEARCH_OPERATING_SYSTEM.md` exists and has been read by the human.

**Estimated Difficulty:** Easy.
**Estimated Time:** 1–2 hours.
**Parallelizable:** No — every later step depends on the ratified decisions.

**Inputs:** `MASTER_RESEARCH_OPERATING_SYSTEM.md`.

**Expected Outputs:**
- A ratification note recording: stack confirmed, license chosen, canonical repository name (`ai-digital-forensics` unless the human overrides), and the human's stance on DEF-001…DEF-004 (kept deferred with the handbook's decision criteria, or pre-decided).
- Handbook cover-page status set to *Ratified* with a version-table row.

**Repository Changes:** *(The repo does not exist yet; these files are created in STEP-002 and this decision is committed there.)* Prepare the content of `01_Project_Management/decision_log/DEC0001.md` (handbook ratification) using [Template 3](MASTER_RESEARCH_OPERATING_SYSTEM.md#14-template-library) and the edit to the handbook cover page/version table.

**Cursor Prompt:**
```
You are the planning agent. Do NOT write code.
Read MASTER_RESEARCH_OPERATING_SYSTEM.md fully.
Produce, as text only:
1. A concise ratification summary listing: the fixed technology stack (§1.4), a recommended open-source LICENSE for an undergraduate research project (state 2 options + recommendation + objective criteria), and the canonical repository name.
2. For each deferred decision DEF-001..DEF-004 (§1.11): restate the topic, the decision criteria, whether it blocks any near-term step, and a recommendation to KEEP DEFERRED or DECIDE NOW with justification.
3. A ready-to-save DEC0001.md following Template 3 (Decision ID, Date, Problem, Options, Chosen Option, Rejected Options, Reason, Expected Impact, Supporting Evidence, Future Review).
4. The exact edit needed on the handbook cover page and version table to set status = Ratified.
Present everything for human approval. Change no scientific direction; only record decisions the human confirms.
```

**Google Antigravity Prompt:** *None — this step is planning/decision only; Antigravity does not implement.*

**GitHub Expectations:** No repo yet. The ratification content is committed in STEP-002 on branch `main` with message `docs: ratify master operating system and record DEC0001`.

**Kaggle Expectations:** None.

**Documentation Updates:** Handbook cover page + version table; prepare `DEC0001.md`.

**Verification Checklist:**
- ✓ Human has explicitly approved the stack, license, and repo name.
- ✓ Each of DEF-001…DEF-004 has a recorded stance (deferred-with-criteria or decided).
- ✓ `DEC0001.md` content is complete per Template 3.
- ✓ Handbook status text updated to *Ratified* with a new version-table row.
- ✓ No new architecture, workflow, or registry was invented.

**Common Mistakes:** Deciding a deferral (e.g. backbone or dataset) prematurely without evidence; editing the handbook's architecture instead of only its status; skipping the Decision Log record.

**Recovery Procedure:** If a decision was recorded incorrectly, do **not** delete the `DEC` entry (IDs are immutable, [A.1](MASTER_RESEARCH_OPERATING_SYSTEM.md#a1-canonical-identifier-scheme)); add a new `DEC` superseding it and set the old one's status to `Superseded`. Never modify the handbook's architecture to fit a decision — escalate to the human.

**Definition of Done:** Handbook ratified; DEF stances recorded; `DEC0001.md` drafted; universal [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) items that apply pre-repo are satisfied (the rest complete in STEP-002).

**Next Step:** STEP-002 — Initialize the repository skeleton.

---

## STEP-002 — Initialize the Repository Skeleton & Folder READMEs  **[C][A]**

**Title:** Create the canonical 20-folder tree with a compliant README in every folder.

**Objective:** Create the exact top-level directory tree from [§2.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#22-top-level-directory-tree), give every folder a `README.md` conforming to the [README policy (A.4)](MASTER_RESEARCH_OPERATING_SYSTEM.md#a4-canonical-readme-policy), and make the first commit on `main`.

**Why this step exists:** [§2.1](MASTER_RESEARCH_OPERATING_SYSTEM.md#21-design-goals) requires that every artifact type has exactly one home *before* artifacts are produced. Literature registration (STEP-011) writes to `02_Literature/metadata/` — that path must exist first.

**Handbook References:** [§2.2 Directory Tree](MASTER_RESEARCH_OPERATING_SYSTEM.md#22-top-level-directory-tree); [§2.3 Folder Contracts](MASTER_RESEARCH_OPERATING_SYSTEM.md#23-folder-contracts); [§2.4 Hygiene Rules](MASTER_RESEARCH_OPERATING_SYSTEM.md#24-repository-hygiene-rules); [A.2 Naming](MASTER_RESEARCH_OPERATING_SYSTEM.md#a2-canonical-file-naming-rules); [A.4 README Policy](MASTER_RESEARCH_OPERATING_SYSTEM.md#a4-canonical-readme-policy); [§10 Phase 1](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-1--repository-initialization).

**Prerequisites:** STEP-001 complete (ratified). A GitHub account and empty remote repository named per STEP-001.

**Estimated Difficulty:** Easy.
**Estimated Time:** 2–3 hours.
**Parallelizable:** No — this is the root every other step builds on.

**Inputs:** Handbook §2.2–§2.3 (folder list + contracts); STEP-001 repo name.

**Expected Outputs:** The full folder tree with numeric prefixes `01_…20_` plus `environment/`, each containing a `README.md` (Purpose · Contents · Workflow · Owner · Related folders · Expected outputs) and a `.gitkeep` where otherwise empty.

**Repository Changes:**
- *New folders:* all 20 numbered folders + `environment/` and their documented subfolders (e.g. `02_Literature/{papers,summaries,metadata,indexes,research_gap,claims,search_history,trends,drafts}`, `03_Datasets/{raw,processed,splits,metadata,reports,licenses}`, etc. as listed in [§2.3](MASTER_RESEARCH_OPERATING_SYSTEM.md#23-folder-contracts)).
- *New files:* one `README.md` per folder; `.gitkeep` in empty leaf folders.
- *Registries:* none yet (STEP-006).

**Cursor Prompt:**
```
You are the repository architect. Do NOT write application code.
Using MASTER_RESEARCH_OPERATING_SYSTEM.md §2.2 and §2.3 ONLY:
1. Produce the exact folder tree to create, including the documented subfolders named in each folder contract (§2.3) and the environment/ folder.
2. For EACH folder, draft a README.md that follows the README policy (A.4): Purpose, Contents, Workflow, Owner, Related folders, Expected outputs — copying the folder's Purpose/Writes/Reads/Allowed/Forbidden from §2.3. Keep it factual; link back to the governing handbook section instead of duplicating it (16_Documentation forbids duplicating the handbook).
3. Produce a precise creation checklist (paths + files) for Antigravity to execute.
Do not invent folders not present in §2.2/§2.3. Flag any name that would violate §2.4 hygiene rules.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Follow the Cursor-approved plan exactly.
Objective: create the repository skeleton for the AI Digital Forensics project.
Requirements:
- Create every folder and subfolder listed in the approved plan (numeric-prefixed 01_..20_, plus environment/).
- Write each folder's README.md with the exact approved content.
- Add a .gitkeep to any otherwise-empty leaf folder so Git tracks it.
Constraints:
- Create NO files other than READMEs and .gitkeep. No code, no registries, no datasets.
- Filenames/paths must match the plan character-for-character (A.2 naming).
- Do not create any forbidden-name folder (misc/temp/tmp/new/old/backup/copy/Untitled/test123) (§2.4).
Definition of Done: tree matches §2.2/§2.3; every folder has a policy-compliant README; nothing extra exists.
```

**GitHub Expectations:** Branch `main`. Commit `chore: initialize canonical repository skeleton and folder READMEs`. Push to the remote created in STEP-001. Include the STEP-001 handbook ratification edit + `DEC0001.md` in the first commit(s) so the ratified handbook and skeleton land together.

**Kaggle Expectations:** None.

**Documentation Updates:** Every folder `README.md`; the root README is completed in STEP-003.

**Verification Checklist:**
- ✓ Folder tree exactly matches [§2.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#22-top-level-directory-tree) (20 numbered + `environment/`).
- ✓ Documented subfolders from [§2.3](MASTER_RESEARCH_OPERATING_SYSTEM.md#23-folder-contracts) exist.
- ✓ Every folder has a `README.md` with all six [A.4](MASTER_RESEARCH_OPERATING_SYSTEM.md#a4-canonical-readme-policy) fields.
- ✓ No forbidden names ([§2.4](MASTER_RESEARCH_OPERATING_SYSTEM.md#24-repository-hygiene-rules)).
- ✓ Naming is lowercase `snake_case` except acknowledged constants ([A.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#a2-canonical-file-naming-rules)).
- ✓ Committed and pushed to `main`.

**Common Mistakes:** Renaming folders (dropping numeric prefixes); creating extra "helper" folders; empty folders lost by Git (missing `.gitkeep`); README that duplicates the handbook instead of linking.

**Recovery Procedure:** If a folder is misnamed, rename to the exact §2.2 name (do not leave the old one). If Antigravity created extra files, delete them (they violate §2.4). Never delete a numbered folder from §2.2 even if currently unused — it has a reserved contract.

**Definition of Done:** Skeleton matches the handbook; all READMEs compliant; pushed to `main`; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-003 — Root governance & ignore-policy files.

---

## STEP-003 — Root Governance & Ignore-Policy Files  **[C][A]**

**Title:** Author the root README, LICENSE, CONTRIBUTING, CHANGELOG, CODEOWNERS, `.gitignore`, `.gitattributes`.

**Objective:** Populate the repository's root governance files and enforce the [ignore policy (A.7)](MASTER_RESEARCH_OPERATING_SYSTEM.md#a7-canonical-ignore-policy) and [storage tiers (A.6)](MASTER_RESEARCH_OPERATING_SYSTEM.md#a6-canonical-storage--synchronization-policy) so secrets, caches, datasets, and large binaries can never be committed.

**Why this step exists:** [§10 Phase 5](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-5--github-repository-policy) requires `README/LICENSE/CONTRIBUTING/CHANGELOG/CODEOWNERS`; [A.7](MASTER_RESEARCH_OPERATING_SYSTEM.md#a7-canonical-ignore-policy) requires a canonical `.gitignore`/`.gitattributes` from the first day so no forbidden artifact is ever tracked.

**Handbook References:** [§10 Phase 5](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-5--github-repository-policy); [A.6 Storage Tiers](MASTER_RESEARCH_OPERATING_SYSTEM.md#a6-canonical-storage--synchronization-policy); [A.7 Ignore Policy](MASTER_RESEARCH_OPERATING_SYSTEM.md#a7-canonical-ignore-policy); [Template 1 — README](MASTER_RESEARCH_OPERATING_SYSTEM.md#14-template-library); [§1.4 Stack](MASTER_RESEARCH_OPERATING_SYSTEM.md#14-fixed-technology-stack).

**Prerequisites:** STEP-002 (skeleton exists); STEP-001 (license chosen).

**Estimated Difficulty:** Easy.
**Estimated Time:** 2–3 hours.
**Parallelizable:** Partially — README prose can be drafted while ignore rules are finalized, but all land in one commit.

**Inputs:** Chosen license (STEP-001); [§2.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#22-top-level-directory-tree) tree for the README folder guide; [A.7](MASTER_RESEARCH_OPERATING_SYSTEM.md#a7-canonical-ignore-policy) ignore list.

**Expected Outputs:** `README.md`, `LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md`, `CODEOWNERS`, `.gitignore`, `.gitattributes` at the repository root.

**Repository Changes:**
- *New files (root):* the seven governance files above.
- *Modified:* none (root README replaces the placeholder if any).
- *Documentation:* root README is the entry point (Template 1 fields).

**Cursor Prompt:**
```
You are the repository governance architect. Do NOT write application code.
Using the handbook ONLY (Template 1, §10 Phase 5, A.6, A.7, §1.4):
1. Draft README.md (Template 1 fields: Purpose, project description, repository structure map from §2.2, installation, quick start, folder guide, workflow Cursor→Antigravity→GitHub→Kaggle, dependencies, license, citation placeholder, contact). Link to the handbook; do not duplicate it.
2. Draft CONTRIBUTING.md encoding the workflow + commit policy (§10 Phase 2–3), branch strategy (Phase 4), and the human-in-the-loop rule (§1.9).
3. Draft CHANGELOG.md (Keep a Changelog style) seeded with the initialization entries.
4. Draft CODEOWNERS mapping folders to the human owner.
5. Produce the exact .gitignore per A.7 (Python, Node, FastAI/training outputs, notebook checkpoints, caches, OS files, secrets, media, raw/processed data) and .gitattributes (Git LFS declarations for explicitly tracked exports only + normalized line endings).
6. State the LICENSE text choice from STEP-001.
Output ready-to-save file contents. Flag anything that would let a data-tier/secret file be committed (A.6).
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Save the Cursor-approved files verbatim at the repository root:
README.md, LICENSE, CONTRIBUTING.md, CHANGELOG.md, CODEOWNERS, .gitignore, .gitattributes.
Constraints:
- Content must match the approved drafts exactly.
- .gitignore MUST block: secrets/.env, virtualenvs, __pycache__, caches, notebook outputs, node_modules, media uploads, raw/processed datasets, *.pth/*.pkl (except LFS-tracked exports), per A.7.
- Do not commit any secret or dataset. Do not add extra files.
Definition of Done: all 7 files present at root with approved content; a test file matching an ignore rule is confirmed ignored (git check-ignore).
```

**GitHub Expectations:** Branch `main`. Commit `chore: add root governance files and canonical ignore policy`. Verify `git check-ignore` blocks a sample `.env`, `*.pth`, and `03_Datasets/raw/x.jpg`.

**Kaggle Expectations:** None.

**Documentation Updates:** Root README; CHANGELOG initialization entry.

**Verification Checklist:**
- ✓ All seven root files present with handbook-compliant content.
- ✓ `.gitignore` blocks every category in [A.7](MASTER_RESEARCH_OPERATING_SYSTEM.md#a7-canonical-ignore-policy) (verified with `git check-ignore`).
- ✓ `.gitattributes` declares LFS only for explicitly tracked exports ([§10 Phase 11](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-11--git-lfs-strategy)).
- ✓ README structure map matches [§2.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#22-top-level-directory-tree).
- ✓ LICENSE matches STEP-001 decision; CODEOWNERS names the human.
- ✓ Committed + pushed.

**Common Mistakes:** Committing a real `.env`; forgetting to ignore `models/`/`*.pth`; README that copies handbook content; LFS-tracking raw datasets (forbidden — those go to Kaggle Datasets).

**Recovery Procedure:** If a forbidden file was already committed, remove it from history immediately (it is a secret/large-binary leak) and rotate any exposed secret; then fix `.gitignore`. Ask Antigravity to re-run `git check-ignore` proofs. Do not weaken A.7 to make a file fit — reclassify it to the correct storage tier ([A.6](MASTER_RESEARCH_OPERATING_SYSTEM.md#a6-canonical-storage--synchronization-policy)).

**Definition of Done:** Governance + ignore policy enforced and pushed; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-004 — Configure the GitHub workflow (branches, protection, PR/issue templates).

---

## STEP-004 — Configure the GitHub Workflow  **[C][H]**

**Title:** Branch model, protection rules, PR/issue templates, milestones, and release policy.

**Objective:** Establish the branch strategy ([§10 Phase 4](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-4--branch-strategy)), protect `main`/`develop`, and add PR/issue templates and milestones so every later change flows through a reviewed, conventional process.

**Why this step exists:** [§10 Phases 1–5, 12, 14](MASTER_RESEARCH_OPERATING_SYSTEM.md#10-github--kaggle--antigravity-workflow) define how work is integrated, reviewed, and released; the [commit policy (Phase 3)](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-3--commit-policy) and [issue categories (Phase 14)](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-14--issue-management) must exist before real work begins.

**Handbook References:** [§10 Phase 3 Commit Policy](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-3--commit-policy); [Phase 4 Branch Strategy](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-4--branch-strategy); [Phase 5 Repo Policy](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-5--github-repository-policy); [Phase 12 Releases](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-12--release-workflow); [Phase 14 Issues](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-14--issue-management).

**Prerequisites:** STEP-003 (governance files exist).

**Estimated Difficulty:** Easy.
**Estimated Time:** 1–2 hours.
**Parallelizable:** No (repo-wide settings).

**Inputs:** [§10 Phase 4](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-4--branch-strategy) branch list; [Phase 14](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-14--issue-management) issue categories.

**Expected Outputs:** `develop` branch created from `main`; branch-protection on `main` and `develop`; `.github/` with PR template and issue templates (Bug/Dataset/Experiment/Writing/Documentation/Architecture/Deployment/Evaluation/Research/Enhancement); milestones for `v0.1/v0.5/v1.0/v1.1/v2.0`.

**Repository Changes:**
- *New folder:* `.github/` (ISSUE_TEMPLATE/, PULL_REQUEST_TEMPLATE.md).
- *New branch:* `develop`.
- *Settings:* branch protection (human-configured in GitHub UI).

**Cursor Prompt:**
```
You are the GitHub workflow architect. Do NOT write application code.
Using §10 Phases 3,4,5,12,14 ONLY:
1. Draft the PR template (summary, linked issue, checklist that references the relevant Quality Gate/Checklist, DoD A.5 confirmation, platform note "implemented by Antigravity / reviewed in Cursor").
2. Draft one issue template per §10 Phase 14 category (Bug, Dataset, Experiment, Writing, Documentation, Architecture, Deployment, Evaluation, Research, Enhancement) with priority/status/milestone fields.
3. Specify the branch model (main, develop, feature/*, experiment/*, hotfix/*, release/*, writing/*, research/*) and the exact branch-protection settings the human must click in the GitHub UI (require PR review into develop; develop→main only at releases; delete merged branches).
4. List the milestones to create (v0.1 prototype, v0.5 internal eval, v1.0 thesis, v1.1 journal, v2.0 multimodal).
Output the files and a step-by-step human UI checklist (A.8 protocol) for protection settings.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY.
- Create the .github/ directory with the approved PULL_REQUEST_TEMPLATE.md and one issue template per approved category.
- Create the develop branch from main and push it.
Constraints: content matches approved drafts; make no repository-settings changes (those are human UI actions); add no code.
Definition of Done: .github templates present; develop branch exists on the remote.
```

**GitHub Expectations:** Branch `main` for `.github/` files (`chore: add PR/issue templates and branch model`), then create/push `develop`. **[H]** Human sets branch protection + creates milestones in the GitHub UI (cannot be scripted here) per the Cursor checklist.

**Kaggle Expectations:** None.

**Documentation Updates:** CONTRIBUTING.md cross-links the templates; CHANGELOG entry.

**Verification Checklist:**
- ✓ `develop` exists; `main` and `develop` are protected (review required).
- ✓ PR template references the DoD and relevant Quality Gate.
- ✓ All 10 issue categories have templates.
- ✓ Milestones `v0.1…v2.0` created.
- ✓ Merged-branch cleanup policy documented in CONTRIBUTING.

**Common Mistakes:** Committing directly to `main` later; skipping protection so unreviewed code lands; issue categories that don't match Phase 14.

**Recovery Procedure:** If direct commits to `main` occur later, enable protection retroactively and route future work through `develop`. Never force-push to `main`/`develop` ([§10.3](MASTER_RESEARCH_OPERATING_SYSTEM.md#103-infrastructure-rules-binding)).

**Definition of Done:** Workflow, protection, templates, and milestones in place; pushed; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-005 — Install the Template Library.

---

## STEP-005 — Install the Template Library  **[C][A]**

**Title:** Populate `18_Templates/` with all 30 canonical templates.

**Objective:** Create every template from [§14.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates) so no later document ever starts from a blank page and every instance is uniform.

**Why this step exists:** [§14](MASTER_RESEARCH_OPERATING_SYSTEM.md#14-template-library) mandates that every recurring document is produced from a template; many later steps (summaries, decisions, experiments, cards, reports) depend on these existing.

**Handbook References:** [§14.1 Template Contract](MASTER_RESEARCH_OPERATING_SYSTEM.md#141-template-contract); [§14.2 The Templates (1–30)](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); [A.11 Registry Format](MASTER_RESEARCH_OPERATING_SYSTEM.md#a11-canonical-registry-format); [A.2 Naming](MASTER_RESEARCH_OPERATING_SYSTEM.md#a2-canonical-file-naming-rules).

**Prerequisites:** STEP-002 (`18_Templates/` exists).

**Estimated Difficulty:** Medium.
**Estimated Time:** 4–6 hours (or two sessions).
**Parallelizable:** Yes — templates are independent; can be split across two sessions, but all belong to one folder and one commit series.

**Inputs:** [§14.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates) template specifications; each template's linked source section.

**Expected Outputs:** 30 template files in `18_Templates/` named per [A.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#a2-canonical-file-naming-rules) (e.g. `paper_summary.md`, `decision.md`, `config.yaml`, `model_card.md`, `dataset_card.md`, `case_report.md`, `figure_spec.md`, `table_spec.md`, `api_spec.md`, `module_spec.md`, `agent.md`, `prompt.md`, `registry.md`, …).

**Repository Changes:**
- *New files:* 30 template files in `18_Templates/`.
- *Modified:* `18_Templates/README.md` gains an index table (template → purpose → owner → target folder).

**Cursor Prompt:**
```
You are the Research Process Architect. Do NOT write application code.
Using §14.2 (Templates 1–30) and their linked sections ONLY, draft ALL 30 templates as ready-to-save files in 18_Templates/, each with:
- A header block per §14.1 (Template Name, Purpose, When Used, Owner, Inputs, Outputs, Required Sections, Optional Sections, Validation Rules, Naming Convention, Folder Location, Definition of Done, Common Mistakes, Related Templates).
- The body fields exactly as enumerated in the handbook for that template (e.g. Template 7 experiment_readme fields; Template 8 config.yaml sections from Phase M4; Template 22 model_card fields; Template 24 case_report fields).
- Registry-producing templates must follow A.11 (ID primary key + Owner, Version, Status, Created, Updated columns).
Also draft an index table for 18_Templates/README.md mapping each template to its target instance folder.
Do NOT invent new templates or fields. Use A.2 filenames.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Save the 30 Cursor-approved templates verbatim into 18_Templates/ using the approved filenames, and update 18_Templates/README.md with the approved index table.
Constraints: these are blank templates (no filled-in instances — §2.3 forbids instances here). Exact filenames per A.2. Add nothing extra.
Definition of Done: 30 templates present with correct names and fields; README index complete.
```

**GitHub Expectations:** Branch `feature/template-library` → PR into `develop`. Commit `docs: add canonical template library (Templates 1-30)`.

**Kaggle Expectations:** None.

**Documentation Updates:** `18_Templates/README.md` index; CHANGELOG.

**Verification Checklist:**
- ✓ Exactly 30 templates present, matching [§14.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates) names/purposes.
- ✓ Each has the [§14.1](MASTER_RESEARCH_OPERATING_SYSTEM.md#141-template-contract) header block.
- ✓ Registry templates follow [A.11](MASTER_RESEARCH_OPERATING_SYSTEM.md#a11-canonical-registry-format).
- ✓ Field lists match the handbook (config.yaml sections, model_card, case_report, etc.).
- ✓ No filled-in instances in `18_Templates/`.
- ✓ Filenames are `snake_case` per [A.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#a2-canonical-file-naming-rules).

**Common Mistakes:** Missing templates; adding fields not in the handbook; placing a filled example in the templates folder; inconsistent filenames.

**Recovery Procedure:** Diff the 30 delivered templates against [§14.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); add any missing template; strip any extra fields. If an instance leaked into `18_Templates/`, move it to its domain folder.

**Definition of Done:** All 30 templates installed, indexed, PR-merged to `develop`; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-006 — Initialize registries & the Project Management system.

---

## STEP-006 — Initialize Canonical Registries & Project Management System  **[C][A]**

**Title:** Create every registry (headers only) and the `01_Project_Management/` operating files.

**Objective:** Create all canonical registries from [Appendix B](MASTER_RESEARCH_OPERATING_SYSTEM.md#appendix-b--registry-index) as empty CSVs with correct headers and owning path, and stand up the project-management operating files (decision log, risk register, dashboard, review templates, timeline).

**Why this step exists:** [A.11](MASTER_RESEARCH_OPERATING_SYSTEM.md#a11-canonical-registry-format) requires each registry to exist as a single CSV with a stable header and one owner before any entity is registered. [§12](MASTER_RESEARCH_OPERATING_SYSTEM.md#12-daily-research-operating-workflow) requires the daily operating files.

**Handbook References:** [Appendix B — Registry Index](MASTER_RESEARCH_OPERATING_SYSTEM.md#appendix-b--registry-index); [A.11 Registry Format](MASTER_RESEARCH_OPERATING_SYSTEM.md#a11-canonical-registry-format); registry column definitions in [§3](MASTER_RESEARCH_OPERATING_SYSTEM.md#papers-registry), [§4](MASTER_RESEARCH_OPERATING_SYSTEM.md#dataset-registry), [§5](MASTER_RESEARCH_OPERATING_SYSTEM.md#experiment-registry), [§6](MASTER_RESEARCH_OPERATING_SYSTEM.md#evidence-registry), [§7](MASTER_RESEARCH_OPERATING_SYSTEM.md#evaluation-registry), [§9](MASTER_RESEARCH_OPERATING_SYSTEM.md#writing-database); [§12](MASTER_RESEARCH_OPERATING_SYSTEM.md#12-daily-research-operating-workflow); [§13.4 Risk Register](MASTER_RESEARCH_OPERATING_SYSTEM.md#134-risk-register).

**Prerequisites:** STEP-002 (folders), STEP-005 (registry/PM templates available).

**Estimated Difficulty:** Medium.
**Estimated Time:** 3–4 hours.
**Parallelizable:** Yes — registry files are independent; can be split with STEP-007.

**Inputs:** [Appendix B](MASTER_RESEARCH_OPERATING_SYSTEM.md#appendix-b--registry-index) (file paths + primary keys); each registry's canonical column list from its section.

**Expected Outputs:** Empty header-only CSVs at exactly the [Appendix B](MASTER_RESEARCH_OPERATING_SYSTEM.md#appendix-b--registry-index) paths; PM files: `decision_log/` (with `DEC0001.md` from STEP-001), `risk_register.csv`, `dashboard_status.md`, `timeline.md`, `milestones/`, `reviews/`, `research_diary/`, `meetings/`.

**Repository Changes:**
- *New files (registries, header-only):* `02_Literature/metadata/papers.csv`, `02_Literature/research_gap/research_gap.csv`, `02_Literature/claims/claim_database.csv`, `03_Datasets/metadata/{dataset_candidates,datasets,dataset_registry}.csv`, `04_Preprocessing/preprocessing_registry.csv`, `05_Models/{candidate_models,model_registry}.csv`, `06_Experiments/experiment_registry.csv`, `11_AI_Forensic_System/{evidence_registry,case_registry,module_registry}.csv`, `08_Evaluation/evaluation_registry.csv`, `15_Writing/shared/{writing_database,knowledge_index}.csv`, `01_Project_Management/risk_register.csv`.
- *New files (PM):* `dashboard_status.md`, `timeline.md`, `decision_log/DEC0001.md`, review/diary/meeting scaffolds.

**Cursor Prompt:**
```
You are the registry & operations architect. Do NOT write code.
Using Appendix B + A.11 + the per-section column definitions ONLY:
1. For EVERY registry in Appendix B, output the exact CSV header line, using the canonical columns from that registry's section, and appended (if not already present) the A.11 governance columns Owner, Version, Status, Created, Updated. State the exact file path from Appendix B.
2. Draft 01_Project_Management operating files: dashboard_status.md (Phase O16 fields), timeline.md, risk_register.csv header (§13.4 columns), and empty scaffolds for reviews/ (daily/weekly/monthly), research_diary/, meetings/, milestones/.
3. Produce DEC0001.md content from STEP-001 for decision_log/.
Do not invent columns. Preserve the fixed registry names (e.g. "Experiment Registry", never "experiment tracker").
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Create each registry CSV at its exact Appendix B path with ONLY the approved header row (no data rows). Create the approved 01_Project_Management files including decision_log/DEC0001.md.
Constraints: header text must match exactly; one registry per canonical path; no duplicate/renamed registries; CSV files are UTF-8, comma-separated. Add nothing extra.
Definition of Done: every Appendix B registry exists (header-only) at its canonical path; PM operating files present; DEC0001 saved.
```

**GitHub Expectations:** Branch `feature/registries-and-pm` → PR into `develop`. Commit `chore: initialize canonical registries and project management system`.

**Kaggle Expectations:** None.

**Documentation Updates:** `01_Project_Management/README.md`; `dashboard_status.md` first snapshot; CHANGELOG.

**Verification Checklist:**
- ✓ Every registry in [Appendix B](MASTER_RESEARCH_OPERATING_SYSTEM.md#appendix-b--registry-index) exists at its exact path, header-only.
- ✓ Headers match the canonical columns + [A.11](MASTER_RESEARCH_OPERATING_SYSTEM.md#a11-canonical-registry-format) governance columns.
- ✓ Registry names are the fixed canonical names (no aliases).
- ✓ `DEC0001.md` present; risk register + dashboard present.
- ✓ No registry has stray data rows.
- ✓ PR merged into `develop`.

**Common Mistakes:** Wrong path (e.g. putting `experiment_registry.csv` outside `06_Experiments/`); renaming a registry; missing governance columns; adding placeholder data rows.

**Recovery Procedure:** Compare created files against [Appendix B](MASTER_RESEARCH_OPERATING_SYSTEM.md#appendix-b--registry-index) row-by-row; move/rename any misplaced registry; never create a second copy of a registry (one canonical path only). If a header is wrong, correct it now while registries are empty (schema changes later are MAJOR versions per [A.3](MASTER_RESEARCH_OPERATING_SYSTEM.md#a3-canonical-versioning-policy)).

**Definition of Done:** All registries + PM system initialized and merged; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-007 — Prompt Library & Agent Specifications.

---

## STEP-007 — Prompt Library & Agent Specifications  **[C][A]**  **GATE (Checklist 1)**

**Title:** Populate `19_Prompts/` and author the agent specifications; pass Repository Readiness.

**Objective:** Create the versioned prompt library structure and author the single-responsibility agent specifications from [§11](MASTER_RESEARCH_OPERATING_SYSTEM.md#11-agent-framework), then run [Checklist 1 — Repository Readiness](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-1--repository-readiness) as the gate that closes the Foundation phase.

**Why this step exists:** [§11](MASTER_RESEARCH_OPERATING_SYSTEM.md#11-agent-framework) requires each agent to be specified with the [Agent template](MASTER_RESEARCH_OPERATING_SYSTEM.md#template-27--agent-specification-agentmd); [§19_Prompts](MASTER_RESEARCH_OPERATING_SYSTEM.md#19_prompts) requires every prompt versioned. Foundation cannot be declared complete until [Checklist 1](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-1--repository-readiness) passes.

**Handbook References:** [§11.1 Agent Contract](MASTER_RESEARCH_OPERATING_SYSTEM.md#111-canonical-agent-contract); [§11.2 Agent Registry](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain); [§19_Prompts contract](MASTER_RESEARCH_OPERATING_SYSTEM.md#19_prompts); [Template 26 Prompt](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); [Template 27 Agent](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); [Checklist 1](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-1--repository-readiness).

**Prerequisites:** STEP-005 (Templates 26 & 27), STEP-006 (registries).

**Estimated Difficulty:** Medium.
**Estimated Time:** 4–6 hours (agents can be authored in domain batches over two sessions).
**Parallelizable:** Yes — agent specs are independent per domain.

**Inputs:** [§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain) agent lists; [Template 27](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates).

**Expected Outputs:** `19_Prompts/` subfolders (`planning/, implementation/, literature/, writing/, evaluation/, review/`) + `prompt_changelog.md`; agent specification files (one per agent in [§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)) stored per the handbook (agent specs live with `19_Prompts`/agents area per project convention, cross-linked from the relevant domain README).

**Repository Changes:**
- *New folders/files:* `19_Prompts/*` subfolders + `prompt_changelog.md`; agent spec files (`agent.md` instances) for Literature, Dataset, Model, Forensic, Evaluation, Web, Writing, Operations, QA agents.
- *Modified:* domain READMEs cross-link their agents.

**Cursor Prompt:**
```
You are the Agent Framework architect. Do NOT write code.
Using §11 + Template 27 + Template 26 ONLY:
1. Draft the 19_Prompts/ structure (planning/implementation/literature/writing/evaluation/review) and prompt_changelog.md, plus a prompt.md usage note (Template 26 fields).
2. For each agent listed in §11.2 (Literature 10, Dataset 10, Model 9, Forensic 9, Evaluation 10, Web 9, Writing 11, Operations 10, QA 10), draft an agent specification using the full §11.1 contract (Name, Mission, Purpose, Primary/Allowed/Forbidden Responsibilities, Inputs, Outputs, Folder Access, Files Generated/Consumed, Dependencies, Workflow Position, Decision Authority, Escalation Rules, Failure Handling, Quality Checklist, DoD, Example Task, Example Output, Prompt Template). Enforce "one agent, one responsibility" and "communicate only through repository files".
3. Produce a filled Checklist 1 (Repository Readiness) PASS/FAIL audit of the repo so far (structure, READMEs, license, .gitignore, versioning, naming, docs, branch structure, no forbidden names).
Batch the agent specs by domain for review. Do not invent agents beyond §11.2.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Create the approved 19_Prompts/ structure and save each approved agent specification file at its agreed path. Update domain READMEs with the approved agent cross-links and save the Checklist-1 audit report to 01_Project_Management/reviews/ (or 16_Documentation as agreed).
Constraints: content matches approved drafts; one file per agent; no code; A.2 naming.
Definition of Done: prompt library structure present; every §11.2 agent has a spec; Checklist-1 audit saved.
```

**GitHub Expectations:** Branch `feature/agents-and-prompts` → PR into `develop`, then **[H]** merge `develop → main` and tag `v0.1` (research prototype scaffold) per [§10 Phase 12](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-12--release-workflow). Commit `docs: add agent specifications and prompt library; pass repository readiness gate`.

**Kaggle Expectations:** None.

**Documentation Updates:** Domain READMEs; `prompt_changelog.md`; `repository_audit.md` ([A.10 structure](MASTER_RESEARCH_OPERATING_SYSTEM.md#a10-canonical-audit-report-structure)).

**Verification Checklist (GATE — [Checklist 1](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-1--repository-readiness)):**
- ✓ Structure matches [§2.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#22-top-level-directory-tree); every folder has a compliant README.
- ✓ LICENSE, `.gitignore`, `.gitattributes` present and correct.
- ✓ All 30 templates present; all [Appendix B](MASTER_RESEARCH_OPERATING_SYSTEM.md#appendix-b--registry-index) registries present (header-only).
- ✓ Every agent in [§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain) has a spec with all [§11.1](MASTER_RESEARCH_OPERATING_SYSTEM.md#111-canonical-agent-contract) fields.
- ✓ Prompt library structure + changelog present.
- ✓ No [forbidden names](MASTER_RESEARCH_OPERATING_SYSTEM.md#24-repository-hygiene-rules); naming consistent ([A.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#a2-canonical-file-naming-rules)).
- ✓ Branch structure + protection active; `repository_audit.md` = PASS.
- ✓ `v0.1` tag created.

**Common Mistakes:** Merging agent responsibilities; agents that "remember" context instead of reading files; skipping the Checklist-1 audit; tagging `v0.1` before the gate passes.

**Recovery Procedure:** If Checklist 1 FAILS, do not proceed to Literature. Record failures in `repository_audit.md`, fix each (missing README, wrong name, missing registry), re-run the checklist. If an agent overlaps another's responsibility, split or narrow it per [§11.3](MASTER_RESEARCH_OPERATING_SYSTEM.md#113-agent-rules-binding).

**Definition of Done:** Prompt library + all agent specs exist; **[Checklist 1](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-1--repository-readiness) = PASS**; `v0.1` tagged; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied. Foundation phase complete.

**Next Step:** STEP-008 — Define the research question (begins Literature Review).

---
# PART 2 — LITERATURE REVIEW

> Implements [§3 Research & Literature Workflow](MASTER_RESEARCH_OPERATING_SYSTEM.md#3-research--literature-workflow), Phases L1–L7. Literature drives implementation — never the reverse ([§3 intro](MASTER_RESEARCH_OPERATING_SYSTEM.md#3-research--literature-workflow)). All files live in [02_Literature](MASTER_RESEARCH_OPERATING_SYSTEM.md#02_literature); IDs follow [A.1](MASTER_RESEARCH_OPERATING_SYSTEM.md#a1-canonical-identifier-scheme).

---

## STEP-008 — Define the Research Question  **[C][H]**

**Title:** Convert the topic into an approved research question, keyword seeds, and exclusion list (Phase L1).

**Objective:** Produce an approved `research_question.md` (one primary question + ≤3 sub-questions), `keywords.csv` (≥20 seed keywords), and `exclusion_list.csv` (explicit out-of-scope).

**Why this step exists:** [Phase L1](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l1--research-question-definition) requires an official research question before any search; [§1.7 Research philosophy](MASTER_RESEARCH_OPERATING_SYSTEM.md#17-governing-philosophies) forbids work with no question attached.

**Handbook References:** [Phase L1](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l1--research-question-definition); [§1.7](MASTER_RESEARCH_OPERATING_SYSTEM.md#17-governing-philosophies); [§1.9 Human-in-the-loop](MASTER_RESEARCH_OPERATING_SYSTEM.md#19-human-in-the-loop-rule); [Template 3 Decision Log](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates).

**Prerequisites:** STEP-007 (Foundation gate PASS).

**Estimated Difficulty:** Easy.
**Estimated Time:** 2–3 hours.
**Parallelizable:** No — every later literature step depends on the approved question.

**Inputs:** Initial topic "image-based AI-generated face detection"; handbook §1.2 project identity.

**Expected Outputs:** `02_Literature/research_question.md`, `keywords.csv`, `exclusion_list.csv`; a `DEC` entry recording the human's approval of scope.

**Repository Changes:**
- *New files:* `02_Literature/research_question.md`, `02_Literature/keywords.csv`, `02_Literature/exclusion_list.csv`, `01_Project_Management/decision_log/DEC0002.md` (scope approval).

**Cursor Prompt:**
```
You are the Research Planning Agent. Do NOT write code and do NOT select the final question yourself.
Using §1.2 and Phase L1 ONLY:
1. Propose 3 candidate primary research questions for image-based AI-generated face detection, each with ≤3 sub-questions, plus advantages/risks and objective selection criteria.
2. Propose ≥20 seed keywords (as keywords.csv rows: keyword, source="seed", date) covering generators (GAN/diffusion/etc.), tasks (detection/forensics), and cross-cutting themes (generalization, calibration, explainability, robustness).
3. Propose an explicit out-of-scope exclusion_list.csv (e.g. video deepfakes, audio, text — deferred per §1.2 future modalities).
4. Draft DEC0002.md (Template 3) recording the human's chosen question.
Present for human approval. Acceptance: 1 primary + ≤3 sub-questions; ≥20 keywords; explicit exclusions.
```

**Google Antigravity Prompt:** *None — planning + human approval only. Antigravity may later save the approved files if the human prefers, but no code/implementation is involved.*

**GitHub Expectations:** Branch `research/research-question` → PR into `develop`. Commit `research: define approved research question and keyword seeds`.

**Kaggle Expectations:** None.

**Documentation Updates:** `research_question.md`; `DEC0002.md`; dashboard current-phase = Literature.

**Verification Checklist:**
- ✓ Exactly one primary question + ≤3 sub-questions, human-approved.
- ✓ `keywords.csv` has ≥20 rows, each with a source.
- ✓ `exclusion_list.csv` states out-of-scope modalities.
- ✓ `DEC0002.md` records the choice.
- ✓ Committed to `develop`.

**Common Mistakes:** Scope too broad (all deepfakes) or too narrow (one generator); AI choosing the question instead of the human; fewer than 20 keywords.

**Recovery Procedure:** If scope tension appears, record it in the [Decision Log](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates) and iterate on the question (Phase L1 failure handling). Do not begin searching against an unapproved question.

**Definition of Done:** Approved question + keywords + exclusions committed; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-009 — Literature search strategy.

---

## STEP-009 — Build the Literature Search Strategy  **[C]**

**Title:** Reproducible, evolving multi-source search strategy (Phase L2).

**Objective:** Produce `search_string_templates.md` and the `search_history/` logging convention so every search across Scholar, IEEE, ACM, Springer, ScienceDirect, CVF, OpenReview, and arXiv is reproducible.

**Why this step exists:** [Phase L2](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l2--literature-search-strategy) requires each search run to be repeatable from its logged string + filters, with keyword evolution harvested from collected papers.

**Handbook References:** [Phase L2](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l2--literature-search-strategy); [§3.3 Paper Quality Policy](MASTER_RESEARCH_OPERATING_SYSTEM.md#33-paper-quality-policy).

**Prerequisites:** STEP-008 (approved question + keywords).

**Estimated Difficulty:** Easy.
**Estimated Time:** 1–2 hours.
**Parallelizable:** No (defines the method used by STEP-010+).

**Inputs:** `research_question.md`, `keywords.csv`.

**Expected Outputs:** `02_Literature/search_history/search_string_templates.md`; a documented `search_history/` entry schema (source, search string, date, filters, result count, papers selected); filter + ranking policy.

**Repository Changes:**
- *New files:* `search_string_templates.md`; a `search_history/README.md` describing the log entry format.

**Cursor Prompt:**
```
You are the Literature Search Agent (search/filter/rank/collect only — never summarize or download).
Using Phase L2 + §3.3 ONLY:
1. Instantiate the canonical search string template for our question across GAN + diffusion + face + detection/forensics, producing ready-to-use strings per source (Scholar, IEEE Xplore, ACM DL, Springer, ScienceDirect, CVF, OpenReview, arXiv).
2. Define the search_history/ log entry format (source, search string, date, filters, result count, papers selected) so any run is reproducible.
3. Define filters (year, venue quality, citation threshold, DOI/title dedup) and a priority ranking rule based on §3.3 quality dimensions.
4. Define the keyword-evolution rule: new keywords harvested from collected papers are appended to keywords.csv with their source Paper ID.
Output ready-to-save files. Do not download or summarize papers.
```

**Google Antigravity Prompt:** *None — this is a planning artifact; the human executes searches manually in STEP-010.*

**GitHub Expectations:** Branch `research/search-strategy` → PR into `develop`. Commit `research: add reproducible literature search strategy`.

**Kaggle Expectations:** None.

**Documentation Updates:** `search_history/README.md`.

**Verification Checklist:**
- ✓ Search strings provided per source and tied to `keywords.csv`.
- ✓ Log entry format enables exact repetition.
- ✓ Filters + ranking defined; dedup rule stated.
- ✓ Keyword-evolution rule documented.

**Common Mistakes:** Non-reproducible ad-hoc searching; no dedup; ranking that isn't objective.

**Recovery Procedure:** If a past search can't be reproduced, re-run from the logged string; if the string wasn't logged, treat results as provisional and re-log. Never summarize in this step (that is L5).

**Definition of Done:** Search strategy documented + committed; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-010 — Execute searches and download papers.

---

## STEP-010 — Execute Searches & Download Papers  **[C][H]**

**Title:** Run the logged searches and acquire PDFs with canonical, title-free filenames (Phases L2–L3).

**Objective:** Execute the strategy, log each run in `search_history/`, and place downloaded PDFs as `P0001.pdf`, `P0002.pdf`, … in `02_Literature/papers/` (titles live only in metadata).

**Why this step exists:** [Phase L3](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l3--paper-download-workflow) mandates ID-named, title-free PDFs with license verification and DOI/title dedup before assigning a new `P` ID; downloading is a [human task](MASTER_RESEARCH_OPERATING_SYSTEM.md#a8-human-task-protocol) (respect access rights).

**Handbook References:** [Phase L2](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l2--literature-search-strategy); [Phase L3](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l3--paper-download-workflow); [A.8 Human Task Protocol](MASTER_RESEARCH_OPERATING_SYSTEM.md#a8-human-task-protocol); [A.2 naming](MASTER_RESEARCH_OPERATING_SYSTEM.md#a2-canonical-file-naming-rules).

**Prerequisites:** STEP-009 (strategy).

**Estimated Difficulty:** Medium.
**Estimated Time:** 1 day (recurring — repeated as the living review grows).
**Parallelizable:** Yes — searching different sources can be batched; but ID assignment must be serialized to avoid collisions.

**Inputs:** `search_string_templates.md`; access to the literature sources.

**Expected Outputs:** `search_history/` run logs; PDFs named `Pxxxx.pdf` in `02_Literature/papers/`; a temporary intake list mapping each `P` ID → DOI/title/license (feeds STEP-011).

**Repository Changes:**
- *New files:* `search_history/<date>_<source>.md` run logs. **PDFs themselves** are large binaries — keep only if within source-tier norms; per [A.6](MASTER_RESEARCH_OPERATING_SYSTEM.md#a6-canonical-storage--synchronization-policy) small PDFs may live in Git, but respect repo-size discipline ([§10 Phase 11](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-11--git-lfs-strategy)). Follow the handbook's `02_Literature/papers/` allowance.

**Cursor Prompt:**
```
You are the Literature Search Agent. Do NOT summarize or invent metadata.
Given the search strategy, produce:
1. The exact ordered search runs to perform per source, each with the string + filters to log in search_history/.
2. A dedup pre-check procedure (normalize title, compare DOI) the human runs BEFORE assigning a new P ID.
3. The next available P ID sequence and a Human Task block (A.8): why, exactly what to download, exactly where to place it (02_Literature/papers/P0001.pdf ...), expected output, how to confirm (file exists + intake row created).
Do not rename PDFs to titles. Titles go only into metadata (STEP-011).
```

**Google Antigravity Prompt:** *None — downloading is a human task (access rights). Antigravity does not fetch papers.*

**GitHub Expectations:** Branch `research/literature-intake` → PR into `develop`. Commit `research: log search runs and add papers Pxxxx-Pyyyy`. Keep commits small; do not push huge PDF batches at once.

**Kaggle Expectations:** None.

**Documentation Updates:** `search_history/` logs; intake list for STEP-011.

**Verification Checklist:**
- ✓ Every search run has a reproducible log (source, string, filters, counts, selected).
- ✓ Every PDF is `Pxxxx.pdf` — **no title-named files**.
- ✓ DOI/title dedup performed before each new `P` ID.
- ✓ Licenses noted at intake.
- ✓ P IDs are contiguous and never reused ([A.1](MASTER_RESEARCH_OPERATING_SYSTEM.md#a1-canonical-identifier-scheme)).

**Common Mistakes:** Title-named PDFs; duplicate papers under two IDs; skipping the search log; committing paywalled PDFs improperly.

**Recovery Procedure:** If a duplicate `P` ID was assigned, mark the later row `Status=Superseded` in `papers.csv` (STEP-011) — never reuse the ID. If a PDF was title-named, rename to its `Pxxxx.pdf` and record the title in metadata only.

**Definition of Done:** Searches logged; PDFs ID-named; intake list ready; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-011 — Register papers.

---

## STEP-011 — Register Papers  **[C][A]**

**Title:** Populate the Papers Registry — no paper exists without metadata (Phase L4).

**Objective:** For every `Pxxxx.pdf`, create a complete row in the [Papers Registry](MASTER_RESEARCH_OPERATING_SYSTEM.md#papers-registry) `papers.csv` and generate `papers.bib` entries.

**Why this step exists:** [Phase L4](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l4--paper-registration) requires every `P` ID to have all metadata columns populated or explicitly `unknown`; `papers.csv` is the canonical literature registry consumed by every later literature and writing step.

**Handbook References:** [Phase L4 + Papers Registry columns](MASTER_RESEARCH_OPERATING_SYSTEM.md#papers-registry); [A.11 Registry Format](MASTER_RESEARCH_OPERATING_SYSTEM.md#a11-canonical-registry-format); [§3.3 Quality Score](MASTER_RESEARCH_OPERATING_SYSTEM.md#33-paper-quality-policy); agents Paper Registration + Metadata Extraction ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)).

**Prerequisites:** STEP-010 (PDFs + intake list); STEP-006 (`papers.csv` header exists).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day per batch.
**Parallelizable:** Yes — metadata extraction per paper is independent.

**Inputs:** PDFs, intake list, `papers.csv` header.

**Expected Outputs:** Fully populated `papers.csv` rows (all canonical columns), `papers.bib` entries, updated indexes deferred to STEP-013.

**Repository Changes:**
- *Modified:* `02_Literature/metadata/papers.csv` (append rows), `02_Literature/metadata/papers.bib`.
- *Registry:* Papers Registry updated (owner: Paper Registration Agent).

**Cursor Prompt:**
```
You are planning/reviewing the Paper Registration + Metadata Extraction agents (register metadata only; never download; never summarize prose).
Using Phase L4 (Papers Registry canonical columns) + §3.3 + A.11 ONLY:
1. Produce the exact papers.csv row schema and, for each new P ID, a metadata extraction checklist (Title, Authors, Year, Venue, Publisher, DOI, Citation Count, Dataset, Architecture, Task, Modality, Explainability, Generalization, Limitations, Future Work, Code/Dataset Available, Keywords, Reading Status, Priority, Notes, Folder Location, BibTeX Available, PDF Available, Reviewed, Quality Score, Research Relevance) — marking unknown fields as "unknown".
2. Define the Quality Score computation from §3.3 (10 dimensions, 0–5) and the priority ranking.
3. Define the papers.bib entry format and citation-key convention.
Output a per-paper fill plan for Antigravity plus validation rules (unique P IDs, no empty required cells).
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. For each P ID in the intake list, append a fully-populated row to 02_Literature/metadata/papers.csv per the approved schema and add a matching entry to papers.bib.
Constraints:
- Populate every column or write "unknown"; never leave blank required cells.
- P IDs unique; Folder Location points to the PDF; append-or-update only (A.11) — never delete rows.
- Compute Quality Score by the approved formula. Do not invent metadata not present in the paper.
Definition of Done: every PDF has a complete papers.csv row and a papers.bib entry; validation rules pass.
```

**GitHub Expectations:** Branch `research/paper-registration` → PR into `develop`. Commit `research: register papers Pxxxx-Pyyyy in papers.csv and papers.bib`.

**Kaggle Expectations:** None.

**Documentation Updates:** `papers.csv`, `papers.bib`; `reading_progress.csv` seeded (Reading Status).

**Verification Checklist:**
- ✓ Every `Pxxxx.pdf` has exactly one `papers.csv` row.
- ✓ All canonical columns populated or `unknown`.
- ✓ `papers.bib` entry exists per paper; citation keys unique.
- ✓ Quality Score computed by [§3.3](MASTER_RESEARCH_OPERATING_SYSTEM.md#33-paper-quality-policy).
- ✓ No blank required cells; no duplicate/removed rows ([A.11](MASTER_RESEARCH_OPERATING_SYSTEM.md#a11-canonical-registry-format)).

**Common Mistakes:** Blank cells instead of `unknown`; fabricated citation counts/DOIs; a PDF with no registry row; duplicate rows.

**Recovery Procedure:** Cross-check `papers/` against `papers.csv` (every file ↔ row). For fabricated metadata, mark `Reviewed=no` and re-extract from the PDF; the Citation Verification Agent will re-check against the source. Never invent a DOI — use `unknown`.

**Definition of Done:** All papers registered with complete metadata + BibTeX; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-012 — Paper reading & structured summaries.

---

## STEP-012 — Read & Summarize Papers  **[C][A][H]**

**Title:** Structured, non-blind reading producing one summary per paper (Phase L5).

**Objective:** For each paper, produce `summaries/Pxxxx_summary.md` from [Template 2](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates), capturing problem, method, dataset, results, strengths, weaknesses, research gap, future work, and cross-links — every statement traceable to the paper.

**Why this step exists:** [Phase L5](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l5--paper-reading-workflow) feeds the Research Gap (L8) and Claim Database (L9); the Paper Summary Agent never invents content.

**Handbook References:** [Phase L5](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l5--paper-reading-workflow); [Template 2 Paper Summary](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); [§1.8 Ethics](MASTER_RESEARCH_OPERATING_SYSTEM.md#18-research-ethics-binding); Paper Summary Agent ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)).

**Prerequisites:** STEP-011 (registered papers).

**Estimated Difficulty:** Medium.
**Estimated Time:** ~1–2 hours per paper (recurring; batch by priority).
**Parallelizable:** Yes — summaries are per-paper independent.

**Inputs:** PDFs, `papers.csv`, Template 2.

**Expected Outputs:** `summaries/Pxxxx_summary.md` per paper; extracted limitations/future-work pushed to L8 inputs; `Reading Status` updated in `papers.csv`.

**Repository Changes:**
- *New files:* `02_Literature/summaries/Pxxxx_summary.md`.
- *Modified:* `papers.csv` (Reading Status, Reviewed), `reading_progress.csv`.

**Cursor Prompt:**
```
You are reviewing the Paper Summary Agent (structured notes only; never invent; every statement traces to the paper).
Using Phase L5 + Template 2 ONLY:
1. For the priority-ranked papers, produce a reading order (by Quality Score/priority from papers.csv).
2. Provide the exact summary skeleton (Problem, Motivation, Method, Architecture, Dataset, Training, Evaluation, Results, Strengths, Weaknesses, Research Gap, Future Work, Interesting Ideas, Possible Reuse, Questions, Connections) and require each Weakness/Gap/Future-Work item to be phrased so it can later feed research_gap.csv (STEP-014) with this Paper ID as support.
3. Define cross-linking rules (reference other P IDs) and the human-approval requirement for high-priority summaries.
Do not write the summaries' scientific content yourself if it would require fabricating claims; require grounding in the PDF.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. For each assigned paper, create summaries/Pxxxx_summary.md from Template 2, filling every section strictly from the paper's content. Cross-link related P IDs. Update Reading Status/Reviewed in papers.csv.
Constraints: never invent results or citations (§1.8); if a field is not in the paper, write "not reported". Extract explicit limitations/future-work verbatim-in-substance for the gap pipeline.
Definition of Done: every assigned paper has a complete, grounded summary; papers.csv reading status updated.
```
*(High-priority summaries require **[H]** human approval before they are treated as evidence.)*

**GitHub Expectations:** Branch `research/paper-summaries` → PR into `develop`. Commit `research: add structured summaries for Pxxxx-Pyyyy`.

**Kaggle Expectations:** None.

**Documentation Updates:** Summaries; `reading_progress.csv`; `papers.csv` status.

**Verification Checklist:**
- ✓ Every read paper has a Template-2 summary.
- ✓ Every summary statement is grounded in the paper (no invention).
- ✓ Limitations/future-work extracted for L8.
- ✓ Cross-links to other `P` IDs present where applicable.
- ✓ High-priority summaries human-approved.
- ✓ `papers.csv` reading status updated.

**Common Mistakes:** Copy-pasting paper wording ([§9.3](MASTER_RESEARCH_OPERATING_SYSTEM.md#93-scientific-writing-principles-binding) forbids it); inventing results; skipping the gap/future-work extraction.

**Recovery Procedure:** If a summary contains an ungrounded claim, flag `Reviewed=no`, return to the PDF, and correct. Never let an unverified summary feed the Claim Database.

**Definition of Done:** Priority papers summarized, grounded, cross-linked, approved; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-013 — Literature database, indexes, and relationship graph.

---

## STEP-013 — Build the Literature Database, Indexes & Relationship Graph  **[C][A]**

**Title:** Deterministic indexes + metadata-derived relationship graph (Phases L6–L7).

**Objective:** Generate the searchable indexes (`keyword_index.csv`, `author_index.csv`, `venue_index.csv`, `dataset_index.csv`, `model_index.csv`) and the `citation_network.csv` relationship graph — all regenerable from `papers.csv` + summaries.

**Why this step exists:** [Phase L6](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l6--literature-database--indexing) requires indexes that regenerate deterministically; [Phase L7](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l7--paper-relationship-graph) requires relationships derived from metadata only (never guessed), each edge citing its source field.

**Handbook References:** [Phase L6](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l6--literature-database--indexing); [Phase L7](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l7--paper-relationship-graph); Relationship + Knowledge Base agents ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)).

**Prerequisites:** STEP-011 (registry), STEP-012 (summaries).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** Yes — each index is independent.

**Inputs:** `papers.csv`, summaries.

**Expected Outputs:** Five indexes in `02_Literature/indexes/`; `citation_network.csv`; regeneration script spec (implemented by Antigravity as a reusable module in [17_Automation](MASTER_RESEARCH_OPERATING_SYSTEM.md#17_automation)).

**Repository Changes:**
- *New files:* `indexes/{keyword,author,venue,dataset,model}_index.csv`; `citation_network.csv`; a registry-generation module in `17_Automation/` (spec by Cursor, code by Antigravity).

**Cursor Prompt:**
```
You are reviewing the Knowledge Base + Relationship agents.
Using Phase L6 + L7 ONLY:
1. Specify each index (keyword/author/venue/dataset/model): term -> list of P IDs, sourced from papers.csv columns + summaries. Require deterministic regeneration.
2. Specify citation_network.csv edges derived ONLY from metadata (same dataset, improves prior work, new architecture, uses explainability/robustness/cross-dataset/frequency-domain/ViT/foundation model). EACH edge must cite the metadata field(s) that produced it.
3. Write the spec for a reusable Python indexing module (17_Automation) that regenerates all indexes + network from papers.csv + summaries. No guessed relationships.
Output specs + validation (regeneration must reproduce identical files).
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the approved indexing module in 17_Automation/ (packaged, importable) that regenerates keyword/author/venue/dataset/model indexes and citation_network.csv from papers.csv + summaries, then run it to produce the index files in 02_Literature/indexes/.
Constraints: relationships from metadata only; every edge records its source field; deterministic output (re-running yields identical files); no hardcoded/guessed edges.
Definition of Done: five indexes + citation_network.csv generated; re-running the module reproduces them byte-for-byte.
```

**GitHub Expectations:** Branch `feature/literature-indexes` → PR into `develop`. Commit `feat: add deterministic literature indexes and relationship graph`.

**Kaggle Expectations:** None.

**Documentation Updates:** `02_Literature/README.md` (index list); module README in `17_Automation`.

**Verification Checklist:**
- ✓ Five indexes present, each mapping term → `P` IDs.
- ✓ `citation_network.csv` edges each cite a source metadata field.
- ✓ Re-running the module reproduces identical files (deterministic).
- ✓ No guessed relationships.
- ✓ Module packaged in [17_Automation](MASTER_RESEARCH_OPERATING_SYSTEM.md#17_automation) (not a stray script).

**Common Mistakes:** Hardcoded relationships; non-deterministic ordering; a one-off script instead of a reusable module.

**Recovery Procedure:** If regeneration differs from committed files, fix nondeterminism (sort keys) and regenerate; if an edge lacks a source field, delete it (guessing is forbidden).

**Definition of Done:** Indexes + graph generated deterministically and merged; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-014 — Research Gap Discovery (begins Gap & Direction).

---
# PART 3 — RESEARCH GAP & DIRECTION

> Implements [§3 Phases L8–L12](MASTER_RESEARCH_OPERATING_SYSTEM.md#3-research--literature-workflow). Ends with the **Literature Quality Gate** ([Checklist 2](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-2--literature-review)), which must PASS before Dataset work begins ([§13.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#132-quality-gates)).

---

## STEP-014 — Research Gap Discovery  **[C][A]**

**Title:** Discover gaps from evidence, never invent them (Phase L8 — most important).

**Objective:** Extract every limitation/future-work/weakness/open-problem from the summaries, cluster them, rank by frequency + importance, and produce the [Research Gap Registry](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l8--research-gap-discovery-most-important) `research_gap.csv` plus one `gap/GAPxxxx.md` per gap.

**Why this step exists:** [Phase L8](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l8--research-gap-discovery-most-important) is the pivot from literature to direction; a gap is valid only if supported by ≥2 independent papers or explicitly flagged single-source.

**Handbook References:** [Phase L8 + Research Gap Registry columns](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l8--research-gap-discovery-most-important); [Template 14 Gap](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); Research Gap Agent ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)).

**Prerequisites:** STEP-012 (summaries with extracted limitations), STEP-013 (indexes).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1 day.
**Parallelizable:** No — clustering needs all summaries together.

**Inputs:** All summaries, `future_work` extractions, `papers.csv`.

**Expected Outputs:** `research_gap/research_gap.csv` (`Gap ID, Category, Supporting Papers, Frequency, Conflicting Papers, Importance, Research Opportunity`), `research_gap/gap/GAPxxxx.md` per gap, and `future_work.csv`.

**Repository Changes:**
- *New/updated files:* `research_gap.csv`, `gap/GAPxxxx.md`, `future_work.csv`.
- *Registry:* Research Gap Registry (owner: Research Gap Agent).

**Cursor Prompt:**
```
You are reviewing the Research Gap Agent (extract + rank gaps from evidence; never invent).
Using Phase L8 + Template 14 ONLY:
1. Aggregate every limitation/weakness/future-work/open-problem across all Pxxxx_summary.md, tagging each with its source P ID.
2. Cluster into candidate gaps; for each, compute Frequency (count of independent supporting papers), list Supporting Papers and any Conflicting Papers, and rate Importance.
3. Enforce validity: a gap needs >=2 independent supporting papers OR an explicit single-source-hypothesis flag.
4. Draft research_gap.csv rows + one GAPxxxx.md per gap (Template 14: Gap ID, Category, Supporting Papers, Frequency, Importance, Potential Contribution, Implementation Difficulty, Publication Potential).
Output for review. Every gap must link to its supporting P IDs.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Save the approved research_gap.csv rows and GAPxxxx.md files, plus future_work.csv.
Constraints: every gap row lists its Supporting Papers (P IDs); no gap without >=2 independent supporters unless flagged single-source; append-or-update only.
Definition of Done: gap registry + per-gap files complete and traceable to P IDs.
```

**GitHub Expectations:** Branch `research/gap-discovery` → PR into `develop`. Commit `research: derive research gap registry from literature evidence`.

**Kaggle Expectations:** None.

**Documentation Updates:** `research_gap.csv`, gap files, `future_work.csv`; dashboard.

**Verification Checklist:**
- ✓ Every gap links to supporting `P` IDs.
- ✓ Each gap has ≥2 independent supporters or a single-source flag.
- ✓ Frequency + Importance recorded; conflicts noted.
- ✓ One `GAPxxxx.md` per gap (Template 14).
- ✓ No invented gaps.

**Common Mistakes:** Inventing a gap not grounded in summaries; counting the same author group as independent support; missing conflict evidence.

**Recovery Procedure:** For any unsupported gap, either find ≥2 supporters or mark it single-source-hypothesis; delete truly ungrounded gaps. Re-trace each `GAP` to its summaries.

**Definition of Done:** Evidence-based gap registry complete; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-015 — Build the Claim Database.

---

## STEP-015 — Build the Claim Database  **[C][A]**

**Title:** Every scientific claim gets a supported ledger row (Phase L9).

**Objective:** Populate the [Claim Database](MASTER_RESEARCH_OPERATING_SYSTEM.md#claim-database) `claim_database.csv`, the shared evidence ledger linking literature (and later experimental) evidence, used by [Writing Claim Verification (W11)](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w11--claim-verification).

**Why this step exists:** [Phase L9](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l9--evidence-collection-claim-database) makes every claim supportable; it is the backbone of all writing.

**Handbook References:** [Phase L9 + Claim Database columns](MASTER_RESEARCH_OPERATING_SYSTEM.md#claim-database); [Template 13 Claim](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); Knowledge Base Agent ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)).

**Prerequisites:** STEP-012 (summaries), STEP-014 (gaps).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** Yes — claims are independent rows.

**Inputs:** Summaries, `research_gap.csv`, `papers.csv`.

**Expected Outputs:** `claims/claim_database.csv` (`Claim ID, Statement, Supporting Papers, Supporting Experiments, Supporting Figures, Supporting Tables, Contradicting Evidence, Confidence, Page References, Status`) and `claim/CLAIMxxxx.md` per major claim.

**Repository Changes:**
- *Updated:* `claim_database.csv`; new `claim/CLAIMxxxx.md`.
- *Registry:* Claim Database (owner: Knowledge Base Agent).

**Cursor Prompt:**
```
You are reviewing the Knowledge Base Agent (maintain Claim Database + indexes; never alter source papers).
Using Phase L9 + Template 13 ONLY:
1. From summaries + gaps, extract candidate scientific claims relevant to our research question.
2. For each, draft a claim_database.csv row: Statement, Supporting Papers (P IDs), Supporting Experiments (empty for now), Figures/Tables (empty), Contradicting Evidence, Confidence, Page References, Status=draft.
3. For major claims, draft CLAIMxxxx.md (Template 13).
Rule: no claim without at least one supporting P ID (experimental support is added later in the model phase). Output for review.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Save approved claim_database.csv rows + CLAIMxxxx.md files.
Constraints: every claim has >=1 supporting P ID and page references where available; Status field set; append-or-update only; leave Supporting Experiments/Figures/Tables empty to be filled after experiments.
Definition of Done: claim ledger populated and traceable.
```

**GitHub Expectations:** Branch `research/claim-database` → PR into `develop`. Commit `research: populate claim database from literature evidence`.

**Kaggle Expectations:** None.

**Documentation Updates:** `claim_database.csv`, claim files.

**Verification Checklist:**
- ✓ Every claim row has ≥1 supporting `P` ID.
- ✓ Page references recorded where available; Confidence + Status set.
- ✓ Contradicting evidence captured where it exists.
- ✓ Experiment/figure/table support left empty (filled post-experiment).

**Common Mistakes:** Claims with no support; over-confident status; ignoring contradictory evidence.

**Recovery Procedure:** Remove or downgrade unsupported claims; add contradicting evidence found in summaries. Never mark a claim `verified` without support.

**Definition of Done:** Claim ledger populated + traceable; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-016 — Research Direction Selection.

---

## STEP-016 — Research Direction Selection  **[C][H]**

**Title:** The AI proposes candidate directions; the human decides (Phase L10).

**Objective:** Produce `research_directions.md` (top candidates with advantages/disadvantages/complexity/novelty/publication potential/decision criteria) and record the human's chosen direction in the Decision Log.

**Why this step exists:** [Phase L10](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l10--research-direction-selection) + [§1.9](MASTER_RESEARCH_OPERATING_SYSTEM.md#19-human-in-the-loop-rule): direction selection is an irreversible scientific decision reserved for the human. It anchors [DEF-002/DEF-004](MASTER_RESEARCH_OPERATING_SYSTEM.md#111-deferred-decisions).

**Handbook References:** [Phase L10](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l10--research-direction-selection); [§1.9](MASTER_RESEARCH_OPERATING_SYSTEM.md#19-human-in-the-loop-rule); [§1.11 Deferred Decisions](MASTER_RESEARCH_OPERATING_SYSTEM.md#111-deferred-decisions); [Template 3](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); Research Planning Agent ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)).

**Prerequisites:** STEP-014 (gaps), STEP-015 (claims).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day (+ human deliberation).
**Parallelizable:** No — gates everything downstream.

**Inputs:** `research_gap.csv`, `claim_database.csv`, `papers.csv`.

**Expected Outputs:** `research_directions.md`; `DECxxxx.md` recording the selected direction; alignment note tying the direction to the primary contribution (the [AI Forensic Analyst](MASTER_RESEARCH_OPERATING_SYSTEM.md#6-ai-forensic-analyst-architecture)).

**Repository Changes:**
- *New files:* `02_Literature/research_directions.md`, `01_Project_Management/decision_log/DECxxxx.md`.

**Cursor Prompt:**
```
You are the Research Planning Agent (propose only; NEVER select the final topic).
Using Phase L10 + the gap registry + claim database ONLY:
1. Propose the top 3-5 candidate research directions grounded in specific GAP IDs, each with: advantages, disadvantages, complexity, novelty, publication potential, implementation difficulty, dataset needs, evaluation needs, future scalability, and OBJECTIVE decision criteria.
2. Show how each direction supports the project's primary contribution (the AI Forensic Analyst, §1.2/§6), not just a better classifier.
3. Draft research_directions.md + a Template-3 decision log stub for the human to complete with their choice.
Stop and require human selection (A.8 protocol). Do not choose.
```

**Google Antigravity Prompt:** *None — human decision; no implementation.*

**GitHub Expectations:** Branch `research/direction-selection` → PR into `develop`. Commit `research: record selected research direction (DECxxxx)`.

**Kaggle Expectations:** None.

**Documentation Updates:** `research_directions.md`, decision log; dashboard.

**Verification Checklist:**
- ✓ ≥3 candidate directions, each grounded in `GAP` IDs.
- ✓ Objective decision criteria stated per direction.
- ✓ Human has explicitly chosen; recorded in a `DEC` entry.
- ✓ Chosen direction supports the AI Forensic Analyst contribution.

**Common Mistakes:** AI selecting the direction; direction untethered from gaps; direction that reduces the project to a plain classifier (contradicts [§1.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#12-project-identity)).

**Recovery Procedure:** If a direction lacks gap support, return to STEP-014. If it contradicts the forensic-system contribution, reject and re-propose. Never proceed without the recorded human decision.

**Definition of Done:** Direction chosen + logged; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-017 — Literature review generation + Literature Gate.

---

## STEP-017 — Generate the Living Literature Review + Literature Gate  **[C][A][H]**  **GATE (Checklist 2)**

**Title:** Produce the living review draft and pass the Literature Quality Gate (Phases L11–L12).

**Objective:** Generate `literature_review.md` and `related_work.md` (every paragraph traced to papers/summaries/claims/gaps), establish the incremental-update convention, and run [Checklist 2](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-2--literature-review) as the gate closing the literature phase.

**Why this step exists:** [Phases L11–L12](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l11--living-literature-review) require an evidence-generated, continuously updatable review; [§13.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#132-quality-gates) forbids starting Dataset work until Checklist 2 PASSes.

**Handbook References:** [Phase L11](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l11--living-literature-review); [Phase L12](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l12--literature-review-generation); [Checklist 2](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-2--literature-review); [§9 Writing rules (W7)](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w7--writing-rules); [A.10 Audit structure](MASTER_RESEARCH_OPERATING_SYSTEM.md#a10-canonical-audit-report-structure).

**Prerequisites:** STEP-013 (indexes), STEP-014 (gaps), STEP-015 (claims), STEP-016 (direction).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1–2 days.
**Parallelizable:** Partially — Related Work vs. trends sections can be drafted separately.

**Inputs:** Summaries, `papers.csv`, `research_gap.csv`, `claim_database.csv`, indexes, comparison data.

**Expected Outputs:** `drafts/literature_review.md`, `drafts/related_work.md`, a comparison table spec (→ [10_Tables](MASTER_RESEARCH_OPERATING_SYSTEM.md#10_tables)), the incremental-update rule, and `literature_audit.md` = PASS.

**Repository Changes:**
- *New files:* `02_Literature/drafts/{literature_review,related_work}.md`; comparison `TABxxxx_spec.md` in `10_Tables/specs/`; `literature_audit.md`.

**Cursor Prompt:**
```
You are the Literature Writer Agent (evidence-based prose) + Literature Auditor.
Using Phases L11-L12 + §9.7 writing rules + Checklist 2 ONLY:
1. Draft literature_review.md and related_work.md where EVERY paragraph cites specific P IDs / CLAIM IDs / GAP IDs. No hallucinated citations. Follow the academic tone rules (no AI filler, no gratuitous em-dashes).
2. Produce a comparison table SPEC (Template 12) for related work (methods x datasets x metrics), data sourced from papers.csv — spec only, not a rendered figure/table.
3. Define the incremental-update rule (new paper -> update only affected sections, with version history).
4. Run Checklist 2 (research question, search strategy, registration, metadata, summaries, gaps, claim DB, knowledge index, citation verification, related-work completeness) and output literature_audit.md (A.10 structure) with PASS/FAIL per item.
Output drafts + audit for human approval.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Save the approved literature_review.md, related_work.md, the comparison TABxxxx_spec.md, and literature_audit.md at their paths. If a citation-verification script is specified, implement it in 17_Automation to check every cited key against papers.csv/papers.bib.
Constraints: no citation without a matching P ID; drafts saved verbatim; no rendered tables/figures (specs only).
Definition of Done: drafts + comparison spec + audit saved; citation-verification passes (every cited key exists in papers.bib).
```

**GitHub Expectations:** Branch `writing/literature-review` → PR into `develop`, then **[H]** ensure Checklist 2 PASS before merge. Commit `writing: generate living literature review and pass literature gate`.

**Kaggle Expectations:** None.

**Documentation Updates:** Drafts; comparison spec; `literature_audit.md`; dashboard.

**Verification Checklist (GATE — [Checklist 2](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-2--literature-review)):**
- ✓ Research question approved; search strategy reproducible.
- ✓ Every paper registered with metadata + summary.
- ✓ Research gaps derived + supported; Claim Database populated.
- ✓ Knowledge/indexes complete; every citation verified against `papers.csv`/`papers.bib`.
- ✓ Related-work draft complete; every paragraph traces to evidence.
- ✓ `literature_audit.md` = PASS.

**Common Mistakes:** Hallucinated citations; prose from memory; skipping citation verification; declaring the review "finished" (it is living).

**Recovery Procedure:** If Checklist 2 FAILS, do **not** start Dataset work. Fix each failed item (missing summary, unverified citation, unsupported paragraph) and re-audit. Any citation lacking a `P` ID is removed by the Citation Verification Agent.

**Definition of Done:** Review drafted from evidence; **[Checklist 2](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-2--literature-review) = PASS**; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied. Literature phase complete.

**Next Step:** STEP-018 — Dataset Discovery (begins the Dataset Operating System).

---
# PART 4 — DATASET DISCOVERY → DOCUMENTATION

> Implements [§4 Dataset Operating System](MASTER_RESEARCH_OPERATING_SYSTEM.md#4-dataset-operating-system), Phases D1–D8. Files live in [03_Datasets](MASTER_RESEARCH_OPERATING_SYSTEM.md#03_datasets). Large image data never enters Git — it lives in the [data tier / Kaggle Datasets (A.6)](MASTER_RESEARCH_OPERATING_SYSTEM.md#a6-canonical-storage--synchronization-policy). Ends with the **Dataset Readiness Gate** ([Checklist 3](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-3--dataset-readiness)).

---

## STEP-018 — Dataset Discovery  **[C][A]**

**Title:** Find candidate datasets and record them (Phase D1).

**Objective:** Produce `dataset_candidates.csv` (`Candidate ID, Name, Source, URL, License seen, Availability, Duplicate-of, Notes`) covering Kaggle, Hugging Face, GitHub, papers, project sites, Zenodo, Figshare, OpenML, with duplicates flagged and licenses recorded at first sight.

**Why this step exists:** [Phase D1](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d1--dataset-discovery) begins the dataset lifecycle; the chosen research direction (STEP-016) determines what data is needed.

**Handbook References:** [Phase D1](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d1--dataset-discovery); [§4.1 Lifecycle](MASTER_RESEARCH_OPERATING_SYSTEM.md#41-lifecycle-overview); Dataset Discovery Agent ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)); [dataset_index.csv](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-l6--literature-database--indexing) from literature.

**Prerequisites:** STEP-017 (Literature Gate PASS + selected direction).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** Yes — sources searched independently.

**Inputs:** `research_directions.md`, `dataset_index.csv` (datasets seen in the literature), research question.

**Expected Outputs:** `03_Datasets/metadata/dataset_candidates.csv` populated; duplicate flags; license-seen notes.

**Repository Changes:**
- *Updated:* `dataset_candidates.csv`.
- *Registry:* Dataset Candidates (owner: Dataset Discovery Agent).

**Cursor Prompt:**
```
You are reviewing the Dataset Discovery Agent (find candidates only; do not evaluate/download).
Using Phase D1 + the literature dataset_index.csv ONLY:
1. Compile candidate AI-generated-face datasets from Kaggle, Hugging Face, GitHub, cited papers, project sites, Zenodo, Figshare, OpenML — prioritizing datasets already used in our registered papers.
2. For each, draft a dataset_candidates.csv row (Candidate ID, Name, Source, URL, License seen, Availability, Duplicate-of, Notes). Flag duplicates by name/DOI/mirror.
3. Note generator diversity (GAN families, diffusion, etc.) relevant to our unseen-generator evaluation plan (E9).
Output rows for review. Do not score or select yet.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Save the approved dataset_candidates.csv rows.
Constraints: one row per candidate; duplicates flagged in Duplicate-of; license recorded as seen; append-or-update only.
Definition of Done: candidates recorded with sources, licenses, and duplicate flags.
```

**GitHub Expectations:** Branch `dataset/discovery` → PR into `develop`. Commit `dataset: record candidate datasets`.

**Kaggle Expectations:** None yet (no download).

**Documentation Updates:** `dataset_candidates.csv`; `03_Datasets/README.md`.

**Verification Checklist:**
- ✓ Candidates cover multiple sources + generator families.
- ✓ Licenses recorded at first sight; duplicates flagged.
- ✓ Candidates linked to datasets seen in the literature where applicable.
- ✓ No scoring/selection yet (that is D2).

**Common Mistakes:** Missing license info; unflagged mirrors/duplicates; ignoring generator diversity needed for E9.

**Recovery Procedure:** Re-scan sources for license terms; merge duplicate candidates via `Duplicate-of`. Do not download anything in this step.

**Definition of Done:** Candidate list complete + licensed + deduped; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-019 — Dataset evaluation & selection.

---

## STEP-019 — Dataset Evaluation & Selection  **[C][A][H]**

**Title:** Objective scoring, human approval of which datasets proceed (Phase D2, DEF-003).

**Objective:** Produce `dataset_evaluation.csv` scoring each candidate on the [Phase D2](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d2--dataset-evaluation) dimensions; the human approves the datasets that proceed (resolves [DEF-003](MASTER_RESEARCH_OPERATING_SYSTEM.md#111-deferred-decisions) for the training gate).

**Why this step exists:** [Phase D2](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d2--dataset-evaluation): the AI ranks, the human decides — dataset choice is a blocking scientific decision.

**Handbook References:** [Phase D2](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d2--dataset-evaluation); [DEF-003](MASTER_RESEARCH_OPERATING_SYSTEM.md#111-deferred-decisions); [§1.9](MASTER_RESEARCH_OPERATING_SYSTEM.md#19-human-in-the-loop-rule); Dataset Evaluation Agent ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)).

**Prerequisites:** STEP-018 (candidates).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day (+ human deliberation).
**Parallelizable:** Yes — scoring per candidate.

**Inputs:** `dataset_candidates.csv`.

**Expected Outputs:** `dataset_evaluation.csv` (scored + ranked); `DECxxxx.md` recording the approved dataset(s).

**Repository Changes:**
- *Updated:* `dataset_evaluation.csv`.
- *New:* `decision_log/DECxxxx.md` (dataset approval, DEF-003).

**Cursor Prompt:**
```
You are reviewing the Dataset Evaluation Agent (score + rank; the human approves).
Using Phase D2 ONLY:
1. Score every candidate on: Dataset Size, Image Quality, Resolution, Label Quality, Metadata Quality, Class Balance, License, Source Credibility, Research Popularity, Citation Count, Top-Conference Use, Availability, Maintenance, Bias, Explainability Suitability, Generalization Suitability.
2. Produce a ranked dataset_evaluation.csv and a short comparison memo with objective selection criteria tied to our direction and to the unseen-generator evaluation (E9).
3. Draft a Template-3 decision log for the human to approve the selected dataset(s) — this resolves DEF-003.
Stop and require human approval (A.8). Do not select.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Save the approved dataset_evaluation.csv and the DECxxxx.md capturing the human's dataset selection.
Constraints: scores comparable across candidates; decision log records rejected options + reasons; append-or-update only.
Definition of Done: scored/ranked evaluation saved; human selection recorded.
```

**GitHub Expectations:** Branch `dataset/evaluation` → PR into `develop`. Commit `dataset: score/rank candidates and record selection (DECxxxx)`.

**Kaggle Expectations:** None.

**Documentation Updates:** `dataset_evaluation.csv`; decision log; dashboard.

**Verification Checklist:**
- ✓ Every candidate scored on all D2 dimensions.
- ✓ Ranking objective + reproducible; criteria documented.
- ✓ Human approval recorded (DEF-003 resolved for training gate).
- ✓ Selection supports generalization/unseen-generator goals.

**Common Mistakes:** AI selecting the dataset; ignoring license/bias; choosing a single-generator dataset that blocks E9.

**Recovery Procedure:** If a license is incompatible, exclude the dataset and re-rank. If no dataset supports generator diversity, return to STEP-018 to find more. Never train on an unapproved dataset ([§4.3](MASTER_RESEARCH_OPERATING_SYSTEM.md#43-dataset-research-rules-binding)).

**Definition of Done:** Datasets scored + approved; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-020 — Dataset registration.

---

## STEP-020 — Dataset Registration  **[C][A]**

**Title:** Assign `DSxxxx` IDs and full metadata (Phase D3).

**Objective:** For each approved dataset, create a row in `datasets.csv` (`Dataset ID, Name, Version, Source, Download URL, License, Citation, Publication, Image Count, Real/Fake Images, Resolution, File Format, Split Available, Metadata, Downloaded, Validated, Ready`).

**Why this step exists:** [Phase D3](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d3--dataset-registration): every accepted dataset gets a `DS` ID + metadata before download.

**Handbook References:** [Phase D3](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d3--dataset-registration); [A.1 IDs](MASTER_RESEARCH_OPERATING_SYSTEM.md#a1-canonical-identifier-scheme); Metadata Agent ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)).

**Prerequisites:** STEP-019 (approved datasets).

**Estimated Difficulty:** Easy.
**Estimated Time:** 1–2 hours.
**Parallelizable:** Yes.

**Inputs:** Approved datasets + evaluation.

**Expected Outputs:** `datasets.csv` rows with `Downloaded=no, Validated=no, Ready=no` (updated as later steps complete); license files placed in `03_Datasets/licenses/`.

**Repository Changes:**
- *Updated:* `datasets.csv`.
- *New:* `03_Datasets/licenses/DSxxxx_license.txt`.
- *Registry:* Datasets (owner: Metadata Agent).

**Cursor Prompt:**
```
You are reviewing the Metadata Agent.
Using Phase D3 ONLY: for each approved dataset, draft a datasets.csv row with a new DSxxxx ID and all columns (Version, Source, Download URL, License, Citation, Publication, Image Count, Real/Fake, Resolution, File Format, Split Available, Metadata, Downloaded=no, Validated=no, Ready=no). Specify which license text to save under 03_Datasets/licenses/. Output rows for review.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Append the approved DSxxxx rows to datasets.csv and save each dataset's license text to 03_Datasets/licenses/DSxxxx_license.txt.
Constraints: unique DS IDs; status flags all "no" until proven; append-or-update only; do not download image data.
Definition of Done: every approved dataset registered with a DS ID and license on file.
```

**GitHub Expectations:** Branch `dataset/registration` → PR into `develop`. Commit `dataset: register approved datasets with DS IDs`.

**Kaggle Expectations:** None.

**Documentation Updates:** `datasets.csv`; licenses.

**Verification Checklist:**
- ✓ Each approved dataset has a unique `DSxxxx` row.
- ✓ License text saved; citation recorded.
- ✓ Status flags start `no`.
- ✓ No image data in Git.

**Common Mistakes:** Reusing a `DS` ID; missing license file; premature `Ready=yes`.

**Recovery Procedure:** If a `DS` ID collides, assign the next free ID (never reuse). Add any missing license before download.

**Definition of Done:** Datasets registered; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-021 — Dataset download & raw-lock.

---

## STEP-021 — Dataset Download & Raw-Lock  **[C][H][K]**

**Title:** Acquire data with integrity guarantees; make `raw/` immutable (Phases D4–D5).

**Objective:** Download each `DSxxxx` into the data tier (Kaggle Dataset), record SHA-256 checksums, verify integrity, place immutable originals under `raw/DSxxxx/`, and mark `Downloaded=yes`.

**Why this step exists:** [Phase D4](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d4--dataset-download) requires checksums + integrity; [Phase D5 (sacred)](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d5--raw-dataset-policy-sacred) makes raw data immutable. Large data lives in [Kaggle Datasets, never Git (A.6/D19)](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d19--kaggle-data-workflow).

**Handbook References:** [Phase D4](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d4--dataset-download); [Phase D5](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d5--raw-dataset-policy-sacred); [Phase D19 Kaggle Data Workflow](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d19--kaggle-data-workflow); [A.6 Storage Tiers](MASTER_RESEARCH_OPERATING_SYSTEM.md#a6-canonical-storage--synchronization-policy); [A.8 Human Task](MASTER_RESEARCH_OPERATING_SYSTEM.md#a8-human-task-protocol).

**Prerequisites:** STEP-020 (registered datasets + licenses).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day–1 day (download-bound).
**Parallelizable:** Yes — datasets download independently.

**Inputs:** `datasets.csv` download URLs; Kaggle account.

**Expected Outputs:** Data in a Kaggle Dataset (data tier); checksum records in `03_Datasets/reports/integrity_report.csv`; `raw/DSxxxx/` structure documented (metadata/pointers in Git, not the images); `Downloaded=yes`.

**Repository Changes:**
- *Updated:* `datasets.csv` (`Downloaded=yes`), `reports/integrity_report.csv` (checksums), pointer/README describing the Kaggle Dataset location. **No image bytes in Git.**

**Cursor Prompt:**
```
You are planning the dataset download + raw-lock (Metadata/Validation agents).
Using Phase D4, D5, D19, A.6 ONLY:
1. Produce a Human Task block (A.8) for downloading each DSxxxx: source URL, exact Kaggle Dataset to create/upload to, folder layout raw/DSxxxx/, and how to compute + record SHA-256 checksums.
2. Specify the integrity_report.csv schema (file, size, sha256, status) and the pointer note to store in Git (Kaggle Dataset slug/version) — NO image bytes in Git.
3. State the raw-lock rule explicitly: after placement, raw/ is immutable; all transforms happen in processed/.
Output the human instructions + report schemas.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY (metadata/scripts, not data). Implement a reusable checksum + integrity-verification module in 17_Automation that, given a raw/DSxxxx path on Kaggle, computes SHA-256 per file and emits integrity_report.csv. Save the Git-side pointer note (Kaggle Dataset slug + version) under 03_Datasets/metadata/.
Constraints: never add image bytes to Git; never modify raw files (read-only). 
Definition of Done: integrity module exists; checksum report format ready to run on Kaggle.
```

**Kaggle Expectations:** A **Kaggle Dataset** is created containing `raw/DSxxxx/` (the data tier). The checksum module runs in a Kaggle notebook to produce `integrity_report.csv`, which is synced back to GitHub. The raw images remain in the Kaggle Dataset; only the report + pointer return to Git.

**GitHub Expectations:** Branch `dataset/download` → PR into `develop`. Commit `dataset: record download checksums and Kaggle dataset pointer for DSxxxx`. **No large binaries.**

**Documentation Updates:** `integrity_report.csv`; Kaggle pointer note; `datasets.csv` status.

**Verification Checklist:**
- ✓ Data present in the Kaggle Dataset (data tier), not Git.
- ✓ SHA-256 recorded per archive/file; integrity verified.
- ✓ `raw/DSxxxx/` documented as immutable; nothing modifies it.
- ✓ Git holds only pointers + reports (no images).
- ✓ `datasets.csv` `Downloaded=yes`.

**Common Mistakes:** Committing images to Git; modifying `raw/`; missing checksums; no Kaggle pointer recorded.

**Recovery Procedure:** If images were committed to Git, remove from history immediately and move to the Kaggle Dataset. If `raw/` was altered, re-download from source and re-verify checksums — the original must match the source exactly ([Phase D5](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d5--raw-dataset-policy-sacred)).

**Definition of Done:** Data acquired, checksummed, raw-locked, pointer recorded; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-022 — Dataset validation.

---

## STEP-022 — Dataset Validation  **[C][A][K]**

**Title:** Catch broken/duplicate/mislabeled/corrupted data (Phase D6).

**Objective:** Produce `validation_report.csv`, `quality_report.csv`, `integrity_report.csv` covering broken/duplicate images, wrong labels, corrupted/unsupported files, invalid filenames, missing labels/metadata, resolution/aspect-ratio analysis.

**Why this step exists:** [Phase D6](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d6--dataset-validation) guarantees data quality before any training.

**Handbook References:** [Phase D6](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d6--dataset-validation); Validation + Quality agents ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)); [Checklist 3](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-3--dataset-readiness).

**Prerequisites:** STEP-021 (raw data + checksums).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day (compute on Kaggle).
**Parallelizable:** Yes — per dataset.

**Inputs:** `raw/DSxxxx/` on Kaggle; integrity checksums.

**Expected Outputs:** Three validation reports in `03_Datasets/reports/`; `datasets.csv` `Validated=yes` when clean (or issues logged).

**Repository Changes:**
- *Updated:* `reports/{validation,quality,integrity}_report.csv`, `datasets.csv`.

**Cursor Prompt:**
```
You are reviewing the Validation + Quality agents.
Using Phase D6 ONLY, specify a reusable validation module (packaged in 04_Preprocessing or 17_Automation) that scans raw/DSxxxx and reports: broken/corrupted images, duplicates (hash), wrong/missing labels, unsupported formats, invalid filenames, resolution + aspect-ratio distribution, channel checks. Define validation_report.csv / quality_report.csv / integrity_report.csv schemas. Reads raw as read-only.
Output the module spec + report schemas + acceptance thresholds.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the approved validation module (packaged, importable) that reads raw/DSxxxx READ-ONLY and emits the three reports. Provide a Kaggle notebook (EXP-style not needed; put under 04_Preprocessing/notebooks or 17_Automation) to run it.
Constraints: never modify raw files; deterministic reports; handle errors explicitly (no silent skips — §1.7 error philosophy).
Definition of Done: module runs on Kaggle over raw/DSxxxx and produces the three reports; results synced to GitHub.
```

**Kaggle Expectations:** Validation notebook runs over the raw Kaggle Dataset; produces the three reports; reports (small CSVs) synced back to GitHub. Data stays in Kaggle.

**GitHub Expectations:** Branch `dataset/validation` → PR into `develop`. Commit `dataset: validate DSxxxx and record quality/integrity reports`.

**Documentation Updates:** Three reports; `datasets.csv` status.

**Verification Checklist:**
- ✓ Broken/duplicate/mislabeled/corrupted/invalid detected + reported.
- ✓ Resolution + aspect-ratio distributions recorded.
- ✓ Reports deterministic; raw untouched.
- ✓ `datasets.csv` `Validated=yes` (or issues logged with a plan).

**Common Mistakes:** Silent skipping of unreadable files; modifying raw during validation; committing image bytes.

**Recovery Procedure:** If issues found, log them (do not delete raw); decide in preprocessing (STEP-025) whether to filter. If raw was modified, re-download + re-checksum.

**Definition of Done:** Validation complete + reported; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-023 — Exploratory Dataset Analysis.

---

## STEP-023 — Exploratory Dataset Analysis (EDA)  **[C][A][K]**

**Title:** Understand the data before training; figure specs only (Phase D7).

**Objective:** Analyze class/generator/identity distribution, resolution, brightness/contrast, color channels, compression, balance (and, if available, demographic distributions), producing analysis data + **figure specifications** (never rendered figures).

**Why this step exists:** [Phase D7](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d7--exploratory-dataset-analysis) requires understanding before training; [Figure Policy A.9](MASTER_RESEARCH_OPERATING_SYSTEM.md#a9-canonical-figure-policy) forbids the AI rendering figures — it produces specs.

**Handbook References:** [Phase D7](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d7--exploratory-dataset-analysis); [Phase D17 Dataset Figures](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d17--dataset-figures); [A.9 Figure Policy](MASTER_RESEARCH_OPERATING_SYSTEM.md#a9-canonical-figure-policy); Statistics Agent ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)).

**Prerequisites:** STEP-022 (validated data).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** Yes.

**Inputs:** Validated `raw/DSxxxx/`.

**Expected Outputs:** EDA data CSVs in `03_Datasets/reports/`; `FIGxxxx_spec.md` figure specs in `09_Figures/specs/`; the generation script/notebook.

**Repository Changes:**
- *New files:* EDA CSVs; `09_Figures/specs/FIGxxxx_spec.md`; generation notebook (outputs stripped).

**Cursor Prompt:**
```
You are reviewing the Statistics Agent.
Using Phase D7 + A.9 ONLY:
1. Specify EDA analyses (AI recommends, human approves scope): class distribution, resolution, brightness, contrast, color channels, compression, balance, generator distribution, identity distribution; and if available age/gender/ethnicity, missing values, outliers.
2. For each visual, produce a FIGxxxx_spec.md (Template 11): purpose, required data + source, chart type, axes+units, legend, caption, colors, data path, responsible notebook, expected filename. NO rendered images.
3. Specify a reusable EDA module + notebook to compute the underlying data on Kaggle.
Output specs + module plan.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the EDA module + Kaggle notebook that computes the approved statistics over raw/DSxxxx (read-only) and writes EDA data CSVs. Save the FIGxxxx_spec.md files (data-only specs).
Constraints: DO NOT render/save publication figures (A.9) — produce data + specs only; strip notebook outputs before commit (A.7).
Definition of Done: EDA data CSVs produced on Kaggle + synced; figure specs saved; no rendered figures committed.
```

**Kaggle Expectations:** EDA notebook computes distributions over the Kaggle Dataset; outputs small CSVs synced to GitHub.

**GitHub Expectations:** Branch `dataset/eda` → PR into `develop`. Commit `dataset: EDA data and figure specifications for DSxxxx`.

**Documentation Updates:** EDA CSVs; figure specs; `09_Figures/README.md`.

**Verification Checklist:**
- ✓ Required distributions computed; balance + generator distribution known.
- ✓ Every visual is a `FIGxxxx_spec.md` (no rendered figure).
- ✓ Generation notebook present with outputs stripped.
- ✓ Data paths recorded for reproducibility.

**Common Mistakes:** Rendering figures (violates A.9); committing notebook outputs; skipping generator/identity distribution (needed for splits + E9).

**Recovery Procedure:** Replace any rendered figure with a spec + data. Recompute distributions if identity/generator info was missed (critical for leakage-safe splits).

**Definition of Done:** EDA complete as data + specs; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-024 — Dataset documentation + Dataset Gate.

---

## STEP-024 — Dataset Documentation + Dataset Readiness Gate  **[C][A][H]**  **GATE (Checklist 3)**

**Title:** Produce the dataset report + card and pass the Dataset Readiness Gate (Phase D8).

**Objective:** Produce `dataset_report.md` ([Template 5](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates)) and `dataset_card.md` ([Template 23](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates)), then run [Checklist 3](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-3--dataset-readiness). Note: full readiness (`Ready=yes`) requires preprocessing + splits (Part 5); this gate confirms the *raw dataset* is documented + validated.

**Why this step exists:** [Phase D8](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d8--dataset-documentation) requires documented origin/license/statistics/bias/usage; [Checklist 3](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-3--dataset-readiness) gates the dataset phase.

**Handbook References:** [Phase D8](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d8--dataset-documentation); [Template 5](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); [Template 23](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); [Checklist 3](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-3--dataset-readiness); Documentation Agent ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)).

**Prerequisites:** STEP-020…023.

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** Yes — report vs. card.

**Inputs:** Validation + EDA reports; `datasets.csv`; licenses.

**Expected Outputs:** `dataset_report.md`, `dataset_card.md`, `dataset_audit.md` = PASS (for the validated raw dataset).

**Repository Changes:**
- *New files:* `03_Datasets/reports/dataset_report.md`, `dataset_card.md`, `dataset_audit.md`.

**Cursor Prompt:**
```
You are the Documentation Agent + Dataset Auditor.
Using Phase D8 + Templates 5 & 23 + Checklist 3 ONLY:
1. Draft dataset_report.md (origin, purpose, license, statistics, strengths, weaknesses, known biases, recommended usage, known problems, research relevance, citation, location) and dataset_card.md (Template 23).
2. Run Checklist 3 items applicable at this stage (registered, license verified, metadata complete, validation done, integrity/quality/dataset reports present, version assigned) and emit dataset_audit.md (A.10). Mark preprocessing/split/no-leakage items as PENDING (completed in Part 5).
Output for human approval.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Save the approved dataset_report.md, dataset_card.md, and dataset_audit.md.
Constraints: content matches approved drafts; cite the exact report/CSV sources; no invented statistics.
Definition of Done: report + card + audit saved; sources cited.
```

**GitHub Expectations:** Branch `dataset/documentation` → PR into `develop`; **[H]** confirm Checklist-3 (raw-dataset items) PASS. Commit `dataset: document DSxxxx and pass dataset readiness (raw) gate`.

**Kaggle Expectations:** None (documentation).

**Documentation Updates:** Report, card, audit; `03_Datasets/README.md`.

**Verification Checklist (GATE — [Checklist 3](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-3--dataset-readiness), raw-stage items):**
- ✓ Dataset registered; license verified; metadata complete.
- ✓ Validation done; integrity/quality/dataset reports present.
- ✓ Version assigned; report + card complete + evidence-cited.
- ✓ Preprocessing/split/no-leakage items marked PENDING → completed in Part 5 (STEP-029 finalizes the gate).
- ✓ `dataset_audit.md` PASS for raw-stage items.

**Common Mistakes:** Declaring `Ready=yes` before splits exist; invented statistics; missing bias/limitations.

**Recovery Procedure:** If any raw-stage item FAILS, fix (re-validate, complete metadata) and re-audit before preprocessing. Do not set `Ready=yes` until STEP-029.

**Definition of Done:** Raw dataset documented; **Checklist 3 raw-stage items = PASS**; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-025 — Preprocessing pipeline design (begins Preprocessing).

---
# PART 5 — PREPROCESSING → SPLITS → MASTER REGISTRY

> Implements [§4 Phases D9–D15](MASTER_RESEARCH_OPERATING_SYSTEM.md#4-dataset-operating-system). Modular, versioned pipelines in [04_Preprocessing](MASTER_RESEARCH_OPERATING_SYSTEM.md#04_preprocessing); processed data in the [data tier](MASTER_RESEARCH_OPERATING_SYSTEM.md#a6-canonical-storage--synchronization-policy). Ends with the **Preprocessing Gate** ([Checklist 4](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-4--preprocessing)) and finalizes the [Dataset Readiness Gate](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-3--dataset-readiness).

---

## STEP-025 — Preprocessing Pipeline Design  **[C]**

**Title:** Design modular, independent preprocessing steps (Phase D9 — design).

**Objective:** Produce the preprocessing design: independent, testable, reusable modules for image verification, face detection, alignment, cropping, resize, normalization, quality filtering, artifact removal, format conversion, metadata extraction — never one monolithic script.

**Why this step exists:** [Phase D9](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d9--preprocessing-workflow) mandates modular preprocessing; [§1.10](MASTER_RESEARCH_OPERATING_SYSTEM.md#110-planning-before-implementation) requires design before implementation (Cursor plans, Antigravity builds).

**Handbook References:** [Phase D9](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d9--preprocessing-workflow); [04_Preprocessing contract](MASTER_RESEARCH_OPERATING_SYSTEM.md#04_preprocessing); Preprocessing Agent ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)); [Checklist 4](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-4--preprocessing).

**Prerequisites:** STEP-024 (documented/validated raw dataset); STEP-023 (EDA revealing resolution/quality issues).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** No (design gates implementation).

**Inputs:** EDA + validation reports; `datasets.csv`; research question.

**Expected Outputs:** A preprocessing design doc + `module_spec.md` ([Template 17](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates)) per module; the parameter list that will live in the experiment `config.yaml` ([Phase M4](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-m4--configuration-system)).

**Repository Changes:**
- *New files:* `04_Preprocessing/specs/` module specs; design doc.

**Cursor Prompt:**
```
You are the Preprocessing Agent (design only; do NOT write code).
Using Phase D9 + EDA/validation findings + Template 17 ONLY:
1. Design each preprocessing step as an independent, testable, reusable module (image verification, face detection, alignment, crop, resize, normalization, quality filtering, artifact removal, format conversion, metadata extraction). No monolith.
2. For each module, write a module_spec.md (Inputs, Outputs, Parameters, Dependencies, Testing, Future Extensions) and its validation module.
3. List all parameters that must be recorded (to live in config.yaml / preprocessing_registry.csv), so processing is reproducible.
4. Define what "processed/DS0001_PP0001" outputs look like and the preprocessing_report.md contents.
Output specs for review. Reads raw READ-ONLY; writes only to processed/.
```

**Google Antigravity Prompt:** *None yet — implementation is STEP-026.*

**GitHub Expectations:** Branch `feature/preprocessing-design` → PR into `develop`. Commit `docs: design modular preprocessing pipeline specs`.

**Kaggle Expectations:** None.

**Documentation Updates:** Module specs; `04_Preprocessing/README.md`.

**Verification Checklist:**
- ✓ Each step is an independent module with a spec (no monolith).
- ✓ All parameters enumerated for recording.
- ✓ Validation modules specified.
- ✓ Raw is read-only in the design; outputs go to `processed/`.

**Common Mistakes:** Designing one big script; unrecorded parameters; coupling modules.

**Recovery Procedure:** Split any coupled/monolithic step into independent modules; add missing parameters to the record list.

**Definition of Done:** Modular design approved; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-026 — Implement preprocessing modules.

---

## STEP-026 — Implement Preprocessing Modules  **[A]**

**Title:** Build the packaged, testable preprocessing modules (Phase D9 — implementation).

**Objective:** Implement each designed module as importable Python with unit tests, reading raw read-only and writing to `processed/`.

**Why this step exists:** [Phase D9](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d9--preprocessing-workflow) + [§1.7 Software philosophy](MASTER_RESEARCH_OPERATING_SYSTEM.md#17-governing-philosophies): notebook logic becomes reusable packages; Antigravity implements the Cursor spec.

**Handbook References:** [Phase D9](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d9--preprocessing-workflow); [04_Preprocessing contract](MASTER_RESEARCH_OPERATING_SYSTEM.md#04_preprocessing); [A.2 Python naming](MASTER_RESEARCH_OPERATING_SYSTEM.md#a2-canonical-file-naming-rules).

**Prerequisites:** STEP-025 (approved specs).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1–2 days.
**Parallelizable:** Yes — independent modules.

**Inputs:** Module specs; raw dataset (read-only, on Kaggle).

**Expected Outputs:** Packaged preprocessing modules + unit tests in `04_Preprocessing/`.

**Repository Changes:**
- *New files:* Python package(s) under `04_Preprocessing/` + `tests/`.

**Cursor Prompt:**
```
You are reviewing (not writing) the implementation plan. Provide Antigravity with: the module specs, the coding standards (packaged importable modules, snake_case, type hints, docstrings, explicit error handling — no silent failures per §1.7), the test requirements (unit test per module), and the DoD. Then, after implementation, review the code for spec compliance and modularity. Do not write the code yourself.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the approved preprocessing modules as an importable Python package under 04_Preprocessing/, one module per preprocessing step, each:
- pure/parameterized (parameters passed in, never hardcoded),
- reading raw READ-ONLY, writing only to processed/,
- with explicit error handling (log + raise; never silently skip),
- with a unit test in tests/.
Coding standards: snake_case, type hints, docstrings, no monolith. 
Definition of Done: all modules implemented + unit-tested (tests pass), spec-compliant, raw untouched.
```

**GitHub Expectations:** Branch `feature/preprocessing-impl` → PR into `develop` (Cursor code review required). Commit `feat: implement modular preprocessing package with tests`.

**Kaggle Expectations:** None (build/test; execution in STEP-027).

**Documentation Updates:** Module docstrings; `04_Preprocessing/README.md`.

**Verification Checklist:**
- ✓ One packaged module per step; importable; no monolith.
- ✓ Unit tests pass; parameters injected (not hardcoded).
- ✓ Explicit error handling (no silent skips).
- ✓ Raw read-only; outputs to `processed/`.
- ✓ Cursor code review approved.

**Common Mistakes:** Hardcoded parameters; silent exception swallowing; writing into `raw/`; missing tests.

**Recovery Procedure:** If tests fail, fix and re-run; if a module writes to raw, correct the path. Ask Antigravity to add missing tests before merge.

**Definition of Done:** Modules implemented + tested + reviewed; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-027 — Register pipeline & generate processed dataset.

---

## STEP-027 — Register Pipeline & Generate Processed Dataset  **[C][A][K]**

**Title:** Assign `PPxxxx`, run on Kaggle, produce `DSxxxx_PPxxxx` (Phases D10–D11).

**Objective:** Register the pipeline in `preprocessing_registry.csv` (`Pipeline ID, Operations, Parameters, Dataset, Output, Purpose, Date, Research Question`), run it on Kaggle to generate `processed/DSxxxx_PPxxxx`, and write `preprocessing_report.md`.

**Why this step exists:** [Phase D10](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d10--preprocessing-versioning) + [D11](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d11--processed-dataset-generation): every pipeline is versioned; processed data is never overwritten.

**Handbook References:** [Phase D10](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d10--preprocessing-versioning); [Phase D11](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d11--processed-dataset-generation); [Template 6](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); [D19 Kaggle Data Workflow](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d19--kaggle-data-workflow); [A.6](MASTER_RESEARCH_OPERATING_SYSTEM.md#a6-canonical-storage--synchronization-policy).

**Prerequisites:** STEP-026 (tested modules), STEP-021 (raw on Kaggle).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day (compute-bound).
**Parallelizable:** Yes — multiple `PP` variants can be generated independently.

**Inputs:** Preprocessing package; raw Kaggle Dataset; parameters.

**Expected Outputs:** `preprocessing_registry.csv` row (`PPxxxx`); `processed/DSxxxx_PPxxxx` in the data tier (Kaggle); `preprocessing_report.md`.

**Repository Changes:**
- *Updated:* `preprocessing_registry.csv`.
- *New:* `preprocessing_report.md`; Kaggle pointer for the processed dataset. **No processed image bytes in Git.**

**Cursor Prompt:**
```
You are reviewing the Preprocessing + Registry agents.
Using Phase D10-D11 + Template 6 ONLY:
1. Draft the preprocessing_registry.csv row (PPxxxx: Operations, Parameters, Dataset=DSxxxx, Output=DSxxxx_PPxxxx, Purpose, Date, Research Question).
2. Specify the Kaggle notebook that runs the package to produce processed/DSxxxx_PPxxxx and emits preprocessing_report.md (Template 6), plus the pointer note to store in Git.
Enforce: never overwrite existing processed outputs; new params => new PP ID. Output for review.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the Kaggle notebook that runs the preprocessing package over raw/DSxxxx to produce processed/DSxxxx_PPxxxx (stored as a Kaggle Dataset output), and generates preprocessing_report.md. Save the registry row + Git pointer.
Constraints: never overwrite an existing processed output (new params => new PP ID); raw read-only; processed bytes stay in Kaggle (Git holds pointer + report only); strip notebook outputs before commit.
Definition of Done: PPxxxx registered; processed dataset produced on Kaggle; report + pointer synced to Git.
```

**Kaggle Expectations:** Notebook produces `processed/DSxxxx_PPxxxx` as a Kaggle Dataset output; report + pointer sync back to GitHub; processed images remain in Kaggle.

**GitHub Expectations:** Branch `dataset/preprocess-run` → PR into `develop`. Commit `dataset: register PPxxxx and generate processed DSxxxx_PPxxxx (pointer+report)`.

**Documentation Updates:** `preprocessing_registry.csv`; `preprocessing_report.md`.

**Verification Checklist:**
- ✓ `PPxxxx` registered with all parameters.
- ✓ `processed/DSxxxx_PPxxxx` exists in the data tier; not overwritten.
- ✓ `preprocessing_report.md` present (Template 6).
- ✓ Git holds pointer + report only.

**Common Mistakes:** Overwriting processed data; missing parameters in registry; committing processed images.

**Recovery Procedure:** If a processed output was overwritten, regenerate under a **new** `PP` ID (the prior one is immutable). Add any missing parameters to the registry row.

**Definition of Done:** Pipeline registered + processed data generated + reported; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-028 — Train/validation/test split.

---

## STEP-028 — Train/Validation/Test Split  **[C][A][K]**

**Title:** Leakage-safe, reproducible splitting (Phase D12 — leakage-critical).

**Objective:** Produce `DSxxxx_PPxxxx_SPLITxxxx` grouped by identity and (where relevant) generator so no identity/generator/duplicate spans train and test; record seed, algorithm, statistics in `split_report.md`.

**Why this step exists:** [Phase D12](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d12--trainvalidationtest-split-leakage-critical) prevents identity/duplicate/generator/future leakage — the most common invalidator of forensic results; enables [unseen-generator evaluation (E9)](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-e9--unseen-generator-evaluation-critical).

**Handbook References:** [Phase D12](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d12--trainvalidationtest-split-leakage-critical); [Glossary: Leakage](MASTER_RESEARCH_OPERATING_SYSTEM.md#appendix-d--glossary); Split Agent ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)); [Checklist 3](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-3--dataset-readiness).

**Prerequisites:** STEP-027 (processed dataset), STEP-023 (identity/generator distribution).

**Estimated Difficulty:** Hard.
**Estimated Time:** Half day.
**Parallelizable:** Yes — multiple split schemes (e.g. standard + leave-one-generator-out) can be produced.

**Inputs:** `processed/DSxxxx_PPxxxx`; identity/generator metadata.

**Expected Outputs:** Split index files `DSxxxx_PPxxxx_SPLITxxxx` (in `03_Datasets/splits/`, index/pointer form); `split_report.md` (seed, algorithm, statistics, leakage checks).

**Repository Changes:**
- *New files:* split index files (small, in Git), `reports/split_report.md`.

**Cursor Prompt:**
```
You are reviewing the Split Agent.
Using Phase D12 ONLY:
1. Specify a reusable, seeded splitting module that groups by identity AND (where relevant) by generator so the same identity/generator never spans train/test; also prevent duplicate + future leakage.
2. Define standard split (train/val/test) AND at least one leave-one-generator-out split to support E9.
3. Define split_report.md (seed, algorithm, per-split counts, class + generator balance, explicit leakage checks) and the split index file format (image IDs per split, not image bytes).
Output specs + validation (re-running with the same seed reproduces the split).
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the approved seeded splitting module + a Kaggle notebook to produce DSxxxx_PPxxxx_SPLITxxxx index files and split_report.md over processed/DSxxxx_PPxxxx.
Constraints: grouped by identity/generator (no leakage); deterministic given the seed; split indices reference image IDs (no image bytes in Git); include an automated leakage assertion (fail if any identity/generator crosses splits).
Definition of Done: split index files + report produced; leakage assertion passes; re-run with same seed reproduces identical splits.
```

**Kaggle Expectations:** Split notebook runs over the processed Kaggle Dataset; emits small index files + report synced to Git.

**GitHub Expectations:** Branch `dataset/split` → PR into `develop`. Commit `dataset: create leakage-safe split DSxxxx_PPxxxx_SPLITxxxx`.

**Documentation Updates:** `split_report.md`; split index files.

**Verification Checklist:**
- ✓ No identity/generator/duplicate spans train and test (automated assertion passes).
- ✓ Seed + algorithm + statistics recorded.
- ✓ Standard + leave-one-generator-out splits available (for E9).
- ✓ Re-running with the seed reproduces the split.
- ✓ Only index files in Git (no image bytes).

**Common Mistakes:** Random split ignoring identity (leakage); no seed; single split blocking E9; committing image data.

**Recovery Procedure:** If leakage is detected, discard the split (do not patch), fix grouping, regenerate under a new `SPLIT` ID. Never evaluate on a leaky split.

**Definition of Done:** Leakage-safe splits reproducible + reported; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-029 — FastAI prep, dataset versioning, master registry + Preprocessing Gate.

---

## STEP-029 — FastAI Prep, Version Control & Master Registry + Preprocessing Gate  **[C][A]**  **GATE (Checklist 4 + finalize Checklist 3)**

**Title:** Design FastAI `DataLoaders`, version the dataset, populate the master Dataset Registry, and gate.

**Objective:** Define the FastAI `DataBlock`/transforms parameters (into `config.yaml`, [Phase D13](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d13--fastai-dataset-preparation-design-only)); record `dataset_versions.csv` ([D14](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d14--dataset-version-control)); populate the master [Dataset Registry](MASTER_RESEARCH_OPERATING_SYSTEM.md#dataset-registry) `dataset_registry.csv` ([D15](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d15--dataset-registry-master-traceability)); set `datasets.csv Ready=yes`; pass [Checklist 4](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-4--preprocessing) and finalize [Checklist 3](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-3--dataset-readiness).

**Why this step exists:** [D13–D15](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d13--fastai-dataset-preparation-design-only) complete the dataset lifecycle: FastAI-ready parameters, versioning, and the master traceability spine linking dataset→version→PP→split→EXP→MODEL. The Preprocessing/Dataset gates must PASS before training.

**Handbook References:** [Phase D13](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d13--fastai-dataset-preparation-design-only); [D14](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d14--dataset-version-control); [D15 Dataset Registry](MASTER_RESEARCH_OPERATING_SYSTEM.md#dataset-registry); [Checklist 4](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-4--preprocessing); [Checklist 3](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-3--dataset-readiness); [§4.4 DoD](MASTER_RESEARCH_OPERATING_SYSTEM.md#44-dataset-definition-of-done).

**Prerequisites:** STEP-027 (PP), STEP-028 (splits).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** No — the master registry needs all prior IDs.

**Inputs:** `PPxxxx`, `SPLITxxxx`, EDA normalization stats.

**Expected Outputs:** FastAI `DataBlock` parameter spec (into experiment config); `dataset_versions.csv`; populated `dataset_registry.csv`; `datasets.csv Ready=yes`; `dataset_audit.md` = PASS; a preprocessing audit.

**Repository Changes:**
- *Updated:* `dataset_registry.csv`, `dataset_versions.csv`, `datasets.csv`.
- *New:* FastAI prep spec (in `05_Models`/config area or `04_Preprocessing/specs`); preprocessing audit.

**Cursor Prompt:**
```
You are reviewing the Registry + FastAI Configuration agents.
Using Phase D13-D15 + Checklists 3 & 4 ONLY:
1. Specify the FastAI DataBlock/DataLoaders design (blocks, get_items, splitter=our SPLIT, item/batch transforms, augmentations, normalization stats, image size, batch size) — as parameters destined for config.yaml (NOT hidden in code).
2. Draft dataset_versions.csv (v1.0) and the master dataset_registry.csv rows linking DSxxxx -> version -> PPxxxx -> SPLITxxxx (EXP/MODEL columns empty until training).
3. Run Checklist 4 (pipeline registered, params recorded, outputs documented, version assigned, raw untouched, processed reproducible, config stored) and finalize Checklist 3 (add split + no-leakage items). Emit updated dataset_audit.md + preprocessing audit (A.10). Set datasets.csv Ready=yes only if both PASS.
Output for human confirmation.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Save the approved FastAI prep spec, dataset_versions.csv, master dataset_registry.csv rows, updated audits, and set datasets.csv Ready=yes.
Constraints: FastAI params recorded as config (not code); master registry links DS->version->PP->SPLIT; append-or-update only; Ready=yes only after both gates PASS.
Definition of Done: master registry populated; versions recorded; gates PASS; Ready=yes.
```

**GitHub Expectations:** Branch `dataset/finalize` → PR into `develop`; **[H]** confirm Checklists 3 & 4 PASS. Commit `dataset: finalize FastAI prep, versioning, master registry; pass dataset+preprocessing gates`.

**Kaggle Expectations:** None (design/registry).

**Documentation Updates:** Registries; audits; FastAI prep spec.

**Verification Checklist (GATE — [Checklist 4](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-4--preprocessing) + finalize [Checklist 3](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-3--dataset-readiness)):**
- ✓ Pipeline registered; parameters recorded; processed reproducible; raw untouched.
- ✓ FastAI `DataBlock` parameters captured as config.
- ✓ `dataset_versions.csv` version assigned; `dataset_registry.csv` links DS→version→PP→SPLIT.
- ✓ No-leakage verified; split documented.
- ✓ `datasets.csv Ready=yes`; both audits PASS.

**Common Mistakes:** FastAI params hidden in notebook code; incomplete master registry; setting `Ready=yes` before gates pass.

**Recovery Procedure:** Move any code-embedded parameters into config; complete missing registry links; if a gate FAILS, fix and re-audit before training.

**Definition of Done:** Dataset FastAI-ready, versioned, master-registered; **Checklists 3 & 4 = PASS**; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied. Dataset + Preprocessing phases complete.

**Next Step:** STEP-030 — Environment definition & version lock (begins Environment & Model Foundation).

---
# PART 6 — ENVIRONMENT & MODEL FOUNDATION

> Implements [§10 Phase 16 Environment Management](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-16--environment-management), [§4 D19 Kaggle Data Workflow](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d19--kaggle-data-workflow), and [§5 Phases M1–M4](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system). This is the "Environment Setup" stage — the engineering hardening deferred from Part 1, done here just before training.

---

## STEP-030 — Environment Definition & Version Locking  **[C][A]**

**Title:** Pin the reproducible environment (Phase 16).

**Objective:** Populate `environment/` with `requirements.txt`, `environment.yml`, `kaggle-requirements.txt`, and `versions.lock.md` pinning Python/FastAI/PyTorch/CUDA, matched to the Kaggle GPU runtime.

**Why this step exists:** [§10 Phase 16](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-16--environment-management) + [Principle 1 (reproducibility)](MASTER_RESEARCH_OPERATING_SYSTEM.md#16-the-eight-operating-principles): training must be reproducible; Kaggle is the only execution environment, so dependencies must match its runtime.

**Handbook References:** [§10 Phase 16](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-16--environment-management); [§1.4 Stack](MASTER_RESEARCH_OPERATING_SYSTEM.md#14-fixed-technology-stack); [environment/ tree](MASTER_RESEARCH_OPERATING_SYSTEM.md#22-top-level-directory-tree); [§10.4 DoD](MASTER_RESEARCH_OPERATING_SYSTEM.md#104-infrastructure-definition-of-done).

**Prerequisites:** STEP-029 (dataset ready). STEP-002 (`environment/` skeleton).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** No — foundational for all training.

**Inputs:** Kaggle runtime versions (Python/CUDA/PyTorch); [§1.4](MASTER_RESEARCH_OPERATING_SYSTEM.md#14-fixed-technology-stack) stack (FastAI + PyTorch).

**Expected Outputs:** `environment/requirements.txt`, `environment.yml`, `kaggle-requirements.txt`, `versions.lock.md`.

**Repository Changes:**
- *Updated/new:* the four environment files.

**Cursor Prompt:**
```
You are reviewing the DevOps/Automation agent (environment).
Using §10 Phase 16 + §1.4 ONLY:
1. Specify the pinned dependency set for FastAI-first + PyTorch, matched to the CURRENT Kaggle GPU runtime (Python/CUDA/torch versions). Separate general requirements.txt/environment.yml from kaggle-requirements.txt (only what Kaggle lacks).
2. Draft versions.lock.md recording exact Python/FastAI/PyTorch/CUDA versions + Kaggle image reference + date.
3. Note that experiments must record the Git commit + these versions in config.yaml (M4).
Output the files for review. Do not add unpinned dependencies.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Save the approved environment/requirements.txt, environment.yml, kaggle-requirements.txt, and versions.lock.md.
Constraints: all dependencies pinned to exact versions; kaggle-requirements.txt contains only packages missing from the Kaggle base image; no secrets.
Definition of Done: environment files present and pinned; versions.lock.md complete.
```

**GitHub Expectations:** Branch `feature/environment-lock` → PR into `develop`. Commit `config: pin reproducible environment and lock versions`.

**Kaggle Expectations:** Versions must match the Kaggle GPU image; a smoke notebook may confirm `import fastai, torch` and CUDA availability.

**Documentation Updates:** `versions.lock.md`; `environment/README.md`.

**Verification Checklist:**
- ✓ All four environment files present; dependencies pinned.
- ✓ Versions match the Kaggle runtime (CUDA/torch/fastai).
- ✓ `versions.lock.md` records exact versions + date + Kaggle image.
- ✓ No unpinned/loose specs; no secrets.

**Common Mistakes:** Unpinned versions; mismatch with Kaggle runtime; bloated `kaggle-requirements.txt`.

**Recovery Procedure:** If a Kaggle import fails, align versions to the Kaggle image and re-lock; record the change in `versions.lock.md`.

**Definition of Done:** Environment pinned + Kaggle-verified; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-031 — Kaggle dataset upload & sync setup.

---

## STEP-031 — Kaggle Dataset Upload & Sync Setup  **[C][A][K]**

**Title:** Establish the Local↔GitHub↔Kaggle data + sync workflow (Phase D19, §10 Phase 7 prep).

**Objective:** Ensure raw + processed datasets are published as Kaggle Datasets, and implement the sync scripts (clone repo, download dataset/checkpoints, push metadata) so Kaggle sessions are reproducible and survivable.

**Why this step exists:** [§10 Phase 7](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-7--kaggle-training-workflow) + [D19](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d19--kaggle-data-workflow): Kaggle is the only training environment; the sync pattern must exist before the first experiment.

**Handbook References:** [Phase D19](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d19--kaggle-data-workflow); [§10 Phase 7](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-7--kaggle-training-workflow); [§10 Phase 10 Sync](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-10--synchronization-strategy); [§10 Phase 18 Automation](MASTER_RESEARCH_OPERATING_SYSTEM.md#10-github--kaggle--antigravity-workflow); [A.6](MASTER_RESEARCH_OPERATING_SYSTEM.md#a6-canonical-storage--synchronization-policy).

**Prerequisites:** STEP-021/027 (data on Kaggle), STEP-030 (environment).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** No.

**Inputs:** Kaggle Datasets (raw + processed); repo URL.

**Expected Outputs:** Sync scripts in `17_Automation/` (repo clone/pull, dataset download, artifact upload, metadata push); a documented Kaggle session template notebook.

**Repository Changes:**
- *New files:* `17_Automation/kaggle_sync/` scripts; a Kaggle session template under `06_Experiments/` conventions (empty template).

**Cursor Prompt:**
```
You are reviewing the Automation/DevOps agent.
Using §10 Phase 7, 10, 18 + D19 + A.6 ONLY:
1. Specify sync scripts (packaged in 17_Automation): git clone/pull the repo on Kaggle, install kaggle-requirements, attach raw+processed Kaggle Datasets, download checkpoints (artifact tier), and after training upload outputs + push metadata/registries back to GitHub.
2. Specify a Kaggle session template notebook implementing Phase 7 order: start -> clone -> verify env -> download dataset -> download checkpoints -> verify config -> (resume) train -> evaluate -> export -> upload -> push metadata -> shutdown.
3. Enforce A.6: only source-tier + pointers/metadata return to Git; weights/large data stay in artifact/data tiers.
Output specs. Never store secrets in the repo (use Kaggle secrets).
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the approved sync scripts in 17_Automation/kaggle_sync/ and the Kaggle session template notebook skeleton.
Constraints: no secrets committed (read Kaggle API token from Kaggle secrets/env); scripts idempotent; respect storage tiers (A.6). 
Definition of Done: sync scripts implemented; a dry-run on Kaggle clones the repo, attaches datasets, and confirms env — without leaking secrets.
```

**Kaggle Expectations:** Raw + processed Datasets exist and are attachable; a dry-run session confirms clone + dataset attach + environment.

**GitHub Expectations:** Branch `feature/kaggle-sync` → PR into `develop`. Commit `feat: add Kaggle sync automation and session template`.

**Documentation Updates:** `17_Automation/README.md`; session template notes.

**Verification Checklist:**
- ✓ Raw + processed Kaggle Datasets attachable.
- ✓ Sync scripts clone/pull repo, attach data, push metadata; idempotent.
- ✓ No secrets in repo (Kaggle secrets used).
- ✓ Storage tiers respected (weights/data never in Git).
- ✓ Session template follows [Phase 7](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-7--kaggle-training-workflow) order.

**Common Mistakes:** Committing Kaggle API tokens; pushing weights to Git; non-reproducible manual steps.

**Recovery Procedure:** If a token leaked, rotate it immediately and purge from history. If weights entered Git, move to Releases/Kaggle output. Convert manual steps into scripts ([Principle 7](MASTER_RESEARCH_OPERATING_SYSTEM.md#16-the-eight-operating-principles)).

**Definition of Done:** Kaggle sync operational + secret-safe; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-032 — Candidate model discovery.

---

## STEP-032 — Candidate Model Discovery  **[C][A][H]**

**Title:** Rank candidate architectures; human approves (Phase M1, DEF-002).

**Objective:** Produce `candidate_models.csv` (`Model ID, Architecture, Paper, Year, Conference, Parameters, Pretrained, FastAI Compatible, Input Size, Advantages, Weaknesses, Computation Cost, Research Relevance, Explainability Support, Generalization, Notes`); the AI ranks, the human approves which to baseline.

**Why this step exists:** [Phase M1](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-m1--candidate-model-discovery) + [DEF-002](MASTER_RESEARCH_OPERATING_SYSTEM.md#111-deferred-decisions): backbone choice is deferred until evidence exists; baselines proceed first.

**Handbook References:** [Phase M1](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-m1--candidate-model-discovery); [DEF-002](MASTER_RESEARCH_OPERATING_SYSTEM.md#111-deferred-decisions); Model Discovery Agent ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)); [§1.7 Model philosophy](MASTER_RESEARCH_OPERATING_SYSTEM.md#17-governing-philosophies).

**Prerequisites:** STEP-017 (literature: architectures seen), STEP-029 (dataset ready).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** Yes.

**Inputs:** `model_index.csv` (from literature), `papers.csv`, candidate sources (timm, FastAI, HF, official repos).

**Expected Outputs:** `05_Models/candidate_models.csv` scored + ranked; a shortlist for baselines (human-approved), keeping DEF-002 open.

**Repository Changes:**
- *Updated:* `candidate_models.csv`.

**Cursor Prompt:**
```
You are reviewing the Model Discovery Agent (rank; human approves).
Using Phase M1 + the literature model_index.csv ONLY:
1. Compile candidate FastAI-compatible architectures relevant to AI-generated face detection (from timm/FastAI/HF/official repos + our registered papers).
2. Draft candidate_models.csv rows with all columns; emphasize FastAI compatibility, explainability support (Grad-CAM etc.), generalization evidence, and compute cost (Kaggle-feasible).
3. Recommend a baseline shortlist with objective criteria; keep DEF-002 (final backbone) OPEN pending evaluation.
Stop for human approval of the shortlist. Do not finalize the backbone.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Save the approved candidate_models.csv rows.
Constraints: FastAI-compatible + Kaggle-feasible flagged; append-or-update only; no backbone finalized (DEF-002 stays open).
Definition of Done: candidate models recorded + ranked; baseline shortlist marked.
```

**GitHub Expectations:** Branch `research/model-discovery` → PR into `develop`. Commit `research: record candidate model architectures`.

**Kaggle Expectations:** None.

**Documentation Updates:** `candidate_models.csv`; `05_Models/README.md`.

**Verification Checklist:**
- ✓ Candidates scored on all M1 columns; FastAI-compatible flagged.
- ✓ Compute cost feasible on Kaggle.
- ✓ Human-approved baseline shortlist; DEF-002 remains open.
- ✓ Explainability + generalization considered.

**Common Mistakes:** Choosing a final backbone prematurely; ignoring compute limits; ignoring explainability support (needed for Module 10 / E13).

**Recovery Procedure:** Drop Kaggle-infeasible models; ensure at least one explainability-friendly backbone is shortlisted.

**Definition of Done:** Candidates ranked + shortlisted; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-033 — Baseline strategy & fairness invariants.

---

## STEP-033 — Baseline Strategy & Fairness Invariants  **[C]**

**Title:** Define fair baselines (Phase M2).

**Objective:** Produce `baseline_plan.md` defining the baseline experiment(s) and the fairness invariants (identical dataset version, split, `PP`, metrics, evaluation protocol) that all compared experiments must share.

**Why this step exists:** [Phase M2](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-m2--baseline-strategy): a baseline is a fair reference; unfair comparisons invalidate results and feed [Comparison Study (E16)](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-e16--comparison-study).

**Handbook References:** [Phase M2](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-m2--baseline-strategy); [Phase M13 Comparison](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-m13--model-comparison); [E16](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-e16--comparison-study).

**Prerequisites:** STEP-032 (shortlist), STEP-029 (dataset version/split).

**Estimated Difficulty:** Easy.
**Estimated Time:** 2–3 hours.
**Parallelizable:** No.

**Inputs:** Shortlist; dataset version/split IDs; metric set.

**Expected Outputs:** `05_Models/baseline_plan.md` with fairness invariants + the first baseline experiment definition.

**Repository Changes:**
- *New:* `05_Models/baseline_plan.md`.

**Cursor Prompt:**
```
You are reviewing the Baseline/Experiment agents.
Using Phase M2 ONLY: draft baseline_plan.md defining (a) the first baseline architecture from the shortlist, (b) the FAIRNESS INVARIANTS every compared experiment must hold constant (dataset version, SPLIT ID, PP ID, metrics, evaluation protocol, seed policy), and (c) which comparisons are valid vs. invalid. Tie this to E16 comparison requirements.
Output the plan for review.
```

**Google Antigravity Prompt:** *None — planning artifact.*

**GitHub Expectations:** Branch `research/baseline-plan` → PR into `develop`. Commit `research: define baseline strategy and fairness invariants`.

**Kaggle Expectations:** None.

**Documentation Updates:** `baseline_plan.md`.

**Verification Checklist:**
- ✓ Baseline architecture chosen from the shortlist.
- ✓ Fairness invariants explicit (dataset/split/PP/metrics/protocol/seed).
- ✓ Valid vs. invalid comparisons stated.

**Common Mistakes:** Comparing experiments with different splits/PP (unfair); undefined metric set.

**Recovery Procedure:** Any comparison that violates invariants is discarded ([E16](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-e16--comparison-study)); re-run under matched conditions.

**Definition of Done:** Baseline + fairness invariants defined; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-034 — Configuration system + FastAI training standard.

---

## STEP-034 — Configuration System & FastAI Training Standard  **[C][A]**

**Title:** Establish `config.yaml` as the single source of experiment truth (Phases M3–M4).

**Objective:** Finalize the `config.yaml` schema ([Phase M4](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-m4--configuration-system)) and the FastAI training standard ([Phase M3](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-m3--fastai-training-standard-design-not-code)) so nothing lives only in notebook code, and implement a config-validation module.

**Why this step exists:** [M4](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-m4--configuration-system): everything (dataset/split/model version, hyperparameters, seed, augmentations, hardware, Git commit, timestamp, research question) lives in config; [M3](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-m3--fastai-training-standard-design-not-code): design with FastAI.

**Handbook References:** [Phase M3](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-m3--fastai-training-standard-design-not-code); [Phase M4](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-m4--configuration-system); [Template 8 config.yaml](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); [Checklist 5](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-5--experiment-readiness).

**Prerequisites:** STEP-029 (FastAI prep params), STEP-033 (baseline).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** No.

**Inputs:** Template 8; FastAI prep spec; baseline plan.

**Expected Outputs:** Finalized `config.yaml` template + a config-validation module (checks required sections, ID references exist, seed set).

**Repository Changes:**
- *Updated:* `18_Templates/config.yaml` (if refined); *new:* `17_Automation/config_validation/` module.

**Cursor Prompt:**
```
You are reviewing the FastAI Configuration + Experiment agents.
Using Phase M3-M4 + Template 8 ONLY:
1. Finalize the config.yaml schema with ALL M4 sections (Experiment ID, Dataset Version, Split Version, Model Version, FastAI Settings, Image Size, Batch Size, Epochs, Optimizer, LR, Loss, Metrics, Random Seed, Augmentations, Hardware, Git Commit, Timestamp, Research Question, Purpose, Expected Outcome).
2. Describe the FastAI training standard (DataBlock->DataLoaders->Learner->callbacks->mixed precision->transfer learning->LR Finder->fit_one_cycle->unfreeze/fine-tune->export) as the reference workflow.
3. Spec a config-validation module that fails if any required field is missing, any referenced DS/PP/SPLIT/MODEL ID doesn't exist in its registry, or the seed is unset.
Output schema + module spec.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the config-validation module in 17_Automation (importable + unit-tested): validates a config.yaml against the M4 schema and checks that referenced DS/PP/SPLIT/MODEL IDs exist in their registries and that the seed is set. Refine the config.yaml template if approved.
Constraints: explicit failure messages (no silent pass); unit tests included.
Definition of Done: config validator works + tested; template finalized.
```

**GitHub Expectations:** Branch `feature/config-system` → PR into `develop`. Commit `feat: finalize config schema and config-validation module`.

**Kaggle Expectations:** None (used in every later training session).

**Documentation Updates:** Config template; validator README.

**Verification Checklist:**
- ✓ `config.yaml` schema has all [M4](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-m4--configuration-system) sections.
- ✓ FastAI training standard documented.
- ✓ Validator fails on missing fields/unknown IDs/unset seed; tests pass.
- ✓ Nothing critical lives only in notebook code.

**Common Mistakes:** Hyperparameters hidden in code; validator that passes silently; missing Git-commit/seed fields.

**Recovery Procedure:** Move any code-only setting into config; strengthen validator on any missed field.

**Definition of Done:** Config system + FastAI standard ready + validated; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-035 — Create the first experiment (begins Experiment/Training).

---
# PART 7 — EXPERIMENT SYSTEM · TRAINING PIPELINE · CHECKPOINT SYSTEM

> Implements [§5 Phases M5–M16](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system) and [§10 Phases 7–8](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-7--kaggle-training-workflow). Gated by [Checklist 5 (readiness)](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-5--experiment-readiness), [Checklist 6 (completion)](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-6--training-completion), [Checklist 7 (checkpoint integrity)](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-7--checkpoint-integrity). **This loop (STEP-035…041) is repeated for every experiment/ablation** with a new immutable `EXP` ID ([§5.1 M19](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system)).

---

## STEP-035 — Create the Experiment & Pass Readiness  **[C][A]**  **GATE (Checklist 5)**

**Title:** Create `EXP0001` folder + config and pass Experiment Readiness (Phase M5).

**Objective:** Create the dedicated experiment folder ([06_Experiments contract](MASTER_RESEARCH_OPERATING_SYSTEM.md#06_experiments)) with `config.yaml`, `experiment_readme.md`, and output subfolders; validate config; pass [Checklist 5](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-5--experiment-readiness) **before** training.

**Why this step exists:** [M5](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system): each experiment is isolated and never mixed; [Checklist 5](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-5--experiment-readiness) forbids launching training unprepared.

**Handbook References:** [Phase M5](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system); [06_Experiments](MASTER_RESEARCH_OPERATING_SYSTEM.md#06_experiments); [Template 7](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); [Checklist 5](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-5--experiment-readiness); [A.1 EXP IDs](MASTER_RESEARCH_OPERATING_SYSTEM.md#a1-canonical-identifier-scheme).

**Prerequisites:** STEP-034 (config system + validator), STEP-033 (baseline).

**Estimated Difficulty:** Easy.
**Estimated Time:** 2–3 hours.
**Parallelizable:** No (per experiment); repeated per new `EXP`.

**Inputs:** Baseline plan; dataset/split/model IDs; config template + validator.

**Expected Outputs:** `06_Experiments/EXP0001/` with `config.yaml`, `README.md` (experiment_readme), `logs/`, `metrics/`, `predictions/`, `learning_curves/`, `checkpoints_info.md`, `observations.md`, `notebook/`; config validation PASS; `experiment_registry.csv` row `Status=ready`.

**Repository Changes:**
- *New folder/files:* the `EXP0001/` structure.
- *Updated:* `experiment_registry.csv` (new `EXP` row).

**Cursor Prompt:**
```
You are reviewing the Experiment Agent.
Using Phase M5 + Template 7 + Checklist 5 ONLY:
1. Draft EXP0001/config.yaml (fully populated: dataset version, SPLIT, model version=baseline, FastAI settings, image/batch size, epochs, optimizer, LR policy, loss, metrics, seed, augmentations, hardware=Kaggle GPU, Git commit placeholder, timestamp, research question, purpose, expected outcome).
2. Draft experiment_readme.md (Template 7): research question, hypothesis, dataset, model, config summary, planned results, next experiment.
3. Run config-validation + Checklist 5 (dataset/split/config/seed/model version/experiment ID/hardware/checkpoint location/output folders/expected metrics/research question). Output PASS/FAIL.
Draft the experiment_registry.csv row (Status=ready). Do not launch training.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Create the EXP0001/ folder structure with the approved config.yaml + experiment_readme.md + empty output subfolders, run the config validator, and append the EXP0001 row to experiment_registry.csv (Status=ready).
Constraints: config immutable once training starts (M19/A.3) — a change means a new EXP ID; don't mix experiments; validator must PASS before proceeding.
Definition of Done: EXP0001 scaffold created; config validation PASS; registry row added.
```

**GitHub Expectations:** Branch `experiment/EXP0001` → PR into `develop`. Commit `experiment: create EXP0001 and pass readiness gate`.

**Kaggle Expectations:** None yet (launch is STEP-039).

**Documentation Updates:** `experiment_readme.md`; `experiment_registry.csv`.

**Verification Checklist (GATE — [Checklist 5](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-5--experiment-readiness)):**
- ✓ Dataset/split/model versions referenced + exist in registries.
- ✓ Config complete + validated; seed set; expected metrics stated.
- ✓ Experiment ID assigned; output folders + checkpoint location defined.
- ✓ Research question recorded; registry row `Status=ready`.

**Common Mistakes:** Missing seed; referencing a nonexistent split; editing config after launch (forbidden — new `EXP` instead).

**Recovery Procedure:** If validation FAILS, fix config and re-validate; never launch until PASS. If the config must change after launch, create a new `EXP` ID (the old is immutable).

**Definition of Done:** Experiment scaffolded; **Checklist 5 = PASS**; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-036 — Training pipeline package.

---

## STEP-036 — Implement the Training Pipeline Package  **[C][A]**

**Title:** Build the reusable FastAI training pipeline (Phase M6).

**Objective:** Implement a packaged, config-driven training pipeline: dataset validation → config validation → training → validation → checkpoint save → metric update → learning-curve data → model export → summary, with every step logged.

**Why this step exists:** [M6](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system) + [§1.7 Software philosophy](MASTER_RESEARCH_OPERATING_SYSTEM.md#17-governing-philosophies): training logic is a reusable package, not notebook code; Antigravity implements the Cursor design.

**Handbook References:** [Phase M6](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system); [Phase M3 FastAI standard](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-m3--fastai-training-standard-design-not-code); [Phase M15 Export](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system); [05_Models](MASTER_RESEARCH_OPERATING_SYSTEM.md#05_models).

**Prerequisites:** STEP-034 (config), STEP-035 (EXP0001), STEP-030 (env).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1–2 days.
**Parallelizable:** No (core dependency for training).

**Inputs:** FastAI standard; config schema; dataset loaders spec.

**Expected Outputs:** A packaged training pipeline in `05_Models/` (or `17_Automation/training/`) consuming `config.yaml`, callable from a Kaggle notebook; unit/smoke tests.

**Repository Changes:**
- *New files:* training package + tests; a thin `EXP0001/notebook/EXP0001_train.ipynb` that only calls the package with the config.

**Cursor Prompt:**
```
You are designing (not coding) the training pipeline for Antigravity.
Using Phase M6 + M3 + M15 ONLY, provide:
1. The pipeline architecture: config-driven functions for build_dataloaders (from DS/PP/SPLIT), build_learner (backbone from candidate_models), train (LR Finder + fit_one_cycle + unfreeze/fine-tune, mixed precision, callbacks), evaluate-on-val, save_checkpoints, export (export.pkl + weights.pth), write_metrics + learning_curves + summary. Everything parameterized by config.yaml. Every step logged (M11).
2. Coding standards (packaged, typed, docstrings, explicit errors — no silent failures), test requirements (smoke test on a tiny subset).
3. The rule that the Kaggle notebook is a THIN caller (no logic in the notebook).
Then review the delivered code for compliance.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the approved training pipeline as an importable package, config-driven end to end, using FastAI. Add a smoke test that trains 1 epoch on a tiny subset. Create EXP0001/notebook/EXP0001_train.ipynb as a THIN caller (load config -> run pipeline). 
Constraints: no logic in the notebook; parameters only from config.yaml; explicit error handling + logging; export.pkl + weights.pth produced; strip notebook outputs before commit (A.7).
Definition of Done: pipeline package implemented + smoke test passes; thin notebook created.
```

**GitHub Expectations:** Branch `feature/training-pipeline` → PR into `develop` (Cursor review). Commit `feat: implement config-driven FastAI training pipeline`.

**Kaggle Expectations:** Smoke test may run on Kaggle (tiny subset, 1 epoch) to confirm the pipeline executes end-to-end.

**Documentation Updates:** Pipeline README; `05_Models/README.md`.

**Verification Checklist:**
- ✓ Pipeline is packaged + config-driven; notebook is a thin caller.
- ✓ Produces checkpoints, metrics, learning-curve data, export.pkl + weights.pth.
- ✓ Every step logged; explicit error handling.
- ✓ Smoke test passes.

**Common Mistakes:** Logic in the notebook; hardcoded hyperparameters; missing export artifacts; silent failures.

**Recovery Procedure:** Move any notebook logic into the package; add missing exports; fix silent error paths. Re-run smoke test.

**Definition of Done:** Training pipeline implemented + smoke-tested; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-037 — Checkpoint system.

---

## STEP-037 — Implement the Checkpoint System  **[C][A]**

**Title:** Full-recoverability checkpointing (Phase M7 — critical).

**Objective:** Implement checkpointing that captures best model, last epoch, recovery checkpoint, and full training state (weights + optimizer + scheduler + epoch + random state + experiment state), with manifests + checksums in [07_Checkpoints](MASTER_RESEARCH_OPERATING_SYSTEM.md#07_checkpoints); **nothing ever overwritten**.

**Why this step exists:** [M7](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-7--checkpoint-management-critical): Kaggle sessions terminate; recovery must be guaranteed. Binaries live in the [artifact tier](MASTER_RESEARCH_OPERATING_SYSTEM.md#a6-canonical-storage--synchronization-policy).

**Handbook References:** [Phase M7](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-7--checkpoint-management-critical); [§10 Phase 8 Recovery](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-8--checkpoint-recovery); [07_Checkpoints](MASTER_RESEARCH_OPERATING_SYSTEM.md#07_checkpoints); [Checklist 7](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-7--checkpoint-integrity); [A.2 naming](MASTER_RESEARCH_OPERATING_SYSTEM.md#a2-canonical-file-naming-rules).

**Prerequisites:** STEP-036 (training pipeline).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1 day.
**Parallelizable:** No (safety-critical core).

**Inputs:** Training pipeline; artifact-tier target (Kaggle output / GitHub Releases).

**Expected Outputs:** Checkpoint save/load with manifests (`EXPxxxx_checkpoints.md` listing best/last/recovery + checksums + storage location); resume logic; `checkpoint_policy.md`.

**Repository Changes:**
- *New files:* `07_Checkpoints/checkpoint_policy.md`, `07_Checkpoints/EXP0001_checkpoints.md`; checkpoint module in the training package. **Binaries go to the artifact tier, not Git.**

**Cursor Prompt:**
```
You are designing the checkpoint system for Antigravity.
Using Phase M7 + §10 Phase 8 + Checklist 7 ONLY:
1. Specify save logic for best/last/recovery checkpoints capturing full training state (weights, optimizer, scheduler, epoch, random state, experiment state) at a defined frequency, plus FastAI export.pkl and weights.pth. NOTHING overwritten (versioned filenames per A.2: EXPxxxx_best.pth / EXPxxxx_last.pth / recovery).
2. Specify the checkpoint manifest (EXPxxxx_checkpoints.md): each checkpoint's path (artifact tier), checksum (sha256), epoch, metric, type.
3. Specify resume logic: detect latest valid recovery checkpoint (validate checksum), restore full state, continue training.
4. Draft checkpoint_policy.md (frequency, resume policy, failure recovery, early stopping, retention).
Then review Antigravity's implementation for "never overwrite" + checksum coverage.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the approved checkpoint module in the training package:
- save best/last/recovery with full training state + FastAI export; versioned filenames; write checksums.
- write/update EXPxxxx_checkpoints.md manifest.
- implement resume(): find latest valid checkpoint (verify checksum), restore full state.
Add checkpoint_policy.md. Add a test simulating interruption + resume.
Constraints: NEVER overwrite an existing checkpoint; binaries stored to artifact tier (Kaggle output / Release), Git holds manifest + checksums only.
Definition of Done: save/resume works; interruption-resume test passes; manifest + checksums correct; nothing overwritten.
```

**GitHub Expectations:** Branch `feature/checkpoint-system` → PR into `develop`. Commit `feat: implement recoverable checkpoint system with manifests`.

**Kaggle Expectations:** A test session simulates interruption and resumes from the recovery checkpoint successfully; binaries stored as Kaggle output.

**Documentation Updates:** `checkpoint_policy.md`; manifest.

**Verification Checklist (aligns with [Checklist 7](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-7--checkpoint-integrity)):**
- ✓ Best + last + recovery captured; full training state saved.
- ✓ Resume restores state + continues; interruption test passes.
- ✓ Manifest lists paths + checksums; checksums verify.
- ✓ Nothing overwritten; binaries in artifact tier only.

**Common Mistakes:** Overwriting checkpoints; saving weights only (no optimizer/scheduler/random state → non-resumable); binaries committed to Git; missing checksums.

**Recovery Procedure:** If resume fails, validate checksums and confirm full-state capture; if a checkpoint was overwritten, treat prior state as lost and document in a [failure report](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates) — then fix the code so it can never overwrite again.

**Definition of Done:** Recoverable checkpointing verified; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-038 — Logging system.

---

## STEP-038 — Implement the Logging System  **[C][A]**

**Title:** Persistent training/validation logging (Phase M11).

**Objective:** Implement logging of training/validation metrics, GPU usage, epoch summaries, learning curves, hyperparameters, timing, warnings, errors — so nothing important disappears when a Kaggle session ends.

**Why this step exists:** [M11](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system) + [Principle 6 (evidence)](MASTER_RESEARCH_OPERATING_SYSTEM.md#16-the-eight-operating-principles): logs are the evidence backing every result and every figure.

**Handbook References:** [Phase M11](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system); [Phase M16 Evaluation Trigger](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system); [A.2 log naming](MASTER_RESEARCH_OPERATING_SYSTEM.md#a2-canonical-file-naming-rules).

**Prerequisites:** STEP-036 (pipeline).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** Yes (with STEP-037 review).

**Inputs:** Training pipeline.

**Expected Outputs:** A logging module writing `EXPxxxx_<stage>.log` + metric/learning-curve CSVs into the experiment folder, synced to Git.

**Repository Changes:**
- *New files:* logging module; per-experiment logs + metric CSVs under `06_Experiments/EXP0001/logs|metrics|learning_curves/`.

**Cursor Prompt:**
```
You are designing the logging system for Antigravity.
Using Phase M11 ONLY, specify a logging module that records: per-epoch train/val metrics (CSV), GPU/memory usage, epoch timing, hyperparameters (echo of config), warnings + errors (explicit, never swallowed), and learning-curve data (for later figure specs). Define file naming (EXPxxxx_<stage>.log, metrics CSV schema). Ensure logs persist to the experiment folder and sync to Git (small CSVs) while binaries stay in artifact tier.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the approved logging module integrated into the training pipeline: writes EXPxxxx logs, metric CSVs, and learning-curve data to the experiment folder. Ensure errors/warnings are logged explicitly.
Constraints: deterministic CSV schemas; no silent exception handling; small CSVs to Git, no binaries.
Definition of Done: running the pipeline produces complete logs + metric/learning-curve CSVs; errors are captured.
```

**GitHub Expectations:** Branch `feature/logging-system` → PR into `develop`. Commit `feat: add persistent training logging and metric outputs`.

**Kaggle Expectations:** Logs produced during training sessions sync back to Git.

**Documentation Updates:** Logging README; metric CSV schema.

**Verification Checklist:**
- ✓ Per-epoch metrics, GPU usage, timing, hyperparameters logged.
- ✓ Warnings/errors captured explicitly (no silent failures).
- ✓ Learning-curve data produced for figure specs.
- ✓ Logs persist + sync (small CSVs; no binaries in Git).

**Common Mistakes:** Logs only in notebook output (lost on shutdown); swallowed exceptions; binaries in Git.

**Recovery Procedure:** Redirect logs to files in the experiment folder; ensure the Kaggle sync uploads them before shutdown.

**Definition of Done:** Logging persistent + complete; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-039 — Run the baseline on Kaggle (with checkpoint recovery verification).

---

## STEP-039 — Run the Baseline Experiment on Kaggle  **[C][K][A]**

**Title:** Execute training with full survivability + verify checkpoint recovery (Phases M8, §10 Phase 7–8).

**Objective:** Run `EXP0001` on Kaggle following the [Phase 7 order](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-7--kaggle-training-workflow), surviving time limits via resume, producing checkpoints/metrics/logs/exports, and verifying a mid-run resume works ([Phase 8](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-8--checkpoint-recovery), [Checklist 7](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-7--checkpoint-integrity)).

**Why this step exists:** [M8](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system) + [§10 Phase 7](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-7--kaggle-training-workflow): Kaggle is the only training environment; runs must survive interruptions.

**Handbook References:** [Phase M8](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system); [§10 Phase 7](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-7--kaggle-training-workflow); [§10 Phase 8](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-8--checkpoint-recovery); [§12 O5 Experiment Day](MASTER_RESEARCH_OPERATING_SYSTEM.md#12-daily-research-operating-workflow); [Checklist 7](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-7--checkpoint-integrity).

**Prerequisites:** STEP-036/037/038; STEP-031 (sync); STEP-035 (EXP ready).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1–2 days (training-bound; may span multiple Kaggle sessions).
**Parallelizable:** No per experiment (GPU-bound); different experiments can use separate sessions.

**Inputs:** EXP0001 config; datasets on Kaggle; sync scripts.

**Expected Outputs:** Trained model exports (artifact tier), checkpoints + manifest, metrics/logs/learning-curve data (Git), `observations.md`, and a verified resume.

**Repository Changes:**
- *Updated:* `EXP0001/{logs,metrics,learning_curves,predictions}`, `EXP0001_checkpoints.md`, `observations.md`, `experiment_registry.csv` (`Status=running→trained`). Exports + checkpoints to artifact tier.

**Cursor Prompt:**
```
You are the Training Coordinator (plan + monitor; do not run code yourself).
Using Phase M8 + §10 Phase 7-8 + O5 ONLY, produce the exact Kaggle session runbook for EXP0001:
1. Session order: start -> git pull -> verify repo/env -> attach datasets -> download checkpoints -> verify config (validator) -> resume-or-start train -> validate -> export -> upload outputs -> push metadata/registries -> shutdown.
2. A deliberate mid-run interruption + resume verification (Checklist 7): stop the session, restart, confirm resume from recovery checkpoint continues correctly.
3. What returns to Git (metrics/logs/manifests/small predictions) vs. artifact tier (weights/export). Monitoring checklist + observations.md prompts.
Output the runbook. Escalate any anomaly to the human.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY (session assets, not decisions). Finalize the EXP0001 Kaggle notebook as a thin caller executing the approved Phase-7 runbook end to end, including the resume path. Ensure post-training it uploads exports/checkpoints to the artifact tier and pushes metrics/logs/manifests/registry updates to GitHub.
Constraints: no logic beyond calling the pipeline; respect storage tiers; strip outputs before commit.
Definition of Done: notebook runs EXP0001 to completion with a verified resume; artifacts land in the correct tiers.
```

**Kaggle Expectations:** `EXP0001` trains to completion (possibly across sessions via resume); a deliberate interruption is recovered; exports + checkpoints saved as Kaggle output; metrics/logs synced to GitHub. **Data + weights remain in Kaggle/artifact tier.**

**GitHub Expectations:** Branch `experiment/EXP0001` (continued) → PR into `develop`. Commit `experiment: train EXP0001 baseline on Kaggle (metrics+logs+manifest)`.

**Documentation Updates:** `observations.md`; metrics/logs; checkpoint manifest; registry status.

**Verification Checklist:**
- ✓ Training completed; metrics/logs/learning-curve data present in Git.
- ✓ Checkpoints + exports in artifact tier; manifest + checksums updated.
- ✓ **Resume verified** (interruption → recovery → continued) — Checklist 7 PASS.
- ✓ `experiment_registry.csv` `Status=trained`.
- ✓ No data/weights committed to Git.

**Common Mistakes:** No resume test (fragile to time limits); logic in the notebook; committing weights; not syncing outputs before shutdown (lost work).

**Recovery Procedure:** If a session dies without a valid recovery checkpoint, investigate the checkpoint frequency (STEP-037) and document a [failure report](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); re-run from the last valid checkpoint. Never fake or reconstruct lost metrics.

**Definition of Done:** Baseline trained + recoverable + synced; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-040 — Register model & experiment + Training Completion Gate.

---

## STEP-040 — Register Model & Experiment + Training Completion Gate  **[C][A]**  **GATE (Checklist 6)**

**Title:** Populate Model & Experiment registries, model card, and pass Training Completion (Phases M9–M10, M14).

**Objective:** Register `MODEL0001` in [model_registry.csv](MASTER_RESEARCH_OPERATING_SYSTEM.md#model-registry) with `model_card.md`, complete the [experiment_registry.csv](MASTER_RESEARCH_OPERATING_SYSTEM.md#experiment-registry) row, write `conclusions.md` (or `failure_report.md` if it failed), and pass [Checklist 6](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-6--training-completion).

**Why this step exists:** [M9/M10](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system): every model + experiment is registered and traceable; [M14](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system): failed experiments are documented, never deleted.

**Handbook References:** [Phase M9 Model Registry](MASTER_RESEARCH_OPERATING_SYSTEM.md#model-registry); [Phase M10 Experiment Registry](MASTER_RESEARCH_OPERATING_SYSTEM.md#experiment-registry); [Phase M14 Failure Analysis](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system); [Template 22 Model Card](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); [Checklist 6](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-6--training-completion); [§10 Phase 13 Experiment Sync](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-13--experiment-synchronization).

**Prerequisites:** STEP-039 (trained).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** Yes (registry vs. card).

**Inputs:** EXP0001 outputs; checkpoint manifest; metrics.

**Expected Outputs:** `MODEL0001` row + `model_card.md`; completed `experiment_registry.csv` row; `conclusions.md`; updated `dataset_registry.csv` (EXP/MODEL links) and `claim_database.csv` (experimental support); `experiment_audit.md` = PASS.

**Repository Changes:**
- *Updated:* `model_registry.csv`, `experiment_registry.csv`, `dataset_registry.csv`, `claim_database.csv`; *new:* `05_Models/MODEL0001_model_card.md`, `EXP0001/conclusions.md`, `experiment_audit.md`.

**Cursor Prompt:**
```
You are reviewing the Registry + Failure Analysis agents.
Using Phase M9-M10 + M14 + Template 22 + Checklist 6 + Phase 13 ONLY:
1. Draft the model_registry.csv row for MODEL0001 (Experiment, Dataset, Split, Architecture, Training Time, GPU, Metrics, Checkpoint, Git Commit, Export Path, Deployment Ready, Research Notes, Publication Used) + model_card.md (Template 22).
2. Complete the experiment_registry.csv row (Results, Best Epoch, Training Time, Status=completed or failed, Failures, Reviewer Notes, Next Actions). If failed, draft failure_report.md instead of hiding it.
3. Update dataset_registry.csv to link DS->PP->SPLIT->EXP0001->MODEL0001, and add EXP0001 as Supporting Experiments to relevant claim_database.csv rows.
4. Run Checklist 6 (training finished, logs saved, metrics recorded, checkpoints exported, config archived, learning curves generated, summary written, registry updated, Git synced) -> experiment_audit.md.
Output for review.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Save the approved MODEL0001 row + model_card.md, complete the EXP0001 experiment_registry row, update dataset_registry + claim_database links, and save conclusions.md (or failure_report.md) + experiment_audit.md.
Constraints: never delete/modify prior metrics or configs (M19); append-or-update only; failed experiments documented, not removed.
Definition of Done: model + experiment registered; traceability links complete; Checklist 6 PASS.
```

**GitHub Expectations:** Branch `experiment/EXP0001` (finalize) → PR into `develop`. Commit `experiment: register MODEL0001 and complete EXP0001; pass training completion gate`.

**Kaggle Expectations:** None (registry work).

**Documentation Updates:** Registries; model card; conclusions/failure report; audit.

**Verification Checklist (GATE — [Checklist 6](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-6--training-completion)):**
- ✓ Training finished; logs + metrics + learning curves saved.
- ✓ Checkpoints exported; config archived; Git commit recorded.
- ✓ `MODEL0001` + `model_card.md` registered; `experiment_registry.csv` complete.
- ✓ Traceability links complete (DS→PP→SPLIT→EXP→MODEL); claim support updated.
- ✓ Failed experiments documented (not deleted); `experiment_audit.md` PASS.

**Common Mistakes:** Deleting a failed experiment; editing prior metrics; incomplete model card; missing traceability links.

**Recovery Procedure:** Restore any documentation for a failed run; never alter historical metrics ([M19](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system)). Complete missing registry links before proceeding.

**Definition of Done:** Model + experiment registered + traceable; **Checklist 6 = PASS**; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-041 — Evaluation trigger artifacts.

---

## STEP-041 — Prepare Evaluation Trigger Artifacts  **[C][A]**

**Title:** Auto-prepare all evaluation inputs on training completion (Phase M16).

**Objective:** Ensure training completion automatically produces all evaluation inputs: prediction files, metrics, confusion-matrix data, ROC data, PR data, calibration data, feature-importance data, attention maps, explainability inputs — the raw material for [Section 7](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol).

**Why this step exists:** [M16](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system): evaluation inputs are prepared at training time so figures/metrics can be produced later without re-running training.

**Handbook References:** [Phase M16](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system); [§7 E1–E2](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol); [A.9 Figure Policy](MASTER_RESEARCH_OPERATING_SYSTEM.md#a9-canonical-figure-policy).

**Prerequisites:** STEP-039 (trained model + exports), STEP-040 (registered).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** Yes.

**Inputs:** Trained `MODEL0001`; test split; export.pkl.

**Expected Outputs:** Prediction files + all evaluation-input CSVs in `EXP0001/predictions/` + `08_Evaluation/` staging; explainability input data (no rendered figures).

**Repository Changes:**
- *New files:* prediction + evaluation-input CSVs; explainability data.

**Cursor Prompt:**
```
You are reviewing the Evaluation Trigger Agent.
Using Phase M16 + E1-E2 + A.9 ONLY, specify a module that, given MODEL0001 + the test split, emits: predictions.csv (id, y_true, y_prob, y_pred), confusion data, ROC data, PR data, calibration data, feature-importance data, and explainability inputs (Grad-CAM/attention DATA only). Everything as data files for later figure specs. Reads exported model; no training.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the approved evaluation-trigger module + a Kaggle notebook that loads MODEL0001 export and the test split and produces all evaluation-input data files.
Constraints: DATA only (no rendered figures — A.9); deterministic; probability ranges valid [0,1]; store small CSVs to Git, large prediction dumps to artifact tier if big.
Definition of Done: all evaluation inputs generated + synced; ready for Section 7.
```

**Kaggle Expectations:** Inference notebook produces prediction + evaluation-input data over the test split; synced to Git.

**GitHub Expectations:** Branch `feature/eval-trigger` → PR into `develop`. Commit `feat: generate evaluation inputs for MODEL0001`.

**Documentation Updates:** Prediction schema; `08_Evaluation/README.md`.

**Verification Checklist:**
- ✓ Prediction file has ids + ground truth + probabilities + predictions.
- ✓ Confusion/ROC/PR/calibration/explainability data present.
- ✓ Data only (no rendered figures).
- ✓ Probabilities valid; deterministic.

**Common Mistakes:** Missing ground truth alignment; rendering figures; invalid probability ranges.

**Recovery Procedure:** Re-align predictions to ground truth by image ID; regenerate any missing data file. Do not render figures here.

**Definition of Done:** Evaluation inputs ready; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-042 — Evaluation preparation & prediction validation (begins Evaluation).

---
# PART 8 — EVALUATION PIPELINE

> Implements [§7 Evaluation Protocol, Phases E1–E18](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol). Produces the [Evaluation Registry](MASTER_RESEARCH_OPERATING_SYSTEM.md#evaluation-registry) and figure/table **specs** (never rendered figures — [A.9](MASTER_RESEARCH_OPERATING_SYSTEM.md#a9-canonical-figure-policy)). Ends with the **Evaluation Gate** ([Checklist 8](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-8--evaluation)). Each evaluation gets an immutable `EVAL` ID; **re-computing metrics after seeing results requires a new `EVAL` ID** ([§7.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#72-evaluation-principles-binding)).

---

## STEP-042 — Evaluation Preparation & Prediction Validation  **[C][A]**

**Title:** Reject incomplete experiments; validate predictions (Phases E1–E2).

**Objective:** Confirm the experiment is complete + registered (E1) and validate prediction/ground-truth counts, IDs, duplicates, class labels, probability ranges (E2), producing `prediction_validation_report.md`.

**Why this step exists:** [E1](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol) rejects incomplete experiments; [E2](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol) ensures predictions are trustworthy before any metric.

**Handbook References:** [Phase E1](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol); [Phase E2](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol); [08_Evaluation](MASTER_RESEARCH_OPERATING_SYSTEM.md#08_evaluation); Metric Agent ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)).

**Prerequisites:** STEP-041 (evaluation inputs).

**Estimated Difficulty:** Easy.
**Estimated Time:** 2–3 hours.
**Parallelizable:** No (prerequisite for all metrics).

**Inputs:** Prediction files; registries.

**Expected Outputs:** `08_Evaluation/EVAL0001/prediction_validation_report.md`; a new `EVAL0001` staging folder.

**Repository Changes:**
- *New:* `08_Evaluation/EVAL0001/` + validation report.

**Cursor Prompt:**
```
You are reviewing the Metric Agent (prep).
Using E1-E2 ONLY:
1. Verify EXP0001 is complete + registered: model exported, dataset+split registered, predictions+ground truth available, config+checkpoint archived, Git commit recorded. Reject if incomplete.
2. Specify prediction validation: counts match, image IDs align, no duplicate/missing predictions, valid class labels, probability ranges in [0,1], file integrity. Draft prediction_validation_report.md.
Assign EVAL0001. Output for review.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement a prediction-validation module (packaged + tested) and produce prediction_validation_report.md for EVAL0001.
Constraints: fail loudly on any mismatch; deterministic; no metric computation yet.
Definition of Done: validation report generated; all checks pass or issues listed.
```

**GitHub Expectations:** Branch `evaluation/EVAL0001` → PR into `develop`. Commit `evaluation: prepare EVAL0001 and validate predictions`.

**Kaggle Expectations:** May run on Kaggle if prediction files are large; report syncs to Git.

**Documentation Updates:** `prediction_validation_report.md`.

**Verification Checklist:**
- ✓ Experiment complete + registered (E1); incomplete ones rejected.
- ✓ Prediction counts/IDs/labels/probabilities validated.
- ✓ No duplicate/missing predictions.
- ✓ `EVAL0001` created.

**Common Mistakes:** Evaluating an incomplete experiment; misaligned IDs; ignoring invalid probabilities.

**Recovery Procedure:** If predictions are invalid, return to STEP-041; never compute metrics on unvalidated predictions.

**Definition of Done:** Predictions validated; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-043 — Classification metrics.

---

## STEP-043 — Classification Metrics  **[C][A]**

**Title:** Full metric suite — never accuracy alone (Phase E3).

**Objective:** Compute Accuracy, Precision, Recall, Specificity, Sensitivity, F1, Balanced Accuracy, MCC, ROC-AUC, PR-AUC, FPR, FNR, and macro/micro/weighted averages, each documented with interpretation and publication recommendation.

**Why this step exists:** [E3](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol): class imbalance is expected; accuracy alone is forbidden ([§7.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#72-evaluation-principles-binding)).

**Handbook References:** [Phase E3](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol); [§7.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#72-evaluation-principles-binding).

**Prerequisites:** STEP-042.

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** Yes (with STEP-044).

**Inputs:** Validated predictions.

**Expected Outputs:** Metric CSVs in `EVAL0001/`; a metrics section for the evaluation report.

**Repository Changes:**
- *New:* metric CSVs; metric-computation module (reusable).

**Cursor Prompt:**
```
You are reviewing the Metric Agent.
Using E3 + §7.2 ONLY, specify a reusable metrics module computing the full E3 suite from validated predictions, with per-metric documentation (when appropriate, how to interpret, common mistakes, publication recommendation). Forbid reporting accuracy alone. Output the CSV schema + module spec.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the metrics module (packaged + tested) and produce the E3 metric CSVs for EVAL0001.
Constraints: report full suite (never accuracy alone); deterministic; include class-imbalance-aware metrics (Balanced Accuracy, MCC, PR-AUC).
Definition of Done: metric CSVs produced; module tested.
```

**GitHub Expectations:** Branch `evaluation/EVAL0001` (cont.) → PR. Commit `evaluation: compute classification metrics for EVAL0001`.

**Kaggle Expectations:** Optional (small compute).

**Documentation Updates:** Metric CSVs; metric interpretation notes.

**Verification Checklist:**
- ✓ Full E3 suite computed (not accuracy alone).
- ✓ Imbalance-aware metrics included; averages reported.
- ✓ Each metric documented + deterministic.

**Common Mistakes:** Reporting accuracy alone; ignoring MCC/PR-AUC under imbalance.

**Recovery Procedure:** Add any missing metric; recompute deterministically. Never selectively report favorable metrics.

**Definition of Done:** Metrics complete + documented; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-044 — Calibration & threshold analysis.

---

## STEP-044 — Calibration & Threshold Analysis  **[C][A]**

**Title:** Calibration (E4) + threshold selection (E5).

**Objective:** Compute calibration curve, ECE, MCE, reliability diagram data, confidence distribution, Brier score (E4); perform threshold sweep + optimal-threshold selection + operating-point trade-offs (E5) — distinguishing probability vs. confidence vs. reliability.

**Why this step exists:** [E4](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-e4--calibration-analysis) feeds [Module 9 Confidence Estimation](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-9--confidence-estimation); softmax ≠ forensic certainty. [E5](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol) sets operating points.

**Handbook References:** [Phase E4](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-e4--calibration-analysis); [Phase E5](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol); [Module 9](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-9--confidence-estimation).

**Prerequisites:** STEP-043.

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** Yes.

**Inputs:** Validated predictions + probabilities.

**Expected Outputs:** Calibration + threshold data CSVs; calibration figure specs; recommended operating threshold(s).

**Repository Changes:**
- *New:* calibration/threshold CSVs; `FIGxxxx_spec.md` (calibration/reliability) in `09_Figures/specs/`.

**Cursor Prompt:**
```
You are reviewing the Calibration Agent.
Using E4 + E5 + Module 9 ONLY, specify: calibration curve, ECE, MCE, reliability diagram data, confidence distribution, Brier score; threshold sweep + optimal threshold (ROC/PR) + operating-point trade-offs + application-specific recommendation. Produce figure SPECS (Template 11) for calibration/reliability/threshold curves (data-only). Clarify probability vs confidence vs reliability for Module 9.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement calibration + threshold modules (packaged + tested); produce the data CSVs and save the figure specs. No rendered figures (A.9).
Definition of Done: calibration + threshold data produced; specs saved; deterministic.
```

**GitHub Expectations:** Branch `evaluation/EVAL0001` (cont.) → PR. Commit `evaluation: calibration and threshold analysis for EVAL0001`.

**Kaggle Expectations:** Optional.

**Documentation Updates:** Calibration/threshold CSVs + specs.

**Verification Checklist:**
- ✓ ECE/MCE/Brier + reliability data computed.
- ✓ Optimal threshold selected with trade-offs.
- ✓ Figure specs (data-only) saved; no rendered figures.
- ✓ Probability/confidence/reliability distinguished.

**Common Mistakes:** Treating softmax as confidence; rendering figures; no operating-point recommendation.

**Recovery Procedure:** Recompute calibration on validated probabilities; convert any rendered figure to a spec.

**Definition of Done:** Calibration + thresholds done; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-045 — Confusion & failure analysis.

---

## STEP-045 — Confusion & Failure Analysis  **[C][A]**

**Title:** Confusion matrix + qualitative failure categories (Phases E6, E12).

**Objective:** Produce confusion matrix + per-class stats + FP/FN case summaries (E6) and a `failure_analysis.md` categorizing failure modes (generator/identity confusion, compression, quality, background, lighting, occlusion, artifacts) with *possible causes*, never invented conclusions (E12).

**Why this step exists:** [E6](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol) + [E12](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol): understanding *how* the model fails is essential forensic evidence.

**Handbook References:** [Phase E6](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol); [Phase E12](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol).

**Prerequisites:** STEP-043.

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** Yes.

**Inputs:** Predictions; metadata (generator/identity where available).

**Expected Outputs:** Confusion data + `failure_analysis.md`; confusion-matrix figure spec.

**Repository Changes:**
- *New:* confusion CSVs; `08_Evaluation/EVAL0001/failure_analysis.md`; confusion figure spec.

**Cursor Prompt:**
```
You are reviewing the Failure Analysis Agent.
Using E6 + E12 ONLY, specify confusion matrix + per-class stats + FP/FN summaries and a failure_analysis.md categorizing failures (generator confusion, identity confusion, compression, poor quality, background, lighting, occlusion, artifacts). State POSSIBLE causes only (no invented conclusions). Add a confusion-matrix figure spec (data-only).
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Produce confusion data + failure_analysis.md + confusion figure spec.
Constraints: causes are hypotheses (never asserted); data-only figure spec; deterministic.
Definition of Done: confusion + failure analysis saved.
```

**GitHub Expectations:** Branch `evaluation/EVAL0001` (cont.) → PR. Commit `evaluation: confusion and failure analysis for EVAL0001`.

**Kaggle Expectations:** Optional.

**Documentation Updates:** Confusion CSVs; `failure_analysis.md`.

**Verification Checklist:**
- ✓ Confusion matrix + per-class stats computed.
- ✓ FP/FN cases summarized; failure categories identified.
- ✓ Causes stated as possibilities, not conclusions.

**Common Mistakes:** Asserting causes without evidence; ignoring generator-specific failures.

**Recovery Procedure:** Rephrase asserted causes as hypotheses; tie failures to metadata where possible.

**Definition of Done:** Confusion + failure analysis complete; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-046 — Robustness evaluation.

---

## STEP-046 — Robustness Evaluation  **[C][A][K]**

**Title:** Perturbation robustness (Phase E7).

**Objective:** Measure degradation under JPEG compression, Gaussian noise, blur, brightness/contrast, scaling, cropping, rotation, color perturbation, partial occlusion, low-quality uploads, resolution changes; report degradation, recovery, and failure patterns.

**Why this step exists:** [E7](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol): a forensic system must be robust to real-world upload conditions.

**Handbook References:** [Phase E7](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol); Robustness Agent ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)).

**Prerequisites:** STEP-043; trained model + test data on Kaggle.

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day–1 day (compute).
**Parallelizable:** Yes (per perturbation).

**Inputs:** `MODEL0001` export; test split; perturbation configs.

**Expected Outputs:** Robustness result CSVs + robustness curve figure spec.

**Repository Changes:**
- *New:* robustness module; result CSVs; robustness figure spec.

**Cursor Prompt:**
```
You are reviewing the Robustness Agent.
Using E7 ONLY, specify a robustness module that applies each perturbation at graded intensities to the test set, runs MODEL0001 inference, and records metric degradation + recovery + failure patterns per perturbation. Perturbations are CONFIG (extensible). Add a robustness-curve figure spec (data-only).
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the robustness module (packaged + tested) + Kaggle notebook; produce robustness result CSVs + figure spec.
Constraints: perturbations from config (not hardcoded); reuse preprocessing modules where possible; deterministic seeds; data-only specs.
Definition of Done: robustness results produced on Kaggle + synced; spec saved.
```

**Kaggle Expectations:** Robustness notebook runs perturbed inference over the test set; results sync to Git.

**GitHub Expectations:** Branch `evaluation/robustness` → PR into `develop`. Commit `evaluation: robustness evaluation for MODEL0001`.

**Documentation Updates:** Robustness CSVs + spec.

**Verification Checklist:**
- ✓ All E7 perturbations applied at graded intensities.
- ✓ Degradation/recovery/failure patterns recorded.
- ✓ Perturbations config-driven; deterministic.
- ✓ Robustness figure spec (data-only) saved.

**Common Mistakes:** Hardcoded perturbations; non-deterministic noise; rendering figures.

**Recovery Procedure:** Seed perturbations; move perturbation list to config; recompute.

**Definition of Done:** Robustness evaluated; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-047 — Generalization & unseen-generator evaluation.

---

## STEP-047 — Generalization & Unseen-Generator Evaluation  **[C][A][K]**

**Title:** Cross-dataset + leave-one-generator-out (Phases E8–E9, critical).

**Objective:** Evaluate on cross/external datasets + different distributions (E8) and perform leave-one-generator-out testing (E9) using the generator-held-out split from STEP-028; generators are configuration, not hardcoded.

**Why this step exists:** [E8](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol) forbids evaluating only on the training dataset; [E9 (critical)](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-e9--unseen-generator-evaluation-critical) tests real forensic generalization to unseen generators.

**Handbook References:** [Phase E8](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol); [Phase E9](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-e9--unseen-generator-evaluation-critical); Generalization Agent ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)); leakage-safe splits ([STEP-028](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-d12--trainvalidationtest-split-leakage-critical)).

**Prerequisites:** STEP-028 (generator-held-out split), STEP-043; possibly additional held-out datasets registered (repeat Part 4 for external data).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1 day+ (may require training a held-out model — iterate STEP-035…040).
**Parallelizable:** Yes (per held-out generator/dataset).

**Inputs:** External/held-out datasets; leave-one-generator-out splits; models.

**Expected Outputs:** Cross-dataset + unseen-generator result CSVs; generalization figure specs.

**Repository Changes:**
- *New:* generalization module; result CSVs; figure specs. New `EXP`/`MODEL` IDs if held-out models are trained.

**Cursor Prompt:**
```
You are reviewing the Generalization Agent.
Using E8 + E9 ONLY:
1. Specify cross-dataset evaluation on external/held-out datasets + different distributions/preprocessing.
2. Specify leave-one-generator-out: for each generator X, evaluate a model trained WITHOUT X on X (using the SPLITs from STEP-028; if a dedicated held-out model is needed, define a new EXP following STEP-035..040). Generators are CONFIG (extensible to StyleGAN family/SD/Midjourney/FLUX/DALL-E/future).
3. Add generalization figure specs (data-only).
Flag any required new experiments as separate EXP IDs.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the generalization module (packaged + tested) + Kaggle notebooks; produce cross-dataset + unseen-generator result CSVs + figure specs. If a held-out model is required, run it as a NEW EXP via the training pipeline.
Constraints: generators from config; no leakage between train and held-out generator; deterministic; data-only specs.
Definition of Done: generalization + unseen-generator results produced + synced.
```

**Kaggle Expectations:** Cross-dataset + held-out-generator inference (and any held-out training) run on Kaggle; results synced.

**GitHub Expectations:** Branch `evaluation/generalization` → PR into `develop`. Commit `evaluation: cross-dataset and unseen-generator evaluation`.

**Documentation Updates:** Generalization CSVs + specs; new experiment records if any.

**Verification Checklist:**
- ✓ Evaluated on ≥1 dataset beyond training (E8).
- ✓ Leave-one-generator-out performed; no generator leakage.
- ✓ Generators config-driven; extensible.
- ✓ Any held-out model has its own `EXP`/`MODEL` records.

**Common Mistakes:** Evaluating only on the training dataset; generator leakage; hardcoded generators.

**Recovery Procedure:** If leakage found, rebuild the held-out split (STEP-028) and re-run; never report leaky generalization numbers.

**Definition of Done:** Generalization + unseen-generator evaluated; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-048 — Ablation studies.

---

## STEP-048 — Ablation Studies  **[C][A][K]**

**Title:** Question-driven ablations (Phase E10).

**Objective:** Run systematic ablations (without augmentation, without transfer learning, different image sizes/preprocessing/loss/optimizer, different evidence modules/confidence/explainability), each answering one scientific question, as fairness-compatible experiments.

**Why this step exists:** [E10](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol): every design choice is justified by an ablation; each is a fair experiment ([M2](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-m2--baseline-strategy)).

**Handbook References:** [Phase E10](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol); [Phase M2 fairness](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-m2--baseline-strategy); Ablation Agent ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)).

**Prerequisites:** STEP-040 (baseline registered); fairness invariants (STEP-033).

**Estimated Difficulty:** Hard.
**Estimated Time:** Multiple days (each ablation = a new `EXP`; iterate STEP-035…041).
**Parallelizable:** Yes (independent ablations, GPU permitting).

**Inputs:** Baseline config; ablation questions.

**Expected Outputs:** One `EXP` per ablation + registered models; ablation comparison data + figure spec.

**Repository Changes:**
- *New:* ablation experiments (each a full EXP loop); ablation result CSVs + figure spec.

**Cursor Prompt:**
```
You are reviewing the Ablation Agent.
Using E10 + M2 ONLY:
1. Enumerate ablations, each with ONE scientific question and a config that changes exactly one factor vs. baseline (holding fairness invariants).
2. For each, define the EXP to run (via STEP-035..041) and the expected comparison.
3. Add an ablation-chart figure spec (data-only).
Output the ablation plan; each ablation is a NEW immutable EXP ID.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. For each approved ablation, create + run a new EXP (reusing the training pipeline + config), register the model/experiment, and collect the metric needed for comparison. Produce ablation result CSVs + figure spec.
Constraints: change exactly one factor per ablation; fairness invariants held; new EXP IDs; no editing of prior experiments.
Definition of Done: all planned ablations run + registered; ablation data produced.
```

**Kaggle Expectations:** Each ablation trains/evaluates on Kaggle as its own experiment.

**GitHub Expectations:** Branches `experiment/EXPxxxx` per ablation → PRs into `develop`. Commit `experiment: ablation EXPxxxx (<factor>)`.

**Documentation Updates:** Ablation experiment records; ablation CSVs + spec.

**Verification Checklist:**
- ✓ Each ablation answers one question; changes one factor.
- ✓ Fairness invariants held; each is a new `EXP`.
- ✓ Ablation comparison data + figure spec produced.

**Common Mistakes:** Changing multiple factors at once; comparing unfair experiments; editing the baseline.

**Recovery Procedure:** Split multi-factor ablations into separate `EXP`s; discard unfair comparisons.

**Definition of Done:** Ablations complete + fair + registered; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-049 — Statistical testing.

---

## STEP-049 — Statistical Testing  **[C][A]**

**Title:** No superiority claim without statistical evidence (Phase E11).

**Objective:** Compute confidence intervals, bootstrap, McNemar's test, paired comparisons, Wilcoxon, significance tests, variance/multi-seed analysis, and repeatability across the baseline + ablations.

**Why this step exists:** [E11](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol) + [§7.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#72-evaluation-principles-binding): superiority claims require statistical support.

**Handbook References:** [Phase E11](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol); Statistics Agent ([§11.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-agent-registry-by-domain)).

**Prerequisites:** STEP-043 (metrics), STEP-048 (comparisons); multi-seed runs (additional `EXP`s) as needed.

**Estimated Difficulty:** Hard.
**Estimated Time:** Half day–1 day.
**Parallelizable:** Yes.

**Inputs:** Per-experiment predictions + metrics; multi-seed runs.

**Expected Outputs:** Statistical test result CSVs + interpretation.

**Repository Changes:**
- *New:* statistics module; test result CSVs.

**Cursor Prompt:**
```
You are reviewing the Statistics Agent.
Using E11 ONLY, specify: bootstrap CIs for key metrics, McNemar's test for paired classifier comparisons, Wilcoxon/paired tests across seeds, variance + multi-seed analysis, repeatability. Define which comparisons require multi-seed runs (new EXP IDs) and the significance thresholds. Output the test plan + result schema.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the statistics module (packaged + tested); produce CI + significance test CSVs for the baseline vs ablations/comparisons. If multi-seed runs are required, run them as new EXPs.
Constraints: deterministic; report effect sizes + p-values + CIs; no superiority claim without a passing test.
Definition of Done: statistical results produced + interpreted.
```

**GitHub Expectations:** Branch `evaluation/statistics` → PR into `develop`. Commit `evaluation: statistical testing across experiments`.

**Kaggle Expectations:** Multi-seed runs on Kaggle if needed.

**Documentation Updates:** Statistics CSVs + interpretation.

**Verification Checklist:**
- ✓ CIs + significance tests computed for key comparisons.
- ✓ Multi-seed variance reported.
- ✓ No superiority claim lacks statistical support.

**Common Mistakes:** Claiming SOTA without tests; single-seed conclusions; p-hacking.

**Recovery Procedure:** Add multi-seed runs; withdraw unsupported superiority claims until tested.

**Definition of Done:** Statistical evidence complete; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-050 — Comparison study, figure/table specs, Evaluation Registry + Gate.

---

## STEP-050 — Comparison Study, Publication Specs & Evaluation Gate  **[C][A][H]**  **GATE (Checklist 8)**

**Title:** Comparison report + publication figure/table specs + Evaluation Registry, then gate (Phases E16–E18).

**Objective:** Produce `comparison_tables.csv` + `comparison_report.md` (fairness-compatible only, E16), the publication figure/table **specs** (E17), the [Evaluation Registry](MASTER_RESEARCH_OPERATING_SYSTEM.md#evaluation-registry) rows (E18), and pass [Checklist 8](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-8--evaluation).

**Why this step exists:** [E16–E18](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-e16--comparison-study) consolidate all evaluation into publication-ready specs + the registry; [§13.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#132-quality-gates) gates the Forensic Analyst phase on Checklist 8.

**Handbook References:** [Phase E16](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-e16--comparison-study); [Phase E17](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol); [Phase E18 Evaluation Registry](MASTER_RESEARCH_OPERATING_SYSTEM.md#evaluation-registry); [A.9 Figure Policy](MASTER_RESEARCH_OPERATING_SYSTEM.md#a9-canonical-figure-policy); [Templates 10/11/12](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); [Checklist 8](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-8--evaluation).

**Prerequisites:** STEP-043…049.

**Estimated Difficulty:** Hard.
**Estimated Time:** 1 day.
**Parallelizable:** Partially.

**Inputs:** All evaluation outputs.

**Expected Outputs:** `comparison_tables.csv` + `comparison_report.md`; `evaluation_report.md` (Template 10); publication `FIGxxxx_spec.md` (ROC/PR/calibration/confusion/metric-comparison/training/loss/threshold/robustness/ablation) + `TABxxxx_spec.md`; `evaluation_registry.csv` rows; `evaluation_audit.md` = PASS.

**Repository Changes:**
- *Updated:* `evaluation_registry.csv`; *new:* comparison + evaluation reports, figure/table specs, audit.

**Cursor Prompt:**
```
You are the Comparison + Reporting agents + Evaluation Auditor.
Using E16-E18 + A.9 + Templates 10/11/12 + Checklist 8 ONLY:
1. Draft comparison_tables.csv + comparison_report.md across fairness-compatible experiments ONLY (M2).
2. Draft evaluation_report.md (Template 10) consolidating metrics/calibration/robustness/generalization/ablation/statistics/failure analysis.
3. Draft the publication figure specs (ROC, PR, calibration, confusion, metric comparison, training curve, loss curve, threshold curve, robustness curve, ablation chart) as data-only specs, and table specs (Template 12).
4. Draft the evaluation_registry.csv rows (EVAL IDs) and run Checklist 8 -> evaluation_audit.md (A.10).
Output for human approval. No rendered figures.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Save the approved comparison_tables.csv, comparison_report.md, evaluation_report.md, all FIGxxxx/TABxxxx specs, evaluation_registry.csv rows, and evaluation_audit.md.
Constraints: only fairness-compatible comparisons; specs only (no rendered figures); append-or-update registries; each EVAL immutable.
Definition of Done: reports + specs + registry + audit saved; Checklist 8 PASS.
```

**GitHub Expectations:** Branch `evaluation/finalize` → PR into `develop`; **[H]** confirm Checklist 8 PASS; consider tagging `v0.5` (internal evaluation) per [§10 Phase 12](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-12--release-workflow). Commit `evaluation: comparison study, publication specs, registry; pass evaluation gate`.

**Kaggle Expectations:** None (consolidation).

**Documentation Updates:** Comparison + evaluation reports; figure/table specs; registry; audit.

**Verification Checklist (GATE — [Checklist 8](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-8--evaluation)):**
- ✓ Metrics complete; ROC/PR/confusion + calibration data present.
- ✓ Statistical testing, robustness, generalization, ablation, failure analysis complete.
- ✓ Comparison report (fairness-compatible only) done.
- ✓ Publication figure/table specs saved (data-only).
- ✓ `evaluation_registry.csv` populated; `evaluation_audit.md` PASS.

**Common Mistakes:** Unfair comparisons; rendering figures; recomputing metrics after seeing results without a new `EVAL` ID; SOTA claims without stats.

**Recovery Procedure:** If Checklist 8 FAILS, do not start the Forensic Analyst. Fix each item (missing test, unfair comparison, missing spec) and re-audit. Any post-hoc metric recomputation needs a new `EVAL` ID.

**Definition of Done:** Evaluation consolidated + publication-ready; **Checklist 8 = PASS**; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied. Evaluation phase complete.

**Next Step:** STEP-051 — Module registry & Forensic Analyst architecture (begins the primary contribution).

---
# PART 9 — AI FORENSIC ANALYST (THE PRIMARY CONTRIBUTION)

> Implements [§6 AI Forensic Analyst Architecture, Modules 1–19](MASTER_RESEARCH_OPERATING_SYSTEM.md#6-ai-forensic-analyst-architecture). This is the project's **primary scientific contribution** ([§1.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#12-project-identity)) — an evidence-driven system where the detector is one specialist that never decides. Source lives in [11_AI_Forensic_System](MASTER_RESEARCH_OPERATING_SYSTEM.md#11_ai_forensic_system). Ends with [E14](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-e14--ai-forensic-analyst-evaluation) + [Checklist 9](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-9--ai-forensic-analyst). Each module uses [Template 17 module_spec.md](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates) and registers in [module_registry.csv](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-17--system-registry).

---

## STEP-051 — Module Registry & System Architecture Specification  **[C]**

**Title:** Design the module architecture + populate the Module Registry (Module 17).

**Objective:** Produce a `module_spec.md` for every module (1–18), define the [pipeline](MASTER_RESEARCH_OPERATING_SYSTEM.md#62-pipeline) + interfaces (pluggable `EvidenceCollector`, pluggable fusion strategy), and populate [module_registry.csv](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-17--system-registry).

**Why this step exists:** [§6.1](MASTER_RESEARCH_OPERATING_SYSTEM.md#61-architectural-principles) + [Module 17](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-17--system-registry): loose coupling + defined interfaces + a registry are prerequisites to building any module; [§1.10](MASTER_RESEARCH_OPERATING_SYSTEM.md#110-planning-before-implementation) requires design first.

**Handbook References:** [§6.1](MASTER_RESEARCH_OPERATING_SYSTEM.md#61-architectural-principles); [§6.2 Pipeline](MASTER_RESEARCH_OPERATING_SYSTEM.md#62-pipeline); [Modules 1–18](MASTER_RESEARCH_OPERATING_SYSTEM.md#63-modules); [Module 17 registry](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-17--system-registry); [Template 17](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates).

**Prerequisites:** STEP-050 (Evaluation Gate PASS), STEP-040 (registered model).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1 day.
**Parallelizable:** No (architecture gates all module builds).

**Inputs:** §6 module descriptions; Model Registry (detector).

**Expected Outputs:** `module_spec.md` per module; interface definitions (`EvidenceCollector`, `FusionStrategy`); populated `module_registry.csv`; a system architecture doc.

**Repository Changes:**
- *New:* `11_AI_Forensic_System/specs/MODxxx_spec.md`; `module_registry.csv` rows; interface specs.

**Cursor Prompt:**
```
You are the Systems Architect for the AI Forensic Analyst. Do NOT write code.
Using §6 (Modules 1-18) + Template 17 + Module 17 ONLY:
1. Write a module_spec.md for EACH module (Purpose, Inputs, Outputs, Dependencies, Configuration, Testing, Future Extensions, Interfaces, Failure Handling).
2. Define the common interfaces: EvidenceCollector (so collectors are pluggable + independent — Module 3) and FusionStrategy (pluggable rule-based -> weighted -> Bayesian — Module 7 / DEF-004). Define the evidence object schema tied to the Evidence Registry (EV IDs).
3. Populate module_registry.csv (Module ID MODxxx, Responsibilities, Inputs, Outputs, Dependencies, Version, Status, Owner, Future Extensions).
4. Restate the invariants: the detector NEVER decides; the Decision Engine reads validated evidence ONLY (not the image); uncertainty never hidden; explanations never fabricated; future modalities supported by registering new collectors/strategies.
Output all specs for review.
```

**Google Antigravity Prompt:** *None yet — architecture/spec only. Implementation begins STEP-052.*

**GitHub Expectations:** Branch `feature/forensic-architecture` → PR into `develop`. Commit `docs: specify AI forensic analyst modules and interfaces`.

**Kaggle Expectations:** None.

**Documentation Updates:** Module specs; `module_registry.csv`; `11_AI_Forensic_System/README.md`.

**Verification Checklist:**
- ✓ Every module (1–18) has a `module_spec.md`.
- ✓ `EvidenceCollector` + `FusionStrategy` interfaces defined (pluggable).
- ✓ Evidence schema tied to `EV` IDs.
- ✓ `module_registry.csv` populated.
- ✓ Invariants explicit (detector never decides; decision reads evidence only).

**Common Mistakes:** Coupling modules; letting the detector decide; hardcoding one fusion strategy; no future-modality interface.

**Recovery Procedure:** Decouple any module that depends on another's internals; ensure the Decision Engine spec never references the raw image.

**Definition of Done:** Architecture + interfaces + registry specified; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-052 — Input management + image validation.

---

## STEP-052 — Input Management & Image Validation Modules  **[C][A]**

**Title:** Modules 1 & 2 — intake + validation.

**Objective:** Implement Input Management (receive uploads, validate format/size/resolution/corruption, generate `Input ID`, store metadata; output `input_metadata.json`) and the Image Validation Engine (integrity, format, corruption, channels, resolution, compression, noise, quality, face availability; structured failure on error).

**Why this step exists:** [Module 1](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-1--input-management) + [Module 2](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-2--image-validation-engine): the pipeline must never silently continue on bad input ([§1.7 error philosophy](MASTER_RESEARCH_OPERATING_SYSTEM.md#17-governing-philosophies)).

**Handbook References:** [Module 1](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-1--input-management); [Module 2](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-2--image-validation-engine); [Module 16 Failure Handling](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-16--failure-handling); [Template 17](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates).

**Prerequisites:** STEP-051 (specs).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day–1 day.
**Parallelizable:** Yes (Modules 1 & 2 are independent given the spec).

**Inputs:** Module 1 & 2 specs; interfaces.

**Expected Outputs:** Packaged modules + tests; `input_metadata.json` schema; structured failure reports for bad inputs.

**Repository Changes:**
- *New:* `11_AI_Forensic_System/input_management/`, `image_validation/` packages + tests.

**Cursor Prompt:**
```
You are reviewing Modules 1 & 2 for Antigravity (design compliance + review only).
Provide Antigravity: the Module 1 & 2 specs, the input_metadata.json schema, the InputID scheme, coding standards (packaged, typed, explicit failures via Module 16 — never silent), and unit-test requirements (valid + corrupted + unsupported + no-face inputs). Then review the implementation.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement Module 1 (Input Management) and Module 2 (Image Validation Engine) as packaged, tested modules in 11_AI_Forensic_System.
Requirements: generate Input IDs; write input_metadata.json; validate format/size/resolution/corruption/channels/compression/noise/quality/face availability; on failure produce a STRUCTURED failure report (Module 16) — never silently continue.
Constraints: no training/frontend code; unit tests for valid + corrupted + unsupported + no-face cases.
Definition of Done: both modules implemented + tested; failures structured.
```

**GitHub Expectations:** Branch `feature/forensic-input-validation` → PR into `develop`. Commit `feat: implement input management and image validation modules`.

**Kaggle Expectations:** None (runs in backend later).

**Documentation Updates:** Module docstrings; `input_metadata.json` schema.

**Verification Checklist:**
- ✓ Input IDs generated; `input_metadata.json` produced.
- ✓ Validation covers all Module 2 checks; face availability detected.
- ✓ Bad inputs produce structured failures (no silent continue).
- ✓ Unit tests for valid/corrupted/unsupported/no-face pass.

**Common Mistakes:** Silent acceptance of corrupted files; missing face-availability check; frontend logic leaking in.

**Recovery Procedure:** Add missing validation checks; ensure every failure path returns a structured report (Module 16).

**Definition of Done:** Modules 1 & 2 implemented + tested; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-053 — Evidence acquisition layer + collectors.

---

## STEP-053 — Evidence Acquisition Layer & Collectors  **[C][A]**

**Title:** Module 3 — independent, pluggable evidence collectors.

**Objective:** Implement the `EvidenceCollector` interface and the collectors: Image Statistics, Metadata, Face Detection, Face Quality, Frequency Domain, Compression Artifact, Color Distribution, Texture, Explainability Inputs — each independent, none depending on another.

**Why this step exists:** [Module 3](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-3--evidence-acquisition-layer): pluggable, mutually independent collectors enable future modalities without redesign ([Module 18](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-18--future-modality-support)).

**Handbook References:** [Module 3](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-3--evidence-acquisition-layer); [Module 18](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-18--future-modality-support); [Module 5 Evidence Registry](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-5--evidence-registry).

**Prerequisites:** STEP-052 (validated input).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1–2 days.
**Parallelizable:** Yes (each collector is independent).

**Inputs:** `EvidenceCollector` interface; validated input.

**Expected Outputs:** Packaged collectors + tests, each emitting evidence objects (typed) for the Evidence Registry.

**Repository Changes:**
- *New:* `11_AI_Forensic_System/evidence/collectors/` (one module per collector) + tests.

**Cursor Prompt:**
```
You are reviewing Module 3 for Antigravity.
Using Module 3 + the EvidenceCollector interface ONLY: provide the spec for each collector (Image Statistics, Metadata, Face Detection, Face Quality, Frequency Domain, Compression Artifact, Color Distribution, Texture, Explainability Inputs), the common evidence object schema (feeds EV IDs), the independence rule (no collector imports another), and test requirements. Deep Learning Prediction is a SEPARATE collector built in STEP-054. Review the implementation for independence + interface compliance.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement each evidence collector as an independent module implementing EvidenceCollector, returning a typed evidence object (type, source module, raw + processed output, quality, confidence). Add unit tests per collector.
Constraints: NO collector depends on another; register via the common interface; explicit failure handling; no decision logic.
Definition of Done: all collectors implemented + tested + independent + interface-compliant.
```

**GitHub Expectations:** Branch `feature/evidence-collectors` → PR into `develop`. Commit `feat: implement independent evidence collectors`.

**Kaggle Expectations:** None.

**Documentation Updates:** Collector specs/docstrings.

**Verification Checklist:**
- ✓ Each collector independent (no cross-imports); interface-compliant.
- ✓ Emits typed evidence objects for the registry.
- ✓ Explicit failure handling; unit tests pass.
- ✓ New collectors can be added without touching others.

**Common Mistakes:** Collectors depending on each other; decision logic inside a collector; untyped outputs.

**Recovery Procedure:** Decouple any dependent collector; move any decision logic out. Confirm a dummy new collector can register cleanly.

**Definition of Done:** Collectors implemented + independent + tested; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-054 — Deep Learning Specialist wrapper.

---

## STEP-054 — Deep Learning Specialist Wrapper  **[C][A]**

**Title:** Module 4 — the detector as one evidence source (inference only).

**Objective:** Wrap the exported FastAI model (from the [Model Registry](MASTER_RESEARCH_OPERATING_SYSTEM.md#model-registry)) as an `EvidenceCollector` performing inference only (probabilities, confidence, optional embeddings, metadata, execution time). It **never decides**; the model is swappable behind the interface.

**Why this step exists:** [Module 4](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-4--deep-learning-specialist) + [§1.7 Model philosophy](MASTER_RESEARCH_OPERATING_SYSTEM.md#17-governing-philosophies): the detector is one replaceable specialist supplying evidence, not the decision-maker.

**Handbook References:** [Module 4](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-4--deep-learning-specialist); [Model Registry](MASTER_RESEARCH_OPERATING_SYSTEM.md#model-registry); [§1.7](MASTER_RESEARCH_OPERATING_SYSTEM.md#17-governing-philosophies).

**Prerequisites:** STEP-051 (interface), STEP-040 (exported model), STEP-053 (collector layer).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** Yes.

**Inputs:** `export.pkl`; `EvidenceCollector` interface; Model Registry pointer.

**Expected Outputs:** DL specialist module + tests; evidence object with probabilities/confidence/embeddings/metadata.

**Repository Changes:**
- *New:* `11_AI_Forensic_System/evidence/collectors/deep_learning_specialist/` + tests.

**Cursor Prompt:**
```
You are reviewing Module 4 for Antigravity.
Using Module 4 + §1.7 + the EvidenceCollector interface ONLY: specify a wrapper that loads the exported FastAI model (path from model_registry.csv), performs inference only, and returns an evidence object (probabilities, confidence, optional embeddings, prediction metadata, execution time). The model is swappable behind the interface; the wrapper NEVER decides. Specify tests (including a swapped/mock model). Review for "inference only" + swappability.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the Deep Learning Specialist as an EvidenceCollector that loads the model by Model Registry pointer and returns inference evidence only.
Constraints: NO decision logic; model path from config/registry (not hardcoded); swappable behind the interface; unit test with a mock model to prove swappability.
Definition of Done: wrapper implemented + tested; produces inference evidence; model swappable.
```

**GitHub Expectations:** Branch `feature/dl-specialist` → PR into `develop`. Commit `feat: implement deep learning specialist evidence collector`.

**Kaggle Expectations:** None (inference in backend).

**Documentation Updates:** Module 4 spec/docstrings.

**Verification Checklist:**
- ✓ Loads model via registry pointer (not hardcoded).
- ✓ Returns inference evidence only; no decision logic.
- ✓ Model swappable (mock-model test passes).
- ✓ Execution time + metadata recorded.

**Common Mistakes:** Hardcoding the model path; letting the wrapper decide Real/Fake; non-swappable coupling.

**Recovery Procedure:** Move any decision logic to the Decision Engine (STEP-057); parameterize the model path.

**Definition of Done:** DL specialist implemented + swappable + tested; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-055 — Evidence Registry + validation.

---

## STEP-055 — Evidence Registry & Evidence Validation  **[C][A]**

**Title:** Modules 5 & 6 — record every evidence item; estimate reliability.

**Objective:** Implement the Evidence Registry (every item gets an `EVxxxxxx` ID, recorded in [evidence_registry.csv](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-5--evidence-registry)) and Evidence Validation (per-item reliability: low confidence, poor quality, face-detection failure, incomplete metadata, model uncertainty, conflicts).

**Why this step exists:** [Module 5](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-5--evidence-registry) makes evidence traceable; [Module 6](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-6--evidence-validation): evidence is never treated as uniformly reliable.

**Handbook References:** [Module 5](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-5--evidence-registry); [Module 6](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-6--evidence-validation); [A.1 EV IDs](MASTER_RESEARCH_OPERATING_SYSTEM.md#a1-canonical-identifier-scheme); [A.11](MASTER_RESEARCH_OPERATING_SYSTEM.md#a11-canonical-registry-format).

**Prerequisites:** STEP-053/054 (collectors produce evidence).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day–1 day.
**Parallelizable:** Yes.

**Inputs:** Evidence objects from collectors.

**Expected Outputs:** Evidence Registry writer (`EV` IDs) + validator; per-item reliability scores.

**Repository Changes:**
- *New:* `evidence/registry/` + `evidence/validation/` modules + tests; `evidence_registry.csv` populated at runtime.

**Cursor Prompt:**
```
You are reviewing Modules 5 & 6.
Using Module 5 (evidence_registry.csv columns: Evidence ID, Evidence Type, Source Module, Timestamp, Confidence, Description, Raw Output, Processed Output, Quality, Dependencies) + Module 6 ONLY: specify the registry writer (assign EVxxxxxx per item, append-only) and the validation module (reliability per item using low confidence, poor image quality, face-detection failure, incomplete metadata, model uncertainty, conflicting evidence). Specify tests (including conflicting evidence). Review for traceability + non-uniform reliability.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the Evidence Registry writer (EV IDs, append-only per A.11) and the Evidence Validation module (per-item reliability). Add tests including conflicting + low-quality evidence.
Constraints: every evidence item registered + traceable; reliability never uniform; explicit handling of conflicts.
Definition of Done: registry + validator implemented + tested; every item traceable.
```

**GitHub Expectations:** Branch `feature/evidence-registry-validation` → PR into `develop`. Commit `feat: implement evidence registry and validation`.

**Kaggle Expectations:** None.

**Documentation Updates:** Module 5/6 specs; registry schema.

**Verification Checklist:**
- ✓ Every evidence item gets an `EV` ID + registry row (append-only).
- ✓ Reliability scored per item (not uniform); conflicts handled.
- ✓ Traceability: each item → source module + dependencies.
- ✓ Tests (incl. conflicting/low-quality) pass.

**Common Mistakes:** Treating all evidence as equally reliable; overwriting registry rows; untraceable evidence.

**Recovery Procedure:** Add per-item reliability where missing; convert overwrite to append; ensure each item records its source.

**Definition of Done:** Evidence registered + validated + traceable; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-056 — Evidence fusion engine.

---

## STEP-056 — Evidence Fusion Engine  **[C][A]**

**Title:** Module 7 — the heart: pluggable fusion strategy.

**Objective:** Implement the `FusionStrategy` interface with a rule-based baseline (per [DEF-004](MASTER_RESEARCH_OPERATING_SYSTEM.md#111-deferred-decisions)), accepting evidence from unlimited future collectors; no single strategy hardcoded.

**Why this step exists:** [Module 7](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-7--evidence-fusion-engine): turns independent, validated evidence into one coherent conclusion via a swappable strategy (rule-based → weighted → Bayesian).

**Handbook References:** [Module 7](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-7--evidence-fusion-engine); [DEF-004](MASTER_RESEARCH_OPERATING_SYSTEM.md#111-deferred-decisions); [§6.1](MASTER_RESEARCH_OPERATING_SYSTEM.md#61-architectural-principles).

**Prerequisites:** STEP-055 (validated evidence).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1 day.
**Parallelizable:** No (central component).

**Inputs:** Validated evidence; `FusionStrategy` interface.

**Expected Outputs:** Fusion engine + rule-based strategy + tests; fused-evidence output for the Decision Engine.

**Repository Changes:**
- *New:* `11_AI_Forensic_System/fusion/` (engine + `strategies/rule_based.py`) + tests.

**Cursor Prompt:**
```
You are reviewing Module 7.
Using Module 7 + DEF-004 ONLY: specify the FusionStrategy interface and a rule-based baseline strategy that combines validated evidence (weighting by reliability), handles conflicts explicitly, and accepts an arbitrary set of evidence items (future collectors). Keep the strategy swappable (weighted/Bayesian later). Specify tests (conflicting evidence, missing evidence, single-source). Review for "no hardcoded strategy" + extensibility.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the fusion engine + a rule-based FusionStrategy behind the interface, consuming validated evidence and producing a fused result (with rationale referencing EV IDs). Add tests for conflicting/missing/single-source evidence.
Constraints: strategy swappable (no hardcoded fusion); accepts unlimited evidence types; explicit conflict handling; NO final Real/Fake decision here (that is Module 8).
Definition of Done: fusion engine + rule-based strategy implemented + tested + swappable.
```

**GitHub Expectations:** Branch `feature/fusion-engine` → PR into `develop`. Commit `feat: implement pluggable evidence fusion engine (rule-based baseline)`.

**Kaggle Expectations:** None.

**Documentation Updates:** Module 7 spec; fusion strategy docs; a [DEC/ADR](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates) noting rule-based-first (DEF-004).

**Verification Checklist:**
- ✓ `FusionStrategy` interface + rule-based strategy implemented.
- ✓ Accepts arbitrary evidence sets; conflicts handled.
- ✓ Strategy swappable (no hardcoding); rationale references `EV` IDs.
- ✓ Does not make the final decision.
- ✓ Tests pass.

**Common Mistakes:** Hardcoding fusion; the fusion engine emitting the final verdict; ignoring evidence reliability weights.

**Recovery Procedure:** Extract any hardcoded logic behind the interface; move final decision to Module 8.

**Definition of Done:** Fusion engine pluggable + tested; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-057 — Decision + confidence engine.

---

## STEP-057 — Decision & Confidence Engines  **[C][A]**

**Title:** Modules 8 & 9 — decide from validated evidence; separate confidence from softmax.

**Objective:** Implement the Decision Engine (reads validated/fused evidence only — never the image — outputs Real/Fake/Inconclusive/Unknown + reasoning path + `decision.json`) and Confidence Estimation (Prediction/Evidence/System/Decision confidence, distinct from raw softmax).

**Why this step exists:** [Module 8](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-8--decision-engine): the decision is evidence-based, not model-based; [Module 9](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-9--confidence-estimation): softmax ≠ forensic certainty (informed by [E4 calibration](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-e4--calibration-analysis)).

**Handbook References:** [Module 8](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-8--decision-engine); [Module 9](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-9--confidence-estimation); [Phase E4](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-e4--calibration-analysis).

**Prerequisites:** STEP-056 (fused evidence); STEP-044 (calibration data).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1 day.
**Parallelizable:** Yes (decision vs. confidence, given schemas).

**Inputs:** Fused validated evidence; calibration outputs.

**Expected Outputs:** Decision + confidence modules + tests; `decision.json`.

**Repository Changes:**
- *New:* `11_AI_Forensic_System/decision/`, `confidence/` modules + tests.

**Cursor Prompt:**
```
You are reviewing Modules 8 & 9.
Using Module 8 + Module 9 + E4 ONLY:
1. Specify the Decision Engine: input = validated/fused evidence ONLY (never the image); output = Real/Fake/Inconclusive/Unknown + reasoning path + decision metadata (decision.json). Define when "Inconclusive"/"Unknown" apply.
2. Specify Confidence Estimation: Prediction confidence, Evidence confidence, System confidence, Decision confidence — each with a documented interpretation; incorporate calibration (E4) so confidence != raw softmax.
Specify tests (conflicting evidence -> Inconclusive; missing model -> Unknown). Review for "evidence-only decision".
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the Decision Engine (reads validated evidence only; emits decision.json with Real/Fake/Inconclusive/Unknown + reasoning path) and the Confidence module (four confidence types, calibrated, documented). Add tests including Inconclusive + Unknown paths.
Constraints: Decision Engine NEVER accesses the raw image; confidence separated from softmax; uncertainty never hidden.
Definition of Done: decision + confidence implemented + tested; decision.json schema honored.
```

**GitHub Expectations:** Branch `feature/decision-confidence` → PR into `develop`. Commit `feat: implement decision and confidence engines`.

**Kaggle Expectations:** None.

**Documentation Updates:** Modules 8/9 specs; `decision.json` schema.

**Verification Checklist:**
- ✓ Decision reads validated evidence only (never the image).
- ✓ Outputs Real/Fake/Inconclusive/Unknown + reasoning path.
- ✓ Four confidence types, calibrated + documented.
- ✓ Uncertainty surfaced (Inconclusive/Unknown paths tested).

**Common Mistakes:** Decision reading the image or raw softmax; hiding uncertainty; conflating confidence with probability.

**Recovery Procedure:** Remove any image/softmax access from the decision; ensure Inconclusive/Unknown are reachable and tested.

**Definition of Done:** Decision + confidence implemented + tested; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-058 — Explainability + reasoning engine.

---

## STEP-058 — Explainability & Forensic Reasoning Engines  **[C][A]**

**Title:** Modules 10 & 11 — explanation data + human-readable reasoning.

**Objective:** Implement the Explainability Engine (Grad-CAM/attention/saliency/integrated-gradients interfaces → `explanation.json`, data only, no rendered images) and the Forensic Reasoning Engine (human-readable reasoning derived strictly from collected evidence — never invented).

**Why this step exists:** [Module 10](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-10--explainability-engine) + [Module 11](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-11--forensic-reasoning-engine): explanations must be evidence-derived and figure-policy-compliant.

**Handbook References:** [Module 10](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-10--explainability-engine); [Module 11](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-11--forensic-reasoning-engine); [A.9 Figure Policy](MASTER_RESEARCH_OPERATING_SYSTEM.md#a9-canonical-figure-policy); [E13 Explainability Eval](MASTER_RESEARCH_OPERATING_SYSTEM.md#7-evaluation-protocol).

**Prerequisites:** STEP-057 (decision), STEP-053 (explainability inputs).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1 day.
**Parallelizable:** Yes.

**Inputs:** Explainability input data; decision + evidence.

**Expected Outputs:** Explainability + reasoning modules + tests; `explanation.json` (data only).

**Repository Changes:**
- *New:* `11_AI_Forensic_System/explainability/`, `reasoning/` modules + tests.

**Cursor Prompt:**
```
You are reviewing Modules 10 & 11.
Using Module 10 + Module 11 + A.9 ONLY:
1. Specify the Explainability Engine interfaces (Grad-CAM, attention maps, saliency, integrated gradients) producing explanation.json DATA ONLY (no rendered images).
2. Specify the Forensic Reasoning Engine that composes human-readable reasoning strictly from collected evidence + decision (e.g. "face detected; frequency artifacts present; prediction confidence high -> evidence supports AI-generated origin"). It must NEVER invent explanations.
Specify tests (reasoning cites only present evidence). Review for evidence-grounding + no rendered figures.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the Explainability Engine (data-only explanation.json) and Forensic Reasoning Engine (evidence-derived narrative referencing EV IDs). Add tests proving reasoning only references present evidence and no image is rendered.
Constraints: no rendered figures (A.9 — data only); reasoning never invents; explanation traceable to evidence.
Definition of Done: both modules implemented + tested; explanations evidence-grounded + data-only.
```

**GitHub Expectations:** Branch `feature/explainability-reasoning` → PR into `develop`. Commit `feat: implement explainability and forensic reasoning engines`.

**Kaggle Expectations:** None.

**Documentation Updates:** Modules 10/11 specs; `explanation.json` schema.

**Verification Checklist:**
- ✓ Explanation is data only (no rendered images).
- ✓ Reasoning derived strictly from present evidence (references `EV` IDs).
- ✓ No invented explanations; tests confirm grounding.

**Common Mistakes:** Rendering explanation images (violates A.9); reasoning that asserts beyond the evidence.

**Recovery Procedure:** Convert rendered outputs to data; strip any ungrounded reasoning.

**Definition of Done:** Explainability + reasoning implemented + grounded; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-059 — Report generator, audit, failure handling + Forensic Gate.

---

## STEP-059 — Report Generator, Audit Trail, Failure Handling + Forensic Gate  **[C][A][H]**  **GATE (Checklist 9 + E14)**

**Title:** Modules 12/15/16 — reproducible reports, case audit, robust failures; evaluate the whole platform.

**Objective:** Implement the Report Generator (JSON/Markdown/HTML via [Template 24](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates), including system/model/dataset/experiment versions + Git commit), the Audit Trail (every investigation → [case_registry.csv](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-15--audit-trail)), and Failure Handling (Module 16); then run [E14](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-e14--ai-forensic-analyst-evaluation) + [Checklist 9](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-9--ai-forensic-analyst).

**Why this step exists:** [Module 12](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-12--report-generator)/[15](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-15--audit-trail)/[16](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-16--failure-handling) complete the platform; [E14](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-e14--ai-forensic-analyst-evaluation) evaluates the *whole system*, gating the web phase.

**Handbook References:** [Module 12](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-12--report-generator); [Module 15](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-15--audit-trail); [Module 16](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-16--failure-handling); [Phase E14](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-e14--ai-forensic-analyst-evaluation); [Checklist 9](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-9--ai-forensic-analyst); [Template 24](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); [§6.4 DoD](MASTER_RESEARCH_OPERATING_SYSTEM.md#64-forensic-analyst-definition-of-done).

**Prerequisites:** STEP-052…058 (all prior modules).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1–2 days.
**Parallelizable:** Partially (report vs. audit vs. failure handling).

**Inputs:** Decision, confidence, evidence, explanation, reasoning outputs.

**Expected Outputs:** Report generator + audit + failure-handling modules + tests; end-to-end pipeline test (image → report); `case_registry.csv` writer; E14 evaluation + `Checklist 9` audit = PASS.

**Repository Changes:**
- *New:* `reports/`, `audit/`, `failure_handling/` modules + tests; end-to-end pipeline entrypoint; `08_Evaluation/forensic_analyst_eval/` (E14); forensic audit report.

**Cursor Prompt:**
```
You are reviewing Modules 12/15/16 + running the Forensic Analyst evaluation (E14) + Checklist 9.
Using Module 12/15/16 + Template 24 + E14 + Checklist 9 ONLY:
1. Specify the Report Generator (JSON/Markdown/HTML from Template 24): Case ID, input summary, evidence summary, model results, confidence, explanation, decision, limitations, recommendations, execution stats, and System/Model/Dataset/Experiment versions + Git commit (reproducibility).
2. Specify the Audit Trail writing case_registry.csv per investigation, and Module 16 failure handling (no face, multiple faces, corrupted, unsupported, model unavailable, low confidence, timeout, unexpected) — each -> structured report, never silent.
3. Specify an END-TO-END pipeline test (image -> evidence -> validation -> fusion -> decision -> confidence -> explanation -> report).
4. Specify E14 evaluation (evidence completeness, fusion quality, decision consistency, confidence consistency, report quality, reasoning quality, execution time, module failures, recovery) and run Checklist 9 -> forensic audit (A.10).
Output for human approval.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the Report Generator (Template 24, with version+Git-commit provenance), the Audit Trail (case_registry.csv writer, CASE IDs), and Failure Handling (Module 16, structured reports for all listed failure modes). Wire the end-to-end pipeline entrypoint and add an end-to-end test. Produce the E14 evaluation outputs.
Constraints: reports reproducible (include all versions + Git commit); every failure structured (never silent); CASE IDs append-only.
Definition of Done: report+audit+failure modules implemented + tested; end-to-end test passes; E14 outputs produced.
```

**GitHub Expectations:** Branch `feature/report-audit-failure` → PR into `develop`; **[H]** confirm Checklist 9 PASS. Commit `feat: implement report generator, audit trail, failure handling; pass forensic analyst gate`.

**Kaggle Expectations:** None (E14 runs the assembled system; heavy inference can use Kaggle if needed).

**Documentation Updates:** Modules 12/15/16 specs; `case_registry.csv`; E14 report; forensic audit.

**Verification Checklist (GATE — [Checklist 9](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-9--ai-forensic-analyst)):**
- ✓ Evidence collection, validation, fusion, decision, confidence, explanation, report generation all functional.
- ✓ End-to-end pipeline (image → report) passes.
- ✓ Reports reproducible (versions + Git commit embedded).
- ✓ Audit trail writes `case_registry.csv`; failure handling structured for all modes.
- ✓ E14 evaluation done; forensic audit = PASS.

**Common Mistakes:** Reports missing version/Git provenance; silent failures; the detector's probability leaking out as the "decision"; skipping E14.

**Recovery Procedure:** If Checklist 9 FAILS, do not start backend. Fix each failing module, re-run the end-to-end test + E14, re-audit. Ensure every report is regenerable from recorded versions.

**Definition of Done:** Forensic Analyst complete + evaluated; **Checklist 9 + E14 = PASS**; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) + [§6.4 DoD](MASTER_RESEARCH_OPERATING_SYSTEM.md#64-forensic-analyst-definition-of-done) satisfied. Primary contribution complete.

**Next Step:** STEP-060 — Backend architecture & API spec (begins Backend).

---
# PART 10 — BACKEND DEVELOPMENT

> Implements [§8.4–§8.5 Backend + REST API contract](MASTER_RESEARCH_OPERATING_SYSTEM.md#84-backend-architecture-django--drf). Django + DRF ([13_Backend](MASTER_RESEARCH_OPERATING_SYSTEM.md#13_backend)). **The backend owns the investigation** ([§8.1](MASTER_RESEARCH_OPERATING_SYSTEM.md#81-separation-of-concerns-binding)). Ends with [Checklist 11](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-11--backend).

---

## STEP-060 — Backend Architecture & API Specification  **[C]**

**Title:** Design the Django/DRF apps + the canonical REST contract (§8.4–§8.5).

**Objective:** Produce the backend architecture (apps: `api`, `forensic_engine`, `evidence`, `reports`, `core`, `health`, `versioning`) and the `api_spec.md` for the canonical endpoints via [Template 16](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates).

**Why this step exists:** [§8.4/§8.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#84-backend-architecture-django--drf) + [§1.10](MASTER_RESEARCH_OPERATING_SYSTEM.md#110-planning-before-implementation): the API contract + app boundaries are designed before implementation.

**Handbook References:** [§8.1](MASTER_RESEARCH_OPERATING_SYSTEM.md#81-separation-of-concerns-binding); [§8.4](MASTER_RESEARCH_OPERATING_SYSTEM.md#84-backend-architecture-django--drf); [§8.5 API Contract](MASTER_RESEARCH_OPERATING_SYSTEM.md#django-rest-api-contract); [Template 16](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); [Module 13 API Layer](MASTER_RESEARCH_OPERATING_SYSTEM.md#6-ai-forensic-analyst-architecture).

**Prerequisites:** STEP-059 (Forensic Analyst gate PASS).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** No (gates backend build).

**Inputs:** Forensic Analyst entrypoint; API contract table.

**Expected Outputs:** Backend architecture doc; `13_Backend/api_spec/api_spec.md` (all endpoints); error-handling + config + security plan (§8.7–§8.9).

**Repository Changes:**
- *New:* architecture doc + `api_spec.md`.

**Cursor Prompt:**
```
You are the Backend Architect + API Designer. Do NOT write code.
Using §8.1, §8.4, §8.5, §8.7-§8.9 + Template 16 + Module 13 ONLY:
1. Define the Django apps and each app's single responsibility (api, forensic_engine wrapping 11_AI_Forensic_System, evidence, reports, core, health, versioning). Backend OWNS the investigation; no model training code.
2. Write api_spec.md for the canonical endpoints: POST /cases, GET /cases/{id}, POST /cases/{id}/upload, GET /cases/{id}/status, /evidence, /decision, /explanation, /report, GET /health, GET /version — each with request/response/errors/examples/version.
3. Specify async investigation (polled/streamed job), error handling (no stack traces to users), config (env-based, configured URLs, secrets via env), right-sized security (validation, upload limits, rate limiting, CORS/CSRF), media handling (versioned per case, never overwrite, never committed).
Output specs for review.
```

**Google Antigravity Prompt:** *None yet — architecture/spec only. Implementation begins STEP-061.*

**GitHub Expectations:** Branch `feature/backend-architecture` → PR into `develop`. Commit `docs: specify backend architecture and REST API contract`.

**Kaggle Expectations:** None.

**Documentation Updates:** `api_spec.md`; `13_Backend/README.md`.

**Verification Checklist:**
- ✓ All §8.5 endpoints specified (request/response/errors/examples/version).
- ✓ App responsibilities single + clear; forensic engine isolated.
- ✓ Async investigation + error handling + config + security specified.
- ✓ No training code; no hardcoded URLs; secrets via env.

**Common Mistakes:** Frontend/inference logic in the API spec; hardcoded URLs; exposing stack traces; committing media.

**Recovery Procedure:** Move any inference logic behind `forensic_engine`; ensure the spec matches the canonical endpoint table exactly.

**Definition of Done:** Backend architecture + API contract specified; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-061 — Django scaffold + forensic_engine wrapper.

---

## STEP-061 — Django Scaffold & Forensic Engine Wrapper  **[C][A]**

**Title:** Build the Django project + apps and wrap the Forensic Analyst.

**Objective:** Scaffold the Django/DRF project with the specified apps, environment-based config, logging, and a `forensic_engine` app that invokes the [11_AI_Forensic_System](MASTER_RESEARCH_OPERATING_SYSTEM.md#11_ai_forensic_system) pipeline as an async job — without duplicating any forensic logic.

**Why this step exists:** [§8.4](MASTER_RESEARCH_OPERATING_SYSTEM.md#84-backend-architecture-django--drf): the backend serves the Forensic Analyst; the engine app is the only bridge.

**Handbook References:** [§8.4](MASTER_RESEARCH_OPERATING_SYSTEM.md#84-backend-architecture-django--drf); [§8.6 Storage](MASTER_RESEARCH_OPERATING_SYSTEM.md#86-file-storage); [§8.9 Config/Logging](MASTER_RESEARCH_OPERATING_SYSTEM.md#89-configuration-logging-testing-accessibility-performance); [13_Backend contract](MASTER_RESEARCH_OPERATING_SYSTEM.md#13_backend).

**Prerequisites:** STEP-060 (architecture), STEP-059 (Analyst entrypoint).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1 day.
**Parallelizable:** No.

**Inputs:** Backend architecture; Forensic Analyst entrypoint.

**Expected Outputs:** Django project + apps scaffold; `forensic_engine` wrapping the pipeline; env config + logging; `.env.example`.

**Repository Changes:**
- *New:* Django project under `13_Backend/` with apps; `core/config`; `.env.example` (no secrets); logging config.

**Cursor Prompt:**
```
You are reviewing the backend scaffold plan for Antigravity.
Provide: the app layout (single responsibility each), env-based settings (dev/test/prod), logging config (application/API/inference/case/error/audit/performance), media handling (per-case, versioned, never overwrite, never committed — .gitignore already covers 13_Backend/media/), and the forensic_engine wrapper contract (calls 11_AI_Forensic_System as an async job; NO duplicated forensic logic; model path from config). Then review the implementation for §8 compliance.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Scaffold the Django + DRF project in 13_Backend/ with the approved apps, env-based settings, logging, and a forensic_engine app that runs the 11_AI_Forensic_System pipeline as an async job. Add .env.example (no real secrets).
Constraints: no forensic/inference logic duplicated (call the package); no training code; secrets via env; media never committed; configured URLs only.
Definition of Done: project runs (dev), apps present, forensic_engine invokes the pipeline on a sample, logging works.
```

**GitHub Expectations:** Branch `feature/backend-scaffold` → PR into `develop`. Commit `feat: scaffold Django backend and forensic engine wrapper`.

**Kaggle Expectations:** None.

**Documentation Updates:** Backend setup in `13_Backend/README.md`; `.env.example`.

**Verification Checklist:**
- ✓ Apps scaffolded with single responsibilities.
- ✓ `forensic_engine` calls the pipeline (no duplicated logic).
- ✓ Env-based config + logging; `.env.example` has no secrets.
- ✓ Media never committed; no training code.

**Common Mistakes:** Reimplementing forensic logic in the backend; committing secrets/media; hardcoded config.

**Recovery Procedure:** Replace duplicated logic with a call into `11_AI_Forensic_System`; purge any committed secret/media and rotate.

**Definition of Done:** Backend scaffold + engine wrapper working; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-062 — API endpoints + Backend Gate.

---

## STEP-062 — API Endpoints & Backend Gate  **[C][A][H]**  **GATE (Checklist 11)**

**Title:** Implement all endpoints, serializers, validation, health/version; pass Backend gate.

**Objective:** Implement the canonical endpoints (§8.5) with serializers, input/file validation, error handling, media handling, `/health`, `/version` (system/model/dataset versions + Git commit), and API tests; pass [Checklist 11](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-11--backend).

**Why this step exists:** [§8.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#django-rest-api-contract) + [Checklist 11](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-11--backend): the API is the only interface between frontend and the investigation.

**Handbook References:** [§8.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#django-rest-api-contract); [§8.7 Errors](MASTER_RESEARCH_OPERATING_SYSTEM.md#87-error-handling); [§8.8 Security](MASTER_RESEARCH_OPERATING_SYSTEM.md#88-security-right-sized); [Checklist 11](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-11--backend); [Module 15 audit](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-15--audit-trail).

**Prerequisites:** STEP-061 (scaffold).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1–2 days.
**Parallelizable:** Yes (per endpoint after the case flow exists).

**Inputs:** `api_spec.md`; forensic engine.

**Expected Outputs:** All endpoints implemented + serializers + validation + tests; `backend_audit` = PASS.

**Repository Changes:**
- *New:* endpoint views/serializers/urls/tests; health + version endpoints; audit integration.

**Cursor Prompt:**
```
You are reviewing the API implementation for Antigravity + Backend Auditor.
Using §8.5, §8.7, §8.8 + Checklist 11 ONLY: specify each endpoint's serializer, validation, error responses (no stack traces), and the async status flow (Uploading->Validating->...->Complete per Module 14 semantics). /version returns system/model/dataset versions + Git commit; /health returns health. Specify API tests (happy path + invalid/corrupted upload + not-found + backend-error). Run Checklist 11 -> backend audit.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement all canonical endpoints (POST /cases, GET /cases/{id}, POST /cases/{id}/upload, GET /cases/{id}/status|evidence|decision|explanation|report, GET /health, GET /version) with serializers, validation, structured error handling, media handling (versioned per case), audit-trail writes, and API tests.
Constraints: match api_spec.md exactly; no stack traces to clients; upload limits + validation + CORS/CSRF; configured URLs; secrets via env.
Definition of Done: all endpoints implemented + tested (incl. failure cases); /version reports versions + Git commit; Checklist 11 PASS.
```

**GitHub Expectations:** Branch `feature/backend-api` → PR into `develop`; **[H]** confirm Checklist 11 PASS. Commit `feat: implement REST API endpoints; pass backend gate`.

**Kaggle Expectations:** None.

**Documentation Updates:** `api_spec.md` finalized; backend audit; API tests documented.

**Verification Checklist (GATE — [Checklist 11](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-11--backend)):**
- ✓ All §8.5 endpoints implemented + match the spec.
- ✓ Validation, logging, config, media handling, security in place.
- ✓ `/version` returns system/model/dataset versions + Git commit; `/health` works.
- ✓ API tests (incl. failure cases) pass; no stack traces exposed.
- ✓ Backend audit = PASS.

**Common Mistakes:** Endpoint drift from the spec; leaking stack traces; committing media; missing version provenance.

**Recovery Procedure:** If Checklist 11 FAILS, do not start frontend. Align endpoints to the spec, add missing tests/validation, re-audit.

**Definition of Done:** API complete + tested; **Checklist 11 = PASS**; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-063 — Frontend architecture & API client (begins Frontend).

---

# PART 11 — FRONTEND DEVELOPMENT

> Implements [§8.3 Frontend (React + Vite + Tailwind)](MASTER_RESEARCH_OPERATING_SYSTEM.md#83-frontend-architecture-react--vite--tailwind) in [12_Web](MASTER_RESEARCH_OPERATING_SYSTEM.md#12_web). **The frontend owns the experience; it never performs inference or interprets probabilities** ([§8.1](MASTER_RESEARCH_OPERATING_SYSTEM.md#81-separation-of-concerns-binding)). Ends with [Checklist 10](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-10--frontend).

---

## STEP-063 — Frontend Architecture & API Client Design  **[C]**

**Title:** Design pages/components/state and the API client (§8.3).

**Objective:** Produce the frontend architecture: page list, component library, state boundaries, and the API client module (all fetch logic in `src/api`, configured base URL) — designed as an *investigation experience*.

**Why this step exists:** [§8.3](MASTER_RESEARCH_OPERATING_SYSTEM.md#83-frontend-architecture-react--vite--tailwind) + [Module 14](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-14--frontend-interaction): the experience is an investigation, not a bare verdict; fetch logic never lives in components.

**Handbook References:** [§8.3](MASTER_RESEARCH_OPERATING_SYSTEM.md#83-frontend-architecture-react--vite--tailwind); [Module 14](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-14--frontend-interaction); [§8.1](MASTER_RESEARCH_OPERATING_SYSTEM.md#81-separation-of-concerns-binding); [12_Web contract](MASTER_RESEARCH_OPERATING_SYSTEM.md#12_web).

**Prerequisites:** STEP-062 (API available + spec).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** No (gates frontend build).

**Inputs:** `api_spec.md`; §8.3 page/component lists.

**Expected Outputs:** Frontend architecture doc; API client design; page/component inventory with props + API dependencies.

**Repository Changes:**
- *New:* frontend architecture doc in `12_Web/`.

**Cursor Prompt:**
```
You are the Frontend Architect + API Designer (frontend). Do NOT write code.
Using §8.3 + Module 14 + §8.1 + api_spec.md ONLY:
1. Define the folder structure (pages, layouts, components, hooks, api, context, utils, assets, styles) and the API client module (all fetch logic in src/api; base URL from env/config; NEVER hardcoded).
2. Inventory the pages (Landing, About, Investigation Dashboard, Upload, Progress, Evidence Viewer, Result Summary, Explanation Viewer, Report Viewer, System Info, Docs, API Docs, 404, Error) with purpose, components, API deps, navigation.
3. Inventory reusable components (Navbar, Upload Area, Progress Indicator, Evidence Card, Confidence Gauge, Timeline, Report Viewer, Version Badge, etc.) with props/accessibility/extensibility.
4. Define the investigation UX (progress states from Module 14) — avoid bare "Fake (99.8%)".
Output the architecture for review.
```

**Google Antigravity Prompt:** *None yet — architecture only; build in STEP-064.*

**GitHub Expectations:** Branch `feature/frontend-architecture` → PR into `develop`. Commit `docs: specify frontend architecture and API client`.

**Kaggle Expectations:** None.

**Documentation Updates:** Frontend architecture; `12_Web/README.md`.

**Verification Checklist:**
- ✓ Folder structure + API client (configured URL) specified.
- ✓ All §8.3 pages + components inventoried with API deps.
- ✓ Investigation UX (progress states) designed; no bare verdict.
- ✓ No inference/interpretation logic in the frontend design.

**Common Mistakes:** Fetch logic in components; hardcoded API URL; presenting a bare probability as the verdict.

**Recovery Procedure:** Move fetch logic into `src/api`; ensure the base URL is configured; redesign result page as an investigation summary.

**Definition of Done:** Frontend architecture specified; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-064 — Scaffold + component library.

---

## STEP-064 — Scaffold React App & Component Library  **[C][A]**

**Title:** Build the Vite + Tailwind app shell, routing, API client, and reusable components.

**Objective:** Scaffold the React + Vite + Tailwind app with routing, theme tokens, the API client (`src/api`), context providers, error boundaries, loading states, and the reusable component library.

**Why this step exists:** [§8.3](MASTER_RESEARCH_OPERATING_SYSTEM.md#83-frontend-architecture-react--vite--tailwind): a reusable, accessible component library + centralized API client underpin every page.

**Handbook References:** [§8.3](MASTER_RESEARCH_OPERATING_SYSTEM.md#83-frontend-architecture-react--vite--tailwind); [§8.9 Accessibility/Performance](MASTER_RESEARCH_OPERATING_SYSTEM.md#89-configuration-logging-testing-accessibility-performance); [Checklist 10](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-10--frontend).

**Prerequisites:** STEP-063 (architecture).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1 day.
**Parallelizable:** Yes (components independent).

**Inputs:** Frontend architecture; API spec.

**Expected Outputs:** App shell + routing + theme; API client; component library + error boundaries/loading states.

**Repository Changes:**
- *New:* `12_Web/` Vite project (`src/{pages,layouts,components,hooks,api,context,utils,assets,styles}`), config for API base URL.

**Cursor Prompt:**
```
You are reviewing the frontend scaffold plan.
Provide Antigravity: the Vite+Tailwind setup, routing, theme tokens, the src/api client (base URL from env), context providers (theme, API status), error boundaries, loading/empty/error states, and the reusable component library contracts (props + accessibility). Then review for §8.3/§8.9 compliance (no fetch in components; configured URLs; accessible, responsive).
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Scaffold the React + Vite + Tailwind app in 12_Web with routing, theme, the src/api client (base URL from env config), context providers, error boundaries, loading/empty/error states, and the reusable components (Navbar, Footer, Button, Card, Upload Area, Progress Indicator, Status Badge, Evidence Card, Confidence Gauge, Timeline, Accordion, Table, Modal, Toast, Alert, Loading Spinner, Report Viewer, Image Viewer, Metric Card, Version Badge, Case Summary).
Constraints: NO inference/probability interpretation; ALL fetch logic in src/api; configured URLs; accessible + responsive; no hardcoded API URLs.
Definition of Done: app builds + runs; components render; API client wired to config; accessibility basics in place.
```

**GitHub Expectations:** Branch `feature/frontend-scaffold` → PR into `develop`. Commit `feat: scaffold React app shell and component library`.

**Kaggle Expectations:** None.

**Documentation Updates:** Component docs; `12_Web/README.md`.

**Verification Checklist:**
- ✓ App builds + runs; routing + theme + API client configured.
- ✓ Component library present with accessible, reusable components.
- ✓ No fetch logic in components; no hardcoded URLs.
- ✓ Error boundaries + loading/empty/error states exist.

**Common Mistakes:** Hardcoded API URL; inline fetches; inaccessible components; probability interpretation in the UI.

**Recovery Procedure:** Centralize fetches in `src/api`; parameterize the base URL; add missing accessibility attributes.

**Definition of Done:** App shell + components built; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-065 — Investigation flow pages + Frontend Gate.

---

## STEP-065 — Investigation Flow Pages & Frontend Gate  **[C][A][H]**  **GATE (Checklist 10)**

**Title:** Implement the end-to-end investigation experience; pass Frontend gate.

**Objective:** Implement Upload → Progress → Evidence Viewer → Result Summary → Explanation Viewer → Report Viewer (+ System Info, Docs), consuming the API via `src/api`, presenting an investigation (not a bare verdict); pass [Checklist 10](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-10--frontend).

**Why this step exists:** [Module 14](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-14--frontend-interaction) + [§8.3](MASTER_RESEARCH_OPERATING_SYSTEM.md#83-frontend-architecture-react--vite--tailwind): the frontend visualizes the forensic investigation defined by the backend.

**Handbook References:** [§8.3 Pages](MASTER_RESEARCH_OPERATING_SYSTEM.md#83-frontend-architecture-react--vite--tailwind); [Module 14](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-14--frontend-interaction); [Checklist 10](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-10--frontend); [§8.7 Errors](MASTER_RESEARCH_OPERATING_SYSTEM.md#87-error-handling).

**Prerequisites:** STEP-064 (scaffold + components), STEP-062 (API).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1–2 days.
**Parallelizable:** Yes (per page).

**Inputs:** Component library; API client; API spec.

**Expected Outputs:** All investigation pages functional against the API; `frontend_audit` = PASS.

**Repository Changes:**
- *New:* page components + hooks wired to the API client + tests.

**Cursor Prompt:**
```
You are reviewing the pages implementation + Frontend Auditor.
Using §8.3 + Module 14 + §8.7 + Checklist 10 ONLY: specify each page's data flow via src/api (poll GET /cases/{id}/status; render evidence/decision/explanation/report), the investigation progress UX (Uploading->Validating->Detecting Face->...->Complete), error/empty/loading states, and accessibility. Run Checklist 10 -> frontend audit.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the investigation pages (Upload, Progress, Evidence Viewer, Result Summary, Explanation Viewer, Report Viewer, System Info, Docs, 404/Error) wired to the API client, with polling for status, accessible + responsive layouts, and error/empty/loading handling. Add component/page tests.
Constraints: NO inference/probability interpretation (display backend results only); all fetches via src/api; configured URLs; investigation UX (never a bare "Fake 99.8%").
Definition of Done: full investigation flow works against the API; tests pass; Checklist 10 PASS.
```

**GitHub Expectations:** Branch `feature/frontend-pages` → PR into `develop`; **[H]** confirm Checklist 10 PASS. Commit `feat: implement investigation flow pages; pass frontend gate`.

**Kaggle Expectations:** None.

**Documentation Updates:** Page docs; frontend audit; `12_Web/README.md`.

**Verification Checklist (GATE — [Checklist 10](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-10--frontend)):**
- ✓ All investigation pages implemented + wired to the API.
- ✓ Progress/loading/error/empty states handled; accessible + responsive.
- ✓ No inference/interpretation in the frontend; results displayed only.
- ✓ Component/page tests pass; frontend audit = PASS.

**Common Mistakes:** Interpreting probabilities in the UI; missing error/loading states; bare-verdict result page.

**Recovery Procedure:** If Checklist 10 FAILS, fix each item (missing state, accessibility, spec mismatch) and re-audit before integration.

**Definition of Done:** Investigation experience complete; **Checklist 10 = PASS**; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-066 — System integration.

---

# PART 12 — SYSTEM INTEGRATION & TESTING

> Implements [§8.2 Data Flow](MASTER_RESEARCH_OPERATING_SYSTEM.md#82-data-flow) and [§8.9 Testing](MASTER_RESEARCH_OPERATING_SYSTEM.md#89-configuration-logging-testing-accessibility-performance). Confirms frontend ↔ backend ↔ Forensic Analyst work as one system.

---

## STEP-066 — System Integration  **[C][A]**

**Title:** Wire frontend ↔ backend ↔ Forensic Analyst end to end (§8.2).

**Objective:** Verify the full data flow `Browser → React → API Client → Django REST API → AI Forensic Analyst → … → JSON → React`, including async investigation, media handling, and `/version` provenance, with configured environments.

**Why this step exists:** [§8.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#82-data-flow) + [§8.10](MASTER_RESEARCH_OPERATING_SYSTEM.md#810-deployment-readiness--future-extensions): the tiers must operate as one coherent system.

**Handbook References:** [§8.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#82-data-flow); [§8.6](MASTER_RESEARCH_OPERATING_SYSTEM.md#86-file-storage); [§8.10](MASTER_RESEARCH_OPERATING_SYSTEM.md#810-deployment-readiness--future-extensions); [Checklists 9–11](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-9--ai-forensic-analyst).

**Prerequisites:** STEP-059 (Analyst), STEP-062 (API), STEP-065 (frontend).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1 day.
**Parallelizable:** No.

**Inputs:** All three tiers.

**Expected Outputs:** A working end-to-end run (upload a face image → receive a forensic report in the UI); an integration guide; environment configs (dev/test).

**Repository Changes:**
- *New/updated:* integration config; `16_Documentation/` integration notes; sample `.env.example` for both tiers.

**Cursor Prompt:**
```
You are the integration reviewer.
Using §8.2 + §8.6 + §8.10 ONLY: specify the end-to-end integration test (upload -> case created -> investigation runs async -> status polled -> evidence/decision/explanation/report retrieved -> report rendered), the environment configuration (frontend base URL -> backend; backend -> forensic engine + model path), CORS, media handling, and a smoke checklist. Then review the integration for separation-of-concerns compliance.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Wire the environments so the frontend talks to the backend and the backend runs the Forensic Analyst end to end. Provide a documented run (dev) proving upload->report works, including /version provenance. Fix any integration mismatch (serializer shapes, CORS, async status).
Constraints: configured URLs only; no secrets; media not committed; do not move logic across tier boundaries.
Definition of Done: end-to-end investigation works in dev; integration guide written.
```

**GitHub Expectations:** Branch `feature/system-integration` → PR into `develop`. Commit `feat: integrate frontend, backend, and forensic analyst end-to-end`.

**Kaggle Expectations:** None.

**Documentation Updates:** Integration guide in `16_Documentation`.

**Verification Checklist:**
- ✓ Upload → investigation → report works end to end (dev).
- ✓ Async status flow functions; media handled per case.
- ✓ `/version` provenance surfaced in the UI.
- ✓ Separation of concerns intact (no logic crossing tiers).

**Common Mistakes:** Serializer/shape mismatches; CORS failures; logic leaking across tiers; hardcoded URLs.

**Recovery Procedure:** Align serializer shapes to the frontend contract; fix CORS/config; keep forensic logic in the Analyst package.

**Definition of Done:** System integrated end to end; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-067 — Testing suite.

---

## STEP-067 — Testing Suite  **[C][A]**

**Title:** Frontend, backend, API, integration, smoke, regression, UAT (§8.9).

**Objective:** Establish the full testing suite across tiers (unit, integration, API, component, manual, smoke, regression, UAT) with a documented test plan and passing runs.

**Why this step exists:** [§8.9 Testing](MASTER_RESEARCH_OPERATING_SYSTEM.md#89-configuration-logging-testing-accessibility-performance): a research platform must be verifiable and regression-safe.

**Handbook References:** [§8.9](MASTER_RESEARCH_OPERATING_SYSTEM.md#89-configuration-logging-testing-accessibility-performance); [Checklists 10–11](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-10--frontend); [§13 QA](MASTER_RESEARCH_OPERATING_SYSTEM.md#13-quality-assurance).

**Prerequisites:** STEP-066 (integration).

**Estimated Difficulty:** Medium.
**Estimated Time:** 1 day.
**Parallelizable:** Yes (by tier).

**Inputs:** All tiers + existing unit tests.

**Expected Outputs:** Consolidated test suite + a test plan doc + passing runs; regression + smoke tests.

**Repository Changes:**
- *New:* additional tests (API/integration/component/UAT); test plan in `16_Documentation`.

**Cursor Prompt:**
```
You are the Testing agent (plan + review).
Using §8.9 ONLY: specify the test plan across frontend (component), backend (unit + API), integration (end-to-end), smoke, regression, and a UAT script (upload real + corrupted + no-face images and verify investigation behavior). Then review coverage. Do not write the tests yourself.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Implement the approved test suite (backend unit + API tests, frontend component tests, an end-to-end integration test, smoke + regression tests) and a UAT script. Ensure all pass.
Constraints: deterministic; cover failure cases (corrupted/no-face/backend-down); no network to external services in unit tests.
Definition of Done: full suite implemented + green; UAT script documented.
```

**GitHub Expectations:** Branch `feature/testing-suite` → PR into `develop`. Commit `test: add cross-tier test suite and UAT script`.

**Kaggle Expectations:** None.

**Documentation Updates:** Test plan; coverage notes.

**Verification Checklist:**
- ✓ Unit + API + component + integration + smoke + regression tests pass.
- ✓ Failure cases covered (corrupted/no-face/backend-down).
- ✓ UAT script documented + executed.
- ✓ Tests deterministic + isolated.

**Common Mistakes:** Only happy-path tests; flaky/networked unit tests; no regression coverage.

**Recovery Procedure:** Add failure-case + regression tests; isolate external dependencies with mocks.

**Definition of Done:** Testing suite complete + green; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-068 — System/developer/user documentation.

---

# PART 13 — DOCUMENTATION

> Implements [§16_Documentation](MASTER_RESEARCH_OPERATING_SYSTEM.md#16_documentation) and [§10 Phase 15](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-15--documentation-workflow). Gated by [Checklist 12](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-12--documentation).

---

## STEP-068 — System, Developer & User Documentation + Documentation Gate  **[C][A][H]**  **GATE (Checklist 12)**

**Title:** Author architecture/API/developer/user/installation docs; pass Documentation gate.

**Objective:** Produce `architecture.md`, `api_guide.md`, `developer_guide.md`, `user_guide.md`, `installation.md`, workflow diagrams, and folder guides in [16_Documentation](MASTER_RESEARCH_OPERATING_SYSTEM.md#16_documentation), linking to (not duplicating) the handbook; pass [Checklist 12](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-12--documentation).

**Why this step exists:** [§16](MASTER_RESEARCH_OPERATING_SYSTEM.md#16_documentation) + [Principle 3 (documentation)](MASTER_RESEARCH_OPERATING_SYSTEM.md#16-the-eight-operating-principles): the system must be usable + maintainable by others; a final deliverable ([§1.12](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-final-deliverables)).

**Handbook References:** [§16_Documentation](MASTER_RESEARCH_OPERATING_SYSTEM.md#16_documentation); [§10 Phase 15](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-15--documentation-workflow); [Checklist 12](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-12--documentation); [§1.12 Deliverables](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-final-deliverables).

**Prerequisites:** STEP-062/065/066/067 (system complete + tested).

**Estimated Difficulty:** Medium.
**Estimated Time:** 1 day.
**Parallelizable:** Yes (by document).

**Inputs:** All prior specs/registries; API spec; module registry.

**Expected Outputs:** Full documentation set + workflow diagrams; `documentation_audit` = PASS.

**Repository Changes:**
- *New:* the documentation files + `workflow_diagrams/`.

**Cursor Prompt:**
```
You are the Documentation agent + Documentation Auditor.
Using §16 + Phase 15 + Checklist 12 ONLY: draft architecture.md (system + tiers + forensic pipeline), api_guide.md (from api_spec.md), developer_guide.md (setup, workflow Cursor->Antigravity->GitHub->Kaggle, how to add an evidence collector/fusion strategy), user_guide.md (how to run an investigation), installation.md, folder guides, and workflow diagrams. LINK to the handbook; do not duplicate it. Run Checklist 12 -> documentation audit.
Output for human approval.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Save the approved documentation files + workflow diagrams to 16_Documentation and the documentation audit.
Constraints: link to the handbook (no duplication); keep consistent with api_spec.md + module_registry.csv; no stale/contradictory content.
Definition of Done: documentation set complete + consistent; Checklist 12 PASS.
```

**GitHub Expectations:** Branch `docs/system-documentation` → PR into `develop`; **[H]** confirm Checklist 12 PASS. Commit `docs: add system/developer/user documentation; pass documentation gate`.

**Kaggle Expectations:** None.

**Documentation Updates:** All of `16_Documentation`.

**Verification Checklist (GATE — [Checklist 12](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-12--documentation)):**
- ✓ Architecture, API guide, README, developer + user guides, installation present.
- ✓ Workflow diagrams + folder explanations present.
- ✓ Decision logs + experiment registry referenced; no handbook duplication.
- ✓ Consistent with `api_spec.md` + registries; documentation audit = PASS.

**Common Mistakes:** Duplicating the handbook; docs drifting from the API; missing "how to extend" guidance.

**Recovery Procedure:** Replace duplicated handbook content with links; sync docs to the current API/registries; re-audit.

**Definition of Done:** Documentation complete + consistent; **Checklist 12 = PASS**; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-069 — Writing evidence & Writing Database (begins Writing).

---
# PART 14 — WRITING

> Implements [§9 Writing Operating System, Phases W1–W17](MASTER_RESEARCH_OPERATING_SYSTEM.md#9-writing-operating-system). **Every paragraph originates from verified evidence** ([§9.1](MASTER_RESEARCH_OPERATING_SYSTEM.md#91-writing-philosophy)). Files in [15_Writing](MASTER_RESEARCH_OPERATING_SYSTEM.md#15_writing). Ends with [Checklist 13](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-13--writing-readiness).

---

## STEP-069 — Writing Evidence Collection & Writing Database  **[C][A]**

**Title:** Assemble evidence + stand up the Writing Database (Phases W1–W3).

**Objective:** Gather evidence from all registries (literature, claims, gaps, dataset/experiment/evaluation reports, decision logs, failures), organize it (`knowledge_index.csv`), and populate the [Writing Database](MASTER_RESEARCH_OPERATING_SYSTEM.md#writing-database) `writing_database.csv` (the prose traceability spine).

**Why this step exists:** [W1–W3](MASTER_RESEARCH_OPERATING_SYSTEM.md#9-writing-operating-system): never start from a blank page; every writing unit maps to supporting evidence.

**Handbook References:** [Phase W1](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w1--evidence-collection); [W2](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w2--knowledge-organization); [W3 Writing Database](MASTER_RESEARCH_OPERATING_SYSTEM.md#writing-database); [Claim Database](MASTER_RESEARCH_OPERATING_SYSTEM.md#claim-database).

**Prerequisites:** STEP-050 (evaluation done), STEP-059 (analyst done), STEP-017 (literature).

**Estimated Difficulty:** Medium.
**Estimated Time:** Half day.
**Parallelizable:** Yes.

**Inputs:** All registries + reports.

**Expected Outputs:** `knowledge_index.csv`; populated `writing_database.csv` mapping sections → supporting papers/experiments/claims/figures/tables.

**Repository Changes:**
- *Updated:* `15_Writing/shared/{knowledge_index,writing_database}.csv`.

**Cursor Prompt:**
```
You are the Evidence + Outline writing agents.
Using W1-W3 ONLY: gather evidence from papers.csv, claim_database.csv, research_gap.csv, dataset/experiment/evaluation reports, decision logs, failure reports. Build knowledge_index.csv (categorized evidence) and draft writing_database.csv rows (Writing ID, Section, Topic, Supporting Papers/Experiments/Claims/Figures/Tables, Status, Owner, Revision). No prose yet — just the evidence-to-section map.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Save the approved knowledge_index.csv + writing_database.csv rows.
Constraints: every writing unit links to concrete evidence IDs; append-or-update only; no unsupported entries.
Definition of Done: writing evidence organized + database populated.
```

**GitHub Expectations:** Branch `writing/evidence-base` → PR into `develop`. Commit `writing: assemble evidence base and writing database`.

**Kaggle Expectations:** None.

**Documentation Updates:** `writing_database.csv`, `knowledge_index.csv`.

**Verification Checklist:**
- ✓ Evidence gathered from all registries/reports.
- ✓ `knowledge_index.csv` categorized; `writing_database.csv` maps sections→evidence.
- ✓ No writing unit lacks supporting evidence IDs.

**Common Mistakes:** Planning prose without evidence; missing experiment/claim links.

**Recovery Procedure:** Attach evidence IDs to every writing unit; drop any unit lacking support.

**Definition of Done:** Writing evidence base ready; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-070 — Draft thesis chapters.

---

## STEP-070 — Draft Thesis Chapters  **[C][A][H]**

**Title:** Generate chapter drafts from evidence (Phases W4–W5).

**Objective:** Using section templates (W4), draft the thesis chapters (1 Introduction, 2 Literature Review, 3 Methodology, 4 Implementation, 5 Evaluation, 6 Results, 7 Discussion, 8 Conclusion + Appendices/References), each paragraph traced to the Writing/Claim databases.

**Why this step exists:** [W5](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w5--thesis-pipeline): the thesis is the comprehensive output; [§9.1/§9.3](MASTER_RESEARCH_OPERATING_SYSTEM.md#93-scientific-writing-principles-binding) forbid unsupported/fabricated prose.

**Handbook References:** [Phase W4](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w4--writing-templates); [W5](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w5--thesis-pipeline); [W7 Writing Rules](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w7--writing-rules); [§9.4 Thesis vs Journal](MASTER_RESEARCH_OPERATING_SYSTEM.md#94-thesis-vs-journal).

**Prerequisites:** STEP-069 (evidence base).

**Estimated Difficulty:** Hard.
**Estimated Time:** Multiple days (one chapter per session recommended).
**Parallelizable:** Yes (chapters are independent given the evidence).

**Inputs:** Writing/Claim databases; literature drafts; evaluation reports; figure/table specs.

**Expected Outputs:** Chapter drafts in `15_Writing/thesis/` with inline evidence references.

**Repository Changes:**
- *New:* `15_Writing/thesis/chapterN_*.md` drafts.

**Cursor Prompt:**
```
You are the section writing agents (Related Work, Methodology, Results, Discussion, Conclusion).
Using W4-W5 + W7 + §9.4 ONLY: draft ONE chapter per session. Every paragraph must cite Writing IDs / Claim IDs / P IDs / EXP IDs / FIG/TAB IDs. Follow the writing rules (formal, evidence-based, no AI filler, no gratuitous em-dashes, no fabricated results/citations/limitations). Mark any place lacking evidence as [EVIDENCE NEEDED] rather than inventing.
Output the chapter for human review.
```

**Google Antigravity Prompt:** *Optional — Antigravity may save approved chapter drafts to `15_Writing/thesis/`. It does not author scientific claims; all content is human-approved evidence-based prose. No code.*

**GitHub Expectations:** Branch `writing/thesis-draft` → PR into `develop`. Commit `writing: draft thesis chapter N`.

**Kaggle Expectations:** None.

**Documentation Updates:** Chapter drafts; `writing_progress.csv`.

**Verification Checklist:**
- ✓ Each chapter drafted from evidence; every paragraph references IDs.
- ✓ No fabricated results/citations/limitations; no AI filler.
- ✓ `[EVIDENCE NEEDED]` used instead of invention.
- ✓ Thesis-appropriate depth (§9.4).

**Common Mistakes:** Writing from memory; hallucinated citations; over-claiming novelty.

**Recovery Procedure:** Resolve every `[EVIDENCE NEEDED]` with a real source or cut the sentence; verify citations in STEP-071.

**Definition of Done:** Chapters drafted + evidence-traced; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-071 — Figures/tables/claims/citations/consistency.

---

## STEP-071 — Figures, Tables, Claim Verification, Citations & Consistency  **[C][A][H]**

**Title:** Integrate figures/tables, verify every claim + citation, run consistency checks (Phases W8–W11, W15).

**Objective:** Render figures **from specs** (human, per [A.9](MASTER_RESEARCH_OPERATING_SYSTEM.md#a9-canonical-figure-policy)) and integrate them by `FIG`/`TAB` ID (W8/W9), verify every claim via the [Claim Database](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w11--claim-verification) (W11), verify every citation against the [Papers Registry](MASTER_RESEARCH_OPERATING_SYSTEM.md#papers-registry) (W10), and run consistency checks (W15).

**Why this step exists:** [W8–W11/W15](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w8--figure-integration): traceable figures/tables, verified claims/citations, and consistency are prerequisites to submission.

**Handbook References:** [W8](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w8--figure-integration); [W9](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w9--table-integration); [W10 Citations](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w10--citation-management); [W11 Claim Verification](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w11--claim-verification); [W15](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w15--consistency-checking); [A.9](MASTER_RESEARCH_OPERATING_SYSTEM.md#a9-canonical-figure-policy); [Checklists 14 & 15](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-14--figure-quality).

**Prerequisites:** STEP-070 (drafts), STEP-050 (figure/table specs), STEP-015 (claims).

**Estimated Difficulty:** Hard.
**Estimated Time:** 1–2 days.
**Parallelizable:** Yes (figures vs. citation verification).

**Inputs:** Figure/table specs; drafts; Claim Database; `papers.bib`.

**Expected Outputs:** Rendered figures (human) in `09_Figures/assets/` + captions; tables rendered; every claim verified; citations verified; consistency report.

**Repository Changes:**
- *New/updated:* `09_Figures/assets/FIGxxxx_v1.*`, `10_Tables/rendered/`, updated `claim_database.csv` (Status=verified), consistency report.

**Cursor Prompt:**
```
You are the Citation Verification + Consistency + Results/Discussion agents.
Using W8-W11 + W15 + A.9 + Checklists 14/15 ONLY:
1. Provide human instructions (A.8) to render each FIGxxxx from its spec (the AI never renders — human produces PNG/SVG/PDF), with caption + provenance.
2. Verify every claim in the drafts against claim_database.csv (supporting papers/experiments/figures/tables; flag unsupported).
3. Verify every citation against papers.csv/papers.bib (no citation without a P ID); detect duplicates/inconsistencies.
4. Run consistency checks (terminology, figure/table numbering, IDs, versions, abbreviations, section refs).
Output a verification + consistency report; list every issue to fix.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY (tooling + saving). Implement/refresh a citation-verification + consistency-check script in 17_Automation (every cited key exists in papers.bib; figure/table IDs referenced; terminology consistent). Save rendered figures/captions + tables provided by the human to 09_Figures/10_Tables, and update claim_database.csv statuses per the approved verification.
Constraints: AI does not render figures (A.9) — only saves human-produced assets + runs checks; no unverified citation survives.
Definition of Done: verification + consistency scripts pass; figures/tables integrated; claims marked verified.
```

**GitHub Expectations:** Branch `writing/figures-claims-citations` → PR into `develop`. Commit `writing: integrate figures/tables, verify claims and citations`.

**Kaggle Expectations:** None.

**Documentation Updates:** Captions; consistency report; `claim_database.csv` statuses.

**Verification Checklist:**
- ✓ Every figure has ID + caption + source experiment + generation script ([Checklist 14](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-14--figure-quality)).
- ✓ Every table traceable ([Checklist 15](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-15--table-quality)).
- ✓ Every claim verified via the Claim Database; unsupported claims removed.
- ✓ Every citation exists in `papers.csv`/`papers.bib`; no duplicates.
- ✓ Consistency checks pass.

**Common Mistakes:** AI rendering figures; citations without `P` IDs; unverified claims surviving; inconsistent IDs/terms.

**Recovery Procedure:** Remove any citation lacking a `P` ID; resolve unsupported claims (find evidence or cut); re-run consistency checks until clean.

**Definition of Done:** Figures/tables/claims/citations verified + consistent; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-072 — Revision workflow + Writing Readiness Gate.

---

## STEP-072 — Revision Workflow & Writing Readiness Gate  **[C][H]**  **GATE (Checklist 13)**

**Title:** Multi-stage revision + writing-readiness gate (Phases W12–W13, W17).

**Objective:** Run the revision workflow (self → supervisor → grammar → technical → evidence → reference → formatting), track versions (W12), update the writing dashboard (W17), and pass [Checklist 13](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-13--writing-readiness).

**Why this step exists:** [W13](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w13--revision-workflow) + [Checklist 13](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-13--writing-readiness): drafts become submission-ready only after documented revision.

**Handbook References:** [W12](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w12--writing-version-control); [W13](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w13--revision-workflow); [W17 Dashboard](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w17--writing-dashboard); [Checklist 13](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-13--writing-readiness); [§9.3](MASTER_RESEARCH_OPERATING_SYSTEM.md#93-scientific-writing-principles-binding).

**Prerequisites:** STEP-071 (verified content).

**Estimated Difficulty:** Medium.
**Estimated Time:** Multiple days (supervisor-dependent).
**Parallelizable:** No (sequential review stages).

**Inputs:** Verified chapters; supervisor feedback.

**Expected Outputs:** Revised chapters with tracked versions; `writing_progress.csv` updated; `writing_audit` = PASS.

**Repository Changes:**
- *Updated:* chapter versions; `writing_progress.csv`; writing audit.

**Cursor Prompt:**
```
You are the Grammar + Consistency + Revision agents + Writing Auditor.
Using W12-W13 + W17 + Checklist 13 ONLY: run self-review + grammar + technical + evidence + reference + formatting reviews; track versions (SemVer); update writing_progress.csv (section completion, evidence completeness, missing figures/tables/citations, pending reviews). Prepare supervisor-review notes (A.8) for the human. Run Checklist 13 -> writing audit.
Output the revision report + audit.
```

**Google Antigravity Prompt:** *Optional — save revised versions + audit. No scientific authorship; no code beyond consistency tooling.*

**GitHub Expectations:** Branch `writing/revision` → PR into `develop`; **[H]** supervisor review + confirm Checklist 13 PASS. Commit `writing: complete revision workflow; pass writing readiness gate`.

**Kaggle Expectations:** None.

**Documentation Updates:** Version history; `writing_progress.csv`; writing audit.

**Verification Checklist (GATE — [Checklist 13](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-13--writing-readiness)):**
- ✓ Claims supported; figures/tables available; citations + references verified.
- ✓ Terminology consistent; grammar + formatting reviewed.
- ✓ Supervisor notes addressed; versions tracked.
- ✓ `writing_progress.csv` updated; writing audit = PASS.

**Common Mistakes:** Skipping supervisor review; untracked versions; unresolved reviewer notes.

**Recovery Procedure:** If Checklist 13 FAILS, address each item (missing figure, unverified reference, supervisor comment) and re-audit before assembly.

**Definition of Done:** Writing revised + review-ready; **Checklist 13 = PASS**; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-073 — Thesis assembly + Publication Readiness Score.

---

# PART 15 — THESIS SUBMISSION

> Implements [§9 Phase W18](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w18--publication-readiness), [Checklist 19 Publication Readiness Score](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-19--publication-readiness-score), and [Checklist 17 Thesis Submission](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-17--thesis-submission).

---

## STEP-073 — Thesis Assembly & Publication Readiness Score  **[C][A][H]**  **GATE (Checklist 19)**

**Title:** Assemble the full thesis and compute the Publication Readiness Score.

**Objective:** Assemble all chapters + figures + tables + references + appendices into the complete thesis, run the weighted [Publication Readiness Score](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-19--publication-readiness-score), and produce `publication_readiness_report.md` (PASS/FAIL).

**Why this step exists:** [W18](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w18--publication-readiness) + [Checklist 19](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-19--publication-readiness-score): objective readiness scoring before submission.

**Handbook References:** [Phase W18](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w18--publication-readiness); [Checklist 19](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-19--publication-readiness-score); [Checklist 17](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-17--thesis-submission).

**Prerequisites:** STEP-072 (Writing Readiness PASS).

**Estimated Difficulty:** Medium.
**Estimated Time:** 1 day.
**Parallelizable:** No.

**Inputs:** Revised chapters + assets; all registries.

**Expected Outputs:** Assembled thesis; `publication_readiness_report.md` (category scores + overall + critical issues + PASS/FAIL).

**Repository Changes:**
- *New:* assembled thesis in `15_Writing/thesis/`; `publication_readiness_report.md`.

**Cursor Prompt:**
```
You are the Publication Auditor.
Using W18 + Checklist 19 ONLY: assemble the thesis structure (all chapters, figures by FIG ID, tables by TAB ID, references from references.bib, appendices) and compute the weighted Publication Readiness Score across Research Quality, Engineering Quality, Reproducibility, Documentation, Writing, Evaluation, Novelty, Software Quality, Scientific Integrity. Produce publication_readiness_report.md with category scores, overall readiness, critical issues, recommended actions, PASS/FAIL.
Output for human review.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Assemble the thesis document (compile chapters + assets + references) and save publication_readiness_report.md.
Constraints: figures/tables referenced by ID; references from references.bib; no unverified content.
Definition of Done: assembled thesis + readiness report saved.
```

**GitHub Expectations:** Branch `writing/thesis-assembly` → PR into `develop`; **[H]** review readiness score. Commit `writing: assemble thesis and compute publication readiness score`.

**Kaggle Expectations:** None.

**Documentation Updates:** Readiness report; assembled thesis.

**Verification Checklist (GATE — [Checklist 19](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-19--publication-readiness-score)):**
- ✓ All chapters/figures/tables/references/appendices assembled.
- ✓ Weighted score computed across all 9 categories.
- ✓ Critical issues listed + addressed; overall = PASS.
- ✓ Reproducibility + scientific integrity confirmed.

**Common Mistakes:** Submitting below the readiness threshold; missing appendices/references; ignoring critical issues.

**Recovery Procedure:** If FAIL, resolve critical issues (missing evidence, low reproducibility) and re-score before proceeding.

**Definition of Done:** Thesis assembled; **Checklist 19 = PASS**; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-074 — Thesis submission.

---

## STEP-074 — Thesis Submission  **[C][H]**  **GATE (Checklist 17)**

**Title:** Final thesis submission (Checklist 17).

**Objective:** Pass [Checklist 17](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-17--thesis-submission) (all chapters/figures/tables/references/appendices; formatting; supervisor approval; grammar; similarity check; final PDF; repository archived) and submit.

**Why this step exists:** [Checklist 17](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-17--thesis-submission): the thesis submission gate; a [final deliverable](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-final-deliverables).

**Handbook References:** [Checklist 17](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-17--thesis-submission); [Template 25 Submission Checklist](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); [§10 Phase 12 Releases](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-12--release-workflow); [W19 Archiving](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w19--archiving-policy).

**Prerequisites:** STEP-073 (readiness PASS).

**Estimated Difficulty:** Medium.
**Estimated Time:** 1 day (+ institutional process).
**Parallelizable:** No.

**Inputs:** Assembled thesis; readiness report.

**Expected Outputs:** Final PDF; completed `submission.md`; `v1.0` release tag; final thesis archived to [20_Archive](MASTER_RESEARCH_OPERATING_SYSTEM.md#20_archive).

**Repository Changes:**
- *New:* final thesis PDF (archived); `submission.md`; `v1.0` release; CHANGELOG entry.

**Cursor Prompt:**
```
You are the Publication Auditor.
Using Checklist 17 + Template 25 + Phase 12 + W19 ONLY: produce the submission checklist (all chapters/figures/tables/references/appendices complete; formatting per institution; supervisor approval; grammar; similarity check; final PDF; repository archived) and the human submission runbook (A.8): what to submit, where, and how to confirm. Specify the v1.0 release contents (source snapshot + key artifacts + docs + CHANGELOG) and the archival move to 20_Archive.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Save the completed submission.md, place the human-produced final PDF into 20_Archive (read-only), add the CHANGELOG entry, and prepare the v1.0 release notes/artifacts list.
Constraints: 20_Archive is read-only after placement; no active files there; final artifacts bundled to a GitHub Release (weights/exports via artifact tier).
Definition of Done: submission checklist complete; final thesis archived; v1.0 release prepared.
```

**GitHub Expectations:** Branch `release/v1.0` → PR `develop → main`; **[H]** tag `v1.0` (thesis submission) per [§10 Phase 12](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-12--release-workflow). Commit `release: thesis submission v1.0`.

**Kaggle Expectations:** None.

**Documentation Updates:** `submission.md`; CHANGELOG; archive.

**Verification Checklist (GATE — [Checklist 17](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-17--thesis-submission)):**
- ✓ All chapters/figures/tables/references/appendices complete + formatted.
- ✓ Supervisor approval; grammar + similarity check done.
- ✓ Final PDF produced + archived (read-only) to `20_Archive`.
- ✓ `v1.0` release tagged; repository archived.

**Common Mistakes:** Submitting without supervisor approval or similarity check; editing `20_Archive` after placement; forgetting the release tag.

**Recovery Procedure:** If a submission requirement is unmet, do not submit — resolve it. Never modify archived finals; supersede with a new archived version if needed.

**Definition of Done:** Thesis submitted; **Checklist 17 = PASS**; `v1.0` released; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-075 — Journal manuscript.

---

# PART 16 — JOURNAL SUBMISSION

> Implements [§9 Phase W6 Journal Pipeline](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w6--journal-pipeline) and [W14 Reviewer Response](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w14--reviewer-response-system). Reuses the **same evidence base** as the thesis ([§9.4](MASTER_RESEARCH_OPERATING_SYSTEM.md#94-thesis-vs-journal)). Gated by [Checklist 16](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-16--journal-submission).

---

## STEP-075 — Journal Manuscript & Journal Submission Gate  **[C][A][H]**  **GATE (Checklist 16)**

**Title:** Write the concise, novelty-focused manuscript from the shared evidence base (W6).

**Objective:** Produce the journal manuscript (Abstract, Introduction, Related Work, Method, Experiments, Results, Discussion, Conclusion, References, Supplementary) — concise + method-centric — reusing the Writing/Claim databases; pass [Checklist 16](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-16--journal-submission).

**Why this step exists:** [W6](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w6--journal-pipeline) + [§9.4](MASTER_RESEARCH_OPERATING_SYSTEM.md#94-thesis-vs-journal): the journal is the concise, novelty-focused variant of the same research; a [final deliverable](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-final-deliverables).

**Handbook References:** [Phase W6](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w6--journal-pipeline); [§9.4](MASTER_RESEARCH_OPERATING_SYSTEM.md#94-thesis-vs-journal); [Checklist 16](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-16--journal-submission); [W10 Citations](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w10--citation-management).

**Prerequisites:** STEP-074 (thesis submitted).

**Estimated Difficulty:** Hard.
**Estimated Time:** Multiple days.
**Parallelizable:** Yes (by section).

**Inputs:** Writing/Claim databases; thesis; target journal format.

**Expected Outputs:** Journal manuscript in `15_Writing/journal/` + supplementary; `submission.md` for the journal; `publication_audit` = PASS.

**Repository Changes:**
- *New:* `15_Writing/journal/` manuscript + supplementary; journal submission checklist.

**Cursor Prompt:**
```
You are the writing agents + Publication Auditor (journal).
Using W6 + §9.4 + Checklist 16 ONLY: draft the concise, novelty-focused manuscript reusing the SAME evidence base (no new unsupported claims), targeting high information density; select the most impactful figures/tables by ID; prepare supplementary + data/code availability statements. Verify citations against papers.bib. Run Checklist 16 -> publication audit.
Output for human review.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Save the approved manuscript + supplementary; refresh citation verification against papers.bib; save the journal submission checklist + publication audit.
Constraints: reuse existing evidence only; no fabricated content; format per target journal.
Definition of Done: manuscript + supplementary + audit saved; citations verified; Checklist 16 PASS.
```

**GitHub Expectations:** Branch `writing/journal` → PR into `develop`; **[H]** confirm Checklist 16 PASS. Commit `writing: prepare journal manuscript; pass journal submission gate`.

**Kaggle Expectations:** None.

**Documentation Updates:** Manuscript; supplementary; publication audit.

**Verification Checklist (GATE — [Checklist 16](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-16--journal-submission)):**
- ✓ Abstract/keywords/novelty/contribution clear; concise + method-centric.
- ✓ References + formatting per journal; supplementary prepared.
- ✓ Reproducibility + code/data availability statements present.
- ✓ Citations verified; author checklist complete; publication audit = PASS.

**Common Mistakes:** Introducing unsupported claims; exceeding scope; missing availability statements.

**Recovery Procedure:** Trim to supported claims; add availability statements; re-verify citations.

**Definition of Done:** Manuscript ready; **Checklist 16 = PASS**; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-076 — Journal submission & reviewer response.

---

## STEP-076 — Journal Submission & Reviewer Response System  **[C][H]**

**Title:** Submit and manage reviewer responses (Phase W14).

**Objective:** Submit the manuscript, and when reviews arrive, use `review_response.md` ([Template 18](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates)) to track each comment → action → evidence → response, revising the manuscript without losing reviewer history.

**Why this step exists:** [W14](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w14--reviewer-response-system): reviewer history is never lost; responses are evidence-backed. Ties to release `v1.1` (journal revision).

**Handbook References:** [Phase W14](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w14--reviewer-response-system); [Template 18](MASTER_RESEARCH_OPERATING_SYSTEM.md#142-the-templates); [§10 Phase 12 (v1.1)](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-12--release-workflow); [W19 Archiving](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w19--archiving-policy).

**Prerequisites:** STEP-075 (manuscript ready).

**Estimated Difficulty:** Medium.
**Estimated Time:** Recurring (review-cycle-dependent).
**Parallelizable:** Yes (per reviewer comment).

**Inputs:** Manuscript; reviewer comments.

**Expected Outputs:** Submitted manuscript; `reviewer_responses/review_response.md`; revised manuscript versions; `v1.1` release on acceptance/revision.

**Repository Changes:**
- *New/updated:* `15_Writing/reviewer_responses/`; `revisions/`; CHANGELOG; `v1.1` release.

**Cursor Prompt:**
```
You are the Reviewer Response agent.
Using W14 + Template 18 ONLY: produce the human submission runbook (A.8: where/how to submit). When reviews arrive, for each comment draft a review_response.md row (comment, category, affected section, planned action, implemented change, evidence, response draft, status) and the corresponding manuscript revision plan — every response backed by evidence (no fabrication). Track versions (W12). Prepare the v1.1 release notes for the revision.
```

**Google Antigravity Prompt:** *Optional — save reviewer-response docs + revised versions + v1.1 release notes. No fabricated content; no code beyond tooling.*

**GitHub Expectations:** Branch `writing/reviewer-response` → PR into `develop`; on revision, `release/v1.1` → `main`, tag `v1.1`. Commit `writing: address reviewer comments (v1.1)`.

**Kaggle Expectations:** None.

**Documentation Updates:** `review_response.md`; revision history; CHANGELOG.

**Verification Checklist:**
- ✓ Manuscript submitted; submission confirmed.
- ✓ Every reviewer comment tracked with an evidence-backed response.
- ✓ Revisions versioned; reviewer history preserved.
- ✓ `v1.1` release tagged on revision.

**Common Mistakes:** Losing reviewer history; unsupported rebuttals; untracked revision versions.

**Recovery Procedure:** Reconstruct the response ledger from correspondence; ground every rebuttal in recorded evidence.

**Definition of Done:** Submitted + reviewer responses managed; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-077 — Release + archival.

---

# PART 17 — PROJECT ARCHIVAL

> Implements [§10 Phase 12 Releases](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-12--release-workflow), [§9 W19 Archiving](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w19--archiving-policy), and [Checklist 18 Project Completion](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-18--project-completion).

---

## STEP-077 — Release & Archival  **[C][A][H]**

**Title:** Bundle releases and archive finals (Phase 12, W19).

**Objective:** Finalize releases (`v1.0` thesis, `v1.1` journal revision, and any accepted/camera-ready versions), archive submitted/accepted/camera-ready documents + retired designs to the read-only [20_Archive](MASTER_RESEARCH_OPERATING_SYSTEM.md#20_archive), and ensure artifacts are backed up per tier.

**Why this step exists:** [§10 Phase 12](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-12--release-workflow) + [W19](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w19--archiving-policy): releases + immutable archives preserve the record.

**Handbook References:** [§10 Phase 12](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-12--release-workflow); [§10 Phase 17 Backup](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-17--backup-strategy); [W19](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-w19--archiving-policy); [20_Archive contract](MASTER_RESEARCH_OPERATING_SYSTEM.md#20_archive).

**Prerequisites:** STEP-074 (thesis), STEP-076 (journal), all gates PASS.

**Estimated Difficulty:** Medium.
**Estimated Time:** 1 day.
**Parallelizable:** No.

**Inputs:** Final documents + artifacts; release history.

**Expected Outputs:** Tagged releases with bundled source/artifacts/docs/CHANGELOG; archived finals in `20_Archive`; verified backups.

**Repository Changes:**
- *Updated:* release tags; `20_Archive` populated (read-only); CHANGELOG; backup records.

**Cursor Prompt:**
```
You are the DevOps + Publication Auditor.
Using Phase 12 + Phase 17 + W19 ONLY: specify each release's contents (source snapshot, key artifacts via Releases/artifact tier, docs, CHANGELOG entry), the archival plan (submitted/accepted/camera-ready + retired designs -> 20_Archive read-only), and the backup verification (GitHub canonical remote, artifact/checkpoint backups, writing). Provide the human runbook (A.8) for tagging + archiving.
```

**Google Antigravity Prompt:**
```
IMPLEMENTATION ONLY. Prepare release notes + artifact bundles, add CHANGELOG entries, and move approved finals into 20_Archive (read-only). Verify backups exist per tier.
Constraints: never modify existing 20_Archive contents; large artifacts via Releases/Kaggle (not plain Git); no secrets.
Definition of Done: releases prepared; finals archived read-only; backups verified.
```

**GitHub Expectations:** `release/*` → `main`; tags per [Phase 12](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-12--release-workflow). Commit `release: finalize releases and archive project artifacts`.

**Kaggle Expectations:** Final datasets/checkpoints remain in Kaggle/artifact tier; referenced by release notes.

**Documentation Updates:** Release notes; CHANGELOG; archive index.

**Verification Checklist:**
- ✓ Releases tagged with bundled source/artifacts/docs/CHANGELOG.
- ✓ Finals archived to `20_Archive` (read-only); nothing modified there.
- ✓ Backups verified across tiers.
- ✓ Large artifacts via Releases/Kaggle (not plain Git); no secrets.

**Common Mistakes:** Modifying archived finals; committing large binaries; missing release bundles.

**Recovery Procedure:** Restore any altered archive item to its original; move large binaries to the artifact tier; re-tag if a release bundle was incomplete.

**Definition of Done:** Releases + archives + backups complete; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied.

**Next Step:** STEP-078 — Project completion audit.

---

## STEP-078 — Project Completion Audit  **[C][H]**  **GATE (Checklist 18)**

**Title:** Final project-wide completion audit (Checklist 18).

**Objective:** Verify every deliverable ([§1.12](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-final-deliverables)) exists and every gate has PASSed — source code, documentation, datasets, models, experiments, evaluation, writing, deployment readiness, presentation, backup, repository health, everything archived — via [Checklist 18](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-18--project-completion).

**Why this step exists:** [Checklist 18](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-18--project-completion) is the terminal gate confirming the project is truly complete, reproducible, and archived.

**Handbook References:** [Checklist 18](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-18--project-completion); [§1.12 Deliverables](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-final-deliverables); [§13.3 Audit Reports](MASTER_RESEARCH_OPERATING_SYSTEM.md#133-audit-reports); [A.5 DoD](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done).

**Prerequisites:** STEP-077 (releases + archives).

**Estimated Difficulty:** Medium.
**Estimated Time:** 1 day.
**Parallelizable:** No.

**Inputs:** Entire repository + all audits + all registries.

**Expected Outputs:** `project_completion_audit.md` = PASS confirming all deliverables + gates.

**Repository Changes:**
- *New:* `01_Project_Management/reviews/project_completion_audit.md`; final dashboard snapshot.

**Cursor Prompt:**
```
You are the Publication + Repository Auditors (final).
Using Checklist 18 + §1.12 + §13.3 ONLY: verify EVERY deliverable exists (source code, dataset pipeline, trained models, Experiment Registry, evaluation reports, explainability outputs, AI Forensic Analyst, React frontend, Django backend, REST API, thesis, journal manuscript, full documentation, deployment guide, user manual, developer manual) and that EVERY prior gate (Checklists 1-3,4,5,6,7,8,9,10,11,12,13,16,17,19) PASSed. Confirm reproducibility, repository health, and that everything is archived. Produce project_completion_audit.md (A.10) with PASS/FAIL per item.
```

**Google Antigravity Prompt:** *Optional — save the final audit + dashboard snapshot. No code beyond registry-validation/health-check scripts.*

**GitHub Expectations:** Branch `chore/completion-audit` → PR into `develop` → `main`. Commit `chore: final project completion audit (PASS)`.

**Kaggle Expectations:** None.

**Documentation Updates:** `project_completion_audit.md`; final `dashboard_status.md`.

**Verification Checklist (GATE — [Checklist 18](MASTER_RESEARCH_OPERATING_SYSTEM.md#checklist-18--project-completion)):**
- ✓ Every [§1.12](MASTER_RESEARCH_OPERATING_SYSTEM.md#112-final-deliverables) deliverable present.
- ✓ Every prior quality gate PASSed (documented).
- ✓ Reproducibility verified end to end; repository healthy; no [forbidden names](MASTER_RESEARCH_OPERATING_SYSTEM.md#24-repository-hygiene-rules).
- ✓ Everything archived; backups verified; `project_completion_audit.md` = PASS.

**Common Mistakes:** Declaring completion with an open gate; missing a deliverable; unverified reproducibility.

**Recovery Procedure:** For any FAIL, return to the owning step, fix, re-audit. The project is complete only when Checklist 18 fully PASSes.

**Definition of Done:** All deliverables + gates verified; **Checklist 18 = PASS**; [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done) satisfied. **Project complete.**

**Next Step:** *None — the roadmap is complete. Future work (v2.0 multimodal) begins a new cycle by registering new evidence collectors and fusion strategies ([Module 18](MASTER_RESEARCH_OPERATING_SYSTEM.md#module-18--future-modality-support)) without redesign.*

---

# FINAL REVIEW — ROADMAP VALIDATION RECORD

A complete self-review was performed against the required checks. Findings and resolutions:

## Coverage vs. Requested Stage Order
Every requested stage is present and in the mandated order: Research Foundation (001–007) → Literature Review (008–013) → Research Gap (014–017) → Dataset Discovery/Evaluation/Selection/Registration/Validation (018–024) → Preprocessing (025–029) → Repository Initialization + Environment Setup (split across 002–007 skeleton and 030–031 hardening, per handbook dependency order — see the [Ordering Note](#ordering-note-handbook-driven-reconciliation)) → FastAI Baseline (032–039) → Experiment System (035) → Training Pipeline (036) → Checkpoint System (037) → Evaluation Pipeline (042–050) → AI Forensic Analyst (051–059) → Backend (060–062) → Frontend (063–065) → Integration (066) → Testing (067) → Documentation (068) → Writing (069–072) → Thesis (073–074) → Journal (075–076) → Submission (074, 076) → Archival (077–078). **No stage skipped.**

## Dependency Check
- Each step's Prerequisites reference only earlier steps or handbook artifacts. No forward dependency exists.
- The repository skeleton + registries (002–006) precede all registration steps (011, 020, 040, etc.), resolving the literature-needs-a-home dependency.
- Environment hardening (030) + Kaggle sync (031) precede the first training run (039), which precedes evaluation (042) — no training before a validated, leakage-safe, versioned dataset (029).
- The Forensic Analyst (051–059) consumes a registered, evaluated model (040/050); the backend (060–062) consumes the Analyst (059); the frontend (063–065) consumes the API (062); writing (069–072) consumes evaluation (050) + analyst (059) + literature (017).

## Ordering / Duplicate-Work Check
- No duplicate steps: each registry, module, and gate is produced exactly once; iteration (experiments, ablations, generators, collectors) is handled by *re-running* the relevant loop with a new immutable ID, not by duplicate steps ([§5 M19](MASTER_RESEARCH_OPERATING_SYSTEM.md#5-model-development-operating-system), [§7.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#72-evaluation-principles-binding)).
- Gates appear at the exact handbook transition points ([§13.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#132-quality-gates)): Checklist 1 (007), 2 (017), 3 (024/029), 4 (029), 5 (035), 6 (040), 7 (039), 8 (050), 9 (059), 10 (065), 11 (062), 12 (068), 13 (072), 19 (073), 17 (074), 16 (075), 18 (078).

## Contradiction Check
- No step assigns implementation to Cursor or planning-authority to Antigravity; **Cursor plans/reviews, Antigravity implements** ([§10.1](MASTER_RESEARCH_OPERATING_SYSTEM.md#101-core-philosophy--platform-responsibilities)).
- No step requires local execution; all execution/training is on Kaggle ([§10.1](MASTER_RESEARCH_OPERATING_SYSTEM.md#101-core-philosophy--platform-responsibilities)).
- No step commits secrets, raw/processed images, or large binaries to Git ([A.6](MASTER_RESEARCH_OPERATING_SYSTEM.md#a6-canonical-storage--synchronization-policy)/[A.7](MASTER_RESEARCH_OPERATING_SYSTEM.md#a7-canonical-ignore-policy)); the AI never renders figures ([A.9](MASTER_RESEARCH_OPERATING_SYSTEM.md#a9-canonical-figure-policy)); the detector never decides ([§6.1](MASTER_RESEARCH_OPERATING_SYSTEM.md#61-architectural-principles)); irreversible scientific decisions are human ([§1.9](MASTER_RESEARCH_OPERATING_SYSTEM.md#19-human-in-the-loop-rule)).

## Completeness Check (per step)
- Every step includes all required fields: STEP ID, Title, Objective, Why, Handbook References, Prerequisites, Difficulty, Time, Parallelizable, Inputs, Expected Outputs, Repository Changes, Cursor Prompt, Google Antigravity Prompt (or an explicit "none/optional" with reason), GitHub Expectations, Kaggle Expectations, Documentation Updates, Verification Checklist, Common Mistakes, Recovery Procedure, Definition of Done, Next Step.
- Every step's Definition of Done references the universal [DoD A.5](MASTER_RESEARCH_OPERATING_SYSTEM.md#a5-canonical-definition-of-done).
- Every registry in [Appendix B](MASTER_RESEARCH_OPERATING_SYSTEM.md#appendix-b--registry-index) is created (006) and populated by an owning step; every [§14](MASTER_RESEARCH_OPERATING_SYSTEM.md#14-template-library) template is installed (005) and used downstream.

## Issues Found & Auto-Fixed During Review
1. **Repository-before-literature dependency** — resolved by bootstrapping the skeleton/registries in Part 1 and documenting the split in the [Ordering Note](#ordering-note-handbook-driven-reconciliation).
2. **Environment hardening placement** — placed at STEP-030/031 (just before training) rather than Day 1, matching [§10 Phase 16](MASTER_RESEARCH_OPERATING_SYSTEM.md#phase-16--environment-management) and avoiding premature lock against an unknown model.
3. **Unseen-generator dependency** — STEP-028 explicitly produces the leave-one-generator-out split so STEP-047 (E9) has its prerequisite.
4. **Evaluation-inputs-before-figures** — STEP-041 (M16) generates evaluation data before any figure spec, honoring [A.9](MASTER_RESEARCH_OPERATING_SYSTEM.md#a9-canonical-figure-policy).
5. **Claim experimental support** — STEP-015 leaves experiment/figure/table support empty; STEP-040/071 fill it, preventing forward references.
6. **Gate placement** — confirmed each QA checklist gates the correct transition per [§13.2](MASTER_RESEARCH_OPERATING_SYSTEM.md#132-quality-gates); no phase begins before its predecessor's gate PASSes.

**Result:** The roadmap is internally consistent, fully dependency-ordered, gate-complete, non-contradictory with the handbook, executable by one researcher via AI assistance across Cursor → Antigravity → GitHub → Kaggle → GitHub → Cursor, and requires no local execution.

---

*End of `PROJECT_EXECUTION_BLUEPRINT.md` — 78 sequential steps, Literature Review → Thesis → Journal → Archival. Governed by `MASTER_RESEARCH_OPERATING_SYSTEM.md` v1.0.0.*

