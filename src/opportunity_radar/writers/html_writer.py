from __future__ import annotations

from pathlib import Path

import markdown

HTML_SHELL = """<!doctype html>
<html lang="{language}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.55;
      color: #17202a;
      margin: 0;
      background: #f7f8fa;
    }}
    main {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 32px 20px 56px;
      background: #ffffff;
      min-height: 100vh;
    }}
    h1, h2, h3 {{ color: #102033; }}
    table {{ border-collapse: collapse; width: 100%; margin: 16px 0 24px; font-size: 14px; }}
    th, td {{ border: 1px solid #d8dee8; padding: 8px 10px; vertical-align: top; }}
    th {{ background: #edf2f7; text-align: left; }}
    a {{ color: #075985; }}
    code {{ background: #eef2f7; padding: 2px 4px; border-radius: 4px; }}
  </style>
</head>
<body>
<main>
{body}
</main>
</body>
</html>
"""


def render_html(markdown_text: str, title: str, language: str = "en") -> str:
    body = markdown.markdown(markdown_text, extensions=["tables", "sane_lists"])
    return HTML_SHELL.format(title=title, language=language, body=body)


def write_html_report(
    markdown_text: str,
    output_path: str | Path,
    title: str,
    language: str = "en",
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_html(markdown_text, title, language), encoding="utf-8")
    return path
