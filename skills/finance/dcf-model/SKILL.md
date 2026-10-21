---
name: dcf-model
description: Build a discounted cash flow valuation from historicals, projecting revenue, margins, and unlevered FCF, with a CAPM WACC build, Gordon-growth and exit-multiple terminal values, and an odd-dimensioned WACC x terminal-growth sensitivity. Triggers on "dcf", "discounted cash flow", "intrinsic value", "fair value model". Free-tier historicals cover AAPL, GOOGL, NVDA, TSLA only; other tickers need user-supplied financials.
---

# DCF Model Builder

Every projection, margin, discount factor, and present value is derived from a stated input. Show the arithmetic; never type a number that should be calculated. Anchor the result to the current price so the gap is explicit.

## Workflow

### Step 1: Pull and validate inputs
For AAPL, GOOGL, NVDA, or TSLA: pull 3 to 5 years from `mcp__financial-datasets__get_income_statements`, `get_cash_flow_statements`, `get_balance_sheets`, and `get_sec_filings`. For any other ticker, state plainly that the free tier does not cover it and ask for the historicals (or a 10-K). Current price, diluted shares context, and market read: `mcp__tradingview__yahoo_price` and `combined_analysis`. Validate: net debt vs net cash, diluted share count (check recent buybacks), tax rate (21 to 28%), margins consistent with the business.

### Step 2: Analyze history
Compute revenue CAGR, gross and EBIT and FCF margins, D&A and CapEx as % of revenue, and working-capital change as % of revenue growth. These trends discipline the projection; do not assume a margin the company has never run.

### Step 3: Project revenue and margins
Revenue_t = Revenue_t-1 x (1 + growth_t). Step growth down toward the terminal rate (higher near-term visibility, moderating to the industry average by year 5). Model OpEx as % of revenue (S&M, R&D, G&A), all off revenue not gross profit, with operating leverage as the company scales. EBIT = Gross profit - OpEx. Run Bear / Base / Bull growth and margin cases; mark every assumption [ASSUMPTION] with its rationale since no live consensus feed exists.

### Step 4: Build unlevered FCF
```
EBIT
- Taxes (EBIT x tax rate)        = NOPAT
+ D&A (% of revenue, non-cash)
- CapEx (% of revenue, ~4-8%)
- Change in NWC (% of revenue change)
= Unlevered Free Cash Flow
```
A NWC increase is a use of cash (positive subtracts); a release is a source.

### Step 5: WACC (CAPM)
- Cost of equity = Rf + Beta x ERP. Pull Rf (current 10Y Treasury) via WebSearch and cite it. Beta from WebSearch (5Y monthly) or, if not found, mark [ASSUMPTION] with the value used. State the ERP explicitly (5.0 to 6.0%).
- After-tax cost of debt = pre-tax cost of debt x (1 - tax rate); derive pre-tax from interest expense / total debt or a credit-based estimate.
- Weights at market: Equity weight = Mkt cap / EV, Debt weight = Net debt / EV. WACC = Ke x We + Kd_after-tax x Wd. Net cash makes the debt weight negative; if no debt, WACC = Ke.
- Sanity: large-cap stable 7 to 9%, growth 9 to 12%, high-growth 12 to 15%.

### Step 6: Discount and terminal value
Mid-year convention: discount periods 0.5, 1.5, 2.5, ... ; discount factor = 1 / (1 + WACC)^period; PV of FCF = FCF x factor.
- Gordon growth (primary): Terminal value = FCF_final x (1 + g) / (WACC - g). Constraint: g < WACC, and g <= long-term GDP / risk-free (2.0 to 3.0% conservative). PV of TV = TV / (1 + WACC)^final period.
- Exit multiple (cross-check): TV = EBITDA_final x exit multiple (peer-driven, ~8 to 15x). Reconcile the two methods.
- Sanity: terminal value should be 50 to 70% of EV. Above 75% means too terminal-reliant; below 40% means terminal assumptions may be too low.

### Step 7: Equity bridge and price anchor
```
Sum of PV(FCF) + PV(Terminal value) = Enterprise value
- Net debt (or + net cash)           = Equity value
/ Diluted shares                      = Implied value per share
```
Place implied value beside the current price from `yahoo_price`; implied upside = implied / current - 1. Then translate: entry zone (a discount to fair value, ideally near EMA20 or EMA50 support), a stop (below structure), and a first target. Do not chase if `combined_analysis` shows the name overextended (RSI > 70, above upper Bollinger, > 5% over the 20 SMA); wait for the pullback. Treat heavy retail dip-buying as a contrarian caution.

### Step 8: Sensitivity
Build a 5x5 (or 7x7) WACC x terminal-growth grid. Axes symmetric around the base case (`[base-2d, base-d, base, base+d, base+2d]`), so the center cell equals the model's own implied value; that equality is the proof the grid is wired right. Highlight the center. Every cell is a full recompute, not a linear approximation; each cell differs. Optionally add a second grid on revenue growth x EBIT margin.

## Output

Markdown by default:
1. Inputs and historicals block, each figure cited.
2. Projection table: revenue, growth, margins, FCF build, by year (Bear/Base/Bull).
3. WACC build with each input sourced.
4. Terminal value both methods, EV-to-equity bridge, implied value vs current price.
5. Entry / stop / target translation.
6. Sensitivity grid(s) with the base case centered and highlighted.

On request, write a headless `.xlsx` to `./out/` via python openpyxl: formula strings (`ws["D20"] = "=D19*(1+$B$8)"`), blue font for inputs, black for formulas, cell comments citing every hardcode, sensitivity cells written by loop. No Excel add-in.

## Data and limits

- Free-tier historicals: AAPL, GOOGL, NVDA, TSLA only. Anything else needs user-supplied financials; do not invent line items.
- No live consensus, no analyst price targets in this stack; every estimate is [ASSUMPTION].
- Troubleshooting: implied value too high, check TV is not >80% of EV and g < WACC; too low, recheck net debt sign and that WACC is not overstated. Guard divisions (`=IF(div=0,0,num/div)`).
- Flag every data gap. Not financial advice.
