import os
from pathlib import Path
import shutil

# === CONFIGURATION ===
BASE_DOCS = Path("/home/t51/Documents/SIGNAL/aipos-public-eng-main-site/aipos-public-eng-main/docs")
CORE_DOCS_FOLDER = BASE_DOCS / "core-docs"
VISUALS_FOLDER = BASE_DOCS / "visuals"
GA4_ID = "G-FCTN7560BJ"
OUTPUT_FILE = BASE_DOCS / "index.html"
BASE_FOLDER = BASE_DOCS.parent  # /aipos-public-eng-main-site

# === INTRO MESSAGE BLOCK ===
INTRO_HTML = """
<div class="intro">
  <p>Welcome to <b>AIPOS</b> world!</p>

  <p>Please, check the respective materials — it won’t take you long to understand how the Method works.</p>

  <p>In fact, you would be easily getting through the “<b>Copy – Edit – Paste – Control</b>” protocol,
  once you see the benefits of the setup proposed.</p>

  <p>
  Want to know more, consult, or just say hi?<br>
  — <a href="https://www.linkedin.com/in/taras-khamardiuk/" target="_blank">Contact me on LinkedIn</a></p>

  <p>Respectfully user-centric,<br>— Kay</p>
</div>
"""

# === HTML TEMPLATE ===
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AIPOS Viewer Platform</title>

  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={ga4_id}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag() {{ dataLayer.push(arguments); }}
    gtag('js', new Date());
    gtag('config', '{ga4_id}');
  </script>

  <style>
    body {{
      font-family: system-ui, sans-serif;
      background: #f9f9f9;
      color: #222;
      padding: 2rem;
      font-size: 16px;
      line-height: 1.6;
    }}
    h1 {{
      font-size: 1.8rem;
      border-bottom: 2px solid #ccc;
      padding-bottom: 0.4rem;
      margin-bottom: 1.5rem;
    }}
    h2 {{
      font-size: 1.4rem;
      margin-top: 2rem;
      margin-bottom: 0.5rem;
    }}
    ul {{
      padding-left: 1.5rem;
    }}
    li {{
      margin-bottom: 0.6rem;
    }}
    a {{
      color: #1a73e8;
      text-decoration: none;
      font-weight: 500;
    }}
    a:hover {{
      text-decoration: underline;
    }}
    .intro {{
      background: #f1f1f1;
      padding: 1rem;
      border-left: 4px solid #ccc;
      margin-bottom: 2rem;
    }}
    .footer {{
      margin-top: 3rem;
      font-size: 0.8rem;
      color: #888;
      border-top: 1px solid #ccc;
      padding-top: 0.5rem;
    }}
    @media (prefers-color-scheme: dark) {{
      body {{
        background-color: #0d1117;
        color: #c9d1d9;
      }}
      .intro {{
        background: #161b22;
        border-left: 4px solid #444;
      }}
      a {{
        color: #58a6ff;
      }}
      .footer {{
        border-top: 1px solid #333;
        color: #777;
      }}
    }}
  </style>
</head>
<body>

  <h1>AIPOS — Viewer Platform</h1>

  {intro_block}

  <h2>📄 Core Documentation</h2>
  <ul>
    {core_doc_links}
  </ul>

  <h2>🗂️ Configurations</h2>
  <ul>
    <li><a href="configs/index.html" onclick="gtag('event', 'nav_click', {{ 'type': 'configs' }});">View Configuration Files</a></li>
  </ul>

  <h2>🧪 Methods</h2>
  <ul>
    <li><a href="methods/index.html" onclick="gtag('event', 'nav_click', {{ 'type': 'methods' }});">View UX Method Cases</a></li>
  </ul>

  {visuals_section}

  <div class="footer">
    Built by Kay • Static GA4-tracked interface • #fromukrainianswithlovetohumankind
  </div>

</body>
</html>
"""

# === UTILITY ===
def generate_link_list(folder: Path, prefix: str) -> str:
    if not folder.exists(): return ""
    items = []
    for file in sorted(folder.glob("*-viewer.html")):
        fname = file.name
        label = fname.replace("-viewer.html", "").replace("-txt", "").replace("-jpg", "").replace("-jpeg", "").replace("-png", "")
        items.append(f"""<li><a href="{prefix}/{fname}" onclick="gtag('event', 'read_doc', {{ 'file': '{fname}' }});">{label}</a></li>""")
    return "\n    ".join(items)

# === EXECUTION ===
if __name__ == "__main__":
    print("🛠 Generating main index page...")

    # Copy raw visuals if not already present
    RAW_VISUALS_SRC = BASE_FOLDER
    RAW_VISUALS_DEST = VISUALS_FOLDER
    raw_visuals_copied = 0

    for root, _, files in os.walk(RAW_VISUALS_SRC):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                src_path = Path(root) / file
                dest_path = RAW_VISUALS_DEST / file
                if not dest_path.exists():
                    shutil.copy2(src_path, dest_path)
                    raw_visuals_copied += 1

    if raw_visuals_copied > 0:
        print(f"🖼️ Raw visuals copied into /docs/visuals/: {raw_visuals_copied} file(s)")
    else:
        print("✔️ Raw visuals already present in /docs/visuals/ — no new files copied.")

    # Generate core documentation links
    core_links = generate_link_list(CORE_DOCS_FOLDER, "core-docs")

    # Generate visuals section only if viewer files exist
    visuals_section = ""
    if VISUALS_FOLDER.exists() and any(VISUALS_FOLDER.glob("*-viewer.html")):
        visuals_section = """
  <h2>🎞️ Visuals</h2>
  <ul>
    <li>
      <a href="visuals/index.html" onclick="gtag('event', 'nav_click', { 'type': 'visuals' });">
        View Visual Assets
      </a>
    </li>
  </ul>
"""

    # Final HTML write
    rendered = HTML_TEMPLATE.format(
        ga4_id=GA4_ID,
        intro_block=INTRO_HTML.strip(),
        core_doc_links=core_links,
        visuals_section=visuals_section
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"✅ /docs/index.html created at:\n{OUTPUT_FILE}")
