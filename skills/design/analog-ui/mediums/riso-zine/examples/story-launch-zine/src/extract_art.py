#!/usr/bin/env python3
"""Separate the illustrations in the approved board mock into pink and blue
ink layers (coverage maps), with baked-in lettering painted out.

Source: src/source/board-mock.png (the board Rohit supplied). The page type
is re-set live in each artboard, so only illustration pixels are kept.

When higher-resolution art exists (for example from an image model), drop
it in src/source/ and point CROPS at it; the rest of the pipeline is unchanged.
"""
import pathlib, sys
import numpy as np
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
import riso  # noqa: E402

MOCK = Image.open(HERE / "source" / "board-mock.png").convert("RGB")
OUT = HERE / "art"
OUT.mkdir(exist_ok=True)

INK_PINK = (248, 84, 108)
INK_BLUE = (14, 62, 112)
UPSCALE = 4
# True cream stock. The mock's sheets carry a light pink flood; measuring
# against cream turns that flood into real pink-ink coverage.
PAPER = (250, 242, 230)

# name: (mock box, paper sample box, [boxes to clear of blue text], [boxes to clear of pink])
CROPS = {
    "cover": ((39, 129, 338, 546), (40, 130, 340, 548),
              [(118, 113, 271, 176), (6, 363, 109, 409), (196, 396, 288, 413)],
              [(12, 5, 289, 121)]),
    "v-communicator": ((619, 229, 726, 316), (640, 200, 700, 210), [], []),
    "v-mountain": ((737, 229, 848, 316), (640, 200, 700, 210), [], []),
    "v-book": ((619, 365, 726, 447), (640, 200, 700, 210), [], []),
    "v-laptop": ((737, 365, 848, 447), (640, 200, 700, 210), [], []),
    "book-small": ((372, 366, 471, 421), (370, 430, 420, 440), [], []),
}


_V = {"pink": (0.06, 0.62), "blue": (0.10, 0.52)}
LEVELS = {"v-communicator": _V, "v-mountain": _V, "v-book": _V, "v-laptop": _V, "book-small": _V}


def paper_of(box):
    a = np.asarray(MOCK.crop(box), np.float32).reshape(-1, 3)
    lum = a.sum(1)
    return tuple(int(x) for x in a[lum >= np.percentile(lum, 92)].mean(0))


def fill_from_surroundings(cov, box, pad=6):
    """Replace a box in a coverage map with a median-filtered version of its
    surroundings, so knocked-out text does not leave holes in the ground ink."""
    x0, y0, x1, y1 = box
    img = Image.fromarray(np.uint8(cov * 255))
    region = img.crop((max(0, x0 - pad), max(0, y0 - pad), x1 + pad, y1 + pad))
    for _ in range(3):
        region = region.filter(ImageFilter.MedianFilter(9))
    arr = np.asarray(region, np.float32) / 255.0
    cov = cov.copy()
    ox, oy = max(0, x0 - pad), max(0, y0 - pad)
    cov[y0:y1, x0:x1] = arr[y0 - oy:y1 - oy, x0 - ox:x1 - ox]
    return cov


def main():
    for name, (box, pbox, clear_blue, clear_pink) in CROPS.items():
        src = MOCK.crop(box)
        pink, blue = riso.separate(src, PAPER, [INK_PINK, INK_BLUE])
        for b in clear_blue:
            x0, y0, x1, y1 = b
            textish = blue[y0:y1, x0:x1] > 0.25
            blue[y0:y1, x0:x1] = np.where(textish, 0, blue[y0:y1, x0:x1])
            pink = fill_from_surroundings(pink, b)
        for b in clear_pink:
            # lettering is solid pink; cap it at the sheet's flood level
            x0, y0, x1, y1 = b
            flood = float(np.median(pink[y1:y1 + 20, x0:x1]))
            pink[y0:y1, x0:x1] = np.minimum(pink[y0:y1, x0:x1], flood)
        if name.startswith("v-"):
            # tiles sit on a tint drawn by the page; remove the source tint
            for ink in (pink, blue):
                edge = np.concatenate([ink[:3].ravel(), ink[-3:].ravel(), ink[:, :3].ravel(), ink[:, -3:].ravel()])
                ink -= np.median(edge)
                np.clip(ink, 0, 1, out=ink)
        for ink, cov in (("pink", pink), ("blue", blue)):
            img = riso.to_image(cov)
            img = img.resize((img.width * UPSCALE, img.height * UPSCALE), Image.LANCZOS)
            img = img.filter(ImageFilter.GaussianBlur(0.6))
            if name in LEVELS:
                # upscaled mock art has soft, half-strength lines that grain
                # turns to static; a levels curve makes lines print solid and
                # leaves light tints light, as a real riso master would
                lo, hi = LEVELS[name][ink]
                c = np.clip((riso.from_image(img) - lo) / (hi - lo), 0, 1)
                img = riso.to_image(c * c * (3 - 2 * c))
            img.save(OUT / f"{name}-{ink}.png", optimize=True)
        print(name, src.size, "-> x", UPSCALE)
    # pieces of the cover reused on later pages (cover-crop coords, x UPSCALE)
    for piece, (x0, y0, x1, y1) in {"cat": (183, 282, 299, 392), "landscape": (142, 147, 299, 282)}.items():
        for ink in ("pink", "blue"):
            img = Image.open(OUT / f"cover-{ink}.png").crop((x0 * UPSCALE, y0 * UPSCALE, x1 * UPSCALE, y1 * UPSCALE))
            if piece == "cat":
                # vignette: fade the crop into paper so it is not a hard rectangle
                cov = riso.from_image(img)
                h, w = cov.shape
                yy, xx = np.mgrid[0:h, 0:w]
                d = np.sqrt(((xx - w * 0.55) / (w * 0.52)) ** 2 + ((yy - h * 0.58) / (h * 0.52)) ** 2)
                cov *= np.clip((1.0 - d) / 0.28, 0, 1)
                img = riso.to_image(cov)
            img.save(OUT / f"{piece}-{ink}.png", optimize=True)


if __name__ == "__main__":
    main()
