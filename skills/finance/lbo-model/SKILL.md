---
name: lbo-model
description: Build a leveraged buyout model from an entry multiple and a capital structure, with sources and uses, an operating model, a debt schedule on beginning-of-period balances, and a returns waterfall to IRR and MOIC. Triggers on "lbo", "leveraged buyout", "buyout model", "sponsor returns", "irr moic". Largely assumption-driven, free-tier EBITDA covers AAPL, GOOGL, NVDA, TSLA, other targets need user-supplied financials.
---

# LBO Model Builder

An LBO tests what a financial sponsor could pay and still hit a target return. Most inputs are assumptions about a hypothetical take-private, so mark each [ASSUMPTION] with its rationale. Every output is derived; show the arithmetic. Use beginning-of-period debt balances for interest so the model does not go circular.

## Workflow

### Step 1: Set the entry
- Pull LTM EBITDA: for AAPL, GOOGL, NVDA, TSLA from `mcp__financial-datasets__get_income_statements` and `get_cash_flow_statements`; for any other target, ask the user for EBITDA and net debt rather than inventing them.
- Entry EV = entry multiple x LTM EBITDA. Entry multiple is [ASSUMPTION], peer-driven.
- Equity purchase price = Entry EV minus net debt (from `get_balance_sheets` or user input).
- Anchor to reality: show the implied offer per share against the current price from `mcp__tradingview__yahoo_price`. The gap is the control premium. A premium far above market is a flag, not a free lunch.

### Step 2: Sources and uses
```
USES                              SOURCES
Purchase equity value             New debt (turns x EBITDA)
+ Refinance existing net debt     + Sponsor equity (the plug)
+ Transaction & financing fees    + Management rollover
= Total uses                      + Balance-sheet cash used
                                  = Total sources  (must equal uses)
```
Leverage is total new debt / EBITDA, stated in turns ([ASSUMPTION], typically 4 to 6x). Sponsor equity is the plug that balances the two columns.

### Step 3: Debt tranches
Lay out the stack senior to junior: revolver (undrawn at close), term loan B, senior notes, subordinated notes. For each: size, pricing (a base rate from WebSearch plus a spread [ASSUMPTION]), mandatory amortization (TLB often 1% per year), and cash-sweep priority. The blended rate sanity-checks the interest line.

### Step 4: Operating model
Project 5 years of revenue (growth [ASSUMPTION], disciplined by the history from Step 1), EBITDA margin, D&A, CapEx, change in NWC, and cash taxes. Free cash flow before financing = EBITDA minus cash taxes minus CapEx minus change in NWC minus cash interest. This FCF services and sweeps the debt.

### Step 5: Debt schedule (beginning-balance interest)
For each year and tranche:
```
Beginning balance
- Mandatory amortization
- Optional prepayment (cash sweep from excess FCF)
= Ending balance
Interest = Beginning balance x rate      (beginning, not average, to avoid circularity)
```
Sweep order follows seniority. The revolver draws if FCF cannot cover mandatory amortization. Track ending net debt each year.

### Step 6: Returns
- Exit EV = exit multiple x exit-year EBITDA. Default exit multiple = entry multiple (no expansion) as the honest base case; flex it in sensitivity.
- Exit equity = Exit EV minus net debt at exit.
- MOIC = sponsor exit equity / sponsor entry equity.
- IRR = MOIC^(1 / holding years) minus 1 with no interim cash, or solve the cash-flow series if there are dividend recaps.
- Decompose the return: how much came from debt paydown (deleveraging), EBITDA growth, and multiple change. A return that leans on multiple expansion is fragile; say so.

### Step 7: Sensitivity
Two 5x5 grids, base case in the center cell:
- Entry multiple x exit multiple, output IRR.
- Leverage (turns) x exit multiple, output IRR with MOIC alongside.
Each cell is a full recompute. The center must equal the base-case IRR; that equality proves the grid is wired right.

## Output

Markdown by default:
1. Entry block: EV, equity price, implied offer vs current price and premium.
2. Sources and uses table (columns tie).
3. Debt stack with pricing and terms.
4. Operating model and FCF table by year.
5. Debt schedule by tranche by year, interest on beginning balances.
6. Returns: IRR, MOIC, and the value-creation bridge.
7. Sensitivity grids, base case centered.

On request, write a headless `.xlsx` to `./out/` via python openpyxl: blue inputs, black formulas, beginning-balance interest as formula strings, comments citing every [ASSUMPTION]. No Excel add-in.

## Data and limits

- An LBO on a public large cap is hypothetical; the value is the return math and the leverage sensitivity, not a price call. Treat it as a what-if.
- Free-tier EBITDA and balance-sheet data: AAPL, GOOGL, NVDA, TSLA only. Other targets need user-supplied financials; do not invent them.
- No live credit-market pricing, no LBO comps in this stack; spreads and multiples are [ASSUMPTION], sourced from WebSearch where possible.
- Flag every data gap. Not financial advice.
