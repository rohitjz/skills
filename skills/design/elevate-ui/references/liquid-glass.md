# Liquid glass chrome

Real refractive "liquid glass" (the Apple / iOS look) on floating chrome is a premium cue most pages miss. The distinction that matters:

- **Frosted glass** = `backdrop-filter: blur(20px)` + a translucent fill. Content behind goes diffuse and unreadable. Looks like shower glass. This is *not* the effect.
- **Liquid glass** = an SVG displacement filter warps the content behind (like looking through curved glass) with very little blur, plus a layered dome shadow for the glass edge. Content is *hinted at and distorted*, not blurred away.

The two ingredients are a displacement filter and a multi-layer shadow. Use it only on chrome that floats over scrolling content (a sticky nav, a search input over a list, a hero button over an image). On a card with nothing behind it, the refraction has nothing to bend, so use the dome shadow from `depth.md` instead.

## Ingredient 1 — the displacement filter

Inline once in `<body>` (filters are referenced by id from `backdrop-filter`). A wider, stronger filter for nav docks; a smaller one for pills.

```html
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <filter id="lg-nav" x="-20%" y="-20%" width="140%" height="140%" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="0.008 0.010" numOctaves="2" seed="5" result="t"/>
    <feGaussianBlur in="t" stdDeviation="3" result="s"/>
    <feDisplacementMap in="SourceGraphic" in2="s" scale="14" xChannelSelector="R" yChannelSelector="B"/>
  </filter>
  <filter id="lg-pill" x="-20%" y="-20%" width="140%" height="140%" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="0.012 0.015" numOctaves="1" seed="7" result="t"/>
    <feGaussianBlur in="t" stdDeviation="2" result="s"/>
    <feDisplacementMap in="SourceGraphic" in2="s" scale="6" xChannelSelector="R" yChannelSelector="B"/>
  </filter>
</defs></svg>
```

Parameter intuition:
- `baseFrequency` = wave size. Low (0.006–0.012) = long liquid swells. High = small ripples. Liquid wants low.
- `scale` on `feDisplacementMap` = how much the content is pushed. **5–12** for content panels, **12–16** for a wide nav over a vivid background. Above ~25 the text behind turns to unreadable garbage.

## Ingredient 2 — the layered dome shadow

This is the same `--lg-shadow` token as in `depth.md`. It draws the glass edge. Keep every layer.

```css
:root{
  --lg-shadow:
    0 0 6px rgba(0,0,0,.22),
    0 4px 16px rgba(0,0,0,.45),
    inset 0 1px 0 0 rgba(255,255,255,.15),
    inset 2.5px 2.5px 0.5px -2px rgba(255,255,255,.15),
    inset -2.5px -2.5px 0.5px -2px rgba(255,255,255,.08),
    inset 1px 1px 1px -0.5px rgba(255,255,255,.11),
    inset -1px -1px 1px -0.5px rgba(255,255,255,.05),
    inset 0 0 8px 4px rgba(255,255,255,.03),
    0 0 14px rgba(255,255,255,.05);
}
```

## Applying to a sticky nav (dark theme)

Keep a semi-dark tint so the nav's own text stays readable while the content behind it refracts. A pure white tint looks more "glass" but can hurt nav legibility; the smoked-glass version below is the safe default.

```css
nav{
  position:fixed; top:0; left:0; right:0; z-index:90; isolation:isolate;
  background:rgba(18,21,30,.55);                                   /* smoked tint, readable */
  -webkit-backdrop-filter:blur(5px) url(#lg-nav) saturate(165%);
  backdrop-filter:blur(5px) url(#lg-nav) saturate(165%);
  border-bottom:1px solid rgba(255,255,255,.08);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.09), 0 10px 30px -16px rgba(0,0,0,.6);
}
/* graceful fallback where backdrop url() filters are unsupported */
@supports not ((backdrop-filter:url(#x)) or (-webkit-backdrop-filter:url(#x))){
  nav{ background:rgba(13,15,21,.86); -webkit-backdrop-filter:blur(12px); backdrop-filter:blur(12px); }
}
```

For a **light/cream theme**, use a cream tint at higher opacity and white highlights: `background:rgba(250,249,245,.52)`, and shift the dome insets so the bright edge is white and the dark edge is a soft black.

## The balance (where both extremes fail)

Three knobs interact. Get them wrong and you land in "frosted" or "wobbly garbage."

| Knob | Too low | Too high | Sweet spot |
|------|---------|----------|------------|
| Tint opacity | content behind fights the chrome text | reads frosted/solid, no refraction visible | dark `0.5–0.6`, light `0.5–0.74` |
| Displacement `scale` | glass looks static/flat | text behind becomes unreadable | `5–8` panels, `12–16` nav |
| Blur | displacement seams look digital | diffuse → you're back to frosted | `1–5px` (just enough to clean seams) |

If the text behind still reads sharply, the tint is too low. If it's unreadable but distracting, the displacement is too high. If everything's blurry, you've drifted to frosted (you probably forgot the `url(#...)` filter; blur alone is frosted).

## Where not to use it

- Inline content cards (nothing behind to refract → use `depth.md` instead).
- Body copy, data tables, semantic callouts.
- Active/pressed states — override to a solid fill; pressed buttons shouldn't refract.
- Always include the `-webkit-` prefix for Safari.
