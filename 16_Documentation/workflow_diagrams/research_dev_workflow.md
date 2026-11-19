# Multi-Platform Research & Development Workflow

Companion to [developer_guide.md](../developer_guide.md) and [§10 Platform Workflow](../../MASTER_RESEARCH_OPERATING_SYSTEM.md#10-github--kaggle--antigravity-workflow).

```mermaid
flowchart LR
    H["Human Lead (Scientific & Gate Approvals: DECxxxx, Checklists)"]
    C["Cursor (Architecture, Experiment Plans, Prompt Authoring)"]
    A["Antigravity (Implementation, Code, Tests, Docs, Registries)"]
    G["GitHub (Canonical Source of Truth: Branches, PRs, Releases)"]
    K["Kaggle GPU (Heavy Training, Inference, Robustness Runs via kaggle_sync)"]

    H -->|"Approves plans & gates"| C
    C -->|"Specs & step prompts"| A
    A -->|"Feature/experiment branches & tests"| G
    G -->|"Syncs verified code + configs"| K
    K -->|"Checkpoints, metrics, logs & artifacts"| G
    G -->|"Presents PRs & audit reports"| H
```

## Branching & Promotion Flow

```mermaid
flowchart TD
    M["main (protected canonical history)"] -->|"git checkout -b feature/... or docs/..."| B["Working Branch"]
    B -->|"Implement + run tests / checks"| T{"Verification & Audit PASS?"}
    T -->|"No"| B
    T -->|"Yes"| PR["Open Pull Request & Present Checklist Gate to Human"]
    PR -->|"Human confirms PASS"| MG["Merge into main & tag milestones/CHANGELOG"]
```
