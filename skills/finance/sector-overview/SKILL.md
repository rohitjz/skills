---
name: sector-overview
description: Industry and sector primer covering market size, growth, segmentation, structure, drivers, top players, sector multiples, and investment implications. Use for sector initiations, thematic pieces, or a landscape read before single-name work. Triggers on "sector overview", "industry report", "market landscape", "sector analysis", "industry deep dive", "thematic research".
---

# Sector Overview

Build a sector or thematic primer on a free data stack. Be explicit about what you can and cannot source. Sector reads age fast, so stamp the date and flag anything that may be stale.

## Workflow

### Step 1: Scope

Pin down before research: sector or subsector and how narrowly drawn; purpose (idea sourcing, primer, pitch); depth (quick read or deep dive); angle (neutral landscape vs. a thesis like "AI infrastructure buildout"); universe boundary. Name the 8 to 15 public companies that define the space.

### Step 2: Market overview

Size and growth: TAM with a cited source, 5-year historical CAGR, forecast growth and the assumptions behind it, segmentation (product, geography, end market, customer type). Source every market-size figure from WebSearch and cite the firm or methodology. Distinguish real addressable market from TAM hype. Mark any figure you cannot source as [UNSOURCED] rather than estimating.

Structure: fragmented vs. consolidated (top-5 share), value-chain map and where margin accrues, business-model types (subscription, transaction, licensing, services), barriers to entry (capital, regulatory, technical, network effects).

Drivers: 3 to 5 secular tailwinds, the headwinds and risks against them, technology disruption vectors, regulatory shifts, M&A and consolidation activity.

### Step 3: Movers and named-stock context

Pull the live tape with `mcp__tradingview__top_gainers` and `top_losers` to see what is leading and lagging in the space right now. For each named company that matters, pull `mcp__tradingview__combined_analysis` for price posture and technical read. Note who is gaining or losing and why.

### Step 4: Competitive landscape

For the top 5 to 10 players, a compact table: company, revenue, growth, margin, rough market share, key differentiator. For each, two or three sentences on the business, its positioning and moat, recent developments, and a valuation snapshot. Then competitive dynamics: how they compete (price, product, service, distribution), who is taking share, and disruption risk from new entrants or adjacents.

### Step 5: Valuation context

Sector trading multiples, current vs. historical range, the premium or discount drivers (growth, margins, position), recent M&A transaction multiples, and how the sector sits against the broader market. Live sell-side consensus is not available on the free stack; use `mcp__tradingview__rating_filter` and `market_sentiment` as a rough proxy and say so.

### Step 6: Investment implications

Best risk/reward spots, the thematic bets the sector can express, the key bull-vs-bear debates, and the catalysts that could change the narrative. When you flag a specific name as the way to play it, anchor it to a price: current level from `combined_analysis`, plus an entry zone, a stop, and a first target. Do not endorse a STRONG BUY that is overextended (RSI above 70, above the upper Bollinger band, or more than 5% above the 20 SMA); wait for an EMA20 or EMA50 pullback. No intraday rally chasing, no falling knives.

## Output

A structured markdown note: market overview and sizing, competitive map, company comparison table, valuation summary, investment implications. Slides only if asked. Headline sections with the insight, not the topic. End with: Not financial advice.

## Data and limits

Uses `mcp__tradingview__{top_gainers, top_losers, combined_analysis, rating_filter, market_sentiment}` for the tape, named-stock posture, and a consensus proxy; WebSearch for market-size figures (cited). Cannot source: live sell-side consensus or price targets, options flow, private-company financials. Free-tier fundamentals (`mcp__financial-datasets__*`) cover AAPL, GOOGL, NVDA, TSLA only; for other names, request inputs rather than invent. Flag every data gap (empty news, ticker limits, no consensus) in the note.
