---
name: analog-ui
description: Design any page, report, update, deck, newsletter or dashboard so it looks deliberately designed by hand instead of AI-templated, by borrowing a real physical medium and rebuilding its objects in code. Eight built mediums - sketchbook (hand-drawn, pencil, highlighter, doodles, xkcd-style charts), blueprint, museum exhibit, lab notebook, risograph zine, receipt, field journal and departure board - plus the first-principles method for any other. Call it as /analog-ui to have a medium chosen, or /analog-ui sketchbook (or blueprint, museum, ...) to go straight to one. Use when a design feels generic or template-like, or someone asks for "hand-drawn", "sketch", "pencil", "off-beat", "like a real designer made it", or a distinctive look for an update, report, milestone, launch, roadmap, review, pricing or status page. Includes email-safe PNG export.
license: MIT
---

# Analog UI

Generic AI design comes from vague direction ("make it premium", "make it pop"). With nothing
concrete to aim at, the model falls back to its defaults: gradient header, rounded cards, soft
shadows, ALL-CAPS labels. Analog UI gives it a **world** instead of an adjective: a real physical
medium, with its own materials, marks, habits and constraints, that people already know how to read.

## How to call it

| Invocation | What happens |
|---|---|
| `/analog-ui` | Read the content, pick the medium whose real-world job matches it (step 2), say why, then build. |
| `/analog-ui <medium>` | Skip the choice. Load `mediums/<medium>/MEDIUM.md` and build with it. |
| Plain request ("make it hand-drawn", "do it as a blueprint") | Map the words to a medium below and continue as if it were named. |

**Built mediums** (each folder has a `MEDIUM.md` and at least one tested example):

| Argument | Medium | Its real-world job | Depth |
|---|---|---|---|
| `sketchbook` | Designer's sketchbook | Celebrate a milestone, with warmth | Full kit: CSS, SVG symbols, templates, chart script |
| `blueprint` | Architect's blueprint | Plan, sequence, dependencies | Recipe + example |
| `museum` | Museum exhibit and wall placards | Explain results with authority | Recipe + example |
| `lab-notebook` | Engineer's lab notebook (or a flight recorder log) | Reconstruct what happened | Recipe + example |
| `riso-zine` | Risograph zine | Announce something energetic | Recipe, print pipeline + flipbook example |
| `receipt` | Receipt and price tags | Show cost or line-by-line value | Recipe + example |
| `field-journal` | Field researcher's journal | Share voices and observations | Recipe + example |
| `departure-board` | Departure board and air-traffic flight strips | Track live status | Recipe + example |

Match arguments loosely: ignore case, spaces and hyphens (`lab notebook` = `lab-notebook`). A full medium name always wins over an alias.
Aliases: `sketch`, `hand-drawn`, `pencil`, `doodle`, `notebook` → `sketchbook`; `riso`, `risograph`, `zine`, `risograph zine` → `riso-zine`;
`incident`, `postmortem`, `lab record` → `lab-notebook`; `pricing`, `price tag` → `receipt`; `status`, `departures`, `flight strips` → `departure-board`;
`qbr`, `review`, `exhibit`, `museum exhibit` → `museum`; `roadmap`, `architect` → `blueprint`; `feedback`, `research`, `field notes` → `field-journal`.

**Unknown medium** (for example `/analog-ui polaroid`): don't refuse. Run the full method below
to invent it, and offer to save it as a new `mediums/<name>/MEDIUM.md`.

Read only the `MEDIUM.md` you need. Don't load all eight.

**Do the method before you open any example.** Write your own inventory and mapping table for *this*
content (steps 1–5) first. Open the medium's example only afterwards, to see how a technique is
built. Examples are one answer to a different brief; starting from one copies its layout and its
mistakes.
Run the commands below from the skill root.

## The method

Run these steps in order. Write the outputs down before writing code. With a named medium, step 2
is already done and step 3 starts from that medium's inventory.

### 1. Read the content and its job
- What is the one thing the reader must remember? That becomes the single bold move.
- Who reads it, and in what state: skimming exec, curious customer, engineer on call?
- What is the shape of the content: a before and after, a sequence, a comparison, evidence, a plan?

### 2. Pick a medium that already carries that meaning
Choose the medium whose real-world job matches the content's job (see the table above). Don't pick
one because it looks nice. Offer two or three candidates if the brief is open, pick one if it's
clear, and say why in one sentence.

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
| Misregistration (riso, print) | Duplicate the element and offset it 1–3px in a second spot colour, with `multiply` |
| Tape, pins, labels | Absolutely positioned elements with a small rotation and soft shadow |
| Period or trade type | A face that belongs to the medium (handwriting, typewriter, stencil, technical) |
| Charts in the medium | matplotlib styled to match, exported as a transparent PNG (see `mediums/sketchbook/scripts/sketch_chart.py` and `mediums/museum/examples/museum-qbr/make_artifact.py`) |

### 5. Set the restraint rules
- **One bold move** per page: a highlighter, a stamp, a red-pen circle. Everything else is quiet.
- **Three or four ink colours**, all taken from the medium.
- **Tilt only small elements**, within ±2°. Body text stays straight and readable.
- **The style is loose, the facts are not.** Every number, date and name stays exact and sourced.
- **Content beats costume.** If a device makes a number harder to read, cut the device.
- **Lead with meaning, and don't be snarky.** The hero is the number that measures the mission.
  When the occasion *is* a count (a stars or users milestone), that count can lead; put the number
  that shows real value right under it. Report your progress, not a rival's weakness.
- **Arithmetic on given facts is fine; new facts are not.** "38 minutes" from 09:12–09:50 or a
  month range from a schedule is allowed; a figure the brief can't produce is not.
- **Conventions never license invented data.** If a medium's object needs a value the brief doesn't
  give (a page number, a log excerpt, a duration, a date), drop the object or fill it with a real
  fact. Stamps such as "Draft" or "Not to scale" go on only if they're true.
- **What counts toward the limits.** The ±2° tilt applies to anything carrying text; tape and pure
  decoration can tilt more. The ink count is the marks you draw, not the paper (ruled lines, margin
  rules, grid). A medium's own conventions in the accent colour (a revision delta, a margin rule)
  are not a second bold move.

### 6. Avoid the tells of generated design
Unless the medium itself calls for them, don't use:
- gradient-wash headers;
- identical rounded cards with the same grey shadow;
- tracked-out ALL-CAPS labels above every heading;
- emoji as icons, or "→" appended to every link;
- a headline split into a plain line and a muted italic line;
- a slogan for a headline. The headline says what the reader gets or must know ("Make any page
  look made by hand"), not a clever line about the method ("One method, eight mediums");
- cream background, serif display font and terracotta accent;
- black background with a single acid-green accent.

### 7. Build, render, look, fix
1. Build the page from your mapping table.
2. Render it in a headless browser at desktop width and at 390px.
3. **Look at the screenshots.** Code review alone won't catch visual problems.
4. Fix collisions, overflow, unreadable contrast, class clashes, and anything that reads as costume.
5. Repeat until a stranger could read the key number in three seconds.

Render with a real viewport and wait for web fonts. Chrome's `--window-size` is unreliable at
phone widths, so use Playwright (or load the page in a 390px iframe):

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    try:
        b = p.chromium.launch()                       # Playwright's bundled Chromium
    except Exception:
        b = p.chromium.launch(channel="chrome")       # or the installed Google Chrome
    for name, w in (("desktop", 1280), ("phone", 390)):
        pg = b.new_page(viewport={"width": w, "height": 900})
        pg.goto("file:///abs/path/page.html", wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.screenshot(path=f"{name}.png", full_page=True)
```

Lessons the samples taught:
- Check class names against the medium's own vocabulary. `.board` the container vs `.board` the
  status broke the departure board; `.big` the metric vs `.big` the timeline item broke the sketchbook.
- A stamp or mark must never cover a number. Give it its own space.
- On phones, redraw wide content (timelines, Gantts, wide tables, diagrams) as a vertical stack in
  reading order. Don't scroll it sideways: a scroller hides content, and blind reviews marked down
  every sideways-scrolled plan. Hide secondary columns of a true grid instead. If a scroller is
  unavoidable, start it at the beginning, give it `tabindex="0"`, and keep the bold move visible.
- Put any "fictional" or "illustrative" disclaimer once, in the footer, not on each element.
- A drawn circle around text needs about 1.4× the text box, or it cuts the corner letters, and
  circling an inline span breaks when the text wraps. Circle a block, or keep the circled text short.
- If the bold move sits below the first phone screen, say the change in words in the first screen too.
- Check digits and capitals in hand fonts: some render "H1" as "Hl". Set codes and IDs in the mono face.
- Long values in fixed-width cards wrap or overflow. Put the "from" value on its own line.
- Grid children holding code or tables need `min-width:0`, or the page overflows.
- Animate only on real change. Blinking forever is noise, and must stop under reduced motion.

### 8. Plan delivery
- **Web:** `python scripts/inline_assets.py page.html -o page.single.html` bundles CSS and images
  into one file. Web fonts still load from the network and fall back to system fonts offline.
- **Email:** clients strip web fonts, filters and SVG, so send it as images.
  `python scripts/export_email.py page.html --slices 4` renders at 2x and cuts slices only at
  blank gaps; then open `email/paste-into-email.html`, select all, copy, and paste into a message.
- **Slides:** screenshot sections at 2x.
- Tell the user the trade-off: image text can't be searched or selected. For a formal exec audience,
  offer a clean typographic version too.

Both scripts work for every medium. Install their dependencies with `pip install -r requirements.txt`.

## Output checklist
- [ ] The medium and why it fits are stated in one sentence.
- [ ] The mapping table was written before opening the example, and every device has a job.
- [ ] Exactly one bold move, and it is visible without scrolling sideways on a phone.
- [ ] All numbers are exact and sourced.
- [ ] Desktop and mobile renders were inspected and fixed.
- [ ] A delivery format was chosen and its trade-offs stated.

## Files
- `mediums/<medium>/MEDIUM.md`: inventory, build table, palette, type and pitfalls for one medium.
- `mediums/<medium>/examples/`: built, render-tested samples.
- `mediums/sketchbook/assets/`: the full sketchbook kit (`sketchbook.css`, `symbols.html`,
  `page-skeleton.html`, `newsletter-template.html`).
- `scripts/`: medium-agnostic tools (email export, asset inlining).
- Gallery of all eight samples (in the repo, not copied on install):
  https://rohitjz.github.io/skills/skills/design/analog-ui/gallery/
