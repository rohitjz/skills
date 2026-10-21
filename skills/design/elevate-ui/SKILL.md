---
name: elevate-ui
description: >-
  Transform a flat, generic, or AI-generated-looking web page into something
  that looks like a tasteful designer built it. Use this WHENEVER the user says
  a page or component "looks basic / looks like AI / looks generic / feels flat
  / looks templated," or asks to "elevate / level up / polish / make it premium
  / make it less AI / visualize like a tasteful designer / go visual++ / add
  visuals," and also proactively right after you build any landing page,
  dashboard, marketing site, or single-file HTML artifact that should look
  professional. It replaces emoji with bespoke SVG icons, and adds light (grain,
  glows), depth (glass-dome card shadows, liquid-glass chrome), and life (cursor
  spotlight, an animated signature illustration). Palette-agnostic and fully
  self-contained (inline SVG/CSS/JS, no CDNs). Reach for it even when the user
  never says the word "design," as long as a web UI needs to look intentional
  rather than auto-generated.
---

# Elevate UI: from flat to designed

## Why this exists

Most pages that "look like AI made them" share the same handful of tells. Once you can name them, the fix is mechanical, not a matter of innate taste. This skill turns "make it look designed" into a repeatable pass.

Design quality here lives on three axes. Run a flat page through all three and it stops reading as templated:

- **Light** — surfaces that look *lit*: film grain, soft radial glows, lit top edges, gradient accents.
- **Depth** — a z-axis: layered shadows, glass-dome cards, foreground/background separation, parallax.
- **Life** — motion with intent: cursor-reactive surfaces, one breathing/animated centerpiece, staggered reveals.

The reason this works: "flat + static + emoji" is the visual signature of a template. Real design has hierarchy, dimension, and response. You are not decorating; you are adding the cues a human designer adds without thinking.

## The AI tells, and the fix for each

Audit the page against this list first. Fix in roughly this order (biggest tell first).

| Tell | Why it reads as AI | Fix |
|------|--------------------|-----|
| **Emoji as icons/illustration** (🚀 🧠 ✅) | No design system uses emoji as visual language | Bespoke SVG line-icon set → `references/icons.md` |
| **Flat cards** (solid fill + 1px border) | Everything on one plane, zero light | Glass-dome / layered depth → `references/depth.md` |
| **Static or missing hero visual** | Nothing to look at; reads as a doc, not a product | One animated signature illustration → `references/motion.md` |
| **Nothing responds to the cursor** | Static pages feel dead | Cursor spotlight + parallax → `references/motion.md` |
| **Pure flat color, no texture** | Synthetic, screen-printed look | Film grain + warm glows → `references/motion.md` |
| **Generic blue / bootstrap palette** | The default = the tell | Pick an intentional theme → see **Palette** below |
| **Floating chrome that's just a blurred bar** | Misses the premium "glass" cue | Liquid glass → `references/liquid-glass.md` |

## The procedure

Work top to bottom. Each step is cheap on its own; together they compound.

1. **Audit.** Open the page (or read the file). List which tells above apply. Tell the user your plan in one or two sentences before you start.
2. **Pick a palette and one signature motif** (see below). State the choice up front.
3. **Light.** Add the film-grain overlay. Add one or two soft radial glows behind key headings. (`references/motion.md`, `references/depth.md`)
4. **Icons.** Replace every emoji with the inline icon sprite. This is the single highest-impact change. (`references/icons.md`)
5. **Depth.** Apply the card-depth recipe: glass-dome shadow on tiles, softer layered elevation on big containers. (`references/depth.md`)
6. **Chrome.** Apply liquid glass to floating chrome only: sticky nav, search inputs, hero buttons. Not to body cards. (`references/liquid-glass.md`)
7. **Life.** Add the cursor spotlight to tile grids. Build one animated signature illustration for the hero (rotating rings, a breathing core, gentle parallax). (`references/motion.md`)
8. **Verify.** Render in a real browser. Screenshot desktop and mobile. Confirm no console errors, text stays readable, and motion respects `prefers-reduced-motion`. Then show the user before declaring done.

You don't have to do all eight every time. Even steps 3–5 alone (grain, icons, depth) transform a page. Match the ambition to what the user asked for.

## Palette (stay agnostic)

The skill is palette-agnostic on purpose so it works for anyone. Apply these principles, then plug in whatever colors the project already uses or the user gives you:

- **Surfaces: charcoal, not pure black.** Pure `#000` reads cheap. Use something like `#0b0d13` for the page and a slightly lighter `#161a24` for cards.
- **One warm signal accent.** A single bright, warm hue carries emphasis (a headline word, the active state, key numbers). Warm accents feel alive; a cold blue accent reads default.
- **One cool secondary** for contrast and "good/positive" states.
- **Semantic colors stay semantic.** Red = bad, green = good. Never use the brand accent to mean "error."
- **Text: off-white, not `#fff`.** Pure white on dark vibrates. Use `#eef1f7` for primary, a muted gray for secondary.

**Example theme used in the recipes (swap freely):** page `#0b0d13`, surface `#161a24`, warm accent (amber) `#ffb454`, cool accent (teal) `#34d1bf`, bad `#ff6b6b`, good `#5fd97f`, ink `#eef1f7`, muted `#aeb6c6`. If the user has a brand palette, use theirs and keep only the structure.

## Signature motif

A tasteful page repeats **one** visual idea instead of scattering clip-art. Pick a single motif that encodes the page's concept, then reuse it: as the hero illustration, as small section accents, as the empty-state. Build it from precise geometry (circles, frames, nodes, lines), never a literal drawing of a hard object (a hand-coded horse or rocket looks amateur; abstract it).

Example: for a page about "structure around a system," the motif was *a glowing core held inside a scaffold* — used full-size and animated in the hero, and echoed as small framed-core marks elsewhere.

## Restraint (this is what keeps it tasteful)

The failure mode is overshooting into gaudy. Defaults that stay classy:

- **Grain** opacity ~0.05, never more. It should be felt, not seen.
- **Glows** are soft and sparse. One or two per viewport, low opacity. A page lit like a Christmas tree reads worse than a flat one.
- **Motion** is slow and subtle. A core that breathes over ~4s, rings that rotate over ~50s. Nothing should be distracting while reading.
- **One centerpiece, not ten.** A single animated hero earns attention. Ten animated things earn an exit.
- **Readability always wins.** If a glow or glass effect hurts contrast, dial it back. Run the squint test.
- **Honor `prefers-reduced-motion`.** Disable the animations for users who ask for less.

## Self-contained, always

Keep everything inline: SVG sprites, CSS, JS, the grain as a data-URI. No external icon fonts, no CDN libraries, no AI-generated raster images (those ironically read as "AI" and bloat the file). The payoff is a page that loads instantly, works offline, and is one portable file.

## Reference files (load as needed)

- `references/icons.md` — the bespoke SVG line-icon system: sprite pattern, sizing/color, and a ready-to-paste 16-icon starter set.
- `references/depth.md` — card depth: the glass-dome shadow for tiles, soft elevation for containers, gradient borders, hover lift.
- `references/liquid-glass.md` — true refractive liquid glass for floating chrome (SVG displacement + layered dome shadow), with validated dark and light tokens.
- `references/motion.md` — film grain, cursor spotlight, the animated hero illustration, and scroll reveals, all with `prefers-reduced-motion` guards.
