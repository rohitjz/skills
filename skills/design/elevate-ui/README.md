# elevate-ui

A Claude skill that turns a flat, generic, "AI-generated-looking" web page into something that looks like a tasteful designer built it.

It isn't a theme or a component library. It's a **repeatable pass** over three axes, plus the one fix that matters most.

## The idea

Pages that read as "AI made this" share the same tells: emoji as icons, flat 1px-bordered cards, a static or missing illustration, nothing that responds to the cursor, everything on one plane. Once you can name the tells, the fix is mechanical, not a matter of innate taste.

The skill works on three axes:

- **Light** — film grain, soft radial glows, lit top edges. Surfaces that look lit instead of screen-printed.
- **Depth** — glass-dome card shadows, true refractive liquid-glass chrome, parallax. A z-axis instead of one flat plane.
- **Life** — a cursor-reactive spotlight, one animated signature illustration, staggered reveals. Motion with intent.

And the highest-impact single change: **replace every emoji with a bespoke SVG line-icon set.** That alone moves a page most of the way from templated to designed.

## What it fixes

| Tell | Fix |
|------|-----|
| Emoji as icons (🚀 🧠 ✅) | A hand-built SVG line-icon sprite |
| Flat cards (fill + 1px border) | Layered glass-dome shadow |
| Static / missing hero visual | One animated signature illustration |
| Nothing responds to the cursor | Cursor spotlight + parallax |
| Flat color, no texture | Film grain + warm glows |
| Floating chrome is a blurred bar | True refractive liquid glass |

## Install

Clone it into your Claude skills directory:

```bash
git clone https://github.com/rohitjz/elevate-ui.git ~/.claude/skills/elevate-ui
```

Or, if you use the skills CLI:

```bash
npx skills add rohitjz/elevate-ui
```

Then it triggers automatically in Claude Code when you say things like "make this less AI," "elevate this page," "visualize like a tasteful designer," or "go visual++," and you can always invoke it by name.

## What's inside

```
elevate-ui/
├── SKILL.md                    # the playbook: light/depth/life, the tells, the procedure
└── references/
    ├── icons.md                # SVG icon-sprite pattern + a 16-icon starter set
    ├── depth.md                # glass-dome + soft-elevation card shadows
    ├── liquid-glass.md         # true refractive glass for nav/chrome (dark + light tokens)
    └── motion.md               # grain, cursor spotlight, animated hero, scroll reveals
```

## Self-contained by design

Every recipe is inline SVG, CSS, and JS. No icon fonts, no CDN libraries, no AI-generated raster images (those ironically read as "AI" and bloat the file). It's palette-agnostic with one example theme; pass your own brand colors and it adapts. The output stays a single portable file that loads instantly and works offline.

## Restraint is the point

The failure mode is overshooting into gaudy. The skill bakes in defaults that stay tasteful: grain at ~5% opacity, sparse low-opacity glows, slow subtle motion, one centerpiece not ten, readability over effect, and `prefers-reduced-motion` honored.

## Origin

Extracted from a real build, an interactive [Harness Engineering crash course](https://rohitjz.github.io/harness-engineering-crash-course/), where these techniques took a flat explainer to a designed one over several iterations. Battle-tested, not theoretical.

## License

[MIT](LICENSE)
