# STEP-032 — Candidate Model Discovery

**Status:** COMPLETE (recommended shortlist approved)  
**Handbook:** Phase M1; DEF-002

## Output created
- [x] `05_Models/candidate_models.csv` populated with ranked, FastAI-oriented candidates
- [x] Kaggle feasibility, explainability support, and generalization notes recorded
- [x] DEF-002 remains open; no backbone finalized

## Recommended shortlist
1. `MODEL0001` — ResNet-50
2. `MODEL0002` — Xception
3. `MODEL0003` — EfficientNet-B4

## Hold for later
- `MODEL0004` — ViT-B/16 (use as transformer comparator after CNN baselines)
- `MODEL0005` — ResNet-101 (strong extension candidate, not the cheapest first baseline)
- `MODEL0006` — DenseNet-121 (lightweight fallback)
- `MODEL0007` — GLFNet (interesting explainability profile, higher implementation risk)

## Approval outcome
Approved shortlist:
- `MODEL0001` — ResNet-50
- `MODEL0002` — Xception
- `MODEL0003` — EfficientNet-B4

DEF-002 remains open: this approves the baseline shortlist, not the final backbone decision.
