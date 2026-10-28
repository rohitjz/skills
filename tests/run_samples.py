#!/usr/bin/env python3
"""Render-test every design sample in the repo.

For each examples/*/index.html under skills/, at desktop (1280), tablet (768) and phone (390):
  - no JavaScript errors and no failed local requests
  - no horizontal page overflow (wide content must scroll inside its own container)
  - every image loads and has alt text
  - every inline SVG is either decorative (aria-hidden) or labelled (role="img" + aria-label)
  - exactly one <h1>, a <title>, a lang attribute and a viewport meta tag
  - no text smaller than 10px
  - sideways scrollers are keyboard reachable (tabindex)
  - no infinite animations, and none at all when the user prefers reduced motion
  - receipts add up (data-amt / data-subtotal / data-total)
  - interactive samples behave (see INTERACTIONS)
Screenshots go to tests/out/ for visual review. With --previews, also writes
preview.jpg (desktop, top of page) next to each sample for the gallery.

Usage: python tests/run_samples.py [--previews] [--only name]
"""
import argparse, pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "tests" / "out"
VIEWPORTS = {"desktop": (1280, 900), "tablet": (768, 1024), "phone": (390, 844)}

CHECKS_JS = r"""
() => {
  const issues = [];
  const de = document.documentElement;
  if (de.scrollWidth > de.clientWidth + 1) issues.push(`horizontal overflow: ${de.scrollWidth}px > ${de.clientWidth}px`);
  const h1 = document.querySelectorAll('h1').length;
  if (h1 !== 1) issues.push(`expected 1 <h1>, found ${h1}`);
  if (!document.title.trim()) issues.push('missing <title>');
  if (!de.getAttribute('lang')) issues.push('missing lang attribute');
  if (!document.querySelector('meta[name=viewport]')) issues.push('missing viewport meta');
  for (const img of document.images) {
    if (!img.hasAttribute('alt')) issues.push(`img without alt: ${img.getAttribute('src')}`);
    if (!img.complete || img.naturalWidth === 0) issues.push(`image failed to load: ${img.getAttribute('src')}`);
  }
  for (const svg of document.querySelectorAll('svg')) {
    const r = svg.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    if (svg.closest('[aria-hidden="true"]')) continue;
    const labelled = svg.getAttribute('role') === 'img' && (svg.getAttribute('aria-label') || svg.querySelector('title'));
    if (!labelled && !svg.closest('[aria-label]')) issues.push(`unlabelled visible svg: ${svg.outerHTML.slice(0, 70)}`);
  }
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  while (walker.nextNode()) {
    const t = walker.currentNode; const el = t.parentElement;
    if (!t.textContent.trim() || !el || seen.has(el) || el.closest('svg')) continue;
    seen.add(el);
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    const fs = parseFloat(cs.fontSize);
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;
    if (fs < 10) issues.push(`text under 10px (${fs}px): "${t.textContent.trim().slice(0, 30)}"`);
  }
  for (const el of document.querySelectorAll('*')) {
    const cs = getComputedStyle(el);
    if (!['auto', 'scroll'].includes(cs.overflowX)) continue;
    if (el.scrollWidth > el.clientWidth + 2 && !el.hasAttribute('tabindex'))
      issues.push(`scrollable region not keyboard reachable: <${el.tagName.toLowerCase()} class="${el.className}">`);
  }
  for (const a of document.getAnimations()) {
    const it = a.effect && a.effect.getTiming ? a.effect.getTiming().iterations : 1;
    if (it === Infinity) issues.push(`infinite animation on ${a.effect.target && a.effect.target.className}`);
  }
  const amts = [...document.querySelectorAll('[data-amt]')].map(e => parseFloat(e.dataset.amt));
  const sub = document.querySelector('[data-subtotal]'), tot = document.querySelector('[data-total]');
  if (amts.length && tot) {
    const pos = amts.filter(x => x > 0).reduce((a, b) => a + b, 0);
    const all = amts.reduce((a, b) => a + b, 0);
    if (sub && Math.abs(pos - parseFloat(sub.dataset.subtotal)) > 0.005) issues.push(`subtotal ${sub.dataset.subtotal} != items ${pos.toFixed(2)}`);
    if (Math.abs(all - parseFloat(tot.dataset.total)) > 0.005) issues.push(`total ${tot.dataset.total} != sum ${all.toFixed(2)}`);
  }
  return issues;
}
"""


INTERACTIONS = {
    # sample name -> function(page) returning a list of issues
    "departure-board-status": lambda page: _board(page),
}


def _board(page):
    issues = []
    before = page.inner_text("#s1")
    for _ in range(3):
        page.click("#sim")
    page.wait_for_timeout(600)
    if page.inner_text("#s1") == before:
        issues.append("simulate button did not change the board")
    if not page.is_disabled("#sim"):
        issues.append("simulate button should disable after the last update")
    if not page.inner_text("#live").strip():
        issues.append("aria-live region was not updated")
    return issues


def samples(only=None):
    pages = [("catalog", ROOT / "index.html")]
    pages += [(f"{p.parent.parent.name}-gallery", p) for p in sorted(ROOT.glob("skills/*/*/gallery/index.html"))]
    for name, p in pages:
        if p.exists() and (not only or only == name):
            yield name, p
    for p in sorted(ROOT.glob("skills/**/examples/*/index.html")):
        name = p.parent.name
        if not only or only == name:
            yield name, p


def launch(pw):
    try:
        return pw.chromium.launch(channel="chrome")
    except Exception:
        return pw.chromium.launch()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--previews", action="store_true")
    ap.add_argument("--only")
    o = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    failures, warnings, runs = [], [], 0
    with sync_playwright() as pw:
        browser = launch(pw)
        for name, path in samples(o.only):
            for vp, (w, h) in VIEWPORTS.items():
                for motion in (["no-preference", "reduce"] if vp == "desktop" else ["no-preference"]):
                    runs += 1
                    ctx = browser.new_context(viewport={"width": w, "height": h}, reduced_motion=motion)
                    page = ctx.new_page()
                    errs = []
                    page.on("pageerror", lambda e: errs.append(f"js error: {e}"))
                    page.on("console", lambda m: m.type == "error" and errs.append(f"console: {m.text[:120]}"))
                    page.on("requestfailed", lambda r: (errs if r.url.startswith("file:") else warnings).append(f"{name}: request failed {r.url[:90]}"))
                    page.goto(path.as_uri(), wait_until="networkidle")
                    page.evaluate("document.fonts.ready")
                    issues = errs + page.evaluate(CHECKS_JS)
                    if vp == "desktop" and motion == "no-preference" and name in INTERACTIONS:
                        page.reload(wait_until="networkidle")
                        issues += INTERACTIONS[name](page)
                        page.reload(wait_until="networkidle")
                    if motion == "reduce":
                        running = page.evaluate("document.getAnimations().filter(a => a.playState === 'running').length")
                        if running:
                            issues.append(f"{running} animation(s) running with reduced motion")
                    else:
                        page.screenshot(path=str(OUT / f"{name}-{vp}.png"), full_page=True)
                        if o.previews and vp == "desktop":
                            page.screenshot(path=str(path.parent / "preview.jpg"), type="jpeg", quality=80, clip={"x": 0, "y": 0, "width": w, "height": h})
                    for i in issues:
                        failures.append(f"{name} [{vp}{', reduced motion' if motion == 'reduce' else ''}]: {i}")
                    status = "FAIL" if issues else "ok"
                    print(f"{status:4} {name:28} {vp:8}{' reduced-motion' if motion == 'reduce' else ''}")
                    ctx.close()
        browser.close()
    for wmsg in sorted(set(warnings)):
        print("WARN", wmsg)
    for f in failures:
        print("FAIL", f)
    print(f"\n{runs} page renders, {len(failures)} failures, {len(set(warnings))} warnings. Screenshots: {OUT}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
