# 03_Datasets

**Purpose:** The Dataset Management System.

## Contents
Raw immutable originals, processed datasets, splits, metadata, reports, licenses.

## Workflow
Dataset agents write, Preprocessing and Experiments read. Never modify raw/.

## Owner
Dataset Agents / Human

## Related Folders
04_Preprocessing, 07_Evaluation

## Expected Outputs
datasets.csv, dataset_registry.csv, processed/DSxxxx_PPxxxx

> *This folder follows the canonical repository hygiene and naming rules defined in `MASTER_RESEARCH_OPERATING_SYSTEM.md`. Please refer to the handbook for full policy details.*

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
