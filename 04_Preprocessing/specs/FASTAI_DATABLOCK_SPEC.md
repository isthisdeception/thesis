# FastAI DataBlock Specification (Phase D13 / STEP-029)

**Status:** COMPLETE (design only — parameters live in config, not code)  
**Canonical config:** `05_Models/config/fastai_dataset.yaml`  
**Handbook:** Phase D13; experiment `config.yaml` (Phase M4 / Template 8)

This spec defines how a processed + split dataset becomes FastAI `DataLoaders`. Experiments **copy** these keys into `06_Experiments/EXPxxxx/config.yaml`. Training notebooks must read the config; they must not hardcode blocks, splits, sizes, augs, or stats.

---

## 1. DataBlock

| Parameter | Value | Notes |
|-----------|-------|-------|
| `blocks` | `ImageBlock`, `CategoryBlock` | Binary real/fake detection |
| `get_items` | `assignments.csv` rows | `03_Datasets/splits/{output}_{split}/assignments.csv` |
| `get_x` | `{processed_root}/{processed_path}` | `processed_path` is relative to the Kaggle processed dataset root |
| `get_y` | `class_label` | Values `fake` / `real` |
| `splitter` | column splitter on `partition` | `train` → train; `val` → valid; **never** `RandomSplitter` |
| `test` | `partition == test` | Built as `test_dl` after `dataloaders()`; not mixed into valid |
| `vocab` | `[fake, real]` | Fixed in config so fake-only (DS0002) and real-only (DS0005) eval sets keep both classes |

Equivalent FastAI construction (reference, not source of truth):

```text
DataBlock(
  blocks=(ImageBlock, CategoryBlock),
  get_items=load_assignment_paths,      # from assignments.csv
  get_x=lambda r: processed_root / r.processed_path,
  get_y=lambda r: r.class_label,
  splitter=FuncSplitter(lambda r: r.partition == "val"),
  item_tfms=Resize(224, method="squish"),
  batch_tfms=aug_transforms(...) + [Normalize.from_stats(imagenet_mean, imagenet_std)],
)
```

`ImageDataLoaders.from_df` with `valid_col` derived from `partition` is an allowed equivalent **if** every argument still comes from `config.yaml`.

---

## 2. Item / batch transforms

Processed images are already **224×224 RGB PNG** (`PPMOD05`, `keep_aspect=false`). Normalization was **not** written to disk (`PPMOD06` `apply_on_disk=false`).

| Stage | Transform | Config |
|-------|-----------|--------|
| `item_tfms` | `Resize(224, method=squish)` | Safety clamp; no extra crop |
| `batch_tfms` (train) | light `aug_transforms` | Forensic-preserving (see §3) |
| `batch_tfms` (valid/test) | **no** augs | Resize + Normalize only |
| `batch_tfms` (all) | `Normalize.from_stats` | ImageNet mean/std |

ImageNet stats (from `04_Preprocessing/reports/metadata/*/normalization_stats.json`):

- mean: `[0.485, 0.456, 0.406]`
- std: `[0.229, 0.224, 0.225]`

Do **not** recompute dataset mean/std unless a new `PPxxxx` sets `norm_mode=dataset`.

---

## 3. Augmentations (forensic-preserving)

Preprocessing rule: preserve generative artifacts; do not denoise or geometrically destroy frequency traces.

Default `aug_transforms` (train only):

| Key | Value | Why |
|-----|-------|-----|
| `do_flip` | `true` | Horizontal only |
| `flip_vert` | `false` | Faces are upright |
| `max_rotate` | `10` | Mild; avoids heavy resampling |
| `max_zoom` | `1.05` | Almost identity scale |
| `max_lighting` | `0.1` | Mild brightness/contrast |
| `max_warp` | `0.0` | Warp destroys local artifacts |
| `min_scale` | `1.0` | Disables random resized crop |
| `pad_mode` | `zeros` | Matches `keep_aspect=false` pipeline |

JPEG / blur / compression belong in **evaluation robustness (E8)**, not default training augs. Changing augs requires a new `EXPxxxx`, not an in-place config edit after a run.

---

## 4. Loader sizes

| Key | Default | Notes |
|-----|---------|-------|
| `image_size` | `224` | Matches every current `PP` |
| `batch_size` | `64` | Kaggle GPU default; drop to `32` on OOM |
| `batch_size_eval` | `128` | Valid/test |
| `num_workers` | `2` | Kaggle Linux; use `0` on Windows local |

---

## 5. Split binding (leakage-critical)

The splitter **is** the STEP-028 index. It is not recomputed at train time.

| Dataset | Standard split (train/eval) | LOGO / alternate (E9) |
|---------|-----------------------------|------------------------|
| DS0001 | `DS0001_PP0001_SPLIT0001` | `..._SPLIT0002` hold `stable_diffusion` |
| DS0002 | `DS0002_PP0002_SPLIT0001` (eval) | `..._SPLIT0002` hold `Midjourney` |
| DS0003 | `DS0003_PP0003_SPLIT0001` | `..._SPLIT0002` hold `stylegan` |
| DS0004 | `DS0004_PP0006_SPLIT0001` | `..._SPLIT0002` hold `dalle3` |
| DS0005 | `DS0005_PP0005_SPLIT0001` (bias eval) | `..._SPLIT0002` grouped random |

Rules:

1. `seed` in the experiment config must be recorded; split membership comes from the frozen index (`seed=42` at STEP-028).
2. Fail the run if `leakage_check.json` is missing or `"passed": false`.
3. DS0002 is **eval-only** (fake-only). DS0005 is **bias-eval** (real-only). Neither is a standalone binary training set.

---

## 6. Path resolution

On Kaggle:

```text
processed_root = /kaggle/input/<slug>/
item = processed_root / assignments.processed_path
```

Slugs: `05_Models/config/fastai_dataset.yaml` → `outputs[].processed_kaggle_slug`.  
Git never stores image bytes; indexes stay under `03_Datasets/splits/`.

---

## 7. What training code may not do

- `RandomSplitter` / `GrandparentSplitter` / folder-name splits
- Hardcoded `Resize`, `Normalize`, or `aug_transforms` arguments
- Inferring vocab from a one-class eval set
- Mixing `test` into `valid`
- Reading raw `03_Datasets/raw/` (processed + split only)
