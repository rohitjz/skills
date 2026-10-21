#!/usr/bin/env python3
"""Render a sketchbook newsletter to PNG slices for pasting into Outlook/Gmail.

Email clients strip web fonts, SVG filters and most CSS, so the reliable way to
send this look is as images. This script screenshots the page at 2x in headless
Chrome, crops to the paper sheet, and cuts it into N slices at blank gaps
(never through a line of text). It also writes paste-into-email.html: open it in
a browser, Cmd/Ctrl+A, copy, and paste into a new email.

Usage:
  python scripts/export_email.py examples/lets-encrypt-10-years/index.html --slices 4
"""
import argparse, os, shutil, subprocess, sys, tempfile
from PIL import Image

CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
    "google-chrome", "chromium", "chromium-browser",
]


def find_chrome():
    for p in CHROME_PATHS:
        if os.path.exists(p) or shutil.which(p):
            return p
    sys.exit("Chrome/Edge not found; pass --chrome PATH")


def main():
    a = argparse.ArgumentParser()
    a.add_argument("html")
    a.add_argument("--slices", type=int, default=4)
    a.add_argument("--out", help="output folder (default: <html dir>/email)")
    a.add_argument("--chrome")
    a.add_argument("--height", type=int, default=4000, help="viewport height in CSS px")
    o = a.parse_args()

    html = os.path.abspath(o.html)
    out = o.out or os.path.join(os.path.dirname(html), "email")
    os.makedirs(out, exist_ok=True)
    shot = os.path.join(tempfile.mkdtemp(), "page.png")
    subprocess.run([o.chrome or find_chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--virtual-time-budget=6000",
                    f"--window-size=780,{o.height}", f"--screenshot={shot}", f"file://{html}"],
                   timeout=120, capture_output=True)

    im = Image.open(shot).convert("RGB")
    W, H = im.size
    px = im.convert("L").load()
    # The sheet is the bright column band; the desk around it is grey.
    xs = [x for x in range(W) if px[x, 200] >= 246]
    x0, x1 = xs[0], xs[-1] + 1
    col = [px[x0 + 60, y] for y in range(H)]
    y0 = next(y for y in range(H) if col[y] >= 240)
    y1 = max(y for y in range(H) if col[y] >= 240) + 1
    sheet = im.crop((x0, y0, x1, y1))
    w, h = sheet.size
    g = sheet.convert("L").load()
    quiet = [min(g[x, y] for x in range(int(w * .1), int(w * .96), 3)) > 200 for y in range(h)]

    def blank_band(y, n=44):
        return all(quiet[yy] for yy in range(max(0, y - n // 2), min(h, y + n // 2)))

    cuts = [0]
    for k in range(1, o.slices):
        t = int(h * k / o.slices)
        for dy in range(0, 1200, 2):
            hit = next((y for y in (t - dy, t + dy) if 0 < y < h and blank_band(y)), None)
            if hit:
                cuts.append(hit)
                break
    cuts = sorted(set(cuts)) + [h]

    files = []
    for i in range(len(cuts) - 1):
        fn = f"part-{i + 1}.png"
        sheet.crop((0, cuts[i], w, cuts[i + 1])).save(os.path.join(out, fn), optimize=True)
        files.append(fn)
    sheet.save(os.path.join(out, "full.png"), optimize=True)

    dw = w // 2
    imgs = "".join(
        f'<img src="{f}" width="{dw}" style="display:block;width:{dw}px;max-width:100%;height:auto;border:0;margin:0" alt="">'
        for f in files)
    with open(os.path.join(out, "paste-into-email.html"), "w") as f:
        f.write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>Paste into email</title></head>'
                f'<body style="margin:0;padding:20px;background:#fff">{imgs}</body></html>')
    print(f"{len(files)} slices -> {out}  (cuts at {cuts})")


if __name__ == "__main__":
    main()
