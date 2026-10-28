# Departure board and flight strips

Call with `/analog-ui departure-board`.

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

## Example
`examples/departure-board-status/index.html`. Open it after writing your own inventory and mapping table, for technique only. Northwind Notes is a fictional product; all figures are illustrative.

## Lessons from the sample
- Don't reuse the medium's words as class names (`.board` the panel vs a "boarding" status clashed). Prefix states, for example `.st-board`.
- On phones, hide secondary columns (time, gate) rather than scrolling a status board sideways.
- No permanent blinking. Flip once on a real change, announce it through an `aria-live` region, and respect reduced motion.
