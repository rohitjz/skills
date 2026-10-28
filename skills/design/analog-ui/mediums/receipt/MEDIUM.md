# Receipt and price tag

Call with `/analog-ui receipt`.

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

## Example
`examples/receipt-pricing/index.html`. Open it after writing your own inventory and mapping table, for technique only. Northwind Notes is a fictional product; all figures are illustrative.

## Lessons from the sample
- Mark every amount with `data-amt`, `data-subtotal` and `data-total`; the test suite checks the arithmetic.
- The "saved" stamp must sit beside the total, not on it. Pair it with the barcode in the receipt footer.
- Generate the barcode deterministically so it doesn't change between renders.
