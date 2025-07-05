# 05_01_site_files_sort_and_zip.py

import os
import shutil
from pathlib import Path
from collections import defaultdict

# === CONFIG ===
SRC_FOLDER = Path(r"/home/t51/Documents/SIGNAL/aipos-public-eng-main-site/viewer")
DEST_ROOT = Path(r"/home/t51/Documents/SIGNAL/aipos-public-eng-main-site/aipos-public-eng-main/docs")

DEST_SUBFOLDERS = {
    "configs": DEST_ROOT / "configs",
    "methods": DEST_ROOT / "methods",
    "core-docs": DEST_ROOT / "core-docs",
    "visuals": DEST_ROOT / "visuals",
    "tools": DEST_ROOT / "tools"
}

# === LANGUAGE CONFIG ===
LANGUAGE_VERSION = "none"  # Use "ua" for Ukrainian; "none" = English default
lang_suffix = "en" if LANGUAGE_VERSION == "none" else LANGUAGE_VERSION

# === PREP DESTINATION FOLDERS ===
for path in DEST_SUBFOLDERS.values():
    path.mkdir(parents=True, exist_ok=True)

# === MOVE FILES + TRACK ===
moved_files = defaultdict(list)

for file in SRC_FOLDER.glob("*-viewer.html"):
    fname = file.name.lower()

    if "-jpg-viewer" in fname or "-jpeg-viewer" in fname or "-png-viewer" in fname:
        target_key = "visuals"

    elif fname.startswith("aipos-cfg-"):
        target_key = "configs"

    elif "-py-viewer" in fname or fname.startswith("readme-tools-md-viewer"):
        target_key = "tools"

    elif "-txt-viewer" in fname and fname[:2] in {"01", "02", "03", "04", "05"}:
        target_key = "methods"

    elif "qr-code" in fname or f"method-card-{lang_suffix}" in fname:
        target_key = "visuals"

    else:
        target_key = "core-docs"

    # Move HTML viewer
    dest_folder = DEST_SUBFOLDERS[target_key]
    shutil.copy2(file, dest_folder / file.name)
    moved_files[target_key].append(file.name)

        # === PATCH: If it's a .py-viewer, also move the raw .py source ===
    if target_key == "tools" and "-py-viewer" in fname:
        raw_name = file.name.replace("-py-viewer.html", ".py")

        # 1st: check viewer/
        raw_path = SRC_FOLDER / raw_name

        # 2nd: fallback root folder
        if not raw_path.exists():
            raw_path = DEST_ROOT.parent / raw_name

        # 3rd: fallback /tools/ folder
        if not raw_path.exists():
            raw_path = DEST_ROOT.parent / "tools" / raw_name

        if raw_path.exists():
            shutil.copy2(raw_path, dest_folder / raw_name)
            moved_files[target_key].append(raw_name)
        else:
            print(f"⚠️ Raw .py file missing for: {file.name}")


# === FINAL REPORT (GROUPED FORMAT) ===
print("\n✅ MOVE COMPLETE — FINAL FILE LOCATIONS:\n")
for folder in DEST_SUBFOLDERS.keys():
    print(f"/docs/{folder}/")
    for fname in sorted(moved_files.get(folder, [])):
        print(f"  - {fname}")
    print()
