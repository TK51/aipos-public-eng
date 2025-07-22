# folder_tree_scan.py

import os

def print_folder_tree(start_path='.', indent=''):
    try:
        entries = sorted(os.listdir(start_path))
    except Exception as e:
        print(f"Error accessing {start_path}: {e}")
        return

    for index, entry in enumerate(entries):
        full_path = os.path.join(start_path, entry)
        connector = '└── ' if index == len(entries) - 1 else '├── '
        print(indent + connector + entry)

        if os.path.isdir(full_path):
            next_indent = indent + ('    ' if index == len(entries) - 1 else '│   ')
            print_folder_tree(full_path, next_indent)

if __name__ == "__main__":
    root = os.getcwd()  # Automatically uses the folder where the script is dropped
    print(f"📁 Folder Tree for: {root}")
    print_folder_tree(root)


#python #osmodule #folderstructure #scripting #workflowdebugging #dataanalyst #reportingautomation #traceability

#aiposbuilt #fromukrainianswithlovetohumankind 🇺🇦
