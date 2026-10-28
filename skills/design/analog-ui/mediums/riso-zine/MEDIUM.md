# Risograph zine

Call with `/analog-ui riso-zine`.

**Use for:** launch announcements, community updates, internal events, "what's new" pages.

| Object | Build | Meaning |
|---|---|---|
| Two or three spot inks | e.g. fluorescent pink `#FF48B0` and medium blue `#3255A4` on cream | Energy and personality |
| Misregistration | The same element duplicated, offset 1–3px in the second ink, with `mix-blend-mode: multiply` | Handmade, printed in a run |
| Grain | An SVG noise overlay at about 8% opacity | Ink on paper |
| Overprint | Overlapping shapes multiply into a third colour | Ideas combining |
| Halftone images | A CSS radial-gradient dot pattern masked over a photo | Cheap printing, a bold look |
| Big collage type | Huge condensed type, cut out, slightly rotated | Launch volume |
| Staple and fold marks | Two small grey bars, a faint centre crease | A booklet you can pass around |

**Type:** a heavy condensed face (Anton, Bebas Neue) plus a quirky text face (Space Grotesk).
**Pitfall:** loud by nature. Keep it to one spread of energy, then readable columns for details.

## Two ways to build it

- **Live web page in riso style** (CSS only): the table above. Fast, editable, good for a "what's new" page.
- **A real printed zine** (flipbook of page images): when the launch should feel like an object people pass around. Design each page as an HTML artboard, render it once per ink, then print the passes through `scripts/riso.py`. This gives true riso grain, mottled solids and drum drift that CSS cannot fake.

### Printed-zine pipeline (`scripts/riso.py`)
1. **Artboards.** One 3:4 section per page. Style with ink variables so each pass renders the active ink black and the other transparent. Knockouts are paper-white shapes visible only in their ink's pass.
2. **Art.** Draw or source two-ink art. To reuse existing art (a mock, a sketch), `separate(img, paper, inks)` unmixes it into one coverage map per ink with a transparent-ink model. Measure against the true paper colour, or a tinted sheet comes back as ink.
3. **Passes.** `render_ink_passes(html, size)` screenshots each ink at 2x.
4. **Print.** `print_page(layers, inks, seed, offsets)` adds grain, uneven solids, dropouts and per-page drum offsets, then multiplies onto paper.
5. **Anything that must scan** (a QR code): print it with `overprint_solid()` after the grain, never through it. Grain breaks QR finder patterns.
6. **Export** WebP at 1800 (zoom), 900 (spread) and a thumbnail; write each page's words into its alt text.

### Flipbook viewer pattern
- Closed cover beside the open spread; spreads pair 2-3, 4-5, then the last page with the back cover.
- Page turns in CSS 3D (one leaf element per turn), no library. Instant swap under reduced motion.
- Arrow buttons, ArrowLeft/ArrowRight, pointer swipe, thumbnails, spread/single toggle (single by default on phones), and click-to-zoom in a `<dialog>` that returns focus.
- An `aria-live` page indicator ("Pages 2-3 of 6").

## Examples
Open these after writing your own inventory and mapping table, for technique only.
- `examples/story-launch-zine/`: the printed-zine pipeline and flipbook board for Story, an app in development. Rebuild pages with `src/build.py [page numbers]`; `src/extract_art.py` shows separating art from a mock.
- `examples/riso-launch/index.html`: the CSS-only web page. Northwind Notes is a fictional product; all figures are illustrative.

## Lessons from the samples
- Give stacked display headings a line-height near 1, or the misregistered copies of each line collide.
- Keep decorative staples and the centre fold out of content sections; give sections a solid paper background so the fold only shows on the cover.
- Put the grain overlay on top with `pointer-events:none` so it never blocks a click.
- Rank-normalise grain noise to a uniform threshold. Blurred noise is bell-shaped and silently drops light tints.
- Add a small coverage floor before printing, or source noise speckles the paper.
- Every page in a flipbook needs real content. Do not invent testimonials or logos to fill a "community" page; use true claims instead.
