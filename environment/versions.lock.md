# Environment version lock (Phase 16 / STEP-030)

**Locked:** 2026-09-01  
**Owner:** DevOps / Automation Agent  
**Policy:** Pin to the **current Kaggle GPU runtime**. Do not upgrade in-place; a stack change is a new lock row + a new experiment `config.yaml` (Phase M4).

---

## Kaggle image (source of truth)

| Field | Value |
|-------|-------|
| Image | `gcr.io/kaggle-gpu-images/python` (`gcr.io/kaggle-private-byod/python:v170`) |
| Release | [Kaggle/docker-python **v170 GPU**](https://github.com/Kaggle/docker-python/releases/tag/bdf9e0538555f90453619adefb49ba40cfa136db44a9c9be7a42ea715c0aa068) (published 2026-06-29) |
| Digest | `bdf9e0538555f90453619adefb49ba40cfa136db44a9c9be7a42ea715c0aa068` |
| `BUILD_DATE` | `20260629-122508` |
| Colab tag | `release-colab-external-images_20260514-0600` |
| Python | **3.12** (`/usr/local/lib/python3.12/dist-packages`) |
| CUDA (pip) | `nvidia-cuda-nvcc-cu12==12.8.93` → treat as **CUDA 12.8** |
| `CUDA_HOME` | `/usr/local/cuda` |
| OS | Ubuntu 22.04 (from v170 dpkg base) |

Default Kaggle PyTorch build: **`torch==2.10.0+cu128`** ([docker-python#1546](https://github.com/Kaggle/docker-python/issues/1546)).  
Companion: `torchvision==0.25.0`. FastAI on this stack: **`fastai==2.8.7`** (`torch<3`, compatible with 2.10; `fastcore==1.12.42` is on v170).

### GPU note

| Accelerator | Status |
|-------------|--------|
| Tesla T4 (sm_75) | Supported by default `+cu128` |
| Tesla P100 (sm_60) | **Not** supported by `2.10.0+cu128`. Do not use P100 for locked experiments. If Kaggle assigns P100, stop and re-queue for T4; do not silently switch CUDA wheels. |

---

## Pinned versions

| Component | Version | Where |
|-----------|---------|--------|
| Python | 3.12 | Kaggle image |
| PyTorch | 2.10.0 (`+cu128` on Kaggle) | image / `requirements.txt` |
| torchvision | 0.25.0 | image / `requirements.txt` |
| FastAI | 2.8.7 | `requirements.txt` (matches torch 2.10) |
| fastcore | 1.12.42 | Kaggle v170 pip freeze |
| fasttransform | 0.0.2 | FastAI 2.8.7 dependency |
| NumPy | 2.0.2 | Kaggle v170 pip freeze |
| CUDA | 12.8 | Kaggle v170 |

Local GPU install (do not use on Kaggle):

```bash
pip install torch==2.10.0 torchvision==0.25.0 --index-url https://download.pytorch.org/whl/cu128
pip install -r environment/requirements.txt
```

---

## Files

| File | Role |
|------|------|
| `environment/requirements.txt` | Local/CI pins (exact `==`) |
| `environment/environment.yml` | Conda wrapper → same pins |
| `environment/kaggle-requirements.txt` | **Only** packages missing from v170 (currently none) |
| `environment/versions.lock.md` | This record |

---

## Experiment config (Phase M4)

Every `06_Experiments/EXPxxxx/config.yaml` must record:

- `git_commit` (full SHA of the trained code)
- `python`, `torch`, `fastai`, `cuda` copied from this lock
- `kaggle_image: v170` (or the new image if this file is updated)

Never edit a lock *after* an experiment has used it. Bump by appending a new dated section here and giving later experiments the new values.

---

## Smoke check (Kaggle GPU)

Run at the top of the first training notebook (Internet off is fine):

```python
import sys, torch, fastai, fastcore, numpy
print("python", sys.version.split()[0])
print("torch", torch.__version__, "cuda", torch.version.cuda, "avail", torch.cuda.is_available())
print("fastai", fastai.__version__, "fastcore", fastcore.__version__)
print("numpy", numpy.__version__)
assert torch.cuda.is_available(), "GPU not visible"
assert sys.version_info[:2] == (3, 12)
x = torch.zeros(2, device="cuda").sum()  # fails on P100+cu128
print("ok", float(x))
```

Record stdout in the experiment log. If versions drift from this file, **stop**, update the lock, and start a new `EXP`.

---

## Change log

| Date | Change |
|------|--------|
| 2026-09-01 | Initial lock to Kaggle GPU **v170** (STEP-030). |
