# Module Spec: PPMOD10 — Metadata Extraction

**Purpose:** Extract class, generator, identity, split, and demographic fields into a canonical row schema.  
**Single responsibility:** Metadata only (no pixel writes).

**Inputs:**
- Relative path + dataset_id + optional label CSVs
- Parameters: `label_source`, `require_*`, FairFace/DS0001 CSV paths

**Outputs:**
- Canonical fields: `dataset_id`, `relative_path`, `class_label`, `generator`, `condition`, `identity`, `split`, `age`, `gender`, `race` (nullable)
- Feeds `metadata/index.csv`

**Dependencies:** May share path/label inference rules with `17_Automation/dataset_eda/labels.py` (prefer import/reuse in STEP-026).

**Configuration:**
- DS0001: `metadata.csv`
- DS0002: path/zip → generator, condition, `id_*`
- DS0003: folder `real`/`fake`
- DS0004: RAISE vs synth generator folder
- DS0005: FairFace label CSVs (demographics); class=`real`

**Testing:**
- Unit: one fixture path per dataset_id → expected labels
- Unit: missing required identity on DS0002 → error (not silent empty) when `require_identity=true`
- Validation module: `PPMOD10V` — schema columns present; proportions reconcile with EDA within tolerance on smoke subset

**Future Extensions:** Bounding-box metadata; provenance hashes linking to integrity_report.

**Validation module:** `PPMOD10V`.
