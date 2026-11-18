from __future__ import annotations

import os
import sys
from pathlib import Path

import django

BACKEND_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_DIR.parent
FORENSIC_DIR = REPO_ROOT / "11_AI_Forensic_System"

for entry in (str(BACKEND_DIR), str(FORENSIC_DIR)):
    if entry not in sys.path:
        sys.path.insert(0, entry)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forensic_backend.settings")
django.setup()
