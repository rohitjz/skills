---
name: thesis-tracker
description: Define or load an investment thesis (statement, pillars, risks, catalysts, target, stop), keep an update log, and produce a scorecard. Persists each thesis to a local file so it carries across sessions. Use to start a thesis, log a development, or check if a thesis still holds. Triggers on "update thesis for X", "is my thesis still intact", "thesis check", "add data point to X", "review my positions".
---

# Thesis Tracker

Maintain falsifiable investment theses across sessions. A thesis nothing could disprove is not a thesis. Track disconfirming evidence as hard as confirming evidence.

## Workflow

### Step 1: Define or load

Each thesis lives at `./theses/<TICKER>.md` (create the `./theses/` folder if missing). On any request, check that path first.

If it exists, read it and load the statement, pillars, risks, catalysts, target, stop, and prior log before doing anything else.

If it does not exist, build a new one. Capture: company and ticker; position (long or short); a 1 to 2 sentence thesis statement (e.g., "Long ACME, margin expansion from pricing power plus operating leverage as mix shifts to software"); 3 to 5 supporting pillars, each written so it can be checked against reality; 3 to 5 risks that would invalidate it; catalysts (earnings, launches, regulatory dates) that prove or disprove it; a target price if it plays out; and a stop that defines the exit. Write it to the file using the Output template.

### Step 2: Score against the tape

Pull current price with `mcp__tradingview__yahoo_price` and technical posture with `mcp__tradingview__combined_analysis`. Use them to mark where price sits vs. target and stop, and whether posture supports or fights the thesis. If the position is long and the name is overextended (RSI above 70, above the upper Bollinger band, or more than 5% above the 20 SMA), note it is stretched and not an add-here; an EMA20 or EMA50 pullback is the better add. If price has broken the stop, say so plainly; the thesis is on exit watch regardless of the narrative.

### Step 3: Log the update

For each new development, append a row: date; data point (earnings beat, management departure, competitor move, price through a level); thesis impact (strengthens, weakens, or neutralizes a named pillar); action (no change / add / trim / exit); updated conviction (high / medium / low). Heavy Reddit dip-buying read off `market_sentiment` is a caution flag, not support.

### Step 4: Scorecard

Maintain a running table: pillar, original expectation, current status, trend (stable / improving / concerning). One row per pillar so intact and broken pieces are both visible at a glance.

### Step 5: Persist and report

Write the updated thesis, log, and scorecard back to `./theses/<TICKER>.md`. Return a concise summary fit for a portfolio review: thesis line, price vs. target and stop, scorecard, latest updates, current conviction.

## Output

The persisted file at `./theses/<TICKER>.md`:

```
# <TICKER> Thesis (Long|Short) - updated <date>
Statement: ...
Pillars: 1) ... 2) ... 3) ...
Risks: 1) ... 2) ... 3) ...
Catalysts: <date> <event>; ...
Levels: Entry <zone> | Stop <level> | Target <level>
Current: price <px from yahoo_price>, posture <combined_analysis read>

## Update log
| Date | Data point | Thesis impact | Action | Conviction |

## Scorecard
| Pillar | Original expectation | Current status | Trend |
```

End with: Not financial advice.

## Data and limits

Uses `mcp__tradingview__yahoo_price` for current price, `combined_analysis` for posture, and `market_sentiment` for the retail read. Persists to `./theses/<TICKER>.md`. Cannot source: live sell-side consensus or price targets, options flow, real-time fundamentals beyond the covered four (AAPL, GOOGL, NVDA, TSLA via `mcp__financial-datasets__*`). Review theses at least quarterly even when nothing dramatic happened. Flag every data gap in the report.
