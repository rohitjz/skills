---
name: medium-first-design
description: Design any page, report, deck, newsletter or dashboard by borrowing a real physical medium (sketchbook, blueprint, museum placard, lab notebook, risograph zine, receipt, field journal, flight strip) and rebuilding its objects and marks in code, so the result looks deliberately designed instead of AI-templated. Works from first principles - name the medium, inventory what is physically in it, map each object to a CSS/SVG technique, give every mark a job from the content, spend boldness in one place, then render and fix. Use when someone says a design feels generic, asks for something "hand-designed", "off-beat", "like a real designer made it", or wants a distinctive look for an update, launch, review, roadmap or report. sketchbook-ui is the fully built example of one medium.
license: MIT
---

# Medium-first design

Generic AI design comes from vague direction ("make it premium", "make it pop"). With nothing
concrete to aim at, the model falls back to its defaults: gradient header, rounded cards, soft
shadows, ALL-CAPS labels. The fix is to give it a **world**, not an adjective.

A physical medium is a world. It brings its own materials, marks, habits and constraints, and
people already know how to read it. Rebuild those in code and the page stops looking like a
template.

## The method

Run these steps in order. Write the outputs down before writing code.

### 1. Read the content and its job
- What is the one thing the reader must remember? That becomes the single bold move.
- Who reads it, and in what state: skimming exec, curious customer, engineer on call?
- What is the shape of the content: a before and after, a sequence, a comparison, evidence, a plan?

### 2. Pick a medium that already carries that meaning
Choose the medium whose real-world job matches the content's job. Don't pick one because it looks
nice. See `references/medium-library.md` for worked mediums.

| Content job | Medium that does this job in real life |
|---|---|
| Celebrate a milestone, with warmth | Designer's sketchbook |
| Plan, sequence, dependencies | Architect's blueprint |
| Explain results with authority | Museum exhibit and wall placards |
| Reconstruct what happened | Lab notebook, flight recorder log |
| Announce something energetic | Risograph zine |
| Show cost or line-by-line value | Receipt, price tag |
| Share voices and observations | Field researcher's journal |
| Track live status | Departure board, air-traffic flight strips |

Offer two or three candidates if the brief is open, pick one if it's clear, and say why.

### 3. Inventory the medium
List what is physically there, in four groups:
- **Surface:** paper, film, board, screen; its texture, colour, edges.
- **Marks:** how people write on it (pencil, stamp, typewriter, chalk, pen correction).
- **Objects:** what gets attached (tape, pins, labels, tickets, clips, stamps).
- **Conventions:** layout habits a native reader expects (title block, catalogue number,
  line items with a total, dated entries).

Aim for 8–12 items. Real designers notice the small habits, not just the big texture.

### 4. Map each object to a technique, and give it a job
Build a table before coding: *object → how to build it → what it means in this content*.
Drop any object that can't name its meaning. Common building blocks:

| Effect | Technique |
|---|---|
| Hand-drawn wobble | SVG `feTurbulence` + `feDisplacementMap` filter; uneven `border-radius` |
| Ink, stamp, chalk texture | Same filter at higher scale, `mix-blend-mode: multiply`, slight opacity |
| Drawn marks (arrows, ticks, circles) | Hand-placed cubic Bézier SVG paths with round caps, reused through `<symbol>` |
| Paper and grids | Layered `linear-gradient` backgrounds |
| Misregistration (riso, print) | Duplicate the element and offset it 1–2px in a second spot colour, with `multiply` |
| Tape, pins, labels | Absolutely positioned elements with a small rotation and soft shadow |
| Period or trade type | Pick a face that belongs to the medium (handwriting, typewriter, stencil, technical) |
| Charts in the medium | matplotlib styled to match (xkcd mode for hand-drawn, thin cyan lines for blueprint), exported as a transparent PNG |

### 5. Set the restraint rules
- **One bold move** per page: a highlighter, a stamp, a red-pen circle. Everything else is quiet.
- **Three or four ink colours**, all taken from the medium.
- **Tilt only small elements**, within ±2°. Body text stays straight and readable.
- **The style is loose, the facts are not.** Every number, date and name stays exact and sourced.
- **Content beats costume.** If a device makes a number harder to read, cut the device.

### 6. Avoid the tells of generated design
Unless the medium itself calls for them, don't use:
- gradient-wash headers;
- identical rounded cards with the same grey shadow;
- tracked-out ALL-CAPS labels above every heading;
- emoji as icons, or "→" appended to every link;
- cream background, serif display font and terracotta accent;
- black background with a single acid-green accent.

### 7. Build, render, look, fix
1. Build the page from your mapping table.
2. Render it in a headless browser at desktop width and at 390px.
3. **Look at the screenshots.** Code review alone won't catch visual problems.
4. Fix collisions, overflow, unreadable contrast, class clashes, and anything that reads as costume.
5. Repeat until a stranger could read the key number in three seconds.

```bash
chrome --headless=new --hide-scrollbars --window-size=860,3000 --screenshot=desk.png page.html
```

### 8. Plan delivery
- **Web:** inline CSS and images into one file.
- **Email:** clients strip web fonts, filters and SVG, so export the page as PNG slices cut at
  blank gaps. `sketchbook-ui/scripts/export_email.py` does this for any page.
- **Slides:** screenshot sections at 2x.
- Tell the user the trade-off: image text can't be searched or selected. For a formal audience,
  offer a clean typographic version too.

## Output checklist
- [ ] The medium and why it fits are stated in one sentence.
- [ ] The mapping table exists, and every device has a job.
- [ ] Exactly one bold move.
- [ ] All numbers are exact and sourced.
- [ ] Desktop and mobile renders were inspected and fixed.
- [ ] A delivery format was chosen and its trade-offs stated.

## Related
- `sketchbook-ui`: the pencil-sketchbook medium, fully built with CSS kit, chart script and email export.
- `references/medium-library.md`: eight mediums with inventories, mappings and pitfalls.
- `examples/blueprint-roadmap/`: the blueprint medium applied to a product roadmap.
