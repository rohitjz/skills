# Museum exhibit and wall placards

Call with `/analog-ui museum`.

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

## Example
`examples/museum-qbr/index.html`. Open it after writing your own inventory and mapping table, for technique only. Northwind Notes is a fictional product; all figures are illustrative.

## Lessons from the sample
- One framed artefact per room. A second chart turns the gallery into a dashboard.
- Draw the artefact chart in the gallery's own type and palette (`make_artifact.py` in the sample shows the matplotlib settings).
- Accession numbers only earn their place if each maps to a real source table or query.
