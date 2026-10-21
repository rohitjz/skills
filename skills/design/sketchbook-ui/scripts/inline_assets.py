#!/usr/bin/env python3
"""Inline local stylesheets and images so a sketchbook page ships as one file.

Replaces <link rel="stylesheet" href="local.css"> with <style>...</style> and
<img src="local.png"> with a base64 data URI. Remote URLs (Google Fonts) are kept.

Usage:
  python scripts/inline_assets.py page.html -o page.single.html
"""
import argparse, base64, mimetypes, os, re


def main():
    a = argparse.ArgumentParser()
    a.add_argument("html")
    a.add_argument("-o", "--out", required=True)
    o = a.parse_args()
    base = os.path.dirname(os.path.abspath(o.html))
    html = open(o.html, encoding="utf-8").read()

    def local(href):
        return not re.match(r"^(https?:|data:|//)", href)

    def css(m):
        href = m.group(1)
        if not local(href):
            return m.group(0)
        with open(os.path.join(base, href), encoding="utf-8") as f:
            return "<style>\n" + f.read() + "\n</style>"

    def img(m):
        src = m.group(2)
        if not local(src):
            return m.group(0)
        path = os.path.join(base, src)
        mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f'{m.group(1)}data:{mime};base64,{data}{m.group(3)}'

    html = re.sub(r'<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"[^>]*>', css, html)
    html = re.sub(r'(<img[^>]+src=")([^"]+)(")', img, html)
    with open(o.out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", o.out, f"({len(html) // 1024} KB)")


if __name__ == "__main__":
    main()
