---
name: earnings-analysis
description: Post-earnings update note for a single name already under coverage. Leads with beat or miss, reads the quarter against trend, layers segment and margin detail, guidance, and the technical reaction with exact levels, then a verdict (rating, 12-month target, entry zone, stop). Triggers on "earnings", "earnings update", "quarterly results", "earnings review", "Q1/Q2/Q3/Q4 results", "post-earnings", "earnings analysis". Runs on the free stack (TradingView plus Financial Datasets); live sell-side consensus is unavailable and gets flagged.
---

# Earnings Update Note

Produce a tight, fast-turnaround earnings note for a name the reader already knows. Focus on what is new: the print, the drivers, guidance, the chart reaction, and whether the thesis still holds. Default output is a markdown note. Offer a DOCX export only if the user asks.

## Workflow

### Step 1: Timeliness gate (do this first, do not skip)
Training data is stale; the latest quarter is almost never the one you remember. Confirm the current quarter before any analysis.
- Note today's date explicitly.
- WebSearch `[ticker] latest earnings results` and `[company] most recent quarterly earnings`. For AAPL, GOOGL, NVDA, or TSLA, also call `mcp__financial-datasets__get_company_news` to confirm the release.
- Read the actual release date. It must be within roughly 3 months of today. If it is older, you have the wrong quarter; search again.
- Confirm the fiscal calendar (Apple, Nike, and others do not run on calendar quarters) so you label the period correctly.
- State the quarter and release date in the note. If you cannot confirm a release within 3 months, say so and stop rather than analyze a stale print.

### Step 2: Pull the print
- For AAPL, GOOGL, NVDA, TSLA: `mcp__financial-datasets__get_income_statements` and `get_balance_sheets` and `get_cash_flow_statements` (quarterly) for the reported quarter plus the prior four, and `get_sec_filings` for the 10-Q or 10-K.
- For any other ticker: the free tier does not cover statements. Pull what you can from WebSearch on the earnings release and request the reported figures from the user rather than inventing them. Mark every number you could not source as a gap.
- Record revenue, gross and operating margin, EPS, and the two or three operating metrics that matter for this name (units, ARPU, cloud growth, deliveries, store count, whatever the company leads with).

### Step 3: Read the quarter against trend
- Compute YoY and sequential (QoQ) change on every headline line and key metric.
- Beat or miss leads. There is no free live consensus feed, so do not fabricate estimate numbers. Use `mcp__tradingview__rating_filter` and `mcp__tradingview__market_sentiment` as a rough proxy for where the Street sat, and state plainly that this is a sentiment proxy, not a sell-side consensus print. Frame the result against the prior trend and guidance instead of against a fabricated estimate.
- Explain WHY the line moved, not just that it did. "Strong" means nothing; "data-center revenue up 34% QoQ on H200 ramp" is the read.

### Step 4: Guidance and call read
- Pull guidance from the release and WebSearch the call transcript. Note whether it was raised, cut, maintained, or newly introduced, and against what prior bar.
- Read management tone (confident, hedging, defensive) and what analysts pressed on. If no guidance was given, say so explicitly.

### Step 5: Technical reaction read with exact levels
- Call `mcp__tradingview__yahoo_price`, `mcp__tradingview__combined_analysis`, and `mcp__tradingview__multi_timeframe_analysis`; for the four covered names you can add `mcp__financial-datasets__get_historical_stock_prices`.
- Describe the post-print chart in prose: where price sits versus EMA20, EMA50, the 20 SMA, and the Bollinger bands; how the gap (if any) is being held or filled; volume on the move. Do not generate image files.
- Apply the house overextension check. If the print is good but the stock is RSI > 70, above the upper Bollinger band, or more than 5% above the 20 SMA, do not chase the rally. Call for an EMA20 or EMA50 pullback as the entry. If the stock is in freefall on the print, wait for basing or a resistance reclaim; no falling knives. Heavy retail dip-buying in `market_sentiment` is a contrarian caution flag, not confirmation.

### Step 6: Verify before writing
- Dates align: release within 3 months, transcript matches the release, filing is the same quarter.
- Every number traces to a tool call, a filing, or a user-supplied figure; anything else is marked a gap.
- The math checks: variances, YoY, QoQ all tie.
- The verdict carries all four numbers (rating, target, entry, stop), not just a direction.

## Output

A markdown note, roughly 1 to 2 pages, in this order:
1. **Header.** Ticker, company, quarter, release date, today's date. One line: rating (maintain / raise / cut), price now, 12-month target, entry zone, stop.
2. **Headline takeaways.** Three bullets. Beat or miss first, then the single most important driver, then the thesis call.
3. **The print vs. expectations.** A small table: reported, YoY, QoQ for revenue, gross margin, operating margin, EPS, and the key operating metrics. Beat/miss framed against the sentiment proxy with the no-consensus gap flagged. Each row sourced.
4. **Segment and margin read.** What drove the top line by segment or geography; what moved gross and operating margin and why.
5. **Guidance.** Raised / cut / maintained / none, against the prior bar, with the call tone in a sentence.
6. **Technical reaction.** The prose chart read with exact levels (EMA20, EMA50, 20 SMA, Bollinger, gap, volume) and the overextension or falling-knife verdict.
7. **Verdict.** Rating with a one-paragraph rationale, the 12-month target with method, the entry zone, and the stop. State what would change the call.
8. **Data gaps.** What you could not source.
9. _Not financial advice._

## Data and limits
- Free stack only. No paid consensus, no Bloomberg, no FactSet. `rating_filter` and `market_sentiment` are a sentiment proxy for the Street, flagged as such; never present them as a sell-side estimate.
- Statement-level fundamentals exist only for AAPL, GOOGL, NVDA, TSLA. Every other ticker gets price and technicals from TradingView plus whatever the user supplies from the release; do not invent statement numbers.
- No options flow, no live institutional positioning.
- Flag empty news feeds, free-tier ticker limits, and any number you could not source, every time.
- This note covers a name already under coverage. For a first-time write-up, use the initiating-coverage skill or /initiate. For a sector primer, use the market-researcher agent.
