# 02_render_txt_md_to_html_signalstyle.py
import os
import json
import markdown

# === CONFIGURATION ===
MANIFEST_PATH = r"/home/t51/Documents/SIGNAL/aipos-public-eng-main-site/site_manifest.json"
BASE_FOLDER = os.path.dirname(MANIFEST_PATH)
VIEWER_OUTPUT_FOLDER = os.path.join(BASE_FOLDER, "viewer")
GA4_ID = "G-FCTN7560BJ"
HOMEPAGE = "https://tk51.github.io/aipos-public-eng/"

# === HTML TEMPLATE ===
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — AIPOS Viewer</title>

  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={ga4_id}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag() {{ dataLayer.push(arguments); }}
    gtag('js', new Date());
    gtag('config', '{ga4_id}');
  </script>

  <style>
    :root {{ color-scheme: light dark; }}

    body {{
      font-family: monospace;
      background-color: #ffffff;
      color: #000000;
      padding: 1rem;
      font-size: 16px;
      line-height: 1.6;
    }}

    pre {{
      white-space: pre-wrap;
      word-wrap: break-word;
      background: #f4f4f4;
      padding: 1em;
      border-radius: 5px;
      overflow-x: auto;
      border: 1px solid #ccc;
    }}

    h1 {{
      font-size: 1.4rem;
      margin-bottom: 0.75rem;
      border-bottom: 1px solid #ccc;
      padding-bottom: 0.3rem;
    }}

    .footer {{
      margin-top: 2rem;
      font-size: 0.8rem;
      color: #555;
      border-top: 1px solid #ccc;
      padding-top: 0.5rem;
    }}

    .nav-button {{
      display: inline-block;
      margin: 1rem 0.5rem;
      padding: 0.5rem 1rem;
      background-color: #E0E0E0;
      color: #111111;
      text-decoration: none;
      border-radius: 4px;
      font-size: 0.95rem;
      font-family: 'Roboto Mono', monospace;
      transition: background 0.2s ease-in-out;
    }}

    .nav-button:hover {{
      background-color: #B0B0B0;
    }}

    .download-button {{
      display: inline-block;
      margin-top: 1rem;
      margin-bottom: 1rem;
      padding: 0.5rem 1rem;
      background-color: #E0E0E0;
      color: #111111;
      text-decoration: none;
      border-radius: 4px;
      font-size: 0.95rem;
      font-family: 'Roboto Mono', monospace;
      transition: background 0.2s ease-in-out;
    }}

    .download-button:hover {{
      background-color: #B0B0B0;
    }}

    @media (prefers-color-scheme: dark) {{
      body {{
        background-color: #0d1117;
        color: #c9d1d9;
      }}

      pre {{
        background: #161b22;
        border: 1px solid #30363d;
      }}

      .footer {{
        color: #999;
        border-top: 1px solid #333;
      }}

      .nav-button {{
        background-color: #30363d;
        color: #ffffff;
      }}

      .nav-button:hover {{
        background-color: #505A62;
      }}

      .download-button {{
        background-color: #30363d;
        color: #E6EEF5;
      }}

      .download-button:hover {{
        background-color: #505A62;
      }}
    }}
  </style>
</head>
<body>

  <div style="margin: 1rem 0;">
    <a class="nav-button" href="{homepage}" onclick="gtag('event', 'nav_click', {{'type': 'home'}});">⌂ Home</a>
    <a class="nav-button" href="javascript:history.back()" onclick="gtag('event', 'nav_click', {{'type': 'back'}});">← Back</a>
  </div>

  <h1>{title}</h1>
  {download_block}
  <article>{content}</article>
  {download_block}

  <div style="margin: 1rem 0;">
    <a class="nav-button" href="{homepage}" onclick="gtag('event', 'nav_click', {{'type': 'home'}});">⌂ Home</a>
    <a class="nav-button" href="javascript:history.back()" onclick="gtag('event', 'nav_click', {{'type': 'back'}});">← Back</a>
  </div>

  <div class="footer">
    Static viewer render • {rel_path} • #fromukrainianswithlovetohumankind
  </div>

</body>
</html>
"""

def get_download_html(filename):
    return f"""
<a class="download-button"
   href="../download/{filename}"
   download
   onclick="gtag('event', 'download_click', {{'file': '{filename}'}});">
   ⬇ Download {filename}
</a>
"""

def main():
    os.makedirs(VIEWER_OUTPUT_FOLDER, exist_ok=True)

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # === FORCE VISUALS TO RENDER EVEN IF build_viewer IS FALSE ===
    for entry in manifest:
        if entry.get("ext", "").lower() in [".jpg", ".jpeg", ".png"]:
            entry["build_viewer"] = True

    for item in manifest:
        if not item.get("build_viewer"):
            continue

        filename = item["filename"]
        rel_path = item["rel_path"]
        abs_path = os.path.join(BASE_FOLDER, rel_path)

        if not os.path.isfile(abs_path):
            print(f"⚠️ Missing file: {abs_path}")
            continue

        ext = item["ext"].lower()
        title = item.get("title", filename.replace("-", " ").replace(".txt", "").replace(".md", ""))

        # === TEXT/MARKDOWN FILES ===
        if ext in [".txt", ".md"]:
            with open(abs_path, "r", encoding="utf-8") as f:
                raw_text = f.read()

            # Convert .txt to .md to preserve logic flow
            md_path = abs_path.replace(".txt", ".md")
            with open(md_path, "w", encoding="utf-8") as md_file:
                md_file.write(raw_text)

            html_body = markdown.markdown(raw_text, extensions=["extra", "sane_lists", "nl2br"])

        # === VISUAL FILES ===
        elif ext in [".jpg", ".jpeg", ".png"]:
            html_body = f'<img src="../visuals/{filename}" alt="{title}" style="max-width:100%; height:auto;" />'

        elif ext == ".py":
            with open(abs_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
            html_body = f"<pre>{raw_text}</pre>"

        else:
            continue  # skip unsupported file types

        download_block = get_download_html(filename) if item.get("download") else ""

        html_output = HTML_TEMPLATE.format(
            title=title,
            content=html_body,
            filename=filename,
            ga4_id=GA4_ID,
            homepage=HOMEPAGE,
            download_block=download_block,
            rel_path=rel_path.replace("\\", "/")
        )

        ext_suffix = ext.replace('.', '')  # e.g., "txt" or "jpg"
        out_file = f"{filename.rsplit('.', 1)[0]}-{ext_suffix}-viewer.html"
        out_path = os.path.join(VIEWER_OUTPUT_FOLDER, out_file)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_output)

        print(f"✅ Viewer built: {out_file} {'(⬇ included)' if item.get('download') else '(read-only)'}")

if __name__ == "__main__":
    main()

