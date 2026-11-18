#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> None:
    backend_dir = Path(__file__).resolve().parent
    repo_root = backend_dir.parent
    forensic_dir = repo_root / "11_AI_Forensic_System"
    for entry in (str(backend_dir), str(forensic_dir)):
        if entry not in sys.path:
            sys.path.insert(0, entry)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forensic_backend.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
