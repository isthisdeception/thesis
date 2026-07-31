# 03_Datasets

**Purpose:** The Dataset Operating System (OS) for AI Digital Forensics.

## Phase Status
- **Phase D1 — Dataset Discovery (STEP-018):** `COMPLETED`
  - Registered 17 candidate datasets (`CAND0001`–`CAND0017`) in `03_Datasets/metadata/dataset_candidates.csv`.
  - Cover Kaggle, Hugging Face, GitHub, Zenodo, OpenML, VGG Oxford, TUM, and project sites.
  - Represent diverse generator families (Diffusion models: SD v1.4/1.5/2.1/XL, DALL-E 2/3, Midjourney v5, GLIDE, Firefly; GANs: ProGAN, StyleGAN, StyleGAN2, StyleGAN3, StarGAN, AttGAN; Swaps: Deepfakes, Face2Face, FaceSwap, NeuralTextures).
  - Licenses recorded at first sight; duplicates flagged (e.g. `CAND0011` -> `CAND0010`).

## Contents
Raw immutable originals (`raw/`), processed datasets (`processed/`), splits (`splits/`), metadata (`metadata/`), reports (`reports/`), licenses (`licenses/`).

## Workflow
Dataset agents write, Preprocessing and Experiments read. Never modify `raw/`.

## Owner
Dataset Discovery Agent / Dataset Evaluation Agent / Human

## Related Folders
`04_Preprocessing`, `07_Evaluation`, `02_Literature`

## Expected Outputs & Registries
- `03_Datasets/metadata/dataset_candidates.csv` (Phase D1)
- `03_Datasets/metadata/dataset_evaluation.csv` (Phase D2)
- `03_Datasets/metadata/datasets.csv` (Phase D3)
- `03_Datasets/metadata/dataset_registry.csv` (Phase D8)

> *This folder follows the canonical repository hygiene and naming rules defined in `MASTER_RESEARCH_OPERATING_SYSTEM.md` (§4).*

## Cross-Linked Agents
The following agents operate within this domain:
- [Discovery](../../19_Prompts/agents/dataset/discovery.md)
- [Evaluation](../../19_Prompts/agents/dataset/evaluation.md)
- [Metadata](../../19_Prompts/agents/dataset/metadata.md)
- [Validation](../../19_Prompts/agents/dataset/validation.md)
- [Quality](../../19_Prompts/agents/dataset/quality.md)
- [Preprocessing](../../19_Prompts/agents/dataset/preprocessing.md)
- [Split](../../19_Prompts/agents/dataset/split.md)
- [Statistics](../../19_Prompts/agents/dataset/statistics.md)
- [Documentation](../../19_Prompts/agents/dataset/documentation.md)
- [Registry](../../19_Prompts/agents/dataset/registry.md)
