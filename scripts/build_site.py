#!/usr/bin/env python3
"""Build index.html (the catalog of every skill) from the README catalog tables.
Run after editing the catalog in README.md. CI checks the committed file is current (--check)."""
import html, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "https://github.com/rohitjz/skills/tree/main/"


def md_inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


def build():
    t = (ROOT / "README.md").read_text()
    cats = []
    for m in re.finditer(r"^### (.+?)\n(.*?)(?=^### |^## )", t, re.S | re.M):
        rows = re.findall(r"^\| \[([^\]]+)\]\(([^)]+)\) \| (.+?) \|$", m.group(2), re.M)
        intro = m.group(2).split("\n|")[0].strip().replace("\n", " ")
        cats.append((m.group(1), rows, intro))
    total = sum(len(r) for _, r, _ in cats)
    sections = []
    for i, (name, rows, intro) in enumerate(cats, 1):
        items = []
        for skill, path, desc in rows:
            gallery = ROOT / path / "gallery" / "index.html"
            desc = re.sub(r"\s*\[(Gallery|Live example)\]\([^)]+\)", "", desc)
            links = f'<a href="{REPO}{path}">Source</a>'
            if gallery.exists():
                links = f'<a class="gal" href="{path}/gallery/">Gallery</a>' + links
            items.append(f'<li><div class="nm"><code>/{skill}</code></div><p>{md_inline(desc)}</p><div class="lk">{links}</div></li>')
        intro_html = f'<p class="intro">{md_inline(intro)}</p>' if intro and not intro.startswith("|") else ""
        sections.append(
            f'<section aria-labelledby="c{i}"><h2 id="c{i}"><span>{i:02d}</span>{html.escape(name)}'
            f'<small>{len(rows)} skill{"s" if len(rows) != 1 else ""}</small></h2>{intro_html}<ul>{"".join(items)}</ul></section>')
    return TEMPLATE.replace("{{TOTAL}}", str(total)).replace("{{CATS}}", str(len(cats))).replace("{{SECTIONS}}", "\n".join(sections))


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Skills by rohitjz</title>
<meta name="description" content="{{TOTAL}} agent skills for Claude Code and GitHub Copilot, by category.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root{--bg:#F6F4EF;--ink:#1D1C1A;--muted:#6E6A62;--rule:#D9D4C9;--accent:#C2410C;
    --serif:"Instrument Serif",Georgia,serif;--mono:"DM Mono",ui-monospace,Menlo,monospace}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--mono);font-size:14.5px;line-height:1.6}
  main{max-width:1060px;margin:0 auto;padding:64px 28px 80px}
  header{display:grid;grid-template-columns:1.2fr 1fr;gap:40px;align-items:end;border-bottom:1px solid var(--ink);padding-bottom:30px}
  header>*{min-width:0}
  h1{font-family:var(--serif);font-weight:400;font-size:clamp(38px,5.6vw,70px);line-height:1.02;margin:0;letter-spacing:-.01em;max-width:16ch}
  .lede{margin:0;color:#3A3833;max-width:44ch}
  .lede b{font-weight:500}
  pre{background:var(--ink);color:#EDEAE2;padding:14px 16px;font-size:13px;overflow-x:auto;margin:16px 0 0}
  section{margin-top:56px}
  h2{font-family:var(--serif);font-weight:400;font-size:38px;line-height:1;margin:0 0 6px;display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
  h2 span{font-family:var(--mono);font-size:13px;color:var(--accent)}
  h2 small{font-family:var(--mono);font-size:12px;color:var(--muted);margin-left:auto}
  .intro{color:var(--muted);font-size:13px;max-width:80ch;margin:4px 0 0}
  ul{list-style:none;padding:0;margin:14px 0 0}
  li{display:grid;grid-template-columns:270px 1fr auto;gap:22px;align-items:baseline;padding:14px 0;border-top:1px solid var(--rule)}
  li>*{min-width:0}
  .nm code{font-family:var(--mono);font-size:15px;font-weight:500;color:var(--ink);overflow-wrap:anywhere}
  li p{margin:0;color:#3A3833}
  li p code{font-size:13px;background:#ECE8DF;padding:1px 5px}
  .lk{display:flex;gap:14px;white-space:nowrap}
  a{color:var(--ink)}
  .lk a{font-size:13px;text-decoration:none;border-bottom:1px solid var(--rule)}
  .lk a:hover{border-color:var(--ink)}
  .lk a.gal{color:var(--accent);border-color:var(--accent);font-weight:500}
  a:focus-visible,pre:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
  footer{margin-top:64px;padding-top:16px;border-top:1px solid var(--ink);font-size:12.5px;color:var(--muted);display:flex;gap:22px;flex-wrap:wrap}
  @media (max-width:820px){
    main{padding:40px 18px 60px}
    header{grid-template-columns:1fr;gap:18px}
    li{grid-template-columns:1fr;gap:6px}
    h2 small{margin-left:0;width:100%}
  }
</style>
</head>
<body>
<main>
  <header>
    <h1>{{TOTAL}} agent skills for Claude Code and GitHub Copilot.</h1>
    <div>
      <p class="lede">Design pages that don't look templated, position a product, write and present clearly, and model a stock. {{CATS}} categories; install one skill, a category, or all of them. Each is a folder with a <code>SKILL.md</code> the agent reads.</p>
      <pre tabindex="0" aria-label="Install commands"><code>git clone https://github.com/rohitjz/skills
cd skills &amp;&amp; ./install.sh --list</code></pre>
    </div>
  </header>
{{SECTIONS}}
  <footer><a href="https://github.com/rohitjz/skills">rohitjz/skills on GitHub</a><span>MIT, except finance (Apache-2.0)</span><span>Generated from README.md by scripts/build_site.py</span></footer>
</main>
</body>
</html>
"""

if __name__ == "__main__":
    out = ROOT / "index.html"
    new = build()
    if "--check" in sys.argv:
        ok = out.exists() and out.read_text() == new
        print("index.html is current" if ok else "index.html is stale: run python scripts/build_site.py")
        sys.exit(0 if ok else 1)
    out.write_text(new)
    print("wrote", out)
