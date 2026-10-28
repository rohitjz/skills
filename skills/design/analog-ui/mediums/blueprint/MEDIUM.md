# Architect's blueprint

Call with `/analog-ui blueprint`.

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

## Example
`examples/blueprint-roadmap/index.html`. Open it after writing your own inventory and mapping table, for technique only. Northwind Notes is a fictional product; all figures are illustrative.

## Lessons from the sample
- On phones, redraw the Gantt as a stack: one row per workstream in order, each bar full width with its dates written on it (`data-when`), and the revision note below the clouded bar. Don't scroll it sideways.
- Stamps only when true: this sample is a draft, so it says DRAFT. Its quarter columns are to scale, so it doesn't say NOT TO SCALE.
- Keep rows in plan order and title-block text inside its cells; reviewers notice both.
- Put the revision note below the clouded bar, never above it, or it collides with the lane above.
- Mark finished work with a hatched fill; it reads as "built" without a legend.
