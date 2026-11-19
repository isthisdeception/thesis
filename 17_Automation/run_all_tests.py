"""STEP-067 Consolidated Cross-Tier Test Runner (§8.9).

Runs:
1. AI Forensic Analyst unit/integration tests (`11_AI_Forensic_System`)
2. Django Backend unit/API/HTTP integration/smoke/regression tests (`13_Backend`)
3. React Frontend component/page/regression Vitest suites + Vite production build (`12_Web`)
4. Live cross-tier React-to-Django integration (`17_Automation/verify_integration.py`)
5. Live 6-scenario UAT suite (`17_Automation/run_uat.py`)
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
NPX = "npx.cmd" if os.name == "nt" else "npx"
NPM = "npm.cmd" if os.name == "nt" else "npm"


def _run(label: str, cmd: list[str], cwd: Path) -> bool:
    print(f"\n=== [{label}] {' '.join(cmd)} (cwd={cwd.relative_to(REPO_ROOT) if cwd != REPO_ROOT else '.'}) ===")
    proc = subprocess.run(cmd, cwd=str(cwd), check=False)
    ok = proc.returncode == 0
    print(f"=== [{label}] {'PASS' if ok else f'FAIL (code {proc.returncode})'} ===")
    return ok


def main() -> int:
    checks = [
        ("11_AI_Forensic_System (pytest)", [PY, "-m", "pytest", "-q"], REPO_ROOT / "11_AI_Forensic_System"),
        ("13_Backend (manage.py check)", [PY, "manage.py", "check"], REPO_ROOT / "13_Backend"),
        ("13_Backend (pytest)", [PY, "-m", "pytest", "-q"], REPO_ROOT / "13_Backend"),
        ("12_Web (vitest)", [NPM, "test"], REPO_ROOT / "12_Web"),
        ("12_Web (vite build)", [NPM, "run", "build"], REPO_ROOT / "12_Web"),
        ("Live Cross-Tier Integration", [PY, "17_Automation/verify_integration.py"], REPO_ROOT),
        ("Automated UAT (6 scenarios)", [PY, "17_Automation/run_uat.py"], REPO_ROOT),
    ]
    all_ok = True
    for label, cmd, cwd in checks:
        if not _run(label, cmd, cwd):
            all_ok = False
    print(f"\nOVERALL SUITE STATUS: {'PASS' if all_ok else 'FAIL'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
