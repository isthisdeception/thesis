# 04_Preprocessing/specs

Template-17-style module specifications for Phase D9 (STEP-025).  
Implementation is **STEP-026** — these files are design-only.

| Spec | Module |
|------|--------|
| `PPMOD01_image_verification_spec.md` | Image verification |
| `PPMOD02_face_detection_spec.md` | Face detection |
| `PPMOD03_face_alignment_spec.md` | Face alignment |
| `PPMOD04_cropping_spec.md` | Cropping |
| `PPMOD05_resize_spec.md` | Resize |
| `PPMOD06_normalization_spec.md` | Normalization |
| `PPMOD07_quality_filtering_spec.md` | Quality filtering |
| `PPMOD08_artifact_removal_spec.md` | Artifact removal (junk only) |
| `PPMOD09_format_conversion_spec.md` | Format conversion |
| `PPMOD10_metadata_extraction_spec.md` | Metadata extraction |
| `FASTAI_DATABLOCK_SPEC.md` | Phase D13 FastAI DataBlock / transforms (config, not code) |

Design overview: `../design/PREPROCESSING_PIPELINE_DESIGN.md`  
Parameters: `../design/parameters_catalog.md`  
Canonical FastAI YAML: `../../05_Models/config/fastai_dataset.yaml`
