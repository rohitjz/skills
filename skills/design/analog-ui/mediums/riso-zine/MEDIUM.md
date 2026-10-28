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

## Example
`examples/riso-launch/index.html`. Open it after writing your own inventory and mapping table, for technique only. Northwind Notes is a fictional product; all figures are illustrative.

## Lessons from the sample
- Give stacked display headings a line-height near 1, or the misregistered copies of each line collide.
- Keep decorative staples and the centre fold out of content sections; give sections a solid paper background so the fold only shows on the cover.
- Put the grain overlay on top with `pointer-events:none` so it never blocks a click.
