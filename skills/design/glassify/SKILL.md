---
name: glassify
description: Generate a complete, production-ready single-file website using Rohit's validated glassify pattern (SVG displacement refraction + 8-layer dome shadow), NOT backdrop-filter glassmorphism. Content behind glass is REFRACTED (distorted like looking through curved glass), not blurred. This is Rohit's brand signature, locked in on 2026-04-22 and refined across dark and light themes on 2026-04-24. Theme-agnostic: works on Linear dark, Sand and Sky, Warm Authority, Primary light. Use for landing pages, product launch sites, portfolios, SaaS marketing, event microsites, and any floating UI chrome. Trigger with "glassify," "liquid glass," "Apple glass," "iOS 26 style," or "make this look premium." MUST read reference_liquid_glass_pattern memory before building.
best_for:
  - Landing pages (product, startup, waitlist)
  - Portfolio and personal sites
  - Product launch sites
  - Sticky nav bars, hero overlays, modal backdrops, floating chrome
  - Event and conference microsites
  - Hackathon and demo day sites
estimated_time: "3-7 min"
---

# Liquid-Glassify

Rohit's brand-signature Liquid Glass treatment packaged as a skill. This is NOT backdrop-filter blur glassmorphism. Real Liquid Glass refracts content behind it using an SVG displacement filter and layers 8 box-shadows to build a 3D glass dome.

## READ FIRST

**Before generating any glass, load the canonical memory file:** `~/.claude/memory/reference_liquid_glass_pattern.md`. It has the validated filter parameters, tint values per theme, and the failure modes log from previous iterations. The values in this skill come from that memory but the memory is authoritative. If this skill drifts, trust the memory.

Also read: `~/.claude/memory/feedback_liquid_glass_default.md` (when to apply, when NOT to) and `~/.claude/memory/reference_brand_system.md` (Rohit's theme system, which wraps this glass treatment).

## Frosted Glass vs Liquid Glass (Core Distinction)

**Frosted glass** (wrong, what I built first and Rohit rejected):
- `backdrop-filter: blur(20px) saturate(160%)` + opaque tint
- Looks like shower glass. Content behind is diffuse and unreadable.
- What Rohit called "pretty frosted. Not really liquid glass."

**Liquid glass** (Rohit's brand signature):
- SVG `feTurbulence` + `feDisplacementMap` filter, applied via `backdrop-filter: url('#id')`. Content behind is **distorted** like looking through curved glass, not blurred.
- Layered box-shadow (8-9 inset + outer layers) that creates bright top-left edges, dark bottom-right edges, inner glow, outer halo. This builds a 3D glass dome.
- Very low blur (1-4px), just enough to soften the displacement edges.
- Text behind is HINTED AT, not clearly readable, not invisible.

The 21st.dev `liquid-glass-button` + acquired.fm podcast episodes page are the reference aesthetic. Apple's visionOS / iOS 26 UI is the inspiration.

## The Two-Part Recipe

### Part 1: SVG displacement filter (the refraction)

Inject once per page near the start of `<body>`. Two sizes (bigger filter for big elements, smaller for pills). These values were validated on 2026-04-22; do not re-derive them.

```html
<svg class="lg-svg" aria-hidden="true" focusable="false">
  <defs>
    <!-- For nav bars, hero overlays, large sticky panels -->
    <filter id="liquid-distort" x="0%" y="0%" width="100%" height="100%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.006 0.008" numOctaves="1" seed="5" result="turb"/>
      <feGaussianBlur in="turb" stdDeviation="4" result="softNoise"/>
      <feDisplacementMap in="SourceGraphic" in2="softNoise" scale="8" xChannelSelector="R" yChannelSelector="B"/>
    </filter>
    <!-- For pills, buttons, small search inputs -->
    <filter id="liquid-distort-sm" x="0%" y="0%" width="100%" height="100%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.012 0.015" numOctaves="1" seed="7" result="turb"/>
      <feGaussianBlur in="turb" stdDeviation="2" result="softNoise"/>
      <feDisplacementMap in="SourceGraphic" in2="softNoise" scale="5" xChannelSelector="R" yChannelSelector="B"/>
    </filter>
  </defs>
</svg>
```

Hide the SVG:
```css
.lg-svg { position: absolute; width: 0; height: 0; pointer-events: none; overflow: hidden; }
```

### Part 2: 8-layer dome shadow (the glass edges)

**Do not collapse this into one shadow.** The layering is what makes it look like a 3D glass dome. Each layer does a specific job.

**Light/cream theme dome shadow (validated default):**
```css
--lg-shadow:
  0 0 6px rgba(0, 0, 0, 0.03),
  0 2px 8px rgba(0, 0, 0, 0.08),
  inset 2.5px 2.5px 0.5px -2.5px rgba(255, 255, 255, 0.95),
  inset -2.5px -2.5px 0.5px -2.5px rgba(0, 0, 0, 0.28),
  inset 1px 1px 1px -0.5px rgba(255, 255, 255, 0.7),
  inset -1px -1px 1px -0.5px rgba(0, 0, 0, 0.14),
  inset 0 0 6px 6px rgba(255, 255, 255, 0.08),
  inset 0 0 2px 2px rgba(255, 255, 255, 0.05),
  0 0 12px rgba(255, 255, 255, 0.15);

--lg-shadow-sm: /* ~40% scaled for pills */
  0 0 4px rgba(0, 0, 0, 0.03),
  0 1px 4px rgba(0, 0, 0, 0.08),
  inset 1.5px 1.5px 0.3px -1.5px rgba(255, 255, 255, 0.9),
  inset -1.5px -1.5px 0.3px -1.5px rgba(0, 0, 0, 0.25),
  inset 0.5px 0.5px 0.5px -0.25px rgba(255, 255, 255, 0.6),
  inset -0.5px -0.5px 0.5px -0.25px rgba(0, 0, 0, 0.12),
  inset 0 0 3px 3px rgba(255, 255, 255, 0.06),
  0 0 8px rgba(255, 255, 255, 0.12);
```

**Dark theme dome shadow (e.g., Linear):**
Dark mode is "lit from within," so both corners stay on the white side. The outer shadow carries the darkness.
```css
--lg-shadow:
  0 0 6px rgba(0, 0, 0, 0.2),
  0 4px 14px rgba(0, 0, 0, 0.45),
  inset 2.5px 2.5px 0.5px -2.5px rgba(255, 255, 255, 0.25),
  inset -2.5px -2.5px 0.5px -2.5px rgba(255, 255, 255, 0.09),
  inset 1px 1px 1px -0.5px rgba(255, 255, 255, 0.22),
  inset -1px -1px 1px -0.5px rgba(255, 255, 255, 0.07),
  inset 0 0 6px 6px rgba(255, 255, 255, 0.04),
  inset 0 0 2px 2px rgba(255, 255, 255, 0.03),
  0 0 12px rgba(255, 255, 255, 0.08);

--lg-shadow-sm:
  0 0 4px rgba(0, 0, 0, 0.18),
  0 2px 6px rgba(0, 0, 0, 0.4),
  inset 1.5px 1.5px 0.3px -1.5px rgba(255, 255, 255, 0.22),
  inset -1.5px -1.5px 0.3px -1.5px rgba(255, 255, 255, 0.08),
  inset 0.5px 0.5px 0.5px -0.25px rgba(255, 255, 255, 0.18),
  inset -0.5px -0.5px 0.5px -0.25px rgba(255, 255, 255, 0.06),
  inset 0 0 3px 3px rgba(255, 255, 255, 0.03),
  0 0 8px rgba(255, 255, 255, 0.06);
```

**Warm Authority (ivory + navy):** keep the cream shadow, swap dark insets to `rgba(29, 53, 87, 0.2)` (navy).
**Sand and Sky (warm paper):** swap dark insets to `rgba(62, 44, 35, 0.2)` (ink).

## The Apple Balance (Three Knobs, Balanced Together)

| Knob | Too low | Too high | Sweet spot |
|------|---------|----------|------------|
| **Tint opacity** | Content sharp and distracting, glass thin | Content invisible, reads as solid | 0.5-0.75 on cream, 0.05-0.08 on dark |
| **Displacement `scale`** | No refraction, looks flat | Text behind becomes wobbly garbage | 5-12 for panels, 3-8 for pills |
| **Backdrop blur** | Seams visible, digital feel | Diffuse, mushy (that's frosted again) | 1-4px |

**Rohit's two validated failure modes:**
1. `blur(24px)` + thin tint → shower-door frosted. Rejected 2026-04-22.
2. `scale=40` + 0.22 tint → mangled unreadable wobbly text. Rejected 2026-04-22.

The Apple look: high-ish tint (mutes displaced content) + small displacement (warps, not mangles) + tiny blur (cleans seams).

## When to Apply Full Liquid Glass (SVG filter + dome)

Elements that **float over scrolling content**, where refraction shows:
- Sticky tab bars, nav rails, top bars
- Floating search inputs in scrolling lists
- Hero-overlay buttons on images/video
- Modal backdrops, popovers, command palettes
- Sticky filter bars, toolbars

## When to Apply Shadow-Only Variant (No SVG Filter)

**Inline cards in normal flow** with flat-ish background behind them. The SVG filter would be wasted GPU (nothing meaningful to refract). Apply just the dome shadow:
- Stat cards, metric panels
- Glossary / concept cards, tile grids
- Widgets, interactive panels
- Path / step cards

```css
.card-inline-glass {
  background: rgba(255, 255, 255, 0.06); /* adapt per theme */
  border-radius: 18px;
  box-shadow: var(--lg-shadow);
  border: none;
}
```

## When NOT to Apply Liquid Glass

- Body copy paragraphs, long text blocks
- Data tables (dome shadow eats edge space; keep tables flat)
- Callouts with semantic border-left accents (rim shadow fights the semantic rim, muddies the message)
- Figures holding technical SVG diagrams (inner fill hurts diagram contrast)
- Plain reference / text lists (no visual payoff, just cost)
- Print output (strip in `@media print`)

## Intake (Ask Before Building)

One question at a time, wait for each answer:

1. **Site type.** Landing page, portfolio, product launch, event site, SaaS marketing, other?
2. **Theme.** Which of Rohit's themes? Primary dark (`#1C1D20`), Primary light (`#FAFAFA`), Sand and Sky (warm paper), Warm Authority (ivory + navy), or a Linear-style dark (`#08090a`)? If unclear, ask. State the theme announcement per brand-theme-first rule.
4. **One-sentence pitch.** What does the site sell or communicate?
5. **Primary CTA.** What single action should the visitor take?
6. **Sections needed.** Default is hero + features + CTA. Offer: testimonials, pricing, FAQ, logos, team, stats.

## Build Steps

1. Confirm theme (state it and get approval per brand-theme-first rule).
2. Scaffold semantic HTML5 (`<header>`, `<main>` with `<section>`, `<footer>`).
3. Inject the SVG displacement filter block near the start of `<body>`.
4. Apply `:root` tokens (theme palette + dome-shadow tokens).
5. Build the animated background (mesh gradient tuned to the theme's accent family). Make sure it has vivid content so the refraction has something to work with.
6. Compose sections using the component library below.
7. Apply full Liquid Glass (SVG filter + dome + tint) to floating chrome (nav, eyebrow pill, final CTA card).
8. Apply shadow-only variant to inline cards (feature cards, stat cards).
9. Add the `@supports not` fallback block.
10. Add the `@media print` strip.
11. Save as `./liquid-glass-site/index.html` by default.
12. **Validate by opening in browser.** Check: does content behind nav DISTORT (not blur) as you scroll? Is the dome 3D (top bright, bottom subtle)? If it looks milky, the blur is too high or you forgot the SVG filter.

## Full Liquid Glass Element (Floating Chrome)

```css
.lg-full {
  background: rgba(255, 255, 255, 0.06); /* dark theme; 0.52-0.74 on cream */
  -webkit-backdrop-filter: blur(3px) url('#liquid-distort') saturate(150%);
  backdrop-filter: blur(3px) url('#liquid-distort') saturate(150%);
  border: none;
  border-radius: 22px; /* 16-22 for panels, 99 for pills */
  box-shadow: var(--lg-shadow);
  isolation: isolate;
}
```

For pills / small buttons, use the small filter and smaller shadow:
```css
.lg-pill {
  background: rgba(255, 255, 255, 0.06);
  -webkit-backdrop-filter: blur(2px) url('#liquid-distort-sm') saturate(150%);
  backdrop-filter: blur(2px) url('#liquid-distort-sm') saturate(150%);
  border: none;
  border-radius: 99px;
  box-shadow: var(--lg-shadow-sm);
  isolation: isolate;
}
```

## Shadow-Only Element (Inline Cards)

```css
.lg-card {
  background: rgba(255, 255, 255, 0.06); /* adapt per theme */
  border: none;
  border-radius: 18px;
  box-shadow: var(--lg-shadow);
  padding: 24px 28px;
}
```

## Fallback (For Browsers Without backdrop-filter url())

```css
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .lg-full, .lg-pill { background: var(--bg-solid); backdrop-filter: none; }
}
```

## Print Strip

```css
@media print {
  .lg-full, .lg-pill, .lg-card {
    -webkit-backdrop-filter: none;
    backdrop-filter: none;
    background: #fff;
    box-shadow: none;
  }
}
```

## Active State (Buttons, Pills)

On active / pressed state, kill the refraction and use a solid fill. Active states should not refract.
```css
.lg-pill.active {
  background: var(--accent);
  -webkit-backdrop-filter: none;
  backdrop-filter: none;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.22),
    inset 1px 1px 0.5px -0.5px rgba(255, 255, 255, 0.4),
    inset -1px -1px 0.5px -0.5px rgba(0, 0, 0, 0.4);
}
```

## Background Recipes (Pick One)

The background must have vivid content for the refraction to show. Subtle gradients on a near-black canvas = wasted filter.

### Monochromatic Mesh (default)

```css
.mesh-bg {
  position: fixed; inset: -15%; z-index: -1;
  background:
    radial-gradient(circle at 22% 28%, var(--accent), transparent 50%),
    radial-gradient(circle at 78% 18%, var(--accent-bright), transparent 45%),
    radial-gradient(circle at 48% 88%, var(--accent-deep), transparent 50%),
    var(--bg);
  filter: blur(80px) saturate(150%);
  opacity: 0.75; /* higher than glassmorphism default so glass has content to refract */
  animation: mesh-drift 34s ease-in-out infinite;
}
@keyframes mesh-drift {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(-2%, 1.5%) scale(1.04); }
  66% { transform: translate(1.5%, -2%) scale(0.98); }
}
```

## Typography (Linear-inspired for dark theme)

```css
body {
  font-family: "Inter Variable", "Inter", -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  font-feature-settings: "cv01", "ss03"; /* Linear signature OpenType features */
}
h1 { font-size: clamp(44px, 7vw, 84px); font-weight: 510; line-height: 1.02; letter-spacing: -0.034em; }
h2 { font-size: clamp(32px, 4vw, 48px); font-weight: 510; letter-spacing: -0.022em; }
h3 { font-size: 20px; font-weight: 590; letter-spacing: -0.012em; }
```

Weight 510 (between regular 400 and medium 500) is the Linear signature. Weight 590 for strong emphasis.

## Failure Modes (Save Yourself the Debugging)

1. **Reads as frosted** → you forgot the SVG filter. `backdrop-filter` must include `url('#liquid-distort')`, not just `blur()`.
2. **No effect on scroll** → element is opaque. Drop tint to the validated range.
3. **Dome looks flat** → you collapsed the 8-layer shadow into one. Keep all layers.
4. **SVG filter not applying** → SVG must be in DOM before elements referencing it; id must match exactly.
5. **Text behind unreadable wobbly** → displacement scale too high. Dial back to 5-8.
6. **Everything's blurry** → blur too high. Keep under 4px when using SVG filter.
7. **Active state weird** → override `backdrop-filter: none` on active/pressed states.

## Verification Before Shipping

- [ ] SVG filter block in `<body>` with both `#liquid-distort` and `#liquid-distort-sm`.
- [ ] Floating chrome (nav, eyebrow pill, final CTA) uses full Liquid Glass: `backdrop-filter: blur(1-4px) url('#liquid-distort') saturate(150%)` + dome shadow + theme-adapted tint.
- [ ] Inline cards use shadow-only variant (dome shadow, no SVG filter).
- [ ] Dome shadow has ALL 8-9 layers (top-left bright, bottom-right dark/subtle, inner glow, outer halo). Not collapsed.
- [ ] Border is `none`; the inset shadows ARE the border.
- [ ] Background is animated and vivid enough that refraction shows when scrolling.
- [ ] Scroll test: open in browser, scroll content under the nav. Content should **distort like water** under the nav, not blur away.
- [ ] Typography uses Inter Variable with `cv01, ss03` on dark themes, weight 510 for displays.
- [ ] `@supports not` fallback present.
- [ ] `@media print` strip present.
- [ ] No lorem ipsum; all copy from intake answers.
- [ ] File size under 45KB (the SVG filter adds ~500 bytes).

## Output

Save to `./liquid-glass-site/index.html` by default. Report absolute path. Offer `open ./liquid-glass-site/index.html`.

## Source Attribution

This pattern comes from:
- Rohit's brand signature (locked in 2026-04-22, see `reference_liquid_glass_pattern.md`)
- 21st.dev `liquid-glass-button` (the React reference that clarified the technique)
- acquired.fm episodes page (production example Rohit pointed at)
- Apple visionOS / iOS 26 / macOS 26 UI

This skill packages those specifications. Authoritative source: the memory file. Update the memory first, then reflect changes here.
