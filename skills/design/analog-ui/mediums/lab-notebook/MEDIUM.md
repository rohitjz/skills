# Engineer's lab notebook

Call with `/analog-ui lab-notebook`.

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

## Example
`examples/lab-notebook-incident/index.html`. Open it after writing your own inventory and mapping table, for technique only. Northwind Notes is a fictional product; all figures are illustrative.

## Lessons from the sample
- On phones, move margin timestamps inline above each entry rather than shrinking the margin.
- Action items need a two-column grid on phones so owners and dates align under the text, not under the checkbox.
- Exactly one bold move. In the sample it is the "RESOLVED" stamp; the key finding gets a quiet pen underline, not a highlighter. A red bracket marking the impact window works too, but pick one.
- Page numbers and log excerpts only when the brief provides them; otherwise tape in the brief's own facts.
- Draw only what the brief states; don't add systems, log lines or labels it doesn't mention.
