---
name: 3-statement-model
description: Build an integrated three-statement model linking the income statement, balance sheet, and cash flow through working-capital and debt schedules, with full balance and cash-tie checks. Triggers on "3-statement", "three statement model", "integrated model", "build a financial model", "link the statements". Free-tier historicals cover AAPL, GOOGL, NVDA, TSLA only, other tickers need user-supplied financials.
---

# Three-Statement Model Builder

The three statements are one system: net income flows to the cash flow and to retained earnings, the cash flow rebuilds the balance sheet, and the balance sheet must balance. If it does not balance, the model is wrong; do not paper over it with a plug. Every projected cell is derived from a stated driver.

## Workflow

### Step 1: Pull historicals
For AAPL, GOOGL, NVDA, TSLA: pull 3 years from `mcp__financial-datasets__get_income_statements`, `get_balance_sheets`, `get_cash_flow_statements`, and `get_sec_filings`. For any other ticker, state that the free tier does not cover it and ask for the statements (or a 10-K). Lay the three statements side by side for the historical years and confirm they already tie before projecting.

### Step 2: Driver and assumptions block
One block of explicit drivers, each [ASSUMPTION] with rationale from history: revenue growth, gross margin, OpEx as % of revenue, D&A as % of PP&E or revenue, CapEx as % of revenue, working-capital days (DSO, DIO, DPO), tax rate, dividend and buyback policy, and debt terms. Projections read only from here. No number is typed into a statement cell that a driver should produce.

### Step 3: Income statement
Revenue (driver) to COGS (margin) to Gross profit to OpEx (% of revenue) to EBIT to Interest (from the debt schedule, Step 6) to EBT to Taxes (rate, with the NOL schedule) to Net income. Interest links to the debt schedule, which is the source of circularity; handle it with beginning-of-period balances (Step 6).

### Step 4: Supporting schedules
- Working capital: AR = DSO/365 x revenue, Inventory = DIO/365 x COGS, AP = DPO/365 x COGS. Change in NWC feeds the cash flow.
- PP&E and D&A: ending PP&E = beginning + CapEx minus D&A.
- Equity and retained earnings: ending RE = beginning RE + net income minus dividends. Track buybacks against the share count.

### Step 5: Cash flow statement
- CFO = net income + D&A minus the increase in NWC (a working-capital build is a use of cash).
- CFI = minus CapEx (plus any disposals).
- CFF = debt drawn minus debt repaid + equity issued minus dividends and buybacks.
- Net change in cash = CFO + CFI + CFF. Ending cash = beginning cash + net change, and this ending cash is what lands on the balance sheet.

### Step 6: Debt and interest (break the circularity)
Beginning balance minus mandatory repayment plus draws = ending balance. Interest = beginning balance x rate (beginning, not average, so interest does not depend on a cash balance that depends on interest). A revolver draws when minimum cash is breached and sweeps when there is excess. If you choose average-balance interest, enable iterative calculation deliberately and say so.

### Step 7: Balance and tie checks (the proof the model is right)
- Balance sheet balances: total assets = total liabilities + equity, every year. Show the difference row; it must be zero.
- Cash ties: cash on the balance sheet equals ending cash from the cash flow.
- Net income links: the same net income appears on the IS, the top of CFO, and the RE roll-forward.
- Retained earnings rolls forward: prior RE + NI minus dividends.
- NOL schedule: carry losses forward; post-2017 US NOLs offset at most 80% of taxable income in a year. Apply the limitation; do not zero out taxes with a full offset.

### Step 8: Anchor and read
Pull the current price from `mcp__tradingview__yahoo_price` and posture from `combined_analysis`. The model is the engine for a DCF or a comps read; hand the projected FCF to the `dcf-model` skill for a value, then translate to entry, stop, and target. Do not chase if the name is overextended (RSI > 70, above the upper Bollinger band, > 5% over the 20 SMA).

## Output

Markdown by default:
1. Driver and assumptions block, each cited.
2. Income statement, historical and projected.
3. Balance sheet, with the balance-check row (zeros).
4. Cash flow statement, with the cash tie-out.
5. Supporting schedules: working capital, PP&E and D&A, debt, NOL and taxes.
6. A checks panel: balances, cash ties, RE roll-forward, all passing.

On request, write a headless `.xlsx` to `./out/` via python openpyxl: linked formula strings across tabs, blue inputs and black formulas, a Checks tab of TRUE/FALSE ties. No Excel add-in.

## Data and limits

- Free-tier historicals: AAPL, GOOGL, NVDA, TSLA only. Other tickers need user-supplied statements; do not invent line items.
- No consensus feed; every forward driver is [ASSUMPTION], disciplined by the historicals.
- If the balance sheet does not balance, stop and find the break (usually a sign error in NWC, a missing CFF line, or interest wired to ending instead of beginning balances). Never hide it with a plug.
- Flag every data gap. Not financial advice.
