# 06_scan_folders_for_content.py

import os

BASE_FOLDER = r"/home/t51/Documents/SIGNAL/aipos-public-eng-main-site/aipos-public-eng-main/docs"

def build_folder_tree(base_folder):
    tree = []
    for root, dirs, files in os.walk(base_folder):
        level = root.replace(base_folder, '').count(os.sep)
        indent = '   ' * level
        tree.append(f"{indent}📁 {os.path.basename(root)}/")
        subindent = '   ' * (level + 1)
        for f in sorted(files):
            tree.append(f"{subindent}📄 {f}")
    return "\n".join(tree)

print(build_folder_tree(BASE_FOLDER))
