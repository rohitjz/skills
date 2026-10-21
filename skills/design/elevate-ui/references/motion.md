# Light and life: grain, glows, spotlight, animation

This is the "life" axis plus the grain that does most of the "light" work. Each piece is small; together they make a page feel alive and lit instead of synthetic and static. Keep all of it subtle (see the restraint rules in SKILL.md) and guard the motion with `prefers-reduced-motion`.

## 1. Film grain (the cheapest, highest-impact texture)

A faint noise overlay over the whole page kills the flat, screen-printed look. Pure inline SVG, no image file.

```css
.grain{
  position:fixed; inset:0; z-index:3; pointer-events:none;
  opacity:.05; mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='150' height='150'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.82' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
```
```html
<div class="grain"></div>   <!-- right after <body>; below the nav's z-index so chrome stays crisp -->
```
Keep opacity at 0.05 or less. Grain you can consciously see is too strong.

## 2. Warm radial glows ("magic")

One or two soft glows behind key elements add warmth and depth. Put them on a fixed pseudo-layer or behind a heading. Sparse and low-opacity.

```css
body::before{
  content:""; position:fixed; inset:0; z-index:-2;
  background:
    radial-gradient(900px 600px at 80% -5%, rgba(255,180,84,.10), transparent 60%),
    radial-gradient(800px 600px at 5% 10%, rgba(52,209,191,.08), transparent 55%);
}
```

## 3. Cursor spotlight on tile grids

The signature "designed" micro-interaction: a warm glow tracks the cursor across a card and the card lifts. Implemented as a background gradient (which paints behind text automatically, so no z-index fights) driven by two CSS variables.

```css
.tile{ transition:transform .25s ease, background .2s ease; }
.tile:hover{
  transform:translateY(-4px);
  background:radial-gradient(240px circle at var(--mx,50%) var(--my,50%),
            rgba(255,180,84,.14), transparent 55%), var(--surface-2);
}
```
```js
document.querySelectorAll('.tile').forEach(c=>{
  c.addEventListener('mousemove',e=>{
    const r=c.getBoundingClientRect();
    c.style.setProperty('--mx',((e.clientX-r.left)/r.width*100)+'%');
    c.style.setProperty('--my',((e.clientY-r.top)/r.height*100)+'%');
  });
});
```

## 4. The animated signature illustration

Build one centerpiece for the hero from the page's motif (see SKILL.md → Signature motif) and give it slow, layered motion: a core that breathes, rings that counter-rotate, and gentle parallax toward the cursor. This is the difference between "a hero with a graphic" and "a hero that's alive."

Example: a glowing core inside a scaffold. Structure the SVG with classes on the animated parts:

```html
<svg class="hero-art" viewBox="0 0 520 520" fill="none" aria-hidden="true">
  <defs>
    <radialGradient id="coreGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffb454" stop-opacity=".85"/>
      <stop offset="42%" stop-color="#ffb454" stop-opacity=".22"/>
      <stop offset="100%" stop-color="#ffb454" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect x="70" y="70" width="380" height="380" rx="30" stroke="#34d1bf" stroke-opacity=".22" stroke-width="1.5"/>
  <g class="spin-ring"><circle cx="260" cy="260" r="150" stroke="#34d1bf" stroke-opacity=".3" stroke-width="1.5" stroke-dasharray="2 13"/></g>
  <g class="spin-ring-2"><circle cx="260" cy="260" r="92" stroke="#ffb454" stroke-opacity=".32" stroke-width="1.5" stroke-dasharray="1 15"/></g>
  <circle class="core-pulse" cx="260" cy="260" r="120" fill="url(#coreGlow)"/>
  <circle cx="260" cy="260" r="30" fill="#ffb454" fill-opacity=".16" stroke="#ffb454" stroke-width="1.5"/>
  <circle cx="260" cy="260" r="9" fill="#ffb454"/>
</svg>
```
```css
.hero{position:relative; overflow:hidden}
.hero .container{position:relative; z-index:1}        /* text above the art */
.hero-art{position:absolute; right:-70px; top:46%; transform:translateY(-50%);
          width:500px; height:500px; opacity:.55; pointer-events:none; z-index:0}
@media(max-width:680px){.hero-art{display:none}}      /* keep mobile text clean */

.hero-art .spin-ring  {transform-box:fill-box; transform-origin:center; animation:hspin 46s linear infinite}
.hero-art .spin-ring-2{transform-box:fill-box; transform-origin:center; animation:hspin 64s linear infinite reverse}
.hero-art .core-pulse {transform-box:fill-box; transform-origin:center; animation:hpulse 4.6s ease-in-out infinite}
@keyframes hspin {to{transform:rotate(360deg)}}
@keyframes hpulse{0%,100%{opacity:.6} 50%{opacity:1}}
```
```js
const hero=document.querySelector('.hero'), art=document.querySelector('.hero-art');
if(hero && art && matchMedia('(pointer:fine)').matches){
  hero.addEventListener('mousemove',e=>{
    const r=hero.getBoundingClientRect();
    const x=(e.clientX/r.width-.5), y=(e.clientY/r.height-.5);
    art.style.transform=`translateY(-50%) translate(${x*-22}px, ${y*-18}px)`;
  });
  hero.addEventListener('mouseleave',()=>{ art.style.transform='translateY(-50%)'; });
}
```

`transform-box:fill-box; transform-origin:center` is what makes an SVG element rotate around its own center; without it the rotation pivots off the SVG origin and flies off-screen.

## 5. Scroll reveals (optional, restrained)

Fade-and-rise sections as they enter the viewport. One observer, no library.

```css
.reveal{opacity:0; transform:translateY(28px); transition:opacity .7s ease, transform .7s ease}
.reveal.in{opacity:1; transform:none}
```
```js
const io=new IntersectionObserver(es=>es.forEach(e=>{
  if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); }
}),{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
```

## 6. Always respect reduced motion

Some users get motion sickness from animation. Honor their setting; it costs one block.

```css
@media(prefers-reduced-motion:reduce){
  .hero-art .spin-ring, .hero-art .spin-ring-2, .hero-art .core-pulse{animation:none}
  .reveal{transition:none}
}
```
