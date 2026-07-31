<!--
================================================================================
TEMPLATE NAME: Template 12 — Table Specification
PURPOSE: Comparison table of detection methods for related work.
WHEN USED: Literature review (STEP-017) and thesis writing.
OWNER: Literature Writer Agent
INPUTS: papers.csv, summaries (P0001–P0028)
OUTPUTS: TAB0001_spec.md (this file), TAB0001.csv (data), TAB0001.md (rendered)
REQUIRED SECTIONS: Table ID, Title, Source, Supporting experiment, Formatting, Consistency, Units
VALIDATION RULES: Every row traces to a registered Paper ID.
NAMING CONVENTION: TAB0001_spec.md
FOLDER LOCATION: 10_Tables/specs
DEFINITION OF DONE: Spec is clear and data source is identified.
COMMON MISTAKES: Missing units; including papers not in papers.csv.
RELATED TEMPLATES: Template 11 (Figure Specification)
================================================================================
-->

# Table Spec: TAB0001

**Title:** Comparison of AI-Generated Face Detection Methods

**Source:** `02_Literature/metadata/papers.csv` (papers P0002–P0023, excluding surveys and generation-only papers). Data extracted from structured summaries in `02_Literature/summaries/`.

**Supporting experiment:** None (literature-derived). To be updated with experimental results in STEP-042+.

**Purpose:** Provide a structured comparison of detection methods reviewed in the literature, organized by detection approach, generator coverage, evaluation methodology, and key capabilities. Supports the Related Work section and identifies the dimensions where existing methods fall short, motivating the forensic system design.

**Columns:**

| Column | Description | Data Type | Source |
|---|---|---|---|
| Paper ID | Canonical identifier | Text (Pxxxx) | papers.csv |
| Authors | First author et al. | Text | papers.csv |
| Year | Publication year | Integer | papers.csv |
| Method | Detection approach name/category | Text | summaries |
| Architecture | Model architecture used | Text | papers.csv |
| Feature Domain | Spatial / Frequency / Hybrid / Biometric / Reconstruction | Category | summaries |
| GAN Coverage | Which GAN architectures tested | Text | summaries |
| DM Coverage | Which diffusion models tested | Text | summaries |
| Cross-Generator | Yes / No / Partial | Category | summaries |
| Cross-Dataset | Yes / No | Category | summaries |
| Source Attribution | Yes / No / Partial | Category | summaries |
| Explainability | Inherent / Partial / Post-hoc / None | Category | summaries |
| Robustness Tested | Yes / No | Category | summaries |
| Best Reported Accuracy | Top accuracy/AUC (with conditions) | Text | summaries |
| Dataset Used | Evaluation dataset(s) | Text | papers.csv |
| Public Code | Yes / No / Unknown | Category | papers.csv |
| Public Dataset | Yes / No / Unknown | Category | papers.csv |

**Rows (detection methods only, excluding surveys P0024–P0028 and generation/privacy papers P0001, P0004, P0009, P0012, P0017, P0020, P0025):**

P0002, P0003, P0005, P0006, P0007, P0008, P0010, P0011, P0013, P0014, P0015, P0016, P0018, P0019, P0021, P0023

**Formatting:**
- Landscape orientation for thesis/journal inclusion.
- Alternating row shading for readability.
- Bold entries for critical-relevance papers.
- Footnotes for conditional metrics (e.g., "97%+ on proprietary dataset").
- Column headers abbreviated in rendered version with a legend.

**Consistency:**
- All Paper IDs from `papers.csv` (no hallucinated entries).
- Architecture names match papers.csv `Architecture` column.
- Dataset names match papers.csv `Dataset` column.
- Every cell traces to a specific summary or papers.csv field.

**Units:**
- Accuracy: percentage (%) or AUC (0–1 scale), specified per entry.
- Year: integer (YYYY).
- All other columns: categorical or text (no numerical units needed).

**Rendering Notes:**
- Data file: `10_Tables/data/TAB0001.csv`
- Rendered Markdown: `10_Tables/rendered/TAB0001.md`
- Both generated from this specification during implementation.

**Related Figures:** None currently. May link to FIG0001 (detection method taxonomy diagram) when created.

**Related Tables:** None currently.

**Update Trigger:** When a new detection-method paper is registered, add a row to TAB0001.csv and re-render TAB0001.md.
