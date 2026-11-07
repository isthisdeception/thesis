# STEP-037 — Checkpoint System

**Status:** COMPLETE — interruption/resume verified locally (CPU); Kaggle round trip (publish → new session → resume) still to be exercised at the first EXP0001 session  
**Handbook:** Phase M7; §10 Phase 8; Checklist 7; A.2

## Output created
- [x] `17_Automation/training/checkpoints.py`: `CheckpointStore` (atomic never-overwrite writes, SHA-256 manifest, quarantine, latest-valid-recovery lookup), RNG capture/restore
- [x] `EpochCheckpointer` rewritten: full-state recovery checkpoint every epoch (weights, optimizer, schedule position, run-wide epoch, RNG, best/early-stopping state, history); resumable early stopping
- [x] `run_experiment` resumes automatically; refuses completed runs, changed configs, and unmanifested files
- [x] A.2 names: `EXPxxxx_epoch_NNN.pth`, `EXPxxxx_best.pth`, `EXPxxxx_last.pth`, `MODELxxxx_export.pkl`, `MODELxxxx_weights.pth`; logs `EXPxxxx_<stage>_<time>.log`
- [x] `07_Checkpoints/checkpoint_policy.md`, `07_Checkpoints/EXP0001_checkpoints.md` (generated; empty until training)
- [x] `kaggle_sync resume-checkpoints` no longer deletes the target folder; it merges and refuses to overwrite differing files. Sync plan resume path aligned with the artifact dataset; `07_Checkpoints` added to metadata paths

## Checklist 7 — Checkpoint Integrity (verified by tests)

| Item | Evidence |
|------|----------|
| Best model | `EXPxxxx_best.pth` = byte copy of best recovery checkpoint (`test_manifest_checksums_verify`) |
| Last checkpoint | `EXPxxxx_last.pth` |
| Optimizer state | non-empty `opt` in every recovery checkpoint (`test_recovery_checkpoint_holds_full_state`) |
| Scheduler state | resumed LR per batch equals uninterrupted run (`test_resumed_schedule_matches_uninterrupted_run`) |
| Epoch | run-wide `epoch` + `phase_epoch` in state; resumed history continuous |
| Resume capability | `test_interrupted_run_resumes_without_overwriting`, `test_resume_quarantines_corrupt_latest_checkpoint` |
| Export model | `MODELxxxx_export.pkl` loads with `load_learner` |
| Version consistency | config SHA-256 in manifest + state; changed config refused (`test_resume_refuses_changed_config`) |
| Checksum | every manifest entry verified against file SHA-256 |

Tests: 90 passed with the pinned CPU stack (14 end-to-end training tests).

## Next step
**STEP-038** — Logging system.
