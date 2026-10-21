---
name: comps-analysis
description: Build a peer trading-multiples spread (EV/EBITDA, EV/Sales, P/E, P/FCF) with consistent metric definitions, summary stats, and outlier flags. Triggers on "comps", "trading comps", "comparable company analysis", "peer multiples", "comp spread". Free-tier fundamentals cover AAPL, GOOGL, NVDA, TSLA only; other peers get a price but no statement-based multiples.
---

# Comparable Company Analysis

Build the right structure first, then let the data tell the story. Every multiple is derived from a cited input, every metric is defined the same way across the peer set, and the statistics fall out automatically. A reader who did not build it should be able to read it.

## Workflow

### Step 1: Scope the peer set
Confirm the target and the 4 to 10 comparables. Drop names that are not truly comparable (different business model, distressed, pre-revenue); a smaller clean set beats a forced one. Note the period (LTM or last fiscal year) and the unit (USD millions) so every column is apples to apples.

### Step 2: Pull the raw inputs
For each peer:
- Current price, shares, market context: `mcp__tradingview__yahoo_price`.
- For a covered ticker (AAPL, GOOGL, NVDA, TSLA): revenue, gross profit, EBITDA, net income, FCF from `mcp__financial-datasets__get_income_statements` and `get_cash_flow_statements`; cash and total debt from `get_balance_sheets`.
- For any other peer: take the price from `yahoo_price`, then flag that statement-based multiples are unavailable on the free tier and ask the user to supply revenue, EBITDA, net income, FCF, net debt, and shares. Do not invent the statement line items.
Cite each input next to the cell. A hardcoded figure with no source gets [ASSUMPTION] or [UNSOURCED].

### Step 3: Build operating metrics (consistent definitions)
Same formula for every peer, or the spread is meaningless:
- Gross margin = Gross profit / Revenue
- EBITDA margin = EBITDA / Revenue
- FCF margin = FCF / Revenue
- Revenue growth = Revenue_t / Revenue_t-1 - 1
Show the arithmetic, never a typed margin.

### Step 4: Build valuation multiples
- Net debt = Total debt - Cash and equivalents (negative = net cash).
- Enterprise value = Market cap + Net debt, where Market cap = Price x Diluted shares.
- EV/Sales = EV / Revenue
- EV/EBITDA = EV / EBITDA
- P/E = Price / Diluted EPS (or Market cap / Net income)
- P/FCF = Market cap / FCF
Multiples reference the operating block; never re-enter revenue twice. Use IFERROR-style guards so a negative or zero denominator reads N/A, not a junk number. Flag negative-EBITDA or negative-FCF names; their multiples are not meaningful.

### Step 5: Summary statistics and outliers
For every comparable metric (margins, growth, each multiple) compute min, 25th percentile, median, mean, 75th percentile, max. Statistics belong on ratios and multiples, not on absolute size (revenue, market cap, EV). Flag any peer more than ~1.5x the median or below ~0.5x as a high or low outlier and say why in one line (faster growth, distressed, different mix). The 75th-percentile multiple is what the market pays for premium names; the median anchors a fair-value read.

### Step 6: Anchor to a price
For the target, place its current price (`yahoo_price`) beside the peer-median implied value (median multiple x the target's own metric). State the gap, then translate into an entry zone, a stop, and a first target. If `combined_analysis` flags the target as overextended (RSI > 70, above upper Bollinger, > 5% over the 20 SMA), say wait for an EMA20 or EMA50 pullback rather than chase. Heavy retail dip-buying in `market_sentiment` is a contrarian caution, not confirmation.

## Output

A markdown comps spread:
1. Header: title, peer list with tickers, "As of [date], USD millions except per-share and ratios."
2. Operating metrics table: Company | Revenue | Rev growth | Gross margin | EBITDA margin | FCF margin.
3. Valuation table: Company | Mkt cap | Net debt | EV | EV/Sales | EV/EBITDA | P/E | P/FCF.
4. Statistics block under each table: Min / 25th / Median / Mean / 75th / Max.
5. Outlier notes and the target's price-vs-peer-implied read with entry, stop, target.
6. Methodology note: data sources per peer, period, EBITDA and FCF definitions, what was [ASSUMPTION] or unavailable.

If the user asks for a spreadsheet, write a headless `.xlsx` to `./out/` with python openpyxl, formulas not hardcodes (`cell.value = "=C7/B7"`), blue font for inputs and black for formulas. Otherwise markdown only.

## Data and limits

- Free-tier statements: AAPL, GOOGL, NVDA, TSLA only. Every other peer is price-only; request the statement inputs rather than estimate them.
- No live analyst consensus feed in this stack; forward multiples need user-supplied estimates, marked [ASSUMPTION].
- Audit before delivery: every derived cell is a formula off an input; units and period consistent across peers; statistics cover at least 5 points; no #DIV/0! or N/A junk; margins logical and multiples reasonable; date stamp current.
- Flag every data gap (price-only peers, empty news, no consensus).
- Not financial advice.
