# Literature Search Strategy: Templates

## Canonical Search String
**Base Template:** `("<core concept>") AND ("<modality>") AND ("<task>") AND ("<method family>")`

**Instantiated for STEP-008 Generalization Question:**
`("deepfake" OR "AI-generated" OR "synthetic") AND ("face" OR "facial") AND ("detection" OR "forensics" OR "generalization") AND ("GAN" OR "diffusion")`

## Source-Specific Implementations

### Google Scholar
`("deepfake" OR "AI-generated" OR "synthetic") AND ("face" OR "facial") AND ("detection" OR "forensics" OR "generalization") AND ("GAN" OR "diffusion")`
*Tip: Use Advanced Search to restrict to Year >= 2020.*

### IEEE Xplore
`("deepfake" OR "AI-generated" OR "synthetic") AND ("face" OR "facial") AND ("detection" OR "forensics" OR "generalization") AND ("GAN" OR "diffusion")`
*Tip: Use Metadata Only search to avoid full-text noise.*

### ACM Digital Library
`("deepfake" OR "AI-generated" OR "synthetic") AND ("face" OR "facial") AND ("detection" OR "forensics" OR "generalization") AND ("GAN" OR "diffusion")`

### Springer
`("deepfake" OR "AI-generated" OR "synthetic") AND ("face" OR "facial") AND ("detection" OR "forensics" OR "generalization") AND ("GAN" OR "diffusion")`

### ScienceDirect
`("deepfake" OR "AI-generated" OR "synthetic") AND ("face" OR "facial") AND ("detection" OR "forensics" OR "generalization") AND ("GAN" OR "diffusion")`

### CVF Open Access (CVPR / ICCV / WACV)
Keyword search may require simpler combinations due to interface limitations:
`deepfake face detection generalization` OR `diffusion face forensics`

### OpenReview
`("deepfake" OR "AI-generated") AND ("face" OR "facial") AND ("detection" OR "generalization") AND ("GAN" OR "diffusion")`

### arXiv
Use Advanced Search with Title/Abstract fields:
`deepfake OR AI-generated OR synthetic` (AND) `face OR facial` (AND) `detection OR forensics OR generalization` (AND) `GAN OR diffusion`

## Keyword Evolution Rule
New keywords harvested from collected papers (titles, keyword sections, method names) MUST be appended to `../keywords.csv` with their source specified as the `Paper ID` (e.g., `P0015`). This ensures the search vocabulary organically evolves from the literature itself.
