# Card depth: kill the flat plane

Flat cards (a solid fill plus a 1px border) are the most common "templated" tell after emoji. The fix is light: a lit top edge, a soft drop shadow, and a faint gradient fill so the surface looks like it catches light from above. This gives the page a z-axis.

Two treatments. Use the **glass-dome** shadow on small tiles (feature cards, stat cards, metric tiles, the cells of a grid) and the **soft elevation** on big containers (a whole panel, a code window, a section wrapper). Dome on everything gets busy; soft on everything stays flat.

## Treatment A — glass-dome shadow (tiles)

A layered inset+outer shadow that makes a card look like a curved piece of dark glass. The layering is what sells it; do not collapse it into one shadow. Tuned for dark charcoal surfaces.

```css
:root{
  --lg-shadow:
    0 0 6px rgba(0,0,0,.22),
    0 4px 16px rgba(0,0,0,.45),
    inset 0 1px 0 0 rgba(255,255,255,.15),                 /* the lit top edge — the key cue */
    inset 2.5px 2.5px 0.5px -2px rgba(255,255,255,.15),
    inset -2.5px -2.5px 0.5px -2px rgba(255,255,255,.08),
    inset 1px 1px 1px -0.5px rgba(255,255,255,.11),
    inset -1px -1px 1px -0.5px rgba(255,255,255,.05),
    inset 0 0 8px 4px rgba(255,255,255,.03),
    0 0 14px rgba(255,255,255,.05);
}
.tile{ box-shadow:var(--lg-shadow); }   /* keep or drop the 1px border; both read fine */
```

The `inset 0 1px 0` top-edge highlight is the single biggest contributor to "this looks like glass" vs "this is a rectangle." Keep it.

**Light-theme version** (cream/white surfaces): flip the insets so the top-left is a bright specular highlight and the bottom-right is a soft dark edge.
```css
--lg-shadow-light:
  0 1px 2px rgba(0,0,0,.06),
  0 12px 30px -14px rgba(0,0,0,.18),
  inset 0 1px 0 0 rgba(255,255,255,.9),
  inset 2px 2px 0.5px -2px rgba(255,255,255,.95),
  inset -2px -2px 0.5px -2px rgba(0,0,0,.12);
```

## Treatment B — soft elevation (containers)

Lighter: a lit top edge plus a long soft shadow for depth, without the dome's inner glow and halo (which get noisy at large sizes).

```css
.panel{
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.05),     /* lit top edge */
    0 2px 4px rgba(0,0,0,.2),
    0 26px 52px -28px rgba(0,0,0,.72);        /* long, soft, far drop */
}
```

## Gradient hairline border (optional polish)

A border that's brighter at the top than the bottom mimics a lit edge. Use the double-background trick:

```css
.tile{
  border:1px solid transparent;
  background:
    linear-gradient(var(--surface), var(--surface)) padding-box,
    linear-gradient(135deg, rgba(255,255,255,.14), rgba(255,255,255,.02)) border-box;
}
```

## Hover lift

Movement on hover makes cards feel responsive. Keep it small and eased.

```css
.tile{ transition:transform .25s ease, box-shadow .25s ease; }
.tile:hover{ transform:translateY(-4px); }
```

Pair this with the cursor spotlight in `motion.md` for the full "designed" hover.

## What to keep flat

Depth is a tool, not a default. Leave these flat so the message stays clean:
- Body-copy containers and paragraph backgrounds.
- Semantic callouts with a left-border accent (a warning, a tradeoff) — the dome rim fights the colored border.
- Data tables — the inset shadow eats the edge space rows need.
- Figures holding technical SVG diagrams — the inner glow lowers the contrast the diagram needs.
- Print output — strip shadows in `@media print`.
