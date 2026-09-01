#!/usr/bin/env python3
import sys
import zipfile
from pathlib import Path

zip_path = Path(sys.argv[1])
forbidden = set("'\"?*:<>|#%\\")
bad = []
with zipfile.ZipFile(zip_path) as zf:
    for name in zf.namelist():
        if any(ch in name for ch in forbidden) or any(ord(ch) > 127 for ch in name):
            bad.append(name)
print(f"entries: {len(zf.namelist())}")
print(f"bad entries: {len(bad)}")
for n in bad[:10]:
    print(n)
