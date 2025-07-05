# 01_scan_zip_and_generate_manifest.py

import os
import zipfile
import json
import fnmatch
from collections import defaultdict

# === CONFIGURATION ===
zip_path = r"/home/t51/Documents/SIGNAL/aipos-public-eng-main.zip"
zip_name = os.path.splitext(os.path.basename(zip_path))[0]
extract_to = os.path.join(os.path.dirname(zip_path), f"{zip_name}-site")

# === STAGE 1: UNZIP ===
if not os.path.isfile(zip_path):
    raise FileNotFoundError(f"[ERROR] ZIP file not found: {zip_path}")

print(f"[ZIP] Extracting ZIP to: {extract_to}")
os.makedirs(extract_to, exist_ok=True)
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to)
print(f"[SCAN] input_path set to: {extract_to}")

# === STAGE 1.5: Convert all .md files to .txt (in-place, recursive) ===
converted = 0
for root, dirs, files in os.walk(extract_to):
    for file in files:
        if file.lower().endswith(".md"):
            md_path = os.path.join(root, file)
            txt_path = os.path.splitext(md_path)[0] + ".txt"
            with open(md_path, "r", encoding="utf-8") as f_in, open(txt_path, "w", encoding="utf-8") as f_out:
                f_out.write(f_in.read())
            os.remove(md_path)
            print(f"[CONVERT] {file} → {os.path.basename(txt_path)}")
            converted += 1

print(f"[INFO] Markdown conversion complete: {converted} files converted.\n")

# === STAGE 1.75: AUTO-GENERATE README-TOOLS.MD IF .py TOOLS EXIST ===
tools_folder = os.path.join(extract_to, "aipos-public-eng-main", "tools")
readme_path = os.path.join(tools_folder, "README-tools.md")

if os.path.isdir(tools_folder):
    py_files = sorted([
        f for f in os.listdir(tools_folder)
        if f.lower().endswith(".py") and f.startswith("tools-")
    ])

    if py_files:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("# AIPOS Tools Folder\n\n")
            f.write("This section holds system-level scripts used to automate key actions in documentation and site generation.\n\n")
            f.write("**Tools list:**\n\n")
            for py in py_files:
                viewer_name = py.replace(".py", "-py-viewer.html")
                f.write(f'- <a href="{viewer_name}">{py}</a>\n')
            f.write("\n---\n\n🛠️ More under construction…\n")

        print(f"✅ README-tools.md generated at: {readme_path}")
    else:
        print("ℹ️ tools folder exists, but no tools-*.py files found. Skipping README generation.")
else:
    print("ℹ️ tools folder not found. Skipping README generation.")

# === STAGE 2: RESCAN ALL FILES TO BUILD MANIFEST ===
manifest = []

core_doc_patterns = [
    "readme.*",
    "training-guide.*",
    "mit-license*",
    "naming-rules.*",
    "aipos-command-and-settings-reference.*",
    "aipos-interpreter.*",
    "aipos-made-by.*",
    "aipos-method-card.*",
    "aipos-mobile-version-guide.*"
]

for root, dirs, files in os.walk(extract_to):
    for file in files:
        full_path = os.path.join(root, file)
        rel_path = os.path.relpath(full_path, extract_to)
        ext = os.path.splitext(file)[1].lower()
        base_name = os.path.splitext(file)[0].lower()
        lang = "ua" if "-ua" in base_name else "en" if "-en" in base_name else "none"

        if ext in [".jpg", ".jpeg", ".png", ".pdf"]:
            target = "visuals"
            download = True
            viewer = False

        elif ext == ".py":
            target = "tools"
            download = True
            viewer = True

        elif base_name.startswith("aipos-cfg-"):
            target = "configs"
            download = True
            viewer = True

        elif base_name.startswith(tuple([f"{i:02d}" for i in range(1, 10)])):
            target = "methods"
            download = True
            viewer = True

        elif base_name == "readme" and ext in [".txt", ".md"]:
             target = "tools"
             download = False
             viewer = True

        elif any(fnmatch.fnmatch(file.lower(), pattern) for pattern in core_doc_patterns):
            target = "core-docs"
            download = False
            viewer = True

        else:
            target = "other"
            download = False
            viewer = False

        manifest.append({
            "filename": file,
            "rel_path": rel_path.replace("\\", "/"),
            "ext": ext,
            "lang": lang,
            "target_folder": target,
            "download": download,
            "build_viewer": viewer
        })

# === STAGE 3: SAVE MANIFEST ===
manifest_path = os.path.join(extract_to, "site_manifest.json")
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

# === STRUCTURED SUMMARY ===
folder_map = defaultdict(list)
for entry in manifest:
    folder_map[entry["target_folder"]].append(entry["filename"])

print("\n📂 Site Manifest Summary (Build Targets):")
for folder in sorted(folder_map.keys()):
    print(f"\n🗂️ {folder}/")
    for fname in sorted(folder_map[folder]):
        print(f"   └── {fname}")

print(f"\n✅ site_manifest.json created at:\n{manifest_path}")

