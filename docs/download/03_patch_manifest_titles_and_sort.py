# 03_patch_manifest_titles_and_sort.py

import os
import json

# === CONFIGURATION ===
# This script patches human-friendly titles, sort order, and language markers into the manifest.
# Use "ua" to force Ukrainian version tags. Use "none" to preserve default language detection.
# === CONFIGURATION ===
MANIFEST_PATH = r"/home/t51/Documents/SIGNAL/aipos-public-eng-main-site/site_manifest.json"
BASE_FOLDER = os.path.dirname(MANIFEST_PATH)
LANGUAGE_VERSION = "none"  # Options: "ua", "none"
GA4_ID = "G-FCTN7560BJ"
HOMEPAGE = "https://tk51.github.io/aipos-public-eng/"

# === MANUAL TITLE + SORT MAP (by filename only, no extension) ===
manual_titles = [
    ("README", "README", 1),
    ("MIT-License", "MIT License", 2),
    ("NAMING-RULES", "Naming Rules", 3),
    ("TRAINING-GUIDE", "Training Guide", 4),
    ("aipos-command-and-settings-reference", "Command + Settings Reference", 5),
    ("aipos-interpreter", "AIPOS Interpreter", 6),
    ("aipos-method-card", "Method Card Template", 7),
    ("aipos-mobile-version-guide", "Mobile Guide", 8),
    ("aipos-made-by", "Made By", 99),
    ("aipos-cfg-base-cynical", "Config: Base Cynical", 10),
    ("aipos-cfg-minimal", "Config: Minimal", 11),
    ("01-triggerless-closure", "Method 1 — Triggerless Closure", 101),
    ("02-ev-infra-mismatch", "Method 2 — EV Infra Mismatch", 102),
    ("03-feedback-loop-death", "Method 3 — Feedback Loop Death", 103),
    ("04-method-cardiac-imaging-relay", "Method 4 — Cardiac Imaging Delay", 104),
    ("05-postop-ux-followup", "Method 5 — Post-Op UX Follow-Up", 105),
]

# Build lookup dictionary keyed by base filename (no extension)
title_sort_map = {fn: {"title": title, "sort": sort} for fn, title, sort in manual_titles}

# === STEP 1: LOAD EXISTING MANIFEST ===
if not os.path.exists(MANIFEST_PATH):
    raise FileNotFoundError(f"[ERROR] Cannot find manifest: {MANIFEST_PATH}")

with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
    manifest = json.load(f)

# === STEP 2: PATCH TITLES, SORT, AND LANGUAGE ===
patched, auto_fallback = 0, 0
for entry in manifest:
    fname = entry["filename"]
    base_name = os.path.splitext(fname)[0]

    # Title/sort from map
    if base_name in title_sort_map:
        entry.update(title_sort_map[base_name])
        patched += 1
    else:
        # Fallback label (if not defined manually)
        entry.setdefault("title", base_name.replace("-", " ").title())
        entry.setdefault("sort", 999)
        auto_fallback += 1

    # Language patching
    lang_flag = entry.get("lang", "none")
    if lang_flag == "none":
        if "-ua" in fname:
            entry["lang"] = "ua"
        elif "-en" in fname:
            entry["lang"] = "en"
        elif LANGUAGE_VERSION != "none":
            entry["lang"] = LANGUAGE_VERSION

# === STEP 3: SAVE MANIFEST BACK ===
with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

# === STEP 4: SUMMARY REPORT ===
print(f"✅ Patched {patched} entries with manual title/sort.")
if auto_fallback:
    print(f"➕ Applied fallback titles to {auto_fallback} file(s) (unlisted in map).")
print(f"🌐 Language set to: {LANGUAGE_VERSION} (if not detected from filename)")
print(f"📄 Manifest updated at: {MANIFEST_PATH}")
