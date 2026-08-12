# Module Spec: PPMOD06 — Normalization

**Purpose:** Compute and optionally apply per-channel normalization statistics.  
**Single responsibility:** Normalization stats / apply — no geometry.

**Inputs:**
- RGB image(s) in [0,255] or [0,1] (document scale)
- Parameters: `norm_mode`, ImageNet mean/std, `dataset_stats_path`, `apply_on_disk`, `stats_sample_n`

**Outputs:**
- `normalization_stats.json` (always when mode needs dataset stats or reporting)
- Optionally float tensors written under `images/` if `apply_on_disk=true`
- Default recommendation: **`apply_on_disk=false`**; FastAI applies transforms from recorded stats/config

**Dependencies:** NumPy; optional torch.

**Configuration:** Default `norm_mode=imagenet`, `apply_on_disk=false`. Dataset-mode may sample `stats_sample_n=3000` stratified (reuse EDA seed policy).

**Testing:**
- Unit: ImageNet apply → known mean≈0 on fixture
- Unit: dataset stats deterministic with fixed seed + file list
- Validation module: `PPMOD06V` — stats finite; std > 0; mode enum validated

**Future Extensions:** Per-generator stats; frequency-domain normalization (research branch).

**Validation module:** `PPMOD06V`.
