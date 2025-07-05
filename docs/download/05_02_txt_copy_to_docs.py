# 05_02_txt_copy_to_docs.py

import os
import shutil
from pathlib import Path

# === CONFIG ===
BASE_PATH = Path("/home/t51/Documents/SIGNAL/aipos-public-eng-main-site/aipos-public-eng-main")
ALT_PATH = BASE_PATH / "signal-methods"
DEST_FOLDER = BASE_PATH / "docs" / "download"
DEST_FOLDER.mkdir(parents=True, exist_ok=True)

# === FILE PATTERNS (.txt wildcards supported)
file_patterns = [
    "aipos-cfg-base-cynical.txt",
    "aipos-cfg-minimal.txt",
    "01-*.txt",
    "02-*.txt",
    "03-*.txt",
    "04-*.txt",
    "05-*.txt"
]

copied_files = []
missing_patterns = []

# === COPY .txt FILES FROM MAIN + ALT PATH ===
for pattern in file_patterns:
    matches = list(BASE_PATH.glob(pattern)) + list(ALT_PATH.glob(pattern))
    if matches:
        for path in matches:
            dest_path = DEST_FOLDER / path.name
            shutil.copy2(path, dest_path)
            copied_files.append(path.name)
    else:
        missing_patterns.append(pattern)

# === COPY RAW .py TOOL FILES FROM SAME DIR AS THIS SCRIPT ===
SCRIPT_DIR = Path(__file__).parent
py_matches = list(SCRIPT_DIR.glob("[0-9][0-9]_*.py"))

if py_matches:
    for path in py_matches:
        dest_path = DEST_FOLDER / path.name
        shutil.copy2(path, dest_path)
        copied_files.append(path.name)
else:
    missing_patterns.append("[0-9][0-9]_*.py")

# === FINAL REPORT ===
print("\n✅ COPY COMPLETE — FINAL FILE LOCATIONS:\n")
print("/docs/download/")
for fname in sorted(set(copied_files)):
    print(f"  - {fname}")

if missing_patterns:
    print("\n⚠️  PATTERNS WITH NO MATCHES:")
    for pattern in sorted(missing_patterns):
        print(f"  - {pattern}")
