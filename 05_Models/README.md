# 05_Models

**Purpose:** Model definitions, the Model Registry, and exported inference models.

## Contents
Architecture definitions, model registries, model cards, export pointers.  
FastAI dataset-prep defaults (STEP-029 / Phase D13): `config/fastai_dataset.yaml`.  
FastAI training standard (STEP-034 / Phase M3): `FASTAI_TRAINING_STANDARD.md`.  
Training pipeline package (STEP-036 / Phase M6): `17_Automation/training/` — `run_experiment(config.yaml)` produces checkpoints, `export.pkl`, `weights.pth`, predictions, metrics, and learning-curve data under `06_Experiments/EXPxxxx/`.

## Workflow
Model/Training agents write, AI Forensic System consumes. No anonymous models.

## Owner
Model/Training Agents

## Related Folders
06_AI_Forensic_Analyst_Architecture

## Expected Outputs
candidate_models.csv, baseline_plan.md, model_registry.csv, model_card.md

> *This folder follows the canonical repository hygiene and naming rules defined in `MASTER_RESEARCH_OPERATING_SYSTEM.md`. Please refer to the handbook for full policy details.*

## Cross-Linked Agents

The following agents operate within this domain:
- [Model Discovery](../../19_Prompts/agents/model/model_discovery.md)
- [Training](../../19_Prompts/agents/model/training.md)
- [Checkpoint](../../19_Prompts/agents/model/checkpoint.md)
- [Experiment](../../19_Prompts/agents/model/experiment.md)
- [Evaluation Trigger](../../19_Prompts/agents/model/evaluation_trigger.md)
- [Failure Analysis](../../19_Prompts/agents/model/failure_analysis.md)
- [Registry](../../19_Prompts/agents/model/registry.md)
- [Comparison](../../19_Prompts/agents/model/comparison.md)
- [FastAI Configuration](../../19_Prompts/agents/model/fastai_configuration.md)
