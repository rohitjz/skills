---
name: sketchbook-ui
description: Design any web page, landing page, blog post, report, dashboard or newsletter in a hand-drawn "sketchbook" style, with pencil-wobbly boxes, a highlighter on the key number, struck-through "before" values, circled words, ink arrows, ticks, sticky notes, a taped-in xkcd-style chart, and doodled icons, while every fact stays exact. Includes a drop-in CSS and SVG kit, a chart script, and email-safe PNG export. Use when someone asks for a "hand-drawn", "pencil", "sketch", "notebook", "doodle", "off-beat" or "made by a designer, not a template" look, or wants a milestone, launch or celebration page or email that feels personal.
license: MIT
---

# Sketchbook UI

A design system that makes an HTML page look drawn by hand on paper, without losing precision.
It works for any page: landing pages, blog posts, changelogs, reports, portfolios, event pages.
**The marquee use is a milestone newsletter**, where warmth matters as much as the numbers.

## When to use

- The user asks for hand-drawn, pencil, sketch, notebook, doodle, zine or "off-beat" styling.
- A page should feel personal: a celebration, a launch, a team update, a story with numbers.
- A redesign of an existing page or post that reads as generic.

**Don't use it** for dense data apps, forms-heavy flows, or anything that has to look official.
For a formal exec audience, offer a clean typographic version with the same content as well.

## The kit

| File | What it is |
|---|---|
| `assets/sketchbook.css` | The whole look: paper, type, marks, boxes, components. Tokens in `:root`. |
| `assets/symbols.html` | Paste once after `<body>`: the pencil filter plus reusable doodles (`arrow`, `tick`, `house`, `star`, `lock`, `big-arrow`, `strike`, `uline`, `circle`). |
| `assets/page-skeleton.html` | Minimal starting page for any site. |
| `assets/newsletter-template.html` | The marquee newsletter layout with `{{PLACEHOLDERS}}`. |
| `scripts/sketch_chart.py` | CSV or XLSX to a pencil-style chart (transparent PNG), with milestone callouts. |
| `scripts/export_email.py` | Renders a page and cuts it into PNG slices for Outlook or Gmail. |
| `scripts/inline_assets.py` | Bundles CSS and images into one self-contained HTML file. |
| `examples/kit/` | Every component on one page. Open it before designing. |
| `examples/lets-encrypt-10-years/` | Marquee example: a public blog post redrawn as a sketchbook page. |

### Components (classes in `sketchbook.css`)

- **Paper:** `.sheet` (720px) or `.sheet.wide` (1040px); textures `.graph`, `.ruled`, `.margin`.
- **Type:** `.hand` (Caveat), Kalam body, `.kicker` (tilted label), `.lede`, `.fine`; `h2` with `<svg class="uline"><use href="#uline"/></svg>`.
- **Marks:** `.hl` highlighter, `.strike` with `#strike`, `.circled` with `#circle`, pencil-underline links, `.tag`.
- **Hero:** `.was.strike` (old value) above `h1.now` with an `.hl` span (new value).
- **Boxes:** `.sk` pencil box (`.sk.blue` for emphasis); `.grid` of `.sk.check` cards with `#tick`.
- **Metric:** `.big` (from → to with `#big-arrow`), `.note`, `.sub` / `.sub.prime` rows.
- **Figure:** `.taped` card with `.tape.l` / `.tape.r`, plus a `.caption`.
- **Lists:** `.arrows` (with `#arrow`), `.timeline` (`li.key` for major moments).
- **Interactive:** `.btn` / `.btn.ghost`, `.nav` (underlines on hover or `aria-current`), `.sticky`.
- **Thanks:** `.village` of `.house` items, `.signoff`, `.sig`, `.foot`.

## How the look is made

- **Wobble:** pencil borders use an irregular `border-radius` and an SVG `feTurbulence` +
  `feDisplacementMap` filter. A faint, offset second outline reads as a redrawn stroke.
- **Highlighter:** a skewed gradient behind the bottom 42% of the text, with ragged ends.
- **Doodles:** hand-drawn cubic Bézier paths in `<symbol>`s with round caps, reused through `<use>`.
- **Chart:** `matplotlib` in `xkcd` mode, a handwriting font, hatched area, curved arrow callouts,
  exported transparent and trimmed so it fills its taped card.
- **Palette:** graphite `#3A3A38`, pencil blue `#2F5BB7`, correction red `#C8463C`, highlighter
  `rgb(255,222,74)`, sticky `#FFF3A8`, tape beige.

## Design rules

1. **One highlighter per page.** It marks the single thing to remember.
2. **Tilt sparingly.** Only kickers, notes, tags, captions and the sign-off, within ±2°. Body text stays straight.
3. **Hand fonts for display, never for long text.** Kalam body text is fine for prose under about 600 words. For longer pages use a clean serif or sans for body text and keep Caveat for headings and marks.
4. **Precision survives the style.** Exact numbers, real dates, cited sources. Never invent data.
5. **Lead with meaning.** The hero is the number that measures the mission, not the vanity count.
6. **Don't be snarky.** Report your share and your progress, not a rival's weakness.
7. **Accessibility:** decorative SVGs get `aria-hidden="true"`, charts get a full `alt`, and links keep a visible focus ring (already in the CSS).

## Workflow

1. **Get the content first.** Collect the headline number (before → after), the supporting facts,
   any time series, what's next, and who to thank. For a redesign, read the source and pull the
   facts from it and from any public data it cites.
2. **Pick a page:** `page-skeleton.html` for a general site, `newsletter-template.html` for an
   update. Copy `sketchbook.css` next to it, or link to it.
3. **Draw the chart** if there is a time series:
   ```bash
   pip install -r requirements.txt
   python scripts/sketch_chart.py data.csv --date date --primary users --out chart.png
   # options: --secondary col --secondary-format ratio|pct|count, --smooth 7, --every 3,
   #          --mark "2020-02-27|1 billionth cert" (repeatable), --primary-label "..."
   ```
4. **Compose** from the components. Keep sections short: one idea per box.
5. **Look at it.** Render at desktop and 390px wide and inspect the images. Check for label
   collisions, overflow, and class clashes (for example `.big` is the metric; timelines use `li.key`).
6. **Ship:**
   - Web: `python scripts/inline_assets.py page.html -o page.single.html`.
   - Email: `python scripts/export_email.py page.html --slices 4`, then open
     `email/paste-into-email.html`, select all, copy, and paste into a new message. Email clients
     strip web fonts and SVG filters, so images are the faithful way to send it. Recipients can't
     select or search image text, so say so.

## Example

`examples/lets-encrypt-10-years/` redraws the public post "10 Years of Let's Encrypt Certificates"
(Dec 9, 2025). The chart is drawn from Let's Encrypt's public daily stats. It is an unofficial
example, credited in the footer and not affiliated with Let's Encrypt or ISRG.

## Other mediums

This skill is one medium, fully built. For other looks (blueprint, museum placard, lab notebook,
risograph zine, receipt, field journal, departure board) and the general method behind them, use
`medium-first-design`.
