# 09_zip_docs_and_scan_folder.py

import os
import zipfile

# === CONFIGURATION ===
SOURCE_FOLDER = r"/home/t51/Documents/SIGNAL/aipos-public-eng-main-site/aipos-public-eng-main/docs"
ZIP_TARGET = r"/home/t51/Documents/SIGNAL/aipos-public-eng-main-site/docs.zip"

def zip_folder(source_dir, output_zip_path):
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                arcname = os.path.relpath(abs_path, start=source_dir)
                zipf.write(abs_path, arcname)
    print(f"\n✅ Zipped to: {output_zip_path}")

def print_zip_tree(zip_path):
    if not os.path.isfile(zip_path):
        print("❌ Zip file not found.")
        return

    print("\n📦 Archive Contents:")
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        file_tree = {}

        # Build nested dict structure from zip paths
        for path in zipf.namelist():
            if path.endswith("/"):  # Skip if it's a folder entry
                continue
            parts = path.strip("/").split("/")
            cursor = file_tree
            for part in parts[:-1]:
                cursor = cursor.setdefault(part, {})
            cursor.setdefault(parts[-1], None)

        # Walk dict tree and print indented structure
        def walk_tree(tree, indent=""):
            for key in sorted(tree):
                if tree[key] is None:
                    print(f"{indent}📄 {key}")
                else:
                    print(f"{indent}📁 {key}/")
                    walk_tree(tree[key], indent + "   ")

        walk_tree(file_tree)

if __name__ == "__main__":
    if not os.path.exists(SOURCE_FOLDER):
        raise FileNotFoundError(f"Source folder not found: {SOURCE_FOLDER}")
    zip_folder(SOURCE_FOLDER, ZIP_TARGET)
    print_zip_tree(ZIP_TARGET)
