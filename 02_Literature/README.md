# 02_Literature

**Purpose:** The Literature Intelligence System.

## Contents
Papers, summaries, metadata, indexes, research gaps, claims, search history, trends, drafts.

## Workflow
Literature agents write, Writing system consumes. No renaming PDFs to titles allowed.

## Owner
Literature Agents / Human

## Related Folders
09_Writing_Operating_System

## Expected Outputs
papers.csv, claim_database.csv, summaries/Pxxxx_summary.md, indexes/*.csv

## Searchable Indexes & Relationship Graph
Generated deterministically via `python 17_Automation/literature_indexer.py`:
- `indexes/keyword_index.csv`: 104 indexed keywords mapped to paper IDs
- `indexes/author_index.csv`: 108 indexed authors mapped to paper IDs
- `indexes/venue_index.csv`: 22 publication venues mapped to paper IDs
- `indexes/dataset_index.csv`: 31 datasets mapped to paper IDs
- `indexes/model_index.csv`: 44 model architectures mapped to paper IDs
- `indexes/citation_network.csv`: 118 relationship edges (`cross_reference`, `same_research_group`, `same_dataset`)

> *This folder follows the canonical repository hygiene and naming rules defined in `MASTER_RESEARCH_OPERATING_SYSTEM.md`. Please refer to the handbook for full policy details.*

## Cross-Linked Agents

The following agents operate within this domain:
- [Literature Search](../../19_Prompts/agents/literature/literature_search.md)
- [Paper Registration](../../19_Prompts/agents/literature/paper_registration.md)
- [Metadata Extraction](../../19_Prompts/agents/literature/metadata_extraction.md)
- [Paper Summary](../../19_Prompts/agents/literature/paper_summary.md)
- [Relationship](../../19_Prompts/agents/literature/relationship.md)
- [Research Gap](../../19_Prompts/agents/literature/research_gap.md)
- [Trend Analysis](../../19_Prompts/agents/literature/trend_analysis.md)
- [Research Planning](../../19_Prompts/agents/literature/research_planning.md)
- [Citation Verification](../../19_Prompts/agents/literature/citation_verification.md)
- [Knowledge Base](../../19_Prompts/agents/literature/knowledge_base.md)
