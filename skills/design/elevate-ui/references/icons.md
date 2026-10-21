# Bespoke SVG line-icon system

Replacing emoji with a coherent custom icon set is the single biggest jump from "AI-made" to "designed." Emoji are inconsistent in weight, color, and metaphor, and every model reaches for them. A hand-built line set with one stroke weight and one geometry instantly reads as intentional.

## The pattern: one inline sprite, referenced by `<use>`

Define all icons once as `<symbol>`s in a hidden SVG at the top of `<body>`, then reference them anywhere (including from JS-injected markup). This keeps them DRY, self-contained, and themeable via `currentColor`.

```html
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <symbol id="ic-compass" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M15.6 8.4 11 11 8.4 15.6 13 13Z"/></symbol>
  <!-- ...more symbols... -->
</defs></svg>
```

Reference one like this; size and color come from CSS:

```html
<svg class="ico"><use href="#ic-compass"/></svg>
```

```css
.ico{
  width:24px; height:24px;
  stroke:currentColor; fill:none;
  stroke-width:1.6; stroke-linecap:round; stroke-linejoin:round;
  display:inline-block; vertical-align:middle; flex:none;
}
.ico-lg{width:30px;height:30px}
.ico-sm{width:18px;height:18px}
.ico-xl{width:38px;height:38px}
```

Color an icon by setting `color` on it or its container, since the stroke is `currentColor`:
```css
.feature-tile .ico{color:var(--accent)}   /* amber icons on a card */
```

Because `stroke` follows `currentColor`, a JS toggle that swaps a card's text color also recolors its icon for free.

## Rules that keep the set coherent

- **One stroke weight** (1.6 in a 24 viewBox) and **rounded caps/joins** everywhere. Consistency is the whole point.
- **`viewBox="0 0 24 24"`** for every icon, so they share a grid and optical size.
- **`fill:none`, stroke-only** line style. If an icon needs a filled dot (a gamepad button, a node), set `fill="currentColor" stroke="none"` on just that element.
- **Pick accurate metaphors.** A terminal for "tools/shell" beats a wrench. A database cylinder for "state/storage." A compass or map for "instructions/guidance."
- **Abstract hard objects.** Do not hand-code a realistic horse, car, or face; it looks amateur. Represent the idea geometrically instead.
- **Inject SVG strings via `innerHTML`, not `textContent`.** If you set an icon from JS (e.g., swapping a status icon), `textContent` will print the raw markup. Use `el.innerHTML = '<svg class="ico"><use href="#ic-check"/></svg>'`.

## Ready-to-paste starter set (16 icons)

Drop these into the sprite `<defs>`. They cover most UI needs; add your own in the same style.

```html
<symbol id="ic-compass" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M15.6 8.4 11 11 8.4 15.6 13 13Z"/></symbol>
<symbol id="ic-terminal" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9l3 3-3 3M13 15h4"/></symbol>
<symbol id="ic-cube" viewBox="0 0 24 24"><path d="M12 2.5 20 7v10l-8 4.5L4 17V7Z"/><path d="M4 7l8 4.5L20 7M12 11.5v10"/></symbol>
<symbol id="ic-database" viewBox="0 0 24 24"><ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v12c0 1.66 3.13 3 7 3s7-1.34 7-3V6"/><path d="M19 12c0 1.66-3.13 3-7 3s-7-1.34-7-3"/></symbol>
<symbol id="ic-check" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M8.4 12.4l2.6 2.6 4.6-5.6"/></symbol>
<symbol id="ic-chip" viewBox="0 0 24 24"><rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5" rx="1"/><path d="M9 6V3M15 6V3M9 21v-3M15 21v-3M6 9H3M6 15H3M21 9h-3M21 15h-3"/></symbol>
<symbol id="ic-eye" viewBox="0 0 24 24"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></symbol>
<symbol id="ic-eyeoff" viewBox="0 0 24 24"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/><line x1="3.5" y1="3.5" x2="20.5" y2="20.5"/></symbol>
<symbol id="ic-edit" viewBox="0 0 24 24"><path d="M4 20h4L18.5 9.5l-4-4L4 16Z"/><path d="M13.5 6.5l4 4"/></symbol>
<symbol id="ic-folder" viewBox="0 0 24 24"><path d="M3 7a2 2 0 0 1 2-2h3.4l2 2H19a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/></symbol>
<symbol id="ic-message" viewBox="0 0 24 24"><path d="M4 5h16a1.5 1.5 0 0 1 1.5 1.5v9a1.5 1.5 0 0 1-1.5 1.5H9l-4 4v-4H4a1.5 1.5 0 0 1-1.5-1.5v-9A1.5 1.5 0 0 1 4 5Z"/></symbol>
<symbol id="ic-doc" viewBox="0 0 24 24"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5M9 13h6M9 16.5h4"/></symbol>
<symbol id="ic-ticket" viewBox="0 0 24 24"><path d="M3 8a1 1 0 0 1 1-1h16a1 1 0 0 1 1 1v2a2 2 0 0 0 0 4v2a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-2a2 2 0 0 0 0-4Z"/><path d="M15 7.5v9" stroke-dasharray="1.5 2.5"/></symbol>
<symbol id="ic-user" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M5 20a7 7 0 0 1 14 0"/></symbol>
<symbol id="ic-alert" viewBox="0 0 24 24"><path d="M12 3 22 19H2Z"/><path d="M12 10v4M12 17h.01"/></symbol>
<symbol id="ic-gamepad" viewBox="0 0 24 24"><rect x="2" y="8" width="20" height="10" rx="5"/><path d="M7 11v4M5 13h4"/><circle cx="16" cy="12" r="1" fill="currentColor" stroke="none"/><circle cx="18.5" cy="14.5" r="1" fill="currentColor" stroke="none"/></symbol>
```

## Drawing your own

Need an icon not in the set? Build it from the same primitives (`rect`, `circle`, `path`, `line`) on the 24-grid with the same stroke. Keep shapes simple, one or two elements. If you can describe the metaphor in a word, you can usually draw it with two paths. When in doubt, look at how Lucide or Feather construct the equivalent icon and match that economy of line.
