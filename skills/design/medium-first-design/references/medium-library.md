# Medium library

Eight worked mediums. Each one lists when to use it, its inventory, how to build it, what each
mark means, its palette and type, and the pitfalls. Use them as starting points: inventory the
real medium again for every brief, because the small habits are what make it convincing.

Fonts named here are free on Google Fonts unless noted.

---

## 1. Designer's sketchbook
**Use for:** milestones, celebrations, team updates, personal launches. **Fully built:** `sketchbook-ui`.

| Object | Build | Meaning |
|---|---|---|
| Paper, optional graph grid | White sheet on a grey desk; 26px `linear-gradient` grid | Work in progress, human-made |
| Handwriting | Caveat (display), Kalam (body) | A person, not a system |
| Wobbly pencil box | Uneven `border-radius` + turbulence filter, faint second outline | A group of related facts |
| Highlighter | Skewed gradient behind the bottom 42% of the text | The one number to remember |
| Strike-through | Two loose SVG strokes | Where we were |
| Ticks, arrows | Hand-drawn Bézier `<symbol>`s | Wins, and what's next |
| Tape | Translucent beige strips on a slightly rotated card | Evidence pinned in place |

**Palette:** graphite `#3A3A38`, pencil blue `#2F5BB7`, highlighter `#FFDE4A`.
**Pitfall:** turns childish if more than small elements tilt or more than one thing is highlighted.

---

## 2. Architect's blueprint
**Use for:** roadmaps, architecture overviews, migration plans, anything with phases and dependencies.

| Object | Build | Meaning |
|---|---|---|
| Cyanotype sheet | Deep blue `#123A6B` with a faint fine grid plus a heavier grid every 5 cells | A plan, not a promise |
| White technical linework | 1px `rgba(255,255,255,.85)` borders, no radius | Structure and boundaries |
| Title block (bottom right) | A bordered table: project, drawn by, date, revision, sheet "1 of 1" | Ownership and version |
| Dimension lines | SVG lines with arrowheads at both ends and a label in the middle | Duration and scope of a phase |
| Section callouts | A circle with a letter, plus a leader line | Cross-references between parts |
| Revision cloud | A scalloped SVG outline around changed items | What changed since last time |
| "Not to scale", "Draft" stamps | Small outlined text | Honest uncertainty |

**Type:** IBM Plex Mono or Space Mono for labels; architect-style hand lettering such as
"Architects Daughter" for notes. **Palette:** blueprint blue, white, one red-pencil accent for the
bold move. **Pitfall:** white-on-blue body text tires the eye, so keep prose short. Put long text in
a white "spec sheet" panel.

---

## 3. Museum exhibit and wall placards
**Use for:** quarterly business reviews, annual reports, case studies, "the story of X".

| Object | Build | Meaning |
|---|---|---|
| Gallery wall | Warm off-white `#F3F1EC` with generous whitespace | Calm authority |
| The artefact | One large chart or image, framed with a thin border and a mat | The key result, on display |
| Wall placard | A small card: title in italic, then medium, date and accession number in small caps | Precise provenance for each number |
| Accession numbers | e.g. "Q3.2026.04" in small, tracked type | Traceability to source data |
| Room signage | Large section numbers and room names | Chapters of the story |
| Curator's note | A longer text panel set in a serif | Interpretation and "why it matters" |
| Floor plan | A small map of the rooms | Navigation for long reports |

**Type:** a real serif (Newsreader, Fraunces, EB Garamond) for prose, a neat sans for placards.
**Pitfall:** don't fake a gilded or ornate museum. Modern galleries are restrained, and
restraint is the point.

---

## 4. Engineer's lab notebook
**Use for:** incident reports, root-cause analyses, experiment write-ups, research logs.

| Object | Build | Meaning |
|---|---|---|
| Bound, numbered pages | Faint ruled lines, page number top right, a red margin line | Chronological record, nothing torn out |
| Dated, timestamped entries | `14:02 UTC` in the margin, monospace | The exact timeline |
| Hypothesis, method, result | Labelled blocks in that order | Scientific discipline |
| Crossed-out hypotheses | Single strike, still legible, with "ruled out: why" | What was tested and rejected (never erased) |
| Taped-in printouts | A log or graph excerpt on a white slip with tape | Raw evidence |
| Witness signature | Signature and date line at the end | Accountability and review |
| Margin sketches | Small SVG diagrams | How the system actually behaves |

**Type:** a monospace (JetBrains Mono) for timestamps and logs, a neat handwriting for notes.
**Pitfall:** keep the tone blameless. The lab notebook records facts, not fault.

---

## 5. Risograph zine
**Use for:** launch announcements, community updates, internal events, "what's new" pages.

| Object | Build | Meaning |
|---|---|---|
| Two or three spot inks | e.g. fluorescent pink `#FF48B0` and medium blue `#3255A4` on cream | Energy and personality |
| Misregistration | The same element duplicated, offset 1–3px in the second ink, with `mix-blend-mode: multiply` | Handmade, printed in a run |
| Grain | An SVG noise overlay at about 8% opacity | Ink on paper |
| Overprint | Overlapping shapes multiply into a third colour | Ideas combining |
| Halftone images | A CSS radial-gradient dot pattern masked over a photo | Cheap printing, a bold look |
| Big collage type | Huge condensed type, cut out, slightly rotated | Launch volume |
| Staple and fold marks | Two small grey bars, a faint centre crease | A booklet you can pass around |

**Type:** a heavy condensed face (Anton, Bebas Neue) plus a quirky text face (Space Grotesk).
**Pitfall:** loud by nature. Keep it to one spread of energy, then readable columns for details.

---

## 6. Receipt and price tag
**Use for:** pricing pages, plan comparisons, "what you get" summaries, cost breakdowns, ROI.

| Object | Build | Meaning |
|---|---|---|
| Thermal-paper strip | A narrow white column with zig-zag torn edges (CSS `mask` with a conic-gradient pattern) | Itemised and honest |
| Line items | Monospace, dotted leaders, right-aligned amounts | Exactly what is included |
| Subtotal, discount, total | A double rule above the total | The bottom line |
| Barcode or QR | An SVG barcode encoding a real link | Act on it now |
| Price tag | A rotated tag with a punched hole and string | The headline price |
| "Saved $X" stamp | A red stamp-style circle | The one bold move |

**Type:** a receipt monospace (VT323, IBM Plex Mono). **Pitfall:** totals must actually add up.
The medium invites the reader to check the arithmetic.

---

## 7. Field researcher's journal
**Use for:** customer feedback digests, research readouts, user-interview syntheses.

| Object | Build | Meaning |
|---|---|---|
| Weathered kraft pages | Warm paper `#EFE6D2` with soft edge darkening | Collected in the field |
| Pressed specimens | Quotes on small cards, pinned or taped | Real voices, preserved verbatim |
| Specimen labels | Who, where, when, sample size | Context and representativeness |
| Tally marks | Hand-drawn `||||` groups | How often each theme came up |
| Sketched map | A rough SVG map of the journey | Where the friction happens |
| Field notes | Handwritten observations beside the quotes | The researcher's interpretation |
| Sample bag | A small "n = 412" label | Honest sample size |

**Type:** a handwriting for notes and a typewriter face (Special Elite) for labels.
**Pitfall:** never invent or paraphrase quotes. Pressed specimens are verbatim and anonymised.

---

## 8. Departure board and flight strips
**Use for:** live status pages, launch trackers, service health, release trains.

| Object | Build | Meaning |
|---|---|---|
| Split-flap rows | Dark tiles, monospace caps, a hairline through the middle of each character | Live, ticking status |
| Status column | ON TIME, BOARDING, DELAYED, CANCELLED in amber, green or red | State at a glance |
| Gate and time | Right-aligned monospace columns | Owner and ETA |
| Flight strips | Coloured paper strips in a rack, one per item | Each workstream in flight |
| Flip animation | One `rotateX` flip when a value changes, respecting reduced motion | Something actually changed |

**Type:** a monospace caps face (Share Tech Mono). **Pitfall:** only animate on real change.
A board that flips constantly is noise.

---

## Adding a medium
Copy this shape: *use for*, *inventory with build and meaning*, *type and palette*, *pitfall*.
Test it on real content and inspect a render before adding it here.
