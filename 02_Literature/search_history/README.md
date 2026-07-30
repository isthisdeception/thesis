# Search History Log Schema and Policies

Every search run must be documented in a new file in this directory (e.g., `2026-07-30_scholar_generalization.md`) to ensure perfect reproducibility (Phase L2).

## Log Entry Format
Copy and paste this template for every search run:

```markdown
**Date:** YYYY-MM-DD
**Source:** [e.g., Google Scholar, IEEE Xplore]
**Search String Used:** 
`[The exact string copied from the search bar]`

**Filters Applied:**
- **Year:** [e.g., >= 2020]
- **Venue/Quality:** [e.g., Top-tier CV/Security conferences only]
- **Citation Threshold:** [e.g., >= 10 for older papers, 0 for < 1 year old]

**Results:**
- **Total Result Count:** [e.g., 2,450]
- **Papers Selected for Intake:** [e.g., 5]

**Papers Selected (Title & DOI):**
1. [Paper Title] - [DOI/Link]
2. ...
```

## Filters and Priority Ranking (per §3.3)

### Mandatory Filters
1. **Year:** Prefer recent work (>= 2020) given the rapid evolution of GANs and diffusion models.
2. **Venue Quality:** Prioritize top-tier venues (CVPR, ICCV, ECCV, NeurIPS, ICLR, IEEE T-PAMI, ACM CCS, USENIX Security).
3. **Citation Threshold:** For papers older than 2 years, expect a minimum citation count (e.g., >20) unless published in a top-tier venue.
4. **Deduplication:** Before assigning a `Pxxxx` ID, normalize the title (lowercase, strip punctuation) and compare the DOI against the existing `papers.csv` registry.

### Priority Ranking Policy
Papers are objectively scored (0-5) across dimensions defined in Phase L2 / §3.3:
- Venue Quality
- Citation Impact
- Novelty
- Dataset Quality
- Evaluation Quality (cross-dataset testing is paramount for generalization)
- Reproducibility (Code Availability)
- Explainability
- External Validation
- Generalization

*Papers with higher aggregate scores dictate the priority reading order.*
