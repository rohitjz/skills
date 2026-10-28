#!/usr/bin/env python3
"""Risograph print simulation for analog-ui.

Two jobs:

1. separate(image, paper, inks) -> one coverage map per ink (0..1).
   Unmixes existing artwork into spot-ink layers with a multiplicative
   (transparent ink) model, which is how a riso separation works.

2. print_page(layers, size, inks) -> RGB page.
   Turns coverage maps into printed ink: grain, mottled solids,
   misregistration between drums, multiply onto textured paper.

Typical flow for a page: render the page artboard once per ink (see
render_ink_passes), then print_page() the passes.
"""
import numpy as np
from PIL import Image, ImageFilter

PAPER = (245, 233, 215)
PINK = (255, 72, 110)    # fluorescent pink
BLUE = (16, 62, 118)     # medium/federal blue


def _arr(img):
    return np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0


def separate(img, paper, inks, step=0.04, chunk=20000):
    """Unmix an RGB image into coverage maps for 1-2 transparent inks.
    obs = paper * prod_i (1 - a_i * (1 - ink_i/paper)), solved by grid search."""
    obs = _arr(img).reshape(-1, 3)
    p = np.array(paper, np.float32) / 255.0
    T = [np.clip(np.array(k, np.float32) / 255.0 / p, 0, 1) for k in inks]
    grid = np.arange(0, 1 + 1e-6, step, dtype=np.float32)
    if len(inks) == 1:
        combos = grid[:, None]
    else:
        a, b = np.meshgrid(grid, grid, indexing="ij")
        combos = np.stack([a.ravel(), b.ravel()], 1)
    pred = np.ones((len(combos), 3), np.float32) * p
    for i, t in enumerate(T):
        pred *= 1 - combos[:, i:i + 1] * (1 - t)
    pred_log = np.log(pred + 1e-4)
    out = np.zeros((len(obs), len(inks)), np.float32)
    for s in range(0, len(obs), chunk):
        o = np.log(obs[s:s + chunk] + 1e-4)
        err = ((o[:, None, :] - pred_log[None, :, :]) ** 2).sum(-1)
        out[s:s + chunk] = combos[err.argmin(1)]
    h, w = img.size[1], img.size[0]
    return [out[:, i].reshape(h, w) for i in range(len(inks))]


def to_image(cov):
    """Coverage map -> grayscale image (black = full ink)."""
    return Image.fromarray(np.uint8(np.clip(255 * (1 - cov), 0, 255)), "L")


def from_image(img):
    return 1 - np.asarray(img.convert("L"), np.float32) / 255.0


def _noise(h, w, scale, rng):
    """Smooth value noise in 0..1 at roughly `scale` px features."""
    sh, sw = max(2, int(h / scale) + 2), max(2, int(w / scale) + 2)
    small = Image.fromarray(np.uint8(rng.random((sh, sw)) * 255), "L")
    big = small.resize((w, h), Image.BICUBIC)
    return np.asarray(big, np.float32) / 255.0


def _grain(cov, rng, fine=0.7, mottle=0.18, speck=0.06, floor=0.05, smooth=1.2, grit=0.6):
    """Coverage -> printed ink: stochastic grain, uneven solids, dropouts.
    floor drops near-zero coverage (scan noise) so clean paper stays clean;
    smooth softens source noise before screening; grit blends the dither with
    the smooth tone (1 = pure dither, which turns light tints into static)."""
    h, w = cov.shape
    if smooth:
        cov = np.asarray(Image.fromarray(np.uint8(np.clip(cov, 0, 1) * 255)).filter(ImageFilter.GaussianBlur(smooth)), np.float32) / 255.0
    cov = np.clip((cov - floor) / (1 - floor), 0, 1)
    thr = rng.random((h, w)).astype(np.float32)
    thr = np.asarray(Image.fromarray(np.uint8(thr * 255)).filter(ImageFilter.GaussianBlur(fine)), np.float32) / 255.0
    # Rank-normalise so the threshold is uniform: mean printed ink then equals
    # the requested coverage (a bell-shaped threshold drops light tints).
    flat = thr.ravel()
    thr = (np.argsort(np.argsort(flat)).astype(np.float32) / flat.size).reshape(thr.shape)
    tone = np.clip((cov - thr) * 8 + 0.5, 0, 1)           # soft-edged dither
    tone = grit * tone + (1 - grit) * cov                  # riso tints read as soft grain, not static
    tone = np.where(cov > 0.92, 1.0, tone)                 # solids stay solid
    ink = tone * (1 - mottle * _noise(h, w, 90, rng)) * (1 - 0.5 * mottle * _noise(h, w, 14, rng))
    drop = rng.random((h, w)) < speck * cov                # tiny paper specks in ink
    ink = np.where(drop, ink * 0.55, ink)
    return np.clip(ink, 0, 1)


def paper_texture(w, h, rng, base=PAPER, age=1.0):
    """Uncoated stock: fibre, faint low-frequency stains and a darker, warmer
    edge where the sheet has been handled. age=0 gives clean new paper."""
    p = np.ones((h, w, 3), np.float32) * (np.array(base, np.float32) / 255.0)
    fib = 0.035 * (_noise(h, w, 6, rng) - 0.5) + 0.03 * (_noise(h, w, 120, rng) - 0.5)
    p = p * (1 + fib[..., None])
    if age:
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        d = np.minimum.reduce([xx, yy, w - 1 - xx, h - 1 - yy]) / (0.075 * min(w, h))
        burn = np.exp(-d) * (0.6 + 0.8 * _noise(h, w, 60, rng))       # uneven handled edge
        stain = np.clip(_noise(h, w, 260, rng) - 0.62, 0, 1) * 0.10    # a few soft blotches
        dark = age * (0.12 * burn + stain)
        warm = np.array([0.35, 0.75, 1.35], np.float32)                 # edges yellow as they darken
        p = p * (1 - dark[..., None] * warm)
    return np.clip(p, 0, 1)


def _shift(cov, dx, dy):
    return np.asarray(Image.fromarray(np.uint8(cov * 255)).transform(
        (cov.shape[1], cov.shape[0]), Image.AFFINE, (1, 0, -dx, 0, 1, -dy), resample=Image.BILINEAR), np.float32) / 255.0


def print_page(layers, inks, seed=7, offsets=None, paper=PAPER):
    """layers: list of coverage maps (same size). Returns an RGB PIL image."""
    rng = np.random.default_rng(seed)
    h, w = layers[0].shape
    out = paper_texture(w, h, rng, paper)
    offsets = offsets or [(0, 0), (3, 2)]
    p = out.copy()
    for cov, ink, (dx, dy) in zip(layers, inks, offsets):
        c = _grain(_shift(cov, dx, dy) if (dx or dy) else cov, rng)
        t = np.clip(np.array(ink, np.float32) / 255.0 / (np.array(paper, np.float32) / 255.0), 0, 1)
        out = out * (1 - c[..., None] * (1 - t))
    edge = _noise(h, w, 400, rng)[..., None]               # faint uneven paper tone
    out = out * (0.985 + 0.03 * edge)
    return Image.fromarray(np.uint8(np.clip(out, 0, 1) * 255), "RGB")


def render_ink_passes(html_path, size, inks=("pink", "blue"), scale=2):
    """Render an artboard once per ink. The page must style
    body.pass-<ink> so only that ink's elements show, in black on white."""
    from playwright.sync_api import sync_playwright
    out = []
    with sync_playwright() as pw:
        try:
            br = pw.chromium.launch(channel="chrome")
        except Exception:
            br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": size[0], "height": size[1]}, device_scale_factor=scale)
        pg.goto(html_path.as_uri() if hasattr(html_path, "as_uri") else html_path, wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        for ink in inks:
            pg.evaluate(f"document.body.className='pass-{ink}'")
            pg.wait_for_timeout(120)
            png = pg.screenshot(clip={"x": 0, "y": 0, "width": size[0], "height": size[1]})
            import io
            out.append(from_image(Image.open(io.BytesIO(png))))
        br.close()
    return out


def overprint_solid(img, cov, ink, offset=(0, 0), paper=PAPER):
    """Print a crisp solid (no grain) on top of a printed page, e.g. a QR code
    that must stay scannable. Uses the same drum offset as that ink's layer."""
    if offset != (0, 0):
        cov = _shift(cov, *offset)
    out = np.asarray(img, np.float32) / 255.0
    t = np.clip(np.array(ink, np.float32) / 255.0 / (np.array(paper, np.float32) / 255.0), 0, 1)
    out = out * (1 - np.clip(cov, 0, 1)[..., None] * (1 - t))
    return Image.fromarray(np.uint8(np.clip(out, 0, 1) * 255), "RGB")
