---
name: idea-generation
description: Stock screening and idea sourcing that screens a quality large-cap universe for the best setups, with an optional filtered momentum sweep, returning a shortlist where every name carries exact entry, stop, and target levels. Use to run a screen, find new ideas, or do a thematic sweep. Triggers on "idea generation", "stock screen", "find ideas", "what looks interesting", "screen for", "new ideas", "pitch me something".
---

# Idea Generation

Surface candidates, then hand back a shortlist where every name carries a metric line and exact levels. Screens surface candidates, not conclusions; each one still needs fundamental work. Default to quality large-caps. The free movers feed skews to micro-cap and penny names, so do not let raw gainers set the agenda.

## Workflow

### Step 1: Define criteria and the universe
Confirm: direction (long, short, both), market-cap band, sector or cross-sector, style (value, growth, quality, special situation, event-driven), geography, and any thematic angle.

Then fix the universe, because the free movers feed is full of micro-cap noise:
- If the user gives a watchlist, use it.
- Otherwise default to a curated large-cap universe and say so. Starter set (edit to taste): AAPL, MSFT, GOOGL, AMZN, NVDA, META, AVGO, AMD, TSLA, NFLX, CRM, ORCL, ADBE, JPM, V, MA, UNH, LLY, JNJ, XOM, COST, WMT, HD, CAT. Add the user's holdings and any thematic names in scope.

### Step 2: Primary screen, setup quality across the universe
This is the main screen, and it works for every ticker since technicals are available market-wide even where fundamentals are not. For each universe name pull `mcp__tradingview__combined_analysis` (and `multi_timeframe_analysis` for the leaders) and rank by setup quality aligned to the house rules:
- Trend intact: price above EMA200, EMA50 above EMA200 (golden cross). Skip broken structures.
- Pullback entry, not chase: RSI roughly 40 to 60 with price near EMA20 or EMA50 support scores best. RSI above 70, or price more than 5% above the 20 SMA, is overextended and waits.
- Confirmation: volume and MACD posture support the move.
Rank the universe by this setup score and carry the top names forward.

### Step 3: Momentum sweep (optional, higher risk)
For fresh movers outside the core universe, run `mcp__tradingview__top_gainers`, `top_losers`, `rating_filter`, and `volume_breakout_scanner` on NASDAQ or NYSE. Filter hard, because this feed skews micro-cap:
- Drop names under about $10 and anything with thin volume (penny and micro-cap noise).
- Drop RSI above 70. The feed surfaces overbought names, and `rating_filter` "Strong Buy" is a Bollinger-momentum rating, not a fundamental or sell-side rating.
- Label survivors as higher-risk and smaller-cap, and size accordingly.

### Step 4: Thematic sweep
For a thematic idea: state the thesis, map the value chain (direct vs. indirect beneficiaries), separate pure-play from diversified exposure, judge what is already priced in vs. under-appreciated, and look for second-order beneficiaries the market has not connected to the theme yet.

### Step 5: Style and fundamental overlay
Apply the style cues, and for the four covered names (AAPL, GOOGL, NVDA, TSLA) confirm with `mcp__financial-datasets__*` statements:
- Value: cheap multiples, FCF yield above 5%, insider buying.
- Growth: revenue above 15% and earnings above 20% YoY with acceleration, expanding margins.
- Quality: 5-plus years of consistent growth, ROE above 15%, low debt, high FCF conversion.
- Short: decelerating revenue, margin compression, receivables or inventory rising vs. sales, premium valuation without justification, accounting red flags.
For names outside the covered four, fundamentals are not on the free tier; request inputs rather than invent them.

### Step 6: Validate and build the shortlist
Before a name makes the list, re-check the house rules: no rally chasing (overextended longs wait for an EMA20/50 pullback), no falling knives (a name in freefall needs basing or a resistance reclaim), retail dip-buying in `market_sentiment` is a contrarian caution, avoid crowded trades. Short ideas need higher conviction.

For each surviving name, one line of metrics plus exact levels:

**[TICKER] - [Long/Short] - [one-line thesis hook]** | metric or setup line | Entry [zone], Stop [level], Target 1 [level] | confidence and the catalyst.

## Output

A shortlist of 5 to 10 names in the format above, with the universe, criteria, and tools stated up top, and a prioritized "research first" order. Contrarian names without a catalyst get downgraded; early without a catalyst is the same as wrong. End with: Not financial advice.

## Data and limits

Primary screen uses `mcp__tradingview__combined_analysis` and `multi_timeframe_analysis` across the universe (works for any ticker). Momentum sweep uses `mcp__tradingview__{top_gainers, top_losers, rating_filter, volume_breakout_scanner, smart_volume_scanner, bollinger_scan}`, which on the free feed skew to micro-cap and penny movers, so filter by price, volume, and RSI. Fundamentals via `mcp__financial-datasets__*` cover AAPL, GOOGL, NVDA, TSLA only. Cannot source: live sell-side consensus or price targets, options flow, short-interest feeds, insider-transaction feeds. Flag every data gap on the shortlist.
