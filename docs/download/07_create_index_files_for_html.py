# 07_generate_html_indexes.py

import os
import json
from pathlib import Path

# === CONFIGURATION ===
MANIFEST_PATH = r"/home/t51/Documents/SIGNAL/aipos-public-eng-main-site/site_manifest.json"
BASE_FOLDER = os.path.dirname(MANIFEST_PATH)
VIEWER_OUTPUT_FOLDER = os.path.join(BASE_FOLDER, "viewer")
GA4_ID = "G-FCTN7560BJ"
HOMEPAGE = "https://tk51.github.io/aipos-public-eng/"
OUTPUT_TEMPLATE = "index.html"

# === HTML TEMPLATE ===
HTML_HEAD = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{{title}} — AIPOS</title>
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA4_ID}');
  </script>
  <style>
    body {{
      font-family: system-ui, sans-serif;
      background: #f9f9f9;
      color: #222;
      padding: 1rem;
      font-size: 16px;
      line-height: 1.6;
    }}
    h1 {{
      font-size: 1.5rem;
      border-bottom: 2px solid #ccc;
      padding-bottom: 0.5rem;
      margin-bottom: 1rem;
    }}
    ul {{ padding-left: 1.25rem; }}
    li {{ margin-bottom: 0.75rem; }}
    a {{
      color: #1a73e8;
      text-decoration: none;
      font-weight: 500;
    }}
    a:hover {{ text-decoration: underline; }}
    .nav {{
      margin-bottom: 1.5rem;
    }}
    .nav-button {{
      display: inline-block;
      margin-right: 1rem;
      padding: 0.4rem 0.8rem;
      background-color: #e0e0e0;
      border-radius: 4px;
      text-decoration: none;
      color: #222;
      font-weight: 500;
      font-size: 0.95rem;
    }}
    .nav-button:hover {{
      background-color: #ccc;
    }}
    .footer {{
      margin-top: 2rem;
      font-size: 0.8rem;
      color: #888;
      border-top: 1px solid #ccc;
      padding-top: 0.5rem;
    }}
    @media (prefers-color-scheme: dark) {{
      body {{
        background: #0d1117;
        color: #c9d1d9;
      }}
      .nav-button {{
        background-color: #21262d;
        color: #c9d1d9;
      }}
      .nav-button:hover {{
        background-color: #30363d;
        color: inherit;
      }}
      .footer {{
        border-top: 1px solid #333;
        color: #777;
      }}
      a {{
        color: #58a6ff;
      }}
    }}
  </style>
</head>
<body>
<div class="nav">
  <a class="nav-button" href="{HOMEPAGE}" onclick="gtag('event', 'nav_click', {{ 'type': 'home' }});">⌂ Home</a>
</div>
"""

HTML_FOOTER = """
<div class="footer">
  {folder}/ folder • Files for mobile-safe viewing and download • Built by Kay • GA4 Tracked
</div>
</body>
</html>
"""

# === LOAD MANIFEST ===
with open(MANIFEST_PATH, encoding="utf-8") as f:
    manifest = json.load(f)

manifest_lookup = {item["filename"]: item for item in manifest}

# === INDEX GENERATOR ===
generated_indexes = []

# === INDEX GENERATOR (RAW STYLE) ===
generated_indexes = []

def generate_index_for_folder(subfolder_path: Path):
    section = subfolder_path.name
    viewer_files = sorted(subfolder_path.glob("*-viewer.html"))

    if not viewer_files:
        return

    items = []
    for html_file in viewer_files:
        filename = html_file.name
        label = (
            filename.replace("-viewer.html", "")
            .replace("-txt", "")
            .replace("-jpg", "")
            .replace("-jpeg", "")
            .replace("-png", "")
            .replace("-py", "")
        )

        items.append(f"""<li>
  <a href="{filename}"
     onclick="gtag('event', 'click_config_viewer', {{ 'file': '{filename}' }});">
     {label}
  </a>
</li>""")

    section_title = section.replace("-", " ").replace("_", " ").title()
    output_path = subfolder_path / OUTPUT_TEMPLATE
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(HTML_HEAD.replace("{title}", section_title))
        f.write(f"<h1>{section_title}</h1>\n<ul>\n")
        f.write("\n".join(items))
        f.write("\n</ul>\n")
        f.write(HTML_FOOTER.replace("{folder}", f"/{section}"))

    generated_indexes.append(str(output_path))
    print(f"✅ index.html written to: /docs/{section}/")


# === EXECUTION ===
if __name__ == "__main__":
    for folder in Path(BASE_FOLDER).joinpath("aipos-public-eng-main", "docs").iterdir():
        if folder.is_dir():
            generate_index_for_folder(folder)

    if generated_indexes:
        print("\n📄 Final Index Pages Generated:\n")
        for path in generated_indexes:
            print(f"  - {path}")
    else:
        print("\n⚠️ No index.html files were created. No -viewer.html files detected.")
