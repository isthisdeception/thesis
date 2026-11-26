# Claim: CLAIM0009

**Statement:** Uncalibrated binary synthetic-face detectors suffer severe overconfidence, threshold-shift collapse, and precision-recall cliffs under domain shift; explicit uncertainty calibration, OOD verification, and abstention reduce silent forensic errors.  
**Supporting Evidence:** Literature papers: P0029, P0030, P0031, P0032, P0036, P0037, P0040, P0043 (P0030: Tables 1–6; P0031: Section V-B; P0032: Table 1; P0036: Table 13 DDPM score shift; P0040: Section 4.3; P0043: Section 7); Experiments: EXP0001, EXP0002; Evaluations: EVAL0001, EVAL0007 (`FIG0011`, `FIG0028`).  
**Contradicting Evidence:** Even calibrated ensembles (P0030) exhibit 6–10x ECE degradation under severe compression/blur shifts, and naive confidence cutoffs (80%–85% in P0031) collapse recall to 18% unless paired with multi-dimensional confidence and structured abstention.  
**Confidence:** Very High  
**Status:** verified  

---

## Detailed Context & Grounding

- **Primary Source Papers:** P0029, P0030, P0031, P0032, P0036, P0037, P0040, P0043
- **Experimental Evidence:** EXP0001, EXP0002, EVAL0001 (ECE 0.0525, MCE 0.1544), EVAL0007 (16 scenarios, E14-10 safety override)
- **Supporting Figures/Tables:** FIG0011, FIG0028, TAB0001
